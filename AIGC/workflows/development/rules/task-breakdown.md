---
id: workflow-development-task-breakdown
title: 开发任务拆解规则
workflow: development
phase: task-breakdown
read_when: 需要把目标拆成可执行开发任务。
updated: 2026-04-30
---

# 开发任务拆解规则

主程负责把用户目标和项目 wiki 中的策划页面拆成项目 wiki 开发任务页。任务页必须能让全新会话在不依赖历史对话的情况下恢复上下文。

## 主程评审

拆解前必须先评审输入页面，结果只能是：

- `ready-for-breakdown`：目标、边界、成功标准和验证方式足够明确，可以拆任务。
- `needs-design`：缺少核心体验、范围、非目标或验收方式，回到策划工作流补项目 wiki。
- `blocked`：缺少目标项目事实、技术路线、文件归属或接口契约，先补项目 wiki 或向用户确认。

## 主任务必须满足

- 一个任务对应一个清晰目标。
- 写入范围明确。
- 文件归属明确。
- 输入和输出明确。
- 成功标准可验证。
- 包含有效输入和无效输入验证。
- 能追溯到用户请求、项目 wiki 策划页面或已确认决策。
- 策划页面入口明确；子任务只引用必要页面和章节。

## 项目 Wiki 开发任务页

任务拆解必须写入目标项目 wiki，推荐结构：

```text
{project_wiki_root}/development/tasks/{task_id}.md
{project_wiki_root}/development/subtasks/{role}-{subtask_id}.md
{project_wiki_root}/development/contracts/{contract_id}.md
```

如果项目适配层不存在，先按 `../../../projects/rules/project-wiki-bootstrap.md` 建立或说明阻塞。

运行过程、验证输出、失败尝试和候选知识审核记录不写入项目 wiki 正文，应写入运行记录或交付物。

## 子任务必须满足

- 指定一个主执行角色。
- 指定全新 SubAgent 或全新会话执行。
- 指定项目 wiki 子任务入口。
- 指定允许读取的项目 wiki 策划页面、任务页、接口契约、源码入口和资源入口。
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
- 在子任务中复制整份策划页面或整份 wiki。

## 探索型任务

如果任务是验证新功能、新交互或新方向，必须额外写明：

- 待验证假设。
- 验证方式。
- 成立后写入位置。
- 不成立时的记录位置。

## 输出

主任务使用 `../templates/development-task-request.md` 写入项目 wiki 的 `development/tasks/`。
子任务使用 `../templates/subtask-assignment.md` 写入项目 wiki 的 `development/subtasks/`。
