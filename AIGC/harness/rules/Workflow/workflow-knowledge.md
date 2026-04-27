# 工作流：Knowledge 知识库构建 (workflow-knowledge.md)

> 工作流类型：知识库构建
> 适用场景：为游戏项目构建/更新 AI 知识库
> 通用 session 记录规范见：[[session-guide]]
> 知识库架构说明见：[[wiki/README]]
> 工具链位于：`aigc/harness/tools/wiki/`

---

## 一、触发条件与路由

```
用户请求
  │
  ├── "构建知识库" ──────→ wiki-env.json 存在？
  │                         ├── 否 → §二 首次构建
  │                         └── 是 → §三 增量更新
  │
  ├── "更新 wiki/knowledge" → §三 增量更新
  ├── "检查漂移/同步 wiki" → §三 增量更新
  ├── "修复漂移/fix drift"   → §三 增量更新
  │
  └── 单项操作 ──────────→ §四 单项更新
      "更新 system-map" / "重建索引" / "检查覆盖率" 等
```

进入本工作流时**必须建立 session-state**（与 discussion 不同，无论规模大小）：

```bash
mkdir -p aigc/harness/session-state/knowledge构建/
# 同步创建 active.md + session-log.md（缺一不可）
```

---

## 二、首次构建（6 步）

> 前置：wiki-env.json 不存在。按顺序执行，每步有明确产出和等待点。

| 步骤 | 做什么 | 工具/命令 | 产出 | ⏸ 等待 |
|------|--------|----------|------|--------|
| **1. 环境检测** | 确认项目路径、`aigc/wiki/` 目录、工具链 | `ls`、`local-env.json` | — | — |
| **2. system-map** | 扫描目录+docs → 生成初稿 | AI 手动编写 | `aigc/wiki/knowledge/system-map.md` | ⏸ ask_user 审核 |
| **3. wiki-env** | 扫描子仓库 → 生成项目配置 | `wiki-sync.py --init` | `aigc/wiki/wiki-env.json` | — |
| **4. features** | 归属文件+检覆盖率 | `auto-assign.py` → `check-coverage.py` | `features/*.md` | ⏸ 归属建议 ask_user |
| **5. wiki-map** | 扫描所有 .md → 生成文档索引 | `wiki-resolve.py --build` → `--check` | `wiki-map.json` | — |
| **6. glossary** | 从代码枚举自动生成名词表 | `build-glossary.py --write` | `glossary.md` | — |
| **7. 代码图谱**（可选） | AST 分析生成代码结构索引 | `update-graph.py --stats` | `graph.json` | — |

步骤 2 完成后输出构建计划，ask_user 确认范围再继续。

### 强制等待点

- 步骤 2：system-map 初稿 → **ask_user 审核**后定稿
- 步骤 4：auto-assign 建议 → **ask_user 审核**后 `--write`
- 从其他项目拷贝前 → **ask_user 确认**拷贝范围

---

## 三、增量更新（wiki-sync 驱动）

> 前置：wiki-env.json 已存在。用户说"更新 wiki"时走这里。

```
wiki-sync.py
  │
  ├── ✅ 无漂移 → 汇报"知识库已同步" → 完毕
  │
  └── ⚠️ 有漂移 → 输出报告 → ask_user 确认修复范围
         │
         ▼
     §三-A 修复 feature（AI 手动创建/更新 feature.md）
         │
         ▼
     wiki-sync.py --update（一条命令完成以下全部）
         ├── system-map --sync 插骨架行
         ├── wiki-map 重建
         ├── 名词表重建
         ├── wiki-link 断链检查
         └── 更新基准 commit
         │
         ▼
     AI 补充 ⚠️ TODO 描述 + §二 意图关键词
```

### §三-A：修复 feature

| 漂移类型 | 判断 | 处理 |
|---------|------|------|
| **新增 BSO*.cs** | 新 Buff | 用模板创建 `buff-{name}.md`，手动追加到消费者 feature 的「关联 Buff」段落 |
| **新增 Mode/IdCard/Vehicle** | 新功能 | 创建对应 feature.md |
| **新增其他 .cs** | 已有功能扩展 | 追加路径到对应 feature.md 代码表 |
| **已删除仍引用** | 代码已删 | 从 feature.md 移除路径；全删 → ask_user 是否删 feature |

#### 新 Buff 模板

```yaml
---
name: buff-{kebab-name}
display_name: BS{PascalName} - {PascalName}
category: buff/{分类}
version: 1.0.0
dependencies:
  - buff-framework
---
```

> category 从类名前缀推断：`BSGoldDash*` → `buff/golddash`，`BSPve*` → `buff/pve`。
> 四文件路径：`BSO{Name}.cs` + `BS{Name}.cs` + `BS{Name}Client.cs` + `BS{Name}Server.cs`

### §三-B：wiki-sync --update（一条命令完成）

`wiki-sync.py --update` 自动执行以下全部步骤：

1. `check-system-map.py --sync` — 新增插骨架行 / 删除标注 REMOVED
2. `wiki-resolve.py --build` — 重建 wiki-map
3. `wiki-resolve.py --check` — wiki-link 断链检查
4. `build-glossary.py --write` — 重建名词表
5. `build-wiki-html.py` — 重新生成离线 Wiki HTML 检索页面（`wiki-viewer.html`）
6. 更新 wiki-env.json 基准 commit

