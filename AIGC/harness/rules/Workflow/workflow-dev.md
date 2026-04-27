# 工作流：业务功能开发 (workflow-dev.md)

> 工作流类型：业务开发
> 本文件定义人与 AI 在游戏功能开发中的分工和完整流程。
> Agent 角色速查见 `AGENTS.md §4.2`，规则文件索引见 [[INDEX]]。
> 通用 session 记录规范见：[[session-guide]]

---

## 一、完整开发流程图

> 门控脚本生成 checklist 时以此表为模板，追加「完成情况」「完成 Agent」「sh 验收」三列。
> 脚本路径：`aigc/harness/tools/Workflow/workflow-dev/gate-check.sh`
> 用法：`./gate-check.sh init {功能名}` 初始化 checklist；`./gate-check.sh p2|p4|p8 {功能名}` 门控检查

> ---
> 🚨 **强制执行规则（不可跳过）**
> 1. **工作流启动时**：[项目负责人] 必须立即运行 `bash aigc/harness/tools/Workflow/workflow-dev/gate-check.sh init {功能名}` 生成 checklist，**不得在 init 之前调度任何 Agent**
> 2. **阶段推进时**：[项目负责人] 使用 `session-sync.sh stage --phase N --text "..."` 推进阶段，脚本内置门控继承链自动拦截：
>    - `--phase 2/4/8`：自动运行 `gate-check.sh pN`，**exit 1 则拒绝推进**
>    - `--phase 3`：继承检查 active.md 中 p2 的 PASS 记录
>    - `--phase 5~7`：继承检查 p4 的 PASS 记录
>    - `--phase 9+`：继承检查 p8 的 PASS 记录
>    - 不传 `--phase`：纯文字更新，不触发门控（适用于非 workflow-dev 流程）
> 3. 门控通过后 `session-sync.sh` 自动在 active.md 门控表追加 PASS 记录，无需手动操作
> ---

