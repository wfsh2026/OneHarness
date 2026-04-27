# 通用架构 Wiki 入口

本 wiki 只保存跨项目可复用的项目架构搭建知识，用于低 token 检索通用架构信息。

## 默认读取

默认只读本文件。按用户意图命中后，再读取对应索引或规则正文。

| 文件 | read_when |
| --- | --- |
| `README.md` | 需要理解新版 wiki 的定位、边界和工作方式。 |
| `SCHEMA.md` | 需要创建、修改或审查 wiki 页面格式。 |
| `rules/retrieval.md` | 需要降低 token 消耗或判断读取顺序。 |
| `rules/building.md` | 需要新增通用架构知识页。 |
| `rules/health.md` | 需要检查 wiki 是否断链、孤岛、缺元数据或混入项目事实。 |
| `architecture/INDEX.md` | 需要检索通用项目架构搭建知识。 |
| `templates/architecture-card.md` | 需要创建新的通用架构知识页。 |

## 当前分区

| 分区 | 用途 |
| --- | --- |
| `architecture/` | 通用项目架构搭建知识。 |
| `rules/` | wiki 检索、写入、健康检查规则。 |
| `templates/` | 新页面模板。 |

## 禁止

- 禁止保存具体项目事实。
- 禁止保存具体项目运行记录。
- 禁止保存具体项目代码结构分析。
- 禁止保存项目专用工具、路径、配置、资源清单。
- 禁止为了保险读取整个 wiki。
