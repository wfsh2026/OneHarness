---
id: architecture-knowledge-boundary
title: 知识写入边界
summary: 用适用范围决定知识进入通用 wiki 还是项目适配层。
type: architecture-card
status: active
tags: [architecture, knowledge, boundary]
relates: ["[[architecture-project-adapter-layer]]", "[[architecture-capability-registry]]"]
read_when: 需要判断一条知识应该写入通用 wiki 还是项目适配层。
source: OneHarness 当前写入边界规则。
updated: 2026-04-27
---

# 知识写入边界

## 结论

知识写入位置由适用范围决定：跨项目可复用的架构知识进通用 wiki，项目事实进项目适配层。

## 适用场景

- 开发完成后需要沉淀经验。
- 讨论中产生了可复用规则或项目决策。
- 需要避免通用框架混入项目资料。

## 最小做法

写入前先判断：

- 是否依赖具体项目路径。
- 是否只对一个项目成立。
- 是否已经验证。
- 是否低频变化。
- 是否能帮助后续检索。

## 验证方式

- 通用 wiki 页面不包含项目路径、项目运行记录或项目决策。
- 项目 wiki 能保存该项目的稳定事实和决策。
- 未确认内容不会写成稳定事实。

## 不适用场景

- 临时推理过程和一次性调试细节，只应保留在运行记录中。
