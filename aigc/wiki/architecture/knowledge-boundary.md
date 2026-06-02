---
id: architecture-knowledge-boundary
title: 通用知识边界原则
summary: 解释通用层和项目层的知识边界；具体写入位置由 issue-routing 决定。
type: architecture-card
status: active
tags: [architecture, knowledge, boundary]
relates: ["[[architecture-capability-registry]]"]
read_when: 需要解释通用层和项目层边界，或检查候选内容是否会污染通用层。
source: Tharness 当前知识边界和写入位置路由规则。
updated: 2026-05-26
---

# 通用知识边界原则

## 结论

通用层只保存跨项目可复用、低频变化、能帮助后续检索的稳定知识。具体写入位置只由 `AIGC/roles/role-manager/issue-routing.md` 决定；本页只解释边界原则。

## 适用场景

- 开发完成后需要沉淀经验。
- 讨论中产生了可复用规则或项目决策。
- 需要避免通用框架混入项目资料。
- 需要解释为什么某些内容不能进入 THarness 通用层。

## 最小做法

判断边界时先确认：

- 是否依赖具体项目路径。
- 是否只对一个项目成立。
- 是否已经验证。
- 是否低频变化。
- 是否能帮助后续检索。

## 验证方式

- 通用层页面不包含项目路径、项目运行记录或项目决策。
- 项目事实不会写入 THarness 通用层。
- 未确认内容不会写成稳定事实。
- 需要决定写入位置时会回到 `issue-routing.md`。

## 不适用场景

- 临时推理过程和一次性调试细节，只应保留在运行记录中。
