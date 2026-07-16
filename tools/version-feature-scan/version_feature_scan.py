#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan git history and generate a release feature directory review document."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


EXIT_OK = 0
EXIT_INVALID = 2
DEFAULT_TIMEOUT_SECONDS = 60.0


def configure_utf8_streams(streams: Iterable[object] | None = None) -> None:
    """Keep Chinese CLI output stable on Windows without assuming stream type."""
    for stream in streams or (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


@dataclass
class Commit:
    repo: str
    sha: str
    date: str
    author: str
    subject: str
    is_merge: bool = False
    files: list[str] = field(default_factory=list)
    inner_subjects: list[str] = field(default_factory=list)


@dataclass
class RepoScan:
    name: str
    path: Path
    base: str
    target: str
    merge_base: str = ""
    commit_count: int = 0
    merge_count: int = 0
    commits: list[Commit] = field(default_factory=list)
    merges: list[Commit] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def run_git(repo: Path, args: list[str], allow_fail: bool = False, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"git {' '.join(args)} timed out after {timeout:g}s in {repo}") from exc
    if proc.returncode != 0 and not allow_fail:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def safe_filename(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\s]+", "-", value.strip())
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def repo_name(path: Path) -> str:
    normalized = str(path).replace("\\", "/")
    if normalized.endswith("/Assets/Script/Biubiubiu2"):
        return "Biubiubiu2"
    if normalized.endswith("/Assets/Script"):
        return "Assets-Script"
    return path.name


def parse_log(text: str, repo: str, is_merge: bool = False) -> list[Commit]:
    rows: list[Commit] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 3)
        if len(parts) < 4:
            continue
        rows.append(Commit(repo=repo, sha=parts[0], date=parts[1], author=parts[2], subject=parts[3], is_merge=is_merge))
    return rows


def collect_files_for_commit(repo: Path, commit: Commit, limit: int, timeout: float) -> list[str]:
    text = run_git(repo, ["show", "--name-only", "--format=", "--find-renames", commit.sha], allow_fail=True, timeout=timeout)
    files = [x.strip() for x in text.splitlines() if x.strip()]
    return files[:limit]


def collect_inner_subjects_for_merge(repo: Path, commit: Commit, limit: int, timeout: float) -> list[str]:
    text = run_git(
        repo,
        ["log", "--date=short", "--pretty=format:%s", f"{commit.sha}^1..{commit.sha}^2", "--no-merges"],
        allow_fail=True,
        timeout=timeout,
    )
    subjects = [x.strip() for x in text.splitlines() if x.strip()]
    return subjects[:limit]


def validate_repo(path: Path, base: str, target: str, timeout: float) -> list[str]:
    errors = []
    if not path.exists():
        return [f"仓库路径不存在: {path}"]
    if not path.is_dir():
        return [f"仓库路径不是目录: {path}"]
    try:
        if run_git(path, ["rev-parse", "--is-inside-work-tree"], timeout=timeout).lower() != "true":
            errors.append(f"路径不是 Git 工作树: {path}")
        run_git(path, ["rev-parse", "--verify", f"{base}^{{commit}}"], timeout=timeout)
        run_git(path, ["rev-parse", "--verify", f"{target}^{{commit}}"], timeout=timeout)
    except RuntimeError as exc:
        errors.append(str(exc))
    return errors


