# 1 代架构 AI 制作规范

> **适用范围**：基于 `RoleAIManager` / `RoleAILogic` 的 1 代 AI 系统开发（行为树节点、AI 投放策略、AI 参数调优）
> **不适用**：2 代 AI 系统（`Biubiubiu2/` 下的 ECS 式 AI 组件）
> **参考实现**：敌人 AI（EnemyAIBehavior），路径 → Client: `ClientRoleAILogic` / `ClientRoleAIBehavior`，Server: `ServerRoleAILogic`，Host: `RoleAILogic`

**占位符说明**：

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{NodeName}` | 行为树节点功能名（大驼峰） | `MoveToTarget`、`CheckDistance` |
| `{BehaviorSign}` | 行为树 SO 标识（行为树文件名） | `EnemyAIBehavior`、`TeamAIBehavior` |
| `{AILevel}` | AI 难度等级 | `1`、`2`、`3` |
| `{MapSign}` | 地图标识 | `CatIsland`、`CombatIsland` |
| `{GameMode}` | 游戏模式标识 | `ClassicMode`、`ArcadeMode` |

---

## 一、架构概述

### 1.1 AI 体系分类

1 代 AI 系统基于 **Behavior Designer** 行为树驱动，按 `RoleAIType` 枚举分为四类 AI，共用同一套框架但使用不同行为树和配置：

| 维度 | 敌人 AI (Enemy) | 队友 AI (Team) | 出生岛 AI (BirthIsland) | 怪物 AI (Monster) |
|------|----------------|----------------|------------------------|-------------------|
| **行为树** | `EnemyAIBehavior_L{N}` | `TeamAIBehavior` | `BirthIslandAIBehavior` | PVE 专用（`RogueAI_*`） |
| **难度分级** | L1/L2/L3（通过 `AIBehaviorMapConfig` 映射） | 固定 | 固定 | 固定 |
| **投放方式** | `CommonServerRoleAISpawnerManager` 按玩家附近投放 | 跟随真人玩家 | 出生岛固定点 | PVE 模式脚本投放 |
| **武器来源** | `SORoleAIItem.txt` 概率随机 | 同 Enemy | 简单配置 | PVE 配置 |
| **时装** | `SORoleAIFashion.txt` 随机搭配 | 同 Enemy | 简单配置 | 固定 |
| **实例数量** | 大量（战场主体 AI） | 少量（队伍补位） | 中等（出生岛装饰） | 少量（PVE 关卡） |

### 1.2 核心类依赖

```
Assets/Script/GamePlay/Host/Modules/RoleAI/                    ← 框架层（Host 中枢）
    ├── RoleAIManager/
    │   └── RoleAIManager.cs            ← AI 管理器（入口：AddRoleAI / RemoveRoleAI / OnUpdate）
    │       ├── ServerRoleAIManager [S]  ← Server 端管理器
    │       └── ClientRoleAIManager [C]  ← Client 端管理器
    ├── RoleAILogic/
    │   └── RoleAILogic.cs              ← AI 实体（单个 AI 角色的 Host 逻辑）
    │       ├── ServerRoleAILogic [S]    ← Server 端实体
    │       └── ClientRoleAILogic [C]    ← Client 端实体（驱动行为树 + 状态机）
    ├── RoleAISpawner/
    │   └── RoleAISpawnerManager.cs     ← 投放管理器
    │       ├── ServerNormalRoleAISpawnerManager [S]    ← 普通模式投放
    │       ├── ServerGoldDashRoleAISpawnerManager [S]  ← GoldDash 模式投放
    │       └── ClientRoleAISpawnerManager [C]          ← Client 端出生点计算
    └── ScriptableObject/
        ├── RoleAIMgrConfig.cs          ← 全局管理配置 SO
        ├── RoleAIConfig.cs             ← 单体 AI 参数配置 SO
        └── RoleAIWeaponConfig.cs       ← AI 武器配置 SO

Assets/Script/GamePlay/Client/Modules/RoleAI/                  ← 行为树层（Client 驱动）
    ├── RoleAIManager/Features/
    │   ├── ClientRoleAIBehaviorMgr.cs  ← ★ 行为树管理（加载/驱动 BehaviorTree）
    │   ├── ClientRoleAILoadMgr.cs      ← 资源加载管理
    │   ├── ClientRoleAIBornMgr.cs      ← 出生管理
    │   ├── ClientRoleAISyncMgr.cs      ← 同步管理
    │   ├── ClientRoleAINavMeshMgr.cs   ← 寻路管理
    │   ├── ClientRoleAIPickItemMgr.cs  ← 捡物管理
    │   ├── ClientRoleAIHealthMgr.cs    ← 健康管理
    │   ├── ClientRoleAIUIMgr.cs        ← UI 管理
    │   └── ClientRoleAIFlyMgr.cs       ← 飞行管理
    ├── RoleAILogic/
    │   ├── ClientRoleAILogic.cs        ← Client 端实体
    │   ├── ClientRoleAIBehavior.cs     ← 行为树驱动（选择/加载行为树 → Tick）
    │   ├── ClientRoleAIState.cs        ← 状态机（Move/Air/Health/Jump/...）
    │   ├── ClientRoleAIAnimator.cs     ← 动画控制
    │   ├── ClientRoleAIController.cs   ← 控制器
    │   └── ClientRoleAIWeapon.cs       ← 武器控制
    └── AIBehavior/                     ← ★ 行为树节点（开发重点）
        ├── Action/
        │   ├── RoleAIAction.cs         ← Action 基类（继承 BehaviorDesigner.Action）
        │   └── RoleAI{NodeName}.cs     ← 具体 Action 节点（93 个）
        └── Conditional/
            ├── RoleAIConditional.cs    ← Conditional 基类（继承 BehaviorDesigner.Conditional）
            └── RoleAI{NodeName}.cs     ← 具体 Conditional 节点

