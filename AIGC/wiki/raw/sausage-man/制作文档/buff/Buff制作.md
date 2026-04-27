# 1 代架构 Buff 制作规范

> **适用范围**：基于 `BuffSOBase` / `BuffSystemBase` 的 1 代 Buff 系统开发（BSO/BS/BSClient/BSServer 四文件模式）
> **不适用**：2 代 Ability 系统（`Biubiubiu2/` 下的 `SAB_`/`SAE_` 前缀类）
> **参考实现**：击退 Buff（BeatBack），路径 → Host: `BSOBeatBack` / `BSBeatBack`，Client: `BSBeatBackClient`，Server: `BSBeatBackServer`

**占位符说明**：

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{BuffName}` | Buff 功能名（大驼峰） | `BeatBack`、`CircleTriggerDamage` |
| `{BuffSign}` | Buff 标识符（配置表主键） | `BeatBack`、`PVEPoisonGas` |
| `{BuffCategory}` | Buff 所属分类目录 | `Common`、`PVE`、`GoldDash` |

---

## 一、架构概述

### 1.1 Buff 体系分类

1 代 Buff 系统存在三种基类分支，新建 Buff 时需根据效果类型选择正确的基类：

| 维度 | 普通 Buff | 破坏物 Buff | 速度 Buff |
|------|----------|------------|----------|
| **BSO 基类** | `BuffSOBase` | `HpBuffSOBase` | `BuffSpeedSOBase` |
| **BS 基类** | `BuffSystemBase` | `HpBuffSystemBase` | `BuffSystemBase` |
| **典型用途** | 击退、触发器、护盾、特效 | 可被击碎的障碍物/物体 | 加速/减速效果 |
| **特有字段** | 无 | `Hp`、`HPOverBuff[]`、`weaponHitRatio[]` | `AddSpeedRatio` |
| **血量管理** | ❌ | ✅ ServerDownHp/ClientDownHp | ❌ |
| **实例数量** | 多数 Buff | ~20+ | ~10+ |

### 1.2 核心类依赖

```
Assets/Script/UI/War/BuffControl/                    ← 框架层（⚠️ 不在 GamePlay/ 下）
    ├── BuffControl.cs              ← Buff 管理器（入口：PlayBuff / RemoveBuff）
    │   ├── ServerBuffControl       ← Server 端 Buff 管理
    │   └── ClientBuffControl       ← Client 端 Buff 管理
    ├── BuffBox.cs                  ← Buff 数据容器（关联 BS + 三端数据）
    │   ├── BuffBoxServer.cs [S]    ← Server/GamePlay/Server/Modules/Buff/
    │   └── BuffBoxClient.cs [C]    ← Client/GamePlay/Client/Modules/Buff/
    ├── BuffSOBase.cs               ← BSO 基类（ScriptableObject，配置数据）
    │   ├── HpBuffSOBase.cs         ← 破坏物 BSO 基类（带 HP）
    │   └── BuffSpeedSOBase.cs      ← 速度 BSO 基类
    ├── BuffSystemBase.cs           ← BS 基类（Host 共享逻辑 + 端侧分发）
    │   └── HpBuffSystemBase.cs     ← 破坏物 BS 基类
    ├── IBuffSystemBase.cs          ← 端侧逻辑接口
    └── IBuffBox.cs                 ← 容器接口

Assets/Script/GamePlay/                              ← 实现层
    ├── Host/Modules/Buff/
    │   ├── BuffScriptableObject/   ← BSOXxx.cs（241 个配置类）
    │   └── BuffSystem/             ← BSXxx.cs（236 个逻辑类）
    ├── Client/Modules/Buff/
    │   ├── BuffSystemClientBase.cs ← Client 端侧基类
    │   └── BuffSystem/             ← BSXxxClient.cs（265 个）
    └── Server/Modules/Buff/
        ├── BuffSystemServerBase.cs ← Server 端侧基类
        └── BuffSystem/             ← BSXxxServer.cs（282 个）
