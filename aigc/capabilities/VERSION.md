# AIGC 版本

current_version: 4.5.0

## 版本级别

| 级别 | 触发条件 |
| --- | --- |
| patch | 修正文档、索引、链接、模板、测试、自检提示或规则表述；收紧既有规则但不破坏当前外部契约。 |
| minor | 新增可被角色管理员调用的能力、角色、工具命令或可选资料入口；现有入口和行为仍兼容。 |
| major | 仅当破坏当前外部契约时使用：改变默认启动入口、主会话可见字段含义、项目事实写入边界、CLI 命令名、必需配置结构，或删除仍被当前能力索引声明的 active 能力。 |

## 版本推进原则

- 当前整体重构后的基线版本为 `1.0.0`。
- 同一轮变更只产生一个系统版本，不因多个文件同步修改而连续叠加版本号。
- 能力条目版本只在该能力自身的可观察行为变化时更新；单纯迁移文件、修链接、补说明不单独提升能力版本。
- 能兼容现有入口的规则补充优先使用 patch。
- 不能因为目录整理、文档收敛或删除废弃记录直接提升 major。

## 当前版本范围

- 角色管理员默认入口。
- 角色库、通用角色最小规则和角色派发规则。
- SubAgent / 全新会话执行隔离规则。
- 角色会话复活运行时标识、查找、唤醒和失败处理规则。
- Claude Code 角色会话复活运行时标识字段。
- 通用架构 wiki。
- 能力索引、版本记录和变更记录。
- 结构自检 CLI、wiki 索引校验、自检命令规划、项目锚点启动和可视化项目绑定。
- 角色资料、方法卡和自检触发规则。
- 2D UI 绘图师实习标签、派发检索、完整界面视觉稿、批量资源绘制、资源绘制边界和正式 Sprite 规格交付要求。
- 2D 游戏资源绘制师实习标签、派发检索、非 UI 游戏静态资源绘制和透明精灵验收边界。
- UI 素材拆分师实习标签、多帧动画精灵表拆分、像素级对齐、透明边缘验收和正式目录清理规则。
- 实习功能案设计者、实习工程架构开发者、实习 UI 开发者、实习玩法系统开发者和实习战斗开发者的通用角色规则与派发检索。
- poe 小助手的通用角色规则、派发检索、modes 落地技能和目录与内容包分析技能。
- 角色管理员批量视觉资源流程、正式资源规格回收规则和替代隔离方式。
- 主会话能力隔离规则。
- 候选问题、候选知识和规则变化的唯一写入位置路由。

## 当前版本功能

