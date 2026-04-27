# 项目资源分布地图 (Resource Map)

> **用途**：Knowledge 构建 & 制作文档编写时快速查找各系统的资源路径
> **数据来源**：`Assets/Script/Asset/Loaders/*.cs` (运行时加载入口) + `SubpackageGroupsBuilder.cs` (分包规则) + 目录实际扫描
> **维护规则**：发现新路径时追加，标注 `[待验证]` 直到实际确认

---

## 〇、项目资源架构总览

### 顶层目录结构

```
Assets/
├── Art/            (327,796 files)  ← 美术资源原始文件（模型/材质/预制体模板）
├── Audio/          (19,720 files)   ← 音频资源（Wwise）
├── Scenes/         (315,479 files)  ← 场景文件 + 场景拆分输出
├── Script/         (38,862 files)   ← 代码（含 1 代 + 2 代）
├── ToBundle/       (230,844 files)  ← 🏆 AssetBundle 打包根目录（运行时加载的主要来源）
├── Shaders/        (1,396 files)    ← Shader 文件
├── Resources/      (224 files)      ← Resources 直接加载（少量）
└── ServerScene/    (632 files)      ← ⚠️ 旧碰撞数据（仅 4 岛），服务端场景已统一至 Scenes/Biubiubiu2/
```

### ToBundle 子目录（运行时资源核心）

> 📊 以下数据基于 2024 年全量目录扫描（非 .meta 文件计数）

```
ToBundle/                          ← 22 个顶层目录
├── AutoPerf/       (1)            ← 自动性能测试
├── Biubiubiu2/     (2,812)        ← 2 代框架层运行时资源
│   ├── GoldDash/   (1,335)        ← 淘金模式
│   ├── GamePlay/   (1,211)        ← 玩法数据
│   └── Configs/    (199)          ← 配置
├── BuiltIn/        (4)            ← 内建预制体
├── CI/             (2)            ← CI 视频
├── Config/         (1,911)        ← 配置
│   ├── Txt/        (1,166)        ← 📋 配置表（txt 格式，SO→Table 生成）
│   └── Editor/     (745)          ← 编辑器配置
├── Editor/         (124)          ← 编辑器专用资源
├── Effect/         (28,701)       ← ✨ 特效预制体（66 个子目录，见附录 C）
├── Fashion/        (22,643)       ← 👗 时装/皮肤（21 个部位子目录，见 §十四）
├── GameBase/       (4)            ← 基础运行时对象（StartGame/RoleCamera/ButtleLayer）
├── GamePlayItem/   (1,353)        ← 🎮 玩法道具预制体（20 个子目录）
├── Global/         (144)          ← 全局资源（SO 84 + Config 29 + Video 31）
├── Items/          (480)          ← 物品预制体（17 个子目录）
├── Map/            (106)          ← 地图数据（天空盒/空气墙/POI）
├── Mat/            (12)           ← 杂项材质
├── Role/           (2,155)        ← 🎭 角色（Controller 1837 + AnimGraph 287）
├── RoleAI/         (121)          ← 🤖 AI（Prefab 43 + Animator 39 + AIBehavior 23）
├── ScriptableObject/ (4,241)      ← 📋 ScriptableObject 配置（48 个子目录，见附录 D）
├── Skin/           (5,741)        ← 皮肤预制体
│   ├── Items/      (1,763)        ← 道具皮肤
│   ├── PickItems/  (1,947)        ← 拾取物皮肤
│   ├── ItemsH/     (1,708)        ← H 版道具皮肤
│   └── Cars/       (323)          ← 🚗 载具皮肤
├── Standalone/     (208)          ← 独立资源（Video 64 + UGUI 58 + SO 36）
├── Tarkov/         (5)            ← Tarkov 玩法
├── UGUI/           (35,449)       ← 🖥️ UI 资源（见 §八）
│   ├── Sprite/     (24,380)       ← 散图
│   ├── Texture/    (5,444)        ← UI 纹理
│   ├── Widgets/    (3,194)        ← UI 组件预制体
│   ├── Font/       (648)          ← 字体
│   ├── Windows/    (612)          ← UI 窗口预制体
│   ├── Animation/  (598)          ← UI 动画
│   ├── Atlas/      (472)          ← SpriteAtlas 图集
│   └── Elements/ Materials/ Skeleton/ UIAdapter/ Editor/ GameIcons/
└── Video/          (75)           ← 视频资源（含 VideoSubtitle 25）
```

### 资源加载体系

- **加载入口**：`AssetsLoad` (partial class，分布在 20 个 Loader 文件中)
- **加载方式**：`AssetManager.LoadAsset<T>()` (同步) / `AssetManager.LoadAssetAsync<T>()` (异步)
- **对象池**：`CarPool` (载具)、`ItemPool` (物品)、`EffectPool` (特效)
- **分包工具**：`SubpackageGroupsBuilder` → `SubpackageGroups.txt`

---

## 一、载具系统 (B5 ✅)

> **Loader**：`CarLoader.cs`
> **制作文档**：[[载具制作]]

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Car/` | 客户端载具逻辑 |
| | `Script/GamePlay/Server/Modules/Car/` | 服务端载具逻辑 |
| | `Script/UI/PlayerControl/Control/VehicleStateButtonControl.cs` | 载具输入控制 |
| **配置表** | `ToBundle/Config/Txt/SOCarData.txt` | 载具数值 |
| | `ToBundle/Config/Txt/SOCarSkill.txt` | 载具技能配置 |
| | `ToBundle/Config/Txt/SOCarSkinData.txt` | 皮肤映射 |
| | `ToBundle/Config/Txt/CarItemAsset.txt` | Bundle 路径映射 |
| | `ToBundle/Config/Txt/CarSkinH.txt` | H 版皮肤 |
| | `ToBundle/Config/Txt/GolddashCarData.txt` | 淘金载具数据 |
| | `ToBundle/Config/Txt/GolddashMotorCarSetting.txt` | 淘金载具设置 |
| | `ToBundle/Config/Txt/GolddashRoleCarSetting.txt` | 淘金角色载具设置 |
| | `ToBundle/Config/Txt/BattleUiVehicleOptions.txt` | 战斗 UI 载具选项 |
| | `ToBundle/Config/Txt/SOAGVehicleSlot.txt` | AG 载具槽位 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Vehicle/` (38 files) | 载具物理配置 (MotorCarSetting) |
| | `ToBundle/ScriptableObject/Biological_Carrier/` (208 files) | 生物载具配置 |
| **预制体** | `ToBundle/Skin/Cars/{Sign}/` | 载具皮肤预制体 (运行时) |
| | `Art/Carrier/Template/` | 载具模板预制体 (编辑器) |
| | `ToBundle/GamePlayItem/CarResource/CarController/` | 载具动画控制器 |
| | `ToBundle/GamePlayItem/AirShip/` | 空艇预制体 |
| **特效** | `ToBundle/Effect/Carrier/` (1,473 files) | 载具特效（按载具分子目录） |
| | `ToBundle/Effect/BiologicalVehicle/` (151 files) | 生物载具特效 |
| | `ToBundle/Effect/Aerocraft/` (797 files) | 飞行器特效 |
| **飞行器** | `ToBundle/GamePlayItem/Aerocraft/` (197 files) | 飞行器预制体 |
| | `ToBundle/GamePlayItem/AirShip/` (5 files) | 空艇预制体 |
| | `ToBundle/GamePlayItem/AirPlane/` (5 files) | 飞机预制体 |
| **UI 图标** | `ToBundle/UGUI/Sprite/Car/` | HUD 能源标识 |
| | `ToBundle/UGUI/Sprite/Weapon/` | 地图标记标识 |
| | `ToBundle/UGUI/Sprite/Item/ItemBase/` | 道具表图标 |
| **地图投放** | `ToBundle/ScriptableObject/SOCreateObjData/` (42 files) | 载具生成概率 |
| | `ToBundle/ScriptableObject/LevelData/` | 关卡投放数据 |