Assets/Script/GamePlay/Server/Modules/RoleAI/                  ← 投放层（Server 控制）
    ├── RoleAIManager/
    │   └── ServerRoleAIManager.cs      ← Server 管理器
    ├── RoleAISpawner/
    │   └── CommonServerRoleAISpawnerManager.cs  ← ★ 新投放系统（基于 AiDeliveryConfigSO）
    └── RoleAILogic/
        └── ServerRoleAILogic.cs        ← Server 实体

Assets/Script/GamePlay/AutoWar/                                 ← 自动战斗（录制回放）
    ├── AutoWar.cs                      ← 自动跑点工具主类
    ├── AutoWarData.cs                  ← 战报数据结构
    └── AutoWarProgram.cs               ← 自动战斗程序入口
```

**三端入口类**：

| 端 | 入口类 | 路径 | 核心职责 |
|----|--------|------|---------|
| **H** (Host) | `RoleAIManager` | `Host/Modules/RoleAI/RoleAIManager/RoleAIManager.cs` | AI 生命周期管理、Feature 系统驱动 |
| **C** (Client) | `ClientRoleAIManager` | `Client/Modules/RoleAI/RoleAIManager/ClientRoleAIManager.cs` | 行为树驱动、表现层管理 |
| **S** (Server) | `ServerRoleAIManager` | `Server/Modules/RoleAI/RoleAIManager/ServerRoleAIManager.cs` | AI 投放、数据同步 |

### 1.3 预制体与资源加载（★ 强制）

AI 系统涉及 **四套资源加载链**：SO 全局配置、投放配置、行为树 SO、运行时预制体。

#### 1.3.1 资源目录总览

```
Assets/ToBundle/
├── ScriptableObject/
│   ├── AI/                             ← 全局 AI 配置 SO（108 个）
│   │   ├── ClassicMode_CatIsland_Level1.asset
│   │   ├── ArcadeMode_CatIsland_Level1.asset
│   │   └── ... （命名：{GameMode}_{MapSign}_Level{AILevel}）
│   ├── AIBehavior/                     ← 行为树参数 SO（19 个）
│   │   ├── Mode/                       ← 模式专用
│   │   ├── Other/                      ← 特殊类型（Alien/AR/Training）
│   │   └── Pve/                        ← PVE 角色（RogueAI_*）
│   ├── AIDrop/                         ← AI 投放配置
│   │   └── Config/
│   │       ├── AIPerson.asset          ← AI 人格配置（8 种人格类型）
│   │       └── Maps/                   ← 按地图模式的投放策略
│   │           └── AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}.asset
│   └── RoleAI/                         ← 角色 AI 专属配置（104 个）
│       ├── Role/                       ← 角色参数
│       └── Weapon/                     ← 武器参数
│
├── RoleAI/                             ← 运行时资源（121 个）
│   ├── AIBehavior/                     ← 行为树 SO（23 个 .asset）
│   │   ├── EnemyAIBehavior.asset       ← 敌人行为树（基础版）
│   │   ├── TeamAIBehavior.asset        ← 队友行为树
│   │   ├── BirthIslandAIBehavior.asset ← 出生岛行为树
│   │   └── ...
│   ├── Animator/                       ← 动画控制器（39 个）
│   │   ├── RoleAIControllerAdvance.controller  ← 主控制器
│   │   ├── UpperMask.mask
│   │   └── {WeaponName}.overrideController     ← 武器动画覆盖
│   ├── Prefabs/                        ← AI 预制体（43 个）
│   │   ├── Ballistic/                  ← 弹道预制体
│   │   ├── Role/                       ← AI 角色预制体
│   │   ├── RoleAIEquip/                ← 装备配置预制体
│   │   └── Weapon/                     ← 武器预制体
│   └── ServerData/                     ← 服务端数据（16 个）
│       ├── GoldDashAIBehavior/
│       ├── MLAgent/
│       └── PartyModeRoleAIBehavior/
│
└── Config/Txt/                         ← 配置表
    ├── AIBehaviorMap.txt                ← AI 行为映射
    ├── AIWeaponConfig.txt               ← AI 武器列表
    ├── AIWeaponSkin.txt                 ← AI 武器皮肤
    ├── AiDropMap.txt                    ← AI 投放映射
    ├── AiParamLocator.txt               ← AI 参数定位器
    ├── SORoleAIFashion.txt              ← AI 时装配置
    ├── SORoleAIItem.txt                 ← AI 道具/装备配置
    ├── SORoleArAI.txt                   ← AR AI 配置
    ├── RoleAiSimulateOpenBox.txt         ← AI 模拟开箱
    ├── RobotGun.txt                     ← 机器人枪械
    └── RookieCampAI.txt                 ← 新手营 AI
