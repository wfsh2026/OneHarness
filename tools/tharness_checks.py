from __future__ import annotations

import re
from pathlib import Path

from tharness_config import config_list, config_value, load_simple_yaml, rel_path, repo_path
from tharness_behavior import removed_role_reference_errors, tool_contract_errors
from tharness_index import wiki_pages_from_index
from tharness_markdown import markdown_files, missing_front_matter_fields, parse_front_matter


def _registry_rows(repo_root: Path, config: dict, key: str, field_count: int) -> tuple[list[list[str]], list[str]]:
    registry_value = config_value(config, "capability_registry_file")
    if not registry_value:
        return [], ["自检配置缺少 capability_registry_file"]

    registry_path = repo_path(repo_root, registry_value)
    if not registry_path.exists():
        return [], [f"机器注册源缺失: {registry_value}"]

    registry = load_simple_yaml(registry_path)
    rows = []
    errors = []
    for raw in config_list(registry, key):
        fields = [field.strip() for field in raw.split("|")]
        if len(fields) != field_count or any(not field for field in fields):
            errors.append(f"机器注册源格式错误: {key} -> {raw}")
            continue
        rows.append(fields)
    if not rows:
        errors.append(f"机器注册源为空: {key}")
    return rows, errors


def _markdown_capability_ids(path: Path) -> set[str]:
    ids = set()
    if not path.exists():
        return ids
    in_current_capabilities = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip() == "## 当前能力":
            in_current_capabilities = True
            continue
        if in_current_capabilities and line.startswith("## "):
            break
        if not in_current_capabilities:
            continue
        match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if match and match.group(1) != "capability_id":
            ids.add(match.group(1))
    return ids


