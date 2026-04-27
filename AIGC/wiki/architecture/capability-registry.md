---
id: architecture-capability-registry
title: 能力注册表
summary: 用能力索引记录入口、状态、版本和读取条件。
type: architecture-card
status: active
tags: [architecture, capability, versioning]
relates: ["[[architecture-workflow-routing]]"]
read_when: 需要设计能力入口、状态、版本和可检索维护规则。
source: OneHarness 当前能力索引结构。
updated: 2026-04-27
---

# 能力注册表

## 结论

当项目的通用能力会持续演进时，应使用能力注册表统一记录入口、状态、版本和读取条件。

## 适用场景

- 项目有多个可复用工作流、规则或工具能力。
- 能力需要区分可直接执行和候选状态。
- 能力变更需要追溯版本影响。

## 最小做法

能力注册表至少记录：

- 能力 ID。
- 名称。
- 状态。
- 入口文件。
- 版本。
- `read_when`。

## 验证方式

- 每个能力入口都能从注册表访问。
- 删除或移动能力时同步更新注册表。
- 改变能力行为时同步更新版本记录。

## 不适用场景

- 项目只有单一固定流程，且不会沉淀可复用能力。
