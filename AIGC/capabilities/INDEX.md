# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`1.0.0`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `role-dispatch` | 角色管理员调度 | active | `../roles/INDEX.md` | 1.0.0 | 所有用户请求先由角色管理员接收，角色管理员确认目标、边界和验证方式后，通过 SubAgent 或全新会话派发具体角色。 |
| `role-library` | 角色库 | active | `../roles/INDEX.md` | 1.0.0 | 维护角色边界、允许读取、允许写入、禁止范围、调用方式和角色资料。 |
| `project-adapter-routing` | 项目适配路由 | active | `../roles/role-manager/project-adapter-routing.md` | 1.0.0 | 需要接入、切换或读取目标项目事实、项目专属角色、项目知识或运行记录。 |
| `session-role-marker` | 会话角色标识 | active | `../roles/common/session-visible-state.md` | 1.0.0 | 主会话正式输出展示当前角色、主要职责和工作依据；用户可见当前角色固定为角色管理员，被派发角色只能出现在派发、依据、回收或内部记录中。 |
| `role-session-revival` | 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 1.0.0 | 需要继续、唤醒、恢复或追溯已派发角色任务；Tharness 只保存最小会话索引，复活必须恢复运行时原 `session_id`；Claude Code subagent 还必须恢复原 `agent_id`。 |
| `issue-routing` | 问题路由 | active | `../roles/role-manager/issue-routing.md` | 1.0.0 | 执行角色发现问题后形成候选，由角色管理员审核沉淀位置。 |
| `project-knowledge-maintenance` | 项目知识维护 | active | `../roles/wiki-manager/skills/project-knowledge-routing.md` | 1.0.0 | 需要检索、更新或检查目标项目适配包中的项目知识、决策、来源或开放问题。 |
| `capability-evolution` | AIGC 能力演化 | active | `../roles/tharness-maintainer/RULE.md` | 1.0.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 1.0.0 | 需要检索跨项目通用架构搭建知识。 |
| `knowledge-layering` | 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 1.0.0 | 需要拆分过大的规则、知识页、说明文档或能力入口。 |
| `tharness-self-check` | Tharness 结构自检 | active | `../../tools/tharness.py` | 1.0.0 | 需要检查入口、元数据、wiki 索引、角色库、会话角色标识或结构边界是否存在问题。 |
| `role-self-check-trigger` | 自检触发规则 | active | `../roles/tharness-maintainer/skills/self-check.md` | 1.0.0 | Tharness 自身改动影响 AIGC 文档、角色规则、配置、工具或准备交付时。 |
| `index-sync` | Wiki 索引同步 | active | `../../tools/tharness.py` | 1.0.0 | 需要按扫描结果校验或写回 `AIGC/wiki/index.yaml` 页面清单。 |
| `self-check-planner` | 自检命令规划 | active | `../../tools/tharness.py` | 1.0.0 | 需要按变更路径确定本轮应该运行哪些自检命令。 |
| `game-design-method-cards` | 游戏策划方法卡 | active | `../roles/role-manager/game-design/method-cards/INDEX.md` | 1.0.0 | 需要把游戏设定、玩法想法或体验目标转成可开发、可反馈、可验证的策划结构。 |

## 状态说明

| 状态 | 含义 |
| --- | --- |
| `active` | 当前可直接按角色规则或工具入口使用。 |
| `candidate` | 候选能力，只能作为参考或待导入结构，不能当强规则执行。 |

## 维护规则

- 新增或删除能力时，必须更新本索引。
- 改变能力行为时，必须更新 `VERSION.md` 和 `CHANGELOG.md`。
- 候选能力不能当强规则执行。
- 能力入口必须能通过索引链路访问。
