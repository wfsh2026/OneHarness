# 项目 Wiki 检索规则

## 结论

工作流需要目标项目事实时，通过本机 registry 定位项目胶囊，只读取目标项目 wiki 索引和命中页面，不读取整个项目 wiki。

## 调用顺序

1. 判断问题是否需要项目事实。
2. 需要项目事实时读取 `AIGC/_local/registry.yaml`，按 `project_id` 定位 `capsule_root`。
3. 读取 `{capsule_root}/ADAPTER.md`。
4. 读取 `{project_wiki_root}/INDEX.md`。
5. 按 `read_when` 命中一个或少数页面。
6. 页面不足时，再读取项目源码或文档入口补证据。
7. 补出的稳定事实按 `project-wiki-update.md` 回写。

## 命中规则

| 需求 | 优先页面 |
| --- | --- |
| 项目入口、目录职责 | `architecture/entry-map.md`、`architecture/repository-structure.md` |
| 模块职责、所有权 | `architecture/module-boundaries.md` |
| 依赖方向、禁止依赖 | `architecture/dependency-direction.md` |
| 配置、环境、参数 | `architecture/configuration-surface.md` |
| 构建、测试、运行 | `source-map/build-test-run.md` |
| 策划案、功能设计、体验目标 | `design/INDEX.md`、命中的 `design/features/{feature_id}.md` |
| 主程任务拆解、子任务、接口契约 | `development/INDEX.md`、命中的 `development/tasks/{task_id}.md` |
| 已确认决策 | `decisions/active.md` |
| 未决问题 | `open-questions.md` |

## 回退

- 如果项目 wiki 不存在，执行 `project-wiki-bootstrap.md`。
- 如果页面存在但信息过期，执行 `project-wiki-update.md`。
- 如果是跨项目架构问题，改读通用 `AIGC/wiki/INDEX.md`。
