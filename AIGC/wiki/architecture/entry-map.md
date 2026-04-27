---
id: architecture-entry-map
title: 架构入口地图
summary: 为项目建立最小可读入口，让 AI 不读全仓也能开始定位。
type: architecture-card
status: active
tags: [architecture, entry, retrieval]
relates: ["[[architecture-repository-structure]]"]
read_when: 需要为项目建立或审查架构检索入口。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 架构入口地图

## 结论

每个项目都需要一个最小架构入口，用来说明从哪里开始读、按什么意图继续读、哪些内容默认禁止全量读取。

## 适用场景

- 新项目接入通用 AIGC 工作流。
- 旧项目缺少稳定入口，AI 每次都要重新扫描。
- 项目已有文档很多，但没有低 token 路由。

## 最小做法

入口文件只回答四件事：

1. 项目是什么类型。
2. 默认先读哪些最少文件。
3. 常见意图分别路由到哪里。
4. 哪些目录默认不能全量读取。

## 验证方式

- 新会话只读入口文件后，能知道下一步该读哪个索引。
- 入口没有复制正文。
- 入口不包含长日志和一次性记录。

## 不适用场景

- 一次性脚本或无后续维护价值的临时目录。
