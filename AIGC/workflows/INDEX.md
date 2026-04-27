# 通用工作流索引

默认只读本索引。按用户意图命中一个工作流后，再读取该工作流的 `WORKFLOW.md`。

会话中需要显式标识当前工作流时，读取 `session-visible-state.md`。

| 工作流 | read_when |
| --- | --- |
| `planning-discussion` | 需求仍然模糊，需要讨论方案、策划案、范围、约束或成功标准。 |
| `development` | 需求已经可以执行，需要开发、修复、重构、补文档、验证或推进 MVP 闭环。 |
| `capability-evolution` | 需要分析外部 harness、提取可复用能力、更新 AIGC 能力索引或版本记录。 |

## 选择规则

- 未确认产品边界、技术路线或写入范围时，先进入 `planning-discussion`。
- 已确认目标、边界和验证方式时，进入 `development`。
- 需要吸收外部 harness、旧项目经验或更新 AIGC 能力版本时，进入 `capability-evolution`。
- 开发中出现会影响范围或决策的歧义时，回到 `planning-discussion` 或向用户确认。
- 任何工作流都不能把目标项目事实写入通用 AIGC。
