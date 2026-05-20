# 项目接入入口

本目录定义其他工程如何通过本机 Tharness 启动通用 AIGC 工作流。

可提交的 `AIGC/projects/` 只保存：

- 本机项目 registry 的规则与模板。
- 项目胶囊规则。
- 项目文档书写规则。
- 项目 wiki 结构模板。

具体项目启动工作流后，必须在被 Git 忽略的 `AIGC/_local/projects/{project_id}/` 项目胶囊中保存运行记录和项目 wiki。

## 默认读取

| 文件 | read_when |
| --- | --- |
| `PROJECT_ADAPTER.md` | 需要为目标项目创建或读取本机项目胶囊。 |
| `rules/project-isolation.md` | 判断可提交通用层与本机项目胶囊的边界。 |
| `rules/project-wiki.md` | 需要理解项目 wiki 总规则。 |
| `rules/project-wiki-bootstrap.md` | 需要检索已有工程并在本机项目胶囊中主动搭建项目 wiki。 |
| `rules/project-wiki-update.md` | 需要在开发后更新已有项目 wiki。 |
| `rules/project-wiki-retrieval.md` | 工作流需要查找项目工程 wiki。 |
| `rules/project-wiki-health.md` | 需要检查项目 wiki 入口、断链、来源或事实边界。 |
| `rules/project-wiki-creation.md` | 需要创建完整项目 wiki 结构、页面和来源索引。 |
| `rules/run-records.md` | 需要保存项目工作流运行记录。 |
| `rules/document-writing.md` | 需要书写项目文档。 |

## 本机读取入口

本机项目 registry 固定为 `AIGC/_local/registry.yaml`。该文件不提交，只保存本机可访问的项目映射。

项目胶囊固定放在 `AIGC/_local/projects/{project_id}/`。胶囊内可以保存项目事实，但不得把其中内容复制到可提交的通用目录。