| 阶段 | 用户行动 | Agent 行动 |
|-----|---------|----------|
| **1. 提交原始需求** | 提交功能描述 / 体验目标 / 策划案路径 | — |
| **2. 需求深度分析** | — | [项目负责人] 初始化 active.md + session-log.md（⚠️ 同步创建，缺一不可） |
| ↑ | — | [GD] 评估核心循环、提炼模糊点、给出体验优化建议 |
| ↑ | — | [DL] 查 system-map.md、确认系统归属、评估技术方案 |
| ↑ | — | [项目负责人] 核查 GD+DL 产出均到齐（见 §四 自检清单） |
| ↑ | — | 输出「需求拆解执行计划草稿」（GD+DL 联合，缺一不行） |
| ↑ | 等待呈现 | ⛔ 2.5 文档门控 Round 1（`./gate-check.sh p2 {功能名}`） |
| **3. 用户决策拍板** | 确认体验目标 / 参数 / 技术方向 | — |
| ↑ | — | [项目负责人] 记录用户决策到 active.md（ADR 格式） |
| **4. 文档化与开发计划** | — | ⚠️ [项目负责人] 派发前必须先读 [[background-agent]] §二 |
| ↑ | — | [GD] 生成「完整策划案.md」（路径：`docs/GamePlay_Dev/{功能名}/策划案.md`） |
| ↑ | — | [DL] 规划文件清单 + 美术灰盒方案，必读：plan-doc.md + technical-doc-format.md |
| ↑ | — | ⚠️ **S-05 文件清单来源约束**：各 Agent 填写 S-05 前，**必须先填写 S-04.7 Codegen 工具预读清单**（读取对应 codegen 工具头部的 `OUTPUT FILES` 注释块，路径：`aigc/harness/tools/codegen/{工具名}.sh`），S-05 中的新建/修改文件必须与工具声明一致，禁止 AI 自行猜测文件结构（格式见 `technical-doc-format.md §一.2`） |
| ↑ | — | [DL] 输出「{功能名}开发计划.md」（路径：`docs/GamePlay_Dev/{功能名}/`，含 M-01/M-02/M-03） |
| ↑ | — | [DL] 创建 技术文档/ 目录 + README.md + 各子文档空框架 |
| ↑ | — | [GPO 工程师] 完整填充 GPO 子文档（含 S-01~S-09 九大要素）⚠️ 必读 `gpo-code.md §强制工具规则` |
| ↑ | — | [Ability 工程师] 完整填充 Ability 子文档（如有）⚠️ 必读 `ability-code.md §强制工具规则` |
| ↑ | — | [场景] 完整填充场景子文档（如有）⚠️ 必读 `scene-code.md §三 AI强制工具规则` |
| ↑ | — | [DL] 审核所有子文档：必须含灰盒方案（形状/颜色/尺寸）+ 核心循环链路 + 交互链路图，无 TODO 空框架。⚠️ **内容合规检查**：每文档 csharp 代码块 ≤5 个，S-04.7 Codegen 工具预读清单已填写且全部 ✅，S-05 文件清单必须与 codegen 工具 `OUTPUT FILES` 声明一致，禁止 AI 猜测 |
| ↑ | — | ⚠️ [DL] 审核通过后，在开发计划文档追加「Codegen 指令清单」：列出所有需要执行的 codegen 工具命令（从各子文档 S-05 推导），用户阶段5审图通过后阶段6直接执行 |
| ↑ | 等待呈现 | ⛔ 4.5 文档门控 Round 0+2（`./gate-check.sh p4 {功能名}`，⚡ exit 0 才可呈现） |
| ↑ | — | ⚠️ [项目负责人] 门控通过后执行 `session-sync.sh ux --init` 导入 M-02 里程碑到 active.md |
| **5. 用户审图确认** | ① 确认开发阶段×体验节点流程图（AI/用户阶段是否清晰） | — |
| ↑ | ② 确认文件清单完整性 | — |
| ↑ | ③ 确认技术方案方向 | — |
| ↑ | ④ 确认美术资产灰盒方案（形状/颜色/尺寸） | — |
| ↑ | ⑤ 确认 UI 资产灰盒方案 | — |
| ↑ | ⑥ 确认 Codegen 指令清单（工具命令是否完整、参数是否正确） | — |
| ↑ | ⑦ 确认 S-04.7 Codegen 工具预读清单（所有工具参数+OUTPUT FILES 已读 ✅） | — |
| **6. 逐模块开发** | — | [DL] 按开发计划「Codegen 指令清单」依次执行所有 codegen 工具生成骨架 → 确认编译通过（0 errors） |
| ↑ | — | ⚠️ **强制工具规则**：GPO/Component/Ability/Mode/Scene 代码**必须通过对应 codegen 工具生成骨架**，禁止手动创建代码文件（详见 `background-agent.md §四`） |
| ↑ | — | [DL] 按模块填充业务逻辑（多 Agent 时先派发「子任务分发说明」见 §三.1）：|
| ↑ | — | · [GPO 工程师] 填充 AI 业务逻辑（含预留桩） |
| ↑ | — | · [Ability 工程师] 填充业务逻辑，完成后提供接口信息 |
| ↑ | — | · [场景] MCP `execute_menu_item` 生成服务端场景（待 GPO Sign 填入） |
| ↑ | — | · [DL] 填充模式逻辑 |
| ↑ | — | [DL] 接口对齐 → 填预留桩 → 串联模式系统 → 确认编译通过 |
| ↑ | — | [DL] 遇不确定项 → ask_user 暂停等待 |
| **7. 用户响应追问** | 响应追问（数值确认等） | — |
| **8. 功能自检与验收** | — | 功能自检（编译 + 逻辑对照验收清单） |
| ↑ | — | [DL] 输出「Phase N 技术验收报告.md」（实现摘要 + 执行计划映射表 + 核心链路自检） |
| ↑ | 等待呈现 | ⛔ 8.5 文档门控 Round 3（`./gate-check.sh p8 {功能名}`，打回→DL 修复→重提交，3次仍失败才上报） |
| **9. 汇报开发完成** | 实机验证（Unity Editor 运行） | [DL] 列出新增/修改文件 + 需用户手动确认事项 |
| ↑ | — | [项目负责人] 更新 active.md 本阶段完成状态 |
| **10-11. Bug 修复**（循环） | 报告 Bug | [DL] 定位 Root Cause → 修改文件 → 通知重测 |
| ↑ | — | [项目负责人] 记录 Bug 现象/根因/修复到 active.md |
| ↑ | _重复阶段 6-11 直至验收通过_ | |
| **12. 验收通过 ✅** | 填回最终数值到策划案 | [DL] 更新「XXX-完整技术文档.md」+ 规范反哺（更新 rules/ 和 system-map.md） |
| ↑ | — | [项目负责人] 更新 active.md 为"Phase N ✅ 验收完成"，记录规范沉淀 |

---

## 二、强制等待原则

**所有需要用户决策的阶段，AI 输出完毕后必须通过 `ask_user` 等待用户回复，不得自行推进。**

| 阶段 | 强制等待 | 禁止行为 |
|------|---------|---------|
| 阶段2 输出后 | ask_user 询问体验目标和技术方案 | 不得自行开始阶段4 |
| 阶段4 输出后 | ask_user 展示五项审阅清单 | 不得自行进入阶段6开发 |
| 阶段6 遇不确定项 | ask_user 暂停等待 | 不得猜测并继续 |

---

## 三、多 Agent 协作规范

### 3.1 任务分发说明格式（DL 输出）

