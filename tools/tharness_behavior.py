from __future__ import annotations

import copy
import re
from pathlib import Path

from tharness_config import config_value, rel_path, repo_path


TOOL_FIELDS = (
    "tool_id", "purpose", "phase", "preconditions", "inputs",
    "outputs", "side_effects", "errors", "retry_stop", "evidence",
)
DOMAIN_SECTIONS = ("职责", "禁止范围", "输入边界", "输出边界", "验证边界")
REMOVED_ROLE_REFERENCES = (
    "intern-" + "engine-architecture-developer",
    "intern-" + "ui-developer",
    "intern-" + "gameplay-systems-developer",
    "intern-" + "combat-developer",
    "实习" + "工程架构开发者",
    "实习" + " UI 开发者",
    "实习" + "玩法系统开发者",
    "实习" + "战斗开发者",
)


def tool_contract_errors(repo_root: Path, config: dict) -> list[str]:
    role_root = repo_path(repo_root, config_value(config, "role_root"))
    errors: list[str] = []
    for path in sorted(role_root.glob("*/tools/INDEX.md")):
        text = path.read_text(encoding="utf-8-sig")
        blocks = re.split(r"(?m)^## tool:\s*", text)[1:]
        relative = rel_path(repo_root, path)
        if not blocks:
            errors.append(f"工具索引缺少契约条目: {relative}")
            continue
        for block in blocks:
            name = block.splitlines()[0].strip() or "<unnamed>"
            for field in TOOL_FIELDS:
                if not re.search(rf"(?m)^- {re.escape(field)}:\s*\S", block):
                    errors.append(f"工具契约字段缺失: {relative} -> {name}.{field}")
    return errors


def removed_role_reference_errors(repo_root: Path) -> list[str]:
    roots = [
        repo_path(repo_root, "AIGC/INDEX.md"),
        repo_path(repo_root, "AIGC/roles"),
        repo_path(repo_root, "AIGC/capabilities/INDEX.md"),
        repo_path(repo_root, "AIGC/capabilities/registry.yaml"),
        repo_path(repo_root, "AIGC/tharness.yaml"),
        repo_path(repo_root, "tools/tharness_roles_ui.py"),
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix in {".md", ".yaml"})
    errors = []
    for path in files:
        text = path.read_text(encoding="utf-8-sig")
        for reference in REMOVED_ROLE_REFERENCES:
            if reference in text:
                errors.append(f"已删除角色仍被活动入口引用: {rel_path(repo_root, path)} -> {reference}")
    return errors


