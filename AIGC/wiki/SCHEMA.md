# Wiki 知识库 — 整理规则 (SCHEMA)

> 本文件是 LLM 维护 wiki/ 知识库的核心配置。每次新会话操作 wiki/ 时，LLM 应首先读取本文件。

---

## 1. 目录结构

```
wiki/
├── SCHEMA.md          # 本文件：wiki 规则与操作规范
├── log.md             # 操作日志：append-only，按时间记录
├── raw/               # 原始资料（只读，LLM 不得修改）
│   └── {项目名}/
│       ├── 内容边界定义/    # 各系统的内容边界文档
│       └── 范例文档/       # 各系统的开发范例
└── knowledge/         # LLM 生成与维护的知识产物
    ├── README.md      # 知识库使用说明
    ├── system-map.md  # 系统导航地图（全局入口）
    ├── wiki-map.json  # wiki-link 名称→路径映射（工具生成）
    ├── feature-format.md # 功能包格式规范
    └── features/      # 功能包（代码→功能映射）
        └── {子目录}/{功能名}.md  # 单个功能包（YAML frontmatter + 代码表）
```

### 分层定位

| 层 | 目录 | 写入者 | 说明 |
|----|------|--------|------|
| 原始层 | `raw/` | 人类 | 项目成品素材，LLM 只读不改 |
| 知识层 | `knowledge/` | LLM + 工具 | 从 raw + 代码中提炼的结构化知识 |

---

## 2. 知识产物类型

### 2.1 系统地图 (system-map.md)

知识库的**全局入口**，记录项目的系统架构、模块边界、依赖关系。

- **生成方式**：人工编写 + AI 辅助
- **更新时机**：新增/重构系统模块时
- **格式规范**：见 `harness/rules/system-map-rules.md`

### 2.2 功能包 (features/*.json)

代码文件到业务功能的映射，AI 通过功能包定位"这个功能涉及哪些文件"。

- **生成方式**：工具辅助 + 人工审核
- **格式规范**：见 `wiki/knowledge/feature-format.md`
- **相关工具**：`auto-assign.py`、`check-coverage.py`

### 2.3 文档索引 (wiki-map.json)

`[[wiki-link]]` 别名到文件路径的映射表，供 `wiki-resolve.py` 解析。

- **生成方式**：`wiki-resolve.py --build` 自动扫描生成
- **更新时机**：文件新增/删除/重命名后重建

---

## 3. 操作工作流

### 3.1 摄入新资料（Ingest）

**触发**：用户将新文件放入 `raw/` 并告知 LLM。

**步骤**：
1. 读取原始资料，与用户讨论关键要点
2. 判断是否需要更新 `system-map.md`（新系统/新模块）
3. 判断是否需要新建/更新功能包（新功能代码）
4. 执行更新
5. `log.md` 自动追加摄入记录

### 3.2 知识库构建（Build）

**触发**：用户发出"构建 knowledge"指令。

**完整流程**：见 `harness/rules/Workflow/workflow-knowledge.md`

构建顺序：system-map → features → wiki-map → 代码图谱（可选）

### 3.3 健康检查（Lint）

**触发**：用户主动要求，或知识库构建完成后。

**检查项**：
- wiki-link 完整性：`wiki-resolve.py --check`
- 功能包覆盖率：`check-coverage.py --summary`
- 知识图谱一致性：`update-graph.py --report-only`（可选）

**执行后 `log.md` 自动追加检查记录。**

---

## 4. 日志规范（log.md）

- `log.md` 只追加，不修改历史记录
- 每条记录以 `## [YYYY-MM-DD] 类型 | 标题` 开头
- 类型：`ingest`（摄入）、`lint`（健康检查）、`query`（仅归档查询）、`schema`（规则变更）
- 最新记录在文件末尾
- **工具自动写入**，由 `harness/tools/wiki/wiki_log.py` 统一处理

---

## 5. 链接规范

- **内部链接**：一律使用 `[[wiki-link]]`，通过 `wiki-resolve.py` 解析
- **避免孤立页面**：新文档创建后，确保被 system-map 或其他文档引用
- **跨目录引用**：wiki/ 内文档可引用 harness/ 下的规范文件

---

## 6. 人机分工

| 工作 | 负责方 |
|------|--------|
| 选择/放入原始资料到 raw/ | 人类 |
| 决定知识库构建范围 | 人类 |
| 编写 system-map 初稿 | LLM（人类审核） |
| 自动归属功能包 | 工具（人类审核） |
| 重建 wiki-map / 索引 | 工具（自动） |
| 维护 log.md | 工具（自动） |
| 审阅知识库内容 | 人类（可选） |
| 更新 SCHEMA | 人机共同演进 |

---

## 7. 演进说明

本 SCHEMA 会随使用经验不断调整。修改 SCHEMA 时：
1. 在 `log.md` 记录变更原因（类型：`schema`）
2. 如有必要，批量更新已有文档的格式