def registry_consistency_errors(repo_root: Path, config: dict) -> list[str]:
    """Validate the machine registry against directories and human-facing indexes."""
    role_rows, errors = _registry_rows(repo_root, config, "role_registry", 11)
    capability_rows, capability_errors = _registry_rows(repo_root, config, "capability_registry", 8)
    errors.extend(capability_errors)
    registry_path = repo_path(repo_root, config_value(config, "capability_registry_file"))
    if registry_path.exists():
        registry_config = load_simple_yaml(registry_path)
        if config_value(registry_config, "schema_version") != "2":
            errors.append("机器注册源 schema_version 必须为 2")
    if errors:
        return errors

    role_index_path = repo_path(repo_root, config_value(config, "role_index_file"))
    routing_index_path = repo_path(repo_root, config_value(config, "role_routing_index_file"))
    capability_index_path = repo_path(repo_root, config_value(config, "capability_index_file"))
    required_paths = set(config_list(config, "check_required_paths"))
    forbidden_names = set(config_list(config, "session_role_forbidden_current_role_names"))

    role_index_text = role_index_path.read_text(encoding="utf-8-sig") if role_index_path.exists() else ""
    routing_index_text = routing_index_path.read_text(encoding="utf-8-sig") if routing_index_path.exists() else ""

    registered_slugs = {row[0] for row in role_rows}
    role_root = repo_path(repo_root, config_value(config, "role_root"))
    directory_slugs = {path.parent.name for path in role_rule_files(repo_root, config)}
    for slug in sorted(directory_slugs - registered_slugs):
        errors.append(f"角色目录未登记到机器注册源: {slug}")
    for slug in sorted(registered_slugs - directory_slugs):
        errors.append(f"机器注册源声明了不存在的角色目录: {slug}")

    registered_capabilities = {row[0] for row in capability_rows}
    if len(registered_capabilities) != len(capability_rows):
        errors.append("机器注册源存在重复 capability_id")
    markdown_capabilities = _markdown_capability_ids(capability_index_path)
    for capability_id in sorted(markdown_capabilities - registered_capabilities):
        errors.append(f"能力索引条目未登记到机器注册源: {capability_id}")
    for capability_id in sorted(registered_capabilities - markdown_capabilities):
        errors.append(f"机器注册源能力未登记到能力索引: {capability_id}")

    maturity_values = {"draft", "contracted", "tested", "evaluated"}
    capability_owners = set()
    for capability_id, entry, owner, contract_status, maturity, last_verified, eval_suite, deprecated_by in capability_rows:
        if not repo_path(repo_root, entry).exists():
            errors.append(f"机器注册源能力入口不存在: {capability_id} -> {entry}")
        if contract_status not in maturity_values or maturity not in maturity_values:
            errors.append(f"能力成熟度字段无效: {capability_id} -> {contract_status}/{maturity}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", last_verified):
            errors.append(f"能力 last_verified 格式错误: {capability_id} -> {last_verified}")
        if deprecated_by != "-" and deprecated_by not in registered_capabilities:
            errors.append(f"能力 deprecated_by 未登记: {capability_id} -> {deprecated_by}")
        if deprecated_by == capability_id:
            errors.append(f"能力不得弃用到自身: {capability_id}")
        capability_owners.add(owner)

    dispatchable_routes = set()
    role_slugs = {row[0] for row in role_rows}
    if len(role_slugs) != len(role_rows):
        errors.append("机器注册源存在重复角色 slug")
    for owner in sorted(capability_owners - role_slugs - {"tharness-core"}):
        errors.append(f"能力 owner 未登记为角色: {owner}")
    for slug, display_name, rule_entry, route_entry, capability_id, role_type, maturity, owner, contract_status, eval_suite, deprecated_by in role_rows:
        if maturity not in maturity_values or contract_status not in maturity_values:
            errors.append(f"角色成熟度字段无效: {slug} -> {maturity}/{contract_status}")
        if deprecated_by != "-" and deprecated_by not in role_slugs:
            errors.append(f"角色 deprecated_by 未登记: {slug} -> {deprecated_by}")
        if owner not in role_slugs and owner not in {"tharness-core"}:
            errors.append(f"角色 owner 未登记: {slug} -> {owner}")
        if not repo_path(repo_root, rule_entry).exists():
            errors.append(f"机器注册源角色入口不存在: {slug} -> {rule_entry}")
        index_entry = f"`{slug}/RULE.md`"
        if role_type != "infrastructure" and (display_name not in role_index_text or index_entry not in role_index_text):
            errors.append(f"角色库缺少机器注册角色: {display_name} -> {slug}/RULE.md")
        if capability_id != "-" and capability_id not in registered_capabilities:
            errors.append(f"角色映射到未登记能力: {slug} -> {capability_id}")

        if role_type != "dispatchable":
            continue
        dispatchable_routes.add(Path(route_entry).name)
        if route_entry == "-" or not repo_path(repo_root, route_entry).exists():
            errors.append(f"可派发角色缺少派发页: {slug} -> {route_entry}")
        route_index_entry = f"`{Path(route_entry).name}`"
        if display_name not in routing_index_text or route_index_entry not in routing_index_text:
            errors.append(f"派发索引缺少机器注册角色: {display_name} -> {Path(route_entry).name}")
        for required in (rule_entry, route_entry, f"AIGC/roles/{slug}/skills/INDEX.md", f"AIGC/roles/{slug}/tools/INDEX.md"):
            if required not in required_paths:
                errors.append(f"自检配置未登记角色必需路径: {required}")
        if display_name not in forbidden_names:
            errors.append(f"主会话禁用角色名未登记: {display_name}")

    if routing_index_path.exists():
        actual_routes = {path.name for path in routing_index_path.parent.glob("*.md") if path.name != "INDEX.md"}
        for route in sorted(actual_routes - dispatchable_routes):
            errors.append(f"派发页未登记到机器注册源: {route}")
        for route in sorted(dispatchable_routes - actual_routes):
            errors.append(f"机器注册源声明了不存在的派发页: {route}")

    registry_value = config_value(config, "capability_registry_file")
    if registry_value not in required_paths:
        errors.append(f"自检配置未登记机器注册源: {registry_value}")
    return errors