---

## 二、模式系统 (B1 📋)

> **Loader**：`ModeConfigLoader.cs` + `WarLoader.cs` + `PveModeLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Mode/` (~471 files) | 客户端模式逻辑 |
| | `Script/GamePlay/Server/Modules/Mode/` (~470 files) | 服务端模式逻辑 |
| | `Script/GamePlay/Host/Modules/Mode/` (~82 files) | 主机端模式逻辑 |
| **配置表** | `ToBundle/Config/Txt/GameMode.txt` | 模式定义 |
| | `ToBundle/Config/Txt/GameModeRule.txt` | 模式规则 |
| | `ToBundle/Config/Txt/GameModeTab.txt` | 模式 Tab 页 |
| | `ToBundle/Config/Txt/MatchMode.txt` | 匹配模式 |
| | `ToBundle/Config/Txt/MatchType.txt` | 匹配类型 |
| | `ToBundle/Config/Txt/GameMap.txt` | 游戏地图 |
| | `ToBundle/Config/Txt/Map.txt` | 地图表 |
| | `ToBundle/Config/Txt/ShowMode.txt` | 展示模式 |
| | `ToBundle/Config/Txt/EntryMode.txt` | 入口模式 |
| | `ToBundle/Config/Txt/ClassicGameModeFlag.txt` | 经典模式标记 |
| | `ToBundle/Config/Txt/GameScene.txt` | 游戏场景 |
| | `ToBundle/Config/Txt/Scene.txt` | 场景表 |
| | `ToBundle/Config/Txt/CustomRoom.txt` | 自定义房间 |
| | `ToBundle/Config/Txt/CgMatchMode.txt` | CG 匹配模式 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Mode/` (926 files) | 模式配置 |
| | `ToBundle/ScriptableObject/Screen/ModeSetting/` | 模式画面设置 |
| | `ToBundle/ScriptableObject/Screen/GameSetting/` | 游戏设置 |
| | `ToBundle/ScriptableObject/CommonMode/` | 通用模式 MVP 配置 |
| | `ToBundle/ScriptableObject/ModeToolMap/` (3 files) | 模式工具映射 |
| | `ToBundle/ScriptableObject/Screen/ModeSetting/` (24 files) | 模式画面设置 |
| | `ToBundle/ScriptableObject/Screen/GameSetting/` (140 files) | 游戏全局设置 |
| | `ToBundle/ScriptableObject/Screen/SOGunfightRoundData/` (54 files) | 枪战回合数据 |
| | `ToBundle/ScriptableObject/Screen/SOWolfParty/` (15 files) | 狼人派对配置 |
| | `ToBundle/ScriptableObject/Screen/SOHypoxia/` (3 files) | 缺氧配置 |
| | `ToBundle/ScriptableObject/Screen/MapBuffs/` (1 file) | 地图Buff配置 |
| | `ToBundle/ScriptableObject/Screen/MapCovers/` (1 file) | 地图掩体配置 |
| **预制体** | `ToBundle/GameBase/Base/` | 基础运行时对象 (StartGame 等) |
| | `ToBundle/GameBase/Pool/` | 对象池预制体 |
| **特效** | `ToBundle/Effect/Mode/` (284 files) | 模式通用特效 |
| | `ToBundle/Effect/BeastCamp/` (18 files) | 打怪兽特效 |
| | `ToBundle/Effect/De_C4/` (24 files) | 拆弹模式特效 |
| | `ToBundle/Effect/RookieCamp/` (19 files) | 新兵营特效 |
| | `ToBundle/Effect/SportParty/` (2 files) | 运动派对特效 |
| | `ToBundle/Effect/GameStartShow/` (60 files) | 游戏开场展示特效 |
| | `ToBundle/Effect/War/` (187 files) | 战场通用特效 |
| | `ToBundle/Effect/WarTakeoffPhase/` (2 files) | 起飞阶段特效 |
| **UI** | `ToBundle/UGUI/Texture/Maps/` | 地图缩略图 |

### 模式专属子目录 (Mode/ 下按模式划分)

```
ToBundle/ScriptableObject/Mode/
├── BeatBeastCamp/     ← 打怪兽
├── BladeBallMode/     ← 刀锋球
├── DefusalMode/       ← 拆弹
├── GoldDash/          ← 淘金
├── PveRogue/          ← PVE 肉鸽
├── RookieCamp/        ← 新兵营
├── SportsParty/       ← 运动派对
└── ...
```

---

## 三、角色系统 (B2 📋)

> **Loader**：`RoleLoader.cs` + `AnimationLoader.cs` + `FashionLoader.cs`
> **动画池**：`AnimatorPool.cs` — 按游戏模式预加载不同的 RuntimeAnimatorController

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Role/` (~129 files) | 客户端角色逻辑 |
| | `Script/GamePlay/Server/Modules/Role/` | 服务端角色逻辑 |
| | `Script/GamePlay/Host/Modules/Role/` (~176 files) | 主机端角色逻辑 |
| | `Script/Asset/GameObjectPools/AnimatorPool.cs` | ⚠️ 动画控制器池（按模式分发 Animator） |
| **配置表** | `ToBundle/Config/Txt/RoleAnimation.txt` | 角色动画 |
| | `ToBundle/Config/Txt/RoleAnimationEvent.txt` | 动画事件 |
| | `ToBundle/Config/Txt/RoleClipAsset.txt` | 动画 Clip 资产 |
| | `ToBundle/Config/Txt/RoleControllerAsset.txt` | ⚠️ 控制器资产（AnimatorPool.GetFashionController 读取） |
| | `ToBundle/Config/Txt/RoleState.txt` | 角色状态 |
| | `ToBundle/Config/Txt/RoleStateForbidFunc.txt` | 状态禁止功能 |
| | `ToBundle/Config/Txt/RoleSitType.txt` | 坐姿类型 |
| | `ToBundle/Config/Txt/RoleCheckOperate.txt` | 操作检查 |
| | `ToBundle/Config/Txt/RoleUprearEffect.txt` | 站起特效 |
| | `ToBundle/Config/Txt/DoubleRoleControllerPosition.txt` | 双人骑乘位置 |
| | `ToBundle/Config/Txt/SORoleSkill.txt` | 角色技能 |
| | `ToBundle/Config/Txt/IdCardSkin.txt` | 身份卡皮肤 |
| | `ToBundle/Config/Txt/IdCardSkinFashion.txt` | 身份卡时装 |
| | `ToBundle/Config/Txt/FashionAsset.txt` | 时装资产 |
| | `ToBundle/Config/Txt/FashionInfo.txt` | 时装信息 |
| | `ToBundle/Config/Txt/FashionEffect.txt` | 时装特效 |
| | `ToBundle/Config/Txt/FashionSet.txt` | 时装套装 |
| | `ToBundle/Config/Txt/FashionPartDefault.txt` | 默认部件 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Misc/SORoleBaseData.asset` | ⚠️ 角色基础数据 |
| | `ToBundle/ScriptableObject/Misc/SoRoleBasePcData.asset` | PC 端角色数据 |
| | `ToBundle/ScriptableObject/Misc/SORoleSpecialBaseData.asset` | 特殊角色基础数据 |
| | `ToBundle/ScriptableObject/Misc/SORoleSandConfig.asset` | 角色沙漠配置 |
| | `ToBundle/ScriptableObject/Misc/SkinHAniConfig.asset` | 皮肤动画配置 |
| | `ToBundle/ScriptableObject/Misc/SOSkinLodConfig.asset` | 皮肤 LOD 配置 |
| | `ToBundle/ScriptableObject/CustomAnimData/` | 自定义动画数据 |
| **预制体** | `ToBundle/Role/Prefabs/` | 角色预制体（HTR_withVest_box 等） |
| | `ToBundle/Role/Materials/` | 角色材质 |
| | `ToBundle/Role/AnimGraphData/` | AnimGraph 动画数据 |
| | `ToBundle/Role/HqParachute/` | 高清降落伞 |
| | `ToBundle/Fashion/` (51,423 files) | 时装资源 |
| **动画控制器** | `ToBundle/Role/Controllers/Fashion/` | 时装动画控制器 |
| | `ToBundle/Role/Controllers/War/AutoGen/` | ⚠️ 默认控制器（Classic/Fast/WeaponUpgrade） |
| | `ToBundle/Role/Controllers/War/AI/` | AI 通用控制器 |
| | `ToBundle/Role/Controllers/War/BirthIsland/` | 出生岛 AI 控制器 |
| | `ToBundle/Role/Controllers/War/TimeMode/` | 团队/自由模式控制器 |
| | `ToBundle/Role/Controllers/War/Football/` | 足球模式控制器 |
| | `ToBundle/Role/Controllers/War/BladeBallMode/` | 刀球模式控制器 |
| | `ToBundle/Role/Controllers/War/FightClose/` | 近战模式控制器 |
| | `ToBundle/Role/Controllers/War/PveMode/` | PVE 模式控制器 |
| | `ToBundle/Role/Controllers/War/DeMode/` | 拆弹模式控制器 |
| | `ToBundle/Role/Controllers/War/OnlyUp/` | OnlyUp 模式控制器 |
| | `ToBundle/Role/Controllers/War/GoldDash/` | 淘金模式控制器 |
| | `ToBundle/Role/Controllers/War/MouseHole/` | 鼠洞模式控制器 |
| | `ToBundle/Role/Controllers/War/TimeModeBeastCamp/` | 兽营模式控制器 |
| | `ToBundle/Role/Controllers/War/GoGoParty/` | GoGo 派对控制器 |
| | `ToBundle/Role/Controllers/War/Malou/` | 狼人 Malou 控制器 |
| | `ToBundle/Role/Controllers/War/TeachingMode/` | 教学模式控制器 |
| | `ToBundle/Role/Controllers/War/Ultrafight/` | 极限格斗控制器 |
| | `ToBundle/Role/Controllers/War/Guide/` | 引导控制器 |
| | `ToBundle/Role/Controllers/War/ShadowCopy/` | 影分身控制器 |
| | `ToBundle/Role/Controllers/War/HandInHand/` | 牵手控制器 |
| | `ToBundle/Role/Controllers/War/XCC/` | XCC 控制器 |
| | `ToBundle/Role/Controllers/War/CPSkinAerocraft/` | CP 皮肤飞行器控制器 |
| **特效** | `ToBundle/Effect/RoleAnimation/` (3,841 files) | 角色动画特效 |
| | `ToBundle/Effect/Fashion/` (21,022 files) | 时装特效 |
| | `ToBundle/Effect/Expression/` (1,870 files) | 表情特效 |

> **⚠️ AnimatorPool 模式分发规则**：每个游戏模式加载特定的 AnimatorController，由 `AnimatorPool.PreloadAnimController()` 中的 switch-case 决定。新增模式时必须在此处添加对应分支并创建 `Controllers/War/{ModeName}/` 目录。`RoleControllerAssetConfig`（读取 `RoleControllerAsset.txt`）用于时装 Fashion 控制器的动态查找。

---

## 四、Buff/技能系统 (B3 📋)

> **Loader**：`ConfigLoader.cs` (buffPath)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Buff/` (~268 files) | 客户端 Buff |
| | `Script/GamePlay/Server/Modules/Buff/` (~285 files) | 服务端 Buff |
| | `Script/GamePlay/Host/Modules/Buff/` (~477 files) | 主机端 Buff |
| | `Script/GamePlay/Client/Modules/RoleSkill/` | 角色技能 |
| **配置表** | `ToBundle/Config/Txt/BuffAsset.txt` | Buff 资产 |
| | `ToBundle/Config/Txt/SORoleSkill.txt` | 角色技能 |
| | `ToBundle/Config/Txt/ExpandSkillConfig.txt` | 扩展技能 |
| | `ToBundle/Config/Txt/SkillTutorial.txt` | 技能教程 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Buff/` (2,734 files) | Buff 配置资产 |
| | `ToBundle/ScriptableObject/Screen/SkillConfig/` | 技能画面配置 |
| **特效** | `ToBundle/Effect/Buff/` (293 files) | Buff 特效 |
| | `ToBundle/Effect/Buff_S6_TransmitDoor/` (23 files) | S6 传送门 Buff 特效 |
| | `ToBundle/Effect/BlindingShield/` (3 files) | 致盲盾 Buff 特效 |
| | `ToBundle/Effect/Feedingbottle/` (4 files) | 奶瓶 Buff 特效 |

---

## 五、AI 系统 (B4 📋)

> **Loader**：`ConfigLoader.cs` (roleAIPath)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/RoleAI/` (~214 files) | 客户端 AI |
| | `Script/GamePlay/Server/Modules/RoleAI/` (~108 files) | 服务端 AI |
| | `Script/GamePlay/AutoWar/` | 自动战斗 |
| **配置表** | `ToBundle/Config/Txt/AIWeaponConfig.txt` | AI 武器配置 |
| | `ToBundle/Config/Txt/AIWeaponSkin.txt` | AI 武器皮肤 |
| | `ToBundle/Config/Txt/AIBehaviorMap.txt` | AI 行为映射 |
| | `ToBundle/Config/Txt/AiDropMap.txt` | AI 掉落映射 |
| | `ToBundle/Config/Txt/AiParamLocator.txt` | AI 参数定位器 |
| | `ToBundle/Config/Txt/SORoleAIFashion.txt` | AI 时装 |
| | `ToBundle/Config/Txt/SORoleAIItem.txt` | AI 道具 |
| | `ToBundle/Config/Txt/SORoleArAI.txt` | AR AI |
| | `ToBundle/Config/Txt/RoleAiSimulateOpenBox.txt` | AI 模拟开箱 |
| | `ToBundle/Config/Txt/RobotGun.txt` | 机器人枪械 |
| **ScriptableObject** | `ToBundle/ScriptableObject/AI/` (219 files) | AI 配置 |
| | `ToBundle/ScriptableObject/AIBehavior/` (41 files) | AI 行为树 |
| | `ToBundle/ScriptableObject/AIDrop/` (60 files) | AI 投放配置 |
| | `ToBundle/ScriptableObject/RoleAI/` (104 files) | 角色 AI 配置 |
| **预制体** | `ToBundle/RoleAI/` (264 files) | AI 预制体 |

