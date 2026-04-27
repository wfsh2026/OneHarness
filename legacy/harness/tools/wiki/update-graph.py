#!/usr/bin/env python3
"""
代码知识图谱工具
===============
使用 tree-sitter AST 解析扫描项目 C# 代码，生成代码结构索引。

核心产出：
  wiki/knowledge/graph.json          — 完整代码图谱（机器用）
  wiki/knowledge/GRAPH_REPORT.md     — 架构分析报告（AI 读这个）
  wiki/knowledge/html/*.html         — 按模块交互式可视化（浏览器打开审阅）

用法：
  python3 aigc/harness/tools/wiki/update-graph.py                    # 生成图谱 + 报告
  python3 aigc/harness/tools/wiki/update-graph.py --stats            # 生成 + 终端统计
  python3 aigc/harness/tools/wiki/update-graph.py --report-only      # 仅从已有 graph.json 重新生成报告
  python3 aigc/harness/tools/wiki/update-graph.py --html             # 按模块生成交互式 HTML
  python3 aigc/harness/tools/wiki/update-graph.py --query Tank       # 查询节点 + 邻居子图
  python3 aigc/harness/tools/wiki/update-graph.py --query Tank --depth 2  # BFS 深度 2
  python3 aigc/harness/tools/wiki/update-graph.py --query Tank --dfs     # DFS 模式
  python3 aigc/harness/tools/wiki/update-graph.py --query "Tank Weapon" --budget 3000  # 多关键词 + token 预算

依赖：
  pip install -r aigc/harness/tools/wiki/requirements.txt
"""

import argparse
import glob
import json
import os
import sys
import time
import hashlib
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # aigc/harness/tools/wiki/ → 项目根
KNOWLEDGE_DIR = PROJECT_ROOT / "aigc" / "wiki" / "knowledge"
OUTPUT_PATH = KNOWLEDGE_DIR / "graph.json"
REPORT_PATH = KNOWLEDGE_DIR / "GRAPH_REPORT.md"
CACHE_DIR = KNOWLEDGE_DIR / ".graph-cache"


def _get_code_root():
    """从 wiki-env.json 获取代码根路径，fallback 到 Assets/Scripts"""
    env_path = PROJECT_ROOT / "aigc" / "wiki" / "wiki-env.json"
    if env_path.exists():
        import json as _json
        with open(env_path) as f:
            env = _json.load(f)
        if "repos" in env:
            script_repo = env["repos"].get("script", {})
            if "path" in script_repo:
                return PROJECT_ROOT / script_repo["path"]
    for name in ["Assets/Scripts", "Assets/Script"]:
        p = PROJECT_ROOT / name
        if p.exists():
            return p
    return PROJECT_ROOT / "Assets" / "Scripts"


CODE_ROOT = _get_code_root()
# 用于 replace 显示：动态获取相对前缀（如 "Assets/Scripts/" 或 "Assets/Script/"）
_CODE_PREFIX = str(CODE_ROOT.relative_to(PROJECT_ROOT)) + "/"

EXCLUDE_DIRS = ["/3rd/", "/Packages/", "/Library/", "/Temp/"]


# ══════════════════════════════════════════════════════════════════════════
#  基础设施
# ══════════════════════════════════════════════════════════════════════════

def check_deps():
    """检查依赖是否安装"""
    try:
        import graphify  # noqa: F401
        import networkx  # noqa: F401
    except ImportError:
        print("❌ 缺少依赖，请先执行:")
        print(f"   pip install -r {SCRIPT_DIR / 'requirements.txt'}")
        sys.exit(1)


def collect_files():
    """收集待扫描的 .cs 文件"""
    pattern = str(CODE_ROOT / "**" / "*.cs")
    all_cs = sorted(glob.glob(pattern, recursive=True))
    filtered = [
        f for f in all_cs
        if not any(ex in f for ex in EXCLUDE_DIRS) and os.path.exists(f)
    ]
    return [Path(f) for f in filtered]


# ══════════════════════════════════════════════════════════════════════════
#  SHA256 增量缓存
# ══════════════════════════════════════════════════════════════════════════

def file_hash(path: Path) -> str:
    """SHA256(文件内容 + 绝对路径)，确保唯一"""
    content = path.read_bytes()
    h = hashlib.sha256()
    h.update(content)
    h.update(b"\x00")
    h.update(str(path.resolve()).encode())
    return h.hexdigest()


