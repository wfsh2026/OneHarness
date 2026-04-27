# harness/tools/ 工具目录说明

---

## 目录结构

```
harness/tools/
├── session-sync.sh              ← 会话状态管理（active.md / session-log.md）
├── codegen/                     ← 代码生成脚本（Ability/GPO/Mode/Scene 等）
├── framework-sync/              ← 框架 ↔ 项目同步工具（仅 framework 仓库使用）
├── framework-manifest/          ← 版本发布工具（仅 framework 仓库使用）
├── project-git-clone/           ← 各项目仓库拉取脚本
├── biu2-framework/              ← biubiubiu2-framework 专属工具（仅同步到该项目）
│   ├── README.md                ← 说明文件
│   ├── requirements.txt         ← Python 依赖
│   ├── framework-sync/          ← biu2 游戏代码同步工具
│   └── framework-manifest/      ← biu2 版本管理工具
├── wiki/                        ← 知识库工具
│   ├── wiki_log.py             ← wiki/log.md 追加模块（公共 + CLI）
│   ├── wiki-resolve.py          ← wiki-link 解析 + wiki-map 生成
│   ├── build-wiki-html.py       ← Obsidian 风格离线 Wiki HTML 检索页面生成器
│   ├── migrate-wiki.py          ← 路径引用 → [[wiki-link]] 批量迁移
│   ├── update-graph.py          ← 代码知识图谱（可选，需 tree-sitter）
│   ├── requirements.txt         ← update-graph.py 的 Python 依赖
│   └── features/                ← 功能包工具
│       ├── auto-assign.py       ← 未编目文件自动归属（⚠️ 待适配 .md 格式）
│       ├── wiki-sync.py          ← **wiki 管理中枢**（调度所有子工具）
│       ├── feature-check.py     ← feature 漂移检测（wiki-sync 调用）
│       ├── check-coverage.py    ← 覆盖率报告
│       ├── build-glossary.py    ← 从代码枚举/常量自动生成 glossary.md
│       └── migrate-json-to-md.py ← feature JSON → MD 迁移工具
├── webgl/                       ← WebGL 本地测试服务器
│   ├── serve.sh                 ← 启动服务器（前台运行，Ctrl+C 停止）
│   └── _server.py               ← Python 服务器核心
├── ugc/                         ← UGC 工具
│   ├── README.md                ← 说明文件
│   └── check-ugc-hooks.sh      ← UGC 钩子完整性检查（37 检查点）
├── Workflow/                    ← 工作流工具
│   └── workflow-dev/
│       └── gate-check.sh        ← 开发流程门控检查
└── mcps/                        ← MCP 工具说明
    └── UnityMCP.txt
```

---

## 一、session-sync.sh — 会话状态管理

所有 `active.md` / `session-log.md` 的写入**必须**通过此脚本执行，禁止手动编辑。

```bash
export SESSION_FEATURE="功能名"

session-sync.sh init --template dev              # 初始化
session-sync.sh stage --phase N --text "..."      # 阶段跃迁（自动门控）
session-sync.sh progress --num "..." --agent "..." --content "..."  # 进度
session-sync.sh doc --name "..." --path "..." --status "..."        # 文档
session-sync.sh adr --id N --point "..." --decision "..."           # 决策
session-sync.sh bug --id N --symptom "..." --cause "..." --fix "..." # Bug
session-sync.sh log --title "..." --background "..." --reasoning "..." --conclusion "..."
```

> 完整文档见 `session-sync.sh --help`

---

## 二、codegen/ — 代码生成

AI 开发 Ability / GPO / Mode / Scene 等功能时，**必须优先调用对应生成脚本**。

| 脚本 | 用途 |
|------|------|
| `ability-gen.sh` | 新建 Ability 全套（6 CREATE + 4 MODIFY） |
| `gpo-gen.sh` | 新建 GPO Server/Client System（2 CREATE + 5 MODIFY） |
| `gpom-gen.sh` | 新建 GPOM 模板数据（1 CREATE） |
| `mode-gen.sh` | 新建 Mode 全套（2 CREATE + 3 MODIFY） |
| `component-gen.sh` | 新建 Component 模板（1 CREATE） |
| `scene-gen.sh` | 新建场景全链路（4 CREATE + 2 MODIFY + 1 MCP） |
| `scene-server-gen.sh` | 服务端场景转换（2 CREATE + 1 MCP） |
| `feature-sync.py` | 按功能包同步文件到目标项目 |

> 详细参数见 [[codegen/README]]

---

## 三、framework-sync/ — 框架同步

