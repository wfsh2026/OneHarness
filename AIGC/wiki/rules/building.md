---
id: wiki-building
title: 通用架构知识写入规则
summary: 新增 wiki 页面前先判断是否为跨项目架构知识。
type: rule
status: active
tags: [wiki, writing, architecture]
relates: ["[[wiki-retrieval]]", "[[wiki-health]]"]
read_when: 需要创建或更新通用架构 wiki 页面。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 通用架构知识写入规则

## 结论

只有跨项目可复用、低频变化、能帮助架构检索的内容才能写入本 wiki。

## 可写内容

- 项目目录分层模式。
- 模块边界划分方法。
- 依赖方向和禁止依赖规则。
- 配置入口和环境隔离方式。
- 数据流、控制流和扩展点的通用描述。
- 架构健康检查方法。

## 不可写内容

- 具体项目事实。
- 具体项目路径。
- 具体项目运行记录。
- 具体项目决策。
- 某个业务、引擎、玩法或工具链的专用细节。

## 最小流程

1. 判断内容是否跨项目复用。
2. 选择一个架构主题。
3. 使用 `templates/architecture-card.md`。
4. 更新 `architecture/INDEX.md` 路由。
5. 执行 `rules/health.md` 的最小检查。