```

#### 1.3.2 资源路径与配置表

| 资源类型 | 路径模板 | 加载方法 | 管理类 |
|---------|---------|---------|--------|
| **全局 AI SO** | `Assets/ToBundle/ScriptableObject/AI/{GameMode}_{MapSign}_Level{N}.asset` | `AssetsLoad.GetSORoleAI(id)` | `ConfigLoader.cs` |
| **投放配置 SO** | `Assets/ToBundle/ScriptableObject/AIDrop/Config/Maps/AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}.asset` | `AssetsLoad.GetAiDeliveryConfigSO(gameScene, level)` | `ConfigLoader.cs` |
| **AI 人格 SO** | `Assets/ToBundle/ScriptableObject/AIDrop/Config/AIPerson.asset` | `AssetsLoad.GetAiPersonConfigSO()` | `ConfigLoader.cs` |
| **行为树 SO** | `Assets/ToBundle/RoleAI/AIBehavior/{BehaviorSign}.asset` | `AssetManager.LoadAsset<ExternalBehavior>(path)` | `ClientRoleAIBehaviorMgr.cs` |
| **动画控制器** | `Assets/ToBundle/RoleAI/Animator/RoleAIControllerAdvance.controller` | `AssetManager.LoadAsset<RuntimeAnimatorController>()` | `ClientRoleAILoadMgr.cs` |

#### 1.3.3 全局 AI 配置加载链

```
模式初始化（StartGame）
    │
    ├── RoleAISpawnerManager.InitConfig(mapSign, level)     [Host]
    │       └── AssetsLoad.GetSORoleAI(                     [ConfigLoader.cs:265]
    │               "{GameMode}_{MapSign}_Level{AILevel}")
    │           └── AssetManager.LoadAsset<SORoleAI>(
    │                   "Assets/ToBundle/ScriptableObject/AI/{id}.asset")
    │
    ├── RoleAIManager.OnInit()                              [Host]
    │       └── RoleAILoadMgr.LoadRoleAIMgrConfig(sign)
    │           └── Config = RoleAIMgrConfig
    │
    └── CommonServerRoleAISpawnerManager.OnInit()            [Server]
            ├── AssetsLoad.GetAiDeliveryConfigSO(            [ConfigLoader.cs:692]
            │       mapConfig.GameSOSetting, WarData.AILevel)
            │   └── "Assets/ToBundle/ScriptableObject/AIDrop/Config/Maps/
            │         AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}.asset"
            └── AssetsLoad.GetAiPersonConfigSO()             [ConfigLoader.cs:697]
                └── "Assets/ToBundle/ScriptableObject/AIDrop/Config/AIPerson.asset"
```

#### 1.3.4 行为树加载链

```
ClientRoleAIBehavior.OnInit()
    │
    ├── 根据 AIType 确定行为树标识
    │   switch(logic.Logic.AIType):
    │     Enemy     → "EnemyAIBehavior" + level 后缀
    │     Team      → "TeamAIBehavior"
    │     BirthIsland → "BirthIslandAIBehavior"
    │
    └── behaviorMgr.LoadBehavior(behaviorSign, parent, level)
            │                                               [ClientRoleAIBehaviorMgr.cs]
            ├── BehaviorPath = "Assets/ToBundle/RoleAI/AIBehavior/"
            ├── AssetManager.LoadAsset<ExternalBehavior>(
            │       BehaviorPath + sign + ".asset")
            └── BehaviorTree tree = 创建行为树组件
                tree.ExternalBehavior = loadBehavior
```

**关键源码位置**：

| 文件 | 路径 | 职责 |
|------|------|------|
| `ConfigLoader.cs` | `Assets/Script/Asset/Loaders/ConfigLoader.cs` | `GetSORoleAI()` / `GetAiDeliveryConfigSO()` / `GetAiPersonConfigSO()` |
| `ClientRoleAIBehaviorMgr.cs` | `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIBehaviorMgr.cs` | 行为树加载/驱动 |
| `ClientRoleAILoadMgr.cs` | `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAILoadMgr.cs` | 资源加载管理 |
| `RoleAISpawnerManager.cs` | `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/RoleAISpawnerManager.cs` | 投放配置加载 |

### 1.4 禁止修改的文件

- **`RoleAIAction.cs`** — Action 节点基类，所有 Action 继承此类，修改影响全部 93 个节点
- **`RoleAIConditional.cs`** — Conditional 节点基类，修改影响全部条件节点
- **`RoleAIManager.cs`** — 管理器核心逻辑，Feature 系统调度中枢
- **`ClientRoleAIBehaviorMgr.cs`** — 行为树加载/销毁核心流程，不可随意修改加载路径
- **`ConfigLoader.cs`** — 全局配置加载器，AI 仅为其中一部分，修改需评估全局影响

---

## 二、新建/扩展 Checklist

> 以下覆盖三种典型操作场景：**新增行为树节点**、**新增行为树**、**调整 AI 投放策略**。

### 场景 A：新增行为树 Action 节点

#### Phase 1：创建节点文件

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Client/Modules/RoleAI/AIBehavior/Action/RoleAI{NodeName}.cs` | 新增 | 继承 `RoleAIAction`，重写 `OnUpdate()` |

