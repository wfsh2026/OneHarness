---
id: workflow-development-wiki-sync
title: 开发 Wiki 同步规则
workflow: development
phase: wiki-sync
read_when: 需要沉淀开发知识、项目事实或运行记录。
updated: 2026-04-27
---

# 开发 Wiki 同步规则

## 写入通用架构 wiki

满足以下全部条件时，按 `../../../wiki/rules/building.md` 写入 `AIGC/wiki/architecture/`：

- 与具体项目无关。
- 可被多个项目复用为架构搭建知识。
- 有明确来源。
- 已在开发或验证中产生稳定结论。
- 低频变化。
- 能通过 `read_when` 精确检索。

## 写入目标项目 wiki

满足以下任一条件时，写入目标项目 wiki：

- 项目架构约束。
- 项目模块边界。
- 项目路径、配置或构建规则。
- 已确认技术决策。
- 后续开发会重复查询的稳定经验。

目标项目 wiki 不存在时，先执行 `../../../projects/rules/project-wiki-bootstrap.md`。目标项目 wiki 已存在时，按 `../../../projects/rules/project-wiki-update.md` 更新。

## 写入运行记录

以下内容写入本次工作流运行记录：

- 本轮输入摘要。
- 实施过程摘要。
- 验证命令和结果。
- 临时失败尝试。
- 关键决策。
- 被否决方案。
- 经验教训。
- 未完成事项。

## 知识碎片提取

开发交付物包含以下内容时，优先按知识碎片提取：

| 内容 | 写入位置 |
| --- | --- |
| 可跨项目复用的架构结论 | `AIGC/wiki/architecture/` |
| 通用 wiki 检索、写入、健康检查规则 | `AIGC/wiki/rules/` |
| 目标项目技术决策 | 目标项目 wiki |
| 目标项目踩坑经验 | 目标项目 wiki 或运行记录 |
| 一次性调试过程 | 运行记录 |

通用架构页模板见 `../../../wiki/templates/architecture-card.md`。

## 禁止

- 不允许把项目事实写入通用 wiki。
- 不允许把一次性调试过程写入 wiki。
- 不允许把未确认内容写成稳定架构结论。

通用 wiki 创建规则见 `../../../wiki/rules/building.md`。项目事实边界见 `../../../projects/PROJECT_ADAPTER.md`。项目 wiki 检索规则见 `../../../projects/rules/project-wiki-retrieval.md`。Wiki 健康检查规则见 `../../../wiki/rules/health.md` 和 `../../../projects/rules/project-wiki-health.md`。
