# Session 记录规范 (session-guide.md)

> 适用于所有工作流类型。定义 active.md 通用字段、session-log.md 格式和写入规则。
> 各工作流的专用 active.md 模板见对应 `aigc/harness/rules/Workflow/workflow-*.md`。

---

## 一、active.md 通用字段

所有工作流的 active.md 必须包含以下通用字段，各工作流在此基础上扩展专用字段：

```markdown
# 当前会话状态

## 项目：{项目名或话题名}
## 工作流类型：{业务开发 / framework管理 / 轻量讨论}
## 当前阶段：{状态描述}

## 主进度
（此处由各工作流模板定义结构）

## 开发里程碑
（业务开发工作流专用。由 `session-sync.sh ux --init` 从开发计划自动导入 Phase/UX 表格，含状态列。
 通过 `session-sync.sh ux --id UX-N --status "✅"` 更新单项状态。）

## 关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|

## ⚠️ 遗留待确认
- {待用户确认的内容}
```

---

## 二、session-log.md 格式规范

### 定位
推理/思考记录文件，记录 AI 的决策过程、方案评估、踩坑原因。
不写进度（进度在 active.md），只记录"为什么这么做"。

**核心价值**：session-log 是 AI 的"思考可见化"——你看到的不只是做了什么，而是 AI 怎么想的、考虑了哪些方案、为什么选这个。下次 AI 恢复上下文时，读 session-log 就能重建思路，不用重新推导。

**好的回答要存回来**：凡是 AI 给出了有价值的分析结论（反直觉发现、系统影响链路、方案选型推理），不应只停留在聊天记录里——用 `session-sync.sh log` 把结论存进来。聊天消失了，session-log 留下。

### 文件头
```markdown
# Session Log — {话题名}

> 推理日志：记录关键决策的思考过程，不是进度记录（进度记录在 active.md）

---
```

### 条目格式
```markdown
## [YYYY-MM-DD HH:MM:SS] {问题/场景简述}

**背景**：{问题或需求来源}  
**推理**：{考虑了哪些方案，为什么选/否定某方案}  
**结论**：{最终选择，以及影响}

---
```

> ⚠️ **时间戳获取规则**：写入 session-log 前必须执行 `date "+%Y-%m-%d %H:%M:%S"` 获取本地精确时间，不得手填或估算。

> ⚠️ **推理部分不得简短带过**：推理是 session-log 的核心价值。**所有子命令（含 doc / progress）** 均须满足以下要求：
> - 考虑了哪些备选方案（哪怕只有两个：做 vs 不做）
> - 每个方案的优劣或否定理由
> - 最终选择的具体依据
> - 潜在风险或遗留问题（如有）
>
> **常见反例（禁止）：**
> - ❌ `"需要制作文档记录创建流程"` — 这是在重复事实，不是推理
> - ❌ `"feature已存在只需补制作文档"` — 缺少为什么这样做、有无替代方案
> - ❌ `"21个模式需要统一制作流程指南"` — 描述了需求但没有分析
>
> **正确写法（推理 = 分析 + 取舍）：**
> - ✅ `"备选方案1:直接复用模式制作.md通用模板(优:省时;劣:各模式差异无法体现); 方案2:每个模式独立文档(优:精准定位;劣:维护21份); 选方案2因为开发者需要按模式查阅而非逐行查通用文档; 风险:小文档<10KB质量可能不足"`
>
> 一句话的推理 = 没有推理。工具端 `--reasoning` 最低字数已提升至 80 字（doc/progress）/ 120 字（log）。

### 强制触发条件

| 触发场景 | 说明 | session-sync.sh 命令 |
|---------|------|---------------------|
| 删除/合并文件 | 说明为什么删，是否有替代方案 | `session-sync.sh log --title "..." --background "..." --reasoning "..." --conclusion "..."` |
| 发现规范错误并修正 | 说明原规范错在哪，修正逻辑 | `session-sync.sh log --title "..." --background "..." --reasoning "..." --conclusion "..."` |
| 遇到 Bug 并分析根因 | 帮助复盘 | `session-sync.sh bug --id N ...` |
| 用户纠正了 AI 错误做法 | 记录原来怎么做的，正确做法是什么 | `session-sync.sh log --title "..." --background "..." --reasoning "..." --conclusion "..."` |
| 重要架构取舍 | 记录弃用方案和理由 | `session-sync.sh adr ...` + `session-sync.sh log ...` |
| 用户确认了重要决策 | 记录决策背景和推理过程 | `session-sync.sh adr --id N ...` |
| 阶段/里程碑完成 | 更新阶段行和进度表 | `session-sync.sh stage ...` + `session-sync.sh progress ...` |
| 开发里程碑初始化 | 从开发计划导入 Phase/UX 表格 | `session-sync.sh ux --init` |
| 开发里程碑状态变更 | UX 体验节点通过/进行中/阻塞 | `session-sync.sh ux --id UX-N --status "✅" --reasoning "..."` |
| 流程违规及纠正措施 | 记录违规事件和改进方案 | `session-sync.sh log --title "⚠️ ..." --background "..." --reasoning "..." --conclusion "..."` |

> ⚠️ **所有 active.md / session-log.md 写入必须通过 `session-sync.sh` 工具执行**，禁止手动编辑文件。工具路径：`aigc/harness/tools/session-sync.sh`。

### 规则
- **只追加，不修改已有条目**
- **每条条目之间必须有 `---` 分隔线**
- **新条目追加在文件末尾的 `---` 之后**，不得插入到已有条目中间
- 新建话题时，必须同时创建 `active.md` 和 `session-log.md`
- session-log 与 active.md 永远在同一目录下

---

## 三、触发写入的事件

> 所有写入通过 `session-sync.sh` 执行。时间戳由工具自动获取，无需手动调用 `date` 命令。

| 触发事件 | session-sync.sh 命令 | 说明 |
|---------|---------------------|------|
| 用户决策确认 | `adr --id N --point "..." --decision "..."` | 自动写入 active.md ADR 表 |
| 阶段跃迁 | `stage --text "M-XX 完成"` | 替换 active.md 顶部状态行 |
| 主进度步骤完成 | `progress --num "..." --agent "..." --content "..."` | 追加 active.md 进度表 |
| Bug 修复 | `bug --id N --symptom "..." --cause "..." --fix "..." --reasoning "..."` | 同时写 Bug 表 + session-log |
| 门控通过 | `gate --name "pN ..." --result "✅ 通过"` | 追加 active.md 门控表 |
| 文档/工具产出 | `doc --name "..." --path "..." --status "✅"` | 追加 active.md 文档表 |
| 规范沉淀 | `lesson --id N --text "..."` | 追加 active.md 规范沉淀 |
| 开发里程碑初始化 | `ux --init` | 从开发计划自动导入 Phase/UX 表格到 active.md |
| 里程碑状态更新 | `ux --id UX-N --status "✅" --reasoning "..."` | 原地更新 active.md 里程碑状态列 |
| 重要推理/取舍 | `log --title "..." --background "..." --reasoning "..." --conclusion "..."` | 追加 session-log.md |
| 遗留待确认出现 | （仍需手动编辑 ⚠️ 遗留段） | 每次会话结束前检查是否清空 |