```

**三端入口类**：

| 端 | 入口类 | 路径 |
|----|--------|------|
| **H** (Host) | `BuffControl` | `Assets/Script/UI/War/BuffControl/BuffControl.cs` |
| **C** (Client) | `BuffSystemClientBase` | `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystemClientBase.cs` |
| **S** (Server) | `BuffSystemServerBase` | `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystemServerBase.cs` |

### 1.3 四文件模式（核心创建模式）

每个 Buff 由最多 **4 个文件**组成，缺一不可（部分简单 Buff 可省略 Client/Server）：

```
BSOXxx.cs ─────→ BSXxx.cs ─────→ BSXxxServer.cs
(ScriptableObject)  (Host 逻辑)      (Server 逻辑)
    配置数据         init()            RequestServer<>()
    面板参数         InitServer()
                     InitClient() ───→ BSXxxClient.cs
                                       (Client 逻辑)
                                       RequestClient<>()
```

| 文件 | 前缀 | 基类 | 职责 | 目录 |
|------|------|------|------|------|
| `BSO{BuffName}.cs` | `BSO` | `BuffSOBase` | 配置数据、面板参数、创建 BS 实例 | `Host/.../BuffScriptableObject/` |
| `BS{BuffName}.cs` | `BS` | `BuffSystemBase` | Host 端共享逻辑，分发到 Client/Server | `Host/.../BuffSystem/` |
| `BS{BuffName}Server.cs` | `BS...Server` | `BuffSystemServerBase` | 服务端独有逻辑（碰撞、伤害、计时） | `Server/.../BuffSystem/` |
| `BS{BuffName}Client.cs` | `BS...Client` | `BuffSystemClientBase` | 客户端独有逻辑（特效、动画、音效） | `Client/.../BuffSystem/` |

### 1.4 预制体与资源加载（★ 强制）

Buff 系统涉及 **两套资源加载链**：SO 资产加载和特效 Prefab 加载，分别由不同的配置表驱动。

#### 1.4.1 资源目录总览

```
Assets/ToBundle/
├── ScriptableObject/Buff/              ← SO 资产（Buff 配置数据）
│   ├── Common/                         ← 通用 Buff（BeatBack.asset 等）
│   ├── AddEffectObj/          (137)    ← 特效物体类 Buff
│   ├── Skills/                (113)    ← 技能类 Buff
│   ├── OnlyUp/                (123)    ← OnlyUp 模式
│   ├── Slime/                 (75)     ← 史莱姆模式
│   ├── ClientBomb/            (59)     ← 客户端炸弹
│   ├── LineMove/              (45)     ← 直线移动类
│   ├── GoldDash/              (35)     ← 金币冲刺模式
│   ├── TotemConsume/          (37)     ← 图腾消耗类
│   ├── TotemAddAttr/          (48)     ← 图腾属性加成
│   └── ... (共 170+ 子目录, 1,280 个 .asset 文件)
│
└── Effect/Buff/                        ← 特效 Prefab（视觉表现）
    ├── Common/                (61)     ← 通用特效
    ├── BeastCamp/             (133)    ← 怪兽营地特效
    ├── Dungeon/               (16)     ← 地牢特效
    ├── GoldDash/ → 注意：GoldDash 特效部分位于
    │     Assets/ToBundle/Biubiubiu2/GoldDash/Effect/
    ├── Slime/                 (10)     ← 史莱姆特效
    └── ... (共 20 子目录, 290+ prefab 文件)
```

#### 1.4.2 资源路径与配置表

| 资源类型 | 路径模板 | 配置表 | 管理类 |
|---------|---------|--------|--------|
| **SO 资产** | `Assets/ToBundle/ScriptableObject/Buff/{BuffCategory}/{BuffSign}.asset` | `BuffAsset` | `BuffAssetConfig.cs` |
| **特效 Prefab** | `Assets/ToBundle/Effect/{EffectCategory}/{EffectSign}.prefab` | `EffectAsset` | `EffectAssetConfig.cs` |
| **加载入口** | — | — | `ConfigLoader.cs` / `EffectPool.cs` |

**配置表格式**：

| 配置表 | 格式（Tab 分隔） | 说明 |
|--------|-----------------|------|
| `BuffAsset` | `{BuffSign}\t{BuffCategory}` | SO 加载路径映射 |
| `EffectAsset` | `{EffectSign}\t{source}\t{path}\t{visualForDevice}` | 特效加载路径映射 |

#### 1.4.3 SO 资产加载链

```
BuffControl.PlayBuff(sign, fireRoleId, lockRoleId)
    │
    ▼
