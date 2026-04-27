#!/usr/bin/env python3
"""harness 路径引用 → wiki-link 迁移工具

基于 wiki-map.json 做路径→别名反查，确保生成的 [[alias]] 可被 wiki-resolve.py 解析。

用法:
    python3 aigc/harness/tools/wiki/migrate-wiki.py              # 预览所有变更
    python3 aigc/harness/tools/wiki/migrate-wiki.py --write       # 执行写入
    python3 aigc/harness/tools/wiki/migrate-wiki.py --stats       # 仅统计
    python3 aigc/harness/tools/wiki/migrate-wiki.py --include-code-blocks  # 含代码块内路径
"""

import argparse
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]   # aigc/harness/tools/wiki/ → 项目根
AIGC_ROOT = REPO_ROOT / "aigc"
HARNESS_ROOT = AIGC_ROOT / "harness"
WIKI_ROOT = AIGC_ROOT / "wiki"
DOCS_ROOT = AIGC_ROOT / "docs"
WIKI_MAP_PATH = WIKI_ROOT / "knowledge" / "wiki-map.json"

# 转换 .md 引用；.sh/.py/.json 保持路径引用
# 支持 harness/ 和 aigc/AIGC 开头的路径
REF_PATTERN = re.compile(
    r'`((?:harness|[Aa][Ii][Gg][Cc])/[\w\-/\u4e00-\u9fff. ]+\.md)(\s+§[^`]*)?`'  # group(1): backtick 内路径, group(2): §后缀（可选）
    r'|'
    r'(?<![`\[])((?:harness|[Aa][Ii][Gg][Cc])/[\w\-/\u4e00-\u9fff. ]+\.md)(?![`\]])'  # group(3): 无包裹路径
)


def build_reverse_map() -> dict[str, str]:
    """从 wiki-map.json 构建 path→alias 反查表

    优先级：单目标别名 > 数组别名（消歧义），同级内选最短。
    数组值（多目标别名）逐一展开。
    """
    wm = json.loads(WIKI_MAP_PATH.read_text(encoding="utf-8"))
    # path → [(alias, is_array), ...]
    path_to_aliases: dict[str, list[tuple[str, bool]]] = {}
    for alias, target in wm.items():
        if isinstance(target, list):
            for t in target:
                path_to_aliases.setdefault(t, []).append((alias, True))
        else:
            path_to_aliases.setdefault(target, []).append((alias, False))

    reverse: dict[str, str] = {}
    for path, alias_pairs in path_to_aliases.items():
        norm = path.replace("\\", "/")
        # 优先选单目标别名（精确、无歧义）
        singles = [a for a, is_arr in alias_pairs if not is_arr]
        if singles:
            best = min(singles, key=len)
        else:
            best = min((a for a, _ in alias_pairs), key=len)
        reverse[norm] = best
    return reverse


# 历史遗留路径 → 实际物理路径 的别名映射
# 早期目录结构中 AIGC/rules/ 直接对应 aigc/harness/rules/ 等
PATH_ALIASES: list[tuple[str, str]] = [
    # 精确子目录映射优先（长前缀先匹配）
    ("AIGC/docs/GamePlay_Dev/内容边界定义/", "aigc/wiki/raw/biu2-framework/内容边界定义/"),
    ("AIGC/docs/GamePlay_Dev/范例文档/",     "aigc/wiki/raw/biu2-framework/范例文档/"),
    # 通用映射
    ("AIGC/rules/",  "aigc/harness/rules/"),
    ("AIGC/skills/", "aigc/harness/skills/"),
    ("AIGC/agents/", "aigc/harness/agents/"),
    ("AIGC/tools/",  "aigc/harness/tools/"),
    ("AIGC/docs/",   "aigc/docs/"),
]


def _normalize_path(raw: str) -> str:
    """统一路径分隔符 + 应用别名映射"""
    norm = raw.replace("\\", "/")
    # 应用别名映射（优先匹配最长前缀）
    for old_prefix, new_prefix in PATH_ALIASES:
        if norm.startswith(old_prefix):
            norm = new_prefix + norm[len(old_prefix):]
            break
        # 大小写不敏感匹配
        if norm.lower().startswith(old_prefix.lower()):
            norm = new_prefix + norm[len(old_prefix):]
            break
    return norm


def path_to_wikilink(ref_path: str, reverse_map: dict[str, str]) -> str | None:
    """将路径引用转换为 wiki-link 格式

    通过 wiki-map.json 反查，确保生成的别名可解析。
    支持历史遗留路径别名（如 AIGC/rules/ → aigc/harness/rules/）。
    找不到映射 → 返回 None（跳过转换）。
    """
    norm = _normalize_path(ref_path)
    alias = reverse_map.get(norm)
    # 尝试大小写不敏感匹配（aigc/ vs AIGC/）
    if alias is None:
        norm_lower = norm.lower()
        for k, v in reverse_map.items():
            if k.lower() == norm_lower:
                alias = v
                break
    if alias is None:
        return None
    return f"[[{alias}]]"


