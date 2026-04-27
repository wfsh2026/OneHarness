# BIU26 功能进度追踪 (active.md)

> **当前阶段**：阶段7 — Phase 1 发育循环链路已验证（有怪、能打、有压迫感）；节点1（第一把悬浮武器解锁）待开发；即将启动 GPO Agent 开发节点2（武器掉落+拾取+多把解锁）  
> **最后更新**：2026-03-29 (v1.8)
> **维护者**：[项目负责人]

---

## 功能概述

**功能名**：BIU26 原型开发  
**产品定位**：让被操作门槛劝退的射击老玩家（25-40岁），在低操作门槛下重新感受射击游戏的割草爽感 + 战术博弈乐趣。  
**品类**：多人竞技 × 自动化割草发育 × 吃鸡式战术收尾 × 元素克制策略

---

## 策划文档状态

| 文档 | 版本 | 状态 |
|------|------|------|
| BIU26经营提案.md | v1.1 | ✅ 已完成 |
| BIU26核心体验设计.md | v0.3 | ✅ 已完成（含待确认数值） |
| BIU26武器系统设计.md | v1.0 | ✅ 已完成 |
| BIU26怪物设计.md | v0.1 | ✅ 已完成（含待确认事项） |
| BIU26地图设计.md | v0.1 | ✅ 已完成（含待确认事项） |
| BIU26兴趣曲线.md | v0.1 | ✅ 已完成（待原型测试更新） |
| BIU26原型开发启动包.md | v1.0 | ✅ 已完成 |

---

## 技术文档状态

| 文档 | 负责 Agent | 状态 |
|------|-----------|------|
| DL 主计划（BIU26_开发计划.md） | DL | ✅ 已完成（plan-doc 重构，v1.1，补全全4Phase体验节点；M-03新增GPO子文档）|
| BIU26-模式系统.md | DL | ✅ 已完成（v1.1，架构变更：移除FloatingWeaponAttack/LayoutPoint，FloatingWeaponManager改为生成独立GPO）|
| BIU26-极坐标刷怪器.md | GPO 工程师 | ✅ GPO 代码已完成：GPOM_BIU26Set.cs + SE_BIU26.cs + ServerBIU26SpawnerSystem.cs + MinionsSpawner + ClientBIU26SpawnerSystem.cs；路由已注册；编译通过 |
| BIU26-悬浮武器GPO.md | GPO 工程师 | ✅ GPO 代码已完成：GPOM_BIU26FloatingWeapon + ServerBIU26FloatingWeaponSystem + ServerBIU26FloatingWeaponAttack + ClientBIU26FloatingWeaponSystem + ClientBIU26FloatingWeaponView；路由已注册；编译通过（Phase 1 Ability 使用 UAV 追踪导弹占位） |
| BIU26-悬浮武器Ability.md | Ability 工程师 | ✅ Phase 1 已完成：CSV 追加 ID=3 行（RowSign=BIU26_FloatingWeaponBullet）+ _Select.cs 常量（ID_3/Sign_）+ ServerBIU26FloatingWeaponAttack 代码链路打通；编译 0 错误 |
| BIU26-场景建设.md | 场景建设工程师 | ✅ 已完成（双场景搭建完毕：BIU26_Dev.unity + ServerBIU26_Dev.unity；路径 Assets/Scenes/Runtime/）|
| **BIU26-ServerBIU26Mode（新）** | GPO 工程师 | ✅ ModeData.ModeEnum.ModeBIU26=26；ServerBIU26Mode.cs 已创建并注册；编译 0 错误 |
| **BIU26-怪物GPO系统.md（新）** | DL | ✅ 已完成 v1.1（三档怪物+近身掉血+进化机制+4种行为类型；GpoType=32/33/34；GPO Id=102/104/105；行为组件文件清单含 Rush/Swarm/Ranged/Tank）|
| **BIU26-武器升品质系统.md（新）** | DL | ✅ 已完成 v1.0（满编→升品质分支；概率体系+保底计数；RemoveAI+AddMasterAI升品质链路；蓝质Id=106/金质Id=107；数值白×1.0/蓝×1.5/金×2.5）|
| 归档：BIU26_Phase1_开发执行计划.md（原单文档） | DL | 📁 已归档，保留参考 |

---

## 开发阶段进度

