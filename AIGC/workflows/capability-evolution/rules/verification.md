---
id: workflow-capability-evolution-verification
title: 验证规则
workflow: capability-evolution
phase: verification
read_when: 需要判断本轮能力演化是否完成。
updated: 2026-04-27
---

# 验证规则

能力演化完成前必须验证：

- 本轮只处理一个能力演化目标。
- 来源、读取边界和不读取内容明确。
- 新增或修改的入口能从索引到达。
- 判断标准已包含是否补全现有能力、是否降低 token、是否支持一次只做一件事。
- 项目事实没有写入通用 AIGC。
- 未验证知识没有写成稳定架构知识。
- 版本或变更记录已说明影响范围和验证方式。