AssetsLoad.GetSOBuffData(sign)                          [ConfigLoader.cs]
    │
    ├── BuffAssetConfig.Get(sign)                       [BuffAssetConfig.cs]
    │       └── 查表：ConfigManager.GetConfigRawDatas("BuffAsset")
    │       └── 返回：{id: "{BuffSign}", path: "{BuffCategory}"}
    │
    └── AssetManager.LoadAsset<BuffSOBase>(
            "Assets/ToBundle/ScriptableObject/Buff/{path}/{id}.asset"
        )
    │
    ▼
BuffSOBase so = loaded asset
    │
    ▼
so.init(buffBox)                                        [BSOXxx.cs]
    └── 创建 BSXxx 实例
    └── BSXxx.Init(buffBox, so)
        ├── InitServer() → RequestServer<BSXxxServer>()
        └── InitClient() → RequestClient<BSXxxClient>()
```

#### 1.4.4 特效 Prefab 加载链

特效在 **BSClient** 端代码中加载，通过 `EffectPool` 统一管理：

```
BSXxxClient.Init(buffSystem)
    │
    ├── 获取 BSO 配置中的特效 Sign
    │   config = (BSOXxx)buffSystem.MyBuffSOData
    │   effectSign = config.effectSign  // BSO 面板配置的字段
    │
    ▼
EffectPool.Get(effectSign)  或  EffectPool.GetAsync(effectSign, callback)
    │                                                   [EffectPool.cs]
    ├── EffectAssetConfig.Get(effectSign)               [EffectAssetConfig.cs]
    │       └── 返回：{source, path, visualForDevice}
    │       └── source: 0=Effect/, 1=BirthIsland/, 2=GoldDash/, 3=Pet/
    │
    └── 拼接路径：
        source=0 → "Assets/ToBundle/Effect/{path}/{effectSign}.prefab"
        source=1 → "Assets/Scenes/BirthIsland/Effect/{path}/{effectSign}.prefab"
        source=2 → "Assets/ToBundle/Biubiubiu2/GoldDash/Effect/{path}/{effectSign}.prefab"
        source=3 → "Assets/ToBundle/Biubiubiu2/GamePlay/Pet/Effect/{path}/{effectSign}.prefab"
    │
    ▼