def role_rule_files(repo_root: Path, config: dict) -> list[Path]:
    role_root = repo_path(repo_root, config_value(config, "role_root"))
    role_rule_file_name = config_value(config, "role_rule_file_name")

    if not role_root.exists():
        return []

    return sorted(role_root.rglob(role_rule_file_name))


def run_doctor(repo_root: Path, config: dict) -> tuple[list[str], list[str], list[str]]:
    errors = []
    warnings = []
    info = []

    for entry in config_list(config, "required_entries"):
        if not repo_path(repo_root, entry).exists():
            errors.append(f"入口文件缺失: {entry}")

    index_file = repo_path(repo_root, config_value(config, "wiki_index_file"))
    if not index_file.exists():
        errors.append(f"wiki 索引缺失: {rel_path(repo_root, index_file)}")
        wiki_pages = []
    else:
        wiki_pages, index_errors = wiki_pages_from_index(repo_root, index_file)
        errors.extend(index_errors)

    wiki_required = config_list(config, "wiki_front_matter_required_fields")
    wiki_allow_empty = config_list(config, "wiki_front_matter_allow_empty_fields")
    for page in wiki_pages:
        missing = missing_front_matter_fields(parse_front_matter(page), wiki_required, wiki_allow_empty)
        if missing:
            errors.append(f"wiki 元数据缺失: {rel_path(repo_root, page)} -> {', '.join(missing)}")

    info.append(f"wiki 页面: {len(wiki_pages)}")
    info.append(f"角色规则: {len(role_rule_files(repo_root, config))}")
    framework_root = repo_path(repo_root, config_value(config, "framework_root"))
    info.append(f"AIGC 根目录: {rel_path(repo_root, framework_root)}（大小写兼容解析）")
    if warnings:
        info.append(f"警告: {len(warnings)}")

    return errors, warnings, info


def run_index(repo_root: Path, config: dict) -> tuple[list[str], list[str], list[str], list[Path]]:
    errors = []
    warnings = []
    info = []

    index_file = repo_path(repo_root, config_value(config, "wiki_index_file"))
    index_config = load_simple_yaml(index_file)
    scanned_pages, scan_errors = wiki_pages_from_index(repo_root, index_file)
    errors.extend(scan_errors)

    scanned = [rel_path(repo_root, path) for path in scanned_pages]
    declared = config_list(index_config, "pages")

    missing = sorted(set(scanned) - set(declared))
    extra = sorted(set(declared) - set(scanned))

    for page in missing:
        errors.append(f"索引缺少页面: {page}")
    for page in extra:
        errors.append(f"索引声明了不存在或被排除的页面: {page}")

    seen_ids = {}
    for page in scanned_pages:
        fields = parse_front_matter(page)
        page_id = fields.get("id", "") if fields else ""
        if not page_id:
            continue
        if page_id in seen_ids:
            errors.append(f"wiki id 重复: {page_id} -> {seen_ids[page_id]}, {rel_path(repo_root, page)}")
        else:
            seen_ids[page_id] = rel_path(repo_root, page)

    info.append(f"扫描页面: {len(scanned)}")
    info.append(f"索引页面: {len(declared)}")
    return errors, warnings, info, scanned_pages


def missing_gitignore_patterns(repo_root: Path, required_patterns: list[str]) -> list[str]:
    gitignore_path = repo_root / ".gitignore"
    if not gitignore_path.exists():
        return [pattern for pattern in required_patterns if pattern]

    lines = {
        line.strip().replace("\\", "/").rstrip("/")
        for line in gitignore_path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }

    missing = []
    for pattern in required_patterns:
        normalized = pattern.replace("\\", "/").rstrip("/")
        if normalized and normalized not in lines:
            missing.append(pattern)
    return missing


