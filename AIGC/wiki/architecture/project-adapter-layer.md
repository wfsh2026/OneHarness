---
id: architecture-project-adapter-layer
title: 项目适配包层
summary: 用本机忽略目录中的项目适配包保存项目事实、项目专属角色和运行记录。
type: architecture-card
status: active
tags: [architecture, adapter, isolation]
relates: ["[[architecture-role-system]]", "[[architecture-knowledge-boundary]]"]
read_when: 需要隔离可提交通用框架与目标项目事实、运行记录和项目知识。
source: Tharness 当前项目适配规则。
updated: 2026-04-27
---

# 项目适配包层

## 结论

可提交的通用框架只提供角色规则、通用知识和路由；目标项目事实必须保存在本机 `AIGC/project-adapters/{project_id}/` 项目适配包。

## 适用场景

- 同一套通用角色调度规则要服务多个项目。
- 项目需要保存运行记录、决策、开放问题、项目知识和项目专属角色。
- 同一个本机 Tharness 需要索引多个目标项目。
- 可提交的通用框架曾经被项目事实污染。

## 最小做法

适配层至少确认：

- 项目 ID。
- 项目显示名。
- 本机目标项目根目录。
- 项目适配包根目录。
- 目标项目已有 AIGC 工程入口。
- 项目知识入口。
- 项目专属角色入口。
- 任务运行记录入口。
- 允许读取、允许写入和禁止写入范围。

## 验证方式

- 项目事实不写入可提交的通用框架。
- 运行记录不写入通用 wiki。
- 通用规则中不硬编码目标项目路径。
- `AIGC/project-adapters/` 被 Git 忽略。

## 不适用场景

- 只有一个短期项目且不需要复用通用规则时。