def scan_repo(
    path: Path,
    base: str,
    target: str,
    evidence_dir: Path,
    file_limit: int,
    timeout: float,
    write_evidence: bool = True,
) -> RepoScan:
    scan = RepoScan(name=repo_name(path), path=path, base=base, target=target)
    repo_out = evidence_dir / scan.name
    if write_evidence:
        repo_out.mkdir(parents=True, exist_ok=True)
    try:
        scan.merge_base = run_git(path, ["merge-base", base, target], timeout=timeout)
        commits_text = run_git(path, ["log", "--date=short", "--pretty=format:%H%x09%ad%x09%an%x09%s", f"{base}..{target}"], timeout=timeout)
        merges_text = run_git(path, ["log", "--merges", "--date=short", "--pretty=format:%H%x09%ad%x09%an%x09%s", f"{base}..{target}"], timeout=timeout)
        first_parent_merges = run_git(path, ["log", "--first-parent", "--merges", "--date=short", "--pretty=format:%H%x09%ad%x09%an%x09%s", f"{base}..{target}"], allow_fail=True, timeout=timeout)
        stat_text = run_git(path, ["diff", "--stat", "--find-renames", base, target], allow_fail=True, timeout=timeout)
        name_status = run_git(path, ["diff", "--name-status", "--find-renames", base, target], allow_fail=True, timeout=timeout)

        scan.commits = parse_log(commits_text, scan.name, False)
        scan.merges = parse_log(merges_text, scan.name, True)
        scan.commit_count = len(scan.commits)
        scan.merge_count = len(scan.merges)
        scan.changed_files = [line.split("\t")[-1] for line in name_status.splitlines() if line.strip()]

        for commit in scan.merges:
            commit.files = collect_files_for_commit(path, commit, file_limit, timeout)
            commit.inner_subjects = collect_inner_subjects_for_merge(path, commit, file_limit, timeout)

        if write_evidence:
            (repo_out / "commits.tsv").write_text(commits_text + "\n", encoding="utf-8")
            (repo_out / "merge-commits.tsv").write_text(merges_text + "\n", encoding="utf-8")
            (repo_out / "first-parent-merge-commits.tsv").write_text(first_parent_merges + "\n", encoding="utf-8")
            (repo_out / "diff-stat.txt").write_text(stat_text + "\n", encoding="utf-8")
            (repo_out / "name-status.txt").write_text(name_status + "\n", encoding="utf-8")
            detail_lines = []
            for commit in scan.merges:
                branch = extract_branch_from_merge(commit.subject) or ""
                for subject in commit.inner_subjects:
                    detail_lines.append(f"{commit.sha}\t{branch}\t{subject}")
            (repo_out / "merge-inner-subjects.tsv").write_text("\n".join(detail_lines) + "\n", encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        scan.errors.append(str(exc))
        if write_evidence:
            (repo_out / "ERROR.txt").write_text(str(exc) + "\n", encoding="utf-8")
    return scan


def extract_branch_from_merge(subject: str) -> str | None:
    patterns = [
        r"Merge (?:remote-tracking )?branch ['\"]([^'\"]+)['\"]",
        r"Merge branch ([^\s]+)",
        r"Merge pull request .* from ([^\s]+)",
        r"合并(?:分支)?[：: ]+([^\s]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, subject, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def normalize_feature_key(text: str) -> str:
    text = text.strip().strip(" /'\"")
    text = re.sub(r"^origin/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^global/", "", text, flags=re.IGNORECASE)

    # Prefer concrete feature names from common branch layouts.
    branch_patterns = [
        r"^feature/v\d+(?:\.\d+)?/(.+)$",
        r"^hotfix/feature/v\d+(?:\.\d+)?/(.+)$",
        r"^hotfix/global/feature/v\d+(?:\.\d+)?/(.+)$",
        r"^hotfix/release/v\d+(?:\.\d+)?/\d+/(.+)$",
        r"^hotfix/release/v\d+(?:\.\d+)?/(.+)$",
        r"^bugfix/v\d+(?:\.\d+)?/(.+)$",
    ]
    for pattern in branch_patterns:
        m = re.match(pattern, text, flags=re.IGNORECASE)
        if m:
            text = m.group(1)
            break

    # Drop common suffixes that describe merge rounds rather than distinct features.
    text = re.sub(r"[-_/](merge|merge-dev|merge-to-dev|merge-to-develop)$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[-_]\d{4}$", "", text)
    text = re.sub(r"[-_](new|bak|backup|test\d*)$", "", text, flags=re.IGNORECASE)
    text = text.strip(" /'\"")
    if not text:
        text = "未命名功能"
    return text


def clean_feature_name(key: str) -> str:
    words = [w for w in re.split(r"[-_/]+", key) if w]
    if not words:
        return "未命名功能"
    known = {
        "ai": "AI",
        "ui": "UI",
        "ugc": "UGC",
        "gme": "GME",
        "pc": "PC",
        "ios": "iOS",
        "android": "Android",
        "csv": "CSV",
        "pve": "PVE",
        "pvp": "PVP",
        "br05": "BR05",
    }
    rendered = [known.get(w.lower(), w) for w in words]
    return " ".join(rendered)


def should_skip_feature(key: str, subject: str) -> bool:
    source = (extract_branch_from_merge(subject) or subject).lower().strip()
    value = f"{key} {subject}".lower()

    exact_bad = {"develop", "origin/develop", "master", "origin/master", "未命名功能"}
    if source in exact_bad or key.lower() in exact_bad:
        return True

    # Release/global release merges are version plumbing, not feature directory entries.
    release_patterns = [
        r"^origin/release/", r"^release/", r"^global/release/",
        r"^origin/global/release/", r"^origin/develop$",
    ]
    if any(re.match(pattern, source, flags=re.IGNORECASE) for pattern in release_patterns):
        return True

    skip_terms = [
        "merge-to-dev", "merge-to-develop", "merge-dev", "merge-to-2501", "2414-merge",
        "bugfix", "fixbug", "output", "ci-ignore", "log-delete", "perf-test",
        "auto-commit", "resource/develop", "resource/release", "merge origin/develop",
        "merge remote-tracking branch 'origin/develop'", "merge branch 'develop'",
    ]
    if any(term in value for term in skip_terms):
        return True

    noisy_patterns = [
        r"(^|[-_ /])g?\d{4}[-_ /]*merge[-_ /]*to[-_ /]*g?\d{4}($|[-_ /])",
        r"^\d{4}[-_ /]*global$",
        r"(^|[-_ /])fix($|[-_ /])",
        r"(^|[-_ /])bug($|[-_ /])",
        r"(^|[-_ /])bug[-_ /]*fix($|[-_ /])",
        r"(^|[-_ /])test\d*($|[-_ /])",
    ]
    if any(re.search(pattern, key, flags=re.IGNORECASE) for pattern in noisy_patterns):
        return True

    return False

def canonical_feature_key(key: str) -> str:
    low = key.lower().replace("_", "-")
    canonical_rules = [
        (r"^bounty-", "bounty-task"),
        (r"^(br05-dream-island|dream-island|dreamisland)", "br05-dream-island"),
        (r"^golden-master", "golden-master"),
        (r"^sheep-vehicle", "sheep-vehicle"),
        (r"^roleai-behavio", "roleai-behavior"),
        (r"^guidance", "guidance"),
        (r"^lobby", "lobby"),
        (r"^(football|foot-ball)", "football"),
        (r"^seasonitem", "seasonitem"),
        (r"^ice-", "ice-optimization"),
    ]
    for pattern, value in canonical_rules:
        if re.search(pattern, low, flags=re.IGNORECASE):
            return value
    return key

def summarize_modules(files: Iterable[str], max_items: int = 4) -> str:
    modules: Counter[str] = Counter()
    for file in files:
        parts = file.replace("\\", "/").split("/")
        if len(parts) >= 2:
            modules["/".join(parts[:2])] += 1
        elif parts and parts[0]:
            modules[parts[0]] += 1
    if not modules:
        return "提交信息"
    return "、".join(name for name, _ in modules.most_common(max_items))


def unique_keep_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = value.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def clean_subject_for_feature(subject: str) -> str:
    text = subject.strip()
    text = re.sub(r"(?i)^Revert\s+\"(.+)\"$", r"\1", text)
    text = re.sub(r"(?i)#?XC[-_ ]?\d+", "", text)
    text = re.sub(r"(?i)#?SM[-_ ]?\d+", "", text)
    text = re.sub(r"(?i)<\s*[^>]+\s*>", "", text)
    text = re.sub(r"(?i)\[(fix|feat|feature|md|opt|perf|bug|merge|test)\]", "", text)
    text = re.sub(r"(?i)^(fix|feat|feature|md|opt|perf|bug|test)[:：\-\s]+", "", text)
    text = re.sub(r"(?i)^Merge .+$", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -_：:，,。.")
    return text


def has_chinese(text: str) -> bool:
    return re.search(r"[\u4e00-\u9fff]", text) is not None


EXACT_LABELS = {
    "active-box": "活跃宝箱",
    "ai-air-throw": "AI 空中投掷",
    "aigc-knowledge": "AIGC 知识库",
    "aigc-perfanalyzer": "性能分析工具",
    "android-pss-delay": "Android PSS 延迟采样",
    "anti-cheat": "反外挂",
    "baize": "白泽相关内容",
    "base-back-ground": "基础背景",
    "board-opt": "面板显示优化",
    "bounty-task": "悬赏令",
    "br05-dream-island": "BR05 梦幻岛",
    "car-hit": "载具碰撞",
    "car-skin-opt": "载具皮肤显示优化",
    "classic-event": "经典活动",
    "club-seasonitem": "俱乐部赛季道具",
    "controller6": "六号控制器",
    "figurine-collection": "手办收藏",
    "football": "足球玩法",
    "fr2-optimize": "FR2 工具优化",
    "gamequan-custom-zone-shapes": "游戏圈自定义区域形状",
    "gateway-request-opt": "网关请求优化",
    "glgs": "GLGS 活动",
    "gme-update": "GME 语音组件更新",
    "goldegg-rap": "金蛋说唱活动",
    "golden-master": "金牌大师",
    "guandao": "关刀武器",
    "guidance": "新手引导",
    "hw-play": "HW 玩法",
    "ice-optimization": "冰面效果与性能优化",
    "in-editor-download": "编辑器内下载",
    "inspect-action-pre": "检视动作预览",
    "language-match": "语言匹配",
    "legend-card": "传奇卡",
    "leisure-mode-item": "休闲模式道具",
    "lobby": "大厅",
    "mirror-base-image-perf": "镜像基础图性能优化",
    "pc-audio-optimize": "PC 音频优化",
    "personal-history": "个人历史记录",
    "preload-feature-optimize": "功能预加载优化",
    "random-gunskin-effect": "随机枪皮肤特效",
    "rank": "段位排行",
    "rebuff": "Buff 重做",
    "refactor-battle-role-logic": "战斗角色逻辑重构",
    "reflectionfix": "反射问题修复",
    "res-build-optimize": "资源构建优化",
    "return-lb": "回流礼包",
    "return-yh": "回流优惠",
    "returning": "回流活动",
    "roleai-behavior": "角色 AI 行为",
    "saiki": "Saiki 联动内容",
    "sandstorm-open": "沙暴开放配置",
    "season-ss26": "SS26 赛季",
    "seasonitem": "赛季道具",
    "server-terrain": "服务端地形",
    "session-close-opt": "会话关闭优化",
    "sheep-op": "绵羊载具优化",
    "sheep-vehicle": "绵羊载具",
    "shop-optimize": "商店优化",
    "shopping-cart-opimize": "购物车优化",
    "sm-235281-scene": "场景资源调整",
    "special-level-ai": "特殊关卡 AI",
    "strip-server-scene": "服务端场景裁剪",
    "subpackage": "分包资源",
    "tips-team-controller": "组队提示控制",
    "warui-opt": "战斗 UI 优化",
    "weapon-check-tool": "武器检查工具",
}


def semantic_label_from_key(key: str) -> str:
    low = key.lower().replace("_", "-")
    if low in EXACT_LABELS:
        return EXACT_LABELS[low]
    if re.fullmatch(r"xc-\d+", low):
        return "任务单问题处理"
    words = [w for w in re.split(r"[-_/]+", key) if w]
    translated = {
        "fix": "修复",
        "opt": "优化",
        "optimize": "优化",
        "perf": "性能优化",
        "tool": "工具",
        "scene": "场景",
        "server": "服务端",
        "resource": "资源",
        "audio": "音频",
        "match": "匹配",
        "item": "道具",
        "skin": "皮肤",
        "vehicle": "载具",
        "feature": "功能",
    }
    rendered = [translated.get(w.lower(), w) for w in words]
    return " ".join(rendered) if rendered else "未命名功能"


def is_noise_subject(subject: str) -> bool:
    low = subject.lower().strip()
    exact_noise = {
        "代码审核",
        "代码修改",
        "代码规范提交",
        "修复变基",
        "修复变基后报错",
        "更新 aigc 框架",
        "重命名文件",
        "删除文件",
        "删除不需要的文件",
        "删除无用日志",
        "添加日志",
        "提交测试工具包宏",
        "测试管线搭建",
        "战报测试管线搭建",
    }
    if subject in exact_noise:
        return True
    noisy_terms = [
        "代码审核文档",
        "代码审核能力",
        "优化代码审核",
        "开发功能文档",
        "aigc 框架",
        "aigc框架",
        "debug代码",
        "测试提交",
        "仅提交",
    ]
    return any(term in low for term in noisy_terms)


def relevance_terms_for_key(key: str, label: str) -> list[str]:
    low = key.lower().replace("_", "-")
    custom = {
        "ai-air-throw": ["ai", "空中", "投掷", "空投"],
        "bounty-task": ["bounty", "悬赏", "赏金"],
        "br05-dream-island": ["br05", "梦幻岛", "摸金", "冰面", "小飞碟", "肠岛"],
        "car-skin-opt": ["载具", "皮肤"],
        "classic-event": ["经典", "活动"],
        "figurine-collection": ["手办", "展柜", "模糊玻璃"],
        "golden-master": ["金牌", "大师"],
        "guandao": ["关刀"],
        "guidance": ["引导"],
        "ice-optimization": ["冰面", "滑冰", "冰材质"],
        "legend-card": ["传奇卡"],
        "lobby": ["大厅"],
        "roleai-behavior": ["ai", "AI", "寻路", "行为"],
        "season-ss26": ["ss26", "赛季", "徽章"],
        "sheep-vehicle": ["绵羊", "载具"],
    }
    terms = custom.get(low, [])
    terms.extend([part for part in re.split(r"[-_/ ]+", key) if len(part) >= 3])
    terms.extend([part for part in re.split(r"[-_/ ]+", label) if len(part) >= 2])
    return unique_keep_order(terms)


def filter_relevant_subjects(key: str, label: str, subjects: list[str]) -> list[str]:
    terms = relevance_terms_for_key(key, label)
    if not terms:
        return subjects
    relevant = [
        subject
        for subject in subjects
        if any(term and term.lower() in subject.lower() for term in terms)
    ]
    return relevant or subjects


def summarize_feature(key: str, subjects: list[str], files: list[str]) -> tuple[str, str]:
    cleaned = unique_keep_order(clean_subject_for_feature(subject) for subject in subjects)
    cleaned = [subject for subject in cleaned if not is_noise_subject(subject)]
    chinese_subjects = [subject for subject in cleaned if has_chinese(subject)]
    usable = chinese_subjects or cleaned
    label = semantic_label_from_key(key)
    low_key = key.lower().replace("_", "-")
    if low_key in EXACT_LABELS:
        usable = filter_relevant_subjects(key, label, usable)

    if usable:
        first = usable[0]
        if re.fullmatch(r"xc-\d+", low_key):
            name = first
        elif low_key in EXACT_LABELS:
            name = label
        elif len(first) <= 40 and has_chinese(first):
            name = first
        else:
            name = f"{label}相关调整"
        points = usable[:4]
        desc = "；".join(points)
        if len(usable) > len(points):
            desc += f"；另有 {len(usable) - len(points)} 项提交要点待详细文档展开"
        return name, desc

    module_hint = summarize_modules(files)
    name = f"{label}相关调整"
    desc = f"从分支名和改动模块推断为{label}相关调整；提交标题未提供足够可读要点，需在详细文档阶段结合 diff 确认，当前涉及：{module_hint}。"
    return name, desc


def build_features(scans: list[RepoScan]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, object]] = {}
    for scan in scans:
        for merge in scan.merges:
            branch = extract_branch_from_merge(merge.subject)
            seed = branch or merge.subject
            key = normalize_feature_key(seed)
            if should_skip_feature(key, merge.subject):
                continue
            key = canonical_feature_key(key)
            if should_skip_feature(key, merge.subject):
                continue
            low = key.lower()
            entry = grouped.setdefault(low, {"key": key, "repos": set(), "subjects": [], "files": [], "commits": []})
            entry["repos"].add(scan.name)  # type: ignore[index]
            entry["subjects"].append(merge.subject)  # type: ignore[index]
            entry["subjects"].extend(merge.inner_subjects)  # type: ignore[index]
            entry["files"].extend(merge.files)  # type: ignore[index]
            entry["commits"].append(merge.sha)  # type: ignore[index]

    features: list[dict[str, Any]] = []
    for entry in grouped.values():
        key = str(entry["key"])
        repos = sorted(entry["repos"])  # type: ignore[arg-type]
        files = list(entry["files"])  # type: ignore[arg-type]
        subjects = list(entry["subjects"])  # type: ignore[arg-type]
        commits = unique_keep_order(entry["commits"])  # type: ignore[arg-type]
        name, desc = summarize_feature(key, subjects, files)
        if repos:
            desc = f"{desc}（关联仓库：{'、'.join(repos)}）"
        confidence = "high" if subjects and files else "medium" if subjects or files else "low"
        reasons = []
        if not subjects:
            reasons.append("缺少可读提交标题")
        if not files:
            reasons.append("缺少改动文件证据")
        features.append({
            "name": name,
            "key": key,
            "desc": desc,
            "confidence": confidence,
            "review_reasons": reasons,
            "evidence": {
                "repositories": repos,
                "merge_commits": commits,
                "files": unique_keep_order(files),
            },
        })

    features.sort(key=lambda x: x["name"].lower())
    return features


def relative_link(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def write_doc(version: str, scans: list[RepoScan], features: list[dict[str, Any]], output: Path, detail_root: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_values = sorted({s.base for s in scans})
    target_values = sorted({s.target for s in scans})
    merge_bases = "; ".join(f"{s.name}: {s.merge_base[:12] if s.merge_base else '获取失败'}" for s in scans)
    total_commits = sum(s.commit_count for s in scans)
    total_merges = sum(s.merge_count for s in scans)

    lines = [
        f"# {version}功能目录审核",
        "",
        "## 一、版本范围",
        "",
        "| 项目 | 内容 |",
        "|---|---|",
        f"| 基准分支 / commit | {'；'.join(base_values)} |",
        f"| 目标分支 / commit | {'；'.join(target_values)} |",
        f"| merge-base | {merge_bases} |",
        f"| 提交数量 | {total_commits} |",
        f"| merge commit 数量 | {total_merges} |",
        f"| 生成时间 | {now} |",
        "",
        "## 二、功能目录索引",
        "",
        "| 功能名称 | 功能说明 | 链接 |",
        "|---|---|---|",
    ]
    for feature in features:
        detail_doc = detail_root / safe_filename(feature["name"]) / "开发功能文档.md"
        link = relative_link(output, detail_doc)
        lines.append(f"| {feature['name']} | {feature['desc']} | [开发功能文档]({link}) |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_cluster_csv(features: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "key", "desc"])
        writer.writeheader()
        for feature in features:
            writer.writerow({field: feature[field] for field in ("name", "key", "desc")})


def scan_summary(version: str, scans: list[RepoScan], features: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "version": version,
        "status": "ok" if all(not scan.errors for scan in scans) else "partial-error",
        "repositories": [
            {
                "name": scan.name,
                "path": str(scan.path),
                "base": scan.base,
                "target": scan.target,
                "merge_base": scan.merge_base,
                "commit_count": scan.commit_count,
                "merge_count": scan.merge_count,
                "changed_files": scan.changed_files,
                "errors": scan.errors,
            }
            for scan in scans
        ],
        "features": features,
    }


def write_summary_json(summary: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_output_paths(output: Path) -> list[str]:
    errors = []
    evidence_dir = output.parent / "git-evidence"
    if output.exists() and output.is_dir():
        errors.append(f"输出路径是目录，必须是文件: {output}")
    if output.parent.exists() and not output.parent.is_dir():
        errors.append(f"输出父路径不是目录: {output.parent}")
    if evidence_dir.exists() and not evidence_dir.is_dir():
        errors.append(f"证据输出路径被文件占用: {evidence_dir}")
    return errors


def main() -> int:
    configure_utf8_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", action="append", required=True, help="Git repository path. Repeat for multiple repositories.")
    parser.add_argument("--base", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, help="Output 功能目录审核.md path.")
    parser.add_argument("--detail-root", required=True, help="Root directory for future 开发功能文档.md links.")
    parser.add_argument("--file-limit", type=int, default=80)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="Per-git-command timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and scan without writing output files.")
    args = parser.parse_args()

    output = Path(args.output)
    evidence_dir = output.parent / "git-evidence"
    errors = []
    if args.file_limit <= 0:
        errors.append("--file-limit 必须大于 0")
    if args.timeout <= 0:
        errors.append("--timeout 必须大于 0")
    repo_paths = [Path(repo).resolve() for repo in args.repo]
    repo_names = [repo_name(path) for path in repo_paths]
    if len(set(repo_paths)) != len(repo_paths):
        errors.append("--repo 包含重复仓库路径")
    if len(set(repo_names)) != len(repo_names):
        errors.append("多个仓库生成相同证据目录名，请调整仓库路径或分开扫描")
    if not args.dry_run:
        errors.extend(validate_output_paths(output))
    if args.timeout > 0:
        for repo in repo_paths:
            errors.extend(validate_repo(repo, args.base, args.target, args.timeout))
    if errors:
        for error in errors:
            print(f"error: {error}")
        return EXIT_INVALID

    scans = [
        scan_repo(
            repo,
            args.base,
            args.target,
            evidence_dir,
            args.file_limit,
            args.timeout,
            write_evidence=not args.dry_run,
        )
        for repo in repo_paths
    ]
    features = build_features(scans)
    summary = scan_summary(args.version, scans, features)
    if not args.dry_run:
        write_cluster_csv(features, evidence_dir / "feature-clusters.csv")
        write_summary_json(summary, evidence_dir / "scan-summary.json")
        write_doc(args.version, scans, features, output, Path(args.detail_root))

    print(f"mode: {'dry-run' if args.dry_run else 'write'}")
    if not args.dry_run:
        print(f"wrote: {output}")
    print(f"features: {len(features)}")
    for scan in scans:
        status = "ok" if not scan.errors else "error"
        print(f"{scan.name}: {status}, commits={scan.commit_count}, merges={scan.merge_count}, merge_base={scan.merge_base[:12] if scan.merge_base else '-'}")
        for err in scan.errors:
            print(f"  error: {err}")
    return EXIT_OK if all(not s.errors for s in scans) else EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())




