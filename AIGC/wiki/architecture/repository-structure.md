---
id: architecture-repository-structure
title: 仓库分层结构
summary: 把源码、文档、配置、运行记录和通用规则分层，避免上下文污染。
type: architecture-card
status: active
tags: [architecture, structure, boundary]
relates: ["[[architecture-entry-map]]", "[[architecture-module-boundaries]]"]
read_when: 需要规划或审查项目目录结构。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 仓库分层结构

## 结论

仓库应按内容生命周期和适用范围分层，而不是按一次任务的产物混放。

## 最小做法

推荐区分：

- `src/` 或等价源码目录：产品实现。
- `config/` 或等价配置目录：可调整参数和环境入口。
- `docs/`：稳定文档。
- `runs/` 或项目适配层运行记录：任务过程和验证结果。
- `wiki/`：稳定、可检索、低频变化的项目知识。
- 通用 AIGC：只保存跨项目规则和模板。

## 验证方式

- 项目事实不会写入通用规则。
- 运行记录不会替代稳定 wiki。
- 默认入口不会读取全部历史记录。

## 不适用场景

- 项目已有强约束目录规范时，应遵循项目规范，只补充索引。
