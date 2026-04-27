---
id: architecture-project-adapter-layer
title: 项目适配层
summary: 用目标项目自己的适配目录保存项目事实和运行记录。
type: architecture-card
status: active
tags: [architecture, adapter, isolation]
relates: ["[[architecture-knowledge-boundary]]", "[[architecture-repository-structure]]"]
read_when: 需要隔离通用框架与目标项目事实、运行记录和项目 wiki。
source: OneHarness 当前项目适配规则。
updated: 2026-04-27
---

# 项目适配层

## 结论

通用框架只提供规则、模板和路由；目标项目事实必须保存在目标项目自己的适配层。

## 适用场景

- 同一套通用工作流要服务多个项目。
- 项目需要保存运行记录、决策、开放问题和项目 wiki。
- 通用框架曾经被项目事实污染。

## 最小做法

适配层至少确认：

- 项目名称。
- 项目根目录。
- 项目 AIGC 根目录。
- 当前激活工作流。
- 项目 wiki 根目录。
- 工作流运行记录根目录。

## 验证方式

- 项目事实不写入通用框架。
- 运行记录不写入通用 wiki。
- 通用规则中不硬编码目标项目路径。

## 不适用场景

- 只有一个短期项目且不需要复用通用规则时。
