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
updated: 2026-04-27
---

# 角色调度路由

## 结论

Tharness 架构应提供一个角色调度层。所有用户请求先由角色管理员接收，再按角色库和 `role-manager/role-routing/` 命中最小必要角色、任务包、验证要求和交付边界。

## 适用场景

- 项目同时支持讨论、开发、验证、演进等多种任务。
- AI 容易为了保险读取过多规则。
- 同一请求可能被误判为多个执行路径。

## 最小做法

角色调度层至少包含：

- 角色显示名和角色规则入口。
- 角色派发检索入口。
- 任务包允许读取和允许写入边界。
- 完成标准。
- 验证要求。

## 验证方式

- 一个用户请求只能先由角色管理员接收。
- 具体角色任务必须通过 SubAgent 或全新会话派发。
- 具体角色只读取自身 `RULE.md`、命中的 `skills/`、命中的 `tools/` 和任务包允许资料。
- 出现关键歧义时能回到澄清，而不是继续猜测。

## 不适用场景

- 单一用途脚本或没有长期协作需求的临时任务。