---

## 六、武器/战斗系统 (B6 📋)

> **Loader**：`ItemLoader.cs` (通过 ItemPool)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Features/` (~107 files) | 功能特性 |
| | `Script/GamePlay/Client/Modules/FightClose/` | 近战 |
| | `Script/GamePlay/Client/Modules/MeleeWeapon/` | 近战武器 |
| **配置表** | `ToBundle/Config/Txt/WeaponType.txt` | 武器类型 |
| | `ToBundle/Config/Txt/WeaponPosition.txt` | 武器位置 |
| | `ToBundle/Config/Txt/WeaponStore.txt` | 武器商店 |
| | `ToBundle/Config/Txt/WeaponControlAsset.txt` | 武器控制资产 |
| | `ToBundle/Config/Txt/WeaponSubPath.txt` | 武器子路径 |
| | `ToBundle/Config/Txt/WeaponAssembly.txt` | 武器组装 |
| | `ToBundle/Config/Txt/SOWeaponUp.txt` | 武器升级 |
| | `ToBundle/Config/Txt/SOWeaponFireEffect.txt` | 开火特效 |
| | `ToBundle/Config/Txt/SOWepEquipData.txt` | 武器装备数据 |
| | `ToBundle/Config/Txt/SOEquipPart.txt` | 装备部件 |
| | `ToBundle/Config/Txt/SOEmitter.txt` | 发射器 |
| | `ToBundle/Config/Txt/SOBulletDecal.txt` | 弹孔贴花 |
| | `ToBundle/Config/Txt/SOBulletImpact.txt` | 弹痕效果 |
| | `ToBundle/Config/Txt/GunShootEffect.txt` | 枪射击特效 |
| | `ToBundle/Config/Txt/FrontSight.txt` | 准星 |
| | `ToBundle/Config/Txt/ItemAsset.txt` | 物品资产 |
| | `ToBundle/Config/Txt/SOItemData.txt` | 物品数据 |
| | `ToBundle/Config/Txt/PickItemData.txt` | 拾取物数据 |
| | `ToBundle/Config/Txt/PickItemAsset.txt` | 拾取物资产 |
| | `ToBundle/Config/Txt/SkinItemAsset.txt` | 皮肤物品资产 |
| | `ToBundle/Config/Txt/SkinBulletAsset.txt` | 子弹皮肤 |
| | `ToBundle/Config/Txt/BigWeaponAsset.txt` | 大型武器资产 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Items/` (483 files) | 物品配置 |
| | `ToBundle/ScriptableObject/Checker/` | 武器检查器 |
| | `ToBundle/ScriptableObject/BlastData/` | 爆炸数据 |
| | `ToBundle/ScriptableObject/Equipments/` | 装备 |
| **预制体** | `ToBundle/Skin/Items/` (4,691 files) | 物品皮肤 |
| | `ToBundle/Skin/ItemsH/` (4,946 files) | H 版皮肤 |
| | `ToBundle/Skin/PickItems/` (5,045 files) | 拾取物皮肤 |
| | `ToBundle/GamePlayItem/WeaponControls/` (194 files) | 武器控制预制体 |
| **特效** | `ToBundle/Effect/WeaponEff/` (3,305 files) | 武器特效 |
| | `ToBundle/Effect/WeaponFlame/` (289 files) | 枪口火焰 |
| | `ToBundle/Effect/WeaponHTK/` (150 files) | HTK 武器特效 |
| | `ToBundle/Effect/WeaponCommon/` (3 files) | 通用武器特效 |
| | `ToBundle/Effect/WeaponShellCase/` (16 files) | 弹壳特效 |
| | `ToBundle/Effect/Bullet/` (133 files) | 子弹特效 |
| | `ToBundle/Effect/RandomGunSkin/` (3 files) | 随机枪械皮肤 |
| | `ToBundle/Effect/Machine_Effect/` (310 files) | 机械/炮台特效 |
| **物品预制体** | `ToBundle/Items/` (480 files) | 1 代物品预制体（按类型分子目录） |
| | `ToBundle/Items/Ammunition/` (20) | 弹药 |
| | `ToBundle/Items/Attachments/` (101) | 配件 |
| | `ToBundle/Items/Equipment/` (89) | 装备 |
| | `ToBundle/Items/Stunt/` (82) | 特技道具 |
| | `ToBundle/Items/PrankItem/` (31) | 整蛊道具 |
| | `ToBundle/Items/MouseHoleMode/` (36) | 猫鼠模式道具 |
| | `ToBundle/Items/GoldDash/` (20) | 淘金模式道具 |
| | `ToBundle/Items/PveItem/` (19) | PVE 道具 |
| | `ToBundle/Items/BirthIsland/` (16) | 出生岛道具 |
| | `ToBundle/Items/War/` (23) | 战场道具 |
| | `ToBundle/Items/AbilitiesCards/` (2) | 技能卡牌 |

