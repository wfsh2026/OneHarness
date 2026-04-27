# 项目 Wiki 规则

项目 wiki 用于恢复目标项目上下文。

## 最小文件

- `INDEX.md`
- `status.md`
- `context.md`
- `decisions/INDEX.md`
- `open-questions.md`
- `source-map.md`

## 默认读取

每次进入目标项目工作流时，只默认读取项目 wiki 的 `INDEX.md`。其他文件必须通过 `read_when` 命中后读取。

## 写入规则

- 项目事实写入项目 wiki。
- 未确认内容写入开放问题。
- 决策写入 decisions。
- 来源写入 source-map。

## 创建说明

完整创建流程、页面类型和模板要求见 `project-wiki-creation.md`。
