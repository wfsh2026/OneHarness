---
id: architecture-workflow-routing
title: 工作流路由
summary: 用意图索引和 read_when 把任务路由到一个最小工作流。
type: architecture-card
status: active
tags: [architecture, workflow, routing]
relates: ["[[architecture-entry-map]]", "[[architecture-verifiable-work-loop]]"]
read_when: 需要为任务选择工作流、阶段、规则索引和后续读取路径。
source: OneHarness 当前通用工作流结构。
updated: 2026-04-27
---

# 工作流路由

## 结论

通用项目架构应提供一个工作流路由层，用用户意图命中单一工作流，再由该工作流继续命中阶段、规则和模板。

## 适用场景

- 项目同时支持讨论、开发、验证、演进等多种任务。
- AI 容易为了保险读取过多规则。
- 同一请求可能被误判为多个执行路径。

## 最小做法

工作流路由层至少包含：

- 工作流 ID。
- 触发条件。
- 默认读取路径。
- 阶段列表。
- 完成标准。
- 写入边界。

## 验证方式

- 一个用户请求只能命中一个主工作流。
- 工作流入口能继续路由到规则索引。
- 出现关键歧义时能回到澄清，而不是继续猜测。

## 不适用场景

- 单一用途脚本或没有长期协作需求的临时任务。