def load_cached(path: Path) -> dict | None:
    """读取单文件缓存，hash 不匹配返回 None"""
    try:
        h = file_hash(path)
    except OSError:
        return None
    entry = CACHE_DIR / f"{h}.json"
    if not entry.exists():
        return None
    try:
        return json.loads(entry.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def save_cached(path: Path, result: dict) -> None:
    """保存单文件提取结果到缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    h = file_hash(path)
    entry = CACHE_DIR / f"{h}.json"
    tmp = entry.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(result))
        os.replace(tmp, entry)
    except Exception:
        tmp.unlink(missing_ok=True)


def check_cache(paths: list[Path]) -> tuple[list[dict], list[Path]]:
    """批量检查缓存，返回 (已缓存结果列表, 未缓存文件列表)"""
    cached_results = []
    uncached = []
    for p in paths:
        result = load_cached(p)
        if result is not None:
            cached_results.append(result)
        else:
            uncached.append(p)
    return cached_results, uncached


# ══════════════════════════════════════════════════════════════════════════
#  图谱生成（含增量缓存）
# ══════════════════════════════════════════════════════════════════════════

def generate_graph(paths, verbose=False, force=False):
    """AST 提取 → 构建图谱 → 保存（支持增量缓存）"""
    from graphify.extract import extract
    from graphify.build import build
    import networkx as nx

    t0 = time.time()

    if force:
        cached_results, uncached = [], paths
    else:
        cached_results, uncached = check_cache(paths)

    if verbose:
        print(f"📂 总文件: {len(paths)} 个 .cs")
        print(f"   缓存命中: {len(cached_results)} | 需提取: {len(uncached)}")

    # AST 提取未缓存的文件
    all_nodes = []
    all_edges = []

    # 合并缓存结果
    for r in cached_results:
        all_nodes.extend(r.get("nodes", []))
        all_edges.extend(r.get("edges", []))

    # 提取未缓存的文件（逐文件，以便缓存）
    if uncached:
        for i, p in enumerate(uncached):
            try:
                result = extract([p])
                save_cached(p, result)
                all_nodes.extend(result.get("nodes", []))
                all_edges.extend(result.get("edges", []))
            except Exception as e:
                if verbose:
                    print(f"   ⚠️ 跳过 {p.name}: {e}")

    t1 = time.time()
    if verbose:
        print(f"🔍 提取完成: {len(all_nodes)} nodes, {len(all_edges)} edges ({t1-t0:.1f}s)")

    # 构建 NetworkX 图
    merged_extraction = {"nodes": all_nodes, "edges": all_edges}
    G = build([merged_extraction])
    t2 = time.time()
    if verbose:
        print(f"🏗️  构建完成: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges ({t2-t1:.1f}s)")

    # 保存
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = nx.node_link_data(G)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

    size_mb = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    t3 = time.time()

    print(f"✅ graph.json → {OUTPUT_PATH}")
    print(f"   {G.number_of_nodes()} nodes / {G.number_of_edges()} edges / {size_mb:.1f}MB / {t3-t0:.1f}s")

    return G


# ══════════════════════════════════════════════════════════════════════════
#  P0: GRAPH_REPORT.md 生成
# ══════════════════════════════════════════════════════════════════════════

def _namespace_from_source(source_file: str) -> str:
    """从 source_file 路径提取顶层模块名"""
    # Assets/Scripts/GPO/Server/... → GPO
    path = source_file.replace(_CODE_PREFIX, "").replace(_CODE_PREFIX.replace("/", "\\"), "")
    parts = path.split("/") if "/" in path else path.split("\\")
    return parts[0] if parts else "Unknown"


def _is_class_node(G, node_id: str) -> bool:
    """判断是否是类级节点（排除文件级和方法级）"""
    data = G.nodes[node_id]
    label = data.get("label", "")
    loc = data.get("source_location", "")
    # 文件级: L1 且 label 以 .cs 结尾
    if loc == "L1" and label.endswith(".cs"):
        return False
    # 方法级: 通常 label 含括号或度为 1
    # 类级: 度 > 1 且不是文件名
    return True


def _god_nodes(G, top_n=20):
    """最高连接度节点（排除文件级节点）"""
    degree = dict(G.degree())
    results = []
    for node_id, deg in sorted(degree.items(), key=lambda x: -x[1]):
        data = G.nodes[node_id]
        label = data.get("label", node_id)
        # 排除文件级节点
        if label.endswith(".cs"):
            continue
        results.append({
            "label": label,
            "degree": deg,
            "source_file": data.get("source_file", ""),
        })
        if len(results) >= top_n:
            break
    return results


def _inheritance_tree(G, top_n=15):
    """继承关系统计：最多被继承的基类"""
    base_classes = Counter()
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "inherits":
            vl = G.nodes[v].get("label", v) if v in G.nodes else v
            base_classes[vl] += 1
    return base_classes.most_common(top_n)


def _namespace_distribution(G):
    """按顶层目录统计节点分布"""
    ns_stats = defaultdict(lambda: {"nodes": 0, "classes": 0, "files": set()})
    for node_id, data in G.nodes(data=True):
        sf = data.get("source_file", "")
        if not sf:
            continue
        ns = _namespace_from_source(sf)
        ns_stats[ns]["nodes"] += 1
        ns_stats[ns]["files"].add(sf)
        label = data.get("label", "")
        if not label.endswith(".cs") and not label.endswith("()"):
            ns_stats[ns]["classes"] += 1
    # 转为可序列化
    result = {}
    for ns, info in ns_stats.items():
        result[ns] = {
            "nodes": info["nodes"],
            "classes": info["classes"],
            "files": len(info["files"]),
        }
    return dict(sorted(result.items(), key=lambda x: -x[1]["nodes"]))


def _edge_type_distribution(G):
    """边类型分布"""
    rels = Counter()
    for _, _, d in G.edges(data=True):
        rels[d.get("relation", "unknown")] += 1
    return rels.most_common()


def _bridge_nodes(G, top_n=10):
    """跨模块桥接节点：连接最多不同顶层目录的类"""
    bridges = []
    for node_id, data in G.nodes(data=True):
        label = data.get("label", "")
        if label.endswith(".cs"):
            continue
        sf = data.get("source_file", "")
        own_ns = _namespace_from_source(sf) if sf else ""

        neighbor_ns = set()
        for neighbor in G.neighbors(node_id):
            n_sf = G.nodes[neighbor].get("source_file", "")
            if n_sf:
                n_ns = _namespace_from_source(n_sf)
                if n_ns != own_ns:
                    neighbor_ns.add(n_ns)

        if len(neighbor_ns) >= 2:
            bridges.append({
                "label": label,
                "own_module": own_ns,
                "cross_modules": sorted(neighbor_ns),
                "cross_count": len(neighbor_ns),
                "degree": G.degree(node_id),
                "source_file": sf,
            })

    bridges.sort(key=lambda x: (-x["cross_count"], -x["degree"]))
    return bridges[:top_n]


def generate_report(G):
    """生成 GRAPH_REPORT.md"""
    today = date.today().isoformat()
    gods = _god_nodes(G, top_n=30)
    inheritance = _inheritance_tree(G, top_n=15)
    ns_dist = _namespace_distribution(G)
    edge_dist = _edge_type_distribution(G)
    bridges = _bridge_nodes(G, top_n=10)

    total_inherits = sum(1 for _, _, d in G.edges(data=True) if d.get("relation") == "inherits")

    lines = []
    lines.append(f"# 代码知识图谱分析报告")
    lines.append(f"")
    lines.append(f"> 自动生成于 {today}，由 `update-graph.py --report` 产出。")
    lines.append(f"> AI Agent 应读此文件了解项目架构，**不要**直接读 graph.json（{os.path.getsize(OUTPUT_PATH)/1024/1024:.0f}MB）。")
    lines.append(f"> 需要查询具体类/方法时，使用 `update-graph.py --query <关键词>`。")
    lines.append(f"")

    # ── 概览 ──
    lines.append(f"## 一、概览")
    lines.append(f"")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 节点总数 | {G.number_of_nodes():,} |")
    lines.append(f"| 边总数 | {G.number_of_edges():,} |")
    lines.append(f"| 模块数 | {len(ns_dist)} |")
    lines.append(f"| 继承关系 | {total_inherits:,} |")
    lines.append(f"| graph.json | {os.path.getsize(OUTPUT_PATH)/1024/1024:.1f} MB |")
    lines.append(f"")

    # ── 边类型分布 ──
    lines.append(f"## 二、边类型分布")
    lines.append(f"")
    lines.append(f"| 关系类型 | 数量 | 占比 |")
    lines.append(f"|---------|------|------|")
    total_edges = G.number_of_edges() or 1
    for rel, count in edge_dist:
        pct = round(count / total_edges * 100)
        lines.append(f"| {rel} | {count:,} | {pct}% |")
    lines.append(f"")

    # ── God Nodes ──
    lines.append(f"## 三、God Nodes（核心抽象，最高连接度）")
    lines.append(f"")
    lines.append(f"> 这些是项目中连接最多的类/实体，通常是架构核心。")
    lines.append(f"")
    lines.append(f"| # | 类名 | 连接度 | 所在文件 |")
    lines.append(f"|---|------|-------|---------|")
    for i, node in enumerate(gods, 1):
        sf = node["source_file"].replace(_CODE_PREFIX, "")
        lines.append(f"| {i} | `{node['label']}` | {node['degree']} | {sf} |")
    lines.append(f"")

    # ── 继承树 ──
    lines.append(f"## 四、继承关系（最多被继承的基类）")
    lines.append(f"")
    lines.append(f"> 这些基类定义了项目的核心架构层次。")
    lines.append(f"")
    lines.append(f"| 基类 | 子类数量 |")
    lines.append(f"|------|---------|")
    for base, count in inheritance:
        lines.append(f"| `{base}` | {count} |")
    lines.append(f"")

    # ── 模块分布 ──
    lines.append(f"## 五、模块分布（按顶层目录）")
    lines.append(f"")
    lines.append(f"> 节点按 `代码根/<模块名>/` 分组统计。")
    lines.append(f"")
    lines.append(f"| 模块 | 节点数 | 类数 | 文件数 |")
    lines.append(f"|------|-------|------|-------|")
    for ns, info in list(ns_dist.items())[:30]:
        lines.append(f"| {ns} | {info['nodes']:,} | {info['classes']:,} | {info['files']} |")
    if len(ns_dist) > 30:
        lines.append(f"| ... | 还有 {len(ns_dist)-30} 个模块 | | |")
    lines.append(f"")

    # ── 桥接节点 ──
    lines.append(f"## 六、跨模块桥接节点")
    lines.append(f"")
    lines.append(f"> 这些类连接了多个不同模块，是系统间的耦合点。")
    lines.append(f"")
    if bridges:
        lines.append(f"| 类名 | 所属模块 | 跨越模块数 | 连接的模块 |")
        lines.append(f"|------|---------|----------|----------|")
        for b in bridges:
            modules = ", ".join(b["cross_modules"][:5])
            if len(b["cross_modules"]) > 5:
                modules += f" +{len(b['cross_modules'])-5}"
            lines.append(f"| `{b['label']}` | {b['own_module']} | {b['cross_count']} | {modules} |")
    else:
        lines.append(f"（无跨模块桥接节点）")
    lines.append(f"")

    # ── 使用指南 ──
    lines.append(f"## 七、AI Agent 使用指南")
    lines.append(f"")
    lines.append(f"### 查询命令")
    lines.append(f"")
    lines.append(f"```bash")
    lines.append(f"# 关键词查询（BFS，返回子图）")
    lines.append(f"python3 aigc/harness/tools/wiki/update-graph.py --query Tank")
    lines.append(f"")
    lines.append(f"# 多关键词查询")
    lines.append(f'python3 aigc/harness/tools/wiki/update-graph.py --query "Tank Weapon"')
    lines.append(f"")
    lines.append(f"# DFS 深度追踪")
    lines.append(f"python3 aigc/harness/tools/wiki/update-graph.py --query Tank --dfs")
    lines.append(f"")
    lines.append(f"# 控制 token 预算")
    lines.append(f"python3 aigc/harness/tools/wiki/update-graph.py --query Tank --budget 3000")
    lines.append(f"")
    lines.append(f"# 调整遍历深度")
    lines.append(f"python3 aigc/harness/tools/wiki/update-graph.py --query Tank --depth 3")
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"### 使用原则")
    lines.append(f"")
    lines.append(f"1. **先读本报告**了解项目架构全貌")
    lines.append(f"2. **按需查询**：用 `--query` 查找具体类/方法，不要读 graph.json")
    lines.append(f"3. **God Nodes 优先**：修改高连接度的类时要格外谨慎")
    lines.append(f"4. **桥接节点注意**：跨模块桥接节点的修改可能影响多个系统")
    lines.append(f"")

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"✅ GRAPH_REPORT.md → {REPORT_PATH}")
    print(f"   {len(lines)} 行")
    return report_text


# ══════════════════════════════════════════════════════════════════════════
#  P1: 子图查询（BFS / DFS）
# ══════════════════════════════════════════════════════════════════════════

def _score_nodes(G, terms: list[str]) -> list[tuple[float, str]]:
    """对节点进行关键词匹配评分"""
    scored = []
    for nid, data in G.nodes(data=True):
        label = data.get("label", "").lower()
        source = data.get("source_file", "").lower()
        score = sum(2 for t in terms if t in label) + sum(0.5 for t in terms if t in source)
        if score > 0:
            scored.append((score, nid))
    return sorted(scored, reverse=True)


def _bfs(G, start_nodes: list[str], depth: int) -> tuple[set[str], list[tuple]]:
    """BFS 遍历：广度优先，返回 (节点集, 边列表)"""
    visited = set(start_nodes)
    frontier = set(start_nodes)
    edges_seen = []
    for _ in range(depth):
        next_frontier = set()
        for n in frontier:
            for neighbor in G.neighbors(n):
                if neighbor not in visited:
                    next_frontier.add(neighbor)
                    edges_seen.append((n, neighbor))
        visited.update(next_frontier)
        frontier = next_frontier
    return visited, edges_seen


def _dfs(G, start_nodes: list[str], depth: int) -> tuple[set[str], list[tuple]]:
    """DFS 遍历：深度优先追踪路径"""
    visited = set()
    edges_seen = []
    stack = [(n, 0) for n in reversed(start_nodes)]
    while stack:
        node, d = stack.pop()
        if node in visited or d > depth:
            continue
        visited.add(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                stack.append((neighbor, d + 1))
                edges_seen.append((node, neighbor))
    return visited, edges_seen


def _subgraph_to_text(G, nodes: set[str], edges: list[tuple],
                       terms: list[str], token_budget: int = 2000) -> str:
    """将子图渲染为文本，按相关度排序，受 token 预算限制"""
    char_budget = token_budget * 4  # 约 4 字符/token

    def relevance(nid):
        label = G.nodes[nid].get("label", "").lower()
        return sum(1 for t in terms if t in label)

    ranked_nodes = sorted(nodes, key=relevance, reverse=True)

    lines = []
    for nid in ranked_nodes:
        d = G.nodes[nid]
        label = d.get("label", nid)
        sf = d.get("source_file", "").replace(_CODE_PREFIX, "")
        loc = d.get("source_location", "")
        deg = G.degree(nid)
        lines.append(f"  NODE {label} [src={sf} loc={loc} degree={deg}]")

    for u, v in edges:
        if u in nodes and v in nodes:
            d = G.edges[u, v]
            rel = d.get("relation", "")
            conf = d.get("confidence", "")
            u_label = G.nodes[u].get("label", u)
            v_label = G.nodes[v].get("label", v)
            lines.append(f"  EDGE {u_label} --{rel} [{conf}]--> {v_label}")

    output = "\n".join(lines)
    if len(output) > char_budget:
        output = output[:char_budget] + f"\n  ... (截断于 ~{token_budget} token 预算，用 --budget N 调整)"
    return output


def query_graph(G, keyword: str, mode: str = "bfs", depth: int = 2, budget: int = 2000):
    """子图查询：关键词 → BFS/DFS → 文本输出"""
    terms = [t.lower() for t in keyword.split() if len(t) > 1]
    if not terms:
        print("❌ 请提供查询关键词")
        return

    scored = _score_nodes(G, terms)
    start_nodes = [nid for _, nid in scored[:5]]

    if not start_nodes:
        print(f"❌ 未找到匹配 '{keyword}' 的节点")
        return

    # 遍历
    if mode == "dfs":
        nodes, edges = _dfs(G, start_nodes, depth)
    else:
        nodes, edges = _bfs(G, start_nodes, depth)

    # 输出头
    start_labels = [G.nodes[n].get("label", n) for n in start_nodes[:3]]
    print(f"\n🔎 查询: '{keyword}' | 模式: {mode.upper()} | 深度: {depth}")
    print(f"   起始节点: {start_labels}")
    print(f"   遍历结果: {len(nodes)} 节点, {len(edges)} 边")
    print(f"   Token 预算: ~{budget}")
    print()

    # 子图文本
    text = _subgraph_to_text(G, nodes, edges, terms, budget)
    print(text)

    # 补充：直接匹配的节点详情
    print(f"\n--- 直接匹配的节点 ---")
    for score, nid in scored[:15]:
        data = G.nodes[nid]
        label = data.get("label", nid)
        sf = data.get("source_file", "").replace(_CODE_PREFIX, "")
        deg = G.degree(nid)

        # 列出该节点的关键边
        key_edges = []
        for neighbor in G.neighbors(nid):
            edata = G.edges[nid, neighbor]
            rel = edata.get("relation", "")
            n_label = G.nodes[neighbor].get("label", neighbor)
            if rel in ("inherits", "calls", "imports"):
                key_edges.append(f"{rel}→{n_label}")

        edges_str = f"  [{', '.join(key_edges[:5])}]" if key_edges else ""
        print(f"  {label:45s} degree={deg:>4}  {sf[:50]}{edges_str}")

    if len(scored) > 15:
        print(f"  ... 还有 {len(scored)-15} 个匹配")


# ══════════════════════════════════════════════════════════════════════════
#  P2: HTML 可视化（按模块拆分）
# ══════════════════════════════════════════════════════════════════════════

HTML_DIR = KNOWLEDGE_DIR / "html"
MODULE_MIN_NODES = 50  # 小于此值的模块合并到 Others


def _node_type(G, nid: str) -> str:
    """判断节点类型: class / method / file / namespace"""
    label = G.nodes[nid].get("label", "")
    if "(" in label or label.endswith("()"):
        return "method"
    if label.endswith(".cs"):
        return "file"
    # 命名空间节点：包含多段点号分隔（如 Sofunny.BiuBiuBiu2.ServerGamePlay）
    if "." in label and label.count(".") >= 2:
        return "namespace"
    return "class"


def _build_class_graph(G):
    """从完整图谱构建类级图：只保留类节点，方法调用链折叠为类间 calls 边"""
    import networkx as nx

    class_nodes = [n for n in G.nodes if _node_type(G, n) == "class"]
    class_set = set(class_nodes)

    # --- A. 合并 C# partial class（同名类分布在多个文件中） ---
    # 相同 label 的类节点合并为一个代表节点（取第一个）
    label_to_rep = {}  # label → representative node id
    merge_map = {}     # original node id → representative node id
    for n in class_nodes:
        label = G.nodes[n].get("label", n)
        if label not in label_to_rep:
            label_to_rep[label] = n
        merge_map[n] = label_to_rep[label]

    merged_count = len(class_nodes) - len(label_to_rep)

    # 构建 file→class 重定向表（graphify 约 10% inherits 边连在文件节点上）
    file_to_class = {}
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "contains" and _node_type(G, u) == "file" and v in class_set:
            file_to_class[u] = merge_map.get(v, v)

    def _resolve(nid):
        """将节点重定向：partial class → 代表节点，file → 其包含的类节点"""
        if nid in merge_map:
            return merge_map[nid]
        return file_to_class.get(nid)

    # 只添加代表节点
    H = nx.Graph()
    rep_set = set(label_to_rep.values())
    for n in rep_set:
        H.add_node(n, **dict(G.nodes[n]))

    # 类-类边（inherits, contains），支持 file→class 和 partial→rep 重定向
    for u, v, d in G.edges(data=True):
        ru, rv = _resolve(u), _resolve(v)
        if ru and rv and ru != rv and ru in rep_set and rv in rep_set:
            if not H.has_edge(ru, rv):
                H.add_edge(ru, rv, **d)

    # 折叠方法调用链: class→method→calls→method←class → class calls class
    method_to_class = {}
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "method" and u in class_set and _node_type(G, v) == "method":
            method_to_class[v] = merge_map.get(u, u)

    call_counts = defaultdict(int)
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "calls":
            caller = method_to_class.get(u)
            callee = method_to_class.get(v)
            if caller and callee and caller != callee:
                call_counts[(caller, callee)] += 1

    for (u, v), cnt in call_counts.items():
        if not H.has_edge(u, v):
            H.add_edge(u, v, relation="calls", weight=cnt, confidence="EXTRACTED")

    if merged_count > 0:
        print(f"   合并 partial class: {len(class_nodes)} → {len(rep_set)} 节点（减少 {merged_count}）")

    return H


def _get_module(G, nid: str) -> str:
    """获取节点所属模块"""
    sf = G.nodes[nid].get("source_file", "")
    if not sf:
        return "External"
    path = sf.replace(_CODE_PREFIX, "").replace(_CODE_PREFIX.replace("/", "\\"), "")
    parts = path.split("/") if "/" in path else path.split("\\")
    return parts[0] if parts else "Unknown"


def generate_html(G, verbose=False):
    """按模块生成交互式 HTML 可视化"""
    from graphify.cluster import cluster
    from graphify.export import to_html

    t0 = time.time()
    HTML_DIR.mkdir(parents=True, exist_ok=True)

    # 构建类级图
    H = _build_class_graph(G)
    if verbose:
        print(f"🔨 类级图谱: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

    # 按模块分组
    modules = defaultdict(list)
    for n in H.nodes:
        modules[_get_module(H, n)].append(n)

    # 小模块合并到 Others
    major = {}
    others = []
    for mod, nodes in modules.items():
        if mod == "External":
            continue  # External 节点按需分配给各模块
        if len(nodes) >= MODULE_MIN_NODES:
            major[mod] = nodes
        else:
            others.extend(nodes)
    if others:
        major["Others"] = others

    external_nodes = set(modules.get("External", []))

    if verbose:
        print(f"📦 模块拆分: {len(major)} 个模块")
        for mod, nodes in sorted(major.items(), key=lambda x: -len(x[1])):
            print(f"   {mod}: {len(nodes)} 类节点")

    generated = []
    for mod, mod_nodes in sorted(major.items(), key=lambda x: -len(x[1])):
        mod_set = set(mod_nodes)

        # 加入与本模块有边的 External 节点（基类如 MonoBehaviour, IMessage）
        ext_included = set()
        for n in mod_nodes:
            for neighbor in H.neighbors(n):
                if neighbor in external_nodes:
                    ext_included.add(neighbor)

        all_nodes = mod_set | ext_included
        sub = H.subgraph(all_nodes).copy()

        if sub.number_of_nodes() == 0:
            continue

        # B. 过滤 deg=0 孤岛节点（partial 合并后仍无连接的纯工具类）
        isolated = [n for n in sub.nodes if sub.degree(n) == 0]
        if isolated:
            sub.remove_nodes_from(isolated)

        if sub.number_of_nodes() == 0 or sub.number_of_edges() == 0:
            if verbose:
                print(f"   → {mod}: 跳过（过滤后 {sub.number_of_nodes()} 节点 / {sub.number_of_edges()} 边）")
            continue

        # 标注 External 节点的 source_file 让 HTML 侧面板能显示
        for n in ext_included:
            if n in sub.nodes:
                sub.nodes[n]["source_file"] = sub.nodes[n].get("source_file", "") or "(External)"

        if verbose:
            print(f"   → {mod}: {sub.number_of_nodes()} nodes ({len(ext_included)} external), {sub.number_of_edges()} edges")

        # 聚类
        try:
            communities = cluster(sub)
        except Exception:
            communities = {0: sorted(sub.nodes)}

        # 生成社区标签（用代表性节点命名）
        labels = {}
        for cid, cnodes in communities.items():
            if cnodes:
                # 取度最高的节点作为社区标签
                top = max(cnodes, key=lambda n: sub.degree(n))
                labels[cid] = sub.nodes[top].get("label", top)

        output_path = str(HTML_DIR / f"{mod}.html")
        try:
            to_html(sub, communities, output_path, community_labels=labels)
            generated.append((mod, sub.number_of_nodes(), sub.number_of_edges(), len(communities)))
        except ValueError as e:
            if verbose:
                print(f"   ⚠️ {mod}: {e}")

    t1 = time.time()
    print(f"\n✅ HTML 可视化 → {HTML_DIR}/")
    for mod, n, e, c in generated:
        print(f"   {mod}.html: {n} nodes, {e} edges, {c} communities")
    print(f"   耗时: {t1-t0:.1f}s")

    return generated


# ══════════════════════════════════════════════════════════════════════════
#  终端统计（保留原有功能）
# ══════════════════════════════════════════════════════════════════════════

def print_stats(G):
    """打印图谱统计信息到终端"""
    edge_dist = _edge_type_distribution(G)
    print("\n📊 边类型分布:")
    for r, c in edge_dist:
        print(f"   {r}: {c}")

    gods = _god_nodes(G, top_n=20)
    print("\n🏆 Top 20 God Nodes:")
    for i, node in enumerate(gods, 1):
        sf = node["source_file"].replace(_CODE_PREFIX, "")
        print(f"   {i:2d}. {node['label']:50s} degree={node['degree']:>4}  {sf[:55]}")

    inheritance = _inheritance_tree(G, top_n=10)
    total_inherits = sum(1 for _, _, d in G.edges(data=True) if d.get("relation") == "inherits")
    print(f"\n🧬 继承关系: {total_inherits} 条")
    print("   最多被继承的基类:")
    for bc, count in inheritance:
        print(f"   {bc}: {count} 子类")

    bridges = _bridge_nodes(G, top_n=5)
    if bridges:
        print(f"\n🌉 跨模块桥接节点 (Top 5):")
        for b in bridges:
            modules = ", ".join(b["cross_modules"][:5])
            print(f"   {b['label']:40s} {b['own_module']} → [{modules}]")


# ══════════════════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════════════════

def load_existing_graph():
    """加载已有 graph.json"""
    import networkx as nx
    if not OUTPUT_PATH.exists():
        print(f"❌ graph.json 不存在: {OUTPUT_PATH}")
        print("   请先运行: python3 aigc/harness/tools/wiki/update-graph.py")
        sys.exit(1)
    print(f"📖 加载 graph.json ...")
    with open(OUTPUT_PATH) as f:
        data = json.load(f)
    try:
        G = nx.node_link_graph(data, edges="edges")
    except TypeError:
        G = nx.node_link_graph(data)
    print(f"   {G.number_of_nodes()} nodes / {G.number_of_edges()} edges")
    return G


def main():
    parser = argparse.ArgumentParser(
        description="代码知识图谱工具：生成 graph.json + GRAPH_REPORT.md，支持子图查询和 HTML 可视化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                              # 生成图谱 + 报告
  %(prog)s --stats                      # 生成 + 终端统计
  %(prog)s --report-only                # 仅重新生成报告（不重新扫描）
  %(prog)s --html                       # 按模块生成交互式 HTML（从已有 graph.json）
  %(prog)s --query Tank                 # BFS 查询
  %(prog)s --query "Tank Weapon" --dfs  # DFS 多关键词查询
  %(prog)s --query Tank --budget 3000   # 控制输出 token
  %(prog)s --force                      # 忽略缓存重新扫描
        """,
    )
    parser.add_argument("--stats", action="store_true", help="打印终端统计信息")
    parser.add_argument("--report-only", action="store_true", help="仅从已有 graph.json 重新生成报告")
    parser.add_argument("--html", action="store_true", help="按模块生成交互式 HTML（输出到 knowledge/html/）")
    parser.add_argument("--query", type=str, help="查询关键词（支持空格分隔多关键词）")
    parser.add_argument("--dfs", action="store_true", help="使用 DFS 模式（默认 BFS）")
    parser.add_argument("--depth", type=int, default=2, help="遍历深度（默认 2）")
    parser.add_argument("--budget", type=int, default=2000, help="输出 token 预算（默认 2000）")
    parser.add_argument("--force", action="store_true", help="忽略缓存，强制重新扫描")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    check_deps()

    # 模式 1: 仅查询（不重新生成）
    if args.query and not args.force and not args.report_only and not args.html:
        G = load_existing_graph()
        mode = "dfs" if args.dfs else "bfs"
        query_graph(G, args.query, mode=mode, depth=args.depth, budget=args.budget)
        return

    # 模式 2: 仅重新生成报告
    if args.report_only:
        G = load_existing_graph()
        generate_report(G)
        if args.html:
            generate_html(G, verbose=True)
        if args.stats:
            print_stats(G)
        return

    # 模式 2.5: 仅生成 HTML（从已有 graph.json）
    if args.html and not args.force:
        G = load_existing_graph()
        generate_html(G, verbose=True)
        return

    # 模式 3: 完整生成（扫描 + 图谱 + 报告）
    paths = collect_files()
    if not paths:
        print("❌ 未找到 .cs 文件")
        print(f"   扫描路径: {CODE_ROOT}")
        sys.exit(1)

    G = generate_graph(paths, verbose=True, force=args.force)
    generate_report(G)

    from wiki_log import append_wiki_log
    append_wiki_log("lint", "知识图谱重建",
                    f"使用 tree-sitter 解析代码依赖，生成 graph.json，节点: {G.number_of_nodes()} 个，边: {G.number_of_edges()} 条")

    if args.stats:
        print_stats(G)

    if args.query:
        mode = "dfs" if args.dfs else "bfs"
        query_graph(G, args.query, mode=mode, depth=args.depth, budget=args.budget)


if __name__ == "__main__":
    main()
