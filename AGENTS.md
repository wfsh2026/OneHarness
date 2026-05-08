# AIGC 通用工作流入口

本目录只保存通用 AI 开发工作流逻辑，不保存任何具体项目事实。

## 默认读取顺序

1. `AIGC/INDEX.md`
2. `AIGC/workflows/INDEX.md`
3. 命中工作流的 `WORKFLOW.md`
4. 命中工作流的 `rules/INDEX.md`
5. `AIGC/wiki/INDEX.md`
6. 按 `read_when` 命中的规则继续读取下级文件。
7. 需要目标项目事实时，读取 `AIGC/projects/INDEX.md`，再按目标项目适配配置读取项目 wiki。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `workflows/` | 通用工作流定义。 |
| `wiki/` | 给通用工作流快速检索的知识库。 |
| `projects/` | 在目标项目中建立项目适配层的规则与模板。 |
| `capabilities/` | 当前 AIGC 能力索引、版本和变更记录。 |
| `oneharness.yaml` | 最小自检工具的配置入口。 |

历史项目资料不得保留在通用 AIGC 主分支；需要追溯时从 Git 历史或独立归档仓库读取。

## 不允许写入的内容

- 具体项目的运行记录。
- 具体项目的 wiki。
- 具体项目的决策事实。
- 具体项目的代码结构分析。

这些内容必须写入目标项目自己的项目适配目录，由 `projects/` 下的模板定义。
