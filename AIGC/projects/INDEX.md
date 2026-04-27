# 项目适配入口

本目录定义目标项目如何接入通用 AIGC 工作流。

这里不保存具体项目事实，只保存：

- 项目适配规则。
- 项目文档书写规则。
- 目标项目目录模板。
- 项目 wiki 模板。

具体项目启动工作流后，必须在目标项目自己的适配目录中保存运行记录和项目 wiki。

## 默认读取

| 文件 | read_when |
| --- | --- |
| `PROJECT_ADAPTER.md` | 需要为目标项目启动 AIGC 工作流。 |
| `rules/project-isolation.md` | 判断通用 AIGC 与项目内容边界。 |
| `rules/project-wiki.md` | 需要理解项目 wiki 总规则。 |
| `rules/project-wiki-bootstrap.md` | 需要检索已有工程并主动搭建项目 wiki。 |
| `rules/project-wiki-update.md` | 需要在开发后更新已有项目 wiki。 |
| `rules/project-wiki-retrieval.md` | 工作流需要查找项目工程 wiki。 |
| `rules/project-wiki-health.md` | 需要检查项目 wiki 入口、断链、来源或事实边界。 |
| `rules/project-wiki-creation.md` | 需要创建完整项目 wiki 结构、页面和来源索引。 |
| `rules/run-records.md` | 需要保存项目工作流运行记录。 |
| `rules/document-writing.md` | 需要书写项目文档。 |
