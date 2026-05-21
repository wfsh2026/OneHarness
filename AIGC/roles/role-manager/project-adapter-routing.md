# 项目适配路由规则

## 结论

Tharness 本体只保留一份。目标项目适配内容写入本机 `AIGC/project-adapters/{project_id}/`，由根索引 `AIGC/project-adapters/INDEX.md` 统一检索。

`AIGC/project-adapters/` 是本机项目适配区，必须被 Git 忽略。它可以保存目标项目事实、项目专属角色、项目知识沉淀和运行记录。

## 触发条件

- 用户要求接入、切换或分析某个目标项目。
- 角色管理员需要目标项目事实、项目专属角色或项目已有 AIGC 工程入口。
- 执行角色任务需要读取目标项目知识、决策、来源或运行记录。

## 读取顺序

1. 读取 `AIGC/project-adapters/INDEX.md`，按 `project_id` 或项目显示名命中目标项目。
2. 读取 `AIGC/project-adapters/{project_id}/ADAPTER.md`。
3. 需要项目专属角色时读取 `{project_id}/roles/INDEX.md`，再按任务命中角色规则。
4. 需要项目知识时读取 `{project_id}/knowledge/INDEX.md`，再按 `read_when` 命中具体页面。
5. 需要恢复或追溯任务过程时读取 `{project_id}/runs/INDEX.md`。

## 项目适配包结构

```text
AIGC/project-adapters/
  INDEX.md
  {project_id}/
    ADAPTER.md
    roles/
      INDEX.md
      {project_role}/RULE.md
    knowledge/
      INDEX.md
      rules.md
      decisions/
      source-map/
      open-questions.md
    runs/
      INDEX.md
```

## ADAPTER.md 必须说明

- `project_id` 和项目显示名。
- 目标项目是否已有自己的 AIGC 工程。
- 目标项目 AIGC 工程入口和对接方式。
- 默认项目知识入口。
- 项目专属角色入口。
- 运行记录入口。
- 允许读取、允许写入和禁止写入范围。
- 项目事实来源优先级。

## 边界

- 目标项目事实不得写入可提交的 Tharness 通用层。
- 项目专属角色只能写入 `AIGC/project-adapters/{project_id}/roles/`。
- 项目知识只能写入 `AIGC/project-adapters/{project_id}/knowledge/`。
- 项目运行记录只能写入 `AIGC/project-adapters/{project_id}/runs/`。
- 通用角色库只保存跨项目角色，不保存项目专属角色。

## 禁止

- 禁止新增第二套项目适配规则目录。
- 禁止在可提交通用文件中硬编码目标项目真实路径。
- 禁止多个项目共享同一个 `{project_id}` 目录。
- 禁止把项目运行记录写入项目知识正文。
