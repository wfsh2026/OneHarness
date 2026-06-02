---
id: wiki-building
title: 通用架构 wiki 页面创建规则
summary: 写入位置已由 issue-routing 确认为通用架构 wiki 后，按本规则创建或更新页面。
type: rule
status: active
tags: [wiki, writing, architecture]
relates: ["[[wiki-retrieval]]", "[[wiki-health]]"]
read_when: 写入位置已由 issue-routing 确认为 AIGC/wiki/architecture/，需要创建或更新通用架构 wiki 页面。
source: Tharness 通用 wiki 重建设计。
updated: 2026-05-26
---

# 通用架构 wiki 页面创建规则

## 结论

写入位置必须先由 `AIGC/roles/role-manager/issue-routing.md` 判定。本文件只规定候选内容已经命中 `AIGC/wiki/architecture/` 后，如何创建或更新通用架构 wiki 页面。

## 适用前提

- `issue-routing.md` 已选择 `AIGC/wiki/architecture/` 作为唯一写入位置。
- 候选内容有来源、验证记录或用户确认。
- 候选内容能帮助后续架构检索，不是一次性运行记录。

## 最小流程

1. 选择一个 Tharness 通用架构主题。
2. 使用 `templates/architecture-card.md`。
3. 保持页面只记录通用架构结论，不复制角色技能、工具说明或项目事实。
4. 更新 `architecture/INDEX.md` 路由。
5. 执行 `rules/health.md` 的最小检查。