### 武器类型分类 (SubpackageGroupsBuilder)

```
Assault, DesignatedMarksmanRifle, LightMachineGun, Melee,
ShotGun, Sniper, SpecialWeapon, SubmachineGun, Hiddenweapon, MagicWeapon
```

---

## 七、道具系统 (B7 📋)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Item/` | 道具客户端 |
| | `Script/GamePlay/Server/Modules/Item/` | 道具服务端 |
| | `Script/GamePlay/Client/Modules/PropsBox/` | 道具箱 |
| **配置表** | `ToBundle/Config/Txt/TaskItemData.txt` | 任务道具 |
| | `ToBundle/Config/Txt/ItemTableBase.txt` | 道具表 |
| | `ToBundle/Config/Txt/ItemTabBase.txt` | 道具 Tab |
| | `ToBundle/Config/Txt/ItemSize.txt` | 道具尺寸 |
| | `ToBundle/Config/Txt/ItemQuality.txt` | 道具品质 |
| | `ToBundle/Config/Txt/ItemRoulette.txt` | 道具轮盘 |
| | `ToBundle/Config/Txt/WarDropItem.txt` | 战场掉落物 |
| | `ToBundle/Config/Txt/WarDropItemContent.txt` | 掉落物内容 |
| | `ToBundle/Config/Txt/WarDropItemEffect.txt` | 掉落物特效 |
| | `ToBundle/Config/Txt/WarDropItemProbability.txt` | 掉落概率 |
| | `ToBundle/Config/Txt/LootBag.txt` / `LootGroup.txt` / `LootItem.txt` | 战利品系统 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Screen/DropItem/` | 掉落物配置 |
| | `ToBundle/ScriptableObject/Screen/GameCreateItem/` | 创建物配置 |
| **特效** | `ToBundle/Effect/WarItem/` (295 files) | 战场道具特效 |
| | `ToBundle/Effect/Box/` (4 files) | 箱子特效 |
| | `ToBundle/Effect/DeadItemBox/` (6 files) | 死亡道具箱特效 |
| | `ToBundle/Effect/BlackMarket/` (3 files) | 黑市特效 |
| | `ToBundle/Effect/Killballon/` (3 files) | 击杀气球特效 |
| **玩法道具** | `ToBundle/GamePlayItem/PickItems/` (434 files) | 拾取物预制体 |
| | `ToBundle/GamePlayItem/Killballon/` (276 files) | 击杀气球预制体 |
| | `ToBundle/GamePlayItem/HideSeekObj/` (177 files) | 躲猫猫物品 |
| | `ToBundle/GamePlayItem/ServerData/` (24 files) | 服务端数据预制体 |
| | `ToBundle/GamePlayItem/DungeonGame/` (8 files) | 地牢游戏道具 |
| | `ToBundle/GamePlayItem/VolumeControl/` (7 files) | 体积控制 |
| | `ToBundle/GamePlayItem/BladeBall/` (3 files) | 刀锋球 |
| | `ToBundle/GamePlayItem/DitherFading/` (1 file) | 抖动淡出 |

---

## 八、UI 系统 (B8 📋)

> **Loader**：`UILoader.cs` + `UIAssetReference.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/UI/` (1,968 files) | UI 代码 |
| **配置表** | `ToBundle/Config/Txt/Windows.txt` | 窗口注册 |
| | `ToBundle/Config/Txt/UITextures.txt` | UI 纹理 |
| | `ToBundle/Config/Txt/UIActivityWidgets.txt` | 活动组件 |
| | `ToBundle/Config/Txt/UISoundSourceConfig.txt` | UI 音效 |
| | `ToBundle/Config/Txt/UIModelCamera.txt` | UI 模型相机 |
| **预制体** | `ToBundle/UGUI/Windows/` (612 files) | 窗口预制体 |
| | `ToBundle/UGUI/Widgets/` (3,194 files) | 组件预制体 |
| | `ToBundle/UGUI/Elements/` (52 files) | 元素预制体 |
| **图集/纹理** | `ToBundle/UGUI/Atlas/` (472 files) | SpriteAtlas 图集 |
| | `ToBundle/UGUI/Sprite/` (24,380 files) | 散图 Sprite |
| | `ToBundle/UGUI/Texture/` (5,444 files) | 纹理 |
| | `ToBundle/UGUI/Font/` (648 files) | 字体 |
| | `ToBundle/UGUI/GameIcons/` (5 files) | 游戏图标 |
| **动画/材质** | `ToBundle/UGUI/Animation/` (598 files) | UI 动画 |
| | `ToBundle/UGUI/Materials/` (15 files) | UI 材质 |
| | `ToBundle/UGUI/Skeleton/` (9 files) | UI 骨骼动画 |
| | `ToBundle/UGUI/UIAdapter/` (8 files) | UI 适配器 |
| | `ToBundle/UGUI/Editor/` (12 files) | UI 编辑器资源 |
| **特效** | `ToBundle/Effect/UI/` (1,512 files) | UI 特效 |
| | `ToBundle/Effect/TweenGoEff/` (296 files) | 补间动画特效 |
| | `ToBundle/Effect/EffBG/` (397 files) | 背景特效 |
| | `ToBundle/Effect/Emoji/` (19 files) | 表情特效 |
| | `ToBundle/Effect/Localization/` (92 files) | 本地化特效 |
| | `ToBundle/Effect/Season/` (11 files) | 赛季特效 |
| | `ToBundle/Effect/Show/` (80 files) | 展示特效 |
| **ScriptableObject** | `ToBundle/ScriptableObject/UI/` (67 files) | UI 配置 |

---

## 九、镜头系统 (B9 📋)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/Camera/` | 镜头逻辑 |
| **配置表** | `ToBundle/Config/Txt/CameraAlpha.txt` | 相机 Alpha |
| **ScriptableObject** | `ToBundle/ScriptableObject/Screen/ArtSetting/` (161 files) | 画面美术设置 |
| | `ToBundle/ScriptableObject/Fog/` (147 files) | 雾效配置（按地图分） |
| | `ToBundle/ScriptableObject/GraphicsAsset/` (12 files) | 图形资产配置 |
| | `ToBundle/ScriptableObject/PostProcessSetting/` (1 file) | 后处理设置 |
| | `ToBundle/ScriptableObject/SceneRenderSetting/` (1 file) | 场景渲染设置 |
| | `ToBundle/ScriptableObject/PVSSetting/` (3 files) | PVS 可见性设置 |
| | `ToBundle/ScriptableObject/HLODSetting/` (4 files) | HLOD 设置 |