#### Phase 2：配置行为树

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 2 | `Assets/ToBundle/RoleAI/AIBehavior/{BehaviorSign}.asset` | 修改 | 在 Behavior Designer 编辑器中将新节点拖入行为树 |
| 3 | — | 检查 | 确认节点在 Behavior Designer 的 Task 面板 → `NewRoleAI` 分类下可见 |

### 场景 B：新增行为树 Conditional 节点

#### Phase 1：创建节点文件

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Client/Modules/RoleAI/AIBehavior/Conditional/RoleAI{NodeName}.cs` | 新增 | 继承 `RoleAIConditional` 或 `DelayRoleAIConditional`，重写 `OnUpdate()` |

#### Phase 2：配置行为树

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 2 | `Assets/ToBundle/RoleAI/AIBehavior/{BehaviorSign}.asset` | 修改 | 在 Behavior Designer 编辑器中将新条件节点拖入行为树 |

### 场景 C：新增 AI 投放配置（新地图/新模式）

#### Phase 1：创建全局 AI SO

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `ScriptableObject/AI/{GameMode}_{MapSign}_Level{N}.asset` | 新增 | Unity 菜单 `Create → War/RoleAI/SORoleAI`，配置 `AddAITime`、`AddAIMaxAmount` 等 |

#### Phase 2：创建投放策略 SO

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 2 | `ScriptableObject/AIDrop/Config/Maps/AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}.asset` | 新增 | 配置投放条件、时间间隔、数量上限 |
| 3 | `ToBundle/Config/Txt/AiDropMap.txt` | 修改 | 新增一行：`AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}` |

#### Phase 3：验证

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | — | 检查 | 进入对应模式地图，确认 AI 正常投放 |
| 5 | — | 检查 | 确认 AI 难度等级与 `AIBehaviorMap.txt` 映射正确 |

---

## 三、配置文件详解

### 3.1 AIBehaviorMap.txt — AI 行为映射

> 映射 **匹配模式 + AI 等级 → 行为树等级**，决定 AI 使用哪个难度的行为树。

**格式示例**（Tab 分隔）：

```
id	MatchMode	AILevel	behaviorLv
0	1	1	1
1	1	2	1
10	37	1	1
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 唯一标识（主键） |
| `MatchMode` | int | 匹配模式 ID（对应游戏模式枚举） |
| `AILevel` | int | AI 等级（1-3，由 `WarData.AILevel` 决定） |
| `behaviorLv` | int | 行为树等级（映射到行为树文件名后缀，如 L1/L2/L3） |

**特殊注意**：`behaviorLv` 不是直接等于 `AILevel`，存在模式特定的映射逻辑。

### 3.2 SORoleAIItem.txt — AI 道具/装备配置

> 定义不同地图和等级下 AI 随机生成的武器、配件、子弹、防甲、医疗品。

**格式示例**（Tab 分隔，部分字段含 `|` 分隔的多值列表）：

```
id	ItemList1	ItemList1Probability	Parts1	Parts1Probability	...
CombatIsland_AI_Lv0	S12K|S686|...	0.03|0.09|...	0|1	0.8|0.2	...
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 配置标识（`{MapSign}_AI_Lv{N}`） |
| `ItemList1` | string[] | 主武器列表（`|` 分隔） |
| `ItemList1Probability` | float[] | 主武器概率权重（`|` 分隔，总和不必为 1） |
| `Parts1` / `Parts1Probability` | | 主武器配件等级及概率 |
| `ItemList2-4` | | 副武器/手枪/近战武器列表 |
| `Bullet` / `BulletProbability` | | 子弹数量及概率 |
| `Armor` / `ArmorProbability` | | 防甲等级及概率 |
| `ArmorLevel` / `ArmorLevelProbability` | | 防甲品质 |
| `MedicineType` / `MedicineTypeProbability` | | 医疗品类型及概率 |
| `MedicineNum` / `MedicineNumProbability` | | 医疗品数量及概率 |

**特殊注意**：Probability 是权重值而非百分比，系统内部做归一化处理。

### 3.3 SORoleAIFashion.txt — AI 时装配置

> 定义 AI 角色的外观随机搭配规则。

**格式示例**（Tab 分隔）：

```
id	SuitProbability	Suit	Hair	Countenance	Shirt	Bottoms	Shoe	Coat	FaceDecoration	HandDecorated	BodyType	TypeProbability	TopRing	FlyHigh	SexProbability
Lv1_Fashion	0.5	Suit_1|Suit_2|Suit_6|...	Hair_2|Hair_3|...	...
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 配置标识（`Lv{N}_Fashion` 或 `Birth_{N}`） |
| `SuitProbability` | float | 套装出现概率（整套 vs 拆分搭配） |
| `Suit` | string[] | 套装 ID 列表 |
| `Hair` | string[] | 发型 ID 列表 |
| `Countenance` | string[] | 表情 ID 列表 |
| `Shirt` / `Bottoms` / `Shoe` / `Coat` | string[] | 衣着部件 ID 列表 |
| `BodyType` | string[] | 体型列表 |
| `TypeProbability` | float[] | 体型概率 |
| `SexProbability` | float | 性别概率 |

