---
id: architecture-role-dispatch-routing
title: 角色调度路由
summary: 先由角色管理员接收任务，再按角色库把任务派发给最小必要角色。
type: architecture-card
status: active
tags: [architecture, role, dispatch, routing]
relates: ["[[architecture-role-system]]", "[[architecture-verifiable-work-loop]]"]
read_when: 需要为任务选择角色、派发方式、规则索引和后续读取路径。
source: Tharness 当前角色调度结构。
updated: 2026-05-26
---

# 角色调度路由

## 结论

Tharness 架构应提供一个角色调度层。本页只解释为什么需要调度层；具体派发规则、任务包字段和主会话读取限制以 `AIGC/roles/INDEX.md` 与 `AIGC/roles/role-manager/RULE.md` 为准。

## 适用场景

- 项目同时支持讨论、开发、验证、演进等多种任务。
- AI 容易为了保险读取过多规则。
- 同一请求可能被误判为多个执行路径。

## 最小做法

角色调度层至少需要让以下入口可检索：

- 角色显示名和角色规则入口。
- 角色派发检索入口。
- 任务包模板入口。
- 验证要求入口。
- 交付判断入口。

## 验证方式

- 执行约束只在 `AIGC/roles/` 下维护，本页不复制派发规则。
- 角色派发检索能从 `AIGC/roles/role-manager/role-routing/INDEX.md` 命中。
- 任务包模板能从 `AIGC/roles/role-manager/templates/subagent-task.md` 命中。

## 不适用场景

- 单一用途脚本或没有长期协作需求的临时任务。