GameObject effectObj = Instantiate(prefab)  // 从对象池获取或新建
```

**关键源码位置**：

| 文件 | 路径 | 职责 |
|------|------|------|
| `EffectPool.cs` | `Assets/Script/Asset/GameObjectPools/EffectPool.cs` | 特效对象池（加载/缓存/回收） |
| `EffectAssetConfig.cs` | `Assets/Script/Config/EffectAssetConfig.cs` | 特效配置表解析 |
| `BuffAssetConfig.cs` | `Assets/Script/Config/BuffAssetConfig.cs` | SO 配置表解析 |
| `ConfigLoader.cs` | `Assets/Script/Asset/Loaders/ConfigLoader.cs` | `GetSOBuffData()` 入口 |

#### 1.4.5 新建 Buff 资源放置清单

新建一个 Buff 时需要创建/配置的资源文件：

| # | 资源 | 放置路径 | 配置表注册 |
|---|------|---------|-----------|
| 1 | SO 资产（`.asset`） | `Assets/ToBundle/ScriptableObject/Buff/{BuffCategory}/{BuffSign}.asset` | `BuffAsset` 表添加一行 |
| 2 | 特效 Prefab（如有） | `Assets/ToBundle/Effect/Buff/{EffectCategory}/{EffectSign}.prefab` | `EffectAsset` 表添加一行 |
| 3 | 音效文件（如有） | 参考现有音效目录 | BSO 的 `PlaySoundData[]` 配置 |

> ⚠️ 所有资源必须放在 `Assets/ToBundle/` 目录下才能被打包。放在其他目录（如 `Assets/Art/`）的资源在打包后将无法加载。

### 1.5 Buff 生命周期

```
┌─────────────────────────────────────────────────────────────┐
│  创建阶段                                                    │
│  BuffControl.PlayBuff(sign)                                  │
│    → AssetsLoad.GetSOBuffData(sign)  加载 SO                 │
│    → new BuffBox().Init(gameWorld)   创建容器                │
│    → SO.init(buffBox)               创建 BS 实例            │
│    → BS.Init(buffBox, SO)           初始化 Host 逻辑        │
│    → BS.InitServer() / BS.InitClient()  创建三端逻辑        │
│    → ServerBuffControl.SyncAddBuff()    同步到客户端         │
├─────────────────────────────────────────────────────────────┤
│  运行阶段                                                    │
│  BuffControl.OnUpdate()                                      │
│    → 遍历 userBuffList                                       │
│    → BuffBox.OnUpdate()                                      │
│       ├── BuffBoxServer.OnUpdate()  Server 同步（0.1s 间隔） │
│       ├── BuffBoxClient.OnUpdate()  Client 表现              │
│       └── BuffSystemBase.OnUpdate() Host 通用逻辑            │
├─────────────────────────────────────────────────────────────┤
│  销毁阶段                                                    │
│  BuffControl.RemoveBuff(buffId)                              │
│    → buffBox.isClear = true         标记清理                 │
│    → 下帧 BuffControl.BuffEvent()   实际清理                 │
│       ├── BuffBoxServer.Clear()  → SyncRemoveBuff()          │
│       ├── BuffBoxClient.Clear()  → ClearEffect()             │
│       └── BuffSystemBase.Clear() → ClearLoops()              │
│    → userBuffList.RemoveAt(i)       从列表移除               │
└─────────────────────────────────────────────────────────────┘
```

### 1.6 同步架构

Buff 的同步由 `BuffSOBase.SyncState` 控制，在 SO Inspector 面板中配置：

| SyncState | 说明 | 适用场景 |
|-----------|------|---------|
| `Range` | 发送给范围内玩家 | 大多数战斗 Buff |
| `RangeXZ` | 范围内（忽略 Y 轴） | 地面效果 |
| `TeamAndRange` | 队友 + 范围内 | 团队增益 |
| `Team` | 仅队友 | 纯队伍效果 |
| `OnlyServer` | 仅服务器执行 | 判定逻辑 Buff |
| `OnlySelf` | 仅发给自己 | 自身状态效果 |
| `World` | 全场广播 | 全局事件 Buff |
| `Custom` | 自定义（需实现 `GetCustomSyncList`） | 特殊逻辑 |

同步范围由 `SyncRangeDistance`（移动端）和 `PCSyncRangeDistance`（PC 端）两个字段控制。

### 1.7 禁止修改的文件

| 文件 | 原因 |
|------|------|
| **`BuffControl.cs`** | Buff 系统核心管理器，修改影响全局 |
| **`BuffBox.cs`** | 数据容器基础结构，修改影响所有 Buff |
| **`BuffSOBase.cs`** | 基类字段变更会导致所有 SO 资产反序列化异常 |
| **`BuffSystemBase.cs`** | 基类方法变更影响全部 236+ 个 BS 子类 |
| **`BuffAssetConfig.cs`** | 配置加载器，修改影响 Buff 加载流程 |
| **`ConfigLoader.cs`** | 全局资源加载器，非 Buff 专属 |

---

## 二、新建 Buff Checklist

> 以下步骤按执行顺序编排。假设新建名为 `{BuffName}` 的普通 Buff。

### Phase 1：配置表注册

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `BuffAsset` 配置表 | 新增一行 | 添加 `{BuffSign}\t{BuffCategory}`，BuffSign 是唯一标识 |

### Phase 2：创建 ScriptableObject 配置类（BSO）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 2 | `Host/.../BuffScriptableObject/BSO{BuffName}.cs` | 新建 | 继承 `BuffSOBase`，添加 `[CreateAssetMenu]`，实现 `init()` |
| 3 | Unity Editor | 操作 | 右键 → Create → War/Buff/BSO{BuffName}，创建 SO 资产文件 |
| 4 | SO 资产文件 | 配置 | 在 Inspector 面板中填写 BuffName、SyncState、同步范围等基础参数 |

### Phase 3：创建 Host 端逻辑类（BS）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `Host/.../BuffSystem/BS{BuffName}.cs` | 新建 | 继承 `BuffSystemBase`，实现 `InitServer()` / `InitClient()` |

### Phase 4：创建 Server 端逻辑类

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | `Server/.../BuffSystem/BS{BuffName}Server.cs` | 新建 | 继承 `BuffSystemServerBase`，实现服务端逻辑（伤害、碰撞、计时等） |

### Phase 5：创建 Client 端逻辑类

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 7 | `Client/.../BuffSystem/BS{BuffName}Client.cs` | 新建 | 继承 `BuffSystemClientBase`，实现客户端表现（特效、动画、音效） |

### Phase 6：资源创建与配置

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `Assets/ToBundle/ScriptableObject/Buff/{BuffCategory}/` | 检查 | 确认目录存在，不存在则创建 |
| 9 | SO 资产文件 | 移动/保存 | 将创建的 `.asset` 文件放到正确目录，文件名为 `{BuffSign}.asset` |
| 10 | `BuffAsset` 配置表 | 检查 | 确认 sign 与 SO 文件名一致，path 与目录名一致 |
| 11 | Unity Editor | 验证 | 进入 Play Mode，调用 `BuffControl.PlayBuff("{BuffSign}", ...)` 测试 |

---

## 三、配置文件详解

### 3.1 BuffAsset 配置表

**来源**：`ConfigManager.GetConfigRawDatas("BuffAsset")`

**格式**（Tab 分隔）：

```
BeatBack	Common
CircleTriggerDamage	Common
PVEPoisonGas	PVE
GoldDashTreasure	GoldDash
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `string` | Buff 标识符（即 `{BuffSign}`），也是 SO 资产文件名 |
| `path` | `string` | SO 文件所在子目录名（即 `{BuffCategory}`） |