### 3.4 AiDropMap.txt — AI 投放映射

> 投放配置 SO 的唯一标识注册表。

**格式示例**：

```
id
AiDeliveryConfig_ClassicMode_SOCatIsland_Level1
AiDeliveryConfig_ClassicMode_SOCatIsland_Level2
AiDeliveryConfig_ArcadeMode_SOCatIsland_Level1
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 投放配置标识（命名规则：`AiDeliveryConfig_{GameMode}_SO{MapSign}_Level{N}`） |

**特殊注意**：新增投放配置 SO 后必须在此表注册，否则运行时无法加载。

### 3.5 AiParamLocator.txt — AI 参数定位器

> 根据匹配条件定位 AI 难度参数。

**格式示例**（Tab 分隔）：

```
id	match_mode	group_mode	match_type	roomlv_of_grade_score	roomlv_of_hide_score	born_island_ai	battlefield_ai
3	1	1	0	1	1	20	8
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | ushort | 唯一标识 |
| `match_mode` | int | 匹配模式 |
| `group_mode` | int | 人数模式 |
| `match_type` | int | 匹配类型 |
| `roomlv_of_grade_score` | int | 硬实力等级（段位分） |
| `roomlv_of_hide_score` | int | 软实力等级（隐藏分） |
| `born_island_ai` | int | 出生岛 AI 数量 |
| `battlefield_ai` | int | 战场 AI 数量 |

### 3.6 RookieCampAI.txt — 新手营 AI

> 新手训练营的固定 AI 角色配置。

**格式示例**（Tab 分隔）：

```
id	name	isTeam	behaviorName	fashionId	equips
Team_1	队长	1	RookieAIBehavior	3	
Enemy_1	AI标靶	0	RookieAIBehavior	0	S686
Team_2	队长	1	RookieAIBehavior	3	UMP9|MedKit
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识 |
| `name` | string | 显示名称 |
| `isTeam` | int | 是否队友（1=队友, 0=敌人） |
| `behaviorName` | string | 行为树名称 |
| `fashionId` | int | 时装配置 ID |
| `equips` | string[] | 装备列表（`|` 分隔） |

### 3.7 RobotGun.txt — 机器人枪械参数

> 载具上 AI 控制的枪械射击参数。

**格式示例**（Tab 分隔）：

```
car_sign	add_shoot_srange_fire_num	fire_shoot_range	min_shoot_range	max_shoot_range	zhunxing	pre_shoot_time	gun_too_hot_fire_num	gun_too_hot_cool_time	shoot_delta_time
MachineArmor	5	5	10	45	4	1	60	2	0.08
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `car_sign` | string | 载具标识 |
| `add_shoot_srange_fire_num` | int | 射多少发后开始扩散 |
| `fire_shoot_range` | float | 基础射击扩散 |
| `min_shoot_range` / `max_shoot_range` | float | 最小/最大射击扩散 |
| `zhunxing` | float | 准星大小 |
| `pre_shoot_time` | float | 预热时间（秒） |
| `gun_too_hot_fire_num` | int | 射多少发过热 |
| `gun_too_hot_cool_time` | float | 过热冷却时间（秒） |
| `shoot_delta_time` | float | 射击间隔（秒） |

---

## 四、关键代码修改点

### 4.1 新增 Action 节点

**文件**：`Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAI{NodeName}.cs`

```csharp
using BehaviorDesigner.Runtime;
using BehaviorDesigner.Runtime.Tasks;
using UnityEngine;

[TaskName("{NodeName}")]
[TaskCategory("NewRoleAI")]
public class RoleAI{NodeName} : RoleAIAction
{
    // 行为树面板参数（可在 Behavior Designer 编辑器中配置）
    [SerializeField] private SharedInt target;
    [SerializeField] private float {paramName} = {defaultValue};
    
    // 节点进入时调用一次
    public override void OnStart()
    {
        base.OnStart();
        // 初始化逻辑
    }
    
    // 每帧调用，返回 TaskStatus（Success/Failure/Running）
    public override TaskStatus OnUpdate()
    {
        if (logic == null) return TaskStatus.Failure;
        
        // 核心逻辑
        // logic — ClientRoleAILogic 引用
        // gameWorld — BattleWorld 引用
        // manager — ClientRoleAIManager 引用
        
        return TaskStatus.Success;
    }
    
    // 节点退出时调用（无论成功/失败）
    public override void OnEnd()
    {
        base.OnEnd();
        // 清理逻辑
    }
}
```

**关键 API**：
- `logic.Position` — AI 当前位置
- `logic.RoleAIFireState` — 开火状态枚举
- `logic.HealthState` — 健康状态（Normal/Weak/Dead）
- `GetTargetPosition(target)` — 获取目标位置
- `GetTargetHeadPosition(target)` — 获取目标头部位置（用于射线检测）
- `RoleAIHelper.HasObstacle(from, to, hitInfos)` — 射线检测障碍物

### 4.2 新增 Conditional 节点

**文件**：`Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAI{NodeName}.cs`

