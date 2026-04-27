# 项目系统地图 (knowledge/system-map.md)

> **本文件为项目特定数据**，不通过 framework 同步，各项目独立维护。
> 通用检索规则见 [[system-map-rules]]。
> 本文件属于 knowledge 核心层，构建方式见 [[workflow-knowledge]]。

---

## 一、项目概述

**项目**：sausage-man-2022（香肠派对）
**类型**：多人竞技射击（BR / 多模式）
**架构**：1 代 C/S/H 三端 Modules + 2 代 ECS System/Component（Biubiubiu2）
**代码库根目录**：`Assets\Script`（注意：无 s）

### 两代架构说明

| 代际 | 代码根 | 架构 | 文件数 |
|------|--------|------|--------|
| 1 代 | `Assets/Script/`（不含 Biubiubiu2/） | C/S/H 三端 Modules | ~10,856 |
| 2 代 | `Assets/Script/Biubiubiu2/` | ECS System/Component | ~2,083 |

### 关键目录

| 用途 | 路径 |
|------|------|
| 常量定义 | `Assets/Script/Data/ItemData.cs` |
| 配置代码 | `Assets/Script/Config/` |
| 配置表 | `Assets/ToBundle/Config/Txt/` |
| 物理参数 SO | `Assets/ToBundle/ScriptableObject/Vehicle/` |
| 地图投放 SO | `Assets/ToBundle/ScriptableObject/SOCreateObjData/` |
| 预制体(2代) | `Assets/Art/Biubiubiu2/Prefabs/Car/` |

### 必读文件

| 场景 | 文件 |
|------|------|
| 开发流程 | [[workflow-dev]] |
| 安全规则 | [[safety-rules]] |
| 1 代编码规范 | [[sausage-core-rules]]（含附录 B 工作流差异） |
| 2 代编码规范 | `aigc/harness/rules/GamePlay_Dev/*.md`（按需加载） |

---

## 二、系统地图与意图识别

### 系统总表

| 系统 | 描述 | 关键代码目录 | 边界定义文档 | 开发规范 | base feature |
|------|------|------------|------------|---------|-------------|
| **载具系统** | 地面/飞行/特殊载具的驾驶、上下车、射击、技能 | **C** `GamePlay/Client/Modules/Car/` + `FlyVehicle/`　**S** `GamePlay/Server/Modules/Car/`　**H** `GamePlay/Host/Modules/Car/` | [[载具系统内容边界定义]] | [[载具制作]] | [[car-base]] |
| **模式系统** | 游戏模式管理/阶段控制/模式规则/胜负条件 | **C** `GamePlay/Client/Modules/Mode/`　**S** `GamePlay/Server/Modules/Mode/`　**H** `GamePlay/Host/Modules/Mode/`　**Factory** `ClientModeFactory.cs` · `ServerModeFactory.cs` | — | [[模式制作]] | [[mode-base]] |
| **角色系统** | 双层 Component 架构的角色实体/逻辑/渲染/网络/战斗 + Motion 动画 | **H** `GamePlay/Host/Modules/Role/` (176)　**S** `GamePlay/Server/Modules/Role/` (69)　**C** `GamePlay/Client/Modules/Role/` (129)　**Motion** `GamePlay/Client/Motion/` (99) | — | [[角色制作]] · [[角色动画制作]] | [[role-base]] |
| **Buff 系统** | Buff 创建/管理/同步/生命周期 | **框架** `UI/War/BuffControl/` (11)　**H** `GamePlay/Host/Modules/Buff/` (477)　**S** `Server/Modules/Buff/` (285)　**C** `Client/Modules/Buff/` (268) | — | [[Buff制作]] | [[buff-framework]] |
| **AI 系统** | NPC/Bot 行为树、战场 AI、自动战斗 | **C** `Client/Modules/RoleAI/` (214)　**S** `Server/Modules/RoleAI/` (108)　**AutoWar** `GamePlay/AutoWar/` (35) | — | [[AI制作]] | [[ai-base]] |
| **武器/战斗系统** | 射击(47 SOWeaponControl)、近战(23 SOHitPart)、特殊(27 SO) | **射击** `UI/War/Weapon/WeaponControl.cs`　**近战** `UI/War/Weapon/HitPart.cs`　**近战框架** `Client/Modules/FightClose/` + `MeleeWeapon/` | [[枪械系统内容边界定义]] | [[射击武器制作]] · [[近战武器制作]] · [[特殊武器制作]] · [[武器战斗制作]] | [[weapon-base]] |
| **投掷物系统** | 手雷(Bomb=31)、爆破炸弹(BlastBomb=97)、角色手雷技能 | **基类** `UI/War/Role/RoleSkill/RoleSkillBomb.cs`　**弧线** `UI/War/Weapon/BombLineRender.cs` | — | [[投掷物制作]] | [[throwable-bomb]] |
| **消耗品系统** | 绷带/急救包/医疗箱/止痛药/能量饮料/变身药剂 | **Buff** `Host/Modules/Buff/BS*AddHP*`　**组件** `BattleRoleConsumeItemComponent` | — | [[消耗品制作]] | [[item-consumable]] |
| **武器配件系统** | 瞄准镜/弹匣/枪口/枪托/握把/芯片 | **C** `Client/Modules/WeaponEquip/`　**Config** `SOWepEquipData.txt` | — | [[武器配件制作]] | [[weapon-attachment]] |
| **角色装备系统** | 防弹衣/头盔/背包/吉利服/狗牌 | **组件** `BattleRoleEquipComponent`　**Config** `SOEquipPart.txt` | — | [[角色装备制作]] | [[role-equipment]] |
| **身份卡系统** | 29 种 IdCard，拾取后获得 2 技能 | **框架** `UI/War/Role/RoleSkill/`　**BS三端** `{C\|S\|H}/Modules/Buff/` + `RoleSkill/` | — | [[身份卡制作]] | [[idcard-framework]] |
| **道具系统** | 战场拾取物/装备/空投 | **Pool** `Script/Asset/ItemPool.cs`　**Data** `Config/SOItemDataConfig.cs` | — | — | [[item-base]] |
| **战场活动道具** | 节日/活动限定拾取道具(粽子/红包/鞭炮等) | **Config** `Config/ActivityItemSkinConfig.cs`　**Prefab** `PickItems/Activity*.prefab` (15) | — | [[战场道具制作]] | [[item-activity]] |
| **赛季道具系统** | 赛季通行证/手册/皮肤/道具/奖励 | **C** `Client/Modules/Season/`　**Config** `Config/SeasonItem*.cs` | — | [[赛季道具制作]] | — |
| **UI 系统** | UI 框架/窗口管理/HUD/结算 | `Script/UI/` (1,968) + `Script/Manager/Window*.cs` | `UI 系统内容边界定义.md` | [[UI系统制作]] | [[ui-framework]] · [[ui-player-control]] · [[ui-map]] · [[ui-elements]] · [[ui-war-init]] |
| **镜头系统** | 镜头跟随/震动/切换/后处理 | `GamePlay/Client/Modules/Camera/`　**主控** `CameraController.cs`(246KB)　**SO** `SOCameraUserData.cs` | [[镜头系统内容边界定义]] | [[镜头系统制作]] | [[camera-system]] |
| **时装/皮肤系统** | 时装换装/皮肤渲染/时装特效 | `Script/Asset/Loaders/FashionLoader.cs`　`ToBundle/Fashion/` (22,643) | — | [[角色时装制作]] | — |
| **地图/场景系统** | 场景加载/地图拆分/天空盒 | `Script/Asset/Loaders/SceneLoader.cs`　`ToBundle/Map/` | — | — | — |
| **宠物系统** | 淘金宠物/宠物技能 | `ToBundle/ScriptableObject/Pet/` (164) | — | — | — |
| **背包系统** | 战场背包/装备管理 | `ToBundle/ScriptableObject/Bag/` (225) | — | — | — |
| **新手引导系统** | 新手引导/教程 | `ToBundle/ScriptableObject/BeginnerTutorial/` (63) | — | — | — |
| **技能系统** | 角色技能/卡牌/芯片/特技 | `Host+S+C/Modules/RoleSkill/` | — | — | — |
| **网络/消息系统** | Mirror 网络同步/消息定义/Proto协议(66) | `Script/Biubiubiu2/Message/` (~265)　**Proto** `GamePlay/Host/Network/Proto/Base/` (66)　**C** `GamePlay/Client/Network/` (125)　**S** `GamePlay/Server/Network/` (127) | — | [[网络消息制作]] | [[network-framework]] |
| **基础设施** | 工具库/配置/数据/资源管理/Controller | `Script/Utils/` (494) · `Config/` (678) · `Data/` (290) · `Controller/` (135) | — | [[基础设施制作]] | [[infra-base]] |