---

## 十、地图/场景系统 (B9 附属)

> **Loader**：`SceneLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **地图列表** | CombatIsland, RainbowIsland, SupernovaStar, StarfishIsland, Touradon, CatIsland, CombatRetro | 已知地图 |
| **服务端场景** | `Scenes/Biubiubiu2/Runtime/ServerScene/` (70+ .unity) | ✅ **已统一**：1 代 + 2 代所有服务端场景 |
| | `Scenes/Biubiubiu2/Runtime/Server{Map}/` | 各地图服务端运行时拆分子目录 |
| | `Scenes/Biubiubiu2/ServerCollision/{Map}_Server/` | 服务端碰撞网格（Mesh/ + Navmesh/） |
| | `Scenes/Biubiubiu2/Editor/` | 场景编辑器源文件（GoldDash / BeastCamp 等） |
| | ~~`ServerScene/`~~ | ⚠️ 旧路径，仅剩 4 岛碰撞数据 |
| **客户端场景拆分** | `Scenes/Output/{MapName}/Building/Visual/` | 建筑视觉 |
| | `Scenes/Output/{MapName}/Building/Collider/` | 建筑碰撞 |
| | `Scenes/Output/{MapName}/Vegetation/` | 植被 |
| | `Scenes/Output/{MapName}/Environmental/` | 环境物 |
| **天空盒** | `ToBundle/Map/SkyBox/` (24 files) | 天空盒材质 |
| **地图数据** | `ToBundle/Map/AirThrowServer/` (12 files) | 空投服务端数据 |
| | `ToBundle/Map/AirWall/` (36 files) | 空气墙 |
| | `ToBundle/Map/PoiData/` (8 files) | POI 兴趣点数据 |
| | `ToBundle/Map/TeamMap/` (11 files) | 组队地图 |
| | `ToBundle/Map/WuLinHotelItemBreak/` (15 files) | 武林酒店可破坏物 |
| **草地** | `ToBundle/ScriptableObject/Grass/` (10 files) | 草地配置 |
| | `ToBundle/ScriptableObject/GrassKing/` (21 files) | 草地之王配置 |
| | `ToBundle/Config/Txt/Grass.txt` / `GPUGrassAsset.txt` | 草地配置表 |
| **场景特效** | `ToBundle/Effect/Scene/` (2,291 files) | 场景特效（大量） |
| | `ToBundle/Effect/BirthIsland/` (41 files) | 出生岛特效 |
| **场景 SO** | `ToBundle/ScriptableObject/Screen/ServerTerrain/` (8 files) | 服务端地形 |
| | `ToBundle/ScriptableObject/Screen/NavMesh/` (4 files) | 导航网格 |
| | `ToBundle/ScriptableObject/Screen/Sandstorm/` (2 files) | 沙尘暴 |
| | `ToBundle/ScriptableObject/SOSceneObject/` (1 file) | 场景物体 |
| | `ToBundle/ScriptableObject/LevelData/` (358 files) | 关卡数据（物品/载具投放点位） |
| | `ToBundle/ScriptableObject/ItemSpawn/` (12 files) | 物品刷新配置 |
| | `ToBundle/ScriptableObject/RandomEvent/` (19 files) | 随机事件 |
| | `ToBundle/ScriptableObject/SpotHot/` (4 files) | 热点区域 |

---

## 十一、子玩法模块 (B11 📋)

### 淘金模式 (GoldDash)
> **Loader**：`GoldDashLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **服务端数据** | `ToBundle/Biubiubiu2/GoldDash/ServerData/` | 服务端数据预制体 |
| | `ToBundle/Biubiubiu2/GoldDash/ServerDataCollider/Prefab/` | 碰撞数据 |
| | `ToBundle/Biubiubiu2/GoldDash/Prop/` | 道具预制体 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Mode/GoldDash/` | 模式配置 |
| | `ToBundle/ScriptableObject/Pet/` (336 files) | 宠物配置 |
| **特效** | `ToBundle/Effect/GoldDash/` (692 files) | 淘金主特效 |
| | `ToBundle/Effect/GoldDashAncientDragon/` (49 files) | 远古龙 Boss 特效 |
| | `ToBundle/Effect/GoldDashDiamondAncientDragon/` (51 files) | 钻石远古龙特效 |
| | `ToBundle/Effect/GoldDashAuroraDragon/` (54 files) | 极光龙特效 |
| | `ToBundle/Effect/GoldDashBossAceJoker/` (93 files) | Ace Joker Boss 特效 |
| | `ToBundle/Effect/GoldDashBossSupremeJoker/` (136 files) | Supreme Joker Boss 特效 |
| | `ToBundle/Effect/GoldDashBossJokerDrone/` (89 files) | Joker Drone Boss 特效 |
| | `ToBundle/Effect/GoldDashBossDaDa/` (158 files) | DaDa Boss 特效 |
| | `ToBundle/Effect/GoldDashBossOctopus/` (127 files) | 章鱼 Boss 特效 |
| | `ToBundle/Effect/GoldDashPassiveSkill/` (4 files) | 淘金被动技能特效 |
| | `ToBundle/Effect/GoldDashWarItem/` (9 files) | 淘金战场物品特效 |
| **配置表** | `ToBundle/Config/Txt/GoldDash*.txt` (~80+ files) | 大量淘金配置 |

### 击倒模式 (Knockout)
> **Loader**：`KnockoutLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **ScriptableObject** | `ToBundle/ScriptableObject/Screen/Knockout/Config/` | KO 配置 |
| **配置表** | `ToBundle/Config/Txt/KnockoutRuleTable.txt` | KO 规则 |
| | `ToBundle/Config/Txt/KnockoutUIObj.txt` / `KnockoutUIObjPc.txt` | KO UI 对象 |
| **特效** | `ToBundle/Effect/KnockoutMode/` (70 files) | KO 特效 |