| 功能 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 角色管理员调度 | active | `../roles/INDEX.md` | 所有用户请求先由角色管理员接收，角色管理员确认目标、边界和验证方式后，通过 SubAgent 或全新会话派发具体角色；主会话不得读取执行角色能力资料。 |
| 角色库 | active | `../roles/INDEX.md` | 维护当前有效角色边界、角色标签、角色添加时间、允许读取、允许写入、禁止范围、调用方式、主会话能力隔离、批量视觉资源流程、实习开发角色派发、POE 角色技能入口、正式资源规格回收规则和多帧动画素材拆分边界。 |
| 2D UI 图片绘制 | active | `../roles/2d-ui-artist/RULE.md` | 标签：实习；根据任务描述和可选项目参考图风格绘制、重绘或补齐 UI 图片资源、完整界面效果图、整屏流程稿和 UI 状态变体；没有风格参考时按描述生成；正式 Sprite 或图标必须按透明 PNG / RGBA、语义匹配、无背景污染、非占位、非预览图的规格交付。 |
| 2D 游戏资源绘制 | active | `../roles/2d-game-asset-artist/RULE.md` | 标签：实习；根据任务描述、用户确认样张、设计文档或项目参考资源绘制、重绘或补齐角色或怪物精灵、装备图标、物品图标、地图对象图标、掉落图标、资源点图标、静态 VFX 帧和非 UI 游戏静态资源。 |
| 实习功能案设计 | active | `../roles/intern-feature-designer/RULE.md` | 标签：实习；拆分阶段、功能案、任务包建议、依赖契约、验收标准、读取写入范围和待确认项，不直接实现代码、场景、资源、配置或测试。 |
| 实习工程架构开发 | active | `../roles/intern-engine-architecture-developer/RULE.md` | 标签：实习；实现启动入口、流程路由、全局服务、配置加载基础、错误处理、存档骨架、调试骨架和工程规范，不承接完整玩法、战斗或 UI 业务。 |
| 实习 UI 开发 | active | `../roles/intern-ui-developer/RULE.md` | 标签：实习；实现 UI 界面、控件层级、素材接入、运行时文字、交互状态、空态、禁用态、错误态和前台表现，不负责正式 UI 绘制或素材拆分。 |
| 实习玩法系统开发 | active | `../roles/intern-gameplay-systems-developer/RULE.md` | 标签：实习；实现非战斗逐帧玩法系统、成长、背包、装备、交易、区域、资源点、传送、推荐和对应配置，不承接战斗逐帧、UI 布局或正式素材绘制。 |
| 实习战斗开发 | active | `../roles/intern-combat-developer/RULE.md` | 标签：实习；实现战斗运行时、战斗角色属性、敌人行为、技能请求、预警、伤害、撤退、失败、胜利和战斗结算，不直接修改长期背包、成长或经济系统。 |
| poe 小助手 | active | `../roles/poe-helper/RULE.md` | 处理 Path of Exile / Path of Exile 2、POE 补丁、MOD、modes 落地、GGPK、bundle、VisualGGPK、交易接口、通货价格、游戏安装包、内容包内部索引、补丁工具风险分析和 POE 项目知识沉淀；具体项目事实只写入目标项目。 |
| 通用角色最小规则 | active | `../roles/common/RULE.md` | 所有角色共享的语言、事实、调度、写入、验证和交付规则。 |
| 执行角色通用规则 | active | `../roles/developer/RULE.md` | 具体执行角色默认继承的任务读取、写入和交付边界。 |
| wiki 管理员 | active | `../roles/wiki-manager/RULE.md` | 判断候选知识写入通用 wiki、本轮交付物或不写入。 |
| Tharness 能力维护员 | active | `../roles/tharness-maintainer/RULE.md` | 维护 Tharness 规则、角色库、入口机制、能力索引、自检工具和模板。 |
| UI 素材拆分师 | active | `../roles/ui-asset-slicer/RULE.md` | 标签：实习；将已绘制 UI 正式稿或多帧动画帧表拆分为开发可用透明素材，维护黑白底验收、像素级对齐、manifest、九宫格和接入说明边界。 |
| 会话角色标识 | active | `../roles/common/session-visible-state.md` | 主会话正式输出展示当前角色、职责和依据；用户可见当前角色固定为角色管理员。 |
| 角色会话复活 | active | `../roles/role-manager/session-revival.md` | 角色管理员继续已派发角色任务时，只按运行时原始会话能力定位 `session_id`；Claude Code subagent 必须同时命中原 `agent_id`，不可用时明确说明而不是新建会话冒充。 |
| 写入位置路由 | active | `../roles/role-manager/issue-routing.md` | 候选问题、候选知识和规则变化统一由角色管理员按本入口选择唯一写入位置。 |
| 游戏策划方法卡 | active | `../roles/role-manager/game-design/INDEX.md` | 角色管理员处理游戏策划讨论时调用的方法论、方法卡和输出模板。 |
| 通用架构 wiki | active | `../wiki/INDEX.md` | 保存跨项目可复用的项目架构搭建知识，用于低 token 架构检索。 |
| 结构自检 | active | `../../tools/tharness.py` | 从工具入口解析 THarness 根目录，用 `doctor`、`index --check` 和 `check` 检查入口、元数据、索引、角色库、会话角色标识和结构边界。 |
| 自检命令规划 | active | `../../tools/tharness.py` | 用 `self-check --path ... --delivery` 输出本轮应运行的自检命令。 |
| 项目锚点启动 | active | `../../tools/tharness.py` | 用 `project init --root ...` 在目标项目部署轻量 `.tharness/` 启动锚点和目标项目根目录 `AGENTS.md` 桥接入口，或用 `project start --root ...` 在不复制主工程的情况下输出目标项目与 THarness 主工程绑定的启动包。 |
| 可视化项目绑定 | active | `../../THarness-Binder.exe` | 直接打开 Rust 桌面工具，用深色圆角扁平化界面显示当前 THarness 主工程、目标项目文件夹选择、`.tharness/` 与 `AGENTS.md` 绑定预览、确认绑定和关闭按钮。 |