> **说明**：所有代码路径均相对于 `Assets\Script\`（注意无 s）。
>
> **资源地图**：完整的资源路径索引见 → [[resource-map]]
> 包含 18 个系统章节 + 4 个附录，覆盖 ToBundle/ 全部 22 个顶层目录。

### 意图识别关键词映射

> 通用识别原则见 [[system-map-rules]] §二。
> 每行「加载文档」列必须精确到 feature wiki-link 或制作文档，禁止「同上」。

| 用户关键词示例 | 涉及系统 | 加载文档 |
|-------------|---------|---------|
| 载具、汽车、驾驶、上车、下车 | 载具系统（框架） | [[载具系统内容边界定义]] + [[载具制作]] + [[car-base]] |
| 吉普、碰碰车、装甲巴士 | 载具系统（Buggy 家族） | [[载具制作]] + [[car-buggy-family]] |
| 小马、绵羊、PonyVehicle | 载具系统（Motor 家族） | [[载具制作]] + [[car-motor-family]] |
| 恐龙载具、三角龙、迅猛龙、剑齿虎、霸王龙 | 载具系统（动物家族） | [[载具制作]] + [[car-animal-family]] |
| 机甲、机器人、机甲车、CyberTitan | 载具系统（机甲） | [[载具制作]] + [[car-robot]] |
| 飞龙、Dragon | 载具系统（飞龙） | [[载具制作]] + [[car-dragon]] |
| 翼龙、Peterosaur | 载具系统（翼龙） | [[载具制作]] + [[car-peterosaur]] |
| 飞燕号、GutsWing | 载具系统（飞燕号） | [[载具制作]] + [[car-gutswing]] |
| 神龙、ShenLong | 载具系统（神龙） | [[载具制作]] + [[car-shenlong]] |
| 飞行扫帚、FlyingBroom | 载具系统（飞行扫帚） | [[载具制作]] + [[car-flyingbroom]] |
| 飞行载具框架、FlyVehicle 基类 | 载具系统（飞行框架） | [[载具制作]] + [[fly-vehicle]] |
| 载具射击、载具武器 | 载具系统（射击） | [[载具制作]] + [[car-shoot]] |
| 载具标记、AirShip、AlienWarship、飞毯 | 载具系统（特殊标记） | [[载具制作]] + [[car-special]] |
| 新增载具、添加载具、载具技能 | 载具系统（开发） | [[载具制作]] + [[载具参考范例]] |
| 游戏模式、Mode、ModeManager | 模式系统（框架） | [[模式制作]] + [[mode-base]] |
| 经典模式、Classic、BR | 模式系统（经典） | [[模式制作]] + [[mode-classic]] |
| 模式通用、ModeCommon | 模式系统（通用） | [[CommonMode制作]] + [[mode-common]] |
| 撤离模式、GoldDash、金币撤离 | 模式系统（撤离） | [[GoldDash制作]] + [[mode-golddash]] |
| 快速撤离、FastGoldDash | 模式系统（快速撤离） | [[GoldDashFast制作]] + [[mode-golddash-fast]] |
| 新手营、RookieCamp | 模式系统（新手营） | [[RookieCamp制作]] + [[mode-rookiecamp]] |
| 猛兽营、BeatBeastCamp | 模式系统（猛兽营） | [[BeatBeastCamp制作]] + [[mode-beatbeastcamp]] |
| 竞速、OnlyUp、攀爬 | 模式系统（竞速） | [[OnlyUp制作]] + [[mode-onlyup]] |
| 足球、FootballParty | 模式系统（足球） | [[FootballParty制作]] + [[mode-footballparty]] |
| 社交、SocialLobby | 模式系统（社交） | [[SocialLobby制作]] + [[mode-sociallobby]] |
| PVE、肉鸽、PveRogue、Roguelike | 模式系统（PVE肉鸽） | [[PveRogue制作]] + [[mode-pverogue]] |
| 飞球、BladeBall | 模式系统（飞球） | [[BladeBall制作]] + [[mode-bladeball]] |
| 闯关、GoGoParty | 模式系统（闯关） | [[GoGoParty制作]] + [[mode-gogoparty]] |
| 团队激斗、EvoDeathMatch | 模式系统（进阶激斗） | [[EvoDeathMatch制作]] + [[mode-evodeathmatch]] |
| 爆破、DefusalMode、拆弹 | 模式系统（爆破） | [[DefusalMode制作]] + [[mode-defusal]] |
| 团队模式、TeamMode | 模式系统（团队） | [[TeamMode制作]] + [[mode-teammode]] |
| 枪王、BullFighting | 模式系统（枪王） | [[BullFighting制作]] + [[mode-bullfighting]] |
| PK之王、TurnBased、1V1 | 模式系统（回合制） | [[TurnBasedMode制作]] + [[mode-turnbased]] |
| 阵营对抗、CustomRoomCamp | 模式系统（阵营） | [[CustomRoomCamp制作]] + [[mode-customroomcamp]] |
| 奥特派对、UltraFight | 模式系统（奥特） | [[UltraFight制作]] + [[mode-ultrafight]] |
| 狼人派对、WolfParty、Wolfparty | 模式系统（狼人） | [[WolfParty制作]] + [[mode-wolfparty]] |
| 淘汰赛、Knockout、赛制休闲 | 模式系统（淘汰赛） | [[Knockout制作]] + [[mode-knockout]] |
| 运动派对、SportsParty | 模式系统（运动派对） | [[SportsParty制作]] + [[mode-sportsparty]] |
| 轰炸区、BombArea、空袭 | 模式系统（轰炸区） | [[模式制作]] + [[mode-common]] |
| 毒圈、GameQuan、缩圈 | 模式系统（毒圈） | [[模式制作]] + [[mode-common]] |
| 新增模式、添加模式、创建模式 | 模式系统（开发） | [[模式制作]] + [[mode-base]] |
| 角色、BattleRole、RoleLogic | 角色系统（框架） | [[角色制作]] + [[role-base]] |
| HP、血量、扣血、DownHp、伤害计算、护甲 | 角色系统（伤害） | [[角色制作]] + [[role-damage]] |
| 死亡、复活、淘汰、击杀 | 角色系统（死亡/复活） | [[角色制作]] + [[role-death]] |
| 角色状态、站蹲趴、RoleState | 角色系统（状态） | [[角色制作]] + [[role-state]] |
| 角色移动、MoveSpeed | 角色系统（移动） | [[角色制作]] + [[role-movement]] |
| 游泳、水面、Swim | 角色系统（游泳） | [[角色制作]] + [[role-swim]] |
| 飞行、跳伞、BoxingFly | 角色系统（飞行） | [[角色制作]] + [[role-fly]] |
| 皮肤、换装、DuoBao、RoleSkin | 角色系统（皮肤） | [[角色制作]] + [[role-skin]] |
| 动画、Animator、IK、Playable | 角色系统（动画） | [[角色制作]] + [[role-animation]] + [[role-animator]] |
| AnimatorControl、Motion、动画状态机 | 角色系统（Motion） | [[角色制作]] + [[role-motion]] |
| 碰撞、HitBox、CapsuleMove | 角色系统（物理） | [[角色制作]] + [[role-physics]] |
| RoleNet、角色同步、重连 | 角色系统（网络） | [[角色制作]] + [[role-network]] |
| 反作弊、RoleCheat | 角色系统（反作弊） | [[角色制作]] + [[role-cheat]] |
| 扶人、Uprear、倒地 | 角色系统（救援） | [[角色制作]] + [[role-uprear]] |
| 队友代管、Teammate | 角色系统（代管） | [[角色制作]] + [[role-teammate]] |
| 角色渲染、模型、描边 | 角色系统（渲染） | [[角色制作]] + [[role-render]] |
| 布娃娃、Ragdoll | 角色系统（布娃娃） | [[角色制作]] + [[role-physics]] |
| Buff、增益、减益、BuffControl | Buff 系统（框架） | [[Buff制作]] + [[buff-framework]] |
| BuffSystem、BSO、BS、PlayBuff | Buff 系统（框架） | [[Buff制作]] + [[buff-framework]] |
| 回血、DoT、HoT、BSAddHPForTime | Buff 系统（战斗） | [[Buff制作]] + [[buff-add-hp-for-time]] |
| 击退、BeatBack | Buff 系统（击退） | [[Buff制作]] + [[buff-beat-back]] |
| 爆炸、范围伤害、RangeDownHP | Buff 系统（范围伤害） | [[Buff制作]] + [[buff-range-down-hp]] |
| C4、BlastBomb | Buff 系统（C4炸弹） | [[Buff制作]] + [[buff-blast-bomb]] |
| 冲刺、加速、BSEightDirDash | Buff 系统（移动） | [[Buff制作]] + [[buff-eight-dir-dash]] |
| 护盾、BSRoleShield | Buff 系统（防御） | [[Buff制作]] + [[buff-role-shield]] |
| Buff 特效、BSAddEffectObj | Buff 系统（视觉） | [[Buff制作]] + [[buff-add-effect-obj]] |
| 陷阱、触发器、BSActionTrigger | Buff 系统（道具） | [[Buff制作]] + [[buff-action-trigger]] |
| PVE Buff、BSPve | Buff 系统（PVE） | [[Buff制作]] + [[buff-pve-monster]]；全部 PVE Buff 见 [[mode-pverogue]]（关联 Buff） |
| GoldDash Buff、BSGoldDash | Buff 系统（淘金） | [[Buff制作]] + [[buff-gold-dash-box]]；全部淘金 Buff 见 [[mode-golddash]]（关联 Buff） |
| Totem Buff、BSTotem | Buff 系统（图腾） | [[Buff制作]] + [[buff-totem-combination]]；全部图腾 Buff 见 [[mode-pverogue]]（关联 Buff） |
| 新增 Buff、创建 Buff | Buff 系统（开发） | [[Buff制作]] + [[buff-framework]] |
| AI、Bot、NPC、RoleAI、行为树 | AI 系统（框架） | [[AI制作]] + [[ai-base]] |
| BehaviorAction、Conditional | AI 系统（行为树） | [[AI制作]] + [[ai-behavior]] |
| AI Buff、AI 技能 | AI 系统（AI Buff） | [[AI制作]] + [[ai-buff]] |
| AI 投放、Spawner | AI 系统（投放） | [[AI制作]] + [[ai-spawner]] |
| AI 寻路、Navigation | AI 系统（寻路） | [[AI制作]] + [[ai-navigation]] |
| AutoWar、自动战斗、队友AI | AI 系统（自动战斗） | [[AI制作]] + [[ai-teammate]] + [[autowar-system]] |
| 武器、枪械、射击、弹道、Weapon | 武器系统（射击） | [[射击武器制作]] + [[weapon-shooting]] |
| SOWeaponControl、后坐力、弹匣 | 武器系统（射击配置） | [[射击武器制作]] + [[weapon-shooting]] |
| 双持、WeaponControlMulti | 武器系统（双持） | [[射击武器制作]] + [[weapon-shooting]] |
| 弹体、弹道、BulletControl | 武器系统（弹体） | [[射击武器制作]] + [[weapon-bullet]] |
| 武器皮肤、WeaponSkin | 武器系统（皮肤） | [[weapon-skin]] |
| 近战、FightClose、MeleeWeapon、HitPart | 武器系统（近战框架） | [[近战武器制作]] + [[weapon-melee-framework]] |
| 晾衣杆、火矛、圣剑、长枪、ClothesPole、FlameSpear | 武器系统（近战武器） | [[近战武器制作]] + [[weapon-melee]] |
| 弓、弹射、ElasticWeapon | 武器系统（弹射） | [[特殊武器制作]] + [[weapon-elastic]] |
| 暗器、HiddenWeapon、飞刀、葫芦 | 武器系统（暗器） | [[特殊武器制作]] + [[weapon-hidden]] |
| 射线武器、ZiZiBeng、滋滋棒 | 武器系统（射线） | [[特殊武器制作]] + [[weapon-zizibeng]] |
| 榴弹、FireBallLauncher、火球发射器 | 武器系统（榴弹） | [[特殊武器制作]] + [[weapon-fireball-launcher]] |
| 魔法武器、Harrywand、魔杖 | 武器系统（特殊-魔法） | [[特殊武器制作]] + [[weapon-special]] |
| 手雷、投掷物、Bomb、Grenade、烟雾弹 | 投掷物系统 | [[投掷物制作]] + [[throwable-bomb]] |
| 药品、消耗品、绷带、急救包、止痛药、能量饮料 | 消耗品系统 | [[消耗品制作]] + [[item-consumable]] |
| 配件、瞄准镜、弹匣、枪口、枪托、握把、芯片 | 武器配件系统 | [[武器配件制作]] + [[weapon-attachment]] |
| 防弹衣、头盔、背包、吉利服、护甲 | 角色装备系统 | [[角色装备制作]] + [[role-equipment]] |
| 狗牌、DogTag | 角色装备系统（狗牌） | [[角色装备制作]] + [[role-equipment]] |
| 道具、拾取物、空投、PickItem | 道具系统（框架） | [[item-base]] |
| 战场掉落、LootItem | 道具系统（掉落） | [[item-loot]] |
| GoldDash 道具 | 道具系统（淘金） | [[item-golddash]] |
| 打金道具、金条、祭坛祭品、身份牌、珍宝室钥匙、变异品质 | 道具系统（淘金） | [[打金道具制作]] + [[item-golddash]] |
| 活动道具、ActivityItems、粽子、红包、鞭炮、灯笼、KFC、仙女棒 | 道具系统（活动道具） | [[战场道具制作]] + [[item-activity]] |
| 身份卡、IdCard、英雄卡 | 身份卡系统（框架） | [[身份卡制作]] + [[idcard-framework]] |
| Hades、哈迪斯 | 身份卡（哈迪斯） | [[身份卡制作]] + [[idcard-hades]] |
| Neptune、海神 | 身份卡（海神） | [[身份卡制作]] + [[idcard-neptune]] |
| Zeus、宙斯 | 身份卡（宙斯） | [[身份卡制作]] + [[idcard-zeus]] |
| 诸葛亮、关羽、曹操、吕布 | 身份卡（三国系列） | [[身份卡制作]] + 对应 idcard feature |
| Ganda、Geed、Taiga、Tiga、Zero、Zeta、奥特曼 | 身份卡（奥特曼系列） | [[身份卡制作]] + 对应 idcard feature |
| 彩虹、雪女、诺比鱼、Kitty、太阳神、小丑 | 身份卡（独立卡） | [[身份卡制作]] + 对应 idcard feature |
| UI、界面、窗口、HUD | UI 系统 | `UI 系统内容边界定义.md` |
| 镜头、Camera、跟随、震动、FOV、视距、自由视角 | 镜头系统 | [[镜头系统制作]] + [[camera-system]] |
| 时装、皮肤、换装、Fashion | 时装/皮肤系统 | [[role-skin]] |
| 宠物、Pet | 宠物系统 | [[pet-system]] |
| 新手引导、教程、Tutorial | 新手引导系统 | [[beginner-tutorial]] |
| 技能卡、芯片、特技、AbilityCard | 技能系统 | — |
| 角色技能、RoleSkill、主动技能 | 角色技能系统 | [[role-skill]] |
| 辅助瞄准、AuxiliaryAiming、灵敏度 | 辅助瞄准系统 | [[auxiliary-aiming]] |
| AutoWar、自动战斗、回放 | 自动战斗/回放系统 | [[autowar-system]] |
| 网络、Proto、协议、NetworkClient | 网络框架 | [[网络消息制作]] + [[network-framework]] |
| 网络消息、新增协议、Proto文件、ByteBuffer | 网络框架（开发） | [[网络消息制作]] + [[network-framework]] |
| 反作弊、Cheat、服务端校验 | 服务端反作弊 | [[server-cheat]] |
| 数据上报、Report、NSQ、战斗日志 | 服务端数据上报 | [[server-report]] |
| 调试工具、UnitTest、自动化测试 | 开发工具 | [[dev-tools]] |
| 地图、场景、Scene、天空盒 | 地图/场景系统 | [[mode-common]] |
| 网络、消息、同步、Mirror、RPC | 网络/消息系统 | [[网络消息制作]] + [[network-framework]] |
| 子玩法、SubMode、新模式、模式开发 | 模式系统（子玩法） | [[模式制作]] + [[mode-base]] |
| Utils、工具库、配置系统、Config、Data、基础设施 | 基础设施 | [[基础设施制作]] + [[infra-base]] |
| 对象池、GameObjectPool、LocalSave | 基础设施（工具） | [[基础设施制作]] + [[infra-base]] |

### 代际判断规则

> 意图识别确定系统归属后，**同时判断代际**以决定加载哪套编码规范。

| 系统 | 代际 | 编码规范 | 编码执行者 |
|------|------|---------|-----------|
| 载具/模式/角色/Buff/AI | **1 代** | [[sausage-core-rules]] | DL |
| 武器（射击/近战/特殊） | **1 代** | [[sausage-core-rules]] | DL |
| 投掷物/消耗品/配件/装备/身份卡 | **1 代** | [[sausage-core-rules]] | DL |
| GPO / AI Entity（2 代新实体） | **2 代** | 共享 `core-rules.md` | GPO Agent |
| Ability / AE | **2 代** | 共享 `core-rules.md` | Ability Agent |
| Scene（场景建设） | **2 代** | `scene-code.md` | Scene Agent |
| UI / 网络 / 基础设施 | **两代共存** | 按代码路径判断 | DL（1 代）或对应 Agent（2 代） |

**代码路径判断**：`Assets/Script/Biubiubiu2/` → 2 代；`Assets/Script/`（非 Biubiubiu2） → 1 代。

**⚠️ 高危歧义场景**（必须向用户确认）：

| 用户说了... | 可能是 1 代 | 也可能是 2 代 | 确认问题 |
|------------|-----------|-------------|---------|
| "武器""飞行物" | 1 代射击/近战武器 | 2 代 GPO 单元 | "这是 1 代手持武器还是 2 代 GPO 独立单元？" |
| "刷怪""波次" | 1 代 AI Spawner | 2 代 GPOSpawner | "要用现有 GPOSpawner 框架还是 1 代 AI 投放？" |
| "Buff""效果" | 1 代 BS/BSO 系统 | 2 代 Ability AE | "这是 1 代 Buff 还是 2 代 Ability 持续效果？" |

---

## 三、已有实例清单

> 接到新开发需求时，**先查本章**确认是否有可复用的已有实例。
> 每行的 `feature` 列指向对应的 feature.md wiki-link。
> 聚合 feature（共享控制器、仅 SO 差异）只占一行，不逐实例展开。

### §3.1 载具系统清单

> 载具分为两套体系：地面（BuggyCarController / MotorCarController / AnimalCarSetting）和飞行（FlyVehicle / DragonControl），详见 [[载具制作]]

| 名称 | 说明 | feature |
|------|------|---------|
| Buggy 家族 | Jeep/Buggy/ArmoredBus/JetCar/Kayak，共享 BuggyCarController | [[car-buggy-family]] |
| Motor 家族 | HoverBoard/PonyVehicle/NeptuneShark，共享 MotorCarSetting | [[car-motor-family]] |
| 动物家族 | Raptors/SwordTiger/TRexKing/Triceratops/MotoSheep，共享 AnimalCarSetting | [[car-animal-family]] |
| 机甲载具 | Machine_Carrier/Machine_Robot/CyberTitan，独立 RobotNet | [[car-robot]] |
| 飞行框架 | FlyVehicle 基类，统一飞行物理 | [[fly-vehicle]] |
| 飞龙 | Dragon，独立 DragonControl.cs 控制器 | [[car-dragon]] |
| 翼龙 | Peterosaur，继承 FlyVehicle | [[car-peterosaur]] |
| 飞燕号 | GutsWing，继承 FlyVehicle，蓄力弹/炸弹 | [[car-gutswing]] |
| 神龙 | ShenLong，继承 FlyVehicle | [[car-shenlong]] |
| 飞行扫帚 | FlyingBroom，继承 FlyVehicle | [[car-flyingbroom]] |
| 载具射击 | 载具武器系统（载具射击/炮管） | [[car-shoot]] |
| GoldDash 载具 | 撤离模式专属载具配置 | [[car-golddash]] |
| 特殊标记 | AirShip/AlienWarship/FlyingCarpet/CircusBall 标记组件 | [[car-special]] |

### §3.2 游戏模式清单

> 模式采用 **Manager → Stage → Logic → Data 四层架构**，详见 [[模式制作]]

| 名称 | GameMode 枚举 | 文件数(C/S/H) | feature |
|------|---|---|---|
| 经典 BR | Classic | — | [[mode-classic]] |
| 模式通用 | — | — | [[mode-common]] |
| 撤离模式 | GoldDash=28 | 125/126/13 | [[mode-golddash]] |
| 快速撤离 | FastGoldDash | 13/17/4 | [[mode-golddash-fast]] |
| 新手训练营 | RookieCamp | 63/5/— | [[mode-rookiecamp]] |
| 暴打猛兽营 | BeatCamp=45 | 40/19/19 | [[mode-beatbeastcamp]] |
| 竞速模式 | OnlyUp=40 | 35/25/5 | [[mode-onlyup]] |
| 足球派对 | LimitedtimeFifamode=19 | 28/24/9 | [[mode-footballparty]] |
| 互动大厅 | InteractionSpace=25 | 28/25/3 | [[mode-sociallobby]] |
| PVE 肉鸽 | Pvemode=23 | 21/31/13 | [[mode-pverogue]] |
| 痛击飞球 | Bladeballmode=24 | 17/48/— | [[mode-bladeball]] |
| 闯关吧！ | GogoParty=47 | 17/19/— | [[mode-gogoparty]] |
| 团队激斗进阶 | PartyMode(IsEvo) | 14/14/3 | [[mode-evodeathmatch]] |
| 爆破模式 | Defusalmode=34 | 11/15/— | [[mode-defusal]] |
| 团队模式 | TeamMode | 11/21/— | [[mode-teammode]] |
| 枪王之王 | Bullfighting=43 | 10/13/— | [[mode-bullfighting]] |
| PK之王 | Turnbased=33 | 9/11/— | [[mode-turnbased]] |
| 自定义阵营 | CampCustomized=42 | 5/8/— | [[mode-customroomcamp]] |
| 奥特派对 | Ultrafight=20 | 10/14/— | [[mode-ultrafight]] |
| 狼人派对 | LimitedtimeWolfparty=17 | 27/28/12 | [[mode-wolfparty]] |
| 淘汰赛 | LimitedtimeKnockout=14 | 13/24/42 | [[mode-knockout]] |
| 运动派对 | SportsParty | 6/16/17 | [[mode-sportsparty]] |

### §3.3 角色系统清单

> 角色采用 **双层 Component 架构**：BattleRole (44 表现组件) + BattleRoleLogic (25 逻辑组件)，详见 [[角色制作]]

| 子系统 | 说明 | feature |
|--------|------|---------|
| 角色框架 | 双层 Component 架构、BattleRole/BattleRoleLogic 核心类 | [[role-base]] |
| 伤害系统 | HP/护甲/伤害计算/击倒 | [[role-damage]] |
| 死亡/复活 | 死亡流程/复活逻辑/淘汰 | [[role-death]] |
| 状态管理 | 站/蹲/趴/状态切换 | [[role-state]] |
| 移动控制 | 移动方向/速度/同步 | [[role-movement]] |
| 游泳 | 水面检测/游泳状态 | [[role-swim]] |
| 飞行 | 跳伞/飞行状态/BoxingFly | [[role-fly]] |
| 皮肤/换装 | 角色皮肤/DuoBao/换装 | [[role-skin]] |
| 动画系统 | Animator/Playable API/IK | [[role-animation]] |
| 动画控制器 | AnimatorController 层配置 | [[role-animator]] |
| Motion | 动画状态机/Motion State | [[role-motion]] |
| 物理/碰撞 | HitBox/CapsuleMove/Ragdoll | [[role-physics]] |
| 渲染/模型 | 模型加载/描边/尺寸缩放 | [[role-render]] |
| 网络同步 | RoleNet/重连处理 | [[role-network]] |
| 反作弊 | RoleCheat | [[role-cheat]] |
| 救援/扶人 | Uprear/倒地扶起 | [[role-uprear]] |
| 队友代管 | Teammate 行为/移动/武器/开火 | [[role-teammate]] |

### §3.4 AI 系统清单

> AI 采用行为树驱动，详见 [[AI制作]]

| 子系统 | 说明 | feature |
|--------|------|---------|
| AI 框架 | RoleAI 基类/AI 状态管理 | [[ai-base]] |
| 行为树 | BehaviorAction/Conditional 节点 | [[ai-behavior]] |
| AI Buff | AI 专属 Buff 逻辑 | [[ai-buff]] |
| 寻路 | Navigation/路径规划 | [[ai-navigation]] |
| 投放 | AI Spawner/刷怪点 | [[ai-spawner]] |
| 队友 AI | AutoWar/自动战斗/代管 | [[ai-teammate]] |

### §3.5 武器系统清单

> 详见 [[射击武器制作]] · [[近战武器制作]] · [[特殊武器制作]]

| 名称 | 说明 | feature |
|------|------|---------|
| 武器框架 | WeaponBase/武器管理/切换 | [[weapon-base]] |
| 射击武器 | 47 个 SOWeaponControl（7 WeaponType），共享 WeaponControl.cs | [[weapon-shooting]] |
| 弹体系统 | BulletManager/BulletControl/弹道物理 | [[weapon-bullet]] |
| 武器皮肤 | WeaponSkin/武器外观 | [[weapon-skin]] |
| 近战框架 | FightClose C/S 镜像（Data/Logic/Stage 三层） | [[weapon-melee-framework]] |
| 近战武器 | 晾衣杆/火矛/圣剑/长枪（各有独立 SO 和类） | [[weapon-melee]] |
| 弹射武器 | ElasticWeapon（弓箭），蓄力→抛物线弹体 | [[weapon-elastic]] |
| 暗器 | HiddenWeapon（飞刀/葫芦/水晶球/雷符），Buff 伤害 | [[weapon-hidden]] |
| 射线武器 | ZiZiBeng（滋滋棒/聚焦枪），持续射线 | [[weapon-zizibeng]] |
| 榴弹发射器 | FireBallLauncher，单发 5s CD AOE | [[weapon-fireball-launcher]] |
| 特殊武器（其他） | 魔法/传说/特殊发射类，共享 WeaponControl | [[weapon-special]] |
| 武器配件 | 瞄准镜/弹匣/枪口/枪托/握把/芯片 | [[weapon-attachment]] |

### §3.6 道具系统清单

| 子系统 | 说明 | feature |
|--------|------|---------|
| 道具框架 | ItemPool/SOItemDataConfig/拾取 | [[item-base]] |
| 消耗品 | 绷带/急救包/止痛药/能量饮料/变身药剂 | [[item-consumable]] |
| 角色装备 | 防弹衣/头盔/背包/吉利服/狗牌 | [[role-equipment]] |
| 投掷物 | 手雷/烟雾弹/BlastBomb | [[throwable-bomb]] |
| 战场掉落 | LootItem/掉落物 | [[item-loot]] |
| GoldDash 道具 | 撤离模式专属道具 | [[item-golddash]] |
| 战场活动道具 | 节日/活动限定道具(粽子/红包等) | [[item-activity]] |

### §3.7 身份卡清单

> 29 种身份卡，详见 [[身份卡制作]]

| 名称 | Sign | 技能类型 | feature |
|------|------|---------|---------|
| 哈迪斯 | Hades | 火墙 | [[idcard-hades]] |
| 海神 | Neptune | 水龙卷 | [[idcard-neptune]] |
| 宙斯 | Zeus | 雷电 | [[idcard-zeus]] |
| 诸葛亮 | ZhugeLiang | 火攻 | [[idcard-zhugeliang]] |
| 关羽 | GuanYu | 冲锋 | [[idcard-guanyu]] |
| 曹操 | CaoCao | 指挥 | [[idcard-caocao]] |
| 吕布 | LvBu | 突进 | [[idcard-lvbu]] |
| 忍者 | Ninja | 潜行 | [[idcard-ninja]] |
| 奥特曼迪迦 | Tiga | 变身 | [[idcard-tiga]] |
| 奥特曼盖亚 | Ganda | 飞行 | [[idcard-ganda]] |
| 奥特曼杰德 | Geed | 光线 | [[idcard-geed]] |
| 奥特曼泰迦 | Taiga | 手雷 | [[idcard-taiga]] |
| 奥特曼赛罗 | Zero | 冲刺 | [[idcard-zero]] |
| 奥特曼泽塔 | Zeta | 变身 | [[idcard-zeta]] |
| 彩虹 | Rainbow | 彩虹桥 | [[idcard-rainbow]] |
| 雪女 | SnowGirl | 冰冻 | [[idcard-snowgirl]] |
| 诺比鱼 | NoobFish | 摊位 | [[idcard-noobfish]] |
| Kitty | Kitty | 跳跃/雷达 | [[idcard-kitty]] |
| 太阳神 | SunGod | 光线 | [[idcard-sungod]] |
| 小丑 | Clown | 手雷/平台 | [[idcard-clown]] |
| 飞侠 | FlyMan | 飞行 | [[idcard-flyman]] |
| 跑酷 | PaoKu | 冲刺 | [[idcard-paoku]] |
| 砂忍 | Sand | 潜地 | [[idcard-sand]] |
| 爱德美 | AidMei | 加速 | [[idcard-aidmei]] |
| 船长卡 | CaptainCard | 幽灵/火焰/回血 | [[idcard-captaincard]] |
| 博士 | DoctorWho | 传送 | [[idcard-doctorwho]] |
| 唐僧 | TangSeng | 法术 | [[idcard-tangseng]] |
| 狼人 | WolfMan | 变身 | [[idcard-wolfman]] |
| 卡度拉 | Kadura | 力量 | [[idcard-kadura]] |

### §3.8 Buff 系统清单

> 245 个 Buff feature。**功能专属 buff 挂在对应消费者 feature 的「关联 Buff」段落**，Agent 从功能入口直接找到该功能用到的全部 buff。通用 buff 挂在 [[buff-framework]]。

#### 功能专属 Buff（按消费者分组）

| 消费者 feature | buff 数 | 分类来源 |
|---------------|---------|---------|
| [[mode-golddash]] | 25 | buff/golddash |
| [[mode-pverogue]] | 73 | buff/pve + buff/totem + buff/dungeon |
| [[mode-beatbeastcamp]] | 3 | buff/beatbeast |
| [[mode-bladeball]] | 3 | buff/bladeball |
| [[mode-bullfighting]] | 2 | buff/boxing |
| [[idcard-ganda]] | 3 | buff/ganda |
| [[idcard-kitty]] | 2 | buff/kitty |
| [[idcard-noobfish]] | 4 | buff/noobfish |
| [[idcard-tangseng]] | 3 | buff/tangseng |
| [[idcard-wolfman]] | 4 | buff/wolfparty |
| [[idcard-clown]] | 4 | buff/role-skill (clown) |

#### 通用 Buff（挂在 buff-framework）

| 分类 | 数量 | 说明 |
|------|------|------|
| buff/combat | 15 | 击退/范围伤害/爆炸 |
| buff/movement | 7 | 冲刺/加速/位移 |
| buff/defense | 5 | 护盾/减伤 |
| buff/visual | 9 | 特效/物体生成 |
| buff/item | 23 | 道具/场景交互 |
| buff/misc | 50 | 通用/杂项 |

→ 详见 [[buff-framework]] 的「关联 Buff」段落（109 个）

#### 独立分类索引（无明确消费者）

| 分类 | 数量 | 索引 |
|------|------|------|
| buff/cybertitan | 1 | [[_index-buff-cybertitan]] |
| buff/gourd | 2 | [[_index-buff-gourd]] |
| buff/magic | 4 | [[_index-buff-magic]] |
| buff/malouparty | 2 | [[_index-buff-malouparty]] |

### §3.9 GPO / AB / AE 功能清单（⚠️ 2 代专属，本项目暂无实例）

> GPO 见 `UGC GPO 系统内容边界定义.md`，AB/AE 见 `Ability 系统内容边界定义.md`。待 2 代功能上线后填充。

### §3.10 通用系统清单

| 名称 | 说明 | feature |
|------|------|---------|
| 网络框架 | Proto 协议定义、NetworkClient/Server 基类、Buffer/RTT | [[network-framework]] |
| 服务端反作弊 | 移动/伤害/速度校验、各模式反作弊 | [[server-cheat]] |
| 服务端数据上报 | 战斗日志、NSQ 上报、统计 | [[server-report]] |
| 新手引导 | 脚本化引导事件、触发器、UI 提示 | [[beginner-tutorial]] |
| 宠物系统 | 战场宠物 SO 配置、跟随逻辑 | [[pet-system]] |
| 角色技能 | 身份卡技能 BS、技能冷却、技能 UI | [[role-skill]] |
| 辅助瞄准 | 灵敏度控制、自动追踪、辅助瞄准状态机 | [[auxiliary-aiming]] |
| 自动战斗/回放 | AutoWar AI 托管、战斗回放录制播放 | [[autowar-system]] |
| 开发工具 | AutomationTools、UnitTest、Utils | [[dev-tools]] |

---

## 四、系统依赖关系

> 被依赖的系统优先生成。

```
基础层（被大量依赖）
  ├─ 配置/数据层 → 几乎所有系统依赖
  ├─ 网络/消息   → 几乎所有系统依赖（C/S/H 三端通信）
  └─ UI 系统     → 被大量系统依赖（HUD/窗口/结算）

