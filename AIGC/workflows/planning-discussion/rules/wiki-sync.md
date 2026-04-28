---
id: workflow-planning-discussion-wiki-sync
title: Wiki 同步规则
workflow: planning-discussion
phase: wiki-sync
read_when: 需要沉淀通用知识或项目知识。
updated: 2026-04-27
---

# Wiki 同步规则

## 写入通用架构 wiki

满足以下条件时，按 `../../../wiki/rules/building.md` 写入 `AIGC/wiki/architecture/`：

- 与具体项目无关。
- 可被多个项目复用为架构搭建知识。
- 有明确来源。
- 低频变化。
- 能通过 `read_when` 精确检索。

## 写入目标项目 wiki

满足以下任一条件时，写入目标项目 wiki：

- 项目目标。
- 项目约束。
- 项目决策。
- 项目文档结构。
- 后续会重复查询的稳定项目事实。

一次性讨论过程、临时推理、被否决方案和工作流运行事实写入目标项目运行记录，不写入项目 wiki。

## 禁止

- 不允许把项目事实写入通用 wiki。
- 不允许把未确认内容写成稳定架构结论。