| 阶段 | 内容 | 状态 |
|------|------|------|
| 阶段1 | 用户提交原始需求（策划总纲） | ✅ 已完成 |
| 阶段2 | 需求深度分析（GD评估 + DL技术评估）| ✅ 已完成（Round 1 通过）|
| 阶段3 | 用户决策拍板 | ✅ 已完成（Phase 1 关键项全部确认）|
| 阶段4 | 完整文档生成 + 开发计划制定 | ✅ 已完成（Round 2 通过）|
| 阶段5 | 用户审图确认（五项） | ✅ 已完成（①体验节点 ②文档完整性 ③技术方案 ④美术灰盒 ⑤UI灰盒 全部通过）|
| 阶段6 | Phase 1 开发（核心发育循环） | ✅ P0-1/P0-2/P0-3 完成（含5个运行时Bug修复、3个缺失Prefab创建），待 PlayMode 验证 |
| 阶段6 | Phase 2 开发（缩圈 + PVP） | ✅ 缩圈重构完成（Prefab加载+渐进缩圈+每秒下发）|
| 阶段6 | **Phase 2.5 开发（怪物系统 + 武器升品质）** | ✅ 全部代码完成（编译0错误）；三档灰盒 Prefab 已创建 |
| 阶段6 | Phase 3 开发（元素系统基础：武器元素化+3种状态效果） | 📄 技术文档已完成，待 GPO 工程师实现 |
| 阶段6 | Phase 3.5 开发（元素反应：3种组合反应+同元素增强） | 📄 技术文档已完成，待 Phase 3 验收后实现 |
| 阶段6 | Phase 4 开发（金币经济 + 结算） | ⬜ 最后 |

---

## 待主策划确认的关键事项（P6 汇总）

| 来源文档 | 待确认项 |
|---------|---------|
| 核心体验设计 | 武器解锁时间轴各节点、保底N值（8-12只）、圈外伤害数值、DPS上限倍率、金币三来源比例、排名奖励系数 |
| 武器系统设计 | 六种枪型战斗定位、三种元素反应效果方向、同元素3把额外效果、品质用模型放大表达、武器池结构 |
| 怪物设计 | 四种行为类型确认、电系怪过载短路机制、三档进化比例（30-40%）、头目怪特殊技能、动态刷怪密度技术可行性 |
| 地图设计 | 地图总尺寸（120m×120m）、三区域划分比例、中心点固定、中心区掩体减少设计、地标建筑高度 |

---

## 用户决策记录

| 时间 | 决策内容 |
|------|---------|
| 2026-03-28 | 用户启动 BIU26 开发流程，要求协助完成 BIU26策划总纲需求 |
| 2026-03-28 | **D2** 手持武器沿用现有枪械系统，Phase 1 不新建手持武器参数 |
| 2026-03-28 | **D3** 玩家HP沿用现有默认值，Phase 1 不修改HP体系 |
| 2026-03-28 | **Q1（变更）** 悬浮武器从「视觉挂点方案A2」更新为「独立GPO方案B」，参考UAV无人机逻辑（ServerAIFindInsightTarget + ServerAITrackingMissleAttack），理由：代码量更少，开发更简单 |
| 2026-03-28 | **Q3/C4** 悬浮武器参考UAV逻辑，自动锁敌攻击 |
| 2026-03-28 | **Q2/C1** 武器拾取方式：UI确认弹窗，走近显示提示，玩家手动确认拾取 |
| 2026-03-28 | **B7** 品质数值以武器系统设计文档为准：普通×1.0，蓝质×1.5，金质×2.5 |
| 2026-03-28 | **D1** 满装后武器品质升级保底：每连续5把未升品质必保底升一级 |
| 2026-03-28 | **UI方案** Phase 1 金币HUD改用 `OnGUI（OGUI）` 实现，不引入 TextMeshPro/UGUI，参考 `AimAssistDebugOnGUI.cs` |

---

## Background Agent 记录