核心实体层
  ├─ 角色系统 ← 被模式/载具/AI/武器/Buff/装备依赖
  └─ Buff 系统 ← 被模式/载具/角色技能/身份卡/消耗品依赖

战斗层
  ├─ 武器/战斗 → 依赖角色+Buff ← 被AI/道具依赖
  ├─ 投掷物    → 依赖Buff+角色+道具
  ├─ 消耗品    → 依赖Buff+角色+道具
  ├─ 武器配件  → 依赖武器+道具
  ├─ 角色装备  → 依赖道具+角色+Buff
  └─ 身份卡    → 依赖Buff+角色+装备+投掷物

功能层
  ├─ 道具系统 → 依赖配置/数据层 ← 被武器/投掷物/消耗品/配件/装备依赖
  ├─ AI 系统  → 依赖角色+武器+模式
  ├─ 载具系统 → 依赖角色+UI+Buff+网络
  └─ 模式系统 → 依赖配置+网络+角色+UI ← 被各模式实例依赖

表现层
  ├─ 时装/皮肤 → 依赖角色
  ├─ 镜头系统  → 独立
  ├─ 地图/场景  → 独立
  └─ 宠物/背包/新手引导/技能 → 子系统
```

### 生成顺序

| 优先级 | 系统 | 原因 |
|-------|------|------|
| 1 | 角色系统 | 核心实体，被几乎所有系统依赖 |
| 2 | Buff 系统 | 战斗核心，被模式/载具/角色技能等依赖 |
| 3 | 模式系统 | 所有玩法的基础 |
| 4 | 武器/战斗 | 核心战斗逻辑 |
| 5 | 道具系统 | 战场核心 |
| 6 | AI 系统 | 依赖角色+武器 |
| 7 | 载具系统 | 依赖角色+Buff |
| 8 | 投掷物/消耗品/配件/装备/身份卡 | 战斗子系统 |
| 9 | UI/时装/镜头/地图/其他 | 表现层/子系统 |

---

*文档版本：v2.1（§二意图识别表消除全部「同上」精确到 feature wiki-link；§三实例清单重构：补角色17子系统/AI 6子系统/武器12子系统/道具6子系统/Buff 245分类汇总；载具按 feature 粒度合并为13行；修正指向错误）*
*构建方式：运行 knowledge 构建工作流（[[workflow-knowledge]]）填充实际内容*
