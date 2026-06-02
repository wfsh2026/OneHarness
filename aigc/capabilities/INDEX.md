# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`4.3.4`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `role-dispatch` | 角色管理员调度 | active | `../roles/INDEX.md` | 1.1.1 | 所有用户请求先由角色管理员接收，角色管理员确认目标、边界和验证方式后，通过 SubAgent 或全新会话派发具体角色；主会话不得读取执行角色能力资料。 |
| `role-library` | 角色库 | active | `../roles/INDEX.md` | 3.1.0 | 维护当前有效角色边界、角色标签、角色添加时间、允许读取、允许写入、禁止范围、调用方式、角色资料、主会话能力隔离、批量视觉资源派发、实习开发角色派发、正式资源规格回收规则和多帧动画素材拆分边界。 |
| `2d-ui-art-production` | 2D UI 图片绘制 | active | `../roles/2d-ui-artist/RULE.md` | 1.2.2 | 角色标签：实习；需要根据任务描述和可选项目参考图风格绘制、重绘或补齐图标、按钮底图、面板、徽章、头像框、弹窗装饰、HUD 图形、完整界面效果图、整屏流程稿或 UI 状态变体图片，并按正式 Sprite 规格交付透明资源和异常清单。 |
| `2d-game-asset-production` | 2D 游戏资源绘制 | active | `../roles/2d-game-asset-artist/RULE.md` | 1.0.1 | 角色标签：实习；需要根据任务描述、用户确认样张、设计文档或项目参考资源绘制、重绘或补齐角色或怪物精灵、装备图标、物品图标、地图对象图标、掉落图标、资源点图标、静态 VFX 帧或非 UI 游戏静态资源。 |
| `intern-feature-design` | 实习功能案设计 | active | `../roles/intern-feature-designer/RULE.md` | 1.0.0 | 角色标签：实习；需要拆分阶段、功能案、任务包建议、依赖契约、验收标准、读取写入范围或待确认项。 |
| `intern-engine-architecture-development` | 实习工程架构开发 | active | `../roles/intern-engine-architecture-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现启动入口、流程路由、全局服务、配置加载基础、错误处理、存档骨架、调试骨架或工程规范。 |
| `intern-ui-development` | 实习 UI 开发 | active | `../roles/intern-ui-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现 UI 界面、控件层级、素材接入、运行时文字、交互状态、空态、禁用态、错误态或前台表现。 |
| `intern-gameplay-systems-development` | 实习玩法系统开发 | active | `../roles/intern-gameplay-systems-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现非战斗逐帧玩法系统、成长、背包、装备、交易、区域、资源点、传送、推荐或对应配置。 |
| `intern-combat-development` | 实习战斗开发 | active | `../roles/intern-combat-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现战斗运行时、战斗角色属性、敌人行为、技能请求、预警、伤害、撤退、失败、胜利或战斗结算。 |
| `session-role-marker` | 会话角色标识 | active | `../roles/common/session-visible-state.md` | 1.0.0 | 主会话正式输出展示当前角色、主要职责和工作依据；用户可见当前角色固定为角色管理员，被派发角色只能出现在派发、依据、回收或内部记录中。 |
| `role-session-revival` | 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 2.0.0 | 需要继续、唤醒、恢复或追溯已派发角色任务；Tharness 不保存项目会话索引，复活必须恢复运行时原 `session_id`；Claude Code subagent 还必须恢复原 `agent_id`。 |
| `issue-routing` | 写入位置路由 | active | `../roles/role-manager/issue-routing.md` | 1.0.1 | 候选问题、候选知识和规则变化统一由角色管理员按本入口选择唯一写入位置。 |
| `capability-evolution` | AIGC 能力演化 | active | `../roles/tharness-maintainer/RULE.md` | 1.0.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 1.0.2 | 需要检索跨项目通用架构知识；写入位置先由 `issue-routing` 判定。 |
| `knowledge-layering` | 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 1.0.0 | 需要拆分过大的规则、知识页、说明文档或能力入口。 |
| `tharness-self-check` | Tharness 结构自检 | active | `../../tools/tharness.py` | 2.0.0 | 需要从工具入口检查入口、元数据、wiki 索引、角色库、会话角色标识或结构边界是否存在问题。 |
| `project-anchor-launch` | 项目锚点启动 | active | `../../tools/tharness.py` | 1.0.1 | 需要在指定项目目录快速部署轻量 `.tharness/` 启动锚点和目标项目根目录 `AGENTS.md` 桥接入口，或不复制主工程直接输出目标项目与 THarness 主工程绑定的启动包。 |
| `visual-project-binder` | 可视化项目绑定 | active | `../../THarness-Binder.exe` | 1.0.4 | 需要直接启动深色圆角桌面 exe，选择目标项目文件夹、预览 `.tharness/` 和 `AGENTS.md` 绑定结果，并确认把当前 THarness 主工程绑定到该项目。 |
| `role-self-check-trigger` | 自检触发规则 | active | `../roles/tharness-maintainer/skills/self-check.md` | 1.0.0 | Tharness 自身改动影响 AIGC 文档、角色规则、配置、工具或准备交付时。 |
| `index-sync` | Wiki 索引同步 | active | `../../tools/tharness.py` | 1.0.0 | 需要按扫描结果校验或写回 `AIGC/wiki/index.yaml` 页面清单。 |
| `self-check-planner` | 自检命令规划 | active | `../../tools/tharness.py` | 1.0.0 | 需要按变更路径确定本轮应该运行哪些自检命令。 |
| `game-design-method-cards` | 游戏策划方法卡 | active | `../roles/role-manager/game-design/method-cards/INDEX.md` | 1.0.1 | 需要把游戏设定、玩法想法或体验目标转成可开发、可反馈、可验证的策划结构。 |

## 状态说明

| 状态 | 含义 |
| --- | --- |
| `active` | 当前可直接按角色规则或工具入口使用。 |
| `candidate` | 候选能力，只能作为参考或待导入结构，不能当强规则执行。 |

## 维护规则

- 新增或删除能力时，必须更新本索引。
- 改变能力行为时，必须更新 `VERSION.md` 和 `CHANGELOG.md`。
- 候选能力不能当强规则执行。
- 能力入口必须能通过索引链路访问。
