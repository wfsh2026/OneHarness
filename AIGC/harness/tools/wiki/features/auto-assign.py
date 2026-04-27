#!/usr/bin/env python3
"""
Feature 自动归属工具
==================
检测未被任何 feature 覆盖的文件，并根据目录归属和命名模式
自动（或建议性地）将它们添加到正确的 feature（.md 或 .json）。

支持从 wiki-env.json 读取代码根路径，兼容 Assets/Scripts 和 Assets/Script。

用途：
  - 从下游项目同步新文件回 framework 后，自动更新功能目录
  - 检测手动新增但忘记编目的文件
  - 配合 git diff 增量检测新增文件

用法：
  # 干运行：扫描所有未覆盖文件，显示归属建议（默认）
  python3 aigc/harness/tools/wiki/features/auto-assign.py

  # 写入模式：把高置信度归属写入 feature 文件
  python3 aigc/harness/tools/wiki/features/auto-assign.py --write

  # 只处理指定文件
  python3 aigc/harness/tools/wiki/features/auto-assign.py --files Assets/Scripts/GamePlay/Server/AI/SAI_NewUnit.cs

  # 配合 git diff
  git diff --name-only HEAD~1 | python3 aigc/harness/tools/wiki/features/auto-assign.py --stdin

  # 写入后自动重建索引
  python3 aigc/harness/tools/wiki/features/auto-assign.py --write --rebuild

  # 显示详细匹配过程
  python3 aigc/harness/tools/wiki/features/auto-assign.py --verbose

依赖：
  pyyaml（用于解析 .md frontmatter）
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# ── 常量 ──

EXTENSIONS_CODE = {'.cs'}
EXTENSIONS_CONFIG = {'.csv', '.asset'}
EXTENSIONS_ASSET = {'.png', '.prefab', '.mat', '.anim', '.controller'}

# 排除的目录（和 check-coverage.py 保持一致）
EXCLUDE_DIRS = {
    '3rd', 'SDK', 'SoFunny', 'Mirror', 'DOTween', 'UIParticle',
    'PlayableEditor', 'Grpc', 'Editor', 'Plugins',
    'PerfAnalyzer', 'WebSocket', 'HybridCLR', 'Obfuz',
}

# 置信度阈值：只有 >= HIGH 才会在 --write 时自动写入
CONFIDENCE_HIGH = 'high'
CONFIDENCE_MEDIUM = 'medium'
CONFIDENCE_LOW = 'low'
CONFIDENCE_NONE = 'none'

# 叶目录多数投票阈值
MAJORITY_THRESHOLD = 0.65


# ── 工具函数 ──

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
        with open(env_path) as f:
            return json.load(f)
    return None


def get_script_dir(project_root):
    """从 wiki-env.json 获取代码根路径，fallback 到 Assets/Scripts"""
    env = load_wiki_env(project_root)
    if env and 'repos' in env:
        script_repo = env['repos'].get('script', {})
        if 'path' in script_repo:
            return project_root / script_repo['path']
    for name in ['Assets/Scripts', 'Assets/Script']:
        p = project_root / name
        if p.exists():
            return p
    return project_root / 'Assets' / 'Scripts'


def is_excluded(filepath):
    for d in EXCLUDE_DIRS:
        if f'/{d}/' in filepath:
            return True
    return False


def classify_file_category(filepath):
    """根据路径和扩展名判断 feature 文件 中的 files 分类"""
    ext = Path(filepath).suffix.lower()
    if ext in EXTENSIONS_ASSET:
        return 'asset'
    if ext in EXTENSIONS_CONFIG:
        return 'config'
    if ext in EXTENSIONS_CODE:
        if '/Template/' in filepath:
            return 'template'
        if '/Data/' in filepath and '/Data/Configs/' not in filepath:
            return 'config'
        if '/Data/Configs/' in filepath:
            return 'config'
        return 'code'
    return 'code'


# ── 数据加载 ──

def load_features(project_root):
    """加载所有 feature（.md 和 .json），返回 {name: data} + {file: [names]} + {name: path}"""
    features_dir = project_root / 'aigc' / 'wiki' / 'raw' / 'features'
    if not features_dir.exists():
        raw_dir = project_root / 'aigc' / 'wiki' / 'raw'
        if raw_dir.exists():
            for child in raw_dir.iterdir():
                if child.is_dir() and (child / 'features').is_dir():
                    features_dir = child / 'features'
                    break
    # 也检查 wiki-env.json 的 features_dir
    env = load_wiki_env(project_root)
    if env and 'features_dir' in env:
        candidate = project_root / env['features_dir']
        if candidate.is_dir():
            features_dir = candidate

    skip = {'graph.json', 'README.md', 'feature-format.md'}
    features = {}
    file_to_features = defaultdict(list)
    feature_paths = {}

    for p in sorted(features_dir.rglob('*')):
        if p.suffix not in ('.json', '.md') or p.name in skip or p.name.startswith('_index'):
            continue
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
        feature_paths[name] = p
        for cat in ['code', 'config', 'asset', 'template']:
            for fp in data.get('files', {}).get(cat, []):
                file_to_features[fp].append(name)

    return features, file_to_features, feature_paths


def scan_all_files(project_root):
    """扫描项目中所有应该被编目的文件（从 wiki-env.json 读取代码根路径）"""
    exts = {'.cs', '.csv'}
    scripts_dir = get_script_dir(project_root)
    dirs = [
        scripts_dir,
        project_root / 'Assets' / 'Bundle' / 'Configs',
    ]
    result = set()
    for d in dirs:
        if not d.exists():
            continue
        for ext in exts:
            for p in d.rglob(f'*{ext}'):
                result.add(str(p.relative_to(project_root)))
    return result


# ── 目录归属索引 ──

def build_dir_ownership(file_to_features):
    """构建叶目录 → {feature: count} 映射"""
    ownership = defaultdict(lambda: defaultdict(int))
    for filepath, feat_names in file_to_features.items():
        d = '/'.join(filepath.split('/')[:-1])
        for fn in feat_names:
            ownership[d][fn] += 1
    return ownership


# ── 命名模式匹配 ──

# 模式 → (category, feature_name_builder)
NAMING_PATTERNS = [
    # GPO: GPOM_Tank → gpo:tank, SAI_TankSystem → gpo:tank
    (r'GPOM_(\w+)', 'gpo'),
    (r'[SC]AI_(\w+?)(?:System)?$', 'gpo'),
    # AB: SAB_BlitzSystem → ability/ab:ab-blitz
    (r'[SC]AB_(\w+?)System$', 'ability_ab'),
    (r'AbilityM_(\w+)$', 'ability_ab'),
    # AE: SAE_AddDamageByHpRateSystem → ability/ae:ae-add-damage-by-hp-rate
    (r'[SC]AE_(\w+?)System$', 'ability_ae'),
    # Mode: ServerGoldRushMode → mode:mode-goldrush
    # 也匹配 ServerGoldRushMode_SubPart 形式
    (r'(?:Server|Client)(\w+?)Mode(?:_|$)', 'mode'),
    # UI: UIE_PersonalSpace → ui:ui-personal-space, UIControl_Chat → ui:ui-chat
    (r'UIE_(\w+)', 'ui'),
    (r'UIControl_(\w+)', 'ui'),
    # SceneGPO
    (r'[SC]GPO_(\w+)', 'gpo'),
]


def camel_to_kebab(name):
    """CamelCase → kebab-case"""
    s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '-', name)
    s = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '-', s)
    return s.lower()


def _find_candidates(kebab, features, category_filter, prefix_filter=None):
    """在 features 中查找匹配候选。支持正向和反向 contains 匹配。
    使用去连字符的规范化比较，解决 gold-rush vs goldrush 类问题。"""
    candidates = []
    kebab_norm = kebab.replace('-', '')

    for name, data in features.items():
        if data.get('category') != category_filter:
            continue
        if prefix_filter and not name.startswith(prefix_filter):
            continue
        core = name[len(prefix_filter):] if prefix_filter and name.startswith(prefix_filter) else name
        if category_filter == 'mode' and core.startswith('mode-'):
            core = core[5:]
        core_norm = core.replace('-', '')

        # 规范化比较（去掉连字符后做 contains）
        if kebab_norm in name.replace('-', '') or core_norm in kebab_norm:
            candidates.append(name)
    return candidates


def try_naming_pattern(filepath, features):
    """尝试通过文件名模式匹配到具体 feature"""
    stem = Path(filepath).stem

    for pattern, category in NAMING_PATTERNS:
        m = re.search(pattern, stem)
        if not m:
            continue
        type_name = m.group(1)
        kebab = camel_to_kebab(type_name)

        if category == 'gpo':
            candidates = _find_candidates(kebab, features, 'gpo')
        elif category == 'ability_ab':
            candidates = _find_candidates(kebab, features, 'ability', 'ab-')
        elif category == 'ability_ae':
            candidates = _find_candidates(kebab, features, 'ability', 'ae-')
        elif category == 'mode':
            candidates = _find_candidates(kebab, features, 'mode')
        elif category == 'ui':
            candidates = _find_candidates(kebab, features, 'ui', 'ui-')
        else:
            candidates = []

        # 精确匹配优先
        exact = [c for c in candidates if kebab == (c.split('-', 1)[-1] if '-' in c else c)]
        if exact:
            return exact[0], CONFIDENCE_HIGH, f'naming:{stem}→{kebab}'
        if len(candidates) == 1:
            return candidates[0], CONFIDENCE_HIGH, f'naming:{stem}→{kebab}'
        if candidates:
            return candidates[0], CONFIDENCE_MEDIUM, f'naming:{stem}→{kebab}(ambiguous:{candidates})'

    return None, CONFIDENCE_NONE, ''


def try_directory_ownership(filepath, dir_ownership, features):
    """尝试通过目录归属匹配 feature"""
    leaf_dir = '/'.join(filepath.split('/')[:-1])

    feats = dir_ownership.get(leaf_dir, {})
    if not feats:
        # 尝试父目录
        parent_dir = '/'.join(leaf_dir.split('/')[:-1])
        feats = dir_ownership.get(parent_dir, {})
        if not feats:
            return None, CONFIDENCE_NONE, ''

    if len(feats) == 1:
        name = list(feats.keys())[0]
        count = list(feats.values())[0]
        return name, CONFIDENCE_HIGH, f'dir-single:{leaf_dir}({count} siblings)'

    # 多数投票
    total = sum(feats.values())
    dominant = max(feats.items(), key=lambda x: x[1])
    ratio = dominant[1] / total

    if ratio >= MAJORITY_THRESHOLD:
        return dominant[0], CONFIDENCE_MEDIUM, f'dir-majority:{leaf_dir}({dominant[0]}={dominant[1]}/{total}={ratio:.0%})'

    # 看看能否结合 base 逻辑：如果除去 base features 后只剩一个
    base_features = {
        'manifest', 'mode-base', 'gpo-base', 'ability-base', 'ui-base',
        'game-core', 'game-server', 'character-base', 'weapon-base',
        'network-base', 'data-model', 'event-director', 'component-shared',
        'utils-base', 'template-data', 'template-infra', 'scene-base',
        'camera-base', 'item-base', 'ab-hero-skill-infra', 'war-report',
        'ui-battle-hud', 'gameplay-tag',
    }
    non_base = {k: v for k, v in feats.items() if k not in base_features}
    if len(non_base) == 1:
        name = list(non_base.keys())[0]
        return name, CONFIDENCE_MEDIUM, f'dir-non-base:{leaf_dir}({name})'

    return None, CONFIDENCE_LOW, f'dir-ambiguous:{leaf_dir}({dict(feats)})'


# ── 主逻辑 ──

def assign_file(filepath, features, dir_ownership):
    """对一个文件尝试自动归属，返回 (feature_name, confidence, reason)"""
    # 1. 命名模式（最高优先级）
    name, conf, reason = try_naming_pattern(filepath, features)
    if name:
        return name, conf, reason

    # 2. 目录归属
    name, conf, reason = try_directory_ownership(filepath, dir_ownership, features)
    if name:
        return name, conf, reason

    return None, CONFIDENCE_NONE, 'no-match'


def write_assignments(assignments, feature_paths, features, project_root, verbose=False):
    """把归属结果写入对应的 feature 文件（.md 或 .json）"""
    # Group by feature
    by_feature = defaultdict(list)
    for filepath, feat_name, cat in assignments:
        by_feature[feat_name].append((filepath, cat))

    updated = 0
    for feat_name, file_list in sorted(by_feature.items()):
        if feat_name not in feature_paths:
            print(f"  ⚠️ Feature '{feat_name}' 的文件不存在，跳过")
            continue

        feat_path = feature_paths[feat_name]

        if feat_path.suffix == '.json':
            # JSON 格式写回
            with open(feat_path) as f:
                data = json.load(f)
            changed = False
            for filepath, cat in file_list:
                existing = data.get('files', {}).get(cat, [])
                if filepath not in existing:
                    existing.append(filepath)
                    existing.sort()
                    data.setdefault('files', {}).setdefault(cat, existing)
                    changed = True
                    if verbose:
                        print(f"  ✅ {filepath} → {feat_name} [{cat}]")
            if changed:
                with open(feat_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write('\n')
                updated += 1

        elif feat_path.suffix == '.md':
            # MD 格式写回：在「## 代码文件」表格末尾追加行
            content = feat_path.read_text(encoding='utf-8')
            changed = False
            section_names = {"code": "代码文件", "config": "配置文件", "asset": "资源文件", "template": "模板文件"}

            for filepath, cat in file_list:
                if f'`{filepath}`' in content:
                    continue  # 已存在
                section = section_names.get(cat, "代码文件")
                marker = f'## {section}'
                if marker in content:
                    # 找到表格末尾（连续 | 行的最后一行之后）
                    lines = content.split('\n')
                    insert_idx = None
                    in_section = False
                    for i, line in enumerate(lines):
                        if line.strip().startswith(f'## {section}'):
                            in_section = True
                            continue
                        if in_section:
                            if line.strip().startswith('|') and '`' in line:
                                insert_idx = i + 1
                            elif line.strip().startswith('##') or (insert_idx and not line.strip().startswith('|') and line.strip() != ''):
                                break
                    if insert_idx:
                        lines.insert(insert_idx, f'| `{filepath}` |')
                        content = '\n'.join(lines)
                        changed = True
                        if verbose:
                            print(f"  ✅ {filepath} → {feat_name} [{cat}]")
                else:
                    # 没有对应段落，在文件末尾追加
                    content = content.rstrip('\n') + f'\n\n## {section}\n\n| 路径 |\n|------|\n| `{filepath}` |\n'
                    changed = True
                    if verbose:
                        print(f"  ✅ {filepath} → {feat_name} [{cat}] (新增段落)")

            if changed:
                feat_path.write_text(content, encoding='utf-8')
                updated += 1

    return updated


def main():
    parser = argparse.ArgumentParser(
        description='Feature 自动归属工具 — 未覆盖文件自动添加到 feature 文件'
    )
    parser.add_argument('--files', nargs='+', help='指定文件路径')
    parser.add_argument('--stdin', action='store_true', help='从 stdin 读取文件列表')
    parser.add_argument('--write', action='store_true', help='写入模式（只写入 high 置信度）')
    parser.add_argument('--write-medium', action='store_true',
                        help='写入模式 + 包含 medium 置信度')
    parser.add_argument('--rebuild', action='store_true',
                        help='写入后重建 wiki-map.json')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细匹配过程')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    args = parser.parse_args()

    project_root = find_project_root()
    features, file_to_features, feature_paths = load_features(project_root)
    dir_ownership = build_dir_ownership(file_to_features)

    # 确定要处理的文件
    if args.files:
        target_files = set(args.files)
    elif args.stdin:
        target_files = set(line.strip() for line in sys.stdin if line.strip())
    else:
        all_files = scan_all_files(project_root)
        target_files = set()
        for fp in all_files:
            if fp not in file_to_features and not is_excluded(fp):
                target_files.add(fp)

    if not target_files:
        print("✅ 没有未覆盖文件需要归属")
        return

    # 逐文件归属
    results = []
    for fp in sorted(target_files):
        feat_name, conf, reason = assign_file(fp, features, dir_ownership)
        cat = classify_file_category(fp) if feat_name else None
        results.append({
            'file': fp,
            'feature': feat_name,
            'category': cat,
            'confidence': conf,
            'reason': reason,
        })

    # 统计
    high = [r for r in results if r['confidence'] == CONFIDENCE_HIGH]
    medium = [r for r in results if r['confidence'] == CONFIDENCE_MEDIUM]
    low = [r for r in results if r['confidence'] == CONFIDENCE_LOW]
    none_ = [r for r in results if r['confidence'] == CONFIDENCE_NONE]

    if args.json:
        output = {
            'total': len(results),
            'high': len(high),
            'medium': len(medium),
            'low': len(low),
            'none': len(none_),
            'results': results,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # 文本输出
    print(f"{'='*60}")
    print(f"Feature 自动归属报告")
    print(f"{'='*60}")
    print(f"待归属文件：{len(results)}")
    print(f"├─ 🟢 high（可自动写入）：{len(high)}")
    print(f"├─ 🟡 medium（建议确认）：{len(medium)}")
    print(f"├─ 🟠 low（需人工判断）：{len(low)}")
    print(f"└─ 🔴 none（无法归属）：{len(none_)}")

    if high:
        print(f"\n🟢 HIGH 置信度 ({len(high)} 个):")
        for r in high:
            print(f"  {r['file']}")
            print(f"    → {r['feature']} [{r['category']}]  ({r['reason']})")

    if medium:
        print(f"\n🟡 MEDIUM 置信度 ({len(medium)} 个):")
        for r in medium:
            print(f"  {r['file']}")
            print(f"    → {r['feature']} [{r['category']}]  ({r['reason']})")

    if low and args.verbose:
        print(f"\n🟠 LOW 置信度 ({len(low)} 个):")
        for r in low:
            print(f"  {r['file']}")
            print(f"    → {r['reason']}")

    if none_ and args.verbose:
        print(f"\n🔴 无法归属 ({len(none_)} 个):")
        for r in none_:
            print(f"  {r['file']}")

    # 写入
    if args.write or args.write_medium:
        write_list = []
        for r in high:
            write_list.append((r['file'], r['feature'], r['category']))
        if args.write_medium:
            for r in medium:
                write_list.append((r['file'], r['feature'], r['category']))

        if write_list:
            level = 'high+medium' if args.write_medium else 'high'
            print(f"\n📝 写入 {len(write_list)} 个归属 ({level})...")
            n = write_assignments(write_list, feature_paths, features, project_root, args.verbose)
            print(f"✅ 更新了 {n} 个 feature 文件")

            import sys; sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); from wiki_log import append_wiki_log
            append_wiki_log("ingest", "feature 自动归属",
                            f"按目录规则自动归属未编目文件，写入 {n} 个 feature 文件（匹配级别: {level}）")

            if args.rebuild:
                print("\n🔄 重建索引...")
                script = project_root / 'aigc' / 'harness' / 'tools' / 'wiki' / 'wiki-resolve.py'
                subprocess.run([sys.executable, str(script), '--build'], cwd=str(project_root))
        else:
            print("\n⚠️ 没有符合写入条件的归属")
    else:
        writable = len(high) + (len(medium) if args.write_medium else 0)
        if writable > 0:
            print(f"\n💡 提示：加 --write 可自动写入 {len(high)} 个 high 置信度归属")
            if medium:
                print(f"         加 --write-medium 可额外包含 {len(medium)} 个 medium 置信度")


if __name__ == '__main__':
    main()
