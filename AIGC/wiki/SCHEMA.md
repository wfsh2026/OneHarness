---
id: wiki-schema
title: Wiki 页面 Schema
summary: 定义通用 wiki 可检索页面的类型、元数据和正文规则。
type: rule
status: active
tags: [wiki, schema, metadata]
relates: ["[[wiki-health]]", "[[wiki-building]]"]
read_when: 需要创建、修改或审查通用 wiki 页面格式。
source: OneHarness 通用 wiki 重建设计。
updated: 2026-04-27
---

# Wiki 页面 Schema

## 页面类型

| 类型 | 目录 | 用途 |
| --- | --- | --- |
| `architecture-card` | `architecture/` | 记录一个通用项目架构搭建主题。 |
| `rule` | `rules/` | 记录 wiki 检索、写入或健康检查规则。 |
| `template` | `templates/` | 记录创建页面时使用的模板。 |

## YAML 头

所有可检索页面必须包含：

```yaml
---
id: unique-id
title: 标题
summary: 一句话摘要
type: architecture-card
status: active
tags: [architecture]
relates: []
read_when: 何时读取本页
source: 来源
updated: YYYY-MM-DD
---
```

## 字段规则

| 字段 | 规则 |
| --- | --- |
| `id` | 全局唯一，使用 kebab-case。 |
| `title` | 人类可读标题。 |
| `summary` | 一句话说明，不写完整论证。 |
| `type` | 只能使用本文件定义的页面类型。 |
| `status` | `active`、`candidate`、`deprecated`。 |
| `tags` | 用于检索，不超过 5 个。 |
| `relates` | 使用 `[[id]]` 表达关联。 |
| `read_when` | 明确触发读取条件。 |
| `source` | 说明来自通用规则、用户确认或已验证经验。 |
| `updated` | 最近更新日期。 |

## 正文规则

正文只保留通用架构结论，推荐结构：

1. 结论。
2. 适用场景。
3. 最小做法。
4. 验证方式。
5. 不适用场景。

## 禁止

- 禁止把项目名、项目路径、仓库路径或运行记录写入通用页面。
- 禁止把一次性调试过程写成通用知识。
- 禁止在索引页复制正文。
- 禁止没有 `read_when` 的页面进入可检索区。
