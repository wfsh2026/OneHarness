---
id: workflow-capability-evolution-wiki-sync
title: Wiki 同步规则
workflow: capability-evolution
phase: wiki-sync
read_when: 需要把可复用结论写入通用 wiki。
updated: 2026-04-27
---

# Wiki 同步规则

能力演化产生的通用架构知识，按通用 wiki 规则写入。

## 写入通用架构 wiki

满足以下条件时，按 `../../../wiki/rules/building.md` 写入 `AIGC/wiki/architecture/`：

- 与具体项目无关。
- 能被多个项目复用为架构搭建知识。
- 有明确来源。
- 低频变化。
- 能通过 `read_when` 精确检索。

## 写入规则或能力索引

- wiki 检索、写入、健康检查规则写入 `AIGC/wiki/rules/`。
- 能力入口、状态、版本写入 `AIGC/capabilities/`。
- 目标项目事实、运行记录、项目 wiki 写入目标项目适配层。

## 禁止

- 不允许把外部 harness 的项目事实写入通用 wiki。
- 不允许把未验证结论写成稳定架构知识。
- 不允许在索引里复制正文。