### PVE 模式
> **Loader**：`PveModeLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **预制体** | `ToBundle/GamePlayItem/PveServer/` (22 files) | PVE 服务端 |
| | `ToBundle/GamePlayItem/PveMonster/` (50 files) | PVE 怪物 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Mode/PveRogue/` | PVE 肉鸽配置 |
| | `ToBundle/ScriptableObject/Screen/ServerTerrain/PVE/` | PVE 地形 |
| | `ToBundle/ScriptableObject/Screen/NavMesh/PVE/` | PVE 导航网格 |
| **配置表** | `ToBundle/Config/Txt/Pve*.txt` (~10 files) | PVE 配置 |
| **特效** | `ToBundle/Effect/PveEffect/` (10 files) | PVE 特效 |

### 极限格斗 (UltraFight)
> **Loader**：`UltraFightLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **ScriptableObject** | `ToBundle/ScriptableObject/Screen/SOUltraFight/` (3 files) | 格斗配置 |
| **配置表** | `ToBundle/Config/Txt/UltraFightWeapon.txt` | 格斗武器 |

### 足球 (Football)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **预制体** | `ToBundle/GamePlayItem/Football/` (39 files) | 足球预制体 |
| **配置表** | `ToBundle/Config/Txt/FootBall*.txt` | 足球配置 |

### 鬼屋/惊悚 (Tarkov)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **预制体** | `ToBundle/Tarkov/Carrier/` (2 files) | Tarkov 载具 |
| | `ToBundle/Tarkov/Monster/` (3 files) | Tarkov 怪物 |
| **特效** | `ToBundle/Effect/TarkovEffect/` (54 files) | Tarkov 特效 |

### OnlyUp

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **特效** | `ToBundle/Effect/OnlyUp/` (250 files) | OnlyUp 特效 |

### 刀锋球 (BladeBall)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **预制体** | `ToBundle/GamePlayItem/BladeBall/` (3 files) | 刀锋球预制体 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Mode/BladeBallMode/` | 刀锋球配置 |

### 玩法共享资源

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **GamePlayItem** | `ToBundle/GamePlayItem/WeaponControls/` (97 files) | 武器控制器 |
| | `ToBundle/GamePlayItem/RingEnclose/` (1 file) | 缩圈 |
| | `ToBundle/GamePlayItem/DecalDemo/` (1 file) | 贴花示例 |
| **特效** | `ToBundle/Effect/ChipEffect/` (108 files) | 芯片特效 |
| | `ToBundle/Effect/AbilitiesCards/` (1,255 files) | 技能卡牌特效 |
| | `ToBundle/Effect/Tricks/` (907 files) | 特技特效 |
| | `ToBundle/Effect/RandomAction/` (8 files) | 随机行为特效 |
| | `ToBundle/Effect/ShenLong/` (2 files) | 神龙特效 |
| | `ToBundle/Effect/DragonPalace/` (1 file) | 龙宫特效 |
| | `ToBundle/Effect/SettlementAward/` (1 file) | 结算奖励特效 |

---

## 十二、网络/消息系统 (B10 📋)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/Biubiubiu2/Message/` (~265 files) | 消息定义 (2代) |
| | `Script/Biubiubiu2/GamePlay/` | 框架层 |

---

## 十三、基础设施 (B13 📋)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **工具库** | `Script/Utils/` (494 files) | 通用工具 |
| **配置** | `Script/Config/` (678 files) | 配置代码 |
| **数据层** | `Script/Data/` (290 files) | 数据定义 |
| **控制器** | `Script/Controller/` (135 files) | 控制器 |
| **资源管理** | `Script/Asset/` | 资源加载系统 |
| | `Script/Asset/Loaders/` (20 files) | Loader 入口 |
| **配置表根** | `ToBundle/Config/Txt/` (2,519 files) | 所有配置表 |
| **通用 SO** | `ToBundle/ScriptableObject/Misc/` (58 files) | 杂项配置 |
| | `ToBundle/ScriptableObject/Screen/` (1,461 files) | 画面相关 |
| **音频** | `Audio/Mobile/` | Wwise 音频 |
| | `ToBundle/ScriptableObject/Sound/` | 音效配置 |
| **全局 SO** | `ToBundle/Global/ScriptableObject/` (84 files) | 全局 ScriptableObject |
| | `ToBundle/Global/Config/` (29 files) | 全局配置 |
| **视频** | `ToBundle/Global/Video/` (31 files) | 全局视频 |
| | `ToBundle/Video/` (75 files) | 视频资源 |
| | `ToBundle/Video/VideoSubtitle/` (25 files) | 视频字幕 |
| | `ToBundle/CI/` (2 files) | CI 视频 |
| **Standalone** | `ToBundle/Standalone/Video/` (64 files) | 独立视频 |
| | `ToBundle/Standalone/UGUI/` (58 files) | 独立 UI 资源 |
| | `ToBundle/Standalone/ScriptableObject/` (36 files) | 独立 SO |
| | `ToBundle/Standalone/Fashion/` (30 files) | 独立时装 |
| **编辑器** | `ToBundle/Editor/` (124 files) | 编辑器专用资源 |
| | `ToBundle/Config/Editor/` (745 files) | 编辑器配置 |
| **性能** | `ToBundle/AutoPerf/` (1 file) | 自动性能测试 |
| **内建** | `ToBundle/BuiltIn/` (4 files) | 内建预制体 |

---

## 十四、时装/皮肤系统 (NEW)

> **Loader**：`FashionLoader.cs`

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **时装模型** | `ToBundle/Fashion/` (22,643 files total) | 时装预制体（按部位分目录） |
| | `ToBundle/Fashion/Hair/` (4,552) | 头发 |
| | `ToBundle/Fashion/Shoe/` (3,614) | 鞋子 |
| | `ToBundle/Fashion/Suit/` (3,108) | 套装 |
| | `ToBundle/Fashion/Gloves/` (2,884) | 手套 |
| | `ToBundle/Fashion/Hat/` (2,041) | 帽子 |
| | `ToBundle/Fashion/Trouser/` (1,839) | 裤子 |
| | `ToBundle/Fashion/Parachute/` (1,163) | 降落伞 |
| | `ToBundle/Fashion/FaceMask/` (758) | 面罩 |
| | `ToBundle/Fashion/FaceOrnam/` (754) | 脸部装饰 |
| | `ToBundle/Fashion/BodyEffect/` (487) | 身体特效 |
| | `ToBundle/Fashion/SkinColor/` (330) | 肤色 |
| | `ToBundle/Fashion/Beard/` (302) | 胡子 |
| | `ToBundle/Fashion/Eye/` (216) | 眼睛 |
| | `ToBundle/Fashion/Brow/` (198) | 眉毛 |
| | `ToBundle/Fashion/HandItem/` (132) | 手持物 |
| | `ToBundle/Fashion/Tattoo/` (105) | 纹身 |
| | `ToBundle/Fashion/Mouth/` (69) | 嘴 |
| | `ToBundle/Fashion/Nose/` (59) | 鼻子 |
| | `ToBundle/Fashion/Ear/` (24) | 耳朵 |
| | `ToBundle/Fashion/Cheek/` (7) | 脸颊 |
| | `ToBundle/Fashion/Wrinkle/` (1) | 皱纹 |
| **时装特效** | `ToBundle/Effect/Fashion/` (9,292 files) | 时装特效（最大特效目录） |
| | `ToBundle/Effect/Expression/` (656 files) | 表情特效 |
| | `ToBundle/Effect/Skin/` (14 files) | 皮肤特效 |
| **皮肤预制体** | `ToBundle/Skin/Items/` (1,763 files) | 道具皮肤 |
| | `ToBundle/Skin/PickItems/` (1,947 files) | 拾取物皮肤 |
| | `ToBundle/Skin/ItemsH/` (1,708 files) | H 版道具皮肤 |
| | `ToBundle/Skin/Cars/` (323 files) | 载具皮肤 |
| **材质** | `ToBundle/Mat/` (12 files) | 时装相关材质 |
| **角色动画** | `ToBundle/Effect/RoleAnimation/` (1,641 files) | 角色动画特效 |
| **展示** | `ToBundle/Effect/GameStartShow/` (60 files) | 游戏开始展示 |
| **配置表** | `ToBundle/Config/Txt/FashionItem*.txt` | 时装物品 |
| | `ToBundle/Config/Txt/SkinColor.txt` | 肤色 |
| **ScriptableObject** | `ToBundle/ScriptableObject/Fashion/` (9 files) | 时装配置 |