```csharp
using BehaviorDesigner.Runtime;
using BehaviorDesigner.Runtime.Tasks;
using UnityEngine;

[TaskName("Check {NodeName}")]
[TaskCategory("NewRoleAI")]
public class RoleAI{NodeName} : RoleAIConditional  // 或 DelayRoleAIConditional
{
    [SerializeField] private SharedInt target;
    [SerializeField] private float threshold = {defaultValue};
    
    public override TaskStatus OnUpdate()
    {
        if (logic == null) return TaskStatus.Failure;
        
        // 条件判断逻辑
        bool conditionMet = /* ... */;
        
        // 如果继承 DelayRoleAIConditional，使用 DelayTaskStatus 包裹返回值
        // return DelayTaskStatus(conditionMet ? TaskStatus.Success : TaskStatus.Failure);
        
        return conditionMet ? TaskStatus.Success : TaskStatus.Failure;
    }
}
```

**Conditional 基类选择**：

| 基类 | 适用场景 |
|------|---------|
| `RoleAIConditional` | 即时条件判断（无延迟） |
| `DelayRoleAIConditional` | 带延迟的条件判断（避免频繁切换） |
| `IntervalRoleAIConditional` | 间隔执行的条件（降低 CPU 消耗） |
| `RandomDelayRoleAIConditional` | 随机延迟条件（增加 AI 行为多样性） |

### 4.3 SORoleAI 全局配置

**文件**：`Assets/Script/GamePlay/Host/Modules/RoleAI/ScriptableObject/SORoleAI.cs`（需要看这个 SO 的结构）

> 通过 Unity Inspector 配置，关键字段包括：

```csharp
[CreateAssetMenu(menuName = "War/RoleAI/SORoleAI")]
public class SORoleAI : ScriptableObject
{
    public float AddAITime;                     // 添加 AI 的时间间隔（秒）
    public int AddAIMaxAmount;                  // 每次添加 AI 数量
    public float RealPlayerFullAddAITime;       // 真人满员时的添加间隔
    public float CondNoEnemyNearby;             // "附近无敌人"条件距离
    public List<RefreshNumForTimes> RefreshNumForTimes;  // 时间区间刷新参数
}
```

### 4.4 RoleAIConfig 单体参数

**文件**：`Assets/Script/GamePlay/Host/Modules/RoleAI/ScriptableObject/RoleAIConfig.cs`

> AI 个体行为参数，通过 Inspector 编辑：

```csharp
[CreateAssetMenu(menuName = "War/RoleAI/RoleAI")]
public class RoleAIConfig : ScriptableObject
{
    public int HitRate = 5;                     // 命中概率（0-100）
    public float HitRoleDamageRatio = 0.1f;     // 对玩家伤害比例
    public int HitCountForKill = 10;            // 击中 N 次后直接击杀
    public float MoveSpeed = 3f;                // 移动速度
    public float FireMoveSpeedRatio = 0.8f;     // 开火时移速倍率
    public float RunRate = 1.5f;                // 奔跑速度倍率
    public float SwimRate = 0.7f;               // 游泳速度倍率
    public float JumpHeight = 1.2f;             // 跳跃高度
    public float BattleFarTime = 20f;           // 交战逃跑时间阈值（秒）
    public float WeakDownValue = 1.26f;         // 虚弱衰减速度
    public float ResurrectMachineTime = 6f;     // 复活机使用时间（秒）
    public AnimationCurve MeleeChargeAttackSpeed; // 冲拳攻击速度曲线
}
```

---

## 五、常见问题与踩坑记录

### 5.1 新节点在 Behavior Designer 中不显示

**问题现象**：创建了新的 Action/Conditional 节点文件，但在 Behavior Designer 的 Task 列表中找不到。

**根因分析**：
1. 缺少 `[TaskCategory("NewRoleAI")]` 特性标注
2. 文件有编译错误导致未被加载
3. 基类选错（应继承 `RoleAIAction` / `RoleAIConditional` 而非直接继承 `Action` / `Conditional`）

**解决方案**：
1. 确认节点类添加了 `[TaskName("名称")]` 和 `[TaskCategory("NewRoleAI")]` 两个特性
2. 确认 Unity Console 无编译错误
3. 确认继承了正确的基类，`OnAwake()` 中会自动初始化 `logic` 引用

### 5.2 AI 投放后无行为（站立不动）

**问题现象**：AI 成功投放到场景中，但不执行任何行为，静止站立。

**根因分析**：
1. 行为树 SO 未正确加载（`BehaviorPath` 路径拼接错误）
2. `AIBehaviorMapConfig` 映射不到对应的行为树等级
3. `logic.HasAuthority` 返回 false，导致 `OnUpdate()` 直接跳过

**解决方案**：
1. 检查 `ClientRoleAIBehaviorMgr.BehaviorPath` + `behaviorSign` 拼接的完整路径是否对应实际 .asset 文件
2. 检查 `AIBehaviorMap.txt` 中是否有对应 MatchMode + AILevel 的条目
3. 确认 AI 创建时的 Authority 分配正确

### 5.3 AI 装备为空/武器不对

**问题现象**：AI 生成后没有武器或武器类型异常。