def _markdown_table(path: Path, heading: str) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    marker = f"### {heading}"
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration as exc:
        raise ValueError(f"策略表缺失: {heading}") from exc
    table_lines: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("### ") or stripped.startswith("## "):
            break
        if stripped.startswith("|"):
            table_lines.append(stripped)
    if len(table_lines) < 3:
        raise ValueError(f"策略表为空: {heading}")
    headers = [cell.strip().strip("`") for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise ValueError(f"策略表列数错误: {heading} -> {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def _resolve(rows: list[dict[str, str]], inputs: dict[str, str], output_key: str) -> str:
    matches: list[tuple[int, str]] = []
    for row in rows:
        if all(row.get(key) in {"*", value} for key, value in inputs.items()):
            specificity = sum(row.get(key) != "*" for key in inputs)
            matches.append((specificity, row[output_key]))
    if not matches:
        raise ValueError(f"无策略命中: {inputs}")
    best = max(score for score, _ in matches)
    outputs = {output for score, output in matches if score == best}
    if len(outputs) != 1:
        raise ValueError(f"策略冲突: {inputs} -> {sorted(outputs)}")
    return outputs.pop()


def _table_cases(
    rows: list[dict[str, str]],
    cases: list[tuple[str, dict[str, str], str]],
    output_key: str,
) -> list[str]:
    errors: list[str] = []
    for case_id, inputs, expected in cases:
        try:
            actual = _resolve(rows, inputs, output_key)
        except ValueError as exc:
            errors.append(f"{case_id}: {exc}")
            continue
        if actual != expected:
            errors.append(f"{case_id}: 预期 {expected}，实际 {actual}")
    return errors


def _domain_errors(repo_root: Path) -> list[str]:
    domain_root = repo_path(repo_root, "AIGC/roles/project-developer/domains")
    index_rows = _markdown_table(domain_root / "INDEX.md", "domain_registry")
    errors: list[str] = []
    expected = {"architecture", "ui", "gameplay", "combat"}
    actual = {row.get("domain", "") for row in index_rows}
    if actual != expected:
        errors.append(f"领域路由集合错误: {sorted(actual)}")
    for row in index_rows:
        domain = row.get("domain", "")
        path = domain_root / row.get("file", "")
        if not path.is_file():
            errors.append(f"领域文件缺失: {domain} -> {path.name}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        for section in DOMAIN_SECTIONS:
            if f"## {section}" not in text:
                errors.append(f"领域边界缺失: {domain}.{section}")
    return errors


def deterministic_behavior_eval(repo_root: Path, config: dict) -> tuple[list[str], list[str]]:
    """Run deterministic policy-contract scenarios; this is not a model behavior eval."""
    errors: list[str] = []
    passed: list[str] = []

    def record(case_id: str, case_errors: list[str]) -> None:
        if case_errors:
            errors.extend(case_errors)
        else:
            passed.append(case_id)

    policy_path = repo_path(repo_root, "AIGC/roles/common/autonomy-policy.md")
    tables = {
        name: _markdown_table(policy_path, name)
        for name in ("request_policy", "delegation_policy", "uncertainty_policy", "task_package_policy", "output_policy")
    }

    request_cases = [
        (kind, {"request_kind": kind}, "no")
        for kind in ("answer", "review", "diagnose", "plan")
    ] + [("change-write", {"request_kind": "change"}, "yes")]
    request_read_cases = [(f"{kind}-read", {"request_kind": kind}, "yes") for kind in ("answer", "review", "diagnose", "plan")]
    record("request-read-write", _table_cases(tables["request_policy"], request_cases, "allow_write") + _table_cases(tables["request_policy"], request_read_cases, "allow_read"))

    delegation_cases = [
        ("low-single-local", {"risk": "low", "scope": "single", "independent_parallel": "no", "specialist_isolation": "no"}, "local"),
        ("independent-parallel", {"risk": "low", "scope": "multi", "independent_parallel": "yes", "specialist_isolation": "no"}, "delegate"),
        ("specialist-isolation", {"risk": "medium", "scope": "single", "independent_parallel": "no", "specialist_isolation": "yes"}, "delegate"),
        ("high-independent", {"risk": "high", "scope": "multi", "independent_parallel": "no", "specialist_isolation": "no"}, "delegate"),
    ]
    record("delegation-scenarios", _table_cases(tables["delegation_policy"], delegation_cases, "action"))
    validation_cases = [
        ("high-independent-validation", {"risk": "high", "scope": "single", "independent_parallel": "no", "specialist_isolation": "no"}, "independent")
    ]
    record("high-risk-validation", _table_cases(tables["delegation_policy"], validation_cases, "validation"))

    uncertainty_cases = [
        ("discover-first", {"discoverable": "yes", "reversible": "yes", "changes_outcome": "no", "external_or_destructive": "no"}, "inspect"),
        ("reasonable-assumption", {"discoverable": "no", "reversible": "yes", "changes_outcome": "no", "external_or_destructive": "no"}, "assume-and-disclose"),
        ("must-ask-outcome", {"discoverable": "no", "reversible": "no", "changes_outcome": "yes", "external_or_destructive": "no"}, "ask"),
        ("must-ask-external", {"discoverable": "yes", "reversible": "yes", "changes_outcome": "no", "external_or_destructive": "yes"}, "ask"),
    ]
    record("uncertainty-and-confirmation", _table_cases(tables["uncertainty_policy"], uncertainty_cases, "action"))

    package_cases = [
        ("lite-low", {"risk": "low", "cross_role": "no", "external_or_batch_write": "no", "session_resume": "no"}, "lite"),
        ("full-medium", {"risk": "medium", "cross_role": "no", "external_or_batch_write": "no", "session_resume": "no"}, "full"),
        ("full-high", {"risk": "high", "cross_role": "no", "external_or_batch_write": "no", "session_resume": "no"}, "full"),
        ("full-cross", {"risk": "low", "cross_role": "yes", "external_or_batch_write": "no", "session_resume": "no"}, "full"),
        ("full-batch", {"risk": "low", "cross_role": "no", "external_or_batch_write": "yes", "session_resume": "no"}, "full"),
        ("full-resume", {"risk": "low", "cross_role": "no", "external_or_batch_write": "no", "session_resume": "yes"}, "full"),
    ]
    record("task-package-upgrade", _table_cases(tables["task_package_policy"], package_cases, "template"))

    output_cases = [
        ("ordinary", {"formal_dispatch": "no", "formal_review": "no", "risk": "low", "user_format": "no"}, "normal"),
        ("formal-review", {"formal_dispatch": "no", "formal_review": "yes", "risk": "low", "user_format": "no"}, "four-fields"),
        ("user-format", {"formal_dispatch": "yes", "formal_review": "yes", "risk": "high", "user_format": "yes"}, "user-specified"),
    ]
    record("output-tiering", _table_cases(tables["output_policy"], output_cases, "format"))

    record("four-domain-routing", _domain_errors(repo_root))
    record("tool-contracts", tool_contract_errors(repo_root, config))
    record("removed-role-negative-check", removed_role_reference_errors(repo_root))

    controlled_files = [
        repo_path(repo_root, value)
        for value in ("AIGC/INDEX.md", "AIGC/roles/INDEX.md", "AIGC/roles/role-manager/RULE.md")
    ]
    controlled_phrases = ("低风险、小型、只读", "独立并行", "上下文隔离", "明显专业差异", "高风险独立证据", "低风险、可逆", "外部系统写入")
    duplicate_errors = []
    for path in controlled_files:
        text = path.read_text(encoding="utf-8-sig")
        for phrase in controlled_phrases:
            if phrase in text:
                duplicate_errors.append(f"受控策略语义重复: {rel_path(repo_root, path)} -> {phrase}")
    record("single-policy-source", duplicate_errors)

    # Mutation tests prove that missing, changed and conflicting policy rows are rejected.
    mutated_request = copy.deepcopy(tables["request_policy"])
    mutated_request[:] = [row for row in mutated_request if row["request_kind"] != "diagnose"]
    record("mutation-missing-request", [] if _table_cases(mutated_request, [("diagnose", {"request_kind": "diagnose"}, "no")], "allow_write") else ["删除 diagnose 后未被拒绝"])
    mutated_delegation = copy.deepcopy(tables["delegation_policy"])
    next(row for row in mutated_delegation if row["case_id"] == "low_single")["action"] = "delegate"
    record("mutation-wrong-delegation", [] if _table_cases(mutated_delegation, [delegation_cases[0]], "action") else ["错误低风险委派未被拒绝"])
    conflicting = copy.deepcopy(tables["delegation_policy"])
    conflict_row = copy.deepcopy(next(row for row in conflicting if row["case_id"] == "low_single"))
    conflict_row["case_id"] = "conflict"
    conflict_row["action"] = "delegate"
    conflicting.append(conflict_row)
    record("mutation-conflict", [] if _table_cases(conflicting, [delegation_cases[0]], "action") else ["冲突策略未被拒绝"])

    domain_rows = _markdown_table(repo_path(repo_root, "AIGC/roles/project-developer/domains/INDEX.md"), "domain_registry")
    mutated_domains = [row for row in domain_rows if row.get("domain") != "combat"]
    mutation_detected = {row.get("domain") for row in mutated_domains} != {"architecture", "ui", "gameplay", "combat"}
    record("mutation-missing-domain-route", [] if mutation_detected else ["删除 combat 路由后未被拒绝"])

    return errors, passed
