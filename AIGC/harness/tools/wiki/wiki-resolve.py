#!/usr/bin/env python3
"""Harness wiki-link 解析器

为 AI 提供 [[wiki-link]] → 实际文件路径 的映射。

用法:
    # 生成映射表 → wiki/knowledge/wiki-map.json
    python3 aigc/harness/tools/wiki/wiki-resolve.py --build

    # 解析单个 wiki-link（优先读缓存 JSON，无则实时扫描）
    python3 aigc/harness/tools/wiki/wiki-resolve.py --resolve scene-code
    python3 aigc/harness/tools/wiki/wiki-resolve.py --resolve "knowledge/system-map"

    # 解析文件中所有 wiki-link
    python3 aigc/harness/tools/wiki/wiki-resolve.py --file harness/agents/Project_Lead.md

    # 验证所有 wiki-link 完整性
    python3 aigc/harness/tools/wiki/wiki-resolve.py --check
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]   # aigc/harness/tools/wiki/ → 项目根
HARNESS_ROOT = REPO_ROOT / "aigc" / "harness"
WIKI_ROOT = REPO_ROOT / "aigc" / "wiki"
DOCS_ROOT = REPO_ROOT / "aigc" / "docs"
WIKI_MAP_PATH = WIKI_ROOT / "knowledge" / "wiki-map.json"

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]")


def build_name_map() -> dict[str, list[str]]:
    """扫描 harness/ + wiki/ 构建 name → [paths] 映射

    支持两种 key：
    - 文件名（无扩展名）: "scene-code" → ["harness/rules/GamePlay_Dev/scene-code.md"]
    - 父文件夹/文件名: "codegen/README" → ["harness/tools/codegen/README.md"]
    """
    name_to_paths: dict[str, list[str]] = {}

    for scan_root in [HARNESS_ROOT, WIKI_ROOT, DOCS_ROOT]:
        if not scan_root.exists():
            continue
        for dirpath, _, files in os.walk(scan_root):
            rel_dir = os.path.relpath(dirpath, REPO_ROOT)
            if "session-state" in rel_dir:
                continue
            for f in files:
                if not f.endswith(".md"):
                    continue
                rel_path = os.path.join(rel_dir, f)
                name = f[:-3]  # 去 .md

                # 基础 key: 文件名
                name_to_paths.setdefault(name, []).append(rel_path)

                # 消歧 key: 父文件夹/文件名
                parent = os.path.basename(dirpath)
                disambig = f"{parent}/{name}"
                name_to_paths.setdefault(disambig, []).append(rel_path)

    return name_to_paths


def load_or_build_map() -> dict[str, str | list[str]]:
    """优先读缓存 JSON，无则实时扫描并返回精简映射"""
    if WIKI_MAP_PATH.exists():
        return json.loads(WIKI_MAP_PATH.read_text(encoding="utf-8"))

    raw = build_name_map()
    clean = {}
    for k, v in sorted(raw.items()):
        unique = list(set(v))
        clean[k] = unique[0] if len(unique) == 1 else unique
    return clean


def resolve(link_text: str, name_map: dict[str, str | list[str]]) -> str | None:
    """解析 wiki-link 文本 → 文件路径（唯一匹配返回路径，否则 None）"""
    val = name_map.get(link_text)
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        unique = list(set(val))
        if len(unique) == 1:
            return unique[0]
    return None


def check_all_wikilinks(name_map: dict[str, list[str]]) -> list[tuple[str, int, str]]:
    """扫描所有文件，检查 wiki-link 是否可解析"""
    broken = []
    
    def _scan_file(fpath: str):
        in_code = False
        for i, line in enumerate(
            open(os.path.join(REPO_ROOT, fpath), encoding="utf-8"), 1
        ):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for m in WIKILINK_RE.finditer(line):
                link = m.group(1)
                if not resolve(link, name_map):
                    broken.append((fpath, i, link))
    
    # 1. 扫描 harness/ + wiki/ + docs/ 下所有 .md（排除 session-state）
    for scan_root in [HARNESS_ROOT, WIKI_ROOT, DOCS_ROOT]:
        if not scan_root.exists():
            continue
        for dirpath, _, files in os.walk(scan_root):
            rel_dir = os.path.relpath(dirpath, REPO_ROOT)
            if "session-state" in rel_dir:
                continue
            for f in files:
                if not f.endswith(".md"):
                    continue
                _scan_file(os.path.join(rel_dir, f))
    
    # 2. 扫描 repo root 的 AGENTS.md
    agents_md = os.path.join(REPO_ROOT, "AGENTS.md")
    if os.path.isfile(agents_md):
        _scan_file("AGENTS.md")
    
    return broken


def resolve_file_links(
    filepath: str, name_map: dict[str, list[str]]
) -> list[tuple[int, str, str | None]]:
    """解析文件中所有 wiki-link"""
    results = []
    in_code = False
    for i, line in enumerate(open(filepath, encoding="utf-8"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in WIKILINK_RE.finditer(line):
            link = m.group(1)
            path = resolve(link, name_map)
            results.append((i, link, path))
    return results


def main():
    parser = argparse.ArgumentParser(description="Harness wiki-link 解析器")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true", help="输出 name→path JSON 映射")
    group.add_argument("--resolve", metavar="LINK", help="解析单个 wiki-link")
    group.add_argument("--file", metavar="PATH", help="解析文件中所有 wiki-link")
    group.add_argument("--check", action="store_true", help="检查所有 wiki-link 完整性")
    args = parser.parse_args()

    os.chdir(REPO_ROOT)

    if args.build:
        from wiki_log import append_wiki_log

        raw = build_name_map()
        clean = {}
        for k, v in sorted(raw.items()):
            unique = list(set(v))
            clean[k] = unique[0] if len(unique) == 1 else unique
        WIKI_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
        WIKI_MAP_PATH.write_text(
            json.dumps(clean, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        n_unique = sum(1 for v in clean.values() if isinstance(v, str))
        n_ambig = sum(1 for v in clean.values() if isinstance(v, list))
        print(f"✅ 已生成 {WIKI_MAP_PATH.relative_to(REPO_ROOT)}")
        print(f"   唯一映射: {n_unique}，歧义: {n_ambig}")
        append_wiki_log("lint", "wiki-map 重建",
                        f"扫描 harness/wiki/docs 目录生成 wiki-map.json，唯一映射: {n_unique} 条，歧义: {n_ambig} 条")
        return

    name_map = load_or_build_map()

    if args.resolve:
        path = resolve(args.resolve, name_map)
        if path:
            print(path)
        else:
            val = name_map.get(args.resolve)
            if isinstance(val, list):
                print(f"⚠️ 歧义，{len(val)} 个匹配:", file=sys.stderr)
                for p in val:
                    print(f"  {p}", file=sys.stderr)
            else:
                print(f"❌ 未找到: [[{args.resolve}]]", file=sys.stderr)
            sys.exit(1)

    elif args.file:
        results = resolve_file_links(args.file, name_map)
        if not results:
            print("没有 wiki-link")
            return
        for lineno, link, path in results:
            status = path if path else "❌ 未解析"
            print(f"  L{lineno}: [[{link}]] → {status}")

    elif args.check:
        from wiki_log import append_wiki_log

        broken = check_all_wikilinks(name_map)
        if not broken:
            print("✅ 所有 wiki-link 均可解析")
            append_wiki_log("lint", "wiki-link 完整性检查", "扫描所有 .md 文件中的 wiki-link 引用，结果: ✅ 全部可解析")
            return
        print(f"❌ 发现 {len(broken)} 条无法解析的 wiki-link\n")
        for fpath, lineno, link in broken:
            print(f"  {fpath}:{lineno}  [[{link}]]")
        append_wiki_log("lint", "wiki-link 完整性检查",
                        f"扫描所有 .md 文件中的 wiki-link 引用，结果: ❌ {len(broken)} 条未解析")
        sys.exit(1)


if __name__ == "__main__":
    main()
