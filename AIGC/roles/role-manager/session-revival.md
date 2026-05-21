# 角色会话复活规则

## 结论

角色会话复活依赖运行时自身的会话能力。Tharness 不复制运行时的完整会话、工具调用、推理链路或 transcript 内容，只维护能定位原会话的最小索引。

复活指恢复运行时原始会话继续工作。读取摘要后新建 AI、fork 会话或重建上下文都不是复活。

## 触发条件

- 用户要求继续、唤醒、恢复或接着上次的角色任务。
- 角色管理员需要向同一角色追加增量任务。
- 已派发角色任务需要从暂停、阻塞或完成后继续。
- 需要判断一个角色任务能否回到原运行时会话。

## 事实源

运行时原始会话是唯一事实源：

- Claude Code / Claude SDK 由自身 session transcript 保存上下文、工具调用和结果。
- Codex 由当前运行环境保存 agent 会话上下文和工具结果。
- Tharness 项目适配包只保存查找索引，不保存完整会话副本。

只有跨机器、CI、临时容器、清理策略风险或审计归档时，才允许保存运行时 transcript 的镜像位置。镜像是可选扩展，不是默认复活路径。

## 索引位置

角色会话索引只能写入目标项目适配包运行态目录：

```text
AIGC/project-adapters/{project_id}/runs/sessions/
```

`AIGC/project-adapters/` 必须被 Git 忽略。可提交的 Tharness 通用层只保存规则和索引模板，不保存真实项目会话索引或 transcript。

## 最小索引字段

每条索引只保存定位原运行时会话所需的字段：

- `runtime`：运行时类型，例如 `claude-code`、`codex-desktop`、`codex-cli`。
- `project_id`：所属项目适配包。
- `role_id`：角色库或项目适配包中的角色标识。
- `task_id`：角色管理员派发的任务标识。
- `session_id`：运行时原始会话 ID。
- `agent_id`：运行时子角色 ID；只有 subagent / worker agent 需要。
- `status`：`active`、`paused`、`blocked`、`completed`、`archived` 或 `lost`。
- `updated_at`：最近一次索引更新时间。
- `mirror_ref`：可选 transcript 镜像位置；默认为空。

索引模板见 `templates/session-index.yaml`。

## 状态含义

| 状态 | 含义 |
| --- | --- |
| `active` | 原运行时会话仍可继续接收任务。 |
| `paused` | 原运行时会话暂挂，可尝试唤醒。 |
| `blocked` | 原运行时会话等待输入、权限、工具或用户确认。 |
| `completed` | 原任务已完成；用户明确继续同一任务时可尝试复活。 |
| `archived` | 原运行时会话已归档；默认不复活。 |
| `lost` | 原运行时会话不可定位或不可唤醒；不得伪装成复活。 |

## 复活类型

| 类型 | 是否是真复活 | 判断 |
| --- | --- | --- |
| `runtime-resume` | 是 | 使用运行时原始 `session_id` 恢复；subagent 还必须使用原 `agent_id`。 |
| `runtime-mirror-resume` | 是 | 先恢复原始 transcript 或外部 SessionStore，再使用原 `session_id`；subagent 还必须使用原 `agent_id`。 |
| `summary-rebuild` | 否 | 读取摘要、交付记录或用户说明后新建会话。 |

## 查找顺序

1. 按 `project-adapter-routing.md` 命中 `project_id`。
2. 读取 `AIGC/project-adapters/{project_id}/runs/sessions/INDEX.md`。
3. 按 `runtime`、`role_id`、`task_id` 和 `status` 查找候选索引。
4. 命中多个候选时，优先选择状态为 `active`、`paused` 或 `blocked` 且 `updated_at` 最新的索引。
5. 如果缺少运行时必需的 `session_id` 或 `agent_id`，必须判定为不可真复活。

## Claude Code

Claude Code 主会话复活需要原 `session_id`。

Claude Code subagent 复活需要原 `session_id` 和原 `agent_id`。自定义 agent 还需要运行时能加载同一份 agent definition。

以下情况不是 Claude Code 真复活：

- 只恢复主会话，但无法定位原 subagent `agent_id`。
- 使用 `--fork-session`、`/branch` 或 fork subagent。
- 新建 subagent 后喂入旧摘要。
- 原 transcript 已清理、丢失，且没有可用镜像恢复。

## Codex

Codex 运行时如果能恢复原 agent 会话，则记录对应 `runtime`、`session_id` 和需要的 `agent_id`。

如果运行时只支持读取上下文摘要后重新派发任务，只能标记为 `summary-rebuild`，不得称为复活。

## 任务包要求

涉及复活的 SubAgent 任务包只需要额外说明：

- 会话模式：`runtime-resume`、`runtime-mirror-resume`、`summary-rebuild` 或 `create-new`。
- 会话索引：`AIGC/project-adapters/{project_id}/runs/sessions/{session_file}` 或 `无`。
- 原始会话标识：`session_id` 或 `无`。
- 原始子角色标识：`agent_id` 或 `无`。
- 继续目标：本次追加给原运行时会话的目标。

## 索引更新

角色管理员回收结果后，只更新最小索引：

- 更新 `status`。
- 更新 `updated_at`。
- 运行时返回新的 `session_id` 或 `agent_id` 时同步索引。
- 原会话不可定位或不可唤醒时标记 `lost`。

任务进度、验证结果、交付物、待确认问题和知识沉淀应写入对应任务记录、交付记录或项目知识，不写入会话复活索引。

## 禁止

- 禁止没有运行时原始 `session_id` 时声称已复活角色会话。
- 禁止需要 subagent 的运行时在缺少原 `agent_id` 时声称已复活子角色。
- 禁止把新建 AI 的摘要继承称为复活。
- 禁止默认复制完整 transcript 到 Tharness 通用层。
- 禁止把真实项目会话索引写入可提交的 Tharness 通用层。
