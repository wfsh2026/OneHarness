---
id: workflow-project-wiki-maintenance-routing
title: 项目 Wiki 维护路由规则
workflow: project-wiki-maintenance
phase: routing
read_when: 需要判断本轮是搭建、创建结构、检索、更新还是健康检查项目 wiki。
updated: 2026-04-27
---

# 项目 Wiki 维护路由规则

## 结论

项目 wiki 维护每轮只选择一个主要分支，避免同时扫描工程、更新页面和做全量健康检查。

## 路由

| 用户意图或状态 | 读取规则 |
| --- | --- |
| 项目 wiki 不存在，需要主动搭建 | `../../../projects/rules/project-wiki-bootstrap.md` |
| 需要创建完整项目 wiki 结构 | `../../../projects/rules/project-wiki-creation.md` |
| 只需要查找项目事实 | `../../../projects/rules/project-wiki-retrieval.md` |
| 开发后需要更新稳定项目事实 | `../../../projects/rules/project-wiki-update.md` |
| 需要检查入口、来源、断链或事实边界 | `../../../projects/rules/project-wiki-health.md` |

## 最小读取

1. 先读取目标项目 `{project_aigc_root}/ADAPTER.md`。
2. 项目 wiki 存在时读取 `{project_wiki_root}/INDEX.md`。
3. 项目 wiki 不存在时，只读取项目入口文件、构建配置和主要源码目录一层结构。
4. 命中页面不足时，再读取项目源码或文档入口补证据。

## 禁止

- 禁止把项目事实写入通用 `AIGC/wiki`。
- 禁止为了检查项目 wiki 读取整个目标项目。
- 禁止把一次性运行过程写入项目 wiki。
