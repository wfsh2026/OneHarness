---
id: architecture-configuration-surface
title: 配置面
summary: 把需要动态调整的参数放入配置入口，避免硬编码扩散。
type: architecture-card
status: active
tags: [architecture, configuration, maintainability]
relates: ["[[architecture-repository-structure]]"]
read_when: 需要判断参数、路径、开关或环境差异应该放在哪里。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# 配置面

## 结论

会随环境、项目、版本或用户策略变化的值，应进入配置面，而不是散落在实现代码中。

## 最小做法

配置面至少说明：

- 配置项名称。
- 默认值。
- 允许范围。
- 生效时机。
- 读取入口。
- 验证方式。

## 验证方式

- 调整参数不需要改业务代码。
- 默认配置能独立说明系统行为。
- 无效配置有明确验证方式。

## 不适用场景

- 真正常量、协议固定值或语言级不可配置约束。
