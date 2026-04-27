# AIGC 版本

current_version: 0.2.0

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

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 低 token 工作流路由 | active | `../workflows/INDEX.md` | 先读索引，再按 `read_when` 读取命中的工作流和规则。 |
| 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 把模糊需求讨论成目标、范围、约束、风险和成功标准明确的策划案。 |
| 开发执行 | active | `../workflows/development/WORKFLOW.md` | 把已确认目标转成最小可验证代码、文档、测试或配置改动。 |
| AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 分析外部 harness 或旧项目，提取可复用能力，并更新能力索引和版本记录。 |
| 通用架构 wiki | active | `../wiki/INDEX.md` | 保存跨项目可复用的项目架构搭建知识，用于低 token 架构检索。 |
| 项目适配层规则 | active | `../projects/INDEX.md` | 定义目标项目自己的 AIGC 适配层创建方式，隔离项目事实。 |

## 当前版本边界

- 当前版本只定义通用工作流、索引、模板、wiki 规则和能力版本。
- 当前版本不保存具体项目运行记录、项目 wiki、项目决策事实或项目代码结构分析。
- 通用架构 wiki 只保存跨项目架构搭建知识，不保存项目专用资料。

## 当前版本验证结果

- 工作流入口可从 `../workflows/INDEX.md` 路由。
- 当前能力可从 `INDEX.md` 路由。
- 通用架构 wiki 可从 `../wiki/INDEX.md` 路由。
- 写入边界仍保持：项目事实进入目标项目适配层，通用知识进入通用 wiki。
