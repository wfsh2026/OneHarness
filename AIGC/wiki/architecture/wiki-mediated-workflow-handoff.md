---
id: architecture-wiki-mediated-workflow-handoff
title: 项目 Wiki 工作流交接
summary: 用项目 wiki 页面承载跨工作流交接，避免复制整份上下文。
type: architecture-card
status: active
tags: [architecture, workflow, wiki]
relates: ["[[architecture-project-adapter-layer]]", "[[architecture-knowledge-boundary]]", "[[architecture-workflow-routing]]"]
read_when: 需要设计策划、主程拆解、开发执行之间的低 token 交接方式。
source: OneHarness 2.0.0 策划到开发交接规则。
updated: 2026-04-30
---

# 项目 Wiki 工作流交接

## 结论

当一个工作流的输出会成为另一个工作流的输入，且内容属于项目事实时，应把稳定事实写入目标项目 wiki，并在后续工作流中只传递页面入口。

## 适用场景

- 策划讨论完成后，需要进入主程评审或开发拆解。
- 主程需要把功能拆成可追踪、可验证的开发任务。
- 子任务需要交给全新会话执行。
- 团队需要降低重复读取整份策划案、整份任务包或整份 wiki 的 token 成本。

## 最小做法

项目 wiki 至少提供两类交接页面：

- `design/`：保存已确认策划事实、核心体验、范围、非目标、成功标准和待确认设计问题。
- `development/`：保存主程评审结果、开发任务页、子任务页和接口契约。

工作流交接时只传递：

- 目标项目适配入口。
- 项目 wiki 页面入口。
- 必要的页面章节或 `read_when`。

子任务执行者默认只读取子任务页允许的入口，不读取完整项目 wiki，也不复制整份策划页面。

## 验证方式

- 后续工作流能从项目 wiki 索引命中交接页面。
- 页面只保存稳定事实、任务边界、接口契约和验证方式。
- 运行过程、失败尝试、命令输出和候选知识审核过程写入运行记录或交付物。
- 通用 AIGC 不保存目标项目事实。
- 子任务能在不依赖历史对话的情况下恢复上下文。

## 不适用场景

- 一次性临时讨论，不会进入开发或后续工作流。
- 仍未确认的想法；这类内容应进入开放问题或运行记录。
- 需要保存完整执行过程、终端输出或失败尝试的内容。