| agent_id | 任务描述 | 预期产出文件 | 启动时间 | 状态 |
|----------|---------|-------------|---------|------|
| gd-stage2 | [GD] 阶段2 — 核心体验评估 + 模糊点清单 + 优化建议 | 本轮输出（不创建文件） | 2026-03-28 | ✅ 完成 |
| dl-stage2 | [DL] 阶段2 — 系统归属评估 + 多方案对比 + 技术可行性 | 本轮输出（不创建文件） | 2026-03-28 | ✅ 完成 |
| dl-restructure | [DL] 阶段4重构 — 将单文档拆分为 plan-doc 主计划+子文档体系 | `aigc/docs/Dev_Lead/BIU26/BIU26_开发计划.md` + `技术文档/` 4份 | 2026-03-28 | ✅ 完成 |
| round2-quality-check | [项目负责人] Round 2 多文档体系完整审核（MD-M/S/X） | 本轮输出（不创建文件） | 2026-03-28 | ✅ 完成（全部通过，无强制修改项）|
| dl-biu26-minion-doc | [DL] 创建 BIU26-怪物GPO系统技术文档（三档怪物+近身掉血+进化机制） | `aigc/docs/GamePlay_Dev/BIU26/技术文档/BIU26-怪物GPO系统.md` | 2026-03-30 | ✅ 完成 |
| dl-biu26-minion-behavior | [DL] 补充 BIU26-怪物GPO系统.md 行为类型章节（冲锋/群涌/远程/坦克 × 代码骨架） | `aigc/docs/GamePlay_Dev/BIU26/技术文档/BIU26-怪物GPO系统.md`（修改 v1.0→v1.1） | 2026-03-30 | ✅ 完成 |
| gpo-biu26-minion | [GPO 工程师] 实现三档怪物GPO系统（GpoType=32/33/34，Id=102/104/105，4种行为类型组件，进化机制） | GpoType.cs/Gpo.cs/GPOM_BIU26MinionSet.cs/IGPOM.cs/SE_BIU26.cs/路由/3xSystem/ContactDamage/4xBehavior/MinionsSpawner/ClientMinionSystem | 2026-03-30 | ✅ 完成（编译0错误；新建10文件，修改8文件；GpoType32/33/34注册；GPOM三档+行为类型+进化机制全部实现；项目负责人抽检通过）|
| dl-biu26-weapon-quality | [DL] 编写武器满载升品质技术文档（概率体系+保底机制+升品质算法） | `aigc/docs/GamePlay_Dev/BIU26/技术文档/BIU26-武器升品质系统.md` | 2026-03-30 | ✅ 完成（v1.0，项目负责人审核通过；追加 ServerBIU26Mode 初始武器追踪条目；D2决策：初始武器在 Mode OR_CallBack 中广播 Event_FloatingWeaponAdded） |
| gpo-biu26-weapon-quality | [GPO 工程师] 实现武器满载升品质代码（Event_FloatingWeaponAdded / GPOM蓝质金质 / Manager重构 / PickupZone+Mode追踪 D2） | SE_BIU26.cs / GPOM_BIU26Set.cs / Gpo.cs / ServerBIU26FloatingWeaponManager.cs / ServerBIU26WeaponPickupZone.cs / ServerBIU26Mode.cs | 2026-03-30 | ✅ 完成（编译0错误；修复 ai.iGPO→ai.GetGPO()；项目负责人抽检通过）|

---

## 规范沉淀

| 日期 | 类型 | 内容 |
|------|------|------|
| 2026-03-29 | 场景架构 | `ServerSceneSerialize` 由 `ServerSceneSystem.AddComponent<>()` 运行时注册，**不需要**放在场景 Hierarchy 中 |
| 2026-03-29 | 场景工具 | `ServerSceneOptimizer`（`Tools/功能/场景/服务器场景转换`）用于从客户端场景生成服务端场景，自动移除 Renderer/Light/Particle，保留 MeshCollider |
| 2026-03-29 | ModeData | 测试模式 ID 从 10001 开始，`Id_BIU26 = 10004`；`AddTestMode()` 必须为每个新 ModeEnum 注册 Data 条目；`GetAllGameMatches()` 必须追加对应 ModeMatch 入口才能在测试界面显示 |
| 2026-03-29 | SceneConfig | `TargetScenePath` 存**客户端**场景路径；服务端场景由 `StageData.GetServerStage(name) = "Server" + name` 自动推导；`SceneData.datas` 需同步添加 `{ID, StageSign=客户端场景名, ElementConfig=配置asset名}` 条目 |
| 2026-03-29 | ZoneMarker | `ZoneMarkers` 父节点下所有 Collider 必须设置 `isTrigger = true`；漏设会在 Default 层产生实体碰撞，阻挡玩家进入中心区域（BIU26_Dev Zone_Outer/Mid/Inner 均已修复）|
| 2026-03-29 | Ability CSV | `AbilityM_TrackingMissle.csv` 新增 RowSign 行时，`M_EffectSign` 不可为空；Phase 1 BIU26 FloatingWeapon 复用 `UAVMissle` 特效 |
| 2026-03-29 | AI GPO | AI GPO System 调用 Ability 攻击时（`weaponItemId=0`），FireGPO **必须**包含 `ServerAISummonedCreatureSource` 组件，否则 `SAB_ExplosiveSystem` 无法获取伤害来源 |
| 2026-03-29 | iGPO 作用域 | iGPO 是 Component（ServerNetworkComponentBase 等基类）的属性，不是 System 的属性。Spawner 类 Component 以「自身位置」为刷怪圆心，直接调用 iGPO.GetPoint()，禁止通过 InitData 透传 OwnerGPO（System 不持有该字段）。 |
| 2026-03-29 | AI 客户端实体 | GPOM_CharacterSet 的 AssetSign 如为通用名（如 "Character"）而非 CharacterAI_{heroId}_{skinId} 规范命名，客户端找不到 prefab。修复：在 SM_AI.Event_AddAI 中设置 OR_AISkinSign = "CharacterAI_1_0" 强制覆盖，不修改 DLL 内 GPOM 定义。 |
| 2026-03-30 | Phase 2 缩圈系统（重构） | 毒圈从场景删除，改为 `PrefabPoolManager.OnGetPrefab("Assets/Bundle/GamePlay/AI/Client/BIU26Zone.prefab")`；新增 `Rpc_BIU26ZoneRadiusTick`（FuncID=27）每秒下发半径；`ServerBIU26ZoneSystem` 改为 Waiting→Shrinking 状态机，线性插值 currentRadius；`ClientBIU26ZoneSystem` 平滑插值 scale（1秒内），HUD 显示倒计时/缩圈中 |
| 2026-03-30 | **Phase 2.5 新增** | 在 Phase 2（缩圈）和 Phase 3（元素）之间插入 Phase 2.5：三档怪物GPO（普通/精英/头目）+ 4种行为类型 + 近身掉血 + 武器满载升品质（白→蓝→金）+ 保底升品质机制 |
| 2026-03-30 | **D2（武器追踪）** | 初始第1把悬浮武器不经过 WeaponPickupZone，在 `ServerBIU26Mode.OnAddCharacterCallBack` 的初始武器 OR_CallBack 中手动广播 `SE_BIU26.Event_FloatingWeaponAdded`，确保 `_activeWeapons` 追踪全部6把 |


