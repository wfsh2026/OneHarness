# AIGC 版本

current_version: 0.1.1

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
- 通用 wiki 与策划能力库候选结构。

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 低 token 工作流路由 | active | `../workflows/INDEX.md` | 先读索引，再按 `read_when` 读取命中的工作流和规则。 |
| 策划案讨论 | active | `../workflows/planning-discussion/WORKFLOW.md` | 把模糊需求讨论成目标、范围、约束、风险和成功标准明确的策划案。 |
| 开发执行 | active | `../workflows/development/WORKFLOW.md` | 把已确认目标转成最小可验证代码、文档、测试或配置改动。 |
| AIGC 能力演化 | active | `../workflows/capability-evolution/WORKFLOW.md` | 分析外部 harness 或旧项目，提取可复用能力，并更新能力索引和版本记录。 |
| 通用 wiki | active | `../wiki/INDEX.md` | 保存可复用、可检索、低频变化的通用知识，不保存具体项目事实。 |
| 项目适配层规则 | active | `../projects/INDEX.md` | 定义目标项目自己的 AIGC 适配层创建方式，隔离项目事实。 |
| 策划能力库 | candidate | `../wiki/common/candidates/planning-capabilities/INDEX.md` | 按策划提问、体验转译、系统机制、战斗手感、用户理解、原型验证 6 个模块组织候选策划知识。 |

## 当前版本边界

- 当前版本只定义通用工作流、索引、模板、wiki 规则和能力版本。
- 当前版本不保存具体项目运行记录、项目 wiki、项目决策事实或项目代码结构分析。
- 策划能力库已有目录和来源占位，但书籍内容尚未导入，不能作为强规则输出。
- accepted 通用知识当前为空，候选知识必须经过验证后才能晋升。

## 当前版本验证结果

- 工作流入口可从 `../workflows/INDEX.md` 路由。
- 当前能力可从 `INDEX.md` 路由。
- 策划能力库可从通用 wiki 候选索引路由。
- 写入边界仍保持：项目事实进入目标项目适配层，通用知识进入通用 wiki。
