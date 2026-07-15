# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`4.8.0`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `role-dispatch` | 角色管理员调度 | active | `../roles/INDEX.md` | 1.2.0 | 所有用户请求先由角色管理员接收；默认只派发一个主执行角色并使用最小任务包，只有跨专业、高风险独立验证或写入冲突时条件式补派。 |
| `role-library` | 角色库 | active | `../roles/INDEX.md` | 3.3.0 | 维护当前有效角色边界，并以单主角色、渐进读取、条件式补派和风险触发验证组成低消耗完整开发闭环，同时保留 POE 领域任务派发与角色技能入口。 |
| `2d-ui-art-production` | 2D UI 图片绘制 | active | `../roles/2d-ui-artist/RULE.md` | 1.2.2 | 角色标签：实习；需要根据任务描述和可选项目参考图风格绘制、重绘或补齐图标、按钮底图、面板、徽章、头像框、弹窗装饰、HUD 图形、完整界面效果图、整屏流程稿或 UI 状态变体图片，并按正式 Sprite 规格交付透明资源和异常清单。 |
| `2d-game-asset-production` | 2D 游戏资源绘制 | active | `../roles/2d-game-asset-artist/RULE.md` | 1.0.1 | 角色标签：实习；需要根据任务描述、用户确认样张、设计文档或项目参考资源绘制、重绘或补齐角色或怪物精灵、装备图标、物品图标、地图对象图标、掉落图标、资源点图标、静态 VFX 帧或非 UI 游戏静态资源。 |
| `ui-asset-slicing` | UI 素材拆分 | active | `../roles/ui-asset-slicer/RULE.md` | 1.0.0 | 角色标签：实习；需要将已绘制 UI 正式稿或多帧动画帧表拆分为可接入透明素材，并维护对齐、九宫格、manifest 和验收说明。 |
| `intern-feature-design` | 实习功能案设计 | active | `../roles/intern-feature-designer/RULE.md` | 1.0.0 | 角色标签：实习；需要拆分阶段、功能案、任务包建议、依赖契约、验收标准、读取写入范围或待确认项。 |
| `intern-engine-architecture-development` | 实习工程架构开发 | active | `../roles/intern-engine-architecture-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现启动入口、流程路由、全局服务、配置加载基础、错误处理、存档骨架、调试骨架或工程规范。 |
| `intern-ui-development` | 实习 UI 开发 | active | `../roles/intern-ui-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现 UI 界面、控件层级、素材接入、运行时文字、交互状态、空态、禁用态、错误态或前台表现。 |
| `intern-gameplay-systems-development` | 实习玩法系统开发 | active | `../roles/intern-gameplay-systems-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现非战斗逐帧玩法系统、成长、背包、装备、交易、区域、资源点、传送、推荐或对应配置。 |
| `intern-combat-development` | 实习战斗开发 | active | `../roles/intern-combat-developer/RULE.md` | 1.0.0 | 角色标签：实习；需要实现战斗运行时、战斗角色属性、敌人行为、技能请求、预警、伤害、撤退、失败、胜利或战斗结算。 |
| `poe-domain-support` | poe 小助手 | active | `../roles/poe-helper/RULE.md` | 1.1.0 | 需要处理 Path of Exile / Path of Exile 2、POE 补丁、MOD、modes 落地、GGPK、bundle、VisualGGPK、交易接口、通货价格、游戏安装包、内容包内部索引、补丁工具风险分析或 POE 项目知识沉淀。 |
| `intern-version-feature-analysis` | 实习版本功能分析 | active | `../roles/intern-version-feature-analyst/RULE.md` | 1.0.0 | 角色标签：实习；需要从一个或多个 Git 仓库的提交、merge、rename 和 diff 证据生成版本功能目录审核文档，确认后再生成开发功能文档。 |
| `version-feature-scan` | 版本功能扫描 | active | `../../tools/version-feature-scan/version_feature_scan.py` | 1.0.0 | 需要预检仓库和 Git 引用，以 dry-run 或正式模式提取版本证据，并输出功能目录审核稿与带 commit、file、confidence 的结构化摘要。 |
| `role-browser-ui` | 本地角色管理器 | active | `../../tools/tharness.py` | 1.1.0 | 需要在仅监听 127.0.0.1 的深色页面中按配置成熟度置信度浏览、搜索和筛选角色，按需查看规则、技能与工具索引，并通过冲突保护安全编辑注册角色的 RULE.md。 |
| `session-role-marker` | 会话角色标识 | active | `../roles/common/session-visible-state.md` | 1.0.0 | 主会话正式输出展示当前角色、主要职责和工作依据；用户可见当前角色固定为角色管理员，被派发角色只能出现在派发、依据、回收或内部记录中。 |
| `role-session-revival` | 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 2.0.0 | 需要继续、唤醒、恢复或追溯已派发角色任务；Tharness 不保存项目会话索引，复活必须恢复运行时原 `session_id`；Claude Code subagent 还必须恢复原 `agent_id`。 |
| `issue-routing` | 写入位置路由 | active | `../roles/role-manager/issue-routing.md` | 1.0.1 | 候选问题、候选知识和规则变化统一由角色管理员按本入口选择唯一写入位置。 |
| `capability-evolution` | AIGC 能力演化 | active | `../roles/tharness-maintainer/RULE.md` | 1.0.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 1.0.2 | 需要检索跨项目通用架构知识；写入位置先由 `issue-routing` 判定。 |
| `knowledge-layering` | 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 1.0.0 | 需要拆分过大的规则、知识页、说明文档或能力入口。 |
| `tharness-self-check` | Tharness 结构自检 | active | `../../tools/tharness.py` | 2.1.0 | 需要检查入口、元数据、wiki 索引、角色库、派发页、能力索引、机器注册源、自检配置、会话角色标识或结构边界是否一致。 |
| `capability-registry-consistency` | 角色能力注册一致性 | active | `registry.yaml` | 1.0.0 | 需要用单一机器注册源发现角色或能力只接入目录、索引、派发页、自检配置其中一部分的半接入状态。 |
| `project-anchor-launch` | 项目锚点启动 | active | `../../tools/tharness.py` | 1.0.1 | 需要在指定项目目录快速部署轻量 `.tharness/` 启动锚点和目标项目根目录 `AGENTS.md` 桥接入口，或不复制主工程直接输出目标项目与 THarness 主工程绑定的启动包。 |
| `visual-project-binder` | 可视化项目绑定 | active | `../../THarness-Binder.exe` | 1.0.4 | 需要直接启动深色圆角桌面 exe，选择目标项目文件夹、预览 `.tharness/` 和 `AGENTS.md` 绑定结果，并确认把当前 THarness 主工程绑定到该项目。 |
| `role-self-check-trigger` | 自检触发规则 | active | `../roles/tharness-maintainer/skills/self-check.md` | 1.0.0 | Tharness 自身改动影响 AIGC 文档、角色规则、配置、工具或准备交付时。 |
| `index-sync` | Wiki 索引同步 | active | `../../tools/tharness.py` | 1.0.0 | 需要按扫描结果校验或写回 `AIGC/wiki/index.yaml` 页面清单。 |
| `self-check-planner` | 自检命令规划 | active | `../../tools/tharness.py` | 1.1.0 | 需要按变更路径确定自检命令，并使用当前运行中的 Python 解释器生成可直接执行的命令。 |
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
