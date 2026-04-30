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
    README.md
    SCHEMA.md
    index.yaml
    project.md
    status.md
    decisions/
      INDEX.md
      active.md
      deprecated.md
    architecture/
      INDEX.md
      entry-map.md
      repository-structure.md
      module-boundaries.md
      dependency-direction.md
      configuration-surface.md
    source-map/
      INDEX.md
      important-files.md
      build-test-run.md
      external-services.md
    design/
      INDEX.md
      features/
    development/
      INDEX.md
      tasks/
      subtasks/
      contracts/
    workflows/
      INDEX.md
      development.md
      verification.md
    rules/
      retrieval.md
      building.md
      health.md
    templates/
      project-card.md
    open-questions.md
```

## 边界

通用 AIGC 提供规则和模板。目标项目适配层保存项目事实。

## 调用规则

- 需要通用架构知识时读取通用 `AIGC/wiki/INDEX.md`。
- 需要目标项目事实时读取目标项目 `{project_aigc_root}/ADAPTER.md`，再读取 `{project_wiki_root}/INDEX.md`。
- 项目 wiki 的实际路径必须来自适配配置，不允许写死到通用 AIGC。
- 策划案、主程任务拆解、子任务分配和接口契约属于目标项目事实，写入目标项目 wiki。
- 工作流运行过程、失败尝试和一次性验证输出写入 `{workflow_runs_root}`，不写入项目 wiki 正文。
