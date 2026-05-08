# AIGC

## 核心思想

本目录是一套低 token、目标驱动的 AI 工作流规则。

它只做一件事：把一次用户请求推进成一个可验证的最小结果。

默认不追求一次读完整资料，也不追求一次解决所有问题。每轮只读取必要索引，只选择一个工作流，只完成一个明确目标，然后验证、记录、停止或进入下一轮。

## 最小工作循环

```text
读入口 -> 选工作流 -> 明确一个目标 -> 执行最小改动 -> 验证 -> 记录结果
```

每一轮都必须回答：

- 这次只做哪一件事？
- 成功标准是什么？
- 需要读哪些最少文件？
- 需要修改哪些最少内容？
- 如何验证它已经完成？
- 结果应该写入通用 AIGC，还是目标项目适配层？

## 默认读取路径

AI 进入本目录时，优先按以下顺序读取：

1. `AIGC/INDEX.md`
2. `AIGC/workflows/INDEX.md`
3. 命中工作流的 `WORKFLOW.md`
4. 命中工作流的 `rules/INDEX.md`
5. `AIGC/wiki/INDEX.md`
6. 按 `read_when` 命中的规则继续读取
7. 需要目标项目事实时，读取 `AIGC/projects/INDEX.md` 和目标项目 wiki 入口

禁止为了保险一次性读取全部 wiki 或全部历史记录。

## 工作流选择

| 场景 | 工作流 |
| --- | --- |
| 需求模糊，需要澄清目标、范围、非目标、约束或成功标准 | `planning-discussion` |
| 目标明确，需要开发、修复、补文档、补测试或推进 MVP 闭环 | `development` |
| 用户提供 UI 截图、效果图或素材图，需要转成 Unity UGUI 策划、资源验收、Prefab 施工或截图校准交付物 | `unity-ugui-ui-workflow` |
| 需要为目标项目搭建、检索、更新或检查项目 wiki | `project-wiki-maintenance` |
| 需要分析外部 harness、提取可复用能力或更新 AIGC 能力版本 | `capability-evolution` |

如果开发过程中出现关键歧义，必须暂停执行，回到澄清或让用户确认。

## 目录职责

| 目录 | 职责 |
| --- | --- |
| `workflows/` | 保存通用工作流、阶段、Agent 职责、规则和模板。 |
| `wiki/` | 保存可复用、可检索、低频变化的通用知识。 |
| `projects/` | 保存目标项目适配层的创建规则和模板。 |
| `capabilities/` | 保存当前 AIGC 能力索引、版本和变更记录。 |

## 写入边界

通用 `AIGC` 可以保存：

- 通用工作流。
- 通用规则。
- 通用 Agent 职责。
- 通用 wiki 创建规则。
- 项目适配模板。

通用 `AIGC` 禁止保存：

- 具体项目运行记录。
- 具体项目 wiki。
- 具体项目决策事实。
- 具体项目代码结构分析。

这些内容必须写入目标项目自己的 AIGC 适配层。

## 设计原则

- 少读：先读索引，再按 `read_when` 读取正文。
- 少做：每轮只完成一个明确目标。
- 不猜：存在关键歧义时先确认。
- 最小改动：只修改完成目标必须修改的内容。
- 必验证：没有验证就不能标记完成。
- 可追溯：规则、决策、运行记录和 wiki 都要能追溯来源。
- 分层沉淀：通用知识进通用 wiki，项目事实进项目 wiki。
- 碎片化：经验教训、被否决方案和稳定事实可以拆成单条知识碎片。
- 闭环化：交互式任务必须说明输入、状态变化、反馈、目标和重复路径。
- 假设晋升：未验证想法先作为假设，验证或确认后才能写成稳定事实。
- 反熵增：wiki 更新后做最小健康检查，避免断链、孤岛、缺来源和过时内容。

## 使用方式

如果只是阅读规则，从 `AIGC/INDEX.md` 开始。

如果要讨论方案，进入 `workflows/planning-discussion/`。

如果要执行开发，进入 `workflows/development/`。

如果要把 UI 图转成 Unity UGUI 施工交付物，进入 `workflows/unity-ugui-ui-workflow/`。

如果要为目标项目创建 AIGC 工作区，读取 `projects/PROJECT_ADAPTER.md`。

如果要为目标项目搭建、检索、更新或检查项目 wiki，进入 `workflows/project-wiki-maintenance/`。

如果要沉淀通用架构知识，先读取 `wiki/INDEX.md`、`wiki/SCHEMA.md` 和 `wiki/rules/building.md`。

如果要检查 wiki 质量，读取 `wiki/rules/health.md`。

如果要分析外部 harness 或更新 AIGC 能力版本，进入 `workflows/capability-evolution/`。

如果要执行框架自检，使用仓库根目录下的最小 CLI：

```powershell
python tools/oneharness.py doctor
python tools/oneharness.py index --check
python tools/oneharness.py index --write
python tools/oneharness.py self-check --path AIGC/wiki/architecture/entry-map.md --delivery
python tools/oneharness.py gate
```

修改 OneHarness 自身时，开发工作流按 `workflows/development/rules/self-check.md` 自动触发对应自检；`self-check` 命令可按变更路径输出应运行的自检命令。

## 成功标准

这套 AIGC 规则生效时，应满足：

- AI 不需要读取全部上下文也能开始工作。
- 每轮任务都有明确目标和验证方式。
- 项目事实不会污染通用规则。
- 稳定知识能被后续快速检索。
- 一次循环结束后，可以安全进入下一次最小循环。