**特殊注意**：
- `id` 是主键，全局唯一
- `path` 对应 `Assets/ToBundle/ScriptableObject/Buff/` 下的子目录名
- `BuffAssetConfig.Get(sign)` 通过 `id` 查找，返回 `null` 表示未注册

### 3.2 BuffSOBase Inspector 面板字段

所有 BSO 类共享 `BuffSOBase` 的以下面板字段：

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `BuffName` | `string` | Buff 显示名称 | — |
| `BuffItemId` | `long` | 编号数据 | 0 |
| `IsOpenUpdate` | `bool` | 是否启用每帧 `OnUpdate()` | `false` |
| `SyncState` | `BuffBox.SyncState` | 同步方式（见 §1.6） | `Range` |
| `SyncRangeDistance` | `int` | 移动端同步范围 | — |
| `PCSyncRangeDistance` | `int` | PC 端同步范围 | — |
| `BuffHeight` | `float` | Buff 物理高度 | 0 |
| `BuffRadius` | `float` | Buff 物理半径 | 0 |
| `PlaySoundData[]` | `SoundData[]` | 音效配置数组 | 空 |

**SoundData 子结构**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `Name` | `string` | 音效名称 |
| `Sign` | `string` | 查询键 |
| `Sound` | `string` | 本地音效 ID |
| `GlobalSound` | `string` | 海外音效 ID |

### 3.3 HpBuffSOBase 额外字段（破坏物 Buff 专用）

继承 `BuffSOBase` 之上额外增加：

