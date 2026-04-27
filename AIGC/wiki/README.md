# Wiki 知识库

> AI Agent 理解项目的知识模型。由 AI 全权维护（knowledge/ 层）。
>
> **通用检索规则**见 [[system-map-rules]]（预检流程、意图识别原则、会话执行协议）。
> **构建工作流**见 [[workflow-knowledge]]。

---

## 目录结构

```
wiki/
├── README.md              ← 本文件（知识库总说明）
├── log.md                 ← 操作日志（所有写入自动追加）
│
├── raw/                   ← 原始素材（LLM 只读，修改需用户授权）
│   └── biu2-framework/
│       ├── features/          功能包 JSON 定义 + feature-format.md（格式规范）
│       ├── 内容边界定义/        系统边界文档（8 个系统）
│       ├── 范例文档/            参考实现（8 个系统）
│       └── infra/              基础设施文档（构建系统等）
│
└── knowledge/             ← LLM 维护的成品知识（AI 全权管理）
    ├── system-map.md          系统导航（P0：AI 首读）
    ├── wiki-map.json          wiki-link 索引（P2：自动生成）
    ├── graph.json             代码图谱数据（P3：可选）
    ├── graph.html / html/     图谱可视化
    └── GRAPH_REPORT.md        图谱架构概览
```

---

## 知识层级

```
┌──────────────────────────────────────────────────────────┐
│  核心层（AI 全权维护）                                      │
│                                                          │
│  系统地图 (knowledge/system-map.md)    ← P0：全局导航     │
│  "项目有哪些系统、代码在哪、文档在哪"                        │
│                                                          │
│  功能目录 (raw/features/*.json)        ← P1：功能定位     │
│  "这个功能需要哪些文件、依赖什么"                           │
├──────────────────────────────────────────────────────────┤
│  辅助层                                                   │
│                                                          │
│  文档索引 (knowledge/wiki-map.json)    ← P2：文档解析     │
│  "[[wiki-link]] 对应哪个文件"                              │
│                                                          │
│  代码图谱 (knowledge/graph.*)          ← P3：可选工具     │
│  HTML 可视化 + features 辅助归档                           │
└──────────────────────────────────────────────────────────┘
```

---

## 规则

1. **`raw/` 只读** — LLM 不可直接修改，需用户授权
2. **`knowledge/` AI 全权维护** — AI 在每次功能开发完成后主动更新
3. **`wiki-map.json` 自动生成** — 由 `wiki-resolve.py --build` 生成，禁止手动编辑
4. **`log.md` 自动追加** — 所有写入型工具执行后自动记录

---

## system-map 维护方式

**system-map.md 由 AI 全权维护**，不需要人工参与。

### 文件职责分工

| 文件 | 职责 | 内容 |
|------|------|------|
| [[knowledge/system-map]] | **项目数据** | 系统地图表格、意图关键词、依赖关系、文档清单、实例清单 |
| [[system-map-rules]] | **执行协议** | 预检流程、意图识别原则、会话执行协议、降级处理 |

### 编写规范

system-map.md 的章节结构（v2.1，4 模块）：

```
§一 项目概述         — 项目身份 + 关键目录 + 必读文件
§二 系统地图与意图识别 — 系统总表（含代码/文档/规范列）+ 意图关键词映射
§三 已有实例清单      — GPO/Mode/AB/AE 实例（由 check-system-map.py 同步检查）
§四 系统依赖关系      — 系统间依赖方向 + 生成顺序
```

**使用流程**：

```
用户请求 → §一 确认项目 → §二 关键词匹配系统 → §二 系统表找文档
         → §三 检查已有实例 → §四 确定执行顺序 → 开始开发
```

**各模块规则**：

| 模块 | 规则 |
|------|------|
| §一 | 必须包含项目基本属性表、关键目录表、必读文件列表 |
| §二 系统总表 | 每行必须包含：系统名、描述、代码目录、边界定义文档、范例文档、开发规范、base feature（7 列） |
| §二 关键词表 | 必须覆盖系统总表中的所有系统 |
| §三 实例清单 | 必须与代码 Switch 分支一致（用 `check-system-map.py` 验证）；每行必须包含 `feature` 列指向对应的 feature.json name |
| §四 | 必须标注生成顺序（被依赖的先生成） |
| 版本号 | 每次更新递增（文件底部 `*文档版本：vX.Y*`） |

**system-map 与 features 的关联规则**：
- §二 系统总表的 `base feature` 列 = 该系统框架代码的 feature wiki-link（如 `[[gpo-base]]`）
- §三 实例清单的 `feature` 列 = 该实例对应的 feature wiki-link（如 `[[feiyu]]`）
- 颗粒度规则：1 个实例清单条目 = 1 个 feature（详见 [[feature-format]] §二）
- 新增系统时必须同时创建对应的 base feature
- 新增实例时必须同时创建对应的 feature

