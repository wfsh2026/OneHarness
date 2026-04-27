# 项目 Wiki 主动搭建规则

## 结论

当目标项目需要反复读取项目事实，且没有项目 wiki 时，先用最小检索建立项目 wiki，再进入开发任务。

## 触发条件

- 用户要求为当前工程搭建项目 wiki。
- 工作流需要项目目录、构建、测试、配置或模块事实，但 `{project_wiki_root}/INDEX.md` 不存在。
- 项目已有适配层，但缺少可检索的项目事实入口。

## 输入

- `project_name`
- `project_root`
- `project_aigc_root`
- `project_wiki_root`
- `workflow_runs_root`

所有输入必须来自项目适配配置。

## 最小检索

只读取能建立项目骨架的入口：

- 项目根目录文件列表。
- README 或同等入口文档。
- 构建、包管理、测试配置文件。
- 主要源码目录的一层目录结构。
- 已存在的项目文档索引。

## 搭建流程

1. 确认项目适配配置完整。
2. 创建 `PROJECT_ADAPTER.md` 中定义的项目 wiki 结构。
3. 使用 `../templates/project-wiki-index.md` 创建入口索引。
4. 使用 `../templates/project-card.md` 创建项目事实页。
5. 写入已确认的入口、目录职责、构建测试命令、配置入口和模块边界。
6. 未确认内容写入 `open-questions.md`。
7. 执行 `project-wiki-health.md` 的最小检查。

## 验证

- `{project_wiki_root}/INDEX.md` 存在。
- 每个可检索页面有 `read_when`。
- 项目事实能追溯到来源文件或用户确认。
- 默认读取不会展开整个项目 wiki。

## 禁止

- 禁止把项目 wiki 写入通用 `AIGC/wiki`。
- 禁止把源码全文复制进项目 wiki。
- 禁止在通用 AIGC 中硬编码目标项目路径。
