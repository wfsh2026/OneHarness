---
id: workflow-planning-discussion-project-adaptation
title: 项目适配规则
workflow: planning-discussion
phase: project-adaptation
read_when: 需要在目标项目建立运行记录、项目 wiki 或项目文档规则。
updated: 2026-04-27
---

# 项目适配规则

目标项目启动工作流时，必须先在本机 registry 中建立项目胶囊。

## 项目胶囊负责

- 保存项目工作流运行记录。
- 保存项目 wiki。
- 保存项目决策。
- 保存项目文档规则引用。

## 路径规则

所有路径必须来自 `AIGC/_local/registry.yaml` 或项目胶囊配置，不允许在通用工作流中硬编码目标项目路径。

## 最小适配内容

- 本机 registry 条目。
- 项目胶囊配置。
- 项目 wiki 入口。
- 当前工作流运行记录入口。
- 项目开放问题。
