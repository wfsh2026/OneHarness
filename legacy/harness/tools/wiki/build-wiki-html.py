#!/usr/bin/env python3
"""Obsidian 风格离线 Wiki 检索页面生成器

将 aigc/wiki/ 下的所有 Markdown 文档打包为一个自包含的 HTML 文件，
提供 Obsidian 风格的文件树导航、全文搜索、[[wiki-link]] 点击跳转和反向链接。

用法:
    python3 aigc/harness/tools/wiki/build-wiki-html.py
    python3 aigc/harness/tools/wiki/build-wiki-html.py --output path/to/output.html
    python3 aigc/harness/tools/wiki/build-wiki-html.py --light   # 默认亮色主题
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent

# 智能定位项目根：优先 cwd（支持跨项目调用），回退到脚本位置推算
def _find_project_root() -> Path:
    """查找包含 aigc/wiki/ 的项目根目录"""
    # 1. 检查 cwd
    cwd = Path.cwd()
    if (cwd / "aigc" / "wiki").is_dir():
        return cwd
    # 2. 从 cwd 向上查找
    for p in cwd.parents:
        if (p / "aigc" / "wiki").is_dir():
            return p
    # 3. 回退到脚本位置推算
    return SCRIPT_DIR.parent.parent.parent.parent

PROJECT_ROOT = _find_project_root()
WIKI_ROOT = PROJECT_ROOT / "aigc" / "wiki"
KNOWLEDGE_DIR = WIKI_ROOT / "knowledge"
WIKI_MAP_PATH = KNOWLEDGE_DIR / "wiki-map.json"
DEFAULT_OUTPUT = KNOWLEDGE_DIR / "wiki-viewer.html"

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# ── 文档收集 ──────────────────────────────────────────────────────────────


def collect_docs() -> list[dict]:
    """扫描 wiki/ 下所有 .md 文件，返回文档列表"""
    docs = []
    for dirpath, _, files in os.walk(WIKI_ROOT):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            full = Path(dirpath) / f
            rel = full.relative_to(WIKI_ROOT).as_posix()
            content = full.read_text(encoding="utf-8", errors="replace")

            # 解析 frontmatter
            fm = {}
            body = content
            m = FRONTMATTER_RE.match(content)
            if m:
                body = content[m.end():]
                for line in m.group(1).splitlines():
                    line = line.strip()
                    if ":" in line:
                        k, v = line.split(":", 1)
                        k, v = k.strip(), v.strip()
                        # 简单解析 YAML list
                        if v.startswith("[") and v.endswith("]"):
                            v = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                        elif v.startswith("- "):
                            v = [v[2:].strip()]
                        elif v == "[]":
                            v = []
                        fm[k] = v
                # 多行 dependencies 补充解析
                if "dependencies" in fm and fm["dependencies"] == []:
                    dep_lines = []
                    in_deps = False
                    for line in m.group(1).splitlines():
                        if line.strip().startswith("dependencies:"):
                            in_deps = True
                            continue
                        if in_deps:
                            if line.strip().startswith("- "):
                                dep_lines.append(line.strip()[2:].strip())
                            else:
                                break
                    if dep_lines:
                        fm["dependencies"] = dep_lines

            # 提取 wiki-links
            links = WIKILINK_RE.findall(body)
            link_names = [lnk[0] for lnk in links]

            doc_name = f[:-3]  # 去 .md
            display = fm.get("display_name", doc_name)

            docs.append({
                "path": rel,
                "name": doc_name,
                "display": display,
                "fm": fm,
                "body": body,
                "links": link_names,
            })

    return docs


def load_wiki_map() -> dict:
    """加载 wiki-map.json"""
    if WIKI_MAP_PATH.exists():
        return json.loads(WIKI_MAP_PATH.read_text(encoding="utf-8"))
    return {}


def build_backlinks(docs: list[dict], wiki_map: dict) -> dict[str, list[str]]:
    """预计算反向链接: target_path → [source_paths]"""
    # 构建 name → path 的快速查找
    name_to_path = {}
    for d in docs:
        name_to_path[d["name"]] = d["path"]

    # 也用 wiki-map 补充
    for name, wpath in wiki_map.items():
        if isinstance(wpath, str):
            # wiki-map 路径是相对项目根的，转为相对 wiki/ 的
            if wpath.startswith("aigc/wiki/"):
                name_to_path[name] = wpath[len("aigc/wiki/"):]

    backlinks: dict[str, list[str]] = {}
    for d in docs:
        for link_name in d["links"]:
            target = name_to_path.get(link_name)
            if target:
                backlinks.setdefault(target, [])
                if d["path"] not in backlinks[target]:
                    backlinks[target].append(d["path"])
    return backlinks


# 路径 → category 推断规则（无 frontmatter 时使用）
# 规则按优先级从高到低匹配，第一个匹配即返回
_PATH_CATEGORY_RULES = [
    # 通用规则（适用所有项目）
    ("knowledge/", "knowledge"),                        # system-map, glossary 等知识库文件
]

# 通用目录名 → category 映射
_DIR_NAME_CATEGORIES = {
    "内容边界定义": "boundary",
    "范例文档": "example",
    "infra": "infra",
}


def _infer_category_from_path(rel_path: str) -> str:
    """根据 wiki/ 相对路径推断 category（仅当 frontmatter 无 category 时调用）

    推断优先级：
    1. 固定前缀规则（knowledge/ 等）
    2. 路径中包含的特征目录名（内容边界定义/范例文档 等）
    3. raw/项目名/制作文档 → guide
    4. raw/项目名/features/ 下的非 feature 文件 → index
    5. 兜底 → infra
    """
    # 1. 固定前缀
    for prefix, cat in _PATH_CATEGORY_RULES:
        if rel_path.startswith(prefix):
            return cat

    # 2. 路径中的特征目录名
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in _DIR_NAME_CATEGORIES:
            return _DIR_NAME_CATEGORIES[part]

    # 3. raw/*/制作.md 或 raw/*/xxx制作.md → guide（制作规范文档）
    if rel_path.startswith("raw/") and "制作" in rel_path:
        return "guide"

    # 4. raw/*/features/ 下的非 feature 文件（_index-*.md 等）→ index
    if "/features/" in rel_path and not rel_path.endswith("README.md"):
        return "index"

    # 5. 兜底
    return "infra"


def build_graph_data(docs: list[dict], wiki_map: dict) -> tuple[list[dict], list[dict]]:
    """提取图谱数据: 节点列表 + 边列表"""
    name_to_path = {}
    for d in docs:
        name_to_path[d["name"]] = d["path"]
    for name, wpath in wiki_map.items():
        if isinstance(wpath, str) and wpath.startswith("aigc/wiki/"):
            name_to_path[name] = wpath[len("aigc/wiki/"):]

    # 节点: 所有文档均参与图谱
    nodes = []
    node_set = set()
    for d in docs:
        fm = d["fm"]
        name = fm.get("name", "") or d["name"]
        cat = fm.get("category", "")
        if cat:
            top_cat = cat.split("/")[0]
        else:
            # 无 frontmatter category → 按路径推断
            top_cat = _infer_category_from_path(d["path"])
        nodes.append({
            "id": name,
            "display": d["display"],
            "path": d["path"],
            "category": top_cat,
        })
        node_set.add(name)

    # 边: dependencies (type=dep) + wiki-links (type=ref)
    edges = []
    edge_set = set()
    for d in docs:
        fm = d["fm"]
        src = fm.get("name", "") or d["name"]
        if src not in node_set:
            continue
        # dependency edges
        deps = fm.get("dependencies", [])
        if isinstance(deps, list):
            for dep in deps:
                if dep in node_set and (src, dep) not in edge_set:
                    edges.append({"s": src, "t": dep, "type": "dep"})
                    edge_set.add((src, dep))
        # wiki-link edges (only between nodes with frontmatter)
        for link in d["links"]:
            target_path = name_to_path.get(link)
            if not target_path:
                continue
            # find target node name
            target_name = None
            for dd in docs:
                if dd["path"] == target_path:
                    target_name = dd["fm"].get("name", "") or dd["name"]
                    break
            if target_name and target_name in node_set and target_name != src:
                if (src, target_name) not in edge_set:
                    edges.append({"s": src, "t": target_name, "type": "ref"})
                    edge_set.add((src, target_name))

    return nodes, edges


def build_html(docs: list[dict], backlinks: dict, wiki_map: dict,
               graph_nodes: list[dict], graph_edges: list[dict],
               default_theme: str = "dark") -> str:
    """生成自包含 HTML"""

    # 准备 JS 数据
    js_docs = []
    for d in docs:
        js_docs.append({
            "path": d["path"],
            "name": d["name"],
            "display": d["display"],
            "fm": d["fm"],
            "body": d["body"],
            "links": d["links"],
        })

    # name → wiki/ 相对路径 的解析表（给前端用）
    link_resolve = {}
    name_to_path = {}
    for d in docs:
        name_to_path[d["name"]] = d["path"]
    for name, wpath in wiki_map.items():
        if isinstance(wpath, str) and wpath.startswith("aigc/wiki/"):
            link_resolve[name] = wpath[len("aigc/wiki/"):]
    for d in docs:
        link_resolve[d["name"]] = d["path"]

    data_json = json.dumps(js_docs, ensure_ascii=False, separators=(",", ":"))
    backlinks_json = json.dumps(backlinks, ensure_ascii=False, separators=(",", ":"))
    resolve_json = json.dumps(link_resolve, ensure_ascii=False, separators=(",", ":"))
    gnodes_json = json.dumps(graph_nodes, ensure_ascii=False, separators=(",", ":"))
    gedges_json = json.dumps(graph_edges, ensure_ascii=False, separators=(",", ":"))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="{default_theme}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wiki Viewer — Obsidian Offline</title>
<style>
/* ── Reset ── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}

/* ── Theme variables ── */
:root,[data-theme="dark"]{{
  --bg-primary:#1e1e2e;
  --bg-secondary:#181825;
  --bg-tertiary:#11111b;
  --bg-hover:#313244;
  --bg-active:#45475a;
  --text-normal:#cdd6f4;
  --text-muted:#a6adc8;
  --text-faint:#6c7086;
  --accent:#89b4fa;
  --accent-hover:#74c7ec;
  --border:#313244;
  --link:#89b4fa;
  --link-unresolved:#f38ba8;
  --tag-bg:#313244;
  --code-bg:#181825;
  --table-border:#45475a;
  --table-header:#313244;
  --search-bg:#313244;
  --scrollbar:#45475a;
  --scrollbar-hover:#585b70;
  --fm-bg:#1e1e2e;
  --fm-border:#45475a;
  --backlink-bg:#181825;
}}
[data-theme="light"]{{
  --bg-primary:#eff1f5;
  --bg-secondary:#e6e9ef;
  --bg-tertiary:#dce0e8;
  --bg-hover:#ccd0da;
  --bg-active:#bcc0cc;
  --text-normal:#4c4f69;
  --text-muted:#6c6f85;
  --text-faint:#8c8fa1;
  --accent:#1e66f5;
  --accent-hover:#0550ae;
  --border:#ccd0da;
  --link:#1e66f5;
  --link-unresolved:#d20f39;
  --tag-bg:#ccd0da;
  --code-bg:#e6e9ef;
  --table-border:#bcc0cc;
  --table-header:#ccd0da;
  --search-bg:#ccd0da;
  --scrollbar:#bcc0cc;
  --scrollbar-hover:#9ca0b0;
  --fm-bg:#e6e9ef;
  --fm-border:#bcc0cc;
  --backlink-bg:#e6e9ef;
}}

body{{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  background:var(--bg-primary);color:var(--text-normal);
  display:flex;height:100vh;overflow:hidden;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar{{width:6px;height:6px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--scrollbar);border-radius:3px}}
::-webkit-scrollbar-thumb:hover{{background:var(--scrollbar-hover)}}

/* ── Left sidebar ── */
#sidebar{{
  width:280px;min-width:200px;max-width:400px;
  background:var(--bg-secondary);border-right:1px solid var(--border);
  display:flex;flex-direction:column;flex-shrink:0;
  transition:width .2s;
}}
#sidebar.collapsed{{width:0;min-width:0;overflow:hidden;border:none}}

#sidebar-header{{
  padding:12px 16px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  font-weight:600;font-size:14px;color:var(--text-muted);
}}

#search-box{{
  margin:8px 12px;padding:6px 10px;
  background:var(--search-bg);border:1px solid var(--border);border-radius:6px;
  color:var(--text-normal);font-size:13px;outline:none;
}}
#search-box:focus{{border-color:var(--accent)}}
#search-box::placeholder{{color:var(--text-faint)}}

#file-tree{{
  flex:1;overflow-y:auto;padding:4px 0;font-size:13px;
}}
.tree-folder{{cursor:pointer;user-select:none}}
.tree-folder-label{{
  display:flex;align-items:center;padding:3px 12px;gap:4px;
  color:var(--text-muted);font-weight:500;
}}
.tree-folder-label:hover{{background:var(--bg-hover)}}
.tree-folder-label .arrow{{
  display:inline-block;width:16px;text-align:center;
  font-size:10px;transition:transform .15s;color:var(--text-faint);
}}
.tree-folder-label .arrow.open{{transform:rotate(90deg)}}
.tree-folder-label .folder-icon{{color:var(--text-faint);font-size:12px}}
.tree-children{{padding-left:12px}}
.tree-children.hidden{{display:none}}

.tree-file{{
  display:flex;align-items:center;padding:3px 12px 3px 16px;gap:6px;
  cursor:pointer;color:var(--text-normal);text-decoration:none;
  border-radius:4px;margin:0 4px;
}}
.tree-file:hover{{background:var(--bg-hover)}}
.tree-file.active{{background:var(--bg-active);color:var(--accent)}}
.tree-file .file-icon{{color:var(--text-faint);font-size:11px}}

/* ── Main content ── */
#main{{
  flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0;
}}
#toolbar{{
  padding:8px 16px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:12px;background:var(--bg-secondary);
  font-size:13px;
}}
#toolbar button{{
  background:none;border:none;color:var(--text-muted);cursor:pointer;
  font-size:16px;padding:4px 6px;border-radius:4px;
}}
#toolbar button:hover{{background:var(--bg-hover);color:var(--text-normal)}}
#breadcrumb{{color:var(--text-muted);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
#theme-toggle{{font-size:14px}}

#content-wrapper{{
  flex:1;display:flex;overflow:hidden;position:relative;
}}
#content{{
  flex:1;overflow-y:auto;padding:32px 48px;max-width:900px;margin:0 auto;
  line-height:1.7;
}}

/* ── Markdown rendering ── */
#content h1{{font-size:1.8em;margin:0.6em 0 0.4em;font-weight:700;border-bottom:1px solid var(--border);padding-bottom:8px}}
#content h2{{font-size:1.4em;margin:1.2em 0 0.4em;font-weight:600;color:var(--text-normal)}}
#content h3{{font-size:1.15em;margin:1em 0 0.3em;font-weight:600}}
#content h4{{font-size:1em;margin:0.8em 0 0.2em;font-weight:600;color:var(--text-muted)}}
#content p{{margin:0.5em 0}}
#content a{{color:var(--link);text-decoration:none}}
#content a:hover{{text-decoration:underline}}
#content a.wikilink-unresolved{{color:var(--link-unresolved);border-bottom:1px dashed var(--link-unresolved);cursor:help}}

#content code{{
  background:var(--code-bg);padding:2px 5px;border-radius:3px;
  font-size:0.88em;font-family:"Cascadia Code","Fira Code",Consolas,monospace;
}}
#content pre{{
  background:var(--code-bg);padding:14px 18px;border-radius:6px;
  overflow-x:auto;margin:0.8em 0;border:1px solid var(--border);
}}
#content pre code{{background:none;padding:0;font-size:0.85em}}

#content blockquote{{
  border-left:3px solid var(--accent);padding:8px 16px;margin:0.6em 0;
  color:var(--text-muted);background:var(--bg-secondary);border-radius:0 4px 4px 0;
}}

#content table{{
  border-collapse:collapse;width:100%;margin:0.8em 0;font-size:0.92em;
}}
#content th{{
  background:var(--table-header);font-weight:600;text-align:left;
  padding:8px 12px;border:1px solid var(--table-border);
}}
#content td{{padding:6px 12px;border:1px solid var(--table-border)}}
#content tr:hover td{{background:var(--bg-hover)}}

#content ul,#content ol{{margin:0.4em 0;padding-left:24px}}
#content li{{margin:0.15em 0}}

#content hr{{border:none;border-top:1px solid var(--border);margin:1.5em 0}}

#content img{{max-width:100%;border-radius:4px}}

/* ── Frontmatter card ── */
.fm-card{{
  background:var(--fm-bg);border:1px solid var(--fm-border);
  border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:0.88em;
}}
.fm-card .fm-row{{display:flex;gap:8px;margin:3px 0}}
.fm-card .fm-key{{color:var(--text-faint);min-width:90px;font-weight:500}}
.fm-card .fm-val{{color:var(--text-muted)}}
.fm-card .fm-tag{{
  display:inline-block;background:var(--tag-bg);padding:1px 8px;
  border-radius:10px;font-size:0.85em;margin:0 2px;
}}

/* ── Backlinks panel ── */
#backlinks-panel{{
  width:260px;border-left:1px solid var(--border);background:var(--backlink-bg);
  overflow-y:auto;padding:16px;font-size:13px;flex-shrink:0;
}}
#backlinks-panel.hidden{{display:none}}
#backlinks-panel h3{{
  font-size:12px;text-transform:uppercase;letter-spacing:1px;
  color:var(--text-faint);margin-bottom:12px;font-weight:600;
}}
.backlink-item{{
  padding:6px 8px;margin:2px 0;border-radius:4px;cursor:pointer;
  color:var(--link);
}}
.backlink-item:hover{{background:var(--bg-hover)}}

/* ── Welcome screen ── */
.welcome{{text-align:center;color:var(--text-faint);margin-top:20vh}}
.welcome h1{{font-size:1.6em;border:none;color:var(--text-muted)}}
.welcome p{{margin:8px 0}}

/* ── Search results ── */
.search-results{{padding:8px 12px}}
.search-result{{
  padding:6px 8px;margin:2px 0;border-radius:4px;cursor:pointer;
  color:var(--text-normal);font-size:13px;
}}
.search-result:hover{{background:var(--bg-hover)}}
.search-result .sr-path{{color:var(--text-faint);font-size:11px}}
.search-result .sr-match{{color:var(--accent);font-size:12px;margin-top:2px}}
.search-highlight{{background:#89b4fa33;color:var(--accent);padding:0 1px;border-radius:2px}}

/* ── Graph view ── */
#graph-view{{
  position:absolute;top:0;left:0;right:0;bottom:0;
  background:var(--bg-tertiary);display:none;flex-direction:column;
}}
#graph-view.active{{display:flex}}
#graph-toolbar{{
  padding:8px 16px;display:flex;align-items:center;gap:8px;
  border-bottom:1px solid var(--border);background:var(--bg-secondary);
  flex-wrap:wrap;
}}
.graph-chip{{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 10px;border-radius:12px;font-size:12px;
  cursor:pointer;border:1px solid var(--border);color:var(--text-normal);
  user-select:none;transition:opacity .15s;
}}
.graph-chip.off{{opacity:0.3}}
.graph-chip .chip-dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
#graph-canvas{{flex:1;cursor:grab}}
#graph-canvas:active{{cursor:grabbing}}
#graph-tooltip{{
  position:absolute;padding:6px 10px;background:var(--bg-secondary);
  border:1px solid var(--border);border-radius:6px;font-size:12px;
  pointer-events:none;display:none;z-index:20;color:var(--text-normal);
  box-shadow:0 2px 8px #0003;
}}
#graph-tooltip .gt-name{{font-weight:600}}
#graph-tooltip .gt-cat{{color:var(--text-faint);font-size:11px}}

/* ── Local graph ── */
#local-graph-container{{
  border-top:1px solid var(--border);padding:8px;background:var(--bg-secondary);
  display:none;
}}
#local-graph-container.active{{display:block}}
#local-graph-container h4{{
  font-size:11px;text-transform:uppercase;letter-spacing:1px;
  color:var(--text-faint);margin-bottom:4px;font-weight:600;
}}
#local-graph-canvas{{width:100%;height:200px;border-radius:4px;cursor:grab}}

/* ── Responsive ── */
@media(max-width:900px){{
  #sidebar{{width:240px}}
  #backlinks-panel{{display:none}}
  #content{{padding:20px 24px}}
}}
@media(max-width:600px){{
  #sidebar{{position:fixed;z-index:10;height:100%;box-shadow:2px 0 8px #0005}}
  #sidebar.collapsed{{width:0}}
}}
</style>
</head>
<body>

<!-- ── Sidebar ── -->
<div id="sidebar">
  <div id="sidebar-header">
    <span>Wiki</span>
    <button onclick="toggleSidebar()" title="Toggle sidebar">&#9776;</button>
  </div>
  <input type="text" id="search-box" placeholder="Search docs..." oninput="onSearch(this.value)">
  <div id="file-tree"></div>
</div>

<!-- ── Main ── -->
<div id="main">
  <div id="toolbar">
    <button onclick="toggleSidebar()" title="Toggle sidebar">&#9776;</button>
    <span id="breadcrumb"></span>
    <button id="graph-btn" onclick="toggleGraphView()" title="Graph View">&#9737;</button>
    <button id="backlinks-toggle" onclick="toggleBacklinks()" title="Backlinks">&#128279;</button>
    <button id="theme-toggle" onclick="toggleTheme()" title="Toggle theme">&#9790;</button>
  </div>
  <div id="content-wrapper">
    <div id="content">
      <div class="welcome">
        <h1>Wiki Viewer</h1>
        <p>Select a document from the sidebar to start reading.</p>
        <p style="font-size:12px">Use the search box or browse the file tree.</p>
      </div>
    </div>
    <div id="local-graph-container">
      <h4>Local Graph</h4>
      <canvas id="local-graph-canvas"></canvas>
    </div>
    <div id="backlinks-panel" class="hidden">
      <h3>Backlinks</h3>
      <div id="backlinks-list"></div>
    </div>
    <!-- Graph full view -->
    <div id="graph-view">
      <div id="graph-toolbar"></div>
      <canvas id="graph-canvas"></canvas>
      <div id="graph-tooltip"><div class="gt-name"></div><div class="gt-cat"></div></div>
    </div>
  </div>
</div>

<script>
// ── Data ──
const DOCS = {data_json};
const BACKLINKS = {backlinks_json};
const RESOLVE = {resolve_json};
const GRAPH_NODES = {gnodes_json};
const GRAPH_EDGES = {gedges_json};

// ── Index ──
const pathIndex = {{}};
DOCS.forEach((d,i) => pathIndex[d.path] = i);

let currentPath = null;
let searchMode = false;

// ── File Tree ──
function buildTree(docs) {{
  const root = {{}};
  docs.forEach(d => {{
    const parts = d.path.split("/");
    let node = root;
    parts.forEach((p, i) => {{
      if (i === parts.length - 1) {{
        node.__files = node.__files || [];
        node.__files.push(d);
      }} else {{
        node[p] = node[p] || {{}};
        node = node[p];
      }}
    }});
  }});
  return root;
}}

function renderTree(node, container, depth) {{
  // folders first
  const folders = Object.keys(node).filter(k => k !== "__files").sort();
  folders.forEach(fname => {{
    const folder = document.createElement("div");
    folder.className = "tree-folder";
    const label = document.createElement("div");
    label.className = "tree-folder-label";
    label.style.paddingLeft = (12 + depth * 8) + "px";
    label.innerHTML = '<span class="arrow open">&#9654;</span><span class="folder-icon">&#128193;</span> ' + esc(fname);
    const children = document.createElement("div");
    children.className = "tree-children";
    label.onclick = () => {{
      const open = !children.classList.contains("hidden");
      children.classList.toggle("hidden", open);
      label.querySelector(".arrow").classList.toggle("open", !open);
    }};
    folder.appendChild(label);
    folder.appendChild(children);
    container.appendChild(folder);
    renderTree(node[fname], children, depth + 1);
  }});
  // files
  if (node.__files) {{
    node.__files.sort((a,b) => a.name.localeCompare(b.name)).forEach(d => {{
      const el = document.createElement("div");
      el.className = "tree-file";
      el.dataset.path = d.path;
      el.style.paddingLeft = (16 + depth * 8) + "px";
      el.innerHTML = '<span class="file-icon">&#128196;</span> ' + esc(d.display || d.name);
      el.onclick = () => openDoc(d.path);
      container.appendChild(el);
    }});
  }}
}}

function initTree() {{
  const tree = document.getElementById("file-tree");
  tree.innerHTML = "";
  const root = buildTree(DOCS);
  renderTree(root, tree, 0);
}}

// ── Markdown → HTML ──
function md(text) {{
  let s = text;

  // Preserve code blocks — extract then reinsert
  const codeBlocks = [];
  s = s.replace(/```(\\w*)\\n([\\s\\S]*?)```/g, (_, lang, code) => {{
    const ph = "\\x00CB" + codeBlocks.length + "\\x00";
    codeBlocks.push('<pre><code class="lang-' + esc(lang) + '">' + esc(code) + '</code></pre>');
    return ph;
  }});

  // Preserve inline code
  const inlineCodes = [];
  s = s.replace(/`([^`]+)`/g, (_, code) => {{
    const ph = "\\x00IC" + inlineCodes.length + "\\x00";
    inlineCodes.push('<code>' + esc(code) + '</code>');
    return ph;
  }});

  // Escape remaining HTML chars
  s = s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Wiki-links [[name|display]] or [[name]]
  s = s.replace(/\\[\\[([^\\]|]+?)(?:\\|([^\\]]+))?\\]\\]/g, (_, name, display) => {{
    const resolved = RESOLVE[name];
    if (resolved && pathIndex[resolved] !== undefined) {{
      return '<a href="#" class="wikilink" data-target="' + esc(resolved) + '">' + esc(display || name) + '</a>';
    }}
    return '<a href="#" class="wikilink-unresolved" title="Unresolved: ' + esc(name) + '">' + esc(display || name) + '</a>';
  }});

  // Tables
  s = s.replace(/^(\\|.+\\|)\\n(\\|[-| :]+\\|)\\n((?:\\|.+\\|\\n?)*)/gm, (_, header, sep, body) => {{
    const hCells = header.split("|").filter(c => c.trim());
    let html = "<table><thead><tr>" + hCells.map(c => "<th>" + c.trim() + "</th>").join("") + "</tr></thead><tbody>";
    body.trim().split("\\n").forEach(row => {{
      const cells = row.split("|").filter(c => c.trim());
      html += "<tr>" + cells.map(c => "<td>" + c.trim() + "</td>").join("") + "</tr>";
    }});
    return html + "</tbody></table>";
  }});

  // Headers
  s = s.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  s = s.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  s = s.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  s = s.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Blockquotes (multi-line)
  s = s.replace(/^(?:&gt; .+\\n?)+/gm, m => {{
    const inner = m.replace(/^&gt; ?/gm, "");
    return "<blockquote>" + inner.trim() + "</blockquote>";
  }});

  // Horizontal rule
  s = s.replace(/^---+$/gm, '<hr>');

  // Bold / Italic
  s = s.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
  s = s.replace(/\\*(.+?)\\*/g, '<em>$1</em>');

  // Unordered lists
  s = s.replace(/^(\\s*)- (.+)$/gm, (_, indent, content) => {{
    const level = Math.floor((indent || "").length / 2);
    return '<li data-level="' + level + '">' + content + '</li>';
  }});
  s = s.replace(/(<li[^>]*>.*<\\/li>\\n?)+/g, m => '<ul>' + m + '</ul>');

  // Ordered lists
  s = s.replace(/^\\d+\\. (.+)$/gm, '<li>$1</li>');

  // Paragraphs (lines not already wrapped)
  s = s.replace(/^(?!<[a-z/])((?!\\s*$).+)$/gm, '<p>$1</p>');

  // Clean up empty paragraphs
  s = s.replace(/<p>\\s*<\\/p>/g, '');

  // Restore code blocks and inline code
  codeBlocks.forEach((html, i) => {{
    s = s.replace("\\x00CB" + i + "\\x00", html);
  }});
  inlineCodes.forEach((html, i) => {{
    s = s.replace("\\x00IC" + i + "\\x00", html);
  }});

  return s;
}}

function esc(s) {{
  if (!s) return "";
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}}

// ── Frontmatter card ──
function renderFM(fm) {{
  if (!fm || Object.keys(fm).length === 0) return "";
  let html = '<div class="fm-card">';
  const displayKeys = ["name","display_name","category","version","dependencies"];
  displayKeys.forEach(k => {{
    if (fm[k] === undefined) return;
    let val = fm[k];
    if (Array.isArray(val)) {{
      val = val.map(v => '<span class="fm-tag">' + esc(String(v)) + '</span>').join(" ");
    }} else {{
      val = esc(String(val));
    }}
    html += '<div class="fm-row"><span class="fm-key">' + esc(k) + '</span><span class="fm-val">' + val + '</span></div>';
  }});
  html += '</div>';
  return html;
}}

// ── Open document ──
function openDoc(path) {{
  const idx = pathIndex[path];
  if (idx === undefined) return;
  if (graphActive) toggleGraphView();
  const doc = DOCS[idx];
  currentPath = path;
  searchMode = false;

  // Render content
  const content = document.getElementById("content");
  content.innerHTML = renderFM(doc.fm) + md(doc.body);

  // Wire up wiki-links
  content.querySelectorAll(".wikilink").forEach(a => {{
    a.onclick = e => {{
      e.preventDefault();
      openDoc(a.dataset.target);
    }};
  }});

  // Breadcrumb
  document.getElementById("breadcrumb").textContent = path;

  // Highlight active in tree
  document.querySelectorAll(".tree-file.active").forEach(el => el.classList.remove("active"));
  const active = document.querySelector('.tree-file[data-path="' + CSS.escape(path) + '"]');
  if (active) {{
    active.classList.add("active");
    active.scrollIntoView({{block:"nearest"}});
  }}

  // Backlinks
  renderBacklinks(path);

  // Local graph
  const docName = doc.fm && doc.fm.name ? doc.fm.name : null;
  if (docName) showLocalGraph(docName);
  else document.getElementById("local-graph-container").classList.remove("active");

  // Scroll to top
  content.scrollTop = 0;

  // Update URL hash
  history.replaceState(null, "", "#" + encodeURIComponent(path));
}}

// ── Backlinks ──
function renderBacklinks(path) {{
  const list = document.getElementById("backlinks-list");
  const bls = BACKLINKS[path] || [];
  if (bls.length === 0) {{
    list.innerHTML = '<div style="color:var(--text-faint)">No backlinks</div>';
    return;
  }}
  list.innerHTML = "";
  bls.forEach(p => {{
    const idx = pathIndex[p];
    const name = idx !== undefined ? (DOCS[idx].display || DOCS[idx].name) : p;
    const el = document.createElement("div");
    el.className = "backlink-item";
    el.innerHTML = esc(name) + '<br><span style="font-size:11px;color:var(--text-faint)">' + esc(p) + '</span>';
    el.onclick = () => openDoc(p);
    list.appendChild(el);
  }});
}}

// ── Search ──
function onSearch(query) {{
  const tree = document.getElementById("file-tree");
  query = query.trim();
  if (!query) {{
    searchMode = false;
    initTree();
    return;
  }}
  searchMode = true;
  const q = query.toLowerCase();
  const results = [];
  DOCS.forEach(d => {{
    let score = 0;
    let matchSnippet = "";
    // Name match (highest priority)
    if (d.name.toLowerCase().includes(q)) score += 10;
    if (d.display.toLowerCase().includes(q)) score += 8;
    // Category match
    if (d.fm.category && String(d.fm.category).toLowerCase().includes(q)) score += 5;
    // Body match
    const bodyLower = d.body.toLowerCase();
    const bodyIdx = bodyLower.indexOf(q);
    if (bodyIdx >= 0) {{
      score += 3;
      const start = Math.max(0, bodyIdx - 30);
      const end = Math.min(d.body.length, bodyIdx + q.length + 50);
      matchSnippet = (start > 0 ? "..." : "") + d.body.slice(start, end).replace(/\\n/g, " ") + (end < d.body.length ? "..." : "");
    }}
    if (score > 0) results.push({{doc: d, score, matchSnippet}});
  }});
  results.sort((a,b) => b.score - a.score);

  tree.innerHTML = "";
  if (results.length === 0) {{
    tree.innerHTML = '<div style="padding:16px;color:var(--text-faint)">No results</div>';
    return;
  }}
  const container = document.createElement("div");
  container.className = "search-results";
  results.slice(0, 50).forEach(r => {{
    const el = document.createElement("div");
    el.className = "search-result";
    let html = '<div>' + highlightMatch(r.doc.display || r.doc.name, q) + '</div>';
    html += '<div class="sr-path">' + esc(r.doc.path) + '</div>';
    if (r.matchSnippet) {{
      html += '<div class="sr-match">' + highlightMatch(r.matchSnippet, q) + '</div>';
    }}
    el.innerHTML = html;
    el.onclick = () => openDoc(r.doc.path);
    container.appendChild(el);
  }});
  tree.appendChild(container);
}}

function highlightMatch(text, q) {{
  const escaped = esc(text);
  const qEsc = esc(q);
  const re = new RegExp("(" + qEsc.replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&") + ")", "gi");
  return escaped.replace(re, '<span class="search-highlight">$1</span>');
}}

// ── Toggle controls ──
function toggleSidebar() {{
  document.getElementById("sidebar").classList.toggle("collapsed");
}}
function toggleBacklinks() {{
  document.getElementById("backlinks-panel").classList.toggle("hidden");
}}
function toggleTheme() {{
  const html = document.documentElement;
  const cur = html.getAttribute("data-theme");
  html.setAttribute("data-theme", cur === "dark" ? "light" : "dark");
  document.getElementById("theme-toggle").innerHTML = cur === "dark" ? "&#9788;" : "&#9790;";
}}

// ══════════════════════════════════════════════════════════════
//  Graph View — Force-directed layout on Canvas
// ══════════════════════════════════════════════════════════════

// 12 色调色板：高辨识度、相邻色差距大
const CAT_COLORS_PALETTE = [
  "#e74c3c","#3498db","#2ecc71","#f39c12","#9b59b6","#1abc9c",
  "#e67e22","#2980b9","#27ae60","#e84393","#00cec9","#fdcb6e"
];
const CAT_COLOR_OTHER = "#8b8fa8";

// 按文档数量降序分配前 11 组，其余归 other
const _catCounts = {{}};
GRAPH_NODES.forEach(n => {{ if (n.category !== "other") _catCounts[n.category] = (_catCounts[n.category]||0) + 1; }});
const _rankedCats = Object.keys(_catCounts)
  .sort((a,b) => _catCounts[b] - _catCounts[a] || a.localeCompare(b));
const CAT_COLORS = {{}};
_rankedCats.slice(0, 11).forEach((cat,i) => {{ CAT_COLORS[cat] = CAT_COLORS_PALETTE[i]; }});
_rankedCats.slice(11).forEach(cat => {{ CAT_COLORS[cat] = CAT_COLOR_OTHER; }});
CAT_COLORS["other"] = CAT_COLOR_OTHER;

function _hexToRgba(hex, a) {{
  const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  return "rgba(" + r + "," + g + "," + b + "," + a + ")";
}}
function nodeColor(node, alpha) {{
  const c = CAT_COLORS[node.category] || CAT_COLOR_OTHER;
  if (alpha !== undefined) return _hexToRgba(c, alpha);
  return c;
}}

let graphActive = false;

// ── Graph state ──
let gNodes = []; // {{id, display, path, category, x, y, vx, vy, r, pinned}}
let gEdges = []; // {{si, ti, type}}  (index-based)
let gIdIndex = {{}}; // id → index
let gCatVisible = {{}};
let gTransform = {{x:0, y:0, scale:1}};
let gDrag = null; // {{nodeIdx, ox, oy}} | null
let gPan = null;  // {{sx, sy, tx, ty}} | null
let gHover = -1;
let gAnimId = 0;
let gInited = false;

function initGraphData() {{
  if (gInited) return;
  gInited = true;
  // build degree map
  const deg = {{}};
  GRAPH_EDGES.forEach(e => {{
    deg[e.s] = (deg[e.s]||0) + 1;
    deg[e.t] = (deg[e.t]||0) + 1;
  }});
  // nodes
  gNodes = GRAPH_NODES.map((n, i) => {{
    const d = deg[n.id] || 0;
    const r = Math.max(8, Math.min(60, 8 + Math.pow(d, 0.7) * 3.6));
    return {{
      ...n, x: (Math.random()-0.5)*800, y: (Math.random()-0.5)*600,
      vx:0, vy:0, r, pinned:false
    }};
  }});
  gIdIndex = {{}};
  gNodes.forEach((n,i) => gIdIndex[n.id] = i);
  // edges (index-based)
  gEdges = [];
  GRAPH_EDGES.forEach(e => {{
    const si = gIdIndex[e.s], ti = gIdIndex[e.t];
    if (si !== undefined && ti !== undefined) gEdges.push({{si, ti, type:e.type}});
  }});
  // categories
  const cats = new Set(gNodes.map(n=>n.category));
  cats.forEach(c => gCatVisible[c] = true);
}}

function buildGraphToolbar() {{
  const tb = document.getElementById("graph-toolbar");
  tb.innerHTML = "";
  const cats = [...new Set(gNodes.map(n=>n.category))].sort();
  cats.forEach(cat => {{
    const cnt = gNodes.filter(n=>n.category===cat).length;
    const chip = document.createElement("span");
    chip.className = "graph-chip";
    const color = CAT_COLORS[cat] || CAT_COLOR_OTHER;
    chip.style.color = color;
    chip.innerHTML = '<span class="chip-dot" style="background:' + color + '"></span>' + cat + ' (' + cnt + ')';
    chip.onclick = () => {{
      gCatVisible[cat] = !gCatVisible[cat];
      chip.classList.toggle("off", !gCatVisible[cat]);
    }};
    tb.appendChild(chip);
  }});
  // edge type toggles
  const depChip = document.createElement("span");
  depChip.className = "graph-chip";
  depChip.textContent = "deps";
  depChip.dataset.etype = "dep";
  depChip.onclick = () => {{
    gShowDep = !gShowDep;
    depChip.classList.toggle("off", !gShowDep);
  }};
  tb.appendChild(depChip);
  const refChip = document.createElement("span");
  refChip.className = "graph-chip";
  refChip.textContent = "refs";
  refChip.dataset.etype = "ref";
  refChip.onclick = () => {{
    gShowRef = !gShowRef;
    refChip.classList.toggle("off", !gShowRef);
  }};
  tb.appendChild(refChip);
}}

let gShowDep = true, gShowRef = true;

function isNodeVisible(n) {{
  return gCatVisible[n.category] !== false;
}}

// ── Force simulation ──
function simStep() {{
  const alpha = 0.3;
  const repulse = 800;
  const attract = 0.005;
  const center = 0.01;
  const damping = 0.85;
  const N = gNodes.length;

  // collect visible indices once
  const visible = [];
  for (let i=0; i<N; i++) {{ if (isNodeVisible(gNodes[i])) visible.push(i); }}
  const vLen = visible.length;

  // repulsion O(N^2)
  for (let vi=0; vi<vLen; vi++) {{
    const i = visible[vi];
    const ni = gNodes[i];
    for (let vj=vi+1; vj<vLen; vj++) {{
      const j = visible[vj];
      const nj = gNodes[j];
      const dx = ni.x - nj.x;
      const dy = ni.y - nj.y;
      const d2 = dx*dx + dy*dy + 1;
      const f = repulse / d2;
      const fx = dx * f, fy = dy * f;
      if (!ni.pinned) {{ ni.vx += fx * alpha; ni.vy += fy * alpha; }}
      if (!nj.pinned) {{ nj.vx -= fx * alpha; nj.vy -= fy * alpha; }}
    }}
  }}

  // edge attraction
  for (let ei=0; ei<gEdges.length; ei++) {{
    const e = gEdges[ei];
    const a = gNodes[e.si], b = gNodes[e.ti];
    if (!isNodeVisible(a) || !isNodeVisible(b)) continue;
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.sqrt(dx*dx + dy*dy) + 0.1;
    const f = (d - 60) * attract;
    const fx = dx/d * f, fy = dy/d * f;
    if (!a.pinned) {{ a.vx += fx * alpha; a.vy += fy * alpha; }}
    if (!b.pinned) {{ b.vx -= fx * alpha; b.vy -= fy * alpha; }}
  }}

  // center gravity + integrate
  for (let vi=0; vi<vLen; vi++) {{
    const n = gNodes[visible[vi]];
    if (n.pinned) continue;
    n.vx -= n.x * center;
    n.vy -= n.y * center;
    n.vx *= damping; n.vy *= damping;
    n.x += n.vx; n.y += n.vy;
  }}
}}

// ── Render ──
function drawGraph(canvas, nodes, edges, transform, hoverIdx, opts) {{
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(W/2 + transform.x, H/2 + transform.y);
  ctx.scale(transform.scale, transform.scale);

  const showDep = opts.showDep !== false;
  const showRef = opts.showRef !== false;

  // active node = hovered or dragged
  const activeIdx = gDrag ? gDrag.nodeIdx : hoverIdx;
  // build neighbor set for active node
  let neighborSet = null;
  let activeEdgeSet = null;
  if (activeIdx >= 0) {{
    neighborSet = new Set();
    activeEdgeSet = new Set();
    neighborSet.add(activeIdx);
    edges.forEach((e, ei) => {{
      if (e.si === activeIdx || e.ti === activeIdx) {{
        neighborSet.add(e.si);
        neighborSet.add(e.ti);
        activeEdgeSet.add(ei);
      }}
    }});
  }}

  const dimmed = activeIdx >= 0;

  // edges — batch by style to reduce beginPath/stroke calls
  // group: dimmed edges, active edges, normal dep edges by color, normal ref edges by color
  const edgeBuckets = {{}};  // grouped edge batches
  const activeEdges = [];
  edges.forEach((e, ei) => {{
    const a = nodes[e.si], b = nodes[e.ti];
    if (!isNodeVisible(a) || !isNodeVisible(b)) return;
    if (e.type === "dep" && !showDep) return;
    if (e.type === "ref" && !showRef) return;
    const isActive = activeEdgeSet && activeEdgeSet.has(ei);
    if (isActive) {{
      const ec = nodeColor(a);
      activeEdges.push({{ax:a.x, ay:a.y, bx:b.x, by:b.y, color:ec, dash:e.type==="ref"}});
    }} else {{
      let style, lw, dash = e.type === "ref";
      if (dimmed) {{
        style = "rgba(80,80,80,0.15)"; lw = 0.5;
      }} else {{
        const ec = nodeColor(a, dash ? 0.7 : 1);
        style = ec; lw = dash ? 1.5 : 2.5;
      }}
      const key = style + "|" + lw + "|" + (dash?1:0);
      if (!edgeBuckets[key]) edgeBuckets[key] = {{style, lw, dash, lines:[]}};
      edgeBuckets[key].lines.push(a.x, a.y, b.x, b.y);
    }}
  }});
  // draw batched normal edges
  for (const key in edgeBuckets) {{
    const b = edgeBuckets[key];
    ctx.strokeStyle = b.style;
    ctx.lineWidth = b.lw;
    ctx.setLineDash(b.dash ? [3,3] : []);
    ctx.beginPath();
    const L = b.lines;
    for (let i=0; i<L.length; i+=4) {{
      ctx.moveTo(L[i], L[i+1]);
      ctx.lineTo(L[i+2], L[i+3]);
    }}
    ctx.stroke();
  }}
  // draw active edges on top
  if (activeEdges.length) {{
    ctx.lineWidth = 4;
    ctx.setLineDash([]);
    // group active by color
    const aBuckets = {{}};
    activeEdges.forEach(e => {{
      const k = e.color + (e.dash?"|d":"");
      if (!aBuckets[k]) aBuckets[k] = {{color:e.color, dash:e.dash, lines:[]}};
      aBuckets[k].lines.push(e.ax, e.ay, e.bx, e.by);
    }});
    for (const k in aBuckets) {{
      const b = aBuckets[k];
      ctx.strokeStyle = b.color;
      ctx.setLineDash(b.dash ? [3,3] : []);
      ctx.beginPath();
      const L = b.lines;
      for (let i=0; i<L.length; i+=4) {{
        ctx.moveTo(L[i], L[i+1]);
        ctx.lineTo(L[i+2], L[i+3]);
      }}
      ctx.stroke();
    }}
  }}
  ctx.setLineDash([]);

  // nodes — batch by fill color
  const nodeBuckets = {{}};
  const nodeStrokes = [];
  nodes.forEach((n, i) => {{
    if (!isNodeVisible(n)) return;
    const color = nodeColor(n);
    const isNeighbor = neighborSet && neighborSet.has(i);
    let fill;
    if (dimmed && !isNeighbor) {{
      fill = "rgba(80,80,80,0.25)";
    }} else if (i === activeIdx) {{
      fill = color;
    }} else {{
      fill = isNeighbor ? color : nodeColor(n, 0.8);
    }}
    if (!nodeBuckets[fill]) nodeBuckets[fill] = [];
    nodeBuckets[fill].push(n.x, n.y, n.r);
    if (i === activeIdx) {{
      nodeStrokes.push({{x:n.x, y:n.y, r:n.r, style:"#fff", lw:3}});
    }} else if (isNeighbor && dimmed) {{
      nodeStrokes.push({{x:n.x, y:n.y, r:n.r, style:color, lw:1.5}});
    }}
  }});
  for (const fill in nodeBuckets) {{
    ctx.fillStyle = fill;
    const arr = nodeBuckets[fill];
    for (let i=0; i<arr.length; i+=3) {{
      ctx.beginPath();
      ctx.arc(arr[i], arr[i+1], arr[i+2], 0, Math.PI*2);
      ctx.fill();
    }}
  }}
  // node strokes (few — active + neighbors)
  nodeStrokes.forEach(s => {{
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
    ctx.strokeStyle = s.style;
    ctx.lineWidth = s.lw;
    ctx.stroke();
  }});

  // labels: show all when zoomed in, or neighbors when active, or large nodes
  const textColor = getComputedStyle(document.documentElement).getPropertyValue("--text-normal").trim() || "#cdd6f4";
  ctx.textAlign = "center";
  const showAll = transform.scale >= 0.6;
  nodes.forEach((n, i) => {{
    if (!isNodeVisible(n)) return;
    const isNeighbor = neighborSet && neighborSet.has(i);
    if (dimmed && !isNeighbor) return;
    if (showAll || isNeighbor || n.r >= 20 || i === hoverIdx) {{
      const fs = Math.max(8, Math.min(20, Math.round(n.r * 0.6)));
      ctx.font = fs + "px sans-serif";
      ctx.fillStyle = textColor;
      ctx.fillText(n.display || n.id, n.x, n.y - n.r - 4);
    }}
  }});

  ctx.restore();
}}

function graphLoop() {{
  if (!graphActive) return;
  simStep();
  const canvas = document.getElementById("graph-canvas");
  drawGraph(canvas, gNodes, gEdges, gTransform, gHover, {{showDep:gShowDep, showRef:gShowRef}});
  gAnimId = requestAnimationFrame(graphLoop);
}}

function screenToGraph(mx, my, canvas) {{
  const W = canvas.width, H = canvas.height;
  return {{
    x: (mx - W/2 - gTransform.x) / gTransform.scale,
    y: (my - H/2 - gTransform.y) / gTransform.scale
  }};
}}

function findNodeAt(gx, gy, nodes) {{
  for (let i = nodes.length-1; i >= 0; i--) {{
    if (!isNodeVisible(nodes[i])) continue;
    const dx = nodes[i].x - gx, dy = nodes[i].y - gy;
    if (dx*dx + dy*dy <= nodes[i].r * nodes[i].r + 16) return i;
  }}
  return -1;
}}

function setupGraphEvents(canvas) {{
  const tooltip = document.getElementById("graph-tooltip");

  canvas.addEventListener("mousedown", e => {{
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (canvas.width/rect.width);
    const my = (e.clientY - rect.top) * (canvas.height/rect.height);
    const gp = screenToGraph(mx, my, canvas);
    const idx = findNodeAt(gp.x, gp.y, gNodes);
    if (idx >= 0) {{
      gDrag = {{nodeIdx: idx, ox: gNodes[idx].x - gp.x, oy: gNodes[idx].y - gp.y}};
      gNodes[idx].pinned = true;
    }} else {{
      gPan = {{sx: e.clientX, sy: e.clientY, tx: gTransform.x, ty: gTransform.y}};
    }}
  }});

  canvas.addEventListener("mousemove", e => {{
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (canvas.width/rect.width);
    const my = (e.clientY - rect.top) * (canvas.height/rect.height);
    if (gDrag) {{
      const gp = screenToGraph(mx, my, canvas);
      gNodes[gDrag.nodeIdx].x = gp.x + gDrag.ox;
      gNodes[gDrag.nodeIdx].y = gp.y + gDrag.oy;
    }} else if (gPan) {{
      gTransform.x = gPan.tx + (e.clientX - gPan.sx);
      gTransform.y = gPan.ty + (e.clientY - gPan.sy);
    }} else {{
      const gp = screenToGraph(mx, my, canvas);
      const idx = findNodeAt(gp.x, gp.y, gNodes);
      gHover = idx;
      if (idx >= 0) {{
        tooltip.style.display = "block";
        tooltip.style.left = (e.clientX + 12) + "px";
        tooltip.style.top = (e.clientY - 10) + "px";
        tooltip.querySelector(".gt-name").textContent = gNodes[idx].display || gNodes[idx].id;
        tooltip.querySelector(".gt-cat").textContent = gNodes[idx].category;
        canvas.style.cursor = "pointer";
      }} else {{
        tooltip.style.display = "none";
        canvas.style.cursor = "grab";
      }}
    }}
  }});

  canvas.addEventListener("mouseup", e => {{
    if (gDrag) {{
      gNodes[gDrag.nodeIdx].pinned = false;
      gDrag = null;
    }}
    gPan = null;
  }});

  canvas.addEventListener("dblclick", e => {{
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (canvas.width/rect.width);
    const my = (e.clientY - rect.top) * (canvas.height/rect.height);
    const gp = screenToGraph(mx, my, canvas);
    const idx = findNodeAt(gp.x, gp.y, gNodes);
    if (idx >= 0 && gNodes[idx].path) {{
      const p = gNodes[idx].path;
      if (pathIndex[p] !== undefined) {{
        toggleGraphView(); // close graph
        openDoc(p);
      }}
    }}
  }});

  canvas.addEventListener("wheel", e => {{
    e.preventDefault();
    const factor = e.deltaY > 0 ? 0.9 : 1.1;
    gTransform.scale = Math.max(0.1, Math.min(5, gTransform.scale * factor));
  }}, {{passive:false}});
}}

function resizeGraphCanvas() {{
  const canvas = document.getElementById("graph-canvas");
  const gv = document.getElementById("graph-view");
  canvas.width = gv.clientWidth;
  canvas.height = gv.clientHeight - 42;
}}

let graphEventsSetup = false;

function toggleGraphView() {{
  const gv = document.getElementById("graph-view");
  graphActive = !graphActive;
  gv.classList.toggle("active", graphActive);
  if (graphActive) {{
    initGraphData();
    buildGraphToolbar();
    resizeGraphCanvas();
    if (!graphEventsSetup) {{
      setupGraphEvents(document.getElementById("graph-canvas"));
      graphEventsSetup = true;
    }}
    gTransform = {{x:0, y:0, scale:1}};
    // 先跑 120 步模拟让布局稳定，再 fit-to-view
    for (let i = 0; i < 120; i++) simStep();
    fitGraphToView();
    graphLoop();
  }} else {{
    cancelAnimationFrame(gAnimId);
  }}
}}

function fitGraphToView() {{
  const canvas = document.getElementById("graph-canvas");
  const W = canvas.width, H = canvas.height;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  let count = 0;
  gNodes.forEach(n => {{
    if (!isNodeVisible(n)) return;
    minX = Math.min(minX, n.x - n.r);
    maxX = Math.max(maxX, n.x + n.r);
    minY = Math.min(minY, n.y - n.r);
    maxY = Math.max(maxY, n.y + n.r);
    count++;
  }});
  if (count === 0) return;
  const graphW = maxX - minX + 100; // padding
  const graphH = maxY - minY + 100;
  const scaleX = W / graphW;
  const scaleY = H / graphH;
  const scale = Math.min(scaleX, scaleY, 2) * 0.9; // cap at 2x, 90% fill
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  gTransform = {{x: -cx * scale, y: -cy * scale, scale: scale}};
}}

// ══════════════════════════════════════════════════════════════
//  Local Graph — small graph for current document
// ══════════════════════════════════════════════════════════════

let lgNodes = [], lgEdges = [], lgTransform = {{x:0,y:0,scale:1}}, lgAnimId = 0, lgHover = -1;

function showLocalGraph(docName) {{
  initGraphData();
  const container = document.getElementById("local-graph-container");
  const idx = gIdIndex[docName];
  if (idx === undefined) {{
    container.classList.remove("active");
    return;
  }}

  // collect neighbors (1 hop)
  const neighborSet = new Set([docName]);
  gEdges.forEach(e => {{
    if (gNodes[e.si].id === docName) neighborSet.add(gNodes[e.ti].id);
    if (gNodes[e.ti].id === docName) neighborSet.add(gNodes[e.si].id);
  }});

  if (neighborSet.size <= 1) {{
    container.classList.remove("active");
    return;
  }}

  container.classList.add("active");

  // build local nodes/edges
  const localIdxMap = {{}};
  lgNodes = [];
  neighborSet.forEach(id => {{
    const gi = gIdIndex[id];
    if (gi === undefined) return;
    localIdxMap[id] = lgNodes.length;
    const angle = Math.random() * Math.PI * 2;
    const dist = id === docName ? 0 : 80 + Math.random() * 40;
    lgNodes.push({{
      ...gNodes[gi],
      x: Math.cos(angle) * dist, y: Math.sin(angle) * dist,
      vx:0, vy:0, r: id === docName ? 8 : gNodes[gi].r,
      pinned: id === docName,
      highlight: id === docName
    }});
  }});

  lgEdges = [];
  gEdges.forEach(e => {{
    const si = localIdxMap[gNodes[e.si].id], ti = localIdxMap[gNodes[e.ti].id];
    if (si !== undefined && ti !== undefined) lgEdges.push({{si, ti, type:e.type}});
  }});

  lgTransform = {{x:0, y:0, scale:1}};
  lgHover = -1;

  const canvas = document.getElementById("local-graph-canvas");
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = 200;

  // simple sim — run 80 ticks then draw
  const origVisible = isNodeVisible;
  // all local nodes visible
  const _iso = (n) => true;

  cancelAnimationFrame(lgAnimId);

  let ticks = 0;
  function lgLoop() {{
    // sim
    const alpha = 0.4;
    for (let i=0;i<lgNodes.length;i++) {{
      for (let j=i+1;j<lgNodes.length;j++) {{
        let dx = lgNodes[i].x - lgNodes[j].x;
        let dy = lgNodes[i].y - lgNodes[j].y;
        let d2 = dx*dx+dy*dy+1;
        let f = 300/d2;
        if (!lgNodes[i].pinned) {{ lgNodes[i].vx += dx*f*alpha; lgNodes[i].vy += dy*f*alpha; }}
        if (!lgNodes[j].pinned) {{ lgNodes[j].vx -= dx*f*alpha; lgNodes[j].vy -= dy*f*alpha; }}
      }}
    }}
    lgEdges.forEach(e => {{
      const a=lgNodes[e.si], b=lgNodes[e.ti];
      let dx=b.x-a.x, dy=b.y-a.y, d=Math.sqrt(dx*dx+dy*dy)+0.1;
      let f=(d-50)*0.02;
      if (!a.pinned) {{ a.vx+=dx/d*f; a.vy+=dy/d*f; }}
      if (!b.pinned) {{ b.vx-=dx/d*f; b.vy-=dy/d*f; }}
    }});
    lgNodes.forEach(n => {{
      if (n.pinned) return;
      n.vx *= 0.8; n.vy *= 0.8;
      n.x += n.vx; n.y += n.vy;
    }});

    // draw
    const ctx = canvas.getContext("2d");
    const W=canvas.width, H=canvas.height;
    ctx.clearRect(0,0,W,H);
    ctx.save();
    ctx.translate(W/2, H/2);

    lgEdges.forEach(e => {{
      const a=lgNodes[e.si], b=lgNodes[e.ti];
      const ec = nodeColor(a, e.type==="dep" ? 1 : 0.7);
      ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y);
      ctx.strokeStyle = ec;
      ctx.lineWidth = e.type==="dep" ? 2.5 : 1.5;
      if (e.type==="ref") ctx.setLineDash([2,2]); else ctx.setLineDash([]);
      ctx.stroke();
    }});
    ctx.setLineDash([]);

    lgNodes.forEach((n,i) => {{
      const color = nodeColor(n);
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI*2);
      ctx.fillStyle = n.highlight ? "#fff" : color;
      ctx.fill();
      if (n.highlight) {{
        ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();
      }}
    }});

    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue("--text-normal").trim() || "#cdd6f4";
    ctx.font = "9px sans-serif"; ctx.textAlign = "center";
    lgNodes.forEach(n => {{
      ctx.fillText(n.display||n.id, n.x, n.y - n.r - 3);
    }});

    ctx.restore();
    ticks++;
    if (ticks < 120) lgAnimId = requestAnimationFrame(lgLoop);
  }}
  lgLoop();

  // click to navigate
  canvas.onclick = e => {{
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (canvas.width/rect.width) - canvas.width/2;
    const my = (e.clientY - rect.top) * (canvas.height/rect.height) - canvas.height/2;
    for (let i=lgNodes.length-1;i>=0;i--) {{
      const dx=lgNodes[i].x-mx, dy=lgNodes[i].y-my;
      if (dx*dx+dy*dy <= lgNodes[i].r*lgNodes[i].r+16) {{
        if (lgNodes[i].path && pathIndex[lgNodes[i].path] !== undefined) {{
          openDoc(lgNodes[i].path);
        }}
        return;
      }}
    }}
  }};
}}

// ── Keyboard shortcuts ──
document.addEventListener("keydown", e => {{
  // Ctrl/Cmd + K → focus search
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {{
    e.preventDefault();
    document.getElementById("search-box").focus();
  }}
  // Escape → clear search
  if (e.key === "Escape") {{
    const sb = document.getElementById("search-box");
    if (document.activeElement === sb) {{
      sb.value = "";
      onSearch("");
      sb.blur();
    }}
  }}
}});

// ── Init ──
initTree();

// Open doc from URL hash
if (location.hash) {{
  const path = decodeURIComponent(location.hash.slice(1));
  if (pathIndex[path] !== undefined) openDoc(path);
}}
</script>
</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(
        description="生成 Obsidian 风格离线 Wiki 检索页面",
    )
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT),
                        help=f"输出 HTML 路径 (默认: {DEFAULT_OUTPUT})")
    parser.add_argument("--light", action="store_true",
                        help="默认使用亮色主题")
    args = parser.parse_args()

    print(f"[scan] wiki dir: {WIKI_ROOT}")
    docs = collect_docs()
    print(f"  found {len(docs)} docs")

    wiki_map = load_wiki_map()
    print(f"  wiki-map: {len(wiki_map)} entries")

    backlinks = build_backlinks(docs, wiki_map)
    bl_count = sum(len(v) for v in backlinks.values())
    print(f"  backlinks: {bl_count} links")

    graph_nodes, graph_edges = build_graph_data(docs, wiki_map)
    print(f"  graph: {len(graph_nodes)} nodes, {len(graph_edges)} edges")

    theme = "light" if args.light else "dark"
    html = build_html(docs, backlinks, wiki_map, graph_nodes, graph_edges,
                      default_theme=theme)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    size_kb = output_path.stat().st_size / 1024
    print(f"\n[done] {output_path}")
    print(f"  size: {size_kb:.0f} KB")
    print(f"  theme: {theme}")
    print(f"  open in browser to use")


if __name__ == "__main__":
    main()
