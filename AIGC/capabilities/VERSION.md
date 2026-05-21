# AIGC 版本

current_version: 1.0.0

## 版本级别

| 级别 | 触发条件 |
| --- | --- |
| patch | 修正文档、索引、链接、模板、测试、自检提示或规则表述；收紧既有规则但不破坏当前外部契约。 |
| minor | 新增可被角色管理员调用的能力、角色、工具命令、项目接入规则或可选资料入口；现有入口和行为仍兼容。 |
| major | 仅当破坏当前外部契约时使用：改变默认启动入口、主会话可见字段含义、项目事实写入边界、CLI 命令名、必需配置结构，或删除仍被当前能力索引声明的 active 能力。 |

## 版本推进原则

- 当前整体重构后的基线版本为 `1.0.0`。
- 同一轮变更只产生一个系统版本，不因多个文件同步修改而连续叠加版本号。
- 能力条目版本只在该能力自身的可观察行为变化时更新；单纯迁移文件、修链接、补说明不单独提升能力版本。
- 能兼容现有入口的规则补充优先使用 patch。
- 不能因为目录整理、文档收敛或删除废弃记录直接提升 major。

## 当前版本范围

- 角色管理员默认入口。
- 角色库、通用角色最小规则和角色派发规则。
- SubAgent / 全新会话执行隔离规则。
- 角色会话复活最小索引、查找、唤醒和失败处理规则。
- Claude Code 角色会话复活运行时索引字段和会话索引模板。
- 按需验证审查员。
- 项目适配包、项目专属角色和项目知识沉淀规则。
- 通用架构 wiki。
- 能力索引、版本记录和变更记录。
- 结构自检 CLI、wiki 索引校验和自检命令规划。
- 角色资料、方法卡和自检触发规则。

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 角色管理员调度 | active | `../roles/INDEX.md` | 所有用户请求先由角色管理员接收，角色管理员确认目标、边界和验证方式后，通过 SubAgent 或全新会话派发具体角色。 |
| 角色库 | active | `../roles/INDEX.md` | 维护角色边界、允许读取、允许写入、禁止范围和调用方式。 |
| 通用角色最小规则 | active | `../roles/common/RULE.md` | 所有角色共享的语言、事实、调度、写入、验证和交付规则。 |
| 执行角色通用规则 | active | `../roles/developer/RULE.md` | 具体执行角色默认继承的任务读取、写入和交付边界。 |
| 验证审查员 | active | `../roles/qa-verification/RULE.md` | 由角色管理员按风险派发，负责复现、回归、验收、失败路径、压力路径或高风险集成验证。 |
| wiki 管理员 | active | `../roles/wiki-manager/RULE.md` | 判断候选知识写入通用 wiki、项目知识、运行记录或不写入。 |
| Tharness 能力维护员 | active | `../roles/tharness-maintainer/RULE.md` | 维护 Tharness 规则、角色库、项目接入机制、能力索引、自检工具和模板。 |
| 项目适配路由 | active | `../roles/role-manager/project-adapter-routing.md` | 目标项目事实、项目专属角色、项目知识和运行记录由本机项目适配包承载。 |
| 会话角色标识 | active | `../roles/common/session-visible-state.md` | 主会话正式输出展示当前角色、职责和依据；用户可见当前角色固定为角色管理员。 |
| 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 角色管理员继续已派发角色任务时，只按最小索引定位运行时原 `session_id`；Claude Code subagent 必须同时命中原 `agent_id`，不可用时明确说明而不是新建会话冒充。 |
| 问题路由 | active | `../roles/role-manager/issue-routing.md` | 执行角色发现问题后形成候选，由角色管理员审核沉淀位置。 |
| 游戏策划方法卡 | active | `../roles/role-manager/game-design/INDEX.md` | 角色管理员处理游戏策划讨论时调用的方法论、方法卡和输出模板。 |
| 项目知识维护路由 | active | `../roles/wiki-manager/skills/project-knowledge-routing.md` | wiki 管理员判断项目知识检索、更新、沉淀或健康检查分支。 |
| 通用架构 wiki | active | `../wiki/INDEX.md` | 保存跨项目可复用的项目架构搭建知识，用于低 token 架构检索。 |
| 项目适配包规则 | active | `../roles/role-manager/project-adapter-routing.md` | 定义本机 `AIGC/project-adapters/{project_id}` 适配包结构和读取方式。 |
| 结构自检 | active | `../../tools/tharness.py` | 用 `doctor`、`index --check` 和 `check` 检查入口、元数据、索引、角色库、会话角色标识和结构边界。 |
| 自检命令规划 | active | `../../tools/tharness.py` | 用 `self-check --path ... --delivery` 输出本轮应运行的自检命令。 |

## 当前版本边界

- 默认入口是角色管理员。
- 主会话用户可见 `【当前角色】` 只能是 `角色管理员`；执行角色通过 SubAgent 或全新会话派发。
- 角色会话复活只允许恢复运行时原 `session_id`；Claude Code subagent 复活还必须恢复原 `agent_id`；原会话不可唤醒时不得把摘要继承或新建会话称为复活。
- Tharness 不默认保存完整会话、工具调用、推理链路或 transcript 内容；跨机器或审计场景只允许保存可选镜像引用。
- 多步骤执行方式由角色管理员基于角色库、项目接入规则和通用 wiki 组合任务包。
- 验证、审查和交付判断由角色管理员、执行角色或验证审查员承担。
- 可提交的通用 AIGC 只保存通用角色、通用规则、通用 wiki、项目接入机制和模板。
- 具体项目事实、项目知识、项目决策事实、项目专属角色和项目代码结构分析只能写入本机项目适配包。
- 项目专属扩展只保存在本机项目适配包，不保存具体项目代码路径、资源路径或历史决策事实到可提交通用层。
- 自检配置只保存通用检查入口、扫描范围、必需字段、会话角色允许值和结构边界规则，不保存目标项目事实。

## 当前版本验证结果

- 角色库入口可从 `../roles/INDEX.md` 命中。
- 角色管理员规则可从 `../roles/role-manager/RULE.md` 命中。
- 通用角色最小规则可从 `../roles/common/RULE.md` 命中。
- 会话角色标识自检会拒绝把执行角色写成主会话 `【当前角色】`。
- 当前能力可从 `INDEX.md` 路由。
- 通用架构 wiki 可从 `../wiki/INDEX.md` 路由。
- 项目适配路由可从 `../roles/role-manager/project-adapter-routing.md` 命中。
- 角色会话复活规则可从 `../roles/role-manager/session-revival.md` 命中，并由 `check_required_paths` 检查存在。
- 角色会话索引模板可从 `../roles/role-manager/templates/session-index.yaml` 命中。
- 写入边界仍保持：项目事实进入本机项目适配包，通用知识进入通用 wiki。
- `python tools/tharness.py doctor` 可检查入口、wiki 元数据和角色规则数量。
- `python tools/tharness.py index --check` 可检查 `AIGC/wiki/index.yaml` 页面清单一致性。
- `python tools/tharness.py check` 可执行结构自检。
- `python tools/tharness.py self-check --path AIGC/wiki/architecture/role-system.md --delivery` 可输出 `index --check` 和 `check`。
- `python -m unittest tools.test_tharness` 覆盖 CLI 无效输入、索引写回、自检命令规划和会话角色标识检查。
