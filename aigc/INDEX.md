# AIGC 通用角色入口

本目录的可提交内容只保存通用 AI 角色调度逻辑、入口机制和模板，不保存任何具体项目事实。

## 默认读取顺序

1. `AIGC/INDEX.md`
2. `AIGC/roles/INDEX.md`
3. `AIGC/roles/common/RULE.md`
4. `AIGC/roles/common/autonomy-policy.md`
5. `AIGC/roles/role-manager/RULE.md`
6. 角色管理员按任务命中读取路由、必要角色入口和紧凑工具摘要；完整技能与操作说明由实际执行者渐进读取。
6. 需要目标项目事实时，只从用户输入或任务包允许读取的当前工作区入口获取；THarness 不提供额外项目接入包。
7. 需要通用架构知识时，读取 `AIGC/wiki/INDEX.md`。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `roles/` | 角色库、角色管理员、通用角色规则和角色派发规则。 |
| `wiki/` | 给角色调度快速检索的通用知识库。 |
| `capabilities/` | 当前 AIGC 能力索引、版本和变更记录。 |
| `tharness.yaml` | 最小自检工具的配置入口。 |

历史项目资料不得保留在可提交的通用 AIGC 主分支；需要长期归档时使用项目自己的文档或独立归档仓库。

## 调度原则

自治、授权、合理假设、委派、任务包和验证分级统一遵守 `AIGC/roles/common/autonomy-policy.md`。本入口不复述其条件。

## 不允许写入的内容

- 具体项目的运行记录。
- 具体项目的知识沉淀。
- 具体项目的决策事实。
- 具体项目的代码结构分析。
这些内容不得写入 THarness 通用层。
