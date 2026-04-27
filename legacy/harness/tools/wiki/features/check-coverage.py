#!/usr/bin/env python3
"""
功能目录覆盖率检测工具
====================
检测哪些文件已被功能目录清单（feature 文件）覆盖，哪些未覆盖。
支持全量扫描和增量检测两种模式。

用法：
  # 全量覆盖率报告
  python3 aigc/harness/tools/wiki/features/check-coverage.py

  # 只检查指定文件（同步后使用）
  python3 aigc/harness/tools/wiki/features/check-coverage.py --files file1.cs file2.cs

  # 从 stdin 读取文件列表（配合 git diff）
  git diff --name-only HEAD~1 | python3 aigc/harness/tools/wiki/features/check-coverage.py --stdin

  # 检查某个目录下的文件
  python3 aigc/harness/tools/wiki/features/check-coverage.py --dir Assets/Scripts/GamePlay/Server/AI

  # 按分类汇总未覆盖文件
  python3 aigc/harness/tools/wiki/features/check-coverage.py --summary

  # 建议归属（试验性）
  python3 aigc/harness/tools/wiki/features/check-coverage.py --suggest --files Assets/Scripts/GamePlay/Server/AI/SAI_NewUnit.cs

依赖：
  无外部依赖（纯 Python 标准库）
"""

import json
import glob
import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path


def find_project_root():
    """向上查找包含 aigc/ 目录的项目根"""
    d = Path(__file__).resolve()
    for _ in range(10):
        d = d.parent
        if (d / 'aigc' / 'wiki').is_dir():
            return d
    return Path.cwd()


def load_wiki_env(project_root):
    """加载 wiki-env.json，返回 dict 或 None"""
    env_path = project_root / 'aigc' / 'wiki' / 'wiki-env.json'
    if env_path.exists():
        import json as _json
        with open(env_path) as f:
            return _json.load(f)
    return None


def get_script_dir(project_root):
    """从 wiki-env.json 获取代码根路径，fallback 到 Assets/Scripts"""
    env = load_wiki_env(project_root)
    if env and 'repos' in env:
        script_repo = env['repos'].get('script', {})
        if 'path' in script_repo:
            return project_root / script_repo['path']
    # fallback: 尝试两种常见路径
    for name in ['Assets/Scripts', 'Assets/Script']:
        p = project_root / name
        if p.exists():
            return p
    return project_root / 'Assets' / 'Scripts'


def load_all_features(project_root):
    """加载所有 feature 文件，返回 {name: data} 和 {file_path: [feature_names]}"""
    features_dir = project_root / 'aigc' / 'wiki' / 'raw' / 'features'
    if not features_dir.exists():
        # 尝试查找 raw/ 下子目录中的 features/
        raw_dir = project_root / 'aigc' / 'wiki' / 'raw'
        if raw_dir.exists():
            for child in raw_dir.iterdir():
                if child.is_dir() and (child / 'features').is_dir():
                    features_dir = child / 'features'
                    break
    skip_names = {'graph.json', 'README.md', 'feature-format.md'}
    all_feature_files = sorted(
        p for p in features_dir.rglob('*')
        if p.suffix in ('.json', '.md') and p.name not in skip_names
    )

    features = {}
    file_to_features = defaultdict(list)

    for p in all_feature_files:
        try:
            if p.suffix == '.json':
                with open(p) as f:
                    data = json.load(f)
            elif p.suffix == '.md':
                content = p.read_text(encoding='utf-8')
                if not content.startswith('---'):
                    continue
                end = content.find('---', 3)
                if end == -1:
                    continue
                import yaml
                fm = yaml.safe_load(content[3:end])
                if not isinstance(fm, dict) or 'name' not in fm:
                    continue
                # 从 MD 正文提取文件路径
                import re
                body = content[end + 3:]
                files = {"code": [], "config": [], "asset": [], "template": []}
                section_map = {"代码文件": "code", "配置文件": "config", "资源文件": "asset", "模板文件": "template", "场景": "asset"}
                current = None
                for line in body.split('\n'):
                    hm = re.match(r'^##\s+(.+)', line)
                    if hm:
                        current = section_map.get(hm.group(1).strip())
                        continue
                    if current and '`' in line and '|' in line:
                        pm = re.search(r'`(Assets/[^`]+)`', line)
                        if pm:
                            files[current].append(pm.group(1))
                data = dict(fm)
                data['files'] = files
            else:
                continue
        except Exception:
            continue
        
        name = data.get('name', p.stem)
        features[name] = data
        features[name]['_path'] = str(p.relative_to(project_root))

        for cat in ['code', 'config', 'asset', 'template']:
            for fp in data['files'].get(cat, []):
                file_to_features[fp].append(name)

    return features, file_to_features