---

## 十五、宠物系统 (NEW)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **ScriptableObject** | `ToBundle/ScriptableObject/Pet/` (164 files) | 宠物配置 |
| **配置表** | `ToBundle/Config/Txt/Pet*.txt` | 宠物配置表 |

---

## 十六、背包系统 (NEW)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **ScriptableObject** | `ToBundle/ScriptableObject/Bag/` (225 files) | 背包配置 |
| **特效** | `ToBundle/Effect/Backpack/` (325 files) | 背包特效 |
| **配置表** | `ToBundle/Config/Txt/Bag*.txt` | 背包配置表 |

---

## 十七、新手引导系统 (NEW)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **ScriptableObject** | `ToBundle/ScriptableObject/BeginnerTutorial/` (63 files) | 新手引导配置 |
| | `ToBundle/ScriptableObject/BeginnerTutorialConfig/` (8 files) | 新手引导全局配置 |
| **配置表** | `ToBundle/Config/Txt/Tutorial*.txt` | 引导配置表 |

---

## 十八、技能系统 (NEW)

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| **代码** | `Script/GamePlay/Client/Modules/RoleSkill/` | 角色技能 |
| **ScriptableObject** | `ToBundle/ScriptableObject/AbilityCards/` (19 files) | 技能卡牌配置 |
| | `ToBundle/ScriptableObject/Ability/` (1 file) | 技能配置 |
| | `ToBundle/ScriptableObject/Screen/SkillConfig/` (3 files) | 技能画面配置 |
| **特效** | `ToBundle/Effect/AbilitiesCards/` (1,255 files) | 技能卡牌特效 |
| | `ToBundle/Effect/Tricks/` (907 files) | 特技特效 |
| | `ToBundle/Effect/ChipEffect/` (108 files) | 芯片特效 |

---

## 附录 A：Loader 文件索引

| Loader 文件 | 对应系统 | 核心路径 |
|------------|---------|---------|
| `AnimationLoader.cs` | 角色动画 | `ToBundle/Role/Controllers/`, `Art/RoleAnimation/` |
| `AuxiliaryAimingLoader.cs` | 辅助瞄准 | `ToBundle/GamePlayItem/AuxiliaryAiming/` |
| `CarLoader.cs` | 载具 | `ToBundle/GamePlayItem/AirShip/`, `ToBundle/GamePlayItem/CarResource/` |
| `ConfigLoader.cs` | 全局配置 | `ToBundle/ScriptableObject/*` (50+ 子路径) |
| `FashionLoader.cs` | 时装 | `ToBundle/Fashion/`, `ToBundle/Mat/` |
| `FontLoader.cs` | 字体 | `ToBundle/UGUI/Font/` |
| `GoldDashLoader.cs` | 淘金模式 | `ToBundle/Biubiubiu2/GoldDash/`, `ToBundle/ScriptableObject/Pet/` |
| `ItemLoader.cs` | 道具/武器 | 通过 ItemPool 管理 |
| `KnockoutLoader.cs` | 击倒模式 | `ToBundle/ScriptableObject/Screen/Knockout/` |
| `LuaLoader.cs` | Lua 脚本 | Lua 字节码路径 |
| `MapLoader.cs` | 地图纹理 | `ToBundle/UGUI/Texture/Maps/` |
| `ModeConfigLoader.cs` | 模式配置 | `ToBundle/ScriptableObject/Mode/` |
| `PveModeLoader.cs` | PVE 模式 | `ToBundle/GamePlayItem/PveServer/`, `ToBundle/ScriptableObject/Mode/PveRogue/` |
| `RoleLoader.cs` | 角色 | `ToBundle/Role/Prefabs/`, `ToBundle/Role/Materials/` |
| `SceneLoader.cs` | 场景/地图 | `Scenes/Output/`, `ToBundle/Map/SkyBox/` |
| `ServerLoader.cs` | 服务端 | `ToBundle/GamePlayItem/ServerData/` |
| `ShaderMap.cs` | Shader | ScriptableObject 配置 |
| `SoundLoader.cs` | 音效 | `ToBundle/ScriptableObject/Sound/Attenuation/` |
| `UIAssetReference.cs` | UI 引用 | 资源引用管理 |
| `UILoader.cs` | UI | `ToBundle/UGUI/*` |
| `UltraFightLoader.cs` | 极限格斗 | `ToBundle/ScriptableObject/Screen/SOUltraFight/` |
| `WarLoader.cs` | 战斗核心 | `ToBundle/GameBase/`, `ToBundle/GamePlayItem/` |

## 附录 B：分包类型 (SubpackageGroupsBuilder)

| 分包类别 | 资源路径 | 说明 |
|---------|---------|------|
| Fashion (时装) | `ToBundle/Fashion/` | 按时装 ID 分包 |
| Fashion Effect | `ToBundle/Effect/Fashion/` | 时装特效 |
| Aerocraft | `ToBundle/GamePlayItem/Aerocraft/`, `ToBundle/Effect/Aerocraft/`, `ToBundle/Skin/ItemsH/Aerocraft/` | 飞行器 |
| Backpack | `ToBundle/Effect/Backpack/`, `ToBundle/Skin/Items/Equipment/Back/`, `ToBundle/Skin/ItemsH/Back/`, `ToBundle/Skin/PickItems/Equipment/Back/` | 背包 |
| Killballon | `ToBundle/GamePlayItem/Killballon/` | 击杀气球 |
| Background | `ToBundle/Effect/EffBG/`, `ToBundle/UGUI/Texture/WarFlagBg/` | 背景 |
| CardFace | `ToBundle/UGUI/Texture/Modules/WarFlagCardFace/` | 卡面 |
| AbilitiesCards | `ToBundle/Effect/AbilitiesCards/` | 技能卡牌 |
| Weapon (10 types) | 按武器类型分包 | Assault/Sniper/Melee/... |
| Scene | 按地图分包 | 场景资源 |
| Audio | `Audio/Mobile/` | 音频按 BNK 分包 |

---

> **最后更新**：Knowledge 构建 resource-map 全面扫描完成
> **下次更新**：system-map 补充对应资源引用

---

## 附录 C：Effect/ 完整目录索引

> 66 个子目录，按文件数降序（非 .meta）

