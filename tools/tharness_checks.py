from __future__ import annotations

import re
from pathlib import Path

from tharness_config import config_list, config_value, load_simple_yaml, rel_path, repo_path
from tharness_index import wiki_pages_from_index
from tharness_markdown import markdown_files, missing_front_matter_fields, parse_front_matter


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