## 当前版本边界

- 默认入口是角色管理员。
- 主会话用户可见 `【当前角色】` 只能是 `角色管理员`；执行角色通过 SubAgent 或全新会话派发。
- 主会话只能读取角色管理员规则、通用规则、派发检索资料和必要的角色 `RULE.md`；执行角色 `skills/`、`tools/`、工具调用说明和其他能力资料只能由被派发执行角色在自己的会话中读取。
- 角色会话复活只允许恢复运行时原 `session_id`；Claude Code subagent 复活还必须恢复原 `agent_id`；原会话不可唤醒时不得把摘要继承或新建会话称为复活。
- Tharness 不默认保存完整会话、工具调用、推理链路或 transcript 内容；跨机器或审计场景只允许保存可选镜像引用。
- 多步骤执行方式由角色管理员基于角色库、用户输入、任务包允许读取入口和通用 wiki 组合任务包；批量视觉资源任务按缺口盘点、绘制派发、正式资源规格回收、异常清单、文档索引和链接校验组织。
- 验证、审查和交付判断由角色管理员和执行角色承担。
- 可提交的通用 AIGC 只保存通用角色、通用规则、通用 wiki、入口机制和模板。
- 候选内容写入位置只由 `../roles/role-manager/issue-routing.md` 判断；其他文件只引用该路由，不维护写入位置路由表。
- 2D UI 绘图师标签为实习；该角色只保存通用 UI 绘图方法和角色边界；任务包提供项目参考图、风格文档或用户参考图时按参考风格生成，没有风格参考时按描述生成；完整界面效果图和批量 UI 视觉资源任务必须由任务包提供资源规格、命名约定、风格参考读取顺序和覆盖策略；正式 Sprite 或图标不得以截屏切片、调试预览、黑白底检查图或扁平占位图交付。
- 2D 游戏资源绘制师标签为实习；该角色只保存通用游戏静态资源绘制方法和角色边界；任务包提供用户确认样张、项目资源、设计文档或风格文档时按参考风格生成，没有风格参考时按描述生成；透明精灵和批量游戏资源任务必须由任务包提供资源清单、资源规格、命名约定、风格参考读取顺序、写入目录和验收标准。
- UI 素材拆分师标签为实习；该角色处理多帧动画素材时必须保持固定源网格、统一缩放、统一画布、统一贴入偏移或 Pivot 约定，并用黑底或深色底验收白底残留；正式目录默认只保留可接入帧 PNG。
- 实习功能案设计者、实习工程架构开发者、实习 UI 开发者、实习玩法系统开发者和实习战斗开发者标签为实习；这些角色只保存通用开发职责边界，不保存具体项目事实；任务包必须提供目标项目的允许读取入口、允许写入范围、禁止范围、成功标准和验证要求。
- poe 小助手只保存 POE 领域任务的通用处理边界、modes 落地方法和目录与内容包分析方法，不保存具体补丁包路径、游戏安装目录、会话历史、内容包索引结果或本地实验结论；这些项目事实必须写入目标项目允许的知识库。
- 具体项目事实、项目知识、项目决策事实、项目专属角色和项目代码结构分析不得写入 THarness 通用层。
- 项目专属扩展不保存在 THarness 中，不保存具体项目代码路径、资源路径或历史决策事实到可提交通用层。
- 自检配置只保存通用检查入口、扫描范围、必需字段、会话角色允许值和结构边界规则，不保存目标项目事实。

## 当前版本验证结果