| 字段 | 类型 | 说明 |
|------|------|------|
| `Hp` | `float` | 破坏物血量 |
| `HPOverBuff[]` | `BuffSOBase[]` | 血量归零后触发的 Buff 列表 |
| `weaponHitRatio[]` | `WeaponTypeHitRatio[]` | 按武器类型的伤害系数 |
| `weaponSignHitRatio[]` | `WeaponSignHitRatio[]` | 按具体武器 Sign 的伤害系数（优先级高于类型） |

---

## 四、关键代码修改点

### 4.1 BSO 配置类（Host）

**文件路径**：`Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSO{BuffName}.cs`

```csharp
using UnityEngine;

[CreateAssetMenu(menuName = "War/Buff/BSO{BuffName}")]
public class BSO{BuffName} : BuffSOBase
{
    // ===== 自定义配置字段（在 Inspector 面板中编辑）=====
    public float damage = 10f;
    public float duration = 3f;
    public float radius = 5f;

    // ===== 创建 BS 实例（固定模式）=====
    public override BuffSystemBase init(BuffBox buffBox)
    {
        BS{BuffName} system = new BS{BuffName}();
        system.Init(buffBox, this);
        return system;
    }

    // ===== 可选：使用权限检查 =====
    // public override string checkCanUser(BattleRoleLogic role)
    // {
    //     return null; // 返回 null 表示可以使用
    // }
}
```

**要点**：
- `[CreateAssetMenu]` 的 `menuName` 必须以 `War/Buff/` 开头
- `init()` 方法是固定模式：new BS → Init → return
- 自定义字段均为 `public`，暴露给 Inspector 面板

### 4.2 BS Host 逻辑类

**文件路径**：`Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BS{BuffName}.cs`

```csharp
public class BS{BuffName} : BuffSystemBase
{
    // ===== 端侧逻辑引用 =====
    public BS{BuffName}Server ServerLogic { get; set; }
    public BS{BuffName}Client ClientLogic { get; set; }

    // ===== Server 端初始化（固定模式）=====
    public override void InitServer(BuffBox buffBox, BuffSOBase buffSOData)
    {
        base.InitServer(buffBox, buffSOData);
        RequestServer<BS{BuffName}Server>();
    }

    // ===== Client 端初始化（固定模式）=====
    public override void InitClient(BuffBox buffBox, BuffSOBase buffSOData)
    {
        base.InitClient(buffBox, buffSOData);
        RequestClient<BS{BuffName}Client>();
    }

    // ===== 可选：Host 端通用逻辑 =====
    // public override void OnUpdate()
    // {
    //     base.OnUpdate();
    //     // Host 端每帧逻辑（Client 和 Server 共用的部分）
    // }
}
```

**要点**：
- `RequestServer<T>()` 和 `RequestClient<T>()` 是 `BuffSystemBase` 提供的泛型方法
- `ServerLogic` / `ClientLogic` 属性用于端侧反向引用 Host 逻辑
- 如果 Buff 无需 Server 逻辑，可省略 `InitServer()` 和对应文件
- 如果需要 Host 端的 `OnUpdate()`，必须在 BSO 中设置 `IsOpenUpdate = true`

### 4.3 BSServer 服务端逻辑

**文件路径**：`Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BS{BuffName}Server.cs`

```csharp
public class BS{BuffName}Server : BuffSystemServerBase
{
    private BSO{BuffName} config;
    private float timer;

    public override void Init(BuffSystemBase buffSystem)
    {
        base.Init(buffSystem);
        // 获取 SO 配置（向上转型）
        config = (BSO{BuffName})buffSystem.MyBuffSOData;
        // 反向注册到 Host 逻辑
        ((BS{BuffName})buffSystem).ServerLogic = this;

        timer = config.duration;
    }

    public override void OnUpdate()
    {
        base.OnUpdate();
        // Server 端逻辑：计时、伤害判定、碰撞检测等
        timer -= Time.deltaTime;
        if (timer <= 0)
        {
            // 通过 gameWorld.BuffControl 管理生命周期
            gameWorld.BuffControl.RemoveBuff(MyBuffBox.autoBuffId);
        }
    }

    public override void Clear()
    {
        base.Clear();
        // 清理 Server 端资源（碰撞体等）
    }
}
```

