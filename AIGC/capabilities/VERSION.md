# AIGC 版本

current_version: 3.0.1

## 版本级别

| 级别 | 触发条件 |
| --- | --- |
| patch | 修正文档、索引、链接、模板，不改变工作流行为。 |
| minor | 新增能力、规则、模板、目录或工作流阶段。 |
| major | 改变默认读取路径、写入边界或工作流选择规则。 |

## 当前版本范围

- 通用工作流索引。
- 策划案讨论工作流。
- 开发执行工作流。
- AIGC 能力演化工作流。
- 通用架构 wiki。
- 项目 wiki 主动搭建和更新能力。
- 项目 wiki 维护工作流。
- 质量门控、问题路由和知识分层能力。
- 最小自检 CLI、wiki 索引校验和文档门控检查。
- 开发工作流内的自检触发规则。
- 一致性工具层、索引写回和自检命令规划。
- 游戏策划方法卡体系和触发索引。
- 主程调度式开发执行工作流。
- 游戏模块开发角色路由。
- 子任务全新会话执行规则。
- 子任务 Agent 默认读取压缩规则。
- 项目专属扩展开发计划入口。
- 会话角色标识规则。
- Wiki 候选知识审核和沉淀边界。
- 策划到开发通过目标项目 wiki 衔接。
- 项目 wiki `design/` 和 `development/` 分区。
- Unity UGUI UI 图转施工工作流和复杂 UI 上下文隔离策略。

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 低 token 工作流路由 | active | `../workflows/INDEX.md` | 先读索引，再按 `read_when` 读取命中的工作流和规则。 |
| 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 把模糊需求讨论成目标、范围、约束、风险和成功标准明确的项目 wiki 策划页面；游戏策划问题会进一步转成玩家幻想、核心体验、机制、反馈和验证原型。 |
| 开发执行 | active | `../workflows/development/WORKFLOW.md` | 由主程把项目 wiki 中已确认的策划页面拆成项目 wiki 开发任务页，按游戏模块角色分配给全新会话执行，并集成验收；项目专属入口由本机项目胶囊声明。 |
| Unity UGUI UI 图转施工 | active | `../workflows/unity-ugui-ui-workflow/WORKFLOW.md` | 把 UI 截图、效果图或素材图按快速路径、资源核查路径或独立施工路径转成 UI 规划、资源验收、UGUI Prefab 施工、Controller 事件接口和截图校准反馈；复杂 UI 命中上下文隔离规则时文件化长产物；会话首次正式输出和正式结论按会话角色标识规则展示。 |
| 游戏开发角色路由 | active | `../workflows/development/rules/game-role-routing.md` | 按 UI、3C、场景、战斗、AI、玩法系统、工具、技术美术和 QA 验证分配子任务；子任务默认只读公共开发规则和当前角色路由行。 |
| 项目扩展开发入口 | active | `../projects/PROJECT_ADAPTER.md` | 项目专属开发入口、规则和角色由本机项目胶囊声明，不写入可提交通用层。 |
| 会话角色标识 | active | `../workflows/session-visible-state.md` | 会话首次正式输出、角色切换、最终结论、阶段性结论、交付汇总和正式评审结论展示当前角色、主要职责和工作依据；角色名只能来自角色选择表、项目胶囊扩展角色或统一兜底模板。 |
| 质量门控 | active | `../workflows/development/rules/quality-gate.md` | 交付前检查目标、范围、项目 wiki 任务页、验证、边界和结果一致性。 |
| 问题路由 | active | `../workflows/development/rules/issue-routing.md` | 将开发中发现的问题先形成候选，再由主程审核写入运行记录、项目 wiki、通用 wiki 或能力索引。 |
| 项目 Wiki 维护 | active | `../workflows/project-wiki-maintenance/WORKFLOW.md` | 为目标项目搭建、检索、更新或检查项目 wiki，包括策划页面、开发任务页、子任务和接口契约入口。 |
| AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 分析外部 harness 或旧项目，提取可复用能力，并更新能力索引和版本记录。 |
| 通用架构 wiki | active | `../wiki/INDEX.md` | 保存跨项目可复用的项目架构搭建知识，用于低 token 架构检索。 |
| 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 把大内容拆成默认速查入口和按需详解，降低重复读取成本。 |
| 项目胶囊规则 | active | `../projects/INDEX.md` | 定义本机项目 registry 和项目胶囊创建方式，隔离可提交通用层与项目事实。 |
| 项目 wiki 主动搭建 | active | `../projects/rules/project-wiki-bootstrap.md` | 检索已有工程并在本机项目胶囊中建立包含 `design/` 和 `development/` 分区的项目 wiki。 |
| 项目 wiki 更新 | active | `../projects/rules/project-wiki-update.md` | 在策划或开发后更新目标项目 wiki，并保持项目事实可检索。 |
| Tharness 自检 | active | `../../tools/tharness.py` | 用 `doctor`、`index --check` 和 `gate` 检查入口、元数据、索引和门控。 |
| 自检触发规则 | active | `../workflows/development/rules/self-check.md` | 按 Tharness 自身改动范围自动选择并运行自检命令。 |
| Wiki 索引同步 | active | `../../tools/tharness.py` | 用 `index --write` 按扫描结果写回 wiki 页面清单。 |
| 自检命令规划 | active | `../../tools/tharness.py` | 用 `self-check --path ... --delivery` 输出本轮应运行的自检命令。 |
| 游戏策划方法卡 | active | `../workflows/planning-discussion/method-cards/INDEX.md` | 按来源、阶段和触发词组织原则卡、提问卡、转译卡和检查卡。 |