### 触发更新的场景

| 场景 | 更新内容 |
|------|---------|
| 新增游戏系统 | §二 + §三 + §四 |
| 新增实例（Buff/Mode/IdCard 等） | §三 + 对应 feature.md |
| 新建边界定义/范例文档 | §二 对应列 |
| 代码目录结构变化 | §二 关键代码目录 |

### AI 维护时机

- **功能开发完成时** — [项目负责人] 主动检查
- **framework 同步后** — 运行 `wiki-resolve.py --check` 验证无断链
- **拉取代码后** — 运行 `wiki-sync.py` 检测知识库漂移（见下节）

---

## 增量漂移检测

> 当成员在 git 中新增/删除/修改了 .cs 文件，知识库需要感知并同步更新。

### 工具

`wiki-sync.py` 是 wiki 管理中枢，一条命令调度所有子工具：

```bash
# 全量检查（只读，不写入）
python3 aigc/harness/tools/wiki/features/wiki-sync.py

# 全量同步（自动写入 + 更新基准）
python3 aigc/harness/tools/wiki/features/wiki-sync.py --update

# 只检查指定仓库
python3 aigc/harness/tools/wiki/features/wiki-sync.py --repo script

# 首次初始化（自动发现子仓库）
python3 aigc/harness/tools/wiki/features/wiki-sync.py --init
```

`--update` 自动执行：feature 漂移检测 → system-map --sync → wiki-map 重建 → 断链检查 → 名词表重建 → 更新基准 commit

### 检测内容

| 检测项 | 含义 | 建议操作 |
|--------|------|---------|
| 新增未覆盖 | 新文件不属于任何 feature | 创建 feature.md 或追加到已有 feature |
| 新增 BSO*.cs | 疑似新 Buff | 创建 buff-xxx.md |
| 已删除仍引用 | 文件已删但 feature.md 还写着 | 从 feature.md 移除该路径 |

### 配置

仓库列表和 sync commit 存储在 `aigc/wiki/wiki-env.json`（项目专有，不随 framework 同步）。
首次使用 `--init` 自动生成，之后 `--update` 自动更新 sync 字段。

---

## Wiki-Link 格式

本框架的 `.md` 文档采用 **Obsidian wiki-link** 格式引用：

```markdown
详见 [[scene-code]]              ← 文件名即链接
详见 [[codegen/README]]          ← 有同名文件时用父目录消歧
```

### 解析方式

| 方法 | 命令 |
|------|------|
| 查询单个 | `python3 aigc/harness/tools/wiki/wiki-resolve.py --resolve "scene-code"` |
| 批量解析 | `python3 aigc/harness/tools/wiki/wiki-resolve.py --file <path>` |
| 完整性检查 | `python3 aigc/harness/tools/wiki/wiki-resolve.py --check` |
| 重建缓存 | `python3 aigc/harness/tools/wiki/wiki-resolve.py --build` |
| 路径迁移 | `python3 aigc/harness/tools/wiki/migrate-wiki.py [--write]` |

> 新增 `.md` 文件后应运行 `--build` 更新 `wiki-map.json`。

---

## 功能目录 (features/)

每个 `feature.json` 描述一组相关代码文件及其依赖关系。

- **格式规范**：见 `raw/biu2-framework/features/feature-format.md`
- **索引文件**：`wiki-map.json`（文档索引），由工具自动生成

### 管理工具

```bash
# 覆盖率检查
python3 aigc/harness/tools/wiki/features/check-coverage.py --summary

# wiki-link 验证
python3 aigc/harness/tools/wiki/wiki-resolve.py --check

# 增量漂移检测 + 全量同步（wiki 管理中枢）
python3 aigc/harness/tools/wiki/features/wiki-sync.py
python3 aigc/harness/tools/wiki/features/wiki-sync.py --update

# 重建 wiki-map
python3 aigc/harness/tools/wiki/wiki-resolve.py --build
```

---

## 代码图谱（可选）

tree-sitter AST 自动生成的代码结构索引。用于辅助构建 features/ 和生成可视化。

```bash
pip install -r aigc/harness/tools/wiki/requirements.txt
python3 aigc/harness/tools/wiki/update-graph.py              # 生成图谱
python3 aigc/harness/tools/wiki/update-graph.py --html       # HTML 可视化
python3 aigc/harness/tools/wiki/update-graph.py --query Tank  # 子图查询
```

> AI 读 `GRAPH_REPORT.md`，不要直接读 `graph.json`（10-30MB 会爆 context）。

---

## 构建知识库

详见 [[workflow-knowledge]]。

推荐构建顺序：**system-map → features → 图谱（可选）**

```bash
# system-map.md — AI 全权维护
# wiki-map.json — 重建文档索引
python3 aigc/harness/tools/wiki/wiki-resolve.py --build
# 代码图谱（可选）
python3 aigc/harness/tools/wiki/update-graph.py --stats
```