```
【子任务分发说明】
功能名称：XXX

子任务1 - GPO 工程师：
  负责：[具体 GPO 类型]
  ⚠️ 工具调用（强制）：
    1. `bash aigc/harness/tools/codegen/gpom-gen.sh --name GPOM_{Name} ...` 生成模板数据
    2. `bash aigc/harness/tools/codegen/gpo-gen.sh --name {Name} --gpom-name GPOM_{Name} ...` 生成 System + 注册（默认 Graybox 占位体）
    3. `bash aigc/harness/tools/codegen/component-gen.sh --name {Name}XXX --side server --type ai --template {模板} ...` 生成 AI Component（按需选择模板：findtarget/lifetime/move/rotate/scale）
  接口约定：
    - GPO Sign：XXX
    - 需要 Ability 工程师提供：[AB Sign 和 InData 参数]
  预留桩位置：ServerAIXXX.FireBullet() → 等 Ability 确认后填充
  验收标准：[≥3条可测试的行为描述]

子任务2 - Ability 工程师：
  负责：[具体 AB/AE 类型]
  ⚠️ 工具调用（强制）：
    `bash aigc/harness/tools/codegen/ability-gen.sh --name {Name} --type AB ...` 生成全套文件
  接口约定：完成后提供调用示例（AB Sign + InData 字段），供 GPO 工程师填桩
  验收标准：[≥3条可测试的行为描述]

子任务3 - 场景：
  负责：[客户端场景 + 服务端场景]
  ⚠️ 工具调用（强制，两步不可跳过）：
    1. `bash aigc/harness/tools/codegen/scene-gen.sh --name {Name} --display-name "..." --sign {Sign} ...`
    2. MCP `execute_menu_item "Tools/功能/场景/AI场景转换"`（服务端场景强制生成）
  接口约定：需要 GPO 工程师提供 SceneGPO Sign
  验收标准：[≥3条可测试的行为描述]

并行关系：GPO + Ability 可并行；场景可并行搭骨架，待 Sign 填入
```

### 3.2 预留桩规范

```csharp
// ✅ 正确：预留桩，注释说明需要什么
private void FireBullet(Vector3 firePoint, Vector3 targetPoint) {
    // TODO: [等 Ability 工程师确认] 填入 AB Sign + InData
    // MsgRegister.Dispatcher(new SM_Ability.PlayAbility { ... });
}

// ❌ 错误：自行假设参数
MData = AbilityM_Bullet.CreateForSign("DefaultBullet"), // 可能不对
```

### 3.3 active.md 更新示例（DL 向 [项目负责人] 汇报，由 [项目负责人] 通过 session-sync.sh 写入）

SESSION_SYNC 协议见 `AGENTS.md §一.3`。以下是多 Agent 场景下 DL 汇报内容的示例，[项目负责人] 据此执行对应的 `session-sync.sh` 命令：

```bash
# 示例：GPO 子任务完成
session-sync.sh progress --num "⑤" --agent "GPO" --content "GPO 开发完成，预留桩待 Ability 填充"

# 示例：场景子任务完成
session-sync.sh progress --num "⑥" --agent "场景" --content "SceneGPO 完成，Sign 待 GPO 提供"

# 示例：记录接口依赖推理
session-sync.sh log --title "接口依赖" --background "GPO FireBullet 方法需调用 Ability" --reasoning "GPO 和 Ability 并行开发，接口参数未确定" --conclusion "预留桩位，等 Ability 工程师提供 AB Sign + InData 后填充"
```

---

## 四、阶段2强制自检清单

阶段2输出前，必须确认 GD 和 DL 两部分都已完成：

| 产出方 | 必须包含 |
|--------|---------|
| **[GD]** | ① 核心体验评估 ② 模糊点清单（A/B/C/D 分类） ③ 体验优化建议（含数值提案） |
| **[DL]** | ① 系统归属评估表 ② 多方案对比（供用户阶段3选择） ③ 技术可行性评估（含风险点） ④ 新发现歧义点 |

任一方缺失 → 阶段2不完整，禁止进入阶段3。

---

## 五、规范反哺规则

功能验收后，若发现新坑点，必须沉淀进对应文档（不写进文档的经验，下次仍会犯）：

| 问题类型 | 沉淀目标 |
|---------|---------|
| 编码方式 / 组件 / API | `aigc/harness/rules/GamePlay_Dev/` 对应规则文件 + [[lessons-learned]] |
| 系统归属识别 / 意图识别 | [[knowledge/system-map]] |
| 协作流程 / 文档要求 | 本文件 |
| 策划案写法缺失 | [[设计文档完整性思维框架]] |
| 历史复盘记录 | [[lessons-learned]] |

---

## 六、active.md 模板

```markdown
# 当前会话状态

## 项目：{功能名}
## 工作流类型：业务开发
## 当前阶段：{阶段描述}

## 主进度：体验节点验收清单

### 【体验节点 N】{节点目标描述}
| 步骤 | 内容 | 状态 |
|------|------|------|
| ① [{角色}] | {工作内容简述} | ✅ / ⏳ / 📋 |

> 细节文件清单见开发计划文档，此处只追踪体验节点级进展。

## 关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|

## Bug 记录
| # | 现象 | 根因 | 修复 | 状态 |
|---|------|------|------|------|

## 规范沉淀
- rules/xxx.md §N：{条目说明}

## ⚠️ 遗留待确认
- {待用户确认的内容}
```
