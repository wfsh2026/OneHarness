---
id: wiki-health
title: Wiki 健康检查规则
summary: 检查入口可达、元数据完整、边界干净和读取成本。
type: rule
status: active
tags: [wiki, health, boundary]
relates: ["[[wiki-building]]"]
read_when: 需要检查 wiki 更新是否破坏低 token 和通用边界。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# Wiki 健康检查规则

## 最小检查

- 入口可达：新增页面能从 `INDEX.md` 或分区索引命中。
- 元数据完整：页面包含 `id`、`title`、`summary`、`type`、`status`、`tags`、`relates`、`read_when`、`source`、`updated`。
- 边界干净：不包含具体项目事实、项目路径、运行记录、项目专用资料。
- 读取成本可控：索引只做路由，不复制正文。
- 关联有效：`relates` 指向存在的 `id`。

## 项目标记扫描

通用 wiki 中不应出现具体项目标记。发现后必须移出通用 wiki 或改写为通用架构表达。

## 禁止

- 禁止用健康检查顺手重写无关页面。
- 禁止为了检查读取全部仓库历史。
- 禁止把项目资料迁回通用 wiki。
