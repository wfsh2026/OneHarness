# 开发执行 Agent 索引

默认不读取所有 agent。按当前阶段选择一个或多个 agent。

| Agent | read_when |
| --- | --- |
| `coordinator` | 需要接收用户目标、确认开发是否可执行、同步阻塞或交付。 |
| `lead-developer` | 需要评估开发输入、拆分任务、定义成功标准和验证方式。 |
| `developer` | 需要实施明确的代码、文档、测试或配置改动。 |
| `wiki-curator` | 需要判断开发结果是否沉淀到通用 wiki 或目标项目 wiki。 |

## 执行说明

Agent 表示职责阶段，不强制要求运行环境启动 SubAgent。只有用户或运行环境明确允许时，才使用独立 SubAgent；否则由当前执行者按阶段串行履行职责，并保留同样的输出边界。
