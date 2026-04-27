#!/usr/bin/env python3
"""
build-glossary.py — 从项目代码枚举自动生成名词表 glossary.md

通用工具 — 枚举源文件配置存储在 wiki-env.json 的 glossary.enums 字段中，
首次使用 --init 交互式引导用户提供关键代码文件路径和枚举名称。

用法:
  python3 aigc/harness/tools/wiki/features/build-glossary.py --init    # 首次：引导配置
  python3 aigc/harness/tools/wiki/features/build-glossary.py           # 预览
  python3 aigc/harness/tools/wiki/features/build-glossary.py --write   # 写入

数据源:
  - wiki/wiki-env.json → glossary.enums 配置（枚举文件路径 + 枚举名）
  - 项目代码 .cs 文件 → C# 枚举解析

依赖: pyyaml（可选，仅 feature 统计需要）
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── 路径工具 ──────────────────────────────────────────────────────────────────

def find_project_root() -> Path:
    """从脚本位置向上查找包含 aigc/wiki 的项目根目录"""
    d = Path(__file__).resolve()
    for _ in range(10):
        d = d.parent
        if (d / 'aigc' / 'wiki').is_dir():
            return d
    print("❌ 找不到项目根目录（需包含 aigc/wiki 目录）", file=sys.stderr)
    sys.exit(1)


def load_wiki_env(root: Path) -> dict:
    """读取 wiki-env.json"""
    env_path = root / 'aigc' / 'wiki' / 'wiki-env.json'
    if not env_path.exists():
        return {}
    with open(env_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_wiki_env(root: Path, env: dict):
    """写入 wiki-env.json"""
    env_path = root / 'aigc' / 'wiki' / 'wiki-env.json'
    with open(env_path, 'w', encoding='utf-8') as f:
        json.dump(env, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已写入 {env_path.relative_to(root)}")


# ── 枚举扫描与解析 ────────────────────────────────────────────────────────────

def scan_enums_in_file(filepath: Path) -> list[str]:
    """扫描 .cs 文件中所有 enum 名称"""
    if not filepath.exists():
        return []
    content = filepath.read_text(encoding='utf-8-sig')
    return re.findall(r'enum\s+(\w+)\s*(?::\s*\w+)?\s*\{', content)


def parse_enum(filepath: Path, enum_name: str) -> list[dict]:
    """解析 C# 枚举或 class 常量，返回 [{name, value, comment}, ...]"""
    if not filepath.exists():
        print(f"  ⚠️ 文件不存在: {filepath}", file=sys.stderr)
        return []
    content = filepath.read_text(encoding='utf-8-sig')

    # 优先尝试 enum 解析
    pattern = rf'enum\s+{enum_name}\s*(?::\s*\w+)?\s*\{{(.*?)\}}'
    m = re.search(pattern, content, re.DOTALL)

    if not m:
        # 回退：class/struct 常量解析（public const int Id_Xxx = 123;）
        class_pattern = rf'(?:class|struct)\s+{enum_name}\s*[^{{]*\{{(.*?)\}}'
        m = re.search(class_pattern, content, re.DOTALL)
        if not m:
            print(f"  ⚠️ 未找到 enum/class {enum_name} in {filepath.name}", file=sys.stderr)
            return []
        # 解析 const int 常量
        entries = []
        for line in m.group(1).split('\n'):
            line = line.strip()
            cm = re.match(
                r'public\s+const\s+(?:int|ushort|byte)\s+(\w+)\s*=\s*(-?\d+)\s*;\s*(?://\s*(.*))?',
                line
            )
            if cm:
                entries.append({
                    'name': cm.group(1),
                    'value': int(cm.group(2)),
                    'comment': cm.group(3).strip() if cm.group(3) else '',
                })
        return entries

    entries = []
    block = m.group(1)
    tooltip = None

    for line in block.split('\n'):
        line = line.strip()

        # [Tooltip("xxx")]
        tt = re.search(r'\[Tooltip\("([^"]+)"\)\]', line)
        if tt:
            tooltip = tt.group(1)
            continue

        # EnumName = 123, //注释
        em = re.match(r'(\w+)\s*=\s*(-?\d+)\s*,?\s*(?://\s*(.*))?', line)
        if em:
            comment = tooltip or (em.group(3).strip() if em.group(3) else '')
            entries.append({
                'name': em.group(1),
                'value': int(em.group(2)),
                'comment': comment,
            })
            tooltip = None
            continue

        # EnumName, //注释（无显式赋值 — 跳过，C# 枚举通常有显式值）
        em2 = re.match(r'(\w+)\s*,?\s*(?://\s*(.*))?$', line)
        if em2 and em2.group(1) not in ('', ):
            name = em2.group(1)
            if name.startswith('[') or name.startswith('/') or name.startswith('#'):
                continue
            comment = tooltip or (em2.group(2).strip() if em2.group(2) else '')
            entries.append({
                'name': name,
                'value': -1,  # 无显式值
                'comment': comment,
            })
            tooltip = None

    return entries


