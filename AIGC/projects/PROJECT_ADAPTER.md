# 项目胶囊说明

项目胶囊是在本机 `AIGC/_local/projects/{project_id}/` 中创建的工作区，用于保存某个目标项目自己的 AIGC 运行记录、项目 wiki、项目决策和项目文档规则引用。

可提交的通用 AIGC 只提供规则、模板和路由；项目事实必须保存在本机项目胶囊中，且 `AIGC/_local/` 必须被 Git 忽略。

## 本机 Registry

启动目标项目工作流前，必须先确认 `AIGC/_local/registry.yaml` 中存在该项目条目。

每个项目条目至少确认：

- `project_id`
- `display_name`
- `source_project_root`
- `capsule_root`
- `active_workflow`
- `project_wiki_root`
- `workflow_runs_root`

`source_project_root` 是本机真实工程路径，只允许写在 `AIGC/_local/registry.yaml` 或项目胶囊内，不允许写入可提交的通用文件。

## 推荐项目胶囊结构

以下结构只作为模板，实际路径必须来自本机 registry 和项目胶囊配置。

```text
{capsule_root}/
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

- `AIGC/workflows`、`AIGC/wiki`、`AIGC/capabilities`、`AIGC/projects` 是可提交通用层。
- `AIGC/_local/` 是本机项目层，不得提交。
- 通用层可以保存项目胶囊规则和模板，不能保存具体项目事实。
- 项目胶囊可以保存对应项目的事实、运行记录、决策和来源索引。

## 调用规则

- 需要通用架构知识时读取通用 `AIGC/wiki/INDEX.md`。
- 需要目标项目事实时读取 `AIGC/projects/INDEX.md`，再读取 `AIGC/_local/registry.yaml`。
- 根据 registry 命中的 `capsule_root` 读取 `{capsule_root}/ADAPTER.md`，再读取 `{project_wiki_root}/INDEX.md`。
- 项目 wiki 的实际路径必须来自 registry 或项目胶囊配置，不允许写死到通用 AIGC。
- 策划案、主程任务拆解、子任务分配和接口契约属于目标项目事实，写入项目胶囊内的项目 wiki。
- 工作流运行过程、失败尝试和一次性验证输出写入 `{workflow_runs_root}`，不写入项目 wiki 正文。
