---
id: wiki-retrieval
title: 低 Token 检索规则
summary: 通过入口索引、read_when 和单页命中降低 wiki 读取成本。
type: rule
status: active
tags: [wiki, retrieval, token]
relates: []
read_when: 需要决定 wiki 读取顺序或控制上下文大小。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 低 Token 检索规则

## 结论

wiki 读取必须从索引开始，以 `read_when` 命中一个最小页面集合。

## 最小做法

1. 先读 `AIGC/wiki/INDEX.md`。
2. 命中架构问题时读 `architecture/INDEX.md`。
3. 只读取与本轮目标直接相关的知识页。
4. 若无法命中，先补索引或提问，不读取全目录。

## 验证方式

- 本轮读取文件能解释为什么需要读。
- 没有读取无关历史、日志、原始资料或项目事实。
- 输出中能说清本轮只用了哪个知识页。

## 不适用场景

- 用户明确要求审计整个 wiki。
- 用户明确要求迁移或重建 wiki 结构。
