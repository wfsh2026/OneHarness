from __future__ import annotations

import hashlib
import difflib
import json
import os
import re
import secrets
import threading
import webbrowser
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from tharness_config import config_list, config_value, load_simple_yaml, rel_path, repo_path


ROLE_TYPE_LABELS = {
    "coordinator": "协调角色",
    "infrastructure": "基础规则",
    "dispatchable": "可派发角色",
}
MATURITY_LABELS = {"draft": "草案", "contracted": "已契约", "tested": "已测试", "evaluated": "已评测"}
MATURITY_ORDER = {"evaluated": 0, "tested": 1, "contracted": 2, "draft": 3}
DOCUMENT_LABELS = {
    "rule": "角色规则",
    "skills": "技能索引",
    "tools": "工具索引",
}
MAX_RULE_BYTES = 512 * 1024
MAX_REQUEST_BYTES = MAX_RULE_BYTES * 2 + 4096
CSRF_HEADER = "X-Tharness-CSRF"
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


def _table_rows(path: Path, heading: str | None = None) -> list[list[str]]:
    if not path.exists():
        return []
    rows = []
    active = heading is None
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if heading and line == heading:
            active = True
            continue
        if active and heading and line.startswith("## "):
            break
        if not active or not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if cells and not all(set(cell) <= {"-", ":"} for cell in cells):
            rows.append(cells)
    return rows


def _capability_details(path: Path) -> dict[str, dict[str, str]]:
    details = {}
    for cells in _table_rows(path, "## 当前能力"):
        if len(cells) < 6 or cells[0] == "capability_id":
            continue
        details[cells[0]] = {
            "id": cells[0],
            "name": cells[1],
            "status": cells[2],
            "entry": cells[3],
            "version": cells[4],
            "description": cells[5],
        }
    return details


def _role_scenarios(path: Path) -> dict[str, str]:
    scenarios = {}
    for cells in _table_rows(path, "## 角色"):
        if len(cells) < 5 or cells[0] == "角色":
            continue
        entry = cells[3]
        if entry.endswith("/RULE.md"):
            scenarios[entry.removesuffix("/RULE.md")] = cells[4]
    return scenarios


def _safe_role_file(role_root: Path, slug: str, path: Path) -> Path:
    role_base = (role_root / slug).resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(role_base)
    except ValueError as exc:
        raise ValueError(f"角色文件越界: {slug}") from exc
    return resolved


