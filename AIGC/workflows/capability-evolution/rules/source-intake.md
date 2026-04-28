---
id: workflow-capability-evolution-source-intake
title: 来源登记规则
workflow: capability-evolution
phase: source-intake
read_when: 需要登记外部 harness、旧项目、文档或工具来源。
updated: 2026-04-27
---

# 来源登记规则

分析外部来源前，必须登记：

- 来源名称。
- 来源位置。
- 分析目标。
- 本轮读取边界。
- 不读取内容。
- 预期可提取能力。

## 读取边界

- 优先读取入口文件、索引、README、规则目录和模板目录。
- 不为了保险读取完整工程。
- 不读取与本轮能力目标无关的业务代码。
- 如果来源结构不清楚，先输出需要确认的问题。
