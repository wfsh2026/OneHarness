---
id: wiki-building
title: 通用架构知识写入规则
summary: 新增 wiki 页面前先判断是否为跨项目、跨角色的通用架构知识。
type: rule
status: active
tags: [wiki, writing, architecture]
relates: ["[[wiki-retrieval]]", "[[wiki-health]]"]
read_when: 需要创建或更新通用架构 wiki 页面。
source: Tharness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 通用架构知识写入规则

## 结论

只有跨项目、跨角色可复用、低频变化、能帮助架构检索的内容才能写入本 wiki。

## 可写内容

- 角色系统架构原则。
- 角色管理员调度原则。
- 项目适配层原则。
- 通用知识写入边界。
- 能力注册和版本治理原则。
- 可验证工作闭环。
- 低 token 知识分层方法。

## 不可写内容

- 具体项目事实。
- 具体项目路径。
- 具体项目运行记录。
- 具体项目决策。
- 某个业务、引擎、玩法或工具链的专用细节。
- 具体角色技能正文。
- 具体角色工具调用说明。
- 角色派发边界表。
- 项目工程目录、模块边界、依赖方向或配置入口细节。

## 最小流程

1. 判断内容是否跨项目复用。
2. 选择一个 Tharness 通用架构主题。
3. 使用 `templates/architecture-card.md`。
4. 更新 `architecture/INDEX.md` 路由。
5. 执行 `rules/health.md` 的最小检查。