def load_manifest(project_root):
    """从 manifest.md 提取文件路径"""
    manifest_path = project_root / 'aigc' / 'harness' / 'version' / 'manifest.md'
    manifest_files = set()

    if manifest_path.exists():
        with open(manifest_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('| Assets/'):
                    path = line.split('|')[1].strip()
                    manifest_files.add(path)

    return manifest_files


def scan_project_files(project_root, extensions=None):
    """扫描项目中的所有代码/配置文件（从 wiki-env.json 读取代码根路径）"""
    if extensions is None:
        extensions = {'.cs', '.csv'}

    scripts_dir = get_script_dir(project_root)
    configs_dir = project_root / 'Assets' / 'Bundle' / 'Configs'

    all_files = set()

    for search_dir in [scripts_dir, configs_dir]:
        if search_dir.exists():
            for ext in extensions:
                for p in search_dir.rglob(f'*{ext}'):
                    rel = str(p.relative_to(project_root))
                    all_files.add(rel)

    return all_files


EXCLUDE_DIRS = {
    '3rd', 'SDK', 'SoFunny', 'Mirror', 'DOTween', 'UIParticle',
    'PlayableEditor', 'Grpc', 'Editor', 'Plugins',
    'PerfAnalyzer', 'WebSocket', 'HybridCLR', 'Obfuz',
}

CATEGORY_PATTERNS = {
    'UI': [r'/UI/', r'/UIControl/', r'/UIView/', r'UI_', r'UIMessage'],
    'Character': [r'/Character/', r'Character\.cs'],
    'Weapon': [r'/Weapon/', r'Weapon\.cs'],
    'EventDirector': [r'/EventDirector/'],
    'Network': [r'/Network/', r'/Grpc/'],
    'Data/Template': [r'/Template/', r'/data/'],
    'Mode': [r'/Mode/', r'Mode\.cs'],
    'GPO/AI': [r'/AI/', r'/GPO/', r'GPOM_', r'SAI_', r'CAI_'],
    'Ability': [r'/Ability/', r'AB_', r'AE_', r'SAB_', r'SAE_', r'CAB_', r'CAE_'],
    'Scene': [r'/Scene/', r'Scene\.cs'],
    'Component': [r'/Component/'],
}


def classify_file(filepath):
    """根据路径模式猜测文件分类"""
    for dir_name in EXCLUDE_DIRS:
        if f'/{dir_name}/' in filepath:
            return '3rd/SDK (不编目)'

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, filepath):
                return category

    return '其他'