def session_role_marker_errors(repo_root: Path, config: dict) -> list[str]:
    role_file_value = config_value(config, "session_role_marker_file")
    if not role_file_value:
        return []

    role_path = repo_path(repo_root, role_file_value)
    if not role_path.exists():
        return [f"会话角色标识文件缺失: {role_file_value}"]

    errors = []
    text = role_path.read_text(encoding="utf-8-sig")
    relative = rel_path(repo_root, role_path)

    for field in config_list(config, "session_role_required_fields"):
        if field and field not in text:
            errors.append(f"会话角色标识字段缺失: {relative} -> {field}")

    fallback = config_value(config, "session_role_fallback_name")
    if fallback and fallback not in text:
        errors.append(f"会话角色标识兜底角色缺失: {relative} -> {fallback}")

    for role_name in config_list(config, "session_role_allowed_names"):
        if role_name and role_name not in text:
            errors.append(f"会话角色标识允许角色缺失: {relative} -> {role_name}")

    for role_name in config_list(config, "session_role_forbidden_current_role_names"):
        if not role_name:
            continue
        pattern = re.compile(rf"【当前角色】\s*{re.escape(role_name)}(?:\s|$)")
        if pattern.search(text):
            errors.append(f"会话角色标识禁止主会话角色: {relative} -> {role_name}")

    for statement in config_list(config, "session_role_required_statements"):
        if statement and statement not in text:
            errors.append(f"会话角色标识关键约束缺失: {relative} -> {statement}")

    return errors


def version_consistency_errors(repo_root: Path, config: dict) -> list[str]:
    expected = config_value(config, "system_version")
    if not expected:
        return ["自检配置缺少 system_version"]
    version_path = repo_path(repo_root, "AIGC/capabilities/VERSION.md")
    index_path = repo_path(repo_root, config_value(config, "capability_index_file"))
    version_text = version_path.read_text(encoding="utf-8-sig") if version_path.exists() else ""
    index_text = index_path.read_text(encoding="utf-8-sig") if index_path.exists() else ""
    errors = []
    if f"current_version: {expected}" not in version_text:
        errors.append(f"VERSION 与 system_version 不一致: {expected}")
    if f"当前系统版本：`{expected}`" not in index_text:
        errors.append(f"能力索引与 system_version 不一致: {expected}")
    return errors


def run_check(repo_root: Path, config: dict) -> tuple[list[str], list[str], list[str]]:
    errors = []
    warnings = []
    info = []

    for path_value in config_list(config, "check_required_paths"):
        if not repo_path(repo_root, path_value).exists():
            errors.append(f"结构自检必需文件缺失: {path_value}")

    for pattern in missing_gitignore_patterns(repo_root, config_list(config, "check_gitignore_required_patterns")):
        errors.append(f"结构自检必需 Git 忽略缺失: {pattern}")

    errors.extend(session_role_marker_errors(repo_root, config))
    errors.extend(registry_consistency_errors(repo_root, config))
    errors.extend(tool_contract_errors(repo_root, config))
    errors.extend(removed_role_reference_errors(repo_root))
    errors.extend(version_consistency_errors(repo_root, config))

    index_errors, index_warnings, index_info, _ = run_index(repo_root, config)
    errors.extend(f"索引结构自检失败: {error}" for error in index_errors)
    warnings.extend(index_warnings)
    info.extend(index_info)

    doctor_errors, doctor_warnings, doctor_info = run_doctor(repo_root, config)
    errors.extend(f"健康检查失败: {error}" for error in doctor_errors)
    warnings.extend(doctor_warnings)
    info.extend(doctor_info)

    boundary_exclude = config_list(config, "check_boundary_exclude_names")
    forbidden_patterns = config_list(config, "check_boundary_forbidden_patterns")
    for scan_path in config_list(config, "check_boundary_scan_paths"):
        base = repo_path(repo_root, scan_path)
        for page in markdown_files(base, boundary_exclude):
            text = page.read_text(encoding="utf-8-sig")
            for pattern in forbidden_patterns:
                if pattern and pattern in text:
                    errors.append(f"边界结构自检失败: {rel_path(repo_root, page)} 包含 `{pattern}`")

    return errors, warnings, info
