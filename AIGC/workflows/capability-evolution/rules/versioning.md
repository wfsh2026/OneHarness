---
id: workflow-capability-evolution-versioning
title: 版本规则
workflow: capability-evolution
phase: versioning
read_when: 需要更新 AIGC 能力索引、版本或变更记录。
updated: 2026-04-27
---

# 版本规则

更新 AIGC 能力时，必须同步检查 `AIGC/capabilities/`。

## 版本级别

| 级别 | 触发条件 |
| --- | --- |
| patch | 修正文档、索引、链接、模板，不改变工作流行为。 |
| minor | 新增能力、规则、模板、目录或工作流阶段。 |
| major | 改变默认读取路径、写入边界或工作流选择规则。 |

## 必须记录

- 版本号。
- 修改内容。
- 修改原因。
- 影响范围。
- 验证方式。

## 禁止

- 禁止只改工作流不更新能力索引。
- 禁止只写 changelog 不保证入口可达。
- 禁止因单张通用架构知识页增加而自动提升总版本。
