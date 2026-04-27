# 项目适配说明

项目适配层是在目标项目中创建的工作区，用于保存该项目自己的 AIGC 运行记录、项目 wiki 和项目文档规则引用。

## 适配配置

目标项目必须先确认：

- `project_name`
- `project_root`
- `project_aigc_root`
- `active_workflow`
- `project_wiki_root`
- `workflow_runs_root`

## 推荐目标项目结构

以下结构只作为模板，实际路径必须来自适配配置。

```text
{project_aigc_root}/
  INDEX.md
  ADAPTER.md
  workflows/
    {workflow_id}/
      runs/
        INDEX.md
  wiki/
    INDEX.md
    status.md
    context.md
    decisions/
      INDEX.md
    open-questions.md
    source-map.md
```

## 边界

通用 AIGC 提供规则和模板。目标项目适配层保存项目事实。

