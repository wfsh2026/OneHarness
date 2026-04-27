#!/usr/bin/env python3
"""
wiki-sync.py — Wiki 知识库管理中枢

纯调度器，按顺序调用各子工具完成 wiki 全量同步：
  1. feature-check.py    — feature 漂移检测
  2. check-system-map.py — system-map 同步检查
  3. wiki-resolve.py     — wiki-map 重建 + 断链检查
  4. build-glossary.py   — 名词表重建

用法：
  python3 wiki-sync.py                    # 全量检查（只读）
  python3 wiki-sync.py --update           # 全量同步（自动写入 + 更新基准）
  python3 wiki-sync.py --init             # 首次初始化
  python3 wiki-sync.py --repo script      # 只检查指定仓库

--update 执行流程：
  1. feature 漂移检测 → 有漂移则中止
  2. check-system-map.py --sync → 自动插骨架行
  3. wiki-resolve.py --build → 重建 wiki-map
  4. wiki-resolve.py --check → 断链检查
  5. build-glossary.py --write → 重建名词表
  6. build-wiki-html.py → 生成离线 Wiki HTML 检索页面
  7. 更新 wiki-env.json 基准 commit
"""

import os, sys, subprocess, json, io

# Windows GBK 终端兼容：强制 stdout/stderr 为 UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_TOOLS_DIR = os.path.join(SCRIPT_DIR, '..')


def find_project_root():
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


# ─── 工具路径 ───

def tool_path(name):
    """查找工具脚本路径"""
    # features/ 子目录
    p = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(p):
        return p
    # wiki/ 目录
    p = os.path.join(WIKI_TOOLS_DIR, name)
    if os.path.exists(p):
        return p
    return None


# ─── 子工具调用 ───

def run_tool(script_path, args=None, label=None, capture=False):
    """调用子工具，返回 (returncode, stdout+stderr)"""
    if not script_path or not os.path.exists(script_path):
        name = os.path.basename(script_path) if script_path else '?'
        print(f"  ⚠️  未找到 {name}，跳过")
        return -1, ''

    cmd = [sys.executable, script_path] + (args or [])
    env = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    if capture:
        r = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
        output = ((r.stdout or '') + (r.stderr or '')).strip()
        return r.returncode, output
    else:
        r = subprocess.run(cmd, cwd=PROJECT_ROOT, env=env)
        return r.returncode, ''


# ─── wiki-env.json ───

def load_env():
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE, encoding='utf-8') as f:
        return json.load(f)


def save_env(env):
    with open(ENV_FILE, 'w', encoding='utf-8') as f:
        json.dump(env, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"  ✅ wiki-env.json 已更新")


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


# ─── Init（委托给 feature-check 的 init 逻辑，或独立实现）───

def do_init():
    """扫描项目目录，自动发现子仓库，生成 wiki-env.json"""
    print("🔍 扫描子目录发现 git 仓库...\n")

    repos = {}
    head = get_repo_head(".")
    if head:
        repos["client"] = {"path": ".", "globs": ["*.cs", "*.unity"]}
        print(f"  发现: . → {head}")

    assets_dir = os.path.join(PROJECT_ROOT, "Assets")
    if os.path.isdir(assets_dir):
        for entry in sorted(os.scandir(assets_dir), key=lambda e: e.name):
            if entry.is_dir():
                git_path = os.path.join(entry.path, ".git")
                if os.path.exists(git_path):
                    rel = os.path.relpath(entry.path, PROJECT_ROOT)
                    h = get_repo_head(rel)
                    if h:
                        key = entry.name.lower().replace(' ', '-')
                        repos[key] = {"path": rel, "globs": ["*.cs"]}
                        print(f"  发现: {rel} → {h}")
                    for sub in sorted(os.scandir(entry.path), key=lambda e: e.name):
                        if sub.is_dir() and os.path.exists(os.path.join(sub.path, ".git")):
                            rel2 = os.path.relpath(sub.path, PROJECT_ROOT)
                            h2 = get_repo_head(rel2)
                            if h2:
                                key2 = sub.name.lower().replace(' ', '-')
                                repos[key2] = {"path": rel2, "globs": ["*.cs"]}
                                print(f"  发现: {rel2} → {h2}")

    if not repos:
        print("  未发现 git 仓库")
        return

    sync = {}
    for key, info in repos.items():
        h = get_repo_head(info["path"])
        if h:
            sync[key] = h

    features_dir = ""
    for candidate in ["aigc/wiki/raw", "AIGC/knowledge/features"]:
        full = os.path.join(PROJECT_ROOT, candidate)
        if os.path.isdir(full):
            for root, dirs, files in os.walk(full):
                if any(f.endswith('.md') for f in files):
                    features_dir = os.path.relpath(root, PROJECT_ROOT)
                    break
            if features_dir:
                break

    env = {
        "project": os.path.basename(PROJECT_ROOT),
        "display_name": os.path.basename(PROJECT_ROOT),
        "engine": "unity",
        "features_dir": features_dir,
        "repos": repos,
        "sync": sync,
    }

    print(f"\n📄 生成 wiki-env.json ({len(repos)} 仓库)")
    save_env(env)