**仅在 framework 仓库中使用，不同步到游戏项目。**

```bash
# framework → 游戏项目
bash aigc/harness/tools/framework-sync/frameworkToProject-diff.sh all
bash aigc/harness/tools/framework-sync/frameworkToProject-sync.sh shotting-duck-ugc

# 游戏项目 → framework
bash aigc/harness/tools/framework-sync/projectToFramework-diff.sh shotting-duck-ugc
bash aigc/harness/tools/framework-sync/projectToFramework-sync.sh shotting-duck-ugc
```

> ⚠️ 必须先 diff 确认再 sync，不得直接执行 sync

---

## 四、wiki/ — 知识库工具

### 4.1 基础设施

| 工具 | 用途 |
|------|------|
| `wiki-resolve.py` | `--build` 生成 wiki-map.json · `--resolve` 解析链接 · `--check` 完整性检查 |
| `build-wiki-html.py` | Obsidian 风格离线 Wiki HTML 检索页面生成器（`--output` 指定输出路径 · `--light` 亮色主题） |
| `migrate-wiki.py` | 路径引用 → `[[wiki-link]]` 批量迁移（`--write` 执行） |
| `wiki_log.py` | `wiki/log.md` 追加 — Python import 或 CLI：`python3 wiki_log.py <type> <title> [details]` |
| `check-system-map.py` | system-map §9 实例清单同步检查（从代码 Switch 文件自动提取并对比） |

### 4.2 功能包工具 (features/)

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| `wiki-sync.py` | **wiki 管理中枢**（纯调度器，调用以下所有子工具） | `--init` `--update` `--repo` |
| `feature-check.py` | feature 漂移检测（wiki-sync Step 1） | `--repo <key>` |
| `check-system-map.py` | system-map 同步检查（wiki-sync Step 2） | `--sync` `--verbose` |
| `auto-assign.py` | 未编目文件 → 自动归属功能包（⚠️ 待适配 .md） | `--write` `--stdin` |
| `check-coverage.py` | 覆盖率报告 | `--summary` `--suggest` |
| `build-glossary.py` | 从代码枚举/常量生成 glossary.md（wiki-sync Step 4） | `--init` `--write` |
| `migrate-json-to-md.py` | feature JSON → MD 格式迁移 | `--write` `--single` |

```bash
# 典型工作流（一条命令搞定）
python3 aigc/harness/tools/wiki/features/wiki-sync.py           # 检查
python3 aigc/harness/tools/wiki/features/wiki-sync.py --update  # 全量同步
```

### 4.3 代码图谱（可选）

```bash
pip install -r aigc/harness/tools/wiki/requirements.txt

python3 aigc/harness/tools/wiki/update-graph.py                # 生成图谱 + 报告
python3 aigc/harness/tools/wiki/update-graph.py --query Tank    # 子图查询
python3 aigc/harness/tools/wiki/update-graph.py --html          # HTML 可视化
```

> AI 读 `GRAPH_REPORT.md`，不要直接读 `graph.json`（10-30MB 会爆 context）

### 4.4 自动日志

所有写入型工具执行后会自动向 `wiki/log.md` 追加记录。AI 手动修改 wiki/ 文件后须手动补日志：

```bash
python3 aigc/harness/tools/wiki/wiki_log.py ingest "system-map 更新" "新增载具系统条目"
```

---

## 五、webgl/ — WebGL 本地测试服务器

Unity WebGL 构建的本地 HTTP 服务器，带完整 MIME / CORS / SharedArrayBuffer 支持。

```bash
# 启动（前台运行，Ctrl+C 自动停止）
bash aigc/harness/tools/webgl/serve.sh

# 指定目录和端口
bash aigc/harness/tools/webgl/serve.sh /path/to/WebGL --port 9000
```

| 文件 | 说明 |
|------|------|
| `serve.sh` | 前台启动服务器，Ctrl+C 或关闭终端自动停止 |
| `_server.py` | Python HTTP 服务器核心（.wasm/.data MIME、.gz/.br 编码、COOP/COEP 头） |

---

## 六、其他

| 目录 | 用途 |
|------|------|
| `framework-manifest/` | 版本发布（`release.sh` + `scan-manifest.sh`），仅 framework |
| `project-git-clone/` | 各项目 clone/切分支脚本 |
| `ugc/` | UGC 钩子完整性检查（`check-ugc-hooks.sh`，37 检查点） |
| `Workflow/workflow-dev/` | 开发流程门控（`gate-check.sh`） |
| `mcps/` | MCP 工具说明文档 |
