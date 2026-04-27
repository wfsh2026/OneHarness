---
id: candidate-single-writer-file-ownership
status: candidate
scope: 多 Agent 协作、开发任务拆分、文档合并
source: source-legacy-mvp-review
last_verified: 2026-04-25
read_when: 需要拆分并行任务、分配文件归属或合并多个 Agent 输出
confidence: medium
---

# 同文件唯一写入者

## 结论

多个 Agent 协作时，同一文件同一时间只能有一个写入者。其他 Agent 只能输出修改建议，由主调度者或指定写入者统一合并。

## 适用范围

- 多 Agent 并行开发。
- 多个角色都需要修改同一知识文件。
- 设定、决策、计划、核心入口等高冲突文档。

## 输出要求

每个 Agent 输出应记录：

- 角色。
- 输入。
- 输出。
- 文件归属。
- 验证方式。
- 采纳状态。
- 未采纳原因。

## 不适用场景

- 单一执行者串行修改。
- 文件已经明确分片且互不重叠。

## 来源

来自旧项目删除前审查中提取的可复用多执行者协作经验，详见来源索引。当前 AIGC 抽象为通用候选知识。