def suggest_feature(filepath, features, file_to_features):
    """试验性：根据文件路径猜测应归属的功能包"""
    filename = os.path.basename(filepath)
    suggestions = []

    # GPO 类型匹配
    gpo_match = re.search(r'GPOM_(\w+)', filename) or re.search(r'SAI_?(\w+)', filename)
    if gpo_match:
        type_name = gpo_match.group(1)
        # 在已有 features 中找匹配
        for name, data in features.items():
            if data.get('category') == 'gpo' and type_name.lower() in name.lower():
                suggestions.append(f"gpo → {name}")

    # Ability AB 匹配
    ab_match = re.search(r'[SC]AB_(\w+)System', filename) or re.search(r'AbilityM_(\w+)', filename)
    if ab_match:
        type_name = ab_match.group(1)
        kebab = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', type_name).lower()
        for name, data in features.items():
            if data.get('category') == 'ability' and kebab in name:
                suggestions.append(f"ability/ab → {name}")

    # Ability AE 匹配
    ae_match = re.search(r'[SC]AE_(\w+)System', filename)
    if ae_match:
        type_name = ae_match.group(1)
        kebab = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', type_name).lower()
        for name, data in features.items():
            if data.get('category') == 'ability' and kebab in name:
                suggestions.append(f"ability/ae → {name}")

    # Mode 匹配
    mode_match = re.search(r'Server(\w+)Mode', filename) or re.search(r'Client(\w+)Mode', filename)
    if mode_match:
        type_name = mode_match.group(1)
        kebab = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', type_name).lower()
        for name, data in features.items():
            if data.get('category') == 'mode' and kebab in name:
                suggestions.append(f"mode → {name}")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description='功能目录覆盖率检测工具')
    parser.add_argument('--files', nargs='+', help='检查指定文件')
    parser.add_argument('--stdin', action='store_true', help='从 stdin 读取文件列表')
    parser.add_argument('--dir', help='检查指定目录下的文件')
    parser.add_argument('--summary', action='store_true', help='按分类汇总未覆盖文件')
    parser.add_argument('--suggest', action='store_true', help='试验性：建议文件归属')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    args = parser.parse_args()

    project_root = find_project_root()
    features, file_to_features = load_all_features(project_root)
    manifest_files = load_manifest(project_root)

    # 确定要检查的文件集
    if args.files:
        check_files = set(args.files)
    elif args.stdin:
        check_files = set(line.strip() for line in sys.stdin if line.strip())
    elif args.dir:
        dir_path = project_root / args.dir
        check_files = set()
        if dir_path.exists():
            for p in dir_path.rglob('*'):
                if p.suffix in {'.cs', '.csv', '.unity', '.prefab', '.asset'}:
                    check_files.add(str(p.relative_to(project_root)))
    else:
        check_files = scan_project_files(project_root)

    # 分类文件
    covered_by_feature = {}      # file → feature_names
    covered_by_manifest = set()  # manifest 覆盖的
    uncovered = set()            # 未覆盖
    excluded = set()             # 3rd/SDK

    for fp in sorted(check_files):
        if fp in file_to_features:
            covered_by_feature[fp] = file_to_features[fp]
        elif fp in manifest_files:
            covered_by_manifest.add(fp)
        elif classify_file(fp) == '3rd/SDK (不编目)':
            excluded.add(fp)
        else:
            uncovered.add(fp)

    total = len(check_files)
    n_feature = len(covered_by_feature)
    n_manifest = len(covered_by_manifest)
    n_excluded = len(excluded)
    n_uncovered = len(uncovered)
    coverage = (n_feature + n_manifest) / total * 100 if total > 0 else 0

    if args.json:
        result = {
            'total_files': total,
            'covered_by_feature': n_feature,
            'covered_by_manifest': n_manifest,
            'excluded_3rd': n_excluded,
            'uncovered': n_uncovered,
            'coverage_percent': round(coverage, 1),
            'uncovered_files': sorted(uncovered),
        }
        if args.suggest:
            result['suggestions'] = {}
            for fp in sorted(uncovered):
                sugg = suggest_feature(fp, features, file_to_features)
                if sugg:
                    result['suggestions'][fp] = sugg
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 文本输出
    print(f"{'='*60}")
    print(f"功能目录覆盖率报告")
    print(f"{'='*60}")
    print(f"扫描文件总数：{total}")
    print(f"├─ feature 文件 覆盖：{n_feature} ({n_feature/total*100:.1f}%)" if total else "")
    print(f"├─ manifest.md 覆盖：{n_manifest} ({n_manifest/total*100:.1f}%)" if total else "")
    print(f"├─ 3rd/SDK 排除：{n_excluded} ({n_excluded/total*100:.1f}%)" if total else "")
    print(f"└─ ⚠️ 未覆盖：{n_uncovered} ({n_uncovered/total*100:.1f}%)" if total else "")
    print(f"\n有效覆盖率（feature + manifest）：{coverage:.1f}%")
    print(f"功能包数量：{len(features)}（含分组索引）")

    if args.summary and uncovered:
        print(f"\n{'='*60}")
        print(f"未覆盖文件分类汇总")
        print(f"{'='*60}")

        by_category = defaultdict(list)
        for fp in sorted(uncovered):
            cat = classify_file(fp)
            by_category[cat].append(fp)

        for cat in sorted(by_category.keys(), key=lambda x: -len(by_category[x])):
            files = by_category[cat]
            print(f"\n  [{cat}] — {len(files)} 个文件")
            for fp in files[:5]:
                print(f"    {fp}")
            if len(files) > 5:
                print(f"    ... 还有 {len(files)-5} 个")

    elif uncovered and not args.summary:
        print(f"\n⚠️ 未覆盖文件（前 20 个）：")
        for fp in sorted(uncovered)[:20]:
            cat = classify_file(fp)
            line = f"  {fp}  [{cat}]"
            if args.suggest:
                sugg = suggest_feature(fp, features, file_to_features)
                if sugg:
                    line += f"  → 建议: {', '.join(sugg)}"
            print(line)
        if len(uncovered) > 20:
            print(f"  ... 还有 {len(uncovered)-20} 个")

    # 检查重复归属
    duplicates = {fp: names for fp, names in file_to_features.items() if len(names) > 1}
    if duplicates:
        print(f"\n⚠️ 重复归属（同一文件在多个功能包中）：")
        for fp, names in sorted(duplicates.items())[:10]:
            print(f"  {os.path.basename(fp)} → {', '.join(names)}")

    # 写入 wiki/log.md
    import sys; sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); from wiki_log import append_wiki_log
    append_wiki_log("lint", "feature 覆盖率检查",
                    f"扫描所有代码文件归属情况，总文件: {total}，已覆盖: {total - n_uncovered}（{coverage:.1f}%），未覆盖: {n_uncovered}")


if __name__ == '__main__':
    main()
