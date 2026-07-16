# AIGC 能力索引

本目录记录当前 AIGC 可用能力，只保存路由、状态和版本信息，不保存具体项目事实。

当前系统版本：`6.0.0`

## 当前能力

| capability_id | 名称 | 状态 | 入口 | 版本 | read_when |
| --- | --- | --- | --- | --- | --- |
| `role-dispatch` | 角色管理员调度 | active | `../roles/INDEX.md` | 1.3.0 | 按收益决定是否委派；主会话可完成低风险、小型、只读或单域任务，并按风险选择轻量或完整审计任务包。 |
| `role-library` | 角色库 | active | `../roles/INDEX.md` | 4.0.0 | 以机器注册源验证正式角色、路由和工具契约；已发布的四个旧开发角色入口已删除。 |
| `project-development` | 项目开发 | active | `../roles/project-developer/RULE.md` | 2.0.0 | 由项目开发者及 architecture、ui、gameplay、combat 独立领域正式承载全部项目开发能力。 |
| `2d-ui-art-production` | 2D UI 图片绘制 | active | `../roles/2d-ui-artist/RULE.md` | 1.2.2 | 角色标签：实习；需要根据任务描述和可选项目参考图风格绘制、重绘或补齐图标、按钮底图、面板、徽章、头像框、弹窗装饰、HUD 图形、完整界面效果图、整屏流程稿或 UI 状态变体图片，并按正式 Sprite 规格交付透明资源和异常清单。 |
| `2d-game-asset-production` | 2D 游戏资源绘制 | active | `../roles/2d-game-asset-artist/RULE.md` | 1.0.1 | 角色标签：实习；需要根据任务描述、用户确认样张、设计文档或项目参考资源绘制、重绘或补齐角色或怪物精灵、装备图标、物品图标、地图对象图标、掉落图标、资源点图标、静态 VFX 帧或非 UI 游戏静态资源。 |
| `ui-asset-slicing` | UI 素材拆分 | active | `../roles/ui-asset-slicer/RULE.md` | 1.0.0 | 角色标签：实习；需要将已绘制 UI 正式稿或多帧动画帧表拆分为可接入透明素材，并维护对齐、九宫格、manifest 和验收说明。 |
| `intern-feature-design` | 实习功能案设计 | active | `../roles/intern-feature-designer/RULE.md` | 1.0.0 | 角色标签：实习；需要拆分阶段、功能案、任务包建议、依赖契约、验收标准、读取写入范围或待确认项。 |
| `poe-domain-support` | poe 小助手 | active | `../roles/poe-helper/RULE.md` | 1.1.0 | 需要处理 Path of Exile / Path of Exile 2、POE 补丁、MOD、modes 落地、GGPK、bundle、VisualGGPK、交易接口、通货价格、游戏安装包、内容包内部索引、补丁工具风险分析或 POE 项目知识沉淀。 |
| `intern-version-feature-analysis` | 实习版本功能分析 | active | `../roles/intern-version-feature-analyst/RULE.md` | 1.0.0 | 角色标签：实习；需要从一个或多个 Git 仓库的提交、merge、rename 和 diff 证据生成版本功能目录审核文档，确认后再生成开发功能文档。 |
| `version-feature-scan` | 版本功能扫描 | active | `../../tools/version-feature-scan/version_feature_scan.py` | 1.0.0 | 需要预检仓库和 Git 引用，以 dry-run 或正式模式提取版本证据，并输出功能目录审核稿与带 commit、file、confidence 的结构化摘要。 |
| `role-browser-ui` | 本地角色管理器 | active | `../../tools/tharness.py` | 1.2.0 | 按证据成熟度浏览角色；RULE 保存要求显式维护模式、差异预览、影响入口、版本策略、自检计划和冲突确认。 |
| `session-role-marker` | 会话角色标识 | active | `../roles/common/session-visible-state.md` | 1.0.0 | 主会话正式输出展示当前角色、主要职责和工作依据；用户可见当前角色固定为角色管理员，被派发角色只能出现在派发、依据、回收或内部记录中。 |
| `role-session-revival` | 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 2.0.0 | 需要继续、唤醒、恢复或追溯已派发角色任务；Tharness 不保存项目会话索引，复活必须恢复运行时原 `session_id`；Claude Code subagent 还必须恢复原 `agent_id`。 |
| `issue-routing` | 写入位置路由 | active | `../roles/role-manager/issue-routing.md` | 1.0.1 | 候选问题、候选知识和规则变化统一由角色管理员按本入口选择唯一写入位置。 |
| `capability-evolution` | AIGC 能力演化 | active | `../roles/tharness-maintainer/RULE.md` | 1.0.0 | 需要分析外部 harness、提取可复用能力、更新能力索引或版本记录。 |
| `generic-architecture-wiki` | 通用架构 Wiki | active | `../wiki/INDEX.md` | 1.0.2 | 需要检索跨项目通用架构知识；写入位置先由 `issue-routing` 判定。 |
| `knowledge-layering` | 知识分层 | active | `../wiki/architecture/knowledge-layering.md` | 1.0.0 | 需要拆分过大的规则、知识页、说明文档或能力入口。 |
| `tharness-self-check` | Tharness 结构自检 | active | `../../tools/tharness.py` | 2.2.0 | 检查入口、索引、schema v2 注册源、工具契约、角色/路由、输出与边界结构。 |
| `capability-registry-consistency` | 角色能力注册一致性 | active | `registry.yaml` | 2.0.0 | schema v2 机器事实源维护 owner、成熟度、契约状态、最后验证、Eval 和弃用迁移，并验证衍生索引；旧 7/2 字段读取器必须迁移。 |
| `project-anchor-launch` | 项目锚点启动 | active | `../../tools/tharness.py` | 1.0.1 | 需要在指定项目目录快速部署轻量 `.tharness/` 启动锚点和目标项目根目录 `AGENTS.md` 桥接入口，或不复制主工程直接输出目标项目与 THarness 主工程绑定的启动包。 |
| `visual-project-binder` | 可视化项目绑定 | active | `../../THarness-Binder.exe` | 1.0.4 | 需要直接启动深色圆角桌面 exe，选择目标项目文件夹、预览 `.tharness/` 和 `AGENTS.md` 绑定结果，并确认把当前 THarness 主工程绑定到该项目。 |
| `role-self-check-trigger` | 自检触发规则 | active | `../roles/tharness-maintainer/skills/self-check.md` | 1.0.0 | Tharness 自身改动影响 AIGC 文档、角色规则、配置、工具或准备交付时。 |
| `index-sync` | Wiki 索引同步 | active | `../../tools/tharness.py` | 1.0.0 | 需要按扫描结果校验或写回 `AIGC/wiki/index.yaml` 页面清单。 |
| `self-check-planner` | 自检命令规划 | active | `../../tools/tharness.py` | 1.1.0 | 需要按变更路径确定自检命令，并使用当前运行中的 Python 解释器生成可直接执行的命令。 |
| `game-design-method-cards` | 游戏策划方法卡 | active | `../roles/role-manager/game-design/method-cards/INDEX.md` | 1.0.1 | 需要把游戏设定、玩法想法或体验目标转成可开发、可反馈、可验证的策划结构。 |
| `deterministic-behavior-eval` | 确定性行为策略评测 | active | `../../tools/tharness.py` | 1.1.0 | 以机器可读策略表运行正向、负向和变异场景；不调用在线模型，也不代表真实模型行为评测。 |

## 状态说明

| 状态 | 含义 |
| --- | --- |
| `active` | 当前可直接按角色规则或工具入口使用。 |
| `candidate` | 候选能力，只能作为参考或待导入结构，不能当强规则执行。 |
| `deprecated` | 仅兼容旧引用；必须声明替代能力，新任务不得优先路由。 |

## 维护规则

- 新增或删除能力时，必须更新本索引。
- 改变能力行为时，必须更新 `VERSION.md` 和 `CHANGELOG.md`。
- 候选能力不能当强规则执行。
- 能力入口必须能通过索引链路访问。
