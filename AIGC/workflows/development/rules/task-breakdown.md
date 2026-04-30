---
id: workflow-development-task-breakdown
title: 开发任务拆解规则
workflow: development
phase: task-breakdown
read_when: 需要把目标拆成可执行开发任务。
updated: 2026-04-30
---

# 开发任务拆解规则

主程负责把用户目标和总策划案拆成项目内任务包。任务包必须能让全新会话在不依赖历史对话的情况下恢复上下文。

## 主任务必须满足

- 一个任务对应一个清晰目标。
- 写入范围明确。
- 文件归属明确。
- 输入和输出明确。
- 成功标准可验证。
- 包含有效输入和无效输入验证。
- 能追溯到用户请求、策划案或已确认决策。
- 总策划案入口明确；子任务只引用必要章节。

## 项目任务包

任务包必须写入目标项目适配层，推荐结构：

```text
{project_aigc_root}/tasks/{task_id}/TASK.md
{project_aigc_root}/tasks/{task_id}/PLAN.md
{project_aigc_root}/tasks/{task_id}/ASSIGNMENTS.md
{project_aigc_root}/tasks/{task_id}/subtasks/{role}-{subtask_id}.md
{project_aigc_root}/tasks/{task_id}/verification.md
{project_aigc_root}/tasks/{task_id}/wiki-candidates.md
```

如果项目适配层不存在，先按 `../../../projects/rules/project-wiki-bootstrap.md` 建立或说明阻塞。

## 子任务必须满足

- 指定一个主执行角色。
- 指定全新 SubAgent 或全新会话执行。
- 指定任务文档入口。
- 指定允许读取的总策划案章节、项目 wiki 页面、源码入口和资源入口。
- 指定允许修改的文件、目录或模块。
- 指定禁止修改范围。
- 指定接口契约，包括事件、数据结构、状态流、资源引用或调用边界。
- 指定成功标准、有效输入验证、无效输入验证和回归检查。
- 指定交付物、验证记录和知识候选输出要求。

## 禁止

- 把模糊目标包装成开发任务。
- 把多个无关目标塞进同一个任务。
- 为一次性实现制造复杂抽象。
- 把未确认事项写成任务事实。
- 让多个执行者同时写入同一个文件。
- 让子任务依赖主程会话里的隐式上下文。
- 在子任务中复制整份总策划案或整份 wiki。

## 探索型任务

如果任务是验证新功能、新交互或新方向，必须额外写明：

- 待验证假设。
- 验证方式。
- 成立后写入位置。
- 不成立时的记录位置。

## 输出

主任务使用 `../templates/development-task-request.md`。
子任务使用 `../templates/subtask-assignment.md`。