def process_file(
    filepath: str, reverse_map: dict[str, str], include_code_blocks: bool = False
) -> tuple[list[tuple[int, str, str, str]], list[str]]:
    """处理单个文件，返回 (变更列表, 新内容行)"""
    lines = open(filepath, encoding="utf-8").readlines()
    new_lines = []
    changes = []
    in_code_block = False

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()

        # 跟踪代码块
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block and not include_code_blocks:
            new_lines.append(line)
            continue

        # 在非代码区域查找引用并替换（从后向前避免偏移）
        new_line = line
        for m in reversed(list(REF_PATTERN.finditer(line))):
            ref_path = m.group(1) or m.group(3)  # group(1): backtick内, group(3): 裸路径
            full_match = m.group(0)
            wiki = path_to_wikilink(ref_path, reverse_map)

            if wiki is None:
                continue

            # 若有 § 后缀（backtick模式 group(2)），追加到 wiki-link 后
            suffix = m.group(2) or ""
            replacement = wiki + suffix

            new_line = new_line[: m.start()] + replacement + new_line[m.end() :]
            changes.append((lineno, full_match, replacement, filepath))

        new_lines.append(new_line)

    return changes, new_lines


def scan_files() -> list[str]:
    """收集要处理的 .md 文件（跳过 session-state）"""
    result = []
    # 扫描 harness/ + wiki/ + docs/ 目录
    for root_dir in [HARNESS_ROOT, WIKI_ROOT, DOCS_ROOT]:
        for dirpath, _, files in os.walk(root_dir):
            rel_dir = os.path.relpath(dirpath, REPO_ROOT)
            if "session-state" in rel_dir:
                continue
            for f in files:
                if f.endswith(".md"):
                    result.append(os.path.join(rel_dir, f))
    # 包含 aigc/ 下的 AGENTS.md
    agents_md = REPO_ROOT / "aigc" / "AGENTS.md"
    if agents_md.exists():
        result.append("aigc/AGENTS.md")
    return sorted(result)


def main():
    parser = argparse.ArgumentParser(description="harness 路径引用 → wiki-link 迁移")
    parser.add_argument("--write", action="store_true", help="执行写入（默认仅预览）")
    parser.add_argument("--stats", action="store_true", help="仅统计")
    parser.add_argument("--include-code-blocks", action="store_true",
                        help="也转换代码块内的路径引用（Agent 加载指令等）")
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    reverse_map = build_reverse_map()
    md_files = scan_files()

    all_changes = []
    file_new_contents = {}

    for fpath in md_files:
        changes, new_lines = process_file(fpath, reverse_map, args.include_code_blocks)
        if changes:
            all_changes.extend(changes)
            file_new_contents[fpath] = new_lines

    if args.stats:
        unmapped = set()
        for fpath in md_files:
            lines = open(fpath, encoding="utf-8").readlines()
            in_cb = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_cb = not in_cb
                    continue
                if in_cb and not args.include_code_blocks:
                    continue
                for m in REF_PATTERN.finditer(line):
                    ref = m.group(1) or m.group(3)  # group(1): backtick内, group(3): 裸路径
                    if path_to_wikilink(ref, reverse_map) is None:
                        unmapped.add(ref)
        print(f"扫描文件:       {len(md_files)}")
        print(f"待转换引用:     {len(all_changes)}")
        print(f"涉及文件:       {len(file_new_contents)}")
        print(f"wiki-map 条目:  {len(reverse_map)}")
        if unmapped:
            print(f"未映射路径:     {len(unmapped)}")
            for p in sorted(unmapped):
                print(f"  - {p}")
        return

    if not all_changes:
        print("✅ 没有需要转换的引用")
        return

    by_file: dict[str, list[tuple[int, str, str]]] = {}
    for lineno, old, new, fpath in all_changes:
        by_file.setdefault(fpath, []).append((lineno, old, new))

    if not args.write:
        print("👀 预览（加 --write 执行）\n")

    for fpath, items in sorted(by_file.items()):
        print(f"  📄 {fpath}")
        for lineno, old, new in items:
            print(f"     L{lineno}: {old}")
            print(f"       → {new}")
        print()

    print(f"共 {len(all_changes)} 处引用待转换（{len(file_new_contents)} 个文件）")

    if args.write:
        for fpath, new_lines in file_new_contents.items():
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        print(f"\n✅ 已写入 {len(file_new_contents)} 个文件")

        from wiki_log import append_wiki_log
        append_wiki_log("schema", "wiki-link 批量迁移",
                        f"将路径引用转换为 wiki-link 格式，共转换 {len(all_changes)} 处引用，涉及 {len(file_new_contents)} 个文件")
    else:
        print("\n💡 确认后执行: python3 aigc/harness/tools/wiki/migrate-wiki.py --write")


if __name__ == "__main__":
    main()
