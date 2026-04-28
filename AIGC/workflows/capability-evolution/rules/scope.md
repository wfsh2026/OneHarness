---
id: workflow-capability-evolution-scope
title: 范围规则
workflow: capability-evolution
phase: scope
read_when: 判断是否应进入能力演化工作流，以及本轮边界。
updated: 2026-04-27
---

# 范围规则

## 本工作流负责

- 分析外部 harness 或旧项目中的 AIGC 能力。
- 对比当前 AIGC 已有能力和缺口。
- 提取可复用规则、模板、目录结构、验证方式或经验。
- 更新当前 AIGC 能力索引和版本记录。
- 规划通用架构 wiki 写入。

## 本工作流不负责

- 直接开发业务功能。
- 整体搬运外部 harness。
- 保存外部项目事实到通用 AIGC。
- 自动把未验证结论写成稳定架构知识。
- 同时演化多个无关能力。

## 单目标约束

每轮只能选择一个能力演化目标。

如果外部 harness 中出现多个可提取能力，必须先列出候选，再选择一个继续。
