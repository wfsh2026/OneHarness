# 开发执行工作流规则索引

默认只读本索引。按命中条件读取具体规则。

| 文件 | read_when |
| --- | --- |
| `scope.md` | 判断是否应进入开发执行，以及开发工作流边界。 |
| `intake.md` | 开发前需要确认目标、边界、禁止事项和验证方式。 |
| `task-breakdown.md` | 需要把目标拆成可执行开发任务。 |
| `implementation.md` | 需要执行代码、文档、测试或配置修改。 |
| `verification.md` | 需要验证新增、修复、重构或文档改动。 |
| `self-check.md` | 本轮修改影响 AIGC 文档、工作流规则、自检工具、配置或准备交付时。 |
| `quality-gate.md` | 交付前需要检查目标、范围、验证、边界和结果一致性。 |
| `delivery.md` | 需要输出开发交付物或收尾记录。 |
| `issue-routing.md` | 开发中发现问题，需要判断写入运行记录、项目 wiki、通用 wiki 还是能力索引。 |
| `wiki-sync.md` | 需要沉淀开发知识、项目事实或运行记录。 |
| `lifecycle.md` | 需要处理长任务、上下文移交、阻塞或重建。 |
| `mvp-closure.md` | 用户要求持续推进到可试用 MVP。 |
