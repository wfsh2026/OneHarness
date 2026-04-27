# 项目 Wiki 维护工作流

## 目标

用最少读取成本为目标项目搭建、检索、更新或检查项目 wiki，并保持项目事实不进入通用 AIGC。

## 激活条件

用户明确表达以下任一意图时激活：

- 为已有工程主动搭建项目 wiki。
- 查找目标项目 wiki 中的项目事实。
- 开发后更新目标项目 wiki。
- 检查项目 wiki 的入口、来源、断链或事实边界。
- 其他工作流需要项目事实，但项目 wiki 缺失或过期。

## 前置条件

- 已确认目标项目根目录。
- 已确认项目适配配置。
- 已确认 `project_aigc_root`、`project_wiki_root` 和 `workflow_runs_root`。

缺少项目适配配置时，先读取 `../../projects/PROJECT_ADAPTER.md`。

## 默认读取

1. 本文件。
2. `../session-visible-state.md`。
3. `rules/INDEX.md`。
4. `../../projects/INDEX.md`。
5. 按维护目标读取命中的项目 wiki 规则。

## 阶段

| 阶段 | 输出 | 验证 |
| --- | --- | --- |
| 配置确认 | 项目适配配置摘要 | 必需路径来自适配配置，没有在通用 AIGC 中硬编码目标项目路径。 |
| 维护路由 | 搭建、检索、更新或健康检查分支 | 只命中一个主要分支。 |
| 最小读取 | 读取清单 | 先读项目 wiki 索引，再读命中页面；项目 wiki 缺失时只读项目入口文件。 |
| 执行维护 | 项目 wiki 页面或检查结果 | 只修改目标项目适配层中受影响的页面。 |
| 验证记录 | 维护验证结果 | 入口可达、来源明确、默认读取不会展开大目录或历史运行记录。 |

## 分支

| 分支 | 规则 |
| --- | --- |
| 主动搭建 | `../../projects/rules/project-wiki-bootstrap.md` |
| 创建结构 | `../../projects/rules/project-wiki-creation.md` |
| 检索事实 | `../../projects/rules/project-wiki-retrieval.md` |
| 更新页面 | `../../projects/rules/project-wiki-update.md` |
| 健康检查 | `../../projects/rules/project-wiki-health.md` |

## 完成标准

- 项目事实只写入目标项目适配层。
- 通用 AIGC 只保留规则、模板和路由。
- 项目 wiki 入口可达，命中页面包含 `read_when`。
- 项目事实有来源文件、验证记录或用户确认。
- 本轮运行过程写入目标项目运行记录，不写入通用 wiki。