---

## 节点2 代码完成记录（追加于 2026-03-29）

### 新增/修改文件

| 文件 | 操作 | 说明 |
|------|------|------|
| Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs | **修改** | Event_MinionKilled 改为 IWorldEvent + 添加 DeathPoint 字段 |
| Assets/Scripts/Template/data/GpoType.cs | **修改** | 添加 Id_BIU26WeaponPickup = 31 及 Data 行 |
| Assets/Scripts/Template/data/Gpo.cs | **修改** | 添加 Id_BIU26WeaponPickup = 103 及 Data 行 |
| Assets/Scripts/Template/gpo/GPOM_BIU26WeaponPickupSet.cs | **新建** | GPOM 结构体+Set类（GpoType=31, Id=103） |
| Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26WeaponPickupSystem.cs | **新建** | S_AI_Base，AddComponent WeaponPickupZone，OnStart CreateEntity |
| Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26WeaponPickupZone.cs | **新建** | 每0.5s扫GPOList，GPOType.Role + 同TeamId + 3m内 → 召唤FloatingWeapon → 销毁自身；15s超时自毁 |
| Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26MinionsSpawner.cs | **修改** | CheckDeadMinions 改用 MsgRegister.Dispatcher，传 DeathPoint |
| Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26FloatingWeaponManager.cs | **新建** | ComponentBase（Mode级），保底概率掉落（20%+5%累加，触发重置），上限6把 |
| Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26WeaponPickupSystem.cs | **新建** | C_AI_Base，CreateEntity(AttributeData.SkinSign) |
| Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs | **修改** | 添加 case GpoTypeSet.Id_BIU26WeaponPickup → ServerBIU26WeaponPickupSystem |
| Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs | **修改** | 添加 case GpoTypeSet.Id_BIU26WeaponPickup → ClientBIU26WeaponPickupSystem |
| Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerBIU26Mode.cs | **修改** | OnAddCharacterCallBack 中 mySystem.AddComponent<ServerBIU26FloatingWeaponManager>；移除 OnMinionKilled |
| Assets/Bundle/GamePlay/AI/Client/BIU26WeaponPickup.prefab | **新建** | 球体占位（金色Material），供 ClientBIU26WeaponPickupSystem 加载 |
| Assets/Bundle/GamePlay/AI/Client/BIU26WeaponPickup_Mat.mat | **新建** | 金色 URP/Lit 材质 |

### 关键架构决策（本轮）

| 决策 | 内容 |
|------|------|
| SE_BIU26.Event_MinionKilled 类型 | ISystemEvent → IWorldEvent（MsgRegister 全局广播，Mode级组件才能接收） |
| FloatingWeaponManager 挂载位置 | Mode 级 ComponentBase（不挂玩家 GPO，通过 mySystem.AddComponent<T> 添加）|
| 探测方式 | GPOList 迭代，过滤 GPOType.Role + 同TeamId + 3m范围（不用 OverlapSphere）|
| 掉落概率 | 初始20%，每次未掉落+5%，触发后重置20%；满6把停止 |
| 拾取物生命周期 | 15s 未拾取自动 Event_RemoveAI 销毁 |

