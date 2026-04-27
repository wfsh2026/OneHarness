---
id: architecture-module-boundaries
title: 模块边界
summary: 用职责、输入输出、所有权和禁止事项定义模块边界。
type: architecture-card
status: active
tags: [architecture, module, ownership]
relates: ["[[architecture-dependency-direction]]"]
read_when: 需要拆分模块、分配文件归属或限制修改范围。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 模块边界

## 结论

模块边界应以职责和依赖关系定义，不能只按文件夹名推断。

## 最小做法

每个模块至少记录：

- 职责。
- 输入。
- 输出。
- 拥有的文件或目录。
- 允许依赖的模块。
- 禁止修改或禁止依赖的范围。

## 验证方式

- 一个变更能明确落到一个主责模块。
- 并行任务有单一文件所有者。
- 跨模块修改能说明原因和接口影响。

## 不适用场景

- 探索阶段尚未形成稳定模块时，只记录候选边界，不写成稳定事实。