| 目录 | 文件数 | 所属系统 |
|------|-------|---------|
| `Fashion/` | 9,292 | 时装 §十四 |
| `WeaponEff/` | 3,305 | 武器 §六 |
| `Scene/` | 2,291 | 地图 §十 |
| `RoleAnimation/` | 1,641 | 角色 §三 / 时装 §十四 |
| `UI/` | 1,512 | UI §八 |
| `Carrier/` | 1,473 | 载具 §一 |
| `AbilitiesCards/` | 1,255 | 技能 §十八 |
| `Tricks/` | 907 | 技能 §十八 |
| `Aerocraft/` | 797 | 载具 §一 |
| `GoldDash/` | 692 | 子玩法 §十一 |
| `Expression/` | 656 | 时装 §十四 |
| `EffBG/` | 397 | UI §八 |
| `Machine_Effect/` | 310 | 武器 §六 |
| `Backpack/` | 325 | 背包 §十六 |
| `TweenGoEff/` | 296 | UI §八 |
| `WarItem/` | 295 | 道具 §七 |
| `Buff/` | 293 | Buff §四 |
| `WeaponFlame/` | 289 | 武器 §六 |
| `Mode/` | 284 | 模式 §二 |
| `OnlyUp/` | 250 | 子玩法 §十一 |
| `War/` | 187 | 模式 §二 |
| `DaDa/` | 158 | 子玩法 §十一 |
| `BiologicalVehicle/` | 151 | 载具 §一 |
| `WeaponHTK/` | 150 | 武器 §六 |
| `BossSupremeJoker/` | 136 | 子玩法 §十一 |
| `Bullet/` | 133 | 武器 §六 |
| `BossOctopus/` | 127 | 子玩法 §十一 |
| `ChipEffect/` | 108 | 技能 §十八 |
| `BossAceJoker/` | 93 | 子玩法 §十一 |
| `Localization/` | 92 | UI §八 |
| `BossJokerDrone/` | 89 | 子玩法 §十一 |
| `Show/` | 80 | UI §八 |
| `KnockoutMode/` | 35 | 子玩法 §十一 |
| `GameStartShow/` | 60 | 时装 §十四 |
| `TarkovEffect/` | 54 | 子玩法 §十一 |
| `DiamondAncientDragon/` | 51 | 子玩法 §十一 |
| `AuroraDragon/` | 54 | 子玩法 §十一 |
| `AncientDragon/` | 49 | 子玩法 §十一 |
| `BirthIsland/` | 41 | 地图 §十 |
| `De_C4/` | 24 | 子玩法 §十一 |
| `Buff_S6_TransmitDoor/` | 23 | Buff §四 |
| `Emoji/` | 19 | UI §八 |
| `RookieCamp/` | 19 | 子玩法 §十一 |
| `BeastCamp/` | 18 | 模式 §二 |
| `WeaponShellCase/` | 16 | 武器 §六 |
| `RepairBotHalo/` | 16 | 道具 §七 |
| `Rescue/` | 16 | 道具 §七 |
| `Skin/` | 14 | 时装 §十四 |
| `Season/` | 11 | UI §八 |
| `PveEffect/` | 10 | 子玩法 §十一 |
| `GoldDashWarItem/` | 9 | 子玩法 §十一 |
| `RandomAction/` | 8 | 技能 §十八 |
| `DeadItemBox/` | 6 | 道具 §七 |
| `Feedingbottle/` | 4 | Buff §四 |
| `GoldDashPassiveSkill/` | 4 | 子玩法 §十一 |
| `RandomGunSkin/` | 3 | 武器 §六 |
| `WeaponCommon/` | 3 | 武器 §六 |
| `Box/` | 4 | 道具 §七 |
| `Killballon/` | 3 | 道具 §七 |
| `BlackMarket/` | 3 | 道具 §七 |
| `BlindingShield/` | 3 | Buff §四 |
| `ShenLong/` | 2 | 子玩法 §十一 |
| `SportParty/` | 2 | 子玩法 §十一 |
| `WarTakeoffPhase/` | 2 | 模式 §二 |
| `SettlementAward/` | 1 | UI §八 |
| `DragonPalace/` | 1 | 子玩法 §十一 |

---

## 附录 D：ScriptableObject/ 完整目录索引

> 48 个子目录，按文件数降序（非 .meta）

| 目录 | 文件数 | 所属系统 |
|------|-------|---------|
| `Buff/` | 1,280 | Buff §四 |
| `Screen/` | 708 | 多系统共用（详见各章节） |
| `Mode/` | 428 | 模式 §二 |
| `LevelData/` | 358 | 地图 §十 |
| `Items/` | 239 | 武器/道具 §六§七 |
| `Bag/` | 225 | 背包 §十六 |
| `Pet/` | 164 | 宠物 §十五 |
| `Fog/` | 147 | 镜头/渲染 §九 |
| `AI/` | 109 | AI §五 |
| `Biological_Carrier/` | 102 | 载具 §一 |
| `Vehicle/` | 38 | 载具 §一 |
| `UI/` | 67 | UI §八 |
| `BeginnerTutorial/` | 63 | 新手引导 §十七 |
| `Misc/` | 58 | 基础设施 §十三 |
| `SOCreateObjData/` | 42 | 载具/地图 §一§十 |
| `Sound/` | 30 | 基础设施 §十三 |
| `Grass/` | 10 | 地图 §十 |
| `GrassKing/` | 21 | 地图 §十 |
| `AbilityCards/` | 19 | 技能 §十八 |
| `RandomEvent/` | 19 | 地图 §十 |
| `ItemSpawn/` | 12 | 地图 §十 |
| `GraphicsAsset/` | 12 | 镜头/渲染 §九 |
| `Fashion/` | 9 | 时装 §十四 |
| `BeginnerTutorialConfig/` | 8 | 新手引导 §十七 |
| `SpotHot/` | 4 | 地图 §十 |
| `HLODSetting/` | 4 | 镜头/渲染 §九 |
| `ModeToolMap/` | 3 | 模式 §二 |
| `CommonMode/` | 3 | 模式 §二 |
| `PVSSetting/` | 3 | 镜头/渲染 §九 |
| `Ability/` | 1 | 技能 §十八 |
| `PostProcessSetting/` | 1 | 镜头/渲染 §九 |
| `SceneRenderSetting/` | 1 | 镜头/渲染 §九 |
| `SOSceneObject/` | 1 | 地图 §十 |

### Screen/ 子目录明细

| 子目录 | 文件数 | 所属系统 |
|-------|-------|---------|
| `GameCreateItem/` | 203 | 模式 §二 |
| `ArtSetting/` | 161 | 镜头/渲染 §九 |
| `GameSetting/` | 140 | 模式 §二 |
| `SOGunfightRoundData/` | 54 | 模式 §二 |
| `DropItem/` | 29 | 道具 §七 |
| `ModeSetting/` | 24 | 模式 §二 |
| `DefaultEquip/` | 21 | 武器 §六 |
| `Knockout/` | 17 | 子玩法 §十一 |
| `SOWolfParty/` | 15 | 子玩法 §十一 |
| `ServerTerrain/` | 8 | 地图 §十 |
| `RebornGun/` | 6 | 武器 §六 |
| `Slime/` | 6 | 子玩法 §十一 |
| `ChestMonster/` | 4 | 子玩法 §十一 |
| `NavMesh/` | 4 | 地图 §十 |
| `SOHypoxia/` | 3 | 子玩法 §十一 |
| `SOUltraFight/` | 3 | 子玩法 §十一 |
| `SkillConfig/` | 3 | 技能 §十八 |
| `Sandstorm/` | 2 | 地图 §十 |
| `BatteryTurret/` | 1 | 武器 §六 |
| `ItemGroup/` | 1 | 道具 §七 |
| `MapBuffs/` | 1 | 模式 §二 |
| `MapCovers/` | 1 | 模式 §二 |
| `SlipRope/` | 1 | 子玩法 §十一 |