@dataclass
class RoleCatalog:
    repo_root: Path
    role_root: Path
    roles: list[dict[str, Any]]
    capabilities: list[dict[str, str]]
    documents: dict[str, dict[str, Path]]
    system_version: str
    write_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def role_by_slug(self) -> dict[str, dict[str, Any]]:
        return {role["slug"]: role for role in self.roles}

    def summary(self) -> dict[str, Any]:
        return {
            "systemVersion": self.system_version,
            "counts": {
                "roles": len(self.roles),
                "dispatchable": sum(role["type"] == "dispatchable" for role in self.roles),
                "capabilities": len(self.capabilities),
            },
            "roleTypes": [
                {"id": role_type, "label": label}
                for role_type, label in ROLE_TYPE_LABELS.items()
                if any(role["type"] == role_type for role in self.roles)
            ],
            "capabilities": self.capabilities,
            "roles": self.roles,
        }

    def read_document(self, slug: str, document: str) -> dict[str, str]:
        if slug not in self.role_by_slug:
            raise KeyError("角色不存在")
        allowed = self.documents.get(slug, {})
        if document not in allowed:
            raise KeyError("该角色没有此文档")
        path = _safe_role_file(self.role_root, slug, allowed[document])
        if not path.is_file():
            raise FileNotFoundError(f"角色文档不存在: {rel_path(self.repo_root, path)}")
        raw = path.read_bytes()
        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError(f"角色文档不是有效 UTF-8: {rel_path(self.repo_root, path)}") from exc
        content_hash = hashlib.sha256(raw).hexdigest()
        return {
            "kind": document,
            "label": DOCUMENT_LABELS[document],
            "path": rel_path(self.repo_root, path),
            "content": content,
            "hash": content_hash,
            "version": content_hash,
        }

    def preview_rule(self, slug: str, content: object, base_hash: object) -> dict[str, Any]:
        if slug not in self.role_by_slug:
            raise KeyError("角色不存在")
        if not isinstance(content, str):
            raise ValueError("content 必须是 UTF-8 文本")
        if not isinstance(base_hash, str) or not base_hash:
            raise ValueError("baseHash 不能为空")
        if not content.strip():
            raise ValueError("角色规则不能为空")

        allowed = self.documents.get(slug, {})
        path = allowed.get("rule")
        if path is None:
            raise KeyError("该角色没有可编辑规则")
        path = _safe_role_file(self.role_root, slug, path)

        current = path.read_bytes()
        try:
            current_text = current.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("当前角色规则不是有效 UTF-8") from exc
        current_hash = hashlib.sha256(current).hexdigest()
        if current_hash != base_hash:
            raise RuleConflictError(current_hash)
        diff = "\n".join(difflib.unified_diff(
            current_text.splitlines(), content.splitlines(),
            fromfile=rel_path(self.repo_root, path), tofile=rel_path(self.repo_root, path), lineterm="",
        ))
        role = self.role_by_slug[slug]
        impacts = [role["ruleEntry"], "AIGC/roles/INDEX.md", "AIGC/capabilities/registry.yaml"]
        if role.get("routeEntry"):
            impacts.append(role["routeEntry"])
        return {
            "diff": diff,
            "changed": bool(diff),
            "affectedEntries": impacts,
            "versionPolicy": "按 AIGC/roles/tharness-maintainer/skills/versioning.md 判断版本并更新能力记录",
            "selfCheckPlan": ["python tools\\tharness.py registry", "python tools\\tharness.py check", "python tools\\tharness.py eval"],
        }

    def save_rule(self, slug: str, content: object, base_hash: object, maintenance_mode: object, acknowledge_impact: object) -> dict[str, Any]:
        if maintenance_mode is not True or acknowledge_impact is not True:
            raise ValueError("保存前必须进入维护模式、预览差异并确认影响范围")
        preview = self.preview_rule(slug, content, base_hash)
        path = self.documents[slug]["rule"]
        with self.write_lock:
            current = path.read_bytes()
            current_hash = hashlib.sha256(current).hexdigest()
            if current_hash != base_hash:
                raise RuleConflictError(current_hash)

            newline = "\r\n" if b"\r\n" in current else "\n"
            normalized = content.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)
            bom = b"\xef\xbb\xbf" if current.startswith(b"\xef\xbb\xbf") else b""
            encoded = bom + normalized.encode("utf-8")
            if len(encoded) > MAX_RULE_BYTES:
                raise ValueError(f"角色规则超过 {MAX_RULE_BYTES} 字节限制")

            temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
            try:
                with temporary.open("xb") as stream:
                    stream.write(encoded)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
            finally:
                if temporary.exists():
                    temporary.unlink()

            saved_hash = hashlib.sha256(encoded).hexdigest()
            return {
                "kind": "rule",
                "label": DOCUMENT_LABELS["rule"],
                "path": rel_path(self.repo_root, path),
                "content": normalized,
                "hash": saved_hash,
                "version": saved_hash,
                "maintenance": preview,
            }


class RuleConflictError(Exception):
    def __init__(self, current_hash: str) -> None:
        super().__init__("角色规则已被其他进程修改，请重新加载后再编辑")
        self.current_hash = current_hash


