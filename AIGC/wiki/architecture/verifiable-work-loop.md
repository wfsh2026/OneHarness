---
id: architecture-verifiable-work-loop
title: 可验证工作循环
summary: 把一次请求压缩成目标、最小改动、验证和记录闭环。
type: architecture-card
status: active
tags: [architecture, workflow, verification]
relates: ["[[architecture-workflow-routing]]", "[[architecture-knowledge-boundary]]"]
read_when: 需要把任务压缩成一个可验证的最小闭环。
source: OneHarness 当前最小工作循环。
updated: 2026-04-27
---

# 可验证工作循环

## 结论

通用项目工作流应把每轮任务压缩成一个可验证闭环，而不是一次读取全部资料或一次解决所有问题。

## 适用场景

- 用户目标可以拆成多个阶段。
- 项目上下文大，读取成本高。
- 任务需要交付、验证和记录。

## 最小做法

每轮只回答：

- 这次只做哪一件事。
- 成功标准是什么。
- 需要读取哪些最少文件。
- 需要修改哪些最少内容。
- 如何验证完成。
- 结果写入通用层还是项目适配层。

## 验证方式

- 本轮输出能对应一个明确目标。
- 验证结果可追溯。
- 未验证内容不会被标记完成。

## 不适用场景

- 用户明确要求开放式头脑风暴且不进入执行闭环时。