- 角色库入口可从 `../roles/INDEX.md` 命中。
- 主会话能力隔离规则可从 `../roles/common/RULE.md` 和 `../roles/role-manager/RULE.md` 命中。
- 2D UI 绘图师规则可从 `../roles/2d-ui-artist/RULE.md` 命中。
- 2D UI 绘图师派发检索可从 `../roles/role-manager/role-routing/2d-ui-artist.md` 命中。
- 2D 游戏资源绘制师规则可从 `../roles/2d-game-asset-artist/RULE.md` 命中。
- 2D 游戏资源绘制师派发检索可从 `../roles/role-manager/role-routing/2d-game-asset-artist.md` 命中。
- UI 素材拆分师规则可从 `../roles/ui-asset-slicer/RULE.md` 命中。
- UI 素材拆分师派发检索可从 `../roles/role-manager/role-routing/ui-asset-slicer.md` 命中。
- 实习功能案设计者规则可从 `../roles/intern-feature-designer/RULE.md` 命中。
- 实习功能案设计者派发检索可从 `../roles/role-manager/role-routing/intern-feature-designer.md` 命中。
- 实习工程架构开发者规则可从 `../roles/intern-engine-architecture-developer/RULE.md` 命中。
- 实习工程架构开发者派发检索可从 `../roles/role-manager/role-routing/intern-engine-architecture-developer.md` 命中。
- 实习 UI 开发者规则可从 `../roles/intern-ui-developer/RULE.md` 命中。
- 实习 UI 开发者派发检索可从 `../roles/role-manager/role-routing/intern-ui-developer.md` 命中。
- 实习玩法系统开发者规则可从 `../roles/intern-gameplay-systems-developer/RULE.md` 命中。
- 实习玩法系统开发者派发检索可从 `../roles/role-manager/role-routing/intern-gameplay-systems-developer.md` 命中。
- 实习战斗开发者规则可从 `../roles/intern-combat-developer/RULE.md` 命中。
- 实习战斗开发者派发检索可从 `../roles/role-manager/role-routing/intern-combat-developer.md` 命中。
- poe 小助手规则可从 `../roles/poe-helper/RULE.md` 命中。
- poe 小助手技能索引可从 `../roles/poe-helper/skills/INDEX.md` 命中。
- poe 小助手 modes 落地技能可从 `../roles/poe-helper/skills/modes-landing.md` 命中。
- poe 小助手目录与内容包分析技能可从 `../roles/poe-helper/skills/content-package-analysis.md` 命中。
- poe 小助手派发检索可从 `../roles/role-manager/role-routing/poe-helper.md` 命中。
- 批量视觉资源流程可从 `../roles/role-manager/RULE.md` 命中。
- 正式资源规格回收规则可从 `../roles/role-manager/RULE.md` 命中。
- 2D UI 绘图师正式 Sprite 交付要求可从 `../roles/2d-ui-artist/RULE.md` 命中。
- 多帧动画素材拆分规则可从 `../roles/ui-asset-slicer/RULE.md` 命中。
- 资源任务附加要求可从 `../roles/role-manager/templates/subagent-task.md` 命中。
- 角色管理员规则可从 `../roles/role-manager/RULE.md` 命中。
- 通用角色最小规则可从 `../roles/common/RULE.md` 命中。
- 会话角色标识自检会拒绝把执行角色写成主会话 `【当前角色】`。
- 当前能力可从 `INDEX.md` 路由。
- 通用架构 wiki 可从 `../wiki/INDEX.md` 路由。
- 角色会话复活规则可从 `../roles/role-manager/session-revival.md` 命中，并由 `check_required_paths` 检查存在。
- 写入边界仍保持：项目事实不进入 THarness 通用层；候选内容写入位置只由 `../roles/role-manager/issue-routing.md` 判断。
- `python tools/tharness.py doctor` 可检查入口、wiki 元数据和角色规则数量。
- `python tools/tharness.py index --check` 可检查 `AIGC/wiki/index.yaml` 页面清单一致性。
- `python tools/tharness.py check` 可执行结构自检。
- `python THarness/tools/tharness.py check` 可从父目录直接解析 THarness 入口并执行结构自检。
- `python tools/tharness.py self-check --path AIGC/wiki/architecture/role-system.md --delivery` 可输出 `index --check` 和 `check`。
- `python tools/tharness.py project start --root <目标目录>` 可在不部署锚点时输出临时启动包。
- `python tools/tharness.py project init --root <目标目录>` 可部署 `.tharness/project.yaml`、`start.ps1`、`start.cmd` 和说明文件，且不复制 `AIGC/`。
- `tools/tharness-binder` 可构建 Rust 桌面绑定工具，打包后的 `THarness-Binder.exe` 位于 THarness 主目录，可直接双击启动。
- `python -m unittest tools.test_tharness` 覆盖 CLI 无效输入、索引写回、自检命令规划、项目锚点启动和会话角色标识检查。