AI 只需在 --update 完成后补充：
- `⚠️ TODO` 行的描述和 feature wiki-link
- §二 意图关键词表（新功能的关键词映射）

---

## 四、单项更新

| 用户指令 | 执行内容 |
|---------|---------|
| "更新 system-map" | `check-system-map.py --sync`（骨架）→ AI 补充描述 |
| "重建文档索引" | `wiki-resolve.py --build` |
| "检查覆盖率" | `check-coverage.py --summary` |
| "自动归属" | `auto-assign.py`（干跑 → ask_user → `--write`） |
| "更新 wiki-map" | `wiki-resolve.py --build` + `--check` |
| "生成代码图谱" | `update-graph.py --stats` |
| "生成 wiki HTML" | `build-wiki-html.py`（产出 `wiki-viewer.html`） |
| "检查漂移" | `wiki-sync.py` |
| "修复漂移" | `wiki-sync.py` → §三-A → `wiki-sync.py --update` |
| "更新 wiki" | `wiki-sync.py` → §三-A → `wiki-sync.py --update` |
| "初始化 wiki-env" | `wiki-sync.py --init` |

---

## 五、从其他项目拷贝

```
1. local-env.json 定位源/目标项目
2. 列出拷贝内容（system-map + features + wiki-map）→ ask_user 确认
3. 执行拷贝
4. 在目标项目重建索引：wiki-resolve.py --build
5. 输出结果摘要
```

> ⚠️ 拷贝后 system-map 和 features 可能与目标代码不一致，需人工审核。

---

## 六、日志规则

> `aigc/wiki/log.md` 是审计轨迹。工具操作自动写入，手动操作必须手动补写。

**工具自动写入**（无需额外操作）：`wiki-resolve.py`、`auto-assign.py`、`check-coverage.py`、`update-graph.py` 等通过 `wiki_log.py` 模块自动追加。

**手动修改必写**：AI 手动修改 `aigc/wiki/` 下任何文件后执行：

```bash
python3 aigc/harness/tools/wiki/wiki_log.py <type> "<title>" "<details>"
# type: ingest（写入/更新） / lint（检查）
```

---

## 七、产出文件清单

| 文件 | 生成方式 | 同步策略 |
|------|---------|---------|
| `aigc/wiki/knowledge/system-map.md` | `check-system-map.py --sync`（骨架）+ AI 补充 | 项目独立 |
| `aigc/wiki/wiki-env.json` | `wiki-sync.py --init` | 项目独立 |
| `aigc/wiki/raw/features/*.md` | 工具辅助+人工 | 项目独立 |
| `aigc/wiki/knowledge/wiki-map.json` | `wiki-resolve --build` | framework 同步 |
| `aigc/wiki/knowledge/wiki-viewer.html` | `build-wiki-html.py`（wiki-sync --update 自动调用） | 项目独立 |
| `aigc/wiki/knowledge/graph.json` | `update-graph.py` | 项目独立（可选） |

---

## 附录 A：工具速查

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| `auto-assign.py` | 自动归属未编目文件（⚠️ 待适配 .md） | `--write` `--stdin` `--verbose` |
| `check-coverage.py` | 覆盖率检查 | `--summary` `--json` `--suggest` |
| `wiki-sync.py` | **wiki 管理中枢**（纯调度器） | `--init` `--update` `--repo <key>` |
| `feature-check.py` | feature 漂移检测（wiki-sync Step 1） | `--repo <key>` |
| `check-system-map.py` | system-map 同步检查（wiki-sync Step 2） | `--sync` `--verbose` |
| `drift-check.py` | ⚠️ 已废弃，使用 `wiki-sync.py` 替代 | — |
| `build-glossary.py` | 从代码枚举/常量生成 glossary.md | `--init` `--write` |
| `build-wiki-html.py` | 生成 Obsidian 风格离线 Wiki HTML 检索页面 | `--output` `--light` |
| `migrate-json-to-md.py` | feature JSON → MD 格式迁移 | `--write` `--single` |
| `wiki-resolve.py` | wiki-link 解析与文档索引 | `--build` `--resolve` `--check` |
| `update-graph.py` | 代码图谱生成（可选） | `--stats` `--html` `--query` |

> 所有工具位于 `aigc/harness/tools/wiki/` 或其 `features/` 子目录。详细用法见各脚本头部 docstring。
> 工具执行写入操作后自动追加 `aigc/wiki/log.md` 记录（via `wiki_log.py`）。

---

## 附录 B：active.md 模板

```
# 当前会话状态

项目：{项目名} knowledge 构建
工作流类型：knowledge 构建
当前阶段：{进行中 / 构建完成}

主进度：

| 步骤 | 内容 | 状态 |
|------|------|------|
| ① system-map | system-map.md 初稿+审核 | 📋 / 🔄 / ✅ |
| ② wiki-env | wiki-env.json 初始化 | 📋 / 🔄 / ✅ |
| ③ features | 归属+索引+覆盖率 | 📋 / 🔄 / ✅ |
| ④ wiki-map | wiki-map.json 生成 | 📋 / 🔄 / ✅ |
| ⑤ 代码图谱 | graph.json（可选） | 📋 / N/A |

关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|
```

---

## 附录 C：流程声明格式

```
→ 进入 [Knowledge 知识库构建] 工作流
→ session-state：已建立
   路径：aigc/harness/session-state/knowledge构建/
   active.md / session-log.md 已创建
```
