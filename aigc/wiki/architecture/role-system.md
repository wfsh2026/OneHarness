---
id: architecture-role-system
title: 角色系统架构
summary: 用角色管理员、角色规则、技能索引和工具索引构成 Tharness 的执行核心。
type: architecture-card
status: active
tags: [architecture, role, system]
relates: ["[[architecture-role-dispatch-routing]]", "[[architecture-knowledge-boundary]]"]
read_when: 需要理解 Tharness 角色体系、角色目录职责、技能工具归属或管理员调度边界。
source: Tharness 当前角色系统设计。
updated: 2026-05-26
---

# 角色系统架构

## 结论

Tharness 的工程核心是角色系统。本页只解释角色系统的分层结构；可执行规则以 `AIGC/roles/INDEX.md`、`AIGC/roles/common/RULE.md`、`AIGC/roles/role-manager/RULE.md` 和对应角色 `RULE.md` 为准。

## 适用场景

- 需要解释为什么主会话只能由角色管理员沟通。
- 需要判断角色规则、技能、工具和派发边界分别放在哪里。
- 需要新增或调整角色目录结构。
- 需要避免把旧工作流阶段重新塞回角色目录。

## 最小做法

角色系统目录职责保持如下：

- `AIGC/roles/common/` 保存所有角色必须遵守的最小规则、会话输出格式和通用模板。
- `AIGC/roles/role-manager/` 保存角色管理员规则、角色派发检索和任务包模板。
- `AIGC/roles/role-manager/session-revival.md` 保存角色会话复活、失败处理和运行态记录要求。
- `AIGC/roles/{role-id}/RULE.md` 是具体角色唯一根入口。
- `AIGC/roles/{role-id}/skills/` 保存该角色执行任务时可复用的技能说明。
- `AIGC/roles/{role-id}/tools/` 保存该角色允许使用的工具调用说明。
- 角色派发边界、冲突判断和主责任面选择只放在 `AIGC/roles/role-manager/role-routing/`。

## 验证方式

- 角色系统强规则只在 `AIGC/roles/` 下维护，本页不复制执行约束。
- 具体角色根目录没有 `INPUT.md`、`OUTPUT.md`、`BOUNDARY.md` 或 `HANDOFF.md`。
- 角色管理员任务包字段、会话复活规则和执行角色读取边界能从 `AIGC/roles/` 对应入口命中。
- wiki 只说明角色系统的通用架构原则，不保存具体角色技能或工具说明正文。

## 不适用场景

- 某个角色的具体执行技巧；应写入该角色 `skills/`。
- 某个角色的工具调用细则；应写入该角色 `tools/`。
- 某个项目的专属角色或项目事实；不得写入 THarness 通用层。
