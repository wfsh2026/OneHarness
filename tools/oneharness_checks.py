from __future__ import annotations

from pathlib import Path

from oneharness_config import config_list, config_value, load_simple_yaml, rel_path, repo_path
from oneharness_index import wiki_pages_from_index
from oneharness_markdown import markdown_files, missing_front_matter_fields, parse_front_matter


def workflow_rule_files(repo_root: Path, config: dict) -> list[Path]:
    workflow_root = repo_path(repo_root, config_value(config, "workflow_root"))
    rules_dir_name = config_value(config, "workflow_rules_dir_name")
    exclude_files = set(config_list(config, "workflow_rule_exclude_files"))

    files = []
    if not workflow_root.exists():
        return files

    for rules_dir in sorted(path for path in workflow_root.rglob(rules_dir_name) if path.is_dir()):
        for path in sorted(rules_dir.glob("*.md")):
            if path.name not in exclude_files:
                files.append(path)
    return files


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

    rule_required = config_list(config, "workflow_rule_required_fields")
    for rule in workflow_rule_files(repo_root, config):
        missing = missing_front_matter_fields(parse_front_matter(rule), rule_required, [])
        if missing:
            errors.append(f"工作流规则元数据缺失: {rel_path(repo_root, rule)} -> {', '.join(missing)}")

    index_name = config_value(config, "workflow_rules_index_name")
    for rule in workflow_rule_files(repo_root, config):
        index_path = rule.parent / index_name
        if not index_path.exists():
            errors.append(f"工作流规则索引缺失: {rel_path(repo_root, index_path)}")
            continue
        if rule.name not in index_path.read_text(encoding="utf-8-sig"):
            errors.append(f"工作流规则未被索引引用: {rel_path(repo_root, rule)}")

    info.append(f"wiki 页面: {len(wiki_pages)}")
    info.append(f"工作流规则: {len(workflow_rule_files(repo_root, config))}")
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


def run_gate(repo_root: Path, config: dict) -> tuple[list[str], list[str], list[str]]:
    errors = []
    warnings = []
    info = []

    for path_value in config_list(config, "gate_required_paths"):
        if not repo_path(repo_root, path_value).exists():
            errors.append(f"门控必需文件缺失: {path_value}")

    index_errors, index_warnings, index_info, _ = run_index(repo_root, config)
    errors.extend(f"索引门控失败: {error}" for error in index_errors)
    warnings.extend(index_warnings)
    info.extend(index_info)

    doctor_errors, doctor_warnings, doctor_info = run_doctor(repo_root, config)
    errors.extend(f"健康检查失败: {error}" for error in doctor_errors)
    warnings.extend(doctor_warnings)
    info.extend(doctor_info)

    boundary_exclude = config_list(config, "gate_boundary_exclude_names")
    forbidden_patterns = config_list(config, "gate_boundary_forbidden_patterns")
    for scan_path in config_list(config, "gate_boundary_scan_paths"):
        base = repo_path(repo_root, scan_path)
        for page in markdown_files(base, boundary_exclude):
            text = page.read_text(encoding="utf-8-sig")
            for pattern in forbidden_patterns:
                if pattern and pattern in text:
                    errors.append(f"边界门控失败: {rel_path(repo_root, page)} 包含 `{pattern}`")

    return errors, warnings, info
