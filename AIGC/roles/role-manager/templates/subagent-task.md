# SubAgent 任务包模板

本模板用于角色管理员派发具体角色任务。任务包必须让执行角色在不依赖主会话隐式记忆的情况下开始工作。

```text
## 角色

- 角色显示名：{被派发角色}
- 角色规则入口：{AIGC/roles/.../RULE.md 或项目适配包角色 RULE.md}
- 通用规则入口：AIGC/roles/common/RULE.md
- 会话模式：{runtime-resume / runtime-mirror-resume / summary-rebuild / create-new}
- 会话索引：{AIGC/project-adapters/{project_id}/runs/sessions/{session_file} 或 无}
- 原始会话标识：{session_id 或 无}
- 原始子角色标识：{agent_id 或 无}

## 任务目标

{本次只完成的一件事}

## 会话复活

{当会话模式为 runtime-resume 或 runtime-mirror-resume 时，本段只写追加给原 session_id 和必要 agent_id 的继续目标。原会话不可唤醒时必须回报角色管理员，不得创建新会话冒充复活。summary-rebuild 只能说明为重建，不能称为复活。}

## 背景和已确认事实

- {用户确认输入}
- {项目适配包或通用规则中已确认的事实}

## 允许读取

- {规则、项目知识、源码、资源或文档入口}

## 允许写入

- {文件、目录或产物范围}

## 禁止范围

- {不能读取、不能写入、不能重构或不能改派的范围}

## 接口契约或交接边界

{与其他角色、模块或产物的边界}

## 成功标准

- {可判断完成的标准}

## 验证要求

- {必须运行或说明无法运行的验证}

## 输出格式

使用角色 `RULE.md` 指定的输出模板。具体执行角色默认使用 `AIGC/roles/developer/templates/implementation-delivery.md`，验证审查员默认使用 `AIGC/roles/qa-verification/templates/verification-report.md`。
```

## 使用要求

- 同一文件同一时间只能派给一个写入角色。
- 写入范围不明确时不得派发。
- 需要项目事实时，先按 `../project-adapter-routing.md` 命中项目适配包。
- 需要继续既有角色任务时，先按 `../session-revival.md` 查找可唤醒原会话。
