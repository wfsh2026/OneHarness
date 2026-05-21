# 角色库入口

本目录是 Tharness 的默认调度入口。所有任务先进入角色管理员，再由角色管理员根据任务目标、风险和写入范围派发给具体角色。

## 默认读取

1. `common/RULE.md`
2. `role-manager/RULE.md`
3. 按角色管理员判断命中的角色规则。

## 目录结构

| 路径 | 存放内容 |
| --- | --- |
| `common/` | 所有角色必须遵守的最小规则、主会话输出格式和通用交付模板。 |
| `role-manager/` | 角色管理员规则、角色派发检索、项目适配路由、问题路由、派发模板和回收模板。 |
| `developer/` | 执行角色通用规则和实现交付模板。 |
| `{dispatchable-role}/` | 可派发角色根目录只保留 `RULE.md`，技能说明放 `skills/`，工具说明放 `tools/`。 |
| `qa-verification/` | 验证审查员规则、验证技能、工具说明和验证报告模板。 |
| `wiki-manager/` | wiki 管理员规则、wiki 管理技能、工具说明和项目知识维护路由。 |
| `tharness-maintainer/` | Tharness 本体维护、版本、自检规则、维护技能和工具说明。 |

## 角色

| 角色 | 入口 | 触发条件 |
| --- | --- | --- |
| 角色管理员 | `role-manager/RULE.md` | 所有用户请求的默认入口；负责沟通、拆分、派发、回收和交付判断。 |
| 执行角色通用规则 | `developer/RULE.md` | 任一角色需要修改代码、文档、配置、资源或测试时。 |
| UI 开发者 | `ui-developer/RULE.md` | 界面、HUD、菜单、提示、交互面板或 UI 状态流。 |
| 3C 开发者 | `character-controller-developer/RULE.md` | 角色、镜头、输入、移动、手感或动画状态接入。 |
| 场景开发者 | `scene-developer/RULE.md` | 场景、关卡、触发器、出生点、导航或场景交互。 |
| 战斗开发者 | `combat-developer/RULE.md` | 攻击、受击、技能、伤害、状态或战斗判定。 |
| AI 开发者 | `ai-developer/RULE.md` | 敌人行为、感知、巡逻、仇恨、目标选择或决策。 |
| 玩法系统开发者 | `gameplay-systems-developer/RULE.md` | 背包、任务、存档、配置、事件流或全局玩法系统。 |
| 工具开发者 | `tools-developer/RULE.md` | 编辑器工具、批处理、导入导出、调试面板或内容管线。 |
| 技术美术开发者 | `technical-art-developer/RULE.md` | 特效、材质、Shader、动画事件或表现接入。 |
| 验证审查员 | `qa-verification/RULE.md` | 复现、回归、验收、失败路径、压力路径或高风险集成验证。 |
| wiki 管理员 | `wiki-manager/RULE.md` | 判断候选知识写入通用 wiki、项目知识、运行记录或不写入。 |
| Tharness 能力维护员 | `tharness-maintainer/RULE.md` | 修改 Tharness 规则、角色库、项目接入机制、能力索引、自检工具或模板。 |

## 调度原则

- 角色管理员是唯一主会话用户沟通者。
- 角色管理员是唯一角色派发者。
- 角色边界、派发判断和冲突处理只由角色管理员读取 `role-manager/role-routing/`。
- 具体角色任务必须通过 SubAgent 或全新会话执行；无法启动时必须由角色管理员记录替代隔离方式。
- 执行角色只遵守 `common/RULE.md`、自身角色规则和任务包中允许读取的资料。
- 执行角色不得自行扩大范围、改派其他角色或直接改变用户目标；发现问题时回报角色管理员。
- 同一文件同一时间只能有一个写入角色。

## 角色资料位置

角色相关规则、调用资料和方法卡都维护在 `AIGC/roles/` 下。需要形成多步骤执行方式时，由角色管理员基于角色库、项目适配规则和通用 wiki 组合任务包。

通用输出格式由 `common/session-visible-state.md` 维护；可复用模板放在各角色目录的 `templates/` 下。角色规则引用模板，不复制模板正文，避免多处规则漂移。

具体可派发角色目录的根目录只保留 `RULE.md`。角色执行技能放在 `skills/`，工具调用说明放在 `tools/`。输入契约、输出契约、边界和交接不作为具体角色根文件维护；输入由角色管理员任务包提供，输出由 `RULE.md` 引用模板，边界和交接由角色管理员检索资料维护。