**要点**：
- 通过 `(BSO{BuffName})buffSystem.MyBuffSOData` 获取配置
- 通过 `((BS{BuffName})buffSystem).ServerLogic = this` 建立双向引用
- 移除 Buff 使用 `gameWorld.BuffControl.RemoveBuff(MyBuffBox.autoBuffId)`
- `base.Init()` 会自动处理 `ServerColliderName`（如果在 SO 中配置了碰撞体名称）

### 4.4 BSClient 客户端逻辑

**文件路径**：`Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BS{BuffName}Client.cs`

```csharp
public class BS{BuffName}Client : BuffSystemClientBase
{
    private BSO{BuffName} config;

    public override void Init(BuffSystemBase buffSystem)
    {
        base.Init(buffSystem);
        config = (BSO{BuffName})buffSystem.MyBuffSOData;
        ((BS{BuffName})buffSystem).ClientLogic = this;

        // Client 初始化逻辑：
        // - 播放特效
        // - 播放音效
        // - 设置动画
        BattleRoleLogic lockRole = MyBuffBox.LockRole;
        if (lockRole != null && lockRole.MyRole != null)
        {
            // 对目标角色施加表现效果
        }
    }

    public override void OnUpdate()
    {
        base.OnUpdate();
        // Client 端每帧表现逻辑
    }

    public override void Clear()
    {
        base.Clear();
        // 清理特效、音效等客户端资源
    }
}
```

**要点**：
- Client 端只做**表现**，不做判定
- 通过 `MyBuffBox.LockRole` / `MyBuffBox.FireRole` 获取关联角色
- 通过 `MyBuffBox.bornPoint` 获取 Buff 出生位置
- `animatorControl` 属性可用于动画控制
- 音效播放使用 `MyBuffSOData.GetPlaySoundAndPlayState(sign)`

### 4.5 数据同步（values 数组）

Server 端通过 `BuffBox.SetBuffData()` 向 Client 端同步数据：

```csharp
// Server 端：写入数据
MyBuffBox.SetBuffData(BuffData.BuffType.MoveSpeedRatio, 0.5f);
MyBuffBox.SetBuffData(BuffData.BuffType.IsInvicable, true);

// 也可使用 values 数组直接同步整数
MyBuffBox.values = new int[] { 100, 200, 300 };
```

- `SetBuffData` 由 Server 端调用，通过 `BuffBoxServer.OnUpdate()` 每 0.1 秒同步一次
- Client 端通过 `MyBuffBox` 读取同步后的数据

---

## 五、常见问题与踩坑记录

### 5.1 PlayBuff 后无效果 / Buff 不生效

**问题现象**：调用 `BuffControl.PlayBuff("{BuffSign}", ...)` 后无任何反应。

**根因分析**：

1. BuffAsset 配置表未注册该 Buff 的 sign
2. SO 资产文件路径与配置表中的 `{id}/{path}` 不匹配
3. BSO 的 `init()` 方法返回了错误类型或 null

**排查顺序**：

1. 检查 `BuffAssetConfig.Has("{BuffSign}")` 是否返回 `true`
2. 检查 SO 文件是否存在于 `Assets/ToBundle/ScriptableObject/Buff/{path}/{id}.asset`
3. 在 `AssetsLoad.GetSOBuffData()` 处断点，确认是否加载成功
4. 检查 BSO 的 `init()` 是否正确创建了 BS 实例

### 5.2 GetSOBuffData 返回 null

**问题现象**：`AssetsLoad.GetSOBuffData(sign)` 返回 `null`，Console 无明显报错。

**根因分析**：

1. `BuffAssetConfig.Get(sign)` 返回 null → 配置表中没有该 sign
2. 配置路径拼接错误 → SO 文件名或目录名与配置不一致
3. SO 资产文件未打入 Bundle → 编辑器下能找到但打包后缺失

**解决方案**：