# ── --init 交互 ───────────────────────────────────────────────────────────────

def do_init(root: Path):
    """交互式引导用户配置 glossary 枚举源"""
    env = load_wiki_env(root)

    if 'glossary' in env and env['glossary'].get('enums'):
        print(f"ℹ️  已有 glossary 配置（{len(env['glossary']['enums'])} 个文件）")
        ans = input("   要重新配置吗？(y/N) ").strip().lower()
        if ans != 'y':
            print("   跳过，保留现有配置")
            return

    print()
    print("=" * 60)
    print("  glossary 枚举源配置")
    print("=" * 60)
    print()
    print("请提供项目中包含关键枚举定义的 C# 文件路径。")
    print("路径相对于项目根目录，例如：Assets/Script/Data/Base/GameMode.cs")
    print("输入空行结束。")
    print()

    enum_configs = []

    while True:
        file_path = input("📄 文件路径（空行结束）: ").strip()
        if not file_path:
            break

        abs_path = root / file_path
        if not abs_path.exists():
            print(f"  ❌ 文件不存在: {file_path}")
            continue

        # 扫描文件中的枚举
        found = scan_enums_in_file(abs_path)
        if not found:
            print(f"  ⚠️ 未找到 enum 定义: {file_path}")
            continue

        print(f"  发现 {len(found)} 个枚举:")
        for i, name in enumerate(found):
            print(f"    [{i+1}] {name}")

        selected = input("  选择要导出的枚举（逗号分隔序号，或 'all'）: ").strip()
        if selected.lower() == 'all':
            names = found
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selected.split(',')]
                names = [found[i] for i in indices if 0 <= i < len(found)]
            except (ValueError, IndexError):
                print("  ⚠️ 输入无效，跳过此文件")
                continue

        label = input("  标签（描述这组枚举，如「游戏模式枚举」）: ").strip()
        if not label:
            label = f"{Path(file_path).stem} 枚举"

        enum_configs.append({
            'file': file_path,
            'names': names,
            'label': label,
        })
        print(f"  ✅ 已添加: {file_path} → {names}")
        print()

    if not enum_configs:
        print("\n⚠️ 未添加任何枚举配置")
        return

    env['glossary'] = {'enums': enum_configs}
    save_wiki_env(root, env)

    print(f"\n📋 已配置 {len(enum_configs)} 个文件，共 {sum(len(c['names']) for c in enum_configs)} 个枚举")
    print(f"   下一步: python3 ... build-glossary.py --write")


# ── glossary 生成 ─────────────────────────────────────────────────────────────

def load_features(root: Path) -> dict:
    """加载所有 feature .md 的 YAML frontmatter → {name: {category, ...}}"""
    if not HAS_YAML:
        return {}
    features = {}
    wiki_raw = root / 'aigc' / 'wiki' / 'raw'
    if not wiki_raw.exists():
        return features
    for feat_dir in wiki_raw.rglob('features'):
        if not feat_dir.is_dir():
            continue
        for md in feat_dir.rglob('*.md'):
            if md.name.startswith('_'):
                continue
            try:
                text = md.read_text(encoding='utf-8-sig').lstrip('\ufeff')
            except Exception:
                continue
            if not text.startswith('---'):
                continue
            end = text.find('---', 3)
            if end == -1:
                continue
            try:
                meta = yaml.safe_load(text[3:end])
                if meta and isinstance(meta, dict) and 'name' in meta:
                    features[meta['name']] = meta
            except yaml.YAMLError:
                pass
    return features


def cn_number(n: int) -> str:
    """数字 → 中文序号"""
    cn = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    return cn[n] if n <= 10 else str(n)


