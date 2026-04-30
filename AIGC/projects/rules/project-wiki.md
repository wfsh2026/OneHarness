# 项目 Wiki 规则

项目 wiki 用于恢复目标项目上下文，只保存该项目稳定、可追溯、可检索的事实和决策。

## 结构原则

- 结构参考通用架构 wiki：入口索引、Schema、机器索引、分区索引、规则、模板。
- 项目 wiki 放在目标项目适配层，不放在通用 AIGC。
- 默认只读 `INDEX.md`，其他页面必须由 `read_when` 命中。
- 页面只写一个主题，不复制大段源码。

## 推荐分区

| 分区 | 用途 |
| --- | --- |
| `architecture/` | 项目入口、目录结构、模块边界、依赖方向和配置入口。 |
| `source-map/` | 重要文件、构建测试命令、外部服务和事实来源。 |
| `decisions/` | 已确认项目决策和废弃决策。 |
| `design/` | 策划案、功能设计、核心体验、成功标准和待确认设计问题。 |
| `development/` | 主程评审、开发任务拆解、子任务分配、接口契约和验收入口。 |
| `workflows/` | 项目内开发、验证、发布或运维流程。 |
| `rules/` | 项目 wiki 的检索、写入、健康检查规则。 |
| `templates/` | 项目 wiki 页面模板。 |

## 默认读取

每次进入目标项目工作流时，只默认读取项目 wiki 的 `INDEX.md`。其他文件必须通过 `read_when` 命中后读取。

## 写入规则

- 项目事实写入项目 wiki。
- 未确认内容写入开放问题。
- 决策写入 decisions。
- 来源写入 source-map。
- 策划工作流确认的功能设计写入 `design/`。
- 主程评审通过后的任务拆解写入 `development/`。
- 临时执行过程、失败尝试和命令输出写入运行记录，不写入项目 wiki。

## 创建说明

完整创建流程见 `project-wiki-bootstrap.md` 和 `project-wiki-creation.md`。更新流程见 `project-wiki-update.md`。
