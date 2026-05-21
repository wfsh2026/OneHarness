# 项目知识沉淀路由规则

## 结论

项目知识沉淀写入 `AIGC/project-adapters/{project_id}/knowledge/`。该目录只保存当前项目稳定、可追溯、可检索的事实、决策、来源和开放问题。

## 读取入口

1. 先由角色管理员按 `../role-manager/project-adapter-routing.md` 定位项目适配包。
2. 读取 `{project_id}/knowledge/INDEX.md`。
3. 按 `read_when` 命中一个或少数页面。
4. 页面不足时，由角色管理员决定是否读取目标项目源码、已有 AIGC 工程或用户提供资料补证据。

## 推荐结构

```text
knowledge/
  INDEX.md
  rules.md
  project.md
  status.md
  decisions/
    INDEX.md
    active.md
    deprecated.md
  source-map/
    INDEX.md
    important-files.md
    build-test-run.md
  design/
    INDEX.md
  development/
    INDEX.md
  open-questions.md
```

## 写入规则

- 已确认项目事实写入 `knowledge/` 对应页面。
- 项目决策写入 `knowledge/decisions/`。
- 来源和证据写入 `knowledge/source-map/`。
- 未确认内容写入 `knowledge/open-questions.md`。
- 一次性调试过程、失败尝试和长命令输出写入 `runs/`，不写入知识正文。
- 项目有自己的 AIGC 工程时，先记录对接入口，不复制整份工程内容。

## 项目专属角色

- 项目专属角色写入 `{project_id}/roles/`。
- 项目专属角色只能收紧或补充通用角色规则，不能放宽 `AIGC/roles/common/RULE.md`。
- 角色管理员派发项目专属角色时，任务包必须明确允许读取和允许写入范围。

## 健康检查

- `knowledge/INDEX.md` 只做路由，不复制正文。
- 可检索页面必须有 `read_when`。
- 稳定事实必须有来源文件、用户确认或验证记录。
- 项目事实不得进入 `AIGC/wiki`、`AIGC/roles` 或其他可提交通用层。
- `AIGC/project-adapters/` 必须被 Git 忽略。

## 禁止

- 禁止把通用规则复制进项目知识正文；只能引用。
- 禁止把未确认推测写成项目事实。
- 禁止用运行记录替代决策记录。
- 禁止提交 `AIGC/project-adapters/` 下的项目适配包。