**根因分析**：
1. `SORoleAIItem.txt` 中对应 id 的 `ItemList1` 字段为空
2. 概率权重全为 0，随机结果无效
3. 对应的武器 Sign 在 `WeaponConfig` 表中不存在

**解决方案**：
1. 确认 `SORoleAIItem.txt` 中对应地图等级的配置存在且武器列表非空
2. 确认 `ItemList1Probability` 的值是有效的正数
3. 确认武器 Sign（如 `AK12`、`S686`）在 `WeaponConfig` 配置表中存在

### 5.4 AI 难度感知不明显

**问题现象**：调整了 `AILevel` 但 AI 行为没有明显差异。

**根因分析**：
1. `AIBehaviorMap.txt` 中不同 AILevel 映射到了相同的 `behaviorLv`
2. 行为树 SO 中不同等级使用了相同的参数
3. `RoleAIConfig` 中的 `HitRate`、`MoveSpeed` 等参数未区分等级

**解决方案**：
1. 检查 `AIBehaviorMap.txt` 确认 behaviorLv 映射正确
2. 在 `Assets/ToBundle/RoleAI/AIBehavior/` 中确认不同等级的行为树 SO 参数有差异
3. 在对应的 `SORoleAI` 的 `RoleAIConfig` 中调整数值参数

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] Unity Console 无 NullReferenceException
- [ ] Behavior Designer 编辑器无报错

### 6.2 配置

- [ ] 新增的配置表条目格式正确（字段数量、类型匹配）
- [ ] `AiDropMap.txt` 新增条目对应的 SO 文件存在
- [ ] `AIBehaviorMap.txt` 映射逻辑覆盖目标 MatchMode + AILevel 组合
- [ ] 新增 SORoleAI SO 的 `AddAITime`、`AddAIMaxAmount` 参数合理

### 6.3 行为树

- [ ] 新节点在 Behavior Designer Task 面板 `NewRoleAI` 分类下可见
- [ ] 新节点的 `[TaskName]` 与 `[TaskCategory]` 特性标注正确
- [ ] 行为树在编辑器中可正常运行（Play 模式无报错）
- [ ] 条件节点返回值符合预期（Success/Failure）

### 6.4 运行时

- [ ] AI 按预期时间间隔投放
- [ ] AI 数量不超过 `AddAIMaxAmount` 上限
- [ ] AI 行为树正常驱动（非静止站立）
- [ ] AI 武器/装备随机生成符合配置概率
- [ ] AI 时装随机搭配正常
- [ ] 不同 AILevel 的 AI 行为差异明显

### 6.5 性能

- [ ] AI 数量峰值时 FPS 无明显下降
- [ ] 行为树 Tick 无死循环或无限递归
- [ ] NavMesh 寻路无异常卡顿

---

## 附录 A：行为树节点完整清单

### A.1 Action 节点（93 个文件）

| 节点 | 功能分类 | 说明 |
|------|---------|------|
| `RoleAIBaseFire` | 战斗 | 基础开火（点射/连射，可配精准度） |
| `RoleAIBlindageFire` | 战斗 | 掩体开火 |
| `RoleAIFire` | 战斗 | 高级开火（带目标跟踪） |
| `RoleAIDashFireByTargetHp` | 战斗 | 根据目标 HP 冲刺开火 |
| `RoleAIBlocking` | 战斗 | 格挡防守 |
| `RoleAIMeleeChargeAttack` | 战斗 | 近战冲拳攻击 |
| `RoleAIGuanyuSprint` | 战斗 | 关羽冲刺（特殊模式） |
| `RoleAIMoveTarget` | 移动 | 移动至指定目标 |
| `RoleAITargetPosMove` | 移动 | 移动至指定位置 |
| `RoleAIDirectionMove` | 移动 | 方向移动 |
| `RoleAIMoveToQuanCenter` | 移动 | 移动至毒圈中心 |
| `RoleAIMoveToResurrect` | 移动 | 移动至复活点 |
| `RoleAIMoveToPickCoin` | 移动 | 移动至硬币位置 |
| `RoleAIBornMove` | 移动 | 出生岛移动 |
| `RoleAIRookieTargetPosMove` | 移动 | 新手训练移动 |
| `RoleAIFollow` | 移动 | 跟随目标 |
| `RoleAIRangeFollow` | 移动 | 范围内跟随 |
| `RoleAIEscape` | 移动 | 逃跑（脱离交战） |
| `RoleAIFar` | 移动 | 远离目标 |
| `RoleAIJump` | 动作 | 跳跃 |
| `RoleAIGlide` | 动作 | 滑翔 |
| `RoleAILookAt` | 动作 | 朝向目标 |
| `RoleAIPickItem` | 物品 | 拾取物品 |
| `RoleAIRookiePickItem` | 物品 | 新手训练拾取 |
| `RoleAIUseItem` | 物品 | 使用物品 |
| `RoleAICreateAndDropItem` | 物品 | 创建并丢弃物品 |
| `RoleAIReload` | 武器 | 装弹 |
| `RoleAINextWeapon` | 武器 | 切换武器 |
| `RoleAIUnEquipWeapon` | 武器 | 卸下武器 |
| `RoleAIMark` | 信息 | 标记 |
| `RoleAIMarkItem` | 信息 | 标记物品 |
| `RoleAIMarkSafeZonePoint` | 信息 | 标记安全区域点 |
| `RoleAISendCommand` | 指令 | 发送指令 |
| `RoleAIClearCommand` | 指令 | 清除指令 |
| `RoleAIUprearRole` | 队友 | 扶起队友 |
| `RoleAIUseResurrectionMachine` | 队友 | 使用复活机 |
| `RoleAIStopAction` | 控制 | 停止动作 |
| `RoleAIForbidTrans` | 控制 | 禁止变换 |
| `RoleAIChangeIdleState` | 控制 | 切换待机状态 |
| `RecordTimeAction` | 工具 | 记录时间 |
| `CheckSharedFloatAction` | 工具 | 检查共享浮点值 |
| `RoleAISearchSafeZonePoint` | 策略 | 搜索安全区域点 |
| `RoleAIChoseBlindagePos` | 策略 | 选择掩体位置 |
| `RoleAICalBlindageFirePos` | 策略 | 计算掩体开火位置 |
| `RoleAIFindAttackRole` | 搜索 | 寻找攻击目标 |
| `RoleAIFindAttackRoleCanFailure` | 搜索 | 寻找攻击目标（允许失败） |
| `RoleAIFindLockRole` | 搜索 | 寻找锁定目标 |
| `RoleAIFindNearRole` | 搜索 | 寻找最近角色 |
| `RoleAIFindSeeRole` | 搜索 | 寻找可视角色 |
| `RoleAIFindSeeRoleCanFailure` | 搜索 | 寻找可视角色（允许失败） |
| `RoleAIFindBlindage` | 搜索 | 寻找掩体 |
| `RoleAIFindCoinTeammatePosition` | 搜索 | 寻找硬币队友位置 |
| `RoleAIPartyModeFindLockRole` | 搜索 | Party 模式锁定目标 |

