---
id: architecture-dependency-direction
title: 依赖方向
summary: 通过稳定层依赖变化层、上层依赖抽象来降低耦合。
type: architecture-card
status: active
tags: [architecture, dependency, coupling]
relates: ["[[architecture-module-boundaries]]"]
read_when: 需要判断依赖方向、循环依赖或跨层调用是否合理。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 依赖方向

## 结论

依赖方向要让变化更频繁的部分依赖稳定接口，而不是让稳定核心依赖临时业务细节。

## 最小做法

- 先列出模块稳定性。
- 再列出允许依赖方向。
- 对反向依赖建立接口、事件或适配层。
- 对循环依赖拆出共同抽象或移动职责。

## 验证方式

- 修改一个高变化模块，不需要改动稳定核心。
- 新增功能能通过扩展点接入。
- 依赖关系能画成无环方向图。

## 不适用场景

- 原型验证可以短期放宽，但必须记录为临时方案。
