# AIGC 版本

current_version: 0.6.2

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

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 低 token 工作流路由 | active | `../workflows/INDEX.md` | 先读索引，再按 `read_when` 读取命中的工作流和规则。 |
| 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 把模糊需求讨论成目标、范围、约束、风险和成功标准明确的策划案。 |
| 开发执行 | active | `../workflows/development/WORKFLOW.md` | 把已确认目标转成最小可验证代码、文档、测试或配置改动。 |
| 质量门控 | active | `../workflows/development/rules/quality-gate.md` | 交付前检查目标、范围、验证、边界和结果一致性。 |
| 问题路由 | active | `../workflows/development/rules/issue-routing.md` | 判断问题和经验应写入运行记录、项目 wiki、通用 wiki 还是能力索引。 |
| 项目 Wiki 维护 | active | `../workflows/project-wiki-maintenance/WORKFLOW.md` | 为目标项目搭建、检索、更新或检查项目 wiki。 |
| AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 分析外部 harness 或旧项目，提取可复用能力，并更新能力索引和版本记录。 |
| 通用架构 wiki | active | `../wiki/INDEX.md` | 保存跨项目可复用的项目架构搭建知识，用于低 token 架构检索。 |
| 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 把大内容拆成默认速查入口和按需详解，降低重复读取成本。 |
| 项目适配层规则 | active | `../projects/INDEX.md` | 定义目标项目自己的 AIGC 适配层创建方式，隔离项目事实。 |
| 项目 wiki 主动搭建 | active | `../projects/rules/project-wiki-bootstrap.md` | 检索已有工程并在目标项目适配层建立项目 wiki。 |
| 项目 wiki 更新 | active | `../projects/rules/project-wiki-update.md` | 在开发后更新目标项目 wiki，并保持项目事实可检索。 |
| OneHarness 自检 | active | `../../tools/oneharness.py` | 用 `doctor`、`index --check` 和 `gate` 检查入口、元数据、索引和门控。 |
| 自检触发规则 | active | `../workflows/development/rules/self-check.md` | 按 OneHarness 自身改动范围自动选择并运行自检命令。 |
| Wiki 索引同步 | active | `../../tools/oneharness.py` | 用 `index --write` 按扫描结果写回 wiki 页面清单。 |
| 自检命令规划 | active | `../../tools/oneharness.py` | 用 `self-check --path ... --delivery` 输出本轮应运行的自检命令。 |

## 当前版本边界

- 当前版本定义通用工作流、索引、模板、wiki 规则、能力版本和最小自检工具。
- 当前版本不保存具体项目运行记录、项目 wiki、项目决策事实或项目代码结构分析。
- 通用架构 wiki 只保存跨项目架构搭建知识，不保存项目专用资料。
- 项目 wiki 只保存到目标项目适配层，不保存到通用 `AIGC/wiki`。
- 自检配置只保存通用检查入口、扫描范围、必需字段和门控规则，不保存目标项目事实。

## 当前版本验证结果

- 工作流入口可从 `../workflows/INDEX.md` 路由。
- 当前能力可从 `INDEX.md` 路由。
- 通用架构 wiki 可从 `../wiki/INDEX.md` 路由。
- 项目 wiki 主动搭建和更新规则可从 `../projects/INDEX.md` 路由。
- 项目 wiki 维护工作流可从 `../workflows/INDEX.md` 路由。
- 质量门控和问题路由规则可从 `../workflows/development/rules/INDEX.md` 路由。
- 知识分层架构页可从 `../wiki/architecture/INDEX.md` 路由。
- 写入边界仍保持：项目事实进入目标项目适配层，通用知识进入通用 wiki。
- `python tools/oneharness.py doctor` 可检查入口、wiki 元数据和工作流规则元数据。
- `python tools/oneharness.py index --check` 可检查 `AIGC/wiki/index.yaml` 页面清单一致性。
- `python tools/oneharness.py gate` 可执行交付前的最小结构门控。
- `../workflows/development/rules/self-check.md` 可从开发规则索引命中。
- 开发交付模板包含自检结果记录区域。
- `python tools/oneharness.py index --write` 可写回 wiki 页面清单并保持 `index --check` 通过。
- `python tools/oneharness.py self-check --path AIGC/wiki/architecture/entry-map.md --delivery` 可输出 `index --check` 和 `gate`。
- `python -m unittest tools.test_oneharness` 覆盖 CLI 无效输入、索引写回和自检命令规划。