### A.2 Conditional 节点

| 节点 | 功能分类 | 说明 |
|------|---------|------|
| `RoleAICheckDistance` | 距离 | 检查与目标距离（支持视线检测） |
| `RoleAICheckQuanCenterDistance` | 距离 | 检查到毒圈中心距离 |
| `RoleAICheckGroundHeight` | 距离 | 检查地面高度 |
| `RoleAICheckIsDead` | 状态 | 检查是否死亡 |
| `RoleAICheckIsEquipWeapon` | 状态 | 检查是否装备武器 |
| `RoleAIIsWeaponNull` | 状态 | 检查武器是否为空 |
| `RoleAICheckBullet` | 状态 | 检查子弹数量 |
| `RoleAIIsNotEnoughBullet` | 状态 | 子弹不足判断 |
| `RoleAIHasMoveState` | 状态 | 检查移动状态 |
| `RoleAIHasJumpState` | 状态 | 检查跳跃状态 |
| `RoleAIHasUseItemState` | 状态 | 检查使用物品状态 |
| `RoleAICheckTargetHasPath` | 寻路 | 检查目标是否有路径 |
| `RoleAIHasObstacle` | 寻路 | 检查障碍物 |
| `RoleAICheckItem` | 物品 | 检查物品 |
| `RoleAICheckMarkItem` | 物品 | 检查标记物品 |
| `RoleAIHasMedical` | 物品 | 检查是否有医疗品 |
| `RoleAIHasMedicalNearby` | 物品 | 检查附近是否有医疗品 |
| `RoleAIHasWeaponEquipNearby` | 物品 | 检查附近是否有武器装备 |
| `RoleAIHasItemRange` | 物品 | 物品范围检查 |
| `RoleAIHealthIsNotEnough` | 健康 | 血量不足判断 |
| `RoleAICanMark` | 信息 | 检查是否可标记 |
| `RoleAICheckCommand` | 指令 | 检查指令 |
| `RoleAICheckRandom` | 随机 | 概率随机条件 |
| `RoleAICheckTeamUprear` | 队友 | 检查队友是否需扶起 |
| `RoleAIHasTeammatesWaitingBeResurrected` | 队友 | 检查是否有队友等待复活 |
| `RoleAICheckResurrectionMachineRange` | 队友 | 检查复活机范围 |
| `RoleAIHasEquipChange` | 装备 | 检查装备变更 |
| `RoleAIHasWeaponChange` | 装备 | 检查武器变更 |
| `RoleAIIsBirthIsland` | 场景 | 是否在出生岛 |
| `RoleAIIsInSafeZone` | 场景 | 是否在安全区 |
| `RoleAIIsPosInSafeZone` | 场景 | 位置是否在安全区 |
| `RoleAIInBlindageCheck` | 场景 | 掩体内检查 |
| `RoleAIBlindageLigalCheck` | 场景 | 掩体合法性检查 |
| `RoleAIStateCheck` | 通用 | 状态检查 |
| `RoleAICheckRookieAction` | 新手 | 新手训练动作检查 |
| `RoleAICheckRookieData` | 新手 | 新手训练数据检查 |
| `DelayRoleAIConditional` | 基类 | 延迟条件基类 |
| `IntervalRoleAIConditional` | 基类 | 间隔条件基类 |
| `RandomDelayRoleAIConditional` | 基类 | 随机延迟条件基类 |