def load_role_catalog(repo_root: Path, config: dict) -> RoleCatalog:
    registry_path = repo_path(repo_root, config_value(config, "capability_registry_file"))
    role_index_path = repo_path(repo_root, config_value(config, "role_index_file"))
    capability_index_path = repo_path(repo_root, config_value(config, "capability_index_file"))
    role_root = repo_path(repo_root, config_value(config, "role_root"))
    registry = load_simple_yaml(registry_path)
    capability_details = _capability_details(capability_index_path)
    capability_index_text = capability_index_path.read_text(encoding="utf-8-sig")
    version_match = re.search(r"当前系统版本：`([^`]+)`", capability_index_text)
    system_version = version_match.group(1) if version_match else "unknown"
    scenarios = _role_scenarios(role_index_path)

    capabilities = []
    for raw in config_list(registry, "capability_registry"):
        fields = [field.strip() for field in raw.split("|")]
        if len(fields) != 8 or not all(fields):
            raise ValueError(f"机器注册源能力格式错误: {raw}")
        capability_id = fields[0]
        detail = capability_details.get(capability_id)
        if detail is None:
            raise ValueError(f"能力索引缺少机器注册能力: {capability_id}")
        capabilities.append(detail)

    roles = []
    documents: dict[str, dict[str, Path]] = {}
    for raw in config_list(registry, "role_registry"):
        fields = [field.strip() for field in raw.split("|")]
        if len(fields) != 11 or not all(fields):
            raise ValueError(f"机器注册源角色格式错误: {raw}")
        slug, display_name, rule_entry, route_entry, capability_id, role_type, maturity, owner, contract_status, eval_suite, deprecated_by = fields
        if role_type not in ROLE_TYPE_LABELS:
            raise ValueError(f"未知角色类型: {slug} -> {role_type}")
        if any(role["slug"] == slug for role in roles):
            raise ValueError(f"机器注册源角色重复: {slug}")
        if maturity not in MATURITY_LABELS or contract_status not in MATURITY_LABELS:
            raise ValueError(f"角色成熟度无效: {slug} -> {maturity}/{contract_status}")

        rule_path = _safe_role_file(role_root, slug, repo_path(repo_root, rule_entry))
        role_documents = {"rule": rule_path}
        for document, relative in (("skills", "skills/INDEX.md"), ("tools", "tools/INDEX.md")):
            candidate = _safe_role_file(role_root, slug, role_root / slug / relative)
            if candidate.is_file():
                role_documents[document] = candidate
        documents[slug] = role_documents

        capability = capability_details.get(capability_id) if capability_id != "-" else None
        roles.append({
            "slug": slug,
            "displayName": display_name,
            "type": role_type,
            "typeLabel": ROLE_TYPE_LABELS[role_type],
            "maturity": maturity,
            "maturityLabel": MATURITY_LABELS[maturity],
            "owner": owner,
            "contractStatus": contract_status,
            "evalSuite": None if eval_suite == "-" else eval_suite,
            "deprecatedBy": None if deprecated_by == "-" else deprecated_by,
            "capabilityId": capability_id if capability else None,
            "capabilityName": capability["name"] if capability else "未绑定独立能力",
            "capabilityDescription": capability["description"] if capability else "该入口提供共享执行规则，不作为独立业务能力派发。",
            "ruleEntry": rel_path(repo_root, rule_path),
            "routeEntry": route_entry if route_entry != "-" else None,
            "scenario": scenarios.get(slug, capability["description"] if capability else "由其他角色规则共同引用。"),
            "documents": [
                {"kind": key, "label": DOCUMENT_LABELS[key], "path": rel_path(repo_root, path)}
                for key, path in role_documents.items()
            ],
        })

    if not any(role["slug"] == "role-manager" for role in roles):
        raise ValueError("机器注册源缺少角色管理员")
    roles.sort(key=lambda role: (role["slug"] != "role-manager", MATURITY_ORDER[role["maturity"]], role["displayName"]))
    capabilities.sort(key=lambda capability: capability["name"])
    return RoleCatalog(repo_root, role_root, roles, capabilities, documents, system_version)