# ─── Main ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Wiki 知识库管理中枢')
    parser.add_argument('--update', action='store_true',
                        help='全量同步：feature 检查 → system-map --sync → wiki-map 重建 → 名词表重建 → 更新基准')
    parser.add_argument('--repo', help='只检查指定仓库 key')
    parser.add_argument('--init', action='store_true',
                        help='首次初始化：扫描发现仓库生成 wiki-env.json')
    args = parser.parse_args()

    if args.init:
        do_init()
        return

    env = load_env()
    if not env:
        print(f"❌ 未找到 {ENV_FILE}")
        print("   运行 --init 自动生成")
        sys.exit(1)

    display_name = env.get('display_name', env.get('project', '?'))
    print(f"📊 Wiki 知识库同步 — {display_name}\n")

    # ═══ Step 1: Feature 漂移检测 ═══
    print("─── Step 1: Feature 漂移检测 ───")
    feature_script = tool_path('feature-check.py')
    feature_args = ['--repo', args.repo] if args.repo else []
    rc, output = run_tool(feature_script, feature_args, capture=True)
    has_feature_drift = (rc != 0 and rc != -1)
    if output:
        print(output)
    print()

    # ═══ Step 2: System-map 同步检查 ═══
    print("─── Step 2: System-map 同步检查 ───")
    sysmap_script = tool_path('check-system-map.py')
    sysmap_args = ['--sync'] if args.update else []
    rc, output = run_tool(sysmap_script, sysmap_args, capture=True)
    has_sysmap_drift = '🆕' in output
    if has_sysmap_drift:
        print(output)
    else:
        print("✅ system-map 无新增漂移")
    print()

    # ═══ Step 3: Wiki-map + 断链检查 ═══
    print("─── Step 3: Wiki-map 索引 ───")
    wiki_resolve = tool_path('wiki-resolve.py')
    if args.update:
        # 重建
        rc, output = run_tool(wiki_resolve, ['--build'], capture=True)
        print(output)
        # 断链检查
        rc, output = run_tool(wiki_resolve, ['--check'], capture=True)
        broken = output.count('❌') if output else 0
        if broken:
            print(f"  ⚠️  wiki-link 断链 {broken} 条（详情见 wiki-resolve.py --check）")
        else:
            print("✅ wiki-link 无断链")
    else:
        # 只检查不重建
        rc, output = run_tool(wiki_resolve, ['--check'], capture=True)
        if rc == 0:
            print("✅ wiki-link 无断链")
        else:
            broken = output.count('❌') if output else 0
            print(f"  ⚠️  wiki-link 断链 {broken} 条")
    print()

    # ═══ Step 4: 名词表 ═══
    print("─── Step 4: 名词表 ───")
    glossary_script = tool_path('build-glossary.py')
    if args.update:
        rc, output = run_tool(glossary_script, ['--write'], capture=True)
        print(output)
    else:
        print("ℹ️  检查模式，跳过名词表重建（--update 时自动执行）")
    print()

    # ═══ Step 5: 生成离线 Wiki HTML ═══
    print("─── Step 5: Wiki HTML 生成 ───")
    html_script = tool_path('build-wiki-html.py')
    if args.update:
        rc, output = run_tool(html_script, [], capture=True)
        if output:
            print(output)
        if rc == 0:
            print("✅ wiki-viewer.html 已生成")
        else:
            print("⚠️  HTML 生成失败（不影响同步流程）")
    else:
        print("ℹ️  检查模式，跳过 HTML 生成（--update 时自动执行）")
    print()

    # ═══ 汇总 ═══
    total_drift = has_feature_drift or has_sysmap_drift
    print("=" * 50)

    if args.update:
        if has_feature_drift:
            print("⚠️  feature 仍有漂移，--update 已中止。请先修复 feature 再重试。")
            sys.exit(1)

        if has_sysmap_drift:
            print("  ℹ️  system-map 已通过 --sync 插入骨架行，⚠️ TODO 行需 AI 补充描述")

        # 更新基准 commit
        repos_conf = env.get('repos', {})
        sync = env.get('sync', {})
        repo_keys = [args.repo] if args.repo else list(repos_conf.keys())
        for key in repo_keys:
            if key in repos_conf:
                h = get_repo_head(repos_conf[key]['path'])
                if h:
                    sync[key] = h
        env['sync'] = sync
        save_env(env)

        print()
        print("🎉 wiki-sync --update 完成")
        print("=" * 50)
    else:
        if total_drift:
            print("⚠️  检测到漂移，请处理后运行 --update")
        else:
            print("✅ 全部同步，知识库是最新的")
        print("=" * 50)

    sys.exit(1 if total_drift and not args.update else 0)


if __name__ == '__main__':
    main()