1. 确认 BuffAsset 配置表中 `id` 列包含该 sign（区分大小写）
2. 用 `AssetDatabase.FindAssets("t:BuffSOBase")` 搜索确认 SO 存在
3. 确认 SO 位于 `Assets/ToBundle/` 目录下（才能被打包）

### 5.3 Buff 创建后立即消失

**问题现象**：Buff 在 `PlayBuff` 后一帧内就被移除。

**根因分析**：

1. BSServer 的 `OnUpdate()` 中计时逻辑有误，timer 初始值为 0
2. `buffBox.isClear` 在初始化过程中被意外设置为 `true`
3. BSO 的 `IsOpenUpdate` 为 `false`，但 Server 端依赖 `OnUpdate()` 做计时

**解决方案**：

1. 检查 timer 初始值，确保从 SO 配置中读取 duration
2. 确认 `Init()` 中不会触发 `RemoveBuff()`
3. 如果 Server 端需要 `OnUpdate()`，BSO 的 `IsOpenUpdate` 必须设为 `true`

### 5.4 Client 端无表现但 Server 逻辑正常

**问题现象**：Server 端 Buff 逻辑正常执行，但客户端看不到特效/动画。

**根因分析**：

1. BS 的 `InitClient()` 中未调用 `RequestClient<>()`
2. BSClient 的 `Init()` 中获取角色引用为 null（角色尚未加载）
3. SyncState 设置为 `OnlyServer`，Client 端不会收到同步

**解决方案**：

1. 确认 BS 类中存在 `InitClient()` 并调用了 `RequestClient<BS{BuffName}Client>()`
2. 在 BSClient.Init() 中做 null 检查再操作角色
3. 调整 SyncState（使用 `Range` / `World` 等支持 Client 同步的模式）

### 5.5 同步范围不正确 / 远处玩家看不到 Buff

**问题现象**：Buff 效果只有附近玩家可见，远处玩家看不到。

**根因分析**：

1. `SyncRangeDistance` / `PCSyncRangeDistance` 设置过小
2. SyncState 用了 `Range` 但 Buff 应该全局可见
3. PC 和移动端使用不同的同步范围字段

**解决方案**：

1. 在 SO Inspector 中调大同步范围值
2. 如果是全局 Buff，将 SyncState 改为 `World`
3. 注意同时配置移动端 (`SyncRangeDistance`) 和 PC 端 (`PCSyncRangeDistance`)

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error，零 Unity Console error
- [ ] BSO / BS / BSServer / BSClient 四个文件均可正常编译
- [ ] 无 `NullReferenceException` 或 `InvalidCastException`

### 6.2 配置

- [ ] BuffAsset 配置表中已注册，sign 与 SO 文件名一致
- [ ] SO 资产文件位于正确路径：`Assets/ToBundle/ScriptableObject/Buff/{BuffCategory}/{BuffSign}.asset`
- [ ] SO Inspector 面板中 SyncState、同步范围等基础字段已正确填写
- [ ] `[CreateAssetMenu]` 路径以 `War/Buff/` 开头

### 6.3 运行时

- [ ] `BuffControl.PlayBuff("{BuffSign}", fireRoleId, lockRoleId)` 调用后 Buff 成功创建
- [ ] Server 端逻辑正常执行（伤害/计时/碰撞等）
- [ ] Client 端表现正常（特效/动画/音效）
- [ ] Buff 到期后正常销毁，无残留引用
- [ ] 多次创建和销毁不会内存泄漏

### 6.4 同步

- [ ] SyncState 配置正确，对应范围内的玩家能收到同步
- [ ] PC 和移动端同步范围分别配置
- [ ] `values` 数组数据正确同步到 Client 端

### 6.5 资源

- [ ] SO 资产文件在 `Assets/ToBundle/` 目录下（可被打包）
- [ ] 涉及的特效/音效资源路径正确
- [ ] 不依赖 Editor-Only 的资源或 API

---

*文档版本：v1.0*
*对应批次：B3*
*创建依据：BuffSOBase/BuffSystemBase 框架层代码分析 + 制作文档编写规范 README.md*
