#!/usr/bin/env python3
"""
feature-check.py — Feature 漂移检测工具

从 wiki-env.json 读取仓库配置和 sync commit，对比各子仓库到当前 HEAD，
检测 feature 知识库是否覆盖了所有新增/删除的代码文件。

用法：
  python3 feature-check.py                # 检测所有仓库
  python3 feature-check.py --repo script  # 只检查指定仓库

退出码：
  0 = 无漂移
  1 = 有漂移

由 wiki-sync.py 调度调用，也可独立运行。
"""

import os, sys, subprocess, re, json, yaml, io

# Windows GBK 终端兼容：强制 stdout/stderr 为 UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_root():
    """向上查找含 aigc/wiki/ 的项目根目录"""
    d = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
    if os.path.exists(os.path.join(d, "aigc/wiki")):
        return d
    d = os.path.abspath(".")
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "aigc/wiki")):
            return d
        d = os.path.dirname(d)
    return os.path.abspath(".")


PROJECT_ROOT = find_project_root()
ENV_FILE = os.path.join(PROJECT_ROOT, "aigc/wiki/wiki-env.json")


# ─── wiki-env.json ───

def load_env():
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE, encoding='utf-8') as f:
        return json.load(f)


# ─── Git 操作 ───

def get_repo_head(repo_path):
    abs_path = os.path.join(PROJECT_ROOT, repo_path)
    if not os.path.isdir(abs_path):
        return None
    try:
        r = subprocess.run(
            ['git', 'rev-parse', '--short=12', 'HEAD'],
            capture_output=True, text=True, cwd=abs_path
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except FileNotFoundError:
        return None


def git_diff_files(repo_path, since_commit, file_globs):
    abs_path = os.path.join(PROJECT_ROOT, repo_path)
    if not os.path.isdir(abs_path):
        return [], [], []

    glob_args = []
    for g in file_globs:
        glob_args.extend(['--', g])

    try:
        result = subprocess.run(
            ['git', 'diff', '--name-status', f'{since_commit}..HEAD'] + glob_args,
            capture_output=True, text=True, cwd=abs_path
        )
        if result.returncode != 0:
            return [], [], []
    except FileNotFoundError:
        return [], [], []

    added, deleted, modified = [], [], []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        status = parts[0]
        filepath = parts[-1]

        if repo_path != ".":
            filepath = f"{repo_path}/{filepath}"

        if status == 'A':
            added.append(filepath)
        elif status == 'D':
            deleted.append(filepath)
        elif status.startswith('M'):
            modified.append(filepath)
        elif status.startswith('R') and len(parts) >= 3:
            old = f"{repo_path}/{parts[1]}" if repo_path != "." else parts[1]
            new = f"{repo_path}/{parts[2]}" if repo_path != "." else parts[2]
            deleted.append(old)
            added.append(new)

    return added, deleted, modified


# ─── Feature 加载 ───

def load_all_features(features_dir):
    if not features_dir or not os.path.isdir(features_dir):
        return {}
    features = {}
    for root, dirs, files in os.walk(features_dir):
        for f in files:
            if not f.endswith('.md') or f.startswith('_'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding='utf-8-sig') as fh:
                    content = fh.read().lstrip('\ufeff')
            except Exception:
                continue
            if not content.startswith('---'):
                continue
            end = content.find('---', 3)
            if end == -1:
                continue
            try:
                meta = yaml.safe_load(content[3:end]) or {}
            except yaml.YAMLError:
                continue
            name = meta.get('name', f.replace('.md', ''))

            all_paths = set()
            for line in content[end+3:].split('\n'):
                m = re.search(r'`(Assets/[^`]+)`', line)
                if m:
                    all_paths.add(m.group(1))

            features[name] = {
                'paths': all_paths,
                'category': meta.get('category', ''),
            }
    return features


def check_coverage(added, features):
    path_to_feature = {}
    for name, info in features.items():
        for p in info['paths']:
            path_to_feature[p] = name

    uncovered, new_buffs = [], []
    for fp in added:
        if fp in path_to_feature:
            continue
        uncovered.append(fp)
        bn = os.path.basename(fp)
        if bn.startswith('BSO') and bn.endswith('.cs'):
            bs = bn.replace('BSO', '').replace('.cs', '')
            kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', bs).lower()
            expected = f"buff-{kebab}"
            if expected not in features:
                new_buffs.append((fp, expected))
    return uncovered, new_buffs


def check_stale_refs(deleted, features):
    stale = []
    for fp in deleted:
        for name, info in features.items():
            if fp in info['paths']:
                stale.append((fp, name))
    return stale


# ─── Main ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Feature 漂移检测')
    parser.add_argument('--repo', help='只检查指定仓库 key')
    args = parser.parse_args()

    env = load_env()
    if not env:
        print(f"❌ 未找到 {ENV_FILE}")
        sys.exit(1)

    repos_conf = env.get('repos', {})
    sync = env.get('sync', {})
    features_dir_rel = env.get('features_dir', '')
    features_dir = os.path.join(PROJECT_ROOT, features_dir_rel) if features_dir_rel else None

    repo_keys = list(repos_conf.keys())
    if args.repo:
        if args.repo not in repos_conf:
            print(f"❌ 未知仓库: {args.repo}，可选: {', '.join(repo_keys)}")
            sys.exit(1)
        repo_keys = [args.repo]

    # 获取各仓库 HEAD
    heads = {}
    for key in repo_keys:
        info = repos_conf[key]
        heads[key] = get_repo_head(info['path'])

    print(f"{'仓库':<10} {'基准':>14} {'当前':>14}  状态")
    print(f"{'-'*10} {'-'*14} {'-'*14}  {'-'*10}")

    for key in repo_keys:
        s = sync.get(key, '(未设置)')
        h = heads.get(key) or '(不存在)'
        if not heads.get(key):
            status = "⏭️  跳过"
        elif s == '(未设置)':
            status = "🆕 首次"
        elif s == h:
            status = "✅ 同步"
        else:
            status = "🔍 待检"
        print(f"{key:<10} {s:>14} {h:>14}  {status}")
    print()

    # 加载 features
    features = load_all_features(features_dir)
    print(f"已加载 {len(features)} 个 feature\n")

    # 逐仓库检查
    has_drift = False
    for key in repo_keys:
        if not heads.get(key):
            continue
        s = sync.get(key)
        if not s or s == heads[key]:
            continue

        info = repos_conf[key]
        added, deleted, modified = git_diff_files(info['path'], s, info.get('globs', ['*.cs']))
        if not added and not deleted:
            continue

        print(f"{'='*50}")
        print(f"📦 {key} ({info['path']})")
        print(f"   新增: {len(added)}  删除: {len(deleted)}  修改: {len(modified)}")

        if added and features:
            uncovered, new_buffs = check_coverage(added, features)
            if uncovered:
                has_drift = True
                print(f"\n   ⚠️  新增未覆盖 ({len(uncovered)}):")
                for p in uncovered[:15]:
                    print(f"      + {p}")
                if len(uncovered) > 15:
                    print(f"      ... 还有 {len(uncovered)-15} 个")
            if new_buffs:
                print(f"\n   🆕 疑似新 Buff:")
                for p, expected in new_buffs:
                    print(f"      {os.path.basename(p)} → {expected}.md")

        if deleted and features:
            stale = check_stale_refs(deleted, features)
            if stale:
                has_drift = True
                print(f"\n   🗑️  已删除仍引用 ({len(stale)}):")
                for p, fname in stale[:15]:
                    print(f"      - {p}  ↳ {fname}")
        print()

    if has_drift:
        print("⚠️  feature 漂移")
        sys.exit(1)
    else:
        print("✅ feature 无漂移")
        sys.exit(0)


if __name__ == '__main__':
    main()
