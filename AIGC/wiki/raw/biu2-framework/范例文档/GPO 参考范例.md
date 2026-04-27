# 重型防御机枪（MachineGun）炮台类 GPO 制作范例文档

> **定位**：本文档以重型防御机枪为模板，详细记录一个「固定炮台类 AI GPO」从配表、架构、服务端/客户端实现、网络同步到表现层的完整制作流程。所有后续炮台类 GPO（如导弹炮台、激光炮台等）均可以本文档为范本。

---

## 目录

1. [概述](#1-概述)  
2. [配表数据解读（GPOM_MachineGun）](#2-配表数据解读)  
3. [整体架构图](#3-整体架构图)  
4. [服务端实现详解](#4-服务端实现详解)  
5. [客户端实现详解](#5-客户端实现详解)  
6. [攻击机制详解](#6-攻击机制详解)  
7. [炮塔旋转同步机制](#7-炮塔旋转同步机制)  
8. [网络协议完整列表](#8-网络协议完整列表)  
9. [客户端表现层实现](#9-客户端表现层实现)  
10. [玩家驾驶与操控模式](#10-玩家驾驶与操控模式)  
11. [新炮台类 GPO 制作 Checklist](#11-新炮台类-gpo-制作-checklist)  
12. [关键设计原则总结](#12-关键设计原则总结)  

---

## 1. 概述

### 1.1 MachineGun 是什么

重型防御机枪（`MachineGun`）是一种「固定式炮台型 AI GPO」，具有以下核心特性：

| 特性 | 说明 |
|---|---|
| **固定炮台** | 放置于地图固定位置，生成时自动贴地（法线对齐） |
| **持续高频连射** | 攻击间隔仅 0.05 秒，多炮管轮换开火 |
| **过热冷却机制** | 持续射击一段时间后强制冷却，防止无限连射 |
| **可被玩家驾驶** | 玩家可以乘坐并通过输入设备控制射击方向和开火 |
| **AI 自主攻击** | 无人驾驶时自动寻找视野内的敌对 GPO 并开火 |
| **随移动平台移动** | 支持放置在会移动的平台上，跟随平台同步位置 |

### 1.2 作为炮台模板的意义

MachineGun 是项目中第一个完整实现以下特性的炮台 GPO：
- **服务端权威攻击判定** + **Rpc 协议同步炮塔旋转**
- **定制 Attack/HeadRota 组件**与**通用 SetToGround/FindInsightTarget 组件**的清晰划分
- **玩家驾驶输入链路**的完整实现
- **客户端表现层分级渲染**（High/Medium/Low 三档特效策略）

---

## 2. 配表数据解读

### 2.1 配表位置

配表类由 csv-gen 工具自动生成，位于：
```
Assets/Scripts/Template/gpo/GPOM_MachineGun.cs
```

数据通过 `GPOM_MachineGunSet.GetGPOMByIdAndMatchMode(id, matchMode)` 获取。

### 2.2 关键字段说明

| 字段名 | 类型 | 值 | 说明 |
|---|---|---|---|
| `Id` | int | `8` | GPO 模板 ID（对应 `GpoTypeSet.Id_MachineGun`） |
| `Sign` | string | `"MachineGun"` | GPO 唯一标识，用于 AssetURL 路径拼接 |
| `Name` | string | `"重型防御机枪"` | 显示名称 |
| `Hp` | int | `8000` | 最大血量 |
| `Atk` | int | `200` | 基础攻击力（每发子弹伤害基数） |
| `AttackIntervalTime` | float | `0.05f` | 每炮管开火间隔（秒），越小越快 |
| `AttackRange` | float | `5f` | 攻击范围半径（ServerAIAttribute 初始化用） |
| `MaxAttackDistance` | float | `100f` | 最大射程，也是 FindInsightTarget 的检测距离 |
| `GpoType` | int | `8` | GPO 类型 ID，对应 `GpoTypeSet.Id_MachineGun` |
| `AssetSign` | string | `"MachineGun"` | Prefab 路径中的资产名 |
| `Quality` | byte | `1` | 品质等级，影响 AI 行为和外观表现 |
| `GpoSoConfig` | string | `""` | SO 配置路径（空 = 使用默认） |

### 2.3 在代码中的使用方式

在 System 的 `OnAwake` 中强转获取：

```csharp
// ServerAIMachineGunSystem.cs
private GPOM_MachineGun useMData;
protected override void OnAwake() {
    useMData = (GPOM_MachineGun)MData;  // MData 来自 S_GPO_Base，框架自动注入
    AddComponents();
}
```

在组件中同样通过 `aiSystem.MData` 获取：

```csharp
// ServerAIMachineGunAttack.cs
private S_AI_Base aiSystem;
private GPOM_MachineGun useMData;
protected override void OnAwake() {
    aiSystem = (S_AI_Base)mySystem;
    useMData = (GPOM_MachineGun)aiSystem.MData;
}
```

---

## 3. 整体架构图

```
ServerGameWorld
  └─ ServerAIManager
       └─ ServerAIWorld.AddAIForGpoMTypeId(GpoTypeSet.Id_MachineGun)
            └─ ServerAIMachineGunSystem  (S_AI_Base → S_GPO_Base → SystemBase)
                 │
                 ├─ [Entity]   AIEntity "MachineGunServer"   (服务端碰撞体/骨骼)
                 ├─ [IGPO]     ServerGPO                     (GPO 身份证)
                 ├─ [INetwork] ServerNetworkSync              (网络通道)
                 │
                 ├─ ── 默认组件（S_AI_Base.AddComponents）──
                 ├─ ServerAIDead                    死亡处理
                 ├─ ServerAIMaster                  主人绑定
                 ├─ ServerAIHateTarget              仇恨目标
                 ├─ ServerAIHurt                    受伤处理
                 ├─ KnockbackGPO                    击退
                 ├─ StrikeFlyGPO                    击飞
                 ├─ ServerGPOAttackProtect           攻击保护
                 ├─ ServerGPOShowEntity              显隐同步
                 ├─ ServerAIPatrolPoint              巡逻点
                 ├─ ServerGPOAbilityEffect           Ability 效果接收
                 ├─ ServerAIQuality                 品质
                 ├─ ServerGPODropItem               掉落道具
                 │
                 └─ ── 定制组件（MachineGun 专属）──
                      ServerAIMovingPlatformTargetMove   随移动平台移动
                      ServerAIAttribute(Atk/HP/Range)    属性初始化
                      ServerAISummonedCreatureSource      召唤物来源记录
                      ServerAIMachineGunAttack  ★         开火逻辑
                      ServerAIMachineGunHeadRota ★        炮塔旋转 + Rpc 同步
                      ServerTurretSetToGround             贴地放置
                      ServerAIFindInsightTarget           视野内寻敌
                      ServerAIPlayAbilityByBehaviourLevel 行为树伤害倍率
                      ServerUnmovableGPOIceSlideMove      冰面处理

ClientGameWorld
  └─ ClientAIManager
       └─ ClientAIWorld（Proto_AI.TargetRpc_AddAI 触发）
            └─ ClientAIMachineGunSystem  (C_AI_Base → C_GPO_Base → SystemBase)
                 │
                 ├─ [Entity]   AIEntity "MachineGun"         (客户端渲染/动画)
                 ├─ [IGPO]     ClientGPO                     (GPO 身份证)
                 ├─ [INetwork] ClientNetworkSync              (网络通道)
                 │
                 ├─ ── 默认组件（C_AI_Base.AddComponents）──
                 ├─ ClientAIRemove                  移除处理（网络注册）
                 ├─ ClientAIQuality                 品质表现
                 ├─ ClientGPODead                   死亡表现
                 ├─ ClientGPOShowEntity             显隐
                 ├─ ClientGPOAbilityEffect          Ability 表现
                 ├─ ClientAIMaster                  主人绑定
                 ├─ ClientAIEffect                  通用特效
                 │
                 └─ ── 定制组件（MachineGun 专属）──
                      ClientAIAttribute                    属性同步
                      ClientAISummonedCreatureSource        召唤物来源
                      ClientAIMachineGunAttack  ★           开火表现 + 玩家输入
                      ClientAIMachineGunHeadRota ★          炮塔旋转表现（Rpc 接收）
                      ClientGPOOtherTeamMaterial            敌我材质区分
                      ClientGPOCameraHideRoleRenderer       摄像机遮挡
                      ClientAIMovingPlatformTargetMove      随移动平台

网络层（Server → Client）
  TargetRpc_AddAI          → 创建 ClientAIMachineGunSystem
  TargetRpc_AddAIDefault   → 初始化血量
  Rpc_SyncMachineGunUpperBodyRota → 炮塔旋转同步（每 0.1 秒）
  Rpc_AddTag / Rpc_RemoveTag    → GamePlayTag 增量同步
  [子弹 Ability 走 SM_Ability.PlayAbility 消息总线，服务端直接触发]
```

---

## 4. 服务端实现详解

### 4.1 System 生命周期

```csharp
// Assets/Scripts/GamePlay/Server/AI/Systems/ServerAIMachineGunSystem.cs
public class ServerAIMachineGunSystem : S_AI_Base {
    private GPOM_MachineGun useMData;

    // 1. OnAwake：加载配表，挂载所有组件
    protected override void OnAwake() {
        useMData = (GPOM_MachineGun)MData;
        AddComponents();
    }

    // 2. AddComponents：先调父类（默认组件），再加定制组件
    protected override void AddComponents() {
        base.AddComponents();  // S_AI_Base 默认 12 个通用组件
        // ... 见下方详细说明
    }

    // 3. OnStart：加载场景 Entity（Prefab）
    protected override void OnStart() {
        base.OnStart();
        // AttributeData.Sign 值为 useMData.Sign = "MachineGun"
        // 路径：AI/Server/MachineGunServer
        CreateEntity(AttributeData.Sign + "Server");
    }

    // 4. OnClear：由基类自动处理，所有 Component 会依次 Clear
    protected override void OnClear() {
        base.OnClear();
    }
}
```

**生命周期时序**：
```
SetAIData() → OnAwake() [AddComponents] → OnStart() [CreateEntity] → 
框架异步等待 Prefab 加载完成 → OnSetEntityObj() 在各 Component 中触发 →
每帧 OnUpdate() → OnClear() [依次销毁 Component]
```

### 4.2 默认组件说明（来自 S_AI_Base）

所有继承 `S_AI_Base` 的 System 都会自动获得以下组件，**无需在子类中重复添加**：

| 组件名 | 职责 |
|---|---|
| `ServerAIDead` | 处理死亡逻辑（触发 OnDead 流程，通知客户端，延迟销毁） |
| `ServerAIMaster` | 绑定召唤主人（MasterGPO），主人死亡时联动销毁 |
| `ServerAIHateTarget` | 维护仇恨列表，决定优先攻击目标 |
| `ServerAIHurt` | 受伤时应用伤害，更新血量，触发受伤动画事件 |
| `KnockbackGPO` | 被击退时同步位移 |
| `StrikeFlyGPO` | 被击飞时同步抛物线运动 |
| `ServerGPOAttackProtect` | 生成后短暂无敌保护期 |
| `ServerGPOShowEntity` | 管理 Entity 显隐，并通过 Rpc 同步到客户端 |
| `ServerAIPatrolPoint` | 记录巡逻点数据，供其他 Move 组件使用 |
| `ServerGPOAbilityEffect` | 接收 Ability 产生的标签/属性效果 |
| `ServerAIQuality` | 根据品质等级调整 AI 参数（伤害、血量倍率等） |
| `ServerGPODropItem` | AI 死亡时根据 `GpoDropId/GpoDropType` 掉落道具 |

### 4.3 定制组件详解

#### 4.3.1 ServerAIAttribute — 属性初始化

```csharp
AddComponent<ServerAIAttribute>(new ServerGPOAttribute.InitData {
    ATK = useMData.Atk,              // 200，每发子弹的基础伤害参数
    AttackRange = useMData.AttackRange,  // 5f
    MaxHp = useMData.Hp,             // 8000
});
```

- 继承自 `ServerGPOAttribute`，负责创建 `AttributeData`（血量、攻击力等运行时数据）
- 如果 AI 已有 `AttributeData`（如从存档恢复），则复用，不会重复创建
- 监听 `SE_GPO.Event_SetAIConfig` → 根据 AI 等级配置命中率

#### 4.3.2 ServerAIMovingPlatformTargetMove — 随移动平台

- 注册到全局平台列表（`SM_SceneGPO.Event_AddMovingPlatformList`）
- 当炮台站在移动平台上时，跟随平台的 `PlatformMovement` 事件同步位置偏移
- 玩家驾驶状态下暂停平台跟随逻辑

#### 4.3.3 ServerAISummonedCreatureSource — 召唤物来源记录

- 记录该炮台是由哪个玩家 GPO 召唤的（影响击杀归属和经验分配）
- 接收 `TargetRpc_AISource` 协议下发来源信息

#### 4.3.4 ServerAIMachineGunAttack ★ — 核心攻击逻辑（定制）

详见 [第 6 章：攻击机制详解](#6-攻击机制详解)。

#### 4.3.5 ServerAIMachineGunHeadRota ★ — 炮塔旋转（定制）

详见 [第 7 章：炮塔旋转同步机制](#7-炮塔旋转同步机制)。

#### 4.3.6 ServerTurretSetToGround — 落地贴地（通用炮台组件）

```
职责：炮台生成时，向下射线检测地面，将 Entity 贴地并对齐地面法线。
```

- `OnSetEntityObj` 触发时立即执行 `CheckGrounded()`（射线检测）
- 支持平滑插值移动到目标地面位置（0.3 秒过渡，避免突变）
- 每秒同步一次位置到客户端（防止漂移）
- 监听 `SE_GPO.Event_IsIceSlideMove`：冰面时跳过贴地检测

**骨骼节点依赖**：
- `GPOData.PartEnum.Head` → `upperBody`（炮塔基座）
- `GPOData.PartEnum.FootRotaCheck` → `footRotaTransform`（地面法线检测点）

#### 4.3.7 ServerAIFindInsightTarget — 视野内寻敌

```csharp
AddComponent<ServerAIFindInsightTarget>(new ServerAIFindInsightTarget.InitData {
    CheckDistance = useMData.MaxAttackDistance,  // 100f 球形检测半径
    LayerMask = LayerData.ServerLayerMask | LayerData.DefaultLayerMask,
    IgnoreTeamId = TeamId,           // 忽略同队
    IgnoreCollierTrigger = false,    // 不忽略 Trigger 碰撞体
});
```

- 每 **0.5 秒**执行一次球形重叠检测
- 检测到目标变化时 `Dispatcher(new SE_AI.Event_SetInsightTarget { TargetGPO = ... })`
- `ServerAIMachineGunAttack` 和 `ServerAIMachineGunHeadRota` 都订阅此事件

#### 4.3.8 ServerAIPlayAbilityByBehaviourLevel — 行为树伤害倍率

- 监听 `SE_GPO.Event_SetBehaviourLevel` → 查表 `AiBehaviourTreeLevelSet` 获取 `damagePercent`
- 响应 `SE_AI.Event_GetDamagePercent` 事件，供攻击组件查询最终伤害倍率

#### 4.3.9 ServerUnmovableGPOIceSlideMove — 冰面滑动处理

- 炮台为不可移动 GPO，放置在冰面时触发特殊逻辑（如被冰技能推动）
- 通用组件，炮台类 GPO 均可挂载

---

## 5. 客户端实现详解

### 5.1 System 生命周期

客户端 System 的创建由服务端主动下发的 `TargetRpc_AddAI` 协议触发：

```
服务端 TargetRpc_AddAI 到达客户端
  → ClientAIWorld_Switch.case GpoTypeSet.Id_MachineGun
    → manager.AddSystem<ClientAIMachineGunSystem>()
      → SetAIData(mData, protoDoc, soData, gpoId, teamId, skinSign, startPoint, startRota)
```

```csharp
// Assets/Scripts/GamePlay/Client/AI/Systems/ClientAIMachineGunSystem.cs
public class ClientAIMachineGunSystem : C_AI_Base {

    // 1. OnAwake：挂载所有组件
    protected override void OnAwake() {
        base.OnAwake();   // 含 AddNetwork()
        AddComponents();
    }

    // 2. OnStart：设置初始位置，加载客户端 Prefab
    protected override void OnStart() {
        base.OnStart();
        iEntity.SetPoint(startPoint);
        // AttributeData.SkinSign 来自 TargetRpc_AddAI.aiSkinSign（即 "MachineGun"）
        // 路径：AI/Client/MachineGun
        CreateEntity(AttributeData.SkinSign);
    }

    // 3. OnLoadEntityEnd：Prefab 加载完成后的自定义初始化（可选）
    protected override void OnLoadEntityEnd(IEntity iEnter) {
        if (iEnter == null) {
            DebugLogger.LogError("[Error] MachineGun 加载 Entity 失败:" + AttributeData.SkinSign);
            return;
        }
        // 可在此做如初始位置对齐、特殊组件初始化等
    }

    protected override void AddComponents() {
        base.AddComponents();  // C_AI_Base 默认 7 个通用组件
        AddComponent<ClientAIAttribute>();
        AddComponent<ClientAISummonedCreatureSource>();
        AddComponent<ClientAIMachineGunAttack>();        // ★ 定制
        AddComponent<ClientAIMachineGunHeadRota>();      // ★ 定制
        AddComponent<ClientGPOOtherTeamMaterial>();
        AddComponent<ClientGPOCameraHideRoleRenderer>();
        AddComponent<ClientAIMovingPlatformTargetMove>();
    }
}
```

### 5.2 默认组件说明（来自 C_AI_Base）

| 组件名 | 职责 |
|---|---|
| `ClientAIRemove` | 接收 `TargetRpc_RemoveAI` 协议，安全销毁客户端 System |
| `ClientAIQuality` | 根据品质等级切换皮肤/材质 |
| `ClientGPODead` | 接收死亡协议，播放死亡动画和特效 |
| `ClientGPOShowEntity` | 接收显隐协议，控制 Entity 的 SetActive |
| `ClientGPOAbilityEffect` | 接收 Ability 产生的表现（如 Buff 光效） |
| `ClientAIMaster` | 接收 `TargetRpc_AIMaster` 协议，绑定主人 GPO |
| `ClientAIEffect` | 通用特效管理（受击闪光等） |

### 5.3 定制组件详解

#### 5.3.1 ClientAIAttribute — 属性同步

- 接收 `TargetRpc_AddAIDefault { maxHp, nowHp }` 协议 → 初始化本地 `AttributeData`
- 维护客户端血量显示（血条 UI 等）

#### 5.3.2 ClientGPOOtherTeamMaterial — 敌我材质

- 根据 `iGPO.GetTeamID()` 与本地玩家队伍关系，切换敌/友材质颜色

#### 5.3.3 ClientGPOCameraHideRoleRenderer — 相机遮挡

- 当本地玩家进入炮台内部时隐藏炮台外壳 Renderer，避免穿模

#### 5.3.4 ClientAIMachineGunAttack ★ — 开火表现（定制）

详见 [第 6 章](#6-攻击机制详解) 和 [第 9 章](#9-客户端表现层实现)。

#### 5.3.5 ClientAIMachineGunHeadRota ★ — 旋转表现（定制）

详见 [第 7 章](#7-炮塔旋转同步机制)。

---

## 6. 攻击机制详解

### 6.1 完整攻击流程

```
[服务端每帧 Update]
  │
  ├─ ModeData.PlayGameState == RoundStart ? 否 → 跳过
  │
  ├─ UpdateFireOverHotCD()   检查冷却是否结束
  ├─ CountFireOverHotTimer() 累计过热时间
  └─ FireInterval()
        │
        ├─ isCoolingDown || targetGPO == null → 跳过
        ├─ fireIntervalTime > 0 → 递减计时器
        └─ fireIntervalTime <= 0
              │
              ├─ SetFireBoxRotation()   炮管 LookAt 目标
              ├─ fireIntervalTime = useMData.AttackIntervalTime (0.05s)
              ├─ fireIndex = (fireIndex + 1) % fireTran.Count  轮换炮管
              └─ FireBullet(firePoint, entPoint)
                    ├─ entPoint = GetRandomPoint(firePoint, entPoint)  扩散
                    ├─ Dispatcher(SE_AI.Event_MasterAIFire)            通知主人
                    └─ MsgRegister.Dispatcher(SM_Ability.PlayAbility)  发射子弹
```

### 6.2 目标选取

目标由 `ServerAIFindInsightTarget` 组件每 0.5 秒更新一次，通过内部事件通知攻击组件：

```csharp
// 攻击组件订阅目标事件
protected override void OnAwake() {
    mySystem.Register<SE_AI.Event_SetInsightTarget>(OnSetInsightTarget);
}

private void OnSetInsightTarget(ISystemMsg body, SE_AI.Event_SetInsightTarget ent) {
    targetGPO = ent.TargetGPO;
    fireIntervalTime = 0.5f;  // 新目标出现时增加 0.5s 预判延迟（模拟反应时间）
}
```

### 6.3 多炮管轮换

炮管发射点从 Entity 的骨骼节点获取：

```csharp
protected override void OnSetEntityObj(IEntity iEntity) {
    // GPOData.PartEnum.AttactPoint1 对应 Prefab 上的多个发射点 Transform
    fireTran = iEntity.GetBodyTranList(GPOData.PartEnum.AttactPoint1);
}
```

每次开火后 `fireIndex` 递增，超出数组长度时归零，实现多炮管轮换效果。

### 6.4 子弹 Ability 触发

子弹通过消息总线直接在服务端触发，无需客户端命令：

```csharp
private void FireBullet(Vector3 firePoint, Vector3 entPoint) {
    // 1. 扩散计算（加入随机偏移）
    entPoint = GetRandomPoint(firePoint, entPoint);

    // 2. 通知主人记录开火事件
    Dispatcher(new SE_AI.Event_MasterAIFire());

    // 3. 通过消息总线触发 Ability 系统创建子弹
    MsgRegister.Dispatcher(new SM_Ability.PlayAbility {
        FireGPO = iGPO,
        MData = AbilityM_Bullet.CreateForID(AbilityM_Bullet.ID_BulletMachineGun),
        InData = new AbilityIn_Bullet {
            In_StartPoint = firePoint,
            In_TargetPoint = entPoint,
            In_Speed = gunData.BulletSpeed,
            In_MoveDistance = gunData.FireDistance,
            In_BulletAttnMap = gunData.BulletAttnMaps,
            In_WeaponItemId = gunData.ItemId
        }
    });
}
```

> **注意**：子弹的武器数据（`BulletSpeed`、`FireDistance`、`FireOverHotTime` 等）来自 `WeaponData.GunData`，通过 `ItemSet.Id_MachineGun` 查询，而非 GPOM 表。这是机枪武器参数和炮台属性参数分离存储的设计。

### 6.5 扩散计算

```csharp
private Vector3 GetRandomPoint(Vector3 firePoint, Vector3 endPoint) {
    var shootDirection = (endPoint - firePoint).normalized;
    var distance = Vector3.Distance(firePoint, endPoint);
    var forwardPoint = firePoint + shootDirection * Mathf.Max(100, distance);
    // 在目标点附近随机偏移（圆形分布）
    var randomDistance = Random.Range(0f, gunData.FireRange * 0.1f);
    var angle = Random.Range(0f, 360f);
    var x = randomDistance * Mathf.Cos(angle * Mathf.Deg2Rad);
    var y = randomDistance * Mathf.Sin(angle * Mathf.Deg2Rad);
    return forwardPoint + new Vector3(x, y, x);
}
```

扩散半径由 `gunData.FireRange` 控制，与 GPOM 表解耦。

### 6.6 过热冷却状态机

```
        射击中（isFireDown=true）
             │
    countFireOverHotTimer 累加
             │
    >= fireOverHotTimer（来自 gunData）
             │
             ▼
        进入冷却（isCoolingDown=true）
     countFireOverHotTimer 归零
     fireOverHotCDTimer = gunData.FireOverHotCDTime
             │
    fireOverHotCDTimer 递减
             │
    <= 0
             │
             ▼
        冷却结束（isCoolingDown=false）
        可以继续射击
```

- **过热触发**：连续射击超过 `fireOverHotTimer` 秒
- **冷却时间**：`fireOverHotCDTimer` 秒（来自 `gunData.FireOverHotCDTime`）
- **空闲降温**：不射击时 `countFireOverHotTimer` 自动递减

---

## 7. 炮塔旋转同步机制

### 7.1 服务端旋转计算（ServerAIMachineGunHeadRota）

```
骨骼节点依赖：
  GPOData.PartEnum.Head      → upperBody  （炮台底座水平旋转轴）
  GPOData.PartEnum.RightHand → gunBody    （炮管仰角旋转轴）
```

**每帧执行**（有目标时）：

```
1. 水平旋转 upperBody
   target = targetGPO.GetPoint()
   lookDirection = (target - upperBody.position).normalized
   newRotation = Slerp(current, LookRotation(lookDirection), deltaTime * 5f)
   upperBody.rotation = Euler(currentX, newRotation.y, 0)  // 只更新 Y 轴

2. 仰角调整 gunBody
   directionToTarget = targetPoint - gunBody.position
   elevationAngle = Atan2(dirY, targetDistance) → Clamp(0, 45°)
   gunBody.localEulerAngles = Euler(-elevationAngle, 0, 0)
```

**每 0.1 秒**通过 Rpc 同步：

```csharp
private void SyncUpperBodyRota() {
    if (syncTime > 0) { syncTime -= Time.deltaTime; return; }
    syncTime = 0.1f;
    // eulerAngles.x = 270 + gunBody.localEulerAngles.x（将局部仰角转为网络传输格式）
    // eulerAngles.y = upperBody.eulerAngles.y（世界坐标水平角）
    playerUpperBodyRota = new Vector3(270 + gunBody.localEulerAngles.x, upperBody.eulerAngles.y, 0);
    Rpc(new Proto_AI.Rpc_SyncMachineGunUpperBodyRota() {
        eulerAngles = playerUpperBodyRota
    });
}
```

### 7.2 网络协议

```csharp
// 6_Proto_AI.cs — FuncID = 27
public struct Rpc_SyncMachineGunUpperBodyRota : IRpc {
    public const byte FuncID = 27;
    public const string ID = "Proto_AI.Rpc_SyncMachineGunUpperBodyRota";
    public Vector3 eulerAngles;   // x=仰角(270偏移), y=水平角, z=0
    public int GetChannel() => NetworkData.Channels.Reliable;
    // Serialize/UnSerialize 通过 ByteBuffer 读写 Vector3
}
```

> 使用 `IRpc`（广播给所有客户端），确保所有观战者和附近玩家都能看到炮塔旋转。

### 7.3 客户端旋转表现（ClientAIMachineGunHeadRota）

```csharp
// 在 OnSetNetwork 时注册网络协议回调
protected override void OnSetNetwork() {
    AddProtoCallBack(Proto_AI.Rpc_SyncMachineGunUpperBodyRota.ID, OnSyncMachineGunUpperBodyRota);
}

// 收到协议时仅存储目标角度
private void OnSyncMachineGunUpperBodyRota(INetwork network, IProto_Doc docData) {
    var rpcData = (Proto_AI.Rpc_SyncMachineGunUpperBodyRota)docData;
    rpcTargetRota = rpcData.eulerAngles;
}

// 每帧平滑插值（rotationSpeed = 10f）
private void UpdateRpcMachineGunUpperBodyRota() {
    // 水平旋转
    rootBody.rotation = Quaternion.Slerp(
        rootBody.rotation,
        Quaternion.Euler(0, rpcTargetRota.y, 0),
        Time.deltaTime * rotationSpeed);

    // 仰角旋转（局部坐标）
    gunBody.localRotation = Quaternion.Slerp(
        gunBody.localRotation,
        Quaternion.Euler(rpcTargetRota.x, 0, 0),
        Time.deltaTime * rotationSpeed);
}
```

```
骨骼节点依赖：
  GPOData.PartEnum.RootBody  → rootBody  （对应服务端 upperBody）
  GPOData.PartEnum.RightHand → gunBody   （仰角，与服务端一致）
```

**关键点**：客户端旋转完全跟随服务端，不做任何本地预测，确保与权威状态一致。Slerp 平滑插值避免了 0.1 秒网络间隔带来的突变。

---

## 8. 网络协议完整列表

### 8.1 AI 生命周期协议（Proto_AI）

| 协议名 | 类型 | 方向 | 触发时机 | 关键字段 |
|---|---|---|---|---|
| `TargetRpc_AddAI` | ITargetRpc | Server→指定Client | 新玩家连接时 / AI 首次生成 | gpoId, teamId, gpoMId(8), aiSkinSign, startPoint, startRota, protoDoc |
| `TargetRpc_AddAIDefault` | ITargetRpc | Server→指定Client | 随 TargetRpc_AddAI 打包发送 | maxHp(8000), nowHp |
| `TargetRpc_RemoveAI` | ITargetRpc | Server→指定Client | AI 被销毁时 | gpoId |

### 8.2 MachineGun 专用协议（Proto_AI）

| 协议名 | FuncID | 类型 | 方向 | 触发频率 | 关键字段 |
|---|---|---|---|---|---|
| `Rpc_SyncMachineGunUpperBodyRota` | 27 | IRpc | Server→AllClients | 每 0.1 秒 | eulerAngles(Vector3): x=仰角(270偏移), y=水平角 |

### 8.3 GPO 通用协议（Proto_GPO）

| 协议名 | 触发时机 | 说明 |
|---|---|---|
| `TargetRpc_SyncGPOID` | AI 创建时 | 下发 GpoID、TeamID、GpoType 到指定客户端 |
| `Rpc_AddTag` | Tag 首次激活 | 增量同步 GamePlayTag 状态 |
| `Rpc_RemoveTag` | Tag 引用归零 | 增量同步 Tag 移除 |
| `TargetRpc_ActiveTagList` | 新玩家连接 | 全量同步当前所有激活 Tag |

### 8.4 Ability 子弹（消息总线，非网络协议）

子弹 Ability 在**服务端**通过消息总线触发，客户端 Ability 表现由 AbilitySystem 自行处理（不经过 AI 的网络通道）：

```
Server: MsgRegister.Dispatcher(SM_Ability.PlayAbility { ... })
  → ServerAbilityManager 创建 S_Ability_BulletSystem
    → 子弹移动碰撞判定（服务端权威）
    → 命中时 Rpc 通知客户端播放命中特效
  
Client: ServerAbilityManager 对应的 ClientAbilityManager 接收 TargetRpc_AddAbility
  → 创建 C_Ability_BulletSystem
    → 播放子弹飞行特效
```

---

## 9. 客户端表现层实现

### 9.1 动画系统

- 使用 **Playable 动画系统**（`SausagePlayable`），通过 AnimSign 驱动，不依赖 Animator Controller 状态机
- 配置来自 `AIAnimConfig.Get(monsterSign)`（`EntityAnimConfig` ScriptableObject）
- 动画 Sign：`AnimConfig_MachineGun.Play_Fire`

```csharp
// Playable 初始化（在 OnSetEntityObj 之后）
private void InitPlayableGraph() {
    entity = (EntityBase)iEntity;
    var animator = entity.GetComponentInChildren<Animator>(true);
    playable = new SausagePlayable();
    playable.Init(entity.transform, animator, config, $"Client_{monsterSign}");
}

// 触发开火动画（由 CE_Weapon.GetFireBox 事件触发）
private void PlayAnimSign(string animSign) {
    playable?.PlayAnimSign(animSign);
}
```

- 动画播放后设置 `checkIsFireTime = AttackIntervalTime * 2`，超时后自动调用 `playable.StopSign` 停止动画

### 9.2 特效系统（分级渲染）

特效对象均通过 `PrefabPoolManager` 管理（**对象池**），避免频繁 GC：

| 特效资产 | 触发点骨骼节点 | 生命周期 |
|---|---|---|
| `fx_machinegun_fire`（炮口火焰）| `GPOData.PartEnum.AttactPoint1` | 0.2 秒 |
| `fx_machinegun_cartridge_case`（弹壳） | `GPOData.PartEnum.LeftHand` | 0.4~0.5 秒 |

**三档画质策略**：

```csharp
switch (QualityData.GetQualityType()) {
    case QualityData.QualityType.Low:
        return;  // 低画质：不播放特效，节省性能

    case QualityData.QualityType.High:
        // 高画质：每次开火都播放炮口焰 + 弹壳
        LoadAndInitMachineGunEffect(fireEffectUrl, Fire, fireIndex, 0.2f);
        LoadAndInitMachineGunEffect(unloadEffectUrl, Unload, fireIndex, 0.5f);
        break;

    case QualityData.QualityType.Medium:
        // 中画质：每5次开火循环中只在前N次播放（N=炮管数量）
        playEffectCount++;
        if (playEffectCount <= fireTran.Count) {
            // 播放特效
        } else if (playEffectCount >= fireTran.Count * 5) {
            playEffectCount = 0;  // 重置计数
        }
        break;
}
```

特效 GameObject 放置到 `StageData.GameWorldLayerType.Ability` Layer，确保正确渲染排序。

### 9.3 音效系统

| 音效资产 | 触发条件 | 说明 |
|---|---|---|
| `WP_SA_Machinegun_Fire`（1P） | 驾驶者为本地玩家时 | 第一人称射击音效 |
| `WP_SA_Machinegun_Unload`（1P） | 驾驶者为本地玩家时 | 弹壳抛出音效 |
| `WP_SA_Machinegun_Fire_3P`（3P） | 其他玩家观察到时 | 第三人称射击音效（距离衰减） |
| `WP_G_MiniGun_Ovht` | 过热冷却开始时 | 过热音效（仅本地玩家驾驶时播放） |

音效由 `CE_Weapon.Event_BulletSetFireGPO` 事件触发（每次有子弹实际发出时），有 0.05 秒冷却防止重复播放。

### 9.4 过热 UI 通知

客户端过热状态通过内部事件总线同步给 UI 组件：

```csharp
// 冷却中：通知 UI 显示冷却进度
aiBase.Dispatcher(new CE_Weapon.OutFireOverHotTimer {
    NowOverHotTimer = fireOverHotCDTimer,
    MaxOverHotTime = gunData.FireOverHotCDTime,
    IsCooling = true
});

// 正常射击中：通知 UI 显示蓄热进度
aiBase.Dispatcher(new CE_Weapon.OutFireOverHotTimer {
    NowOverHotTimer = countFireOverHotTimer,
    MaxOverHotTime = fireOverHotTimer,
    IsCooling = false
});
```

### 9.5 摄像机震动

本地玩家驾驶时，每次开火触发摄像机震动：

```csharp
private void ShakeCamera() {
    if (driveGPO != null && driveGPO.IsLocalGPO()) {
        MsgRegister.Dispatcher(new CM_Camera.ShakeCamera() {
            Duration = 0.2f,
            Magnitude = 0.1f,
            DampingSharpness = 1.6f,
            NoiseFrequency = new Vector3(10, 10, 0),
            AffectRotation = true,
            MaxRotationAngle = 10,
        });
    }
}
```

---

## 10. 玩家驾驶与操控模式

### 10.1 驾驶状态激活

```csharp
// ClientAIMachineGunAttack 内
private void OnDriveGPOCallBack(ISystemMsg body, CE_GPO.Event_DriveGPO ent) {
    driveGPO = (ClientGPO)ent.PlayerDriveGPO;
    // 只有本地玩家驾驶时，才激活客户端输入处理
    enabledDriveMove = (driveGPO != null) && driveGPO.IsLocalGPO();
}
```

- **AI 自主模式**（无人驾驶）：`enabledDriveMove = false`，服务端 `ServerAIFindInsightTarget` 自动寻敌攻击
- **玩家驾驶模式**（本地玩家驾驶）：`enabledDriveMove = true`，客户端接受输入并发送给服务端

### 10.2 开火输入链路

```
玩家按下开火键
  │
  CE_GPO.Event_OnInputDeviceFire { IsDown = true }
  │
  ClientAIMachineGunAttack.OnDeviceStartFireCallBack
  │  isFireDown = true
  │
  每帧 Update（sendTargetPointTime 节流 0.3s）
  │
  CM_Camera.GetCameraCenterObjPoint（获取瞄准点）
  │  CallBack = GetCameraTargetPoint
  │
  GetCameraTargetPoint(targetPoint, isHit)
  │
  mySystem.Dispatcher(CE_GPO.Event_OnDeviceFire { Points = [targetPoint] })
  │
  [由网络层发送 Cmd 给服务端，服务端攻击组件接收并开火]
```

### 10.3 瞄准辅助

- 使用 `CM_Camera.GetCameraCenterObjPoint` 获取摄像机中心射线的碰撞点
- 参数 `FarDistance = useMData.MaxAttackDistance`（100 米限制）
- `IgnoreTeamId = iGPO.GetTeamID()`（忽略同队目标）
- `CheckForwardPoint = currentFireTrans.position`（从当前炮管位置出发检测）

---

## 11. 新炮台类 GPO 制作 Checklist

基于 MachineGun 模板，制作一个新炮台类 GPO 的完整步骤：

### 📋 配表层

- [ ] **GPOM 表新增行**：填写 `Id`（新唯一 ID）、`Sign`、`Name`、`Hp`、`Atk`、`AttackIntervalTime`、`AttackRange`、`MaxAttackDistance`、`GpoType`、`AssetSign`
- [ ] **GpoTypeSet 常量**：在 `GpoTypeSet.cs` 中添加 `public const int Id_XXX = <新ID>;`
- [ ] **csv-gen 生成**：重新运行 csv-gen 工具生成对应的 `GPOM_XXX.cs` 配表类

### 🔌 路由注册层

- [ ] **ServerAIWorld_Switch**：在 `AddAIForGpoMTypeId` 的 switch 中添加：
  ```csharp
  case GpoTypeSet.Id_XXX:
      system = manager.AddSystem<ServerAIXXXSystem>(callBack);
      break;
  ```
- [ ] **ClientAIWorld_Switch**：同样在客户端路由中添加对应分支

### 🖥️ 服务端 System 层

- [ ] **新建 `ServerAIXXXSystem.cs`**，继承 `S_AI_Base`
- [ ] **OnAwake**：强转 `MData` 为具体配表类型
- [ ] **AddComponents**：先调 `base.AddComponents()`，再添加定制组件
  - 确认是否需要 `ServerTurretSetToGround`（炮台贴地，推荐所有固定炮台使用）
  - 确认是否需要 `ServerAIMovingPlatformTargetMove`（支持移动平台）
  - 确认是否需要 `ServerAIFindInsightTarget`（自动寻敌，需配置检测距离）
  - 确认是否需要 `ServerAIPlayAbilityByBehaviourLevel`（行为树伤害倍率）
  - **添加定制攻击组件**（继承 `ServerNetworkComponentBase`，实现攻击逻辑）
  - **添加定制旋转组件**（如需旋转同步，参考 `ServerAIMachineGunHeadRota`）
- [ ] **OnStart**：调用 `CreateEntity(AttributeData.Sign + "Server")`

### 💻 客户端 System 层

- [ ] **新建 `ClientAIXXXSystem.cs`**，继承 `C_AI_Base`
- [ ] **AddComponents**：先调 `base.AddComponents()`，再添加定制组件
  - 确认是否需要 `ClientAIAttribute`（血量同步）
  - 确认是否需要 `ClientGPOOtherTeamMaterial`（敌我材质）
  - 确认是否需要 `ClientGPOCameraHideRoleRenderer`（相机遮挡）
  - 确认是否需要 `ClientAIMovingPlatformTargetMove`（随平台移动）
  - **添加定制攻击表现组件**（特效、音效、动画）
  - **添加定制旋转表现组件**（接收 Rpc，平滑 Slerp）
- [ ] **OnStart**：调用 `CreateEntity(AttributeData.SkinSign)`

### 📡 网络协议层

- [ ] **是否需要新增旋转同步协议**？若旋转方式与 MachineGun 不同，在 `6_Proto_AI.cs` 新增 `Rpc_SyncXXXRota`（分配新 FuncID），并在 `ReadRpcBuffer` 的 switch 中注册
- [ ] **是否需要新增特殊状态同步协议**？（如冷却状态、特殊攻击模式等）

### 🔫 Ability 子弹层

- [ ] **是否复用 `ID_BulletMachineGun`**？或新增子弹 Ability 配表 `AbilityM_Bullet.ID_BulletXXX`
- [ ] **`AbilityIn_Bullet` 参数**：Speed、MoveDistance、BulletAttnMaps 是否与机枪相同？
- [ ] **WeaponData 配表**：如使用不同武器数据，在 `ItemSet` 中新增对应 ID

### 🎨 资产层

- [ ] **Prefab 资产**：
  - 服务端：`AI/Server/XXXServer.prefab`（含碰撞体、骨骼节点）
  - 客户端：`AI/Client/XXX.prefab`（含 Renderer、Animator、特效挂点）
- [ ] **特效资产**：`Effects/fx_xxx_fire.prefab`（PrefabPool 管理）
- [ ] **音效资产**：注册 1P/3P 音效 Key（AssetURL.GetAudio1P/3P）
- [ ] **动画配置**：`AIAnimConfig` 中注册新炮台的 `EntityAnimConfig`

### ✅ 联调验证

- [ ] Editor 模式下：服务端创建炮台 → Entity 正确贴地 → 自动寻敌开火
- [ ] 旋转同步：客户端炮塔旋转是否与服务端一致（< 0.1 秒延迟）
- [ ] ��弹表现：客户端是否正确播放子弹飞行特效
- [ ] 驾驶模式：本地玩家驾驶时输入→开火链路是否正常
- [ ] 过热机制：服务端和客户端过热状态是否同步
- [ ] 死亡流程：炮台死亡 → 客户端死亡动画 → 服务端销毁 → 客户端移除
- [ ] Tag 同步：`TargetRpc_ActiveTagList` 新玩家加入时是否收到正确 Tag 列表
- [ ] 多端模式：纯客户端 / 纯服务端 / Editor 双端三种模式均正常运行

---

## 12. 关键设计原则总结

### 12.1 服务端权威

所有**攻击判定**（子弹命中、伤害计算）和**目标选取**（视野检测）均在服务端执行。客户端只负责表现，不做任何伤害判定。这确保了多人游戏的公平性，防止作弊。

### 12.2 组件解耦

组件之间**不持有彼此引用**，通过 System 内部事件总线（`mySystem.Register/Dispatcher`）通信：

```
ServerAIFindInsightTarget → SE_AI.Event_SetInsightTarget → ServerAIMachineGunAttack
ServerAIFindInsightTarget → SE_AI.Event_SetInsightTarget → ServerAIMachineGunHeadRota
```

这样新增/移除组件不会影响其他组件，扩展新炮台时只需替换定制组件即可。

### 12.3 表现与逻辑彻底分离

- 服务端：只做逻辑（旋转角度计算、开火时机、过热判断）
- 客户端：只做表现（Slerp 平滑、特效播放、音效、动画）
- 二者通过**网络协议**桥接，互不直接调用

### 12.4 默认组件 vs 定制组件

| 类别 | 来源 | 修改成本 |
|---|---|---|
| **默认组件**（S_AI_Base/C_AI_Base） | 所有 AI 共享 | 修改影响所有 AI，需谨慎 |
| **定制组件**（MachineGun 专属） | 仅本炮台使用 | 自由修改，不影响其他 AI |

新炮台制作时优先复用默认组件，只有炮台特有的逻辑才需要定制新组件。

### 12.5 分级渲染策略

移动端性能差异巨大，特效采用 High/Medium/Low 三档策略：
- **High**：全特效
- **Medium**：降低播放频率（每 5 次只播放前几次）
- **Low**：关闭所有特效，保证最低帧率设备可运行

### 12.6 对象池管理

特效 Prefab 通过 `PrefabPoolManager` 统一管理，避免每次开火都触发 Instantiate/Destroy 导致的 GC 峰值。高频开火（0.05 秒/次）场景下，对象池对性能至关重要。

### 12.7 生命周期严格管理

所有 `Register` 必须在 `OnClear` 中配对 `Unregister`；所有 `AddUpdate` 必须配对 `RemoveUpdate`；所有对象引用在 `OnClear` 中置 null，防止野引用和内存泄漏。

---

*文档版本：v1.0 | 创建日期：2026-03-10 | 基于 MachineGun 代码实现提炼*
