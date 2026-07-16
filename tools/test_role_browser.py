from __future__ import annotations

import json
import io
import hashlib
import os
import socket
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT / "tools"))
from tharness import parse_args
from tharness_config import load_simple_yaml, repo_path
from tharness_roles_ui import MAX_RULE_BYTES, _safe_role_file, create_role_browser_server, load_role_catalog, open_browser_or_warn


class RoleBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_simple_yaml(repo_path(ROOT, "AIGC/tharness.yaml"))

    def make_editable_fixture(self, root: Path, newline: str = "\r\n") -> tuple[dict, Path]:
        role_dir = root / "aigc/roles/role-manager"
        (role_dir / "skills").mkdir(parents=True)
        (role_dir / "tools").mkdir()
        (root / "aigc/capabilities").mkdir(parents=True)
        rule_path = role_dir / "RULE.md"
        rule_path.write_bytes(b"\xef\xbb\xbf" + f"# 角色管理员规则{newline}{newline}- 初始规则{newline}".encode("utf-8"))
        (role_dir / "skills/INDEX.md").write_text("# Skills\n", encoding="utf-8")
        (role_dir / "tools/INDEX.md").write_text("# Tools\n", encoding="utf-8")
        (root / "aigc/roles/INDEX.md").write_text(
            "## 角色\n\n| 角色 | 标签 | 添加时间 | 入口 | 触发条件 |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 角色管理员 | - | now | `role-manager/RULE.md` | 所有请求 |\n",
            encoding="utf-8",
        )
        (root / "aigc/capabilities/INDEX.md").write_text(
            "## 当前能力\n\n| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| `role-dispatch` | 角色管理员调度 | active | `../roles/INDEX.md` | 1.0.0 | 所有请求 |\n",
            encoding="utf-8",
        )
        (root / "aigc/capabilities/registry.yaml").write_text(
            "role_registry:\n"
            "  - role-manager|角色管理员|AIGC/roles/role-manager/RULE.md|-|role-dispatch|coordinator|tested|tharness-core|tested|core|-\n"
            "capability_registry:\n"
            "  - role-dispatch|AIGC/roles/INDEX.md|role-manager|tested|evaluated|2026-07-16|core|-\n",
            encoding="utf-8",
        )
        config = {
            "role_root": "AIGC/roles",
            "role_index_file": "AIGC/roles/INDEX.md",
            "capability_index_file": "AIGC/capabilities/INDEX.md",
            "capability_registry_file": "AIGC/capabilities/registry.yaml",
        }
        return config, rule_path

    def test_catalog_uses_registry_and_loads_documents_on_demand(self) -> None:
        catalog = load_role_catalog(ROOT, self.config)
        summary = catalog.summary()

        self.assertEqual(summary["counts"]["roles"], 12)
        self.assertEqual(summary["systemVersion"], "6.0.0")
        self.assertGreater(summary["counts"]["dispatchable"], 0)
        self.assertGreater(summary["counts"]["capabilities"], 20)
        maturities = [role["maturity"] for role in summary["roles"]]
        self.assertEqual(summary["roles"][0]["slug"], "role-manager")
        self.assertTrue(all(maturity in {"draft", "contracted", "tested", "evaluated"} for maturity in maturities))
        self.assertNotIn("intern-ui-developer", catalog.role_by_slug)
        role = catalog.role_by_slug["tharness-maintainer"]
        self.assertEqual(role["capabilityId"], "capability-evolution")
        self.assertIn("Tharness", role["scenario"])
        document = catalog.read_document("tharness-maintainer", "rule")
        self.assertEqual(document["path"], "AIGC/roles/tharness-maintainer/RULE.md")
        self.assertIn("Tharness 能力维护员规则", document["content"])
        self.assertEqual(len(document["hash"]), 64)
        self.assertEqual(document["version"], document["hash"])

    def test_unknown_role_document_and_path_escape_are_rejected(self) -> None:
        catalog = load_role_catalog(ROOT, self.config)
        with self.assertRaises(KeyError):
            catalog.read_document("missing-role", "rule")
        with self.assertRaises(KeyError):
            catalog.read_document("tharness-maintainer", "../../VERSION.md")
        role_root = repo_path(ROOT, "AIGC/roles")
        with self.assertRaisesRegex(ValueError, "角色文件越界"):
            _safe_role_file(role_root, "tharness-maintainer", ROOT / "AGENTS.md")

    def test_server_is_loopback_read_only_and_sets_security_headers(self) -> None:
        server = create_role_browser_server(ROOT, self.config, 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address
            self.assertEqual(host, "127.0.0.1")
            with urllib.request.urlopen(f"http://{host}:{port}/api/summary", timeout=3) as response:
                payload = json.loads(response.read().decode("utf-8"))
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
                self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
                self.assertEqual(payload["counts"]["roles"], 12)
            with urllib.request.urlopen(
                f"http://{host}:{port}/api/roles/tharness-maintainer/documents/skills",
                timeout=3,
            ) as response:
                payload = json.loads(response.read().decode("utf-8"))
                self.assertEqual(payload["kind"], "skills")
            request = urllib.request.Request(f"http://{host}:{port}/api/summary", method="POST", data=b"{}")
            with self.assertRaises(urllib.error.HTTPError) as write_error:
                urllib.request.urlopen(request, timeout=3)
            self.assertEqual(write_error.exception.code, 405)
            with self.assertRaises(urllib.error.HTTPError) as traversal_error:
                urllib.request.urlopen(
                    f"http://{host}:{port}/api/roles/tharness-maintainer/documents/..%2F..%2FVERSION.md",
                    timeout=3,
                )
            self.assertEqual(traversal_error.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_port_and_cli_arguments_are_validated(self) -> None:
        parsed = parse_args(["roles-ui", "--no-open", "--port", "43210"])
        self.assertTrue(parsed.no_open)
        self.assertEqual(parsed.port, 43210)
        with self.assertRaisesRegex(ValueError, "端口必须"):
            create_role_browser_server(ROOT, self.config, 70000)

        occupied = socket.socket()
        occupied.bind(("127.0.0.1", 0))
        occupied.listen(1)
        try:
            with self.assertRaises(OSError):
                create_role_browser_server(ROOT, self.config, occupied.getsockname()[1])
        finally:
            occupied.close()

    def test_rule_save_is_atomic_conflict_safe_and_security_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir).resolve()
            config, rule_path = self.make_editable_fixture(root)
            server = create_role_browser_server(root, config, 0, ROOT / "tools/role-browser")
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            host, port = server.server_address
            origin = f"http://{host}:{port}"

            def get_json(path: str) -> dict:
                with urllib.request.urlopen(origin + path, timeout=3) as response:
                    return json.loads(response.read().decode("utf-8"))

            def put(path: str, body: bytes, token: str, request_origin: str | None = None, content_type: str = "application/json"):
                headers = {"Content-Type": content_type, "X-Tharness-CSRF": token}
                if request_origin is not None:
                    headers["Origin"] = request_origin
                request = urllib.request.Request(origin + path, method="PUT", data=body, headers=headers)
                return urllib.request.urlopen(request, timeout=3)

            def assert_http_error(code: int, call) -> dict:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    call()
                self.assertEqual(error.exception.code, code)
                return json.loads(error.exception.read().decode("utf-8"))

            try:
                summary = get_json("/api/summary")
                token = summary["csrfToken"]
                loaded = get_json("/api/roles/role-manager/documents/rule")
                self.assertEqual(loaded["hash"], hashlib.sha256(rule_path.read_bytes()).hexdigest())

                base_payload = {"content": "# 角色管理员规则\n\n- 已更新\n", "baseHash": loaded["hash"]}
                valid_payload = json.dumps(base_payload, ensure_ascii=False).encode("utf-8")
                assert_http_error(403, lambda: put("/api/roles/role-manager/documents/rule", valid_payload, "wrong", origin))
                assert_http_error(403, lambda: put("/api/roles/role-manager/documents/rule", valid_payload, token, "http://127.0.0.1:1"))
                assert_http_error(415, lambda: put("/api/roles/role-manager/documents/rule", valid_payload, token, origin, "text/plain"))

                no_maintenance = assert_http_error(400, lambda: put("/api/roles/role-manager/documents/rule", valid_payload, token, origin))
                self.assertIn("维护模式", no_maintenance["error"])
                preview_payload = json.dumps({**base_payload, "previewOnly": True}, ensure_ascii=False).encode("utf-8")
                with put("/api/roles/role-manager/documents/rule", preview_payload, token, origin) as response:
                    preview = json.loads(response.read().decode("utf-8"))
                self.assertTrue(preview["changed"])
                self.assertIn("AIGC/roles/INDEX.md", preview["affectedEntries"])
                maintenance_payload = json.dumps({**base_payload, "maintenanceMode": True, "acknowledgeImpact": True}, ensure_ascii=False).encode("utf-8")
                with patch("tharness_roles_ui.os.replace", wraps=os.replace) as atomic_replace:
                    with put("/api/roles/role-manager/documents/rule", maintenance_payload, token, origin) as response:
                        saved = json.loads(response.read().decode("utf-8"))
                    atomic_replace.assert_called_once()
                saved_bytes = rule_path.read_bytes()
                self.assertTrue(saved_bytes.startswith(b"\xef\xbb\xbf"))
                self.assertIn(b"\r\n", saved_bytes)
                self.assertNotIn(b"\n", saved_bytes.replace(b"\r\n", b""))
                self.assertEqual(saved["hash"], hashlib.sha256(saved_bytes).hexdigest())
                self.assertFalse(list(rule_path.parent.glob(".RULE.md.*.tmp")))

                conflict = assert_http_error(409, lambda: put("/api/roles/role-manager/documents/rule", maintenance_payload, token, origin))
                self.assertEqual(conflict["currentHash"], saved["hash"])
                skills_payload = json.dumps({"content": "# changed", "baseHash": saved["hash"]}).encode("utf-8")
                assert_http_error(405, lambda: put("/api/roles/role-manager/documents/skills", skills_payload, token, origin))
                assert_http_error(404, lambda: put("/api/roles/role-manager/documents/..%2F..%2FRULE.md", skills_payload, token, origin))

                empty = json.dumps({"content": "   ", "baseHash": saved["hash"]}).encode("utf-8")
                assert_http_error(400, lambda: put("/api/roles/role-manager/documents/rule", empty, token, origin))
                oversized = json.dumps({"content": "x" * (MAX_RULE_BYTES + 1), "baseHash": saved["hash"]}).encode("utf-8")
                assert_http_error(400, lambda: put("/api/roles/role-manager/documents/rule", oversized, token, origin))
                assert_http_error(400, lambda: put("/api/roles/role-manager/documents/rule", b"\xff", token, origin))
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

    def test_missing_static_asset_has_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            server = create_role_browser_server(ROOT, self.config, 0, Path(temp_dir))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                host, port = server.server_address
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(f"http://{host}:{port}/", timeout=3)
                self.assertEqual(error.exception.code, 500)
                payload = json.loads(error.exception.read().decode("utf-8"))
                self.assertIn("静态资源缺失", payload["error"])
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)

    def test_frontend_document_tabs_do_not_shadow_browser_document(self) -> None:
        script = (ROOT / "tools/role-browser/app.js").read_text(encoding="utf-8")
        page = (ROOT / "tools/role-browser/index.html").read_text(encoding="utf-8")

        self.assertNotIn("forEach((document)", script)
        self.assertNotIn("function loadDocument(role, document", script)
        self.assertIn("role.documents.forEach((docInfo)", script)
        self.assertIn('const button = document.createElement("button")', script)
        self.assertIn("loadDocument(role, docInfo, button)", script)
        self.assertIn("MATURITY_ORDER", (ROOT / "tools/tharness_roles_ui.py").read_text(encoding="utf-8"))
        self.assertIn("成熟度 ${role.maturityLabel}", script)
        self.assertIn("baseHash: state.currentDocument.hash", script)
        self.assertIn('"X-Tharness-CSRF": state.csrfToken', script)
        self.assertIn('event.key.toLocaleLowerCase() === "s"', script)
        self.assertIn('window.addEventListener("beforeunload"', script)
        self.assertIn("confirmDiscard()", script)
        self.assertIn('id="rule-content"', page)
        self.assertIn('id="save-rule" type="button" disabled', page)
        self.assertIn('id="maintenance-mode" type="checkbox"', page)
        self.assertIn('id="preview-rule" type="button" disabled', page)
        self.assertIn("previewOnly: true", script)
        self.assertIn("acknowledgeImpact", script)
        self.assertIn("THARNESS · LOCAL ROLE MANAGER", page)
        self.assertIn('id="system-version"', page)
        self.assertIn("data.systemVersion", script)
        self.assertIn("skills/tools 只读", page)
        self.assertNotIn("LOCAL READ-ONLY", page)
        self.assertIn("state.saving || !state.dirty", script)
        self.assertIn("updateSaveButton();", script)

    def test_windows_launcher_has_required_python_fallbacks_and_failure_pause(self) -> None:
        launcher_path = ROOT / "Start-Roles-UI.cmd"
        raw_launcher = launcher_path.read_bytes()
        launcher = raw_launcher.decode("utf-8")

        self.assertIn(b"\r\n", raw_launcher)
        self.assertNotIn(b"\n", raw_launcher.replace(b"\r\n", b""))
        self.assertIn('if not "%THARNESS_PYTHON%"=="" goto check_env_python', launcher)
        self.assertIn("where py", launcher)
        self.assertIn("where python", launcher)
        self.assertIn("where python3", launcher)
        self.assertIn("%USERPROFILE%\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe", launcher)
        self.assertIn("%LOCALAPPDATA%\\Programs\\Python\\Python314\\python.exe", launcher)
        self.assertIn("%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe", launcher)
        self.assertNotIn("chenjianping", launcher.lower())
        self.assertNotIn("EnableDelayedExpansion", launcher)
        self.assertNotIn("for /d", launcher.lower())
        self.assertIn("使用解释器：%PYTHON_EXE%", launcher)
        self.assertIn("set \"EXIT_CODE=%ERRORLEVEL%\"", launcher)
        self.assertIn("Python 退出码：%EXIT_CODE%", launcher)
        self.assertIn('roles-ui %*', launcher)
        self.assertIn("可设置 THARNESS_PYTHON", launcher)
        self.assertGreaterEqual(launcher.count("pause"), 2)

    def test_browser_open_failure_prints_url_without_becoming_fatal(self) -> None:
        output = io.StringIO()
        with patch("tharness_roles_ui.webbrowser.open", return_value=False), redirect_stdout(output):
            opened = open_browser_or_warn("http://127.0.0.1:43210/")

        self.assertFalse(opened)
        self.assertIn("请手动打开：http://127.0.0.1:43210/", output.getvalue())

        output = io.StringIO()
        with patch("tharness_roles_ui.webbrowser.open", side_effect=RuntimeError("browser unavailable")), redirect_stdout(output):
            opened = open_browser_or_warn("http://127.0.0.1:43210/")
        self.assertFalse(opened)
        self.assertIn("browser unavailable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