def build_glossary(root: Path) -> str:
    """生成 glossary.md 全文"""
    env = load_wiki_env(root)
    glossary_cfg = env.get('glossary', {})
    enum_configs = glossary_cfg.get('enums', [])
    now = datetime.now().strftime('%Y-%m-%d')

    lines = []
    lines.append('# 名词表索引 (Glossary)')
    lines.append('')
    lines.append('> 项目核心术语与枚举值对照表。**由工具自动生成**，请勿手动编辑。')
    lines.append(f'> 生成命令: `python3 aigc/harness/tools/wiki/features/build-glossary.py --write`')
    lines.append(f'> 最后生成: {now}')
    lines.append('')
    lines.append('---')
    lines.append('')

    section_num = 1

    if not enum_configs:
        lines.append('> ⚠️ 未配置枚举源。请先运行 `--init` 引导配置，或在 `wiki-env.json` 中添加 `glossary.enums` 字段。')
        lines.append('')
    else:
        # 每个枚举配置生成一个章节
        for cfg in enum_configs:
            file_path = cfg['file']
            enum_names = cfg['names']
            label = cfg.get('label', Path(file_path).stem)
            abs_path = root / file_path

            for enum_name in enum_names:
                entries = parse_enum(abs_path, enum_name)
                if not entries:
                    continue

                cn = cn_number(section_num)
                lines.append(f'## {cn}、{enum_name} 枚举')
                lines.append('')
                lines.append(f'> 来源: `{file_path}`（{label}）')
                lines.append('')

                # 判断是否有显式值
                has_values = any(e['value'] >= 0 for e in entries)

                if has_values:
                    lines.append('| 枚举值 | 枚举名 | 中文名 |')
                    lines.append('|--------|--------|--------|')
                    for e in sorted(entries, key=lambda x: x['value']):
                        lines.append(f"| {e['value']} | {e['name']} | {e['comment']} |")
                else:
                    lines.append('| 枚举名 | 中文名 |')
                    lines.append('|--------|--------|')
                    for e in entries:
                        lines.append(f"| {e['name']} | {e['comment']} |")

                lines.append('')
                lines.append('---')
                lines.append('')
                section_num += 1

    # Feature 统计（兜底章节）
    features = load_features(root)
    if features:
        cn = cn_number(section_num)
        lines.append(f'## {cn}、Feature 统计')
        lines.append('')
        cat_count: dict[str, int] = {}
        for name, meta in features.items():
            cat = meta.get('category', 'unknown')
            top = cat.split('/')[0] if '/' in cat else cat
            cat_count[top] = cat_count.get(top, 0) + 1
        lines.append(f'> 总计: **{len(features)}** 个 feature（.md 格式，YAML frontmatter）')
        lines.append('')
        lines.append('| 模块 | 数量 |')
        lines.append('|------|------|')
        for cat in sorted(cat_count.keys()):
            lines.append(f'| {cat} | {cat_count[cat]} |')
        lines.append('')
    elif not HAS_YAML:
        cn = cn_number(section_num)
        lines.append(f'## {cn}、Feature 统计')
        lines.append('')
        lines.append('> ⚠️ 未安装 pyyaml，跳过 feature 统计。安装: `pip install pyyaml`')
        lines.append('')

    return '\n'.join(lines) + '\n'


# ── 入口 ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='从项目代码枚举自动生成名词表 glossary.md')
    parser.add_argument('--init', action='store_true', help='交互式引导配置枚举源')
    parser.add_argument('--write', action='store_true', help='写入 glossary.md')
    parser.add_argument('--project-root', type=str, default=None,
                        help='项目根目录（默认自动检测）')
    args = parser.parse_args()

    root = Path(args.project_root) if args.project_root else find_project_root()

    if args.init:
        do_init(root)
        return

    # 检查配置
    env = load_wiki_env(root)
    if not env.get('glossary', {}).get('enums'):
        print("⚠️ 未配置枚举源。")
        print("   方式一：运行 --init 交互式配置")
        print("   方式二：在 wiki-env.json 中手动添加 glossary.enums 字段")
        print()
        print("   格式示例：")
        print('   "glossary": {')
        print('     "enums": [')
        print('       {')
        print('         "file": "Assets/Script/Data/Base/GameMode.cs",')
        print('         "names": ["GameMode", "MatchMod"],')
        print('         "label": "游戏模式枚举"')
        print('       }')
        print('     ]')
        print('   }')
        print()
        print("   配置完成后重新运行即可。")
        sys.exit(1)

    content = build_glossary(root)
    out_path = root / 'aigc' / 'wiki' / 'knowledge' / 'glossary.md'

    if args.write:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding='utf-8')
        lines_count = content.count('\n')
        print(f'✅ 已生成 {out_path.relative_to(root)}（{lines_count} 行）')
    else:
        print(content)
        print(f'---\n📋 预览模式，加 --write 写入 {out_path.relative_to(root)}')


if __name__ == '__main__':
    main()
