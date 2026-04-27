# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`0.2.0`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `planning-discussion` | 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 0.1.0 | 需求模糊，需要讨论方案、范围、约束或成功标准。 |
| `development` | 开发执行 | active | `../workflows/development/WORKFLOW.md` | 0.1.0 | 目标明确，需要开发、修复、补文档、补测试或推进 MVP 闭环。 |
| `capability-evolution` | AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 0.1.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 0.2.0 | 需要检索跨项目通用架构搭建知识。 |

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
