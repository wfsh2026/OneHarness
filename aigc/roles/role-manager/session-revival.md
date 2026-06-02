# 角色会话复活规则

## 结论

角色会话复活依赖运行时自身的会话能力。Tharness 不复制运行时的完整会话、工具调用、推理链路或 transcript 内容，也不在通用层维护项目会话索引。

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
- Tharness 通用层不保存项目会话索引。

只有跨机器、CI、临时容器、清理策略风险或审计归档时，才允许保存运行时 transcript 的镜像位置。镜像是可选扩展，不是默认复活路径。

## 索引位置

默认不写入索引。需要继续既有角色任务时，优先使用当前运行时提供的会话恢复能力；如果运行时无法定位原会话，必须判定为不可真复活。

## 最小运行时标识

判断能否复活时只关心定位原运行时会话所需的字段：

- `runtime`：运行时类型，例如 `claude-code`、`codex-desktop`、`codex-cli`。
- `role_id`：角色库中的角色标识。
- `task_id`：角色管理员派发的任务标识。
- `session_id`：运行时原始会话 ID。
- `agent_id`：运行时子角色 ID；只有 subagent / worker agent 需要。
- `status`：当前运行时返回或用户确认的会话状态。
- `mirror_ref`：可选 transcript 镜像位置；默认为空。

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

1. 从当前运行时、用户提供信息或当前线程上下文取得候选 `session_id`。
2. 需要 subagent 复活时，同时取得原 `agent_id`。
3. 如果缺少运行时必需的 `session_id` 或 `agent_id`，必须判定为不可真复活。

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
- 会话索引：默认 `无`。
- 原始会话标识：`session_id` 或 `无`。
- 原始子角色标识：`agent_id` 或 `无`。
- 继续目标：本次追加给原运行时会话的目标。

## 状态说明

角色管理员回收结果后，只在本轮交付中说明原会话是否可继续、是否不可定位以及下一步需要的运行时标识。

## 禁止

- 禁止没有运行时原始 `session_id` 时声称已复活角色会话。
- 禁止需要 subagent 的运行时在缺少原 `agent_id` 时声称已复活子角色。
- 禁止把新建 AI 的摘要继承称为复活。
- 禁止默认复制完整 transcript 到 Tharness 通用层。
- 禁止把真实项目会话索引写入可提交的 Tharness 通用层。
