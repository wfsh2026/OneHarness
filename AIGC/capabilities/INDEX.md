# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`2.2.0`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `planning-discussion` | 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 1.0.0 | 需求模糊，需要讨论方案、游戏玩法、范围、约束或成功标准，并把确认后的项目策划事实写入目标项目 wiki。 |
| `development` | 开发执行 | active | `../workflows/development/WORKFLOW.md` | 2.0.0 | 目标明确，需要主程按项目 wiki 策划页面拆解项目 wiki 开发任务页，并分配子任务给全新会话执行。 |
| `unity-ugui-ui-workflow` | Unity UGUI UI 图转施工工作流 | active | `../workflows/unity-ugui-ui-workflow/WORKFLOW.md` | 1.1.0 | 用户提供 UI 截图、效果图或素材图，需要按快速路径、资源核查路径或独立施工路径输出 UI 规划、资源验收、UGUI Prefab 施工、Controller 事件接口和截图校准反馈。 |
| `game-development-role-routing` | 游戏开发角色路由 | active | `../workflows/development/rules/game-role-routing.md` | 2.0.0 | 需要按 UI、3C、场景、战斗、AI、玩法系统、工具、技术美术或 QA 验证分配开发子任务，并限制角色读取项目 wiki 子任务页允许的入口。 |
| `quality-gate` | 质量门控 | active | `../workflows/development/rules/quality-gate.md` | 2.0.0 | 交付前需要检查目标、范围、项目 wiki 任务页、子任务会话隔离、验证、边界和结果一致性。 |
| `issue-routing` | 问题路由 | active | `../workflows/development/rules/issue-routing.md` | 1.0.0 | 开发中发现问题，需要形成候选并由主程审核沉淀位置。 |
| `project-wiki-maintenance` | 项目 Wiki 维护 | active | `../workflows/project-wiki-maintenance/WORKFLOW.md` | 0.5.0 | 需要为目标项目搭建、检索、更新或检查项目 wiki，包括策划页面、开发任务页、子任务和接口契约入口。 |
| `capability-evolution` | AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 0.1.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 0.2.0 | 需要检索跨项目通用架构搭建知识。 |
| `knowledge-layering` | 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 0.5.0 | 需要拆分过大的规则、知识页、说明文档或能力入口。 |
| `project-wiki-bootstrap` | 项目 Wiki 主动搭建 | active | `../projects/rules/project-wiki-bootstrap.md` | 0.4.0 | 需要检索已有工程并主动搭建包含 `design/` 和 `development/` 分区的目标项目 wiki。 |
| `project-wiki-update` | 项目 Wiki 更新 | active | `../projects/rules/project-wiki-update.md` | 0.4.0 | 需要在策划或开发后更新目标项目 wiki。 |
| `oneharness-self-check` | OneHarness 自检 | active | `../../tools/oneharness.py` | 0.6.0 | 需要检查入口、元数据、wiki 索引或交付门控是否存在结构问题。 |
| `workflow-self-check-trigger` | 自检触发规则 | active | `../workflows/development/rules/self-check.md` | 0.6.1 | OneHarness 自身改动影响 AIGC 文档、规则、配置、工具或准备交付时。 |
| `index-sync` | Wiki 索引同步 | active | `../../tools/oneharness.py` | 0.6.2 | 需要按扫描结果校验或写回 `AIGC/wiki/index.yaml` 页面清单。 |
| `self-check-planner` | 自检命令规划 | active | `../../tools/oneharness.py` | 0.6.2 | 需要按变更路径确定本轮应该运行哪些自检命令。 |
| `game-design-method-cards` | 游戏策划方法卡 | active | `../workflows/planning-discussion/method-cards/INDEX.md` | 0.1.0 | 需要把游戏设定、玩法想法或体验目标转成可开发、可反馈、可验证的策划结构。 |

## 状态说明

| 状态 | 含义 |
| --- | --- |
| `active` | 当前可直接按工作流规则使用。 |
| `candidate` | 候选能力，只能作为参考或待导入结构，不能当强规则执行。 |

## 维护规则

- 新增或删除能力时，必须更新本索引。
- 改变能力行为时，必须更新 `VERSION.md` 和 `CHANGELOG.md`。
- 候选能力不能当强规则执行。
- 能力入口必须能通过索引链路访问。