## 当前版本边界

- 当前版本定义通用工作流、索引、模板、wiki 规则、能力版本和最小自检工具。
- 当前版本不保存具体项目运行记录、项目 wiki、项目决策事实或项目代码结构分析。
- 通用架构 wiki 只保存跨项目架构搭建知识，不保存项目专用资料。
- 项目 wiki 只保存到本机项目胶囊，不保存到通用 `AIGC/wiki`。
- 项目策划事实写入目标项目 wiki 的 `design/` 分区。
- 主程任务拆解、子任务分配和接口契约写入目标项目 wiki 的 `development/` 分区。
- Unity UGUI UI 工作流只保存跨项目可复用的瘦身执行路径、已切资源验收规则、施工约束、上下文隔离策略和报告模板；具体界面事实、素材路径、项目 UI 规范和运行记录仍写入本机项目胶囊。
- 工作流运行过程、失败尝试、命令输出和候选知识审核过程写入运行记录或交付物，不写入项目 wiki 正文。
- 自检配置只保存通用检查入口、扫描范围、必需字段和门控规则，不保存目标项目事实。
- 游戏策划方法卡只保存方法论结构和来源锚点，不保存书籍原文或具体项目玩法事实。
- 游戏开发角色只保存通用职责、路由和读取边界；项目内路径、资源、接口和模块事实写入目标项目 wiki。
- 子任务默认不读取每个角色目录下的短定义文件；角色专属文件只在子任务页明确要求或存在额外强规则时读取。
- 项目专属扩展只保存在本机项目胶囊，不保存具体项目代码路径、资源路径或历史决策事实到可提交通用层。
- 会话角色标识描述首次正式输出、角色切换和正式结论的输出格式；普通过程消息、工具进度或临时同步可沿用最近角色标识；输出主题、文档类型、评审对象或任务标题不能作为当前角色名。
- 子任务开发者只提交候选知识点，不直接写入正式 wiki；是否沉淀由主程审核并调用 wiki 规则判断。

## 当前版本验证结果

- 工作流入口可从 `../workflows/INDEX.md` 路由。
- 当前能力可从 `INDEX.md` 路由。
- 通用架构 wiki 可从 `../wiki/INDEX.md` 路由。
- 项目 wiki 主动搭建和更新规则可从 `../projects/INDEX.md` 路由。
- 项目 wiki 维护工作流可从 `../workflows/INDEX.md` 路由。
- 质量门控和问题路由规则可从 `../workflows/development/rules/INDEX.md` 路由。
- 知识分层架构页可从 `../wiki/architecture/INDEX.md` 路由。
- 写入边界仍保持：项目事实进入本机项目胶囊，通用知识进入通用 wiki。
- `python tools/tharness.py doctor` 可检查入口、wiki 元数据和工作流规则元数据。
- `python tools/tharness.py index --check` 可检查 `AIGC/wiki/index.yaml` 页面清单一致性。
- `python tools/tharness.py gate` 可执行交付前的最小结构门控。
- `../workflows/development/rules/self-check.md` 可从开发规则索引命中。
- 开发交付模板包含自检结果记录区域。
- `python tools/tharness.py index --write` 可写回 wiki 页面清单并保持 `index --check` 通过。
- `python tools/tharness.py self-check --path AIGC/wiki/architecture/entry-map.md --delivery` 可输出 `index --check` 和 `gate`。
- `python -m unittest tools.test_tharness` 覆盖 CLI 无效输入、索引写回和自检命令规划。
- 游戏策划方法卡可从 `../workflows/planning-discussion/method-cards/INDEX.md` 路由，并由 `game-design-methodology.md` 调用。
- 开发执行工作流可从 `../workflows/development/WORKFLOW.md` 路由到主程任务拆解、游戏角色分配、子任务全新会话和知识候选审核。
- 游戏开发角色路由规则可从 `../workflows/development/rules/INDEX.md` 命中。
- 子任务 Agent 默认读取压缩规则可从 `../workflows/development/rules/game-role-routing.md` 和 `../workflows/development/rules/implementation.md` 命中。
- 项目专属扩展入口可从项目胶囊命中，并由 `../workflows/development/rules/game-role-routing.md` 回落到通用角色拆分。
- 会话角色标识规则可从 `../workflows/session-visible-state.md` 命中，并由开发工作流和 UGUI 工作流在会话首次正式输出、角色切换和正式结论阶段调用。
- 会话角色名约束可从 `../workflows/session-visible-state.md` 命中：未命中明确专业角色的 Tharness 架构说明、规则检查、偏差追查、方案评审和能力总结必须使用 `Tharness 通用工作流协调员`。
- 子任务分配模板和 Wiki 候选审核模板可从 `../workflows/development/templates/INDEX.md` 命中。
- 策划工作流可从 `../workflows/planning-discussion/WORKFLOW.md` 路由到项目 wiki 策划页面输出。
- 开发任务拆解规则可从 `../workflows/development/rules/INDEX.md` 命中，并写入项目 wiki `development/` 分区。
- 项目 wiki `design/` 和 `development/` 分区可从项目 wiki 入口模板和项目 wiki 检索规则命中。
- Unity UGUI UI 工作流可从 `../workflows/INDEX.md` 路由到 `../workflows/unity-ugui-ui-workflow/WORKFLOW.md`，并按输入完整度、UI 规划、资源验收与拼装、Unity 施工、截图校准和上下文隔离规则继续读取。
