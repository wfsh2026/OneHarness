# 项目 Wiki 创建规则

## 用途

项目 wiki 用于恢复目标项目上下文，保存该项目稳定、可追溯、可检索的事实和决策。

## 创建前必须确认

- `project_name`
- `project_root`
- `project_aigc_root`
- `project_wiki_root`
- `workflow_runs_root`

所有路径必须来自项目适配配置，不允许在通用 AIGC 中硬编码目标项目路径。

## 最小结构

```text
{project_wiki_root}/
  INDEX.md
  status.md
  context.md
  decisions/
    INDEX.md
  open-questions.md
  source-map.md
```

## 推荐扩展结构

当项目知识增加后，可以按需新增：

```text
{project_wiki_root}/
  architecture/
  requirements/
  workflows/
  glossary.md
  risks.md
```

扩展目录必须按实际检索需要创建，不提前空建复杂结构。

## 页面类型

| 类型 | 用途 |
| --- | --- |
| `status` | 当前项目状态和可执行入口。 |
| `context` | 项目背景、目标和范围。 |
| `decision` | 已确认决策。 |
| `architecture` | 稳定架构和模块边界。 |
| `requirement` | 稳定需求。 |
| `workflow` | 项目内流程。 |
| `glossary` | 术语。 |
| `risk` | 已确认风险。 |

## 页面要求

每个页面只写一个主题，并尽量包含：

- 标题。
- 用途。
- 适用范围。
- 当前状态。
- 来源或关联决策。
- `read_when`。

## 写入规则

- 项目事实写入项目 wiki。
- 项目决策写入 `decisions/`。
- 未确认内容写入 `open-questions.md`。
- 来源写入 `source-map.md`。
- 临时执行过程写入运行记录，不进入项目 wiki。

## 假设晋升规则

- 未验证想法只能写入开放问题、候选页面或运行记录。
- 探索型任务必须先记录待验证假设。
- 验证通过或用户确认后，才能晋升为项目事实、机制或决策。
- 验证失败的方案应写入废弃方案或保留在运行记录中，并说明原因。

## 创建流程

1. 读取项目适配配置。
2. 创建最小 wiki 结构。
3. 使用 `../templates/project-wiki-index.md` 创建入口。
4. 使用 `../templates/project-wiki-page.md` 创建具体页面。
5. 使用 `../templates/project-source-map.md` 记录来源。
6. 更新 `INDEX.md` 的读取路由。
7. 验证默认入口不会读取全部历史。
8. 执行最小健康检查，确认入口可达、来源明确、状态正确。

## 禁止

- 禁止多个项目共享同一个项目 wiki。
- 禁止把通用规则复制进项目 wiki；只能引用。
- 禁止把未确认内容写成项目事实。
- 禁止把运行记录替代决策记录。
