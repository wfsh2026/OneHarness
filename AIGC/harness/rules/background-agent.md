# Background Agent 规范 (background-agent.md)

> 本文件定义所有 background agent 的启动、记录与执行规范。
> 适用角色：[项目负责人]（派发者）、[DL]（可派发编码类 background agent）。

---

## 一、启动前：active.md 登记（强制）

**启动 background agent 前**，[项目负责人] 必须在当前功能 `active.md` 中登记：

| agent_id | 任务描述 | 预期产出文件 | 启动时间 | 状态 |
|----------|---------|-------------|---------|------|
| xxx      | ...     | ...         | 2026-XX | 🔄 运行中 |

- **禁止在未登记的情况下启动 background agent**
- **禁止 background agent 完成后不更新 active.md 就继续下一步**
- **禁止在 background agent prompt 中不包含「身份文件读取指令」的情况下启动任何角色类 agent**

---

## 二、Prompt 标准模板（必须遵守）

所有 background agent prompt 必须包含以下步骤：

> **步骤0（强制）**：读取 `aigc/harness/agents/{角色路径}.md`（定位文件），在文档/输出开头显性声明「已熟读」。
>
> **步骤1（按任务类型附加）**：
>
> - **文档生成类** → 还必须读 [[technical-doc-format]] + `plan-doc.md`
>   ⚠️ 若文档内容涉及特定系统（GPO/AI/Ability/UGC/场景/Mode 等），还必须读对应领域规则文件（速查表见 `AGENTS.md §五`）
>
> - **编码类** → 还必须读 `aigc/harness/rules/GamePlay_Dev/{对应规则}.md`（如 `gpo-code.md`、`mode-code.md`）
>   ⚠️ 执行任何代码修改前，必须在输出中包含【Pre-Flight 规范读取声明】（格式见 `AGENTS.md §五`）
>   ⚠️ **强制工具规则**：必须读本文件 §四，所有 GPO/Component/Ability/Mode/Scene 文件必须通过 codegen 工具生成，禁止手动创建。开发过程中需要新增计划外的 Component 时，也必须先用 `component-gen.sh` 生成骨架再填充逻辑
>
> - **分析类** → 按需读取与分析目标相关的文档，不强制指定
>
> **步骤2**：基于以上文件的约束执行任务，文档结构/代码风格必须符合规范要求。
>
> **步骤3（文档生成类专用，禁止跳过）**：输出文档正文前，必须先输出以下自检清单，全部确认 ✅ 后才能开始写文档：
>
> 【文档格式自检 - 必须先于文档内容输出】
> ① 已读规范文件声明（表格格式，含三类条目）：✅ 已准备 / ❌ 未准备
> ② 涉及文件清单（分层表格，每条目含操作类型 **新建**/**修改**）：✅ 已准备 / ❌ 未准备
> ③ S-05 文件清单已基于 codegen 工具 `OUTPUT FILES` 声明编写（路径：`aigc/harness/tools/codegen/*.sh` 头部注释）：✅ 已对照 / ❌ 未对照
> ④ 验收标准（覆盖编译/功能/集成三层）：✅ 已准备 / ❌ 未准备
>
> ⚠️ **代码块限制**：文档中 csharp 代码块**总数不得超过 5 个**（仅允许 S-04.5 中关键数据结构片段或 S-06 链路伪代码）。禁止编写完整 C# 类/方法实现——完整代码由阶段6 codegen 工具生成。
>
> 存在任意 ❌ → 禁止继续输出文档，必须先补齐对应内容再重新自检。

---

## 三、完成后

- background agent 产出文件末尾必须包含 `[SESSION_SYNC]` 命令块
- [项目负责人] 读取后更新 active.md 登记状态为 ✅ 完成
- 如需继续派发下一个 background agent，重复步骤一

---

## 四、强制工具规则（编码类 agent 必读）

> **所有 GPO / Component / Ability / Mode / Scene 代码文件必须通过对应 codegen 工具生成骨架，禁止手动创建代码文件。**

| 代码类型 | 必须使用的 codegen 工具 | 工具路径 |
|---------|----------------------|---------|
| GPOM（数据模板） | `gpom-gen.sh` | `aigc/harness/tools/codegen/gpom-gen.sh` |
| GPO（Server/Client AI System） | `gpo-gen.sh` | `aigc/harness/tools/codegen/gpo-gen.sh` |
| AI / Ability / Mode 组件 | `component-gen.sh` | `aigc/harness/tools/codegen/component-gen.sh` |
| Ability（AB/AE 全套） | `ability-gen.sh` | `aigc/harness/tools/codegen/ability-gen.sh` |
| Mode（模式注册 + Server/Client） | `mode-gen.sh` | `aigc/harness/tools/codegen/mode-gen.sh` |
| Scene（场景注册 + Config） | `scene-gen.sh` | `aigc/harness/tools/codegen/scene-gen.sh` |

### 违规判定

- ❌ 手动创建上表覆盖范围内的 `.cs` 文件 → 违规，必须删除后用工具重新生成
- ❌ 跳过 codegen 工具直接写完整实现 → 违规
- ✅ codegen 生成骨架后，在骨架内填充业务逻辑 → 合规
- ✅ codegen 工具不覆盖的辅助文件（如 Util、Config 解析等）→ 可手动创建
