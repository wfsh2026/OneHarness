# AIGC 通用工作流入口

本目录的可提交内容只保存通用 AI 开发工作流逻辑、项目接入机制和模板，不保存任何具体项目事实。

## 默认读取顺序

1. `AIGC/INDEX.md`
2. `AIGC/workflows/INDEX.md`
3. 命中工作流的 `WORKFLOW.md`
4. 命中工作流的 `rules/INDEX.md`
5. `AIGC/wiki/INDEX.md`
6. 按 `read_when` 命中的规则继续读取下级文件。
7. 需要目标项目事实时，读取 `AIGC/projects/INDEX.md`，再通过本机 `AIGC/_local/registry.yaml` 定位项目胶囊和项目 wiki。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `workflows/` | 通用工作流定义。 |
| `wiki/` | 给通用工作流快速检索的知识库。 |
| `projects/` | 项目接入、项目胶囊和本机索引的规则与模板。 |
| `capabilities/` | 当前 AIGC 能力索引、版本和变更记录。 |
| `_local/` | 本机项目索引、项目胶囊、项目 wiki 和运行记录；必须被 Git 忽略。 |
| `tharness.yaml` | 最小自检工具的配置入口。 |

历史项目资料不得保留在可提交的通用 AIGC 主分支；需要本机沉淀时写入 `AIGC/_local/`，需要长期归档时使用独立归档仓库。

## 不允许写入的内容

- 具体项目的运行记录。
- 具体项目的 wiki。
- 具体项目的决策事实。
- 具体项目的代码结构分析。

这些内容必须写入 `AIGC/_local/projects/{project_id}/` 下的本机项目胶囊，由 `projects/` 下的模板定义；该目录不得提交到 Git。
