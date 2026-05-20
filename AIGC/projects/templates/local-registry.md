# 本机项目 Registry 模板

本模板用于创建 `AIGC/_local/registry.yaml`。该文件必须被 Git 忽略，不得提交。

```yaml
projects:
  - project_id:
    display_name:
    source_project_root:
    capsule_root:
    active_workflow:
    project_wiki_root:
    workflow_runs_root:
    created_at:
```

## 字段说明

| 字段 | 用途 |
| --- | --- |
| `project_id` | 本机唯一项目标识。 |
| `display_name` | 用户可读项目名。 |
| `source_project_root` | 本机真实目标工程根目录。 |
| `capsule_root` | 本机项目胶囊根目录，通常为 `AIGC/_local/projects/{project_id}`。 |
| `active_workflow` | 当前默认工作流。 |
| `project_wiki_root` | 项目 wiki 根目录。 |
| `workflow_runs_root` | 工作流运行记录根目录。 |
| `created_at` | 创建日期。 |

## 禁止

- 禁止把真实项目路径写入可提交的通用文件。
- 禁止提交 `AIGC/_local/registry.yaml`。
- 禁止多个项目共享同一个 `capsule_root` 或 `project_wiki_root`。