def create_role_browser_server(
    repo_root: Path,
    config: dict,
    port: int = 0,
    static_root: Path | None = None,
) -> ThreadingHTTPServer:
    if port < 0 or port > 65535:
        raise ValueError("端口必须在 0 到 65535 之间")
    catalog = load_role_catalog(repo_root, config)
    assets = static_root or repo_root / "tools" / "role-browser"
    csrf_token = secrets.token_urlsafe(32)

    class RoleBrowserHandler(BaseHTTPRequestHandler):
        server_version = "TharnessRoleBrowser/1.0"

        def _headers(self, status: int, content_type: str, content_length: int) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(content_length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
                "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
            )
            self.end_headers()

        def _send_bytes(self, status: int, content_type: str, payload: bytes) -> None:
            self._headers(status, content_type, len(payload))
            self.wfile.write(payload)

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            self._send_bytes(
                status,
                "application/json; charset=utf-8",
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            )

        def _expected_origin(self) -> str:
            return f"http://127.0.0.1:{self.server.server_address[1]}"

        def _valid_host(self) -> bool:
            return self.headers.get("Host", "") == self._expected_origin().removeprefix("http://")

        def _document_route(self, path: str) -> tuple[str, str] | None:
            parts = path.strip("/").split("/")
            if len(parts) == 5 and parts[:2] == ["api", "roles"] and parts[3] == "documents":
                return parts[2], parts[4]
            return None

        def do_GET(self) -> None:  # noqa: N802
            if not self._valid_host():
                self._send_json(403, {"error": "Host 校验失败"})
                return
            path = unquote(urlparse(self.path).path)
            if path == "/api/summary":
                summary = catalog.summary()
                summary["csrfToken"] = csrf_token
                self._send_json(200, summary)
                return
            if path.startswith("/api/roles/"):
                route = self._document_route(path)
                if route is None:
                    self._send_json(404, {"error": "接口不存在"})
                    return
                try:
                    self._send_json(200, catalog.read_document(*route))
                except KeyError as exc:
                    self._send_json(404, {"error": str(exc.args[0])})
                except (FileNotFoundError, ValueError) as exc:
                    self._send_json(400, {"error": str(exc)})
                return
            if path in STATIC_FILES:
                filename, content_type = STATIC_FILES[path]
                target = assets / filename
                if not target.is_file():
                    self._send_json(500, {"error": f"静态资源缺失: {filename}"})
                    return
                self._send_bytes(200, content_type, target.read_bytes())
                return
            self._send_json(404, {"error": "页面不存在"})

        def do_PUT(self) -> None:  # noqa: N802
            if not self._valid_host():
                self._send_json(403, {"error": "Host 校验失败"})
                return
            if self.headers.get("Origin") != self._expected_origin():
                self._send_json(403, {"error": "Origin 校验失败"})
                return
            if self.headers.get(CSRF_HEADER) != csrf_token:
                self._send_json(403, {"error": "CSRF 校验失败"})
                return
            if self.headers.get_content_type() != "application/json":
                self._send_json(415, {"error": "只接受 application/json"})
                return
            path = unquote(urlparse(self.path).path)
            route = self._document_route(path)
            if route is None:
                self._send_json(404, {"error": "接口不存在"})
                return
            slug, document = route
            if document != "rule":
                self._send_json(405, {"error": "只有已注册角色的 RULE.md 可编辑"})
                return
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send_json(400, {"error": "Content-Length 无效"})
                return
            if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
                self._send_json(413, {"error": "请求内容为空或过大"})
                return
            raw = self.rfile.read(content_length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json(400, {"error": "请求必须是有效 UTF-8 JSON"})
                return
            if not isinstance(payload, dict):
                self._send_json(400, {"error": "JSON 根节点必须是对象"})
                return
            try:
                if payload.get("previewOnly") is True:
                    self._send_json(200, catalog.preview_rule(slug, payload.get("content"), payload.get("baseHash")))
                    return
                saved = catalog.save_rule(
                    slug, payload.get("content"), payload.get("baseHash"),
                    payload.get("maintenanceMode"), payload.get("acknowledgeImpact"),
                )
                self._send_json(200, saved)
            except RuleConflictError as exc:
                self._send_json(409, {"error": str(exc), "currentHash": exc.current_hash})
            except KeyError as exc:
                self._send_json(404, {"error": str(exc.args[0])})
            except (FileNotFoundError, ValueError, OSError) as exc:
                self._send_json(400, {"error": str(exc)})

        def do_POST(self) -> None:  # noqa: N802
            self._send_json(405, {"error": "只读工具不支持写请求"})

        def log_message(self, format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer(("127.0.0.1", port), RoleBrowserHandler)


def open_browser_or_warn(url: str) -> bool:
    try:
        opened = bool(webbrowser.open(url))
    except Exception as exc:  # Browser discovery is platform-owned and optional.
        print(f"提示：无法自动打开浏览器（{exc}）。请手动打开：{url}")
        return False
    if not opened:
        print(f"提示：系统未接受自动打开浏览器请求，请手动打开：{url}")
    return opened


def run_roles_ui_command(repo_root: Path, config: dict, port: int, no_open: bool) -> int:
    try:
        server = create_role_browser_server(repo_root, config, port)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"错误: 无法启动角色浏览器: {exc}")
        return 2

    address, selected_port = server.server_address
    url = f"http://{address}:{selected_port}/"
    print(f"roles-ui: PASS\n本地地址: {url}\n按 Ctrl+C 停止。")
    if not no_open:
        browser_timer = threading.Timer(0.15, open_browser_or_warn, args=(url,))
        browser_timer.daemon = True
        browser_timer.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n角色浏览器已停止。")
    finally:
        server.server_close()
    return 0
