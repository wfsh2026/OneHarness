# RoleLogic 子系统打散方案

> **文档版本**：v2.1（Phase 8 试点已执行→回退→暂停）
> **创建时间**：2026-04-11
> **最后更新**：2026-04-14
> **负责 Agent**：[DL] 开发负责人
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **前置条件**：BattleRoleLogic 本体重构 Phase 1-5 已全部完成 ✅，Phase 6-7 已全部完成 ✅

---

## 参考文档

| 类别 | 文件 | 路径 |
|------|------|------|
| 本体重构方案 | BattleRoleLogic 重构方案 | [[BattleRoleLogic重构方案]] |
| 进度跟踪 | 会话状态 | `aigc/harness/session-state/BattleRoleLogic重构/active.md` |
| 本体进度计划 | 分阶段任务清单 | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` |

---

## 1. 目标与范围

将 `RoleLogicClient`（~2,553 行）和 `RoleLogicServer`（~10,720 行）的逻辑打散，融入组件体系。

| 子系统 | partial 文件数 | 总行数 | 子循环 | 外部引用文件 |
|--------|--------------|-------|--------|------------|
| RoleLogicClient | 18 | ~2,531 | 0 | 455 |
| RoleLogicServer | 35 | ~10,719 | 1 (RoleCheat) | 499 |
| **合计** | **53** | **~13,250** | **1** | **954** |

---

## 2. 核心架构（当前状态）

### 2.1 继承关系

```
IBattleSystem（接口：AddUpdate/RemoveUpdate/Register/Unregister/Dispatcher）
  ├── BattleMonoSystemBase (MonoBehaviour + IBattleSystem)  ← 原 BattleSystemBase，已改名
  │     ├── BattleRoleLogic (主角色逻辑系统，122 行，24 个 Component) ✅
  │     └── BattleRole (角色表现系统，338 行，40+ Component) ✅
  └── BattleLogicSystemBase (纯 C# + IBattleSystem)  ← 新建
        ├── RoleLogicClient (客户端子系统，自管组件)
        └── RoleLogicServer (服务端子系统，自管组件) ✅ Phase 7 新增
```

### 2.2 组件体系

```
BattleComponent（纯 C# 组件基类：OnAwake/OnClear/OnStart + Register/Unregister/Dispatcher）
  ├── BattleRoleLogicComponent (BattleRoleLogic 专属)
  │     └── [24 个已完成的 Component]
  ├── RoleLogicClientComponent (RoleLogicClient 专属)
  │     └── RoleLogicClientBladeBallComponent ✅
  └── RoleLogicServerComponent (RoleLogicServer 专属) ✅ Phase 7 新增
        └── [10 个已完成的 Component]
```

### 2.3 双事件总线

BattleRoleLogic 和 RoleLogicClient 各有独立的事件系统：

| 事件总线 | 宿主基类 | 组件基类 | 说明 |
|---------|---------|---------|------|
| BattleRoleLogic 总线 | BattleMonoSystemBase | BattleRoleLogicComponent | 主系统，24 个 Component |
| RoleLogicClient 总线 | BattleLogicSystemBase | RoleLogicClientComponent | 客户端独立组件生命周期 |

**关键设计**：Client 组件注册在 RoleLogicClient 的事件总线上，Facade 使用 `Dispatcher(...)` （继承自 BattleLogicSystemBase）而非 `roleLogic.Dispatcher(...)`。

### 2.4 Feature 系统（与 Component 并行）

BattleRoleLogic 上存在两套并行的扩展机制：

| 维度 | `AbsRoleLogicFeature` | `BattleRoleLogicComponent` |
|------|----------------------|--------------------------|
| 基类定义 | `Base/IRoleLogicFeature.cs` | `BattleComponent.cs` → `BattleRoleLogicComponent.cs` |
| 生命周期 | `Init(BattleRoleLogic)` / `Clear()` | `Awake(IBattleSystem)` / `Start()` / `Clear()` |
| Update | ❌ 无内置，需手动 `roleLogic.AddUpdate` | ✅ 内置 `AddUpdate`/`RemoveUpdate` |
| 事件系统 | ❌ 无 | ✅ `Register`/`Unregister`/`Dispatcher` |
| 容器 | `RoleLogicFeatures`（Dictionary\<Type\>） | IBattleSystem 组件列表 |
| 查询 | `GetFeature<T>()` | `GetComponent<T>()` |
| 当前数量 | ~35+（Client 13 + Server 22+） | 24 个 |

**关键事实**：所有 Feature 通过 `roleLogic.AddFeature<T>()` 注册在 BattleRoleLogic 上（非 Server/Client 上），即使 AddFeature 调用位于 `RoleLogicServer.Init()` 或 `RoleLogicClient.Init()` 中。

**打散策略**：Feature 类本身 **不需要修改基类**，打散时只需将 AddFeature 调用位置从 Server/Client.Init() 移到 BattleRoleLogic 的初始化方法。**Feature → Component 统一**作为 Phase 8 重点推进。

### 2.5 RoleLogicServer 组件体系（Phase 7 新增）

```csharp
RoleLogicServer.AwakeInit()   → AddComponents()       // 注册 10 个 RoleLogicServerComponent
RoleLogicServer.OnUpdate()    → DriveComponents(dt)   // 驱动组件帧更新
RoleLogicServer.Clear()       → ClearAllComponents()  // 清理组件
```

**RoleLogicServerComponent 基类**：

```csharp
public abstract class RoleLogicServerComponent : BattleComponent {
    protected RoleLogicServer serverLogic { get; private set; }
    protected BattleRoleLogic roleLogic => serverLogic?.roleLogic;
    protected BattleWorld gameWorld => roleLogic?.gameWorld;
    protected StartGame startGame => roleLogic?.MyStartGame;
    public override void Awake(IBattleSystem system) {
        serverLogic = system as RoleLogicServer;
        base.Awake(system);
    }
    protected override void OnClear() { serverLogic = null; }
}
```

**10 个已完成的 Server 组件**：

| # | 组件 | 行数 | 说明 |
|---|------|------|------|
| 1 | RoleKillInfo | 627 | 击杀信息统计 |
| 2 | RoleCarSkin | 57 | 载具皮肤映射 |
| 3 | RoleDinoSkin | 182 | 恐龙坐骑皮肤 |
| 4 | RoleSkinChangeSkin | 95 | 时装皮肤同步 |
| 5 | AutoTestRoleData | 114 | 自动测试数据覆盖 |
| 6 | RoleLogicCarShift | 112 | 载具换挡/跳跃表情 |
| 7 | BattleRoleLogicStaminaServer | 159 | 体力条服务端（条件注册） |
| 8 | RoleLogicLimitedRedPackets | 149 | 限时红包/限量道具 |
| 9 | WarFlagData | 286 | 战旗数据统计 |
| 10 | RoleSkillServer | 215 | 技能服务端逻辑 |

**保留为 RequestLoop 的子循环**：

| 子循环 | 行数 | 原因 |
|--------|------|------|
| RoleCheat | 2,007 | 独立反作弊子系统，`#if SERVER_LOGIC` 包裹，有自己的组件系统（ICheatType + 20+ 子模块），直接注册 `gameWorld.AddFixedUpdate` |

### 2.6 Client 组件生命周期

```csharp
RoleLogicClient.Init()       → AddClientComponents()     // 注册组件
RoleLogicClient.OnUpdate()   → DriveComponents(dt)       // 驱动组件帧更新
RoleLogicClient.Clear()      → ClearAllComponents()      // 清理组件（在其他清理之前）
```

### 2.7 Client 组件迁移模式

```csharp
// Step 1 — 事件仍定义在 BattleRoleLogicEvents.cs
public struct CmdBladeBallModeLogic { }

// Step 2 — Facade 在 RoleLogicClient partial
public partial class RoleLogicClient {
    public void BladeBallModeLogic()
        => Dispatcher(new BattleRoleLogicEvents.CmdBladeBallModeLogic());
}

// Step 3 — Component 继承 RoleLogicClientComponent
public class RoleLogicClientBladeBallComponent : RoleLogicClientComponent {
    // clientLogic = RoleLogicClient, roleLogic = BattleRoleLogic
    protected override void OnAwake() {
        Register<BattleRoleLogicEvents.CmdBladeBallModeLogic>(OnBladeBallModeLogic);
    }
}
```

---

## 3. Phase 6: RoleLogicClient 组件化

### 3.1 已完成进度

| 维度 | 改造前 | 当前 |
|------|--------|------|
| 组件系统 | 无 | ✅ BattleLogicSystemBase 独立组件系统 |
| 文件组织 | 散落各处 | ✅ 集中在 `RoleLogicClient/` 子目录，20 个文件 |
| 主文件行数 | 1,992 行 | **158 行**（纯生命周期方法） |
| Partial 文件数 | 7 | **19** (含基类+Facade+Fields+Movement) |
| Component | 0 | **1 个**（BladeBall，260 行） |
| `roleLogic` 可见性 | private | **internal** |

> ⚠️ **字段迁移已废弃**：曾尝试将 Client 字段迁移到 BattleRoleLogic partial（RoleLogic_ClientFields.cs），
> 后因决策15（保留 RoleLogicClient）而回滚。字段保留在 RoleLogicClient 上，不再迁移。

### 3.2 RoleLogicClient 当前文件清单

```
Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/
  RoleLogicClient.cs                    158 行  ← 主文件（纯生命周期：AwakeInit/Init/Clear/OnUpdate）
  RoleLogicClientComponent.cs            21 行  ← ✅ 组件基类
  RoleLogicClient_Fields.cs             205 行  ← ✅ 全部字段 + 属性 + 转发代理（M-6.4 新建）
  RoleLogicClient_Movement.cs            57 行  ← ✅ 吸附移动 + 体力条 + MoveRatioStruct（M-6.4 新建）
  RoleLogicClient_BladeBallMode.cs       30 行  ← ✅ Facade（已组件化 → RoleLogicClientBladeBallComponent）
  RoleLogicClient_ModeCheck.cs          124 行  ← ✅ 模式/区域检测（M-6.2 新建）
  RoleLogicClient_RoleDisplay.cs        163 行  ← ✅ 角色显示管理（M-6.2 新建）
  RoleLogicClient_Misc.cs              161 行  ← ✅ 杂项方法（M-6.2 新建）
  RoleLogicClient_Skill.cs              66 行  ← ✅ 技能方法组（M-6.2 新建）
  RoleLogicClient_NetCheck.cs           46 行  ← ✅ 网络检测（M-6.2 新建）
  RoleLogicClient_MoveSpeed.cs          420 行  ← 移速计算（核心热路径）
  RoleLogicClient_IdCardSkin.cs         240 行  ← 身份证皮肤
  RoleLogicClient_DuoJin.cs             222 行  ← 夺金模式
  RoleLogicClient_Push.cs              216 行  ← 推人物理（通过 RoleLogicPhysicsComponent 事件驱动）
  RoleLogicClient_Football.cs          100 行  ← 足球模式标记
  RoleLogicClient_Item.cs               86 行  ← 物品相关
  RoleLogicClient_DuoBaoSuit.cs         66 行  ← 多宝套装
  RoleLogicClient_Vehicle.cs            57 行  ← 载具相关
  RoleLogicClient_BoxingFly.cs          50 行  ← 拳击飞行
  RoleLogicClient_WolfParty.cs          43 行  ← 狼人派对
```

> 合计 20 个文件 ~2,531 行（主文件 158 + partial 2,352 + 基类 21）

### 3.3 组件化评估结论

经分析，仅 BladeBall 适合组件化（已完成），其余 partial 不适合：

| Partial | 行数 | 结论 | 原因 |
|---------|------|------|------|
| BladeBall | 276 | ✅ 已完成 | 独立状态机 + OnUpdate + 3个API |
| DuoJin | 222 | ❌ SKIP | 15+ public API，33+ 外部调用，纯数据 CRUD |
| MoveSpeed | ~400 | ❌ SKIP | 核心帧计算，深度耦合 |
| IdCardSkin | ~229 | ❌ SKIP | 无 update 逻辑，响应式配置查询 |
| Push | ~205 | ⚠️ 可选 | 有状态机但深度耦合 |
| Football | ~83 | ⚠️ 可选 | 有生命周期但太小 |
| WolfParty | 43 | ❌ SKIP | 死代码，仅 2 字段 |

#### 组件化适配性标准

| 标准 | 适合组件化 | 不适合组件化 |
|------|-----------|------------|
| OnUpdate 驱动逻辑 | ✅ BladeBall, Push | ❌ DuoJin |
| 自包含状态机 | ✅ Push (timer+raycast) | ❌ WolfParty (2 fields) |
| 少量外部 API | ✅ BladeBall (3 APIs) | ❌ DuoJin (15+ APIs) |
| 完整 init/update/clear 生命周期 | ✅ Football | ❌ IdCardSkin |

### 3.4 RoleLogicClient 后续计划

| 优先级 | 任务 | 说明 | 状态 |
|--------|------|------|------|
| ~~P1~~ | ~~进一步拆分主文件（739→~400行）~~ | ~~M-6.2~~ | ✅ 完成（实际338行→158行） |
| ~~P1.5~~ | ~~Push / Football 组件化评估~~ | ~~M-6.3~~ | ✅ 完成（均不适合，保留 partial） |
| ~~P1.6~~ | ~~代码整理 + 字段提取~~ | ~~M-6.4~~ | ✅ 完成（Fields+Movement 提取） |
| P2 | Phase 6 Client 完成 | 所有 Client partial 已最终定型 | ✅ |

> **核心原则（决策15）**：RoleLogicClient 保留为生命周期壳 + 字段容器。
> Partial 逻辑按适配性标准评估，仅独立状态机 + OnUpdate 驱动的模块才组件化。
> 其余 partial 保持现状或进一步拆分为更小的 partial。
> 
> **M-6.3 评估结论**：
> - Push（216行）：❌ 已通过 RoleLogicPhysicsComponent 事件驱动，重复提取无意义
> - Football（100行）：❌ 纯生命周期辅助（Init/Clear/UpdateNowPoint），无独立 update，太小

---

## 4. Phase 7: RoleLogicServer 打散 — ✅ 已完成

> **核心策略（决策15适用）**：保留 RoleLogicServer 为壳 + 字段容器。
> 对标 Client 的成功路径：S-1 字段提取 → S-2 方法群组提取 → S-3 代码整理。
> 子循环 → Component 作为独立里程碑（M-7.1）。

### 4.1 完成结果

| 维度 | 改造前 | 改造后 |
|------|--------|--------|
| 主文件行数 | **5,131 行** | **329 行**（▼ 93.6%）|
| 子循环 (IRoleLogicServer) | 11 个 | **1 个**（RoleCheat 保留） |
| RoleLogicServerComponent | 0 | **10 个** |
| Partial 文件 | 20 个 | **35 个**（含新增 15 个） |
| 架构 | 单继承 IRoleLogic | BattleLogicSystemBase + IRoleLogic（对称 Client）|

### 4.2 里程碑完成记录

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M-7.1 | 子循环→Component：10/11 转换 + RoleCheat 保留 + RoleLogicServerComponent 基类 | ✅ 完成 |
| M-7.2 | 字段提取：~680 行 → RoleLogicServer_Fields.cs | ✅ 完成 |
| M-7.3 | 主文件瘦身：5,131→329 行，新增 15 个 partial | ✅ 完成 |
| M-7.4 | 代码整理：doc 注释 + 文件目录头 + 独立文件提取 | ✅ 完成 |

### 4.3 关键决策

| 决策 | 内容 |
|------|------|
| ADR-16 | 服务端 Component 注册位置：从 BattleRoleLogic.AddComponents() 迁移到 RoleLogicServer.AwakeInit()，通过自身的 AddComponent\<T\>() 注册 |
| ADR-17 | RoleLogicServer 改为继承 BattleLogicSystemBase，与 RoleLogicClient 对称。新增 RoleLogicServerComponent 基类 |
| RoleCheat 保留 | 独立反作弊子系统（2,007 行），`#if SERVER_LOGIC`，有自己的组件系统（ICheatType），保持 RequestLoop |

### 4.4 RoleLogicServer 当前文件清单

```
Assets/Script/GamePlay/Server/Modules/Role/
  RoleLogicServer.cs                    329 行  ← 主文件（生命周期壳）
  RoleLogicServer_Fields.cs             680 行  ← 全部字段与属性声明
  RoleLogicServer_Dead.cs               884 行  ← 死亡流程
  RoleLogicServer_DataInfo.cs           887 行  ← 数据统计信息
  RoleLogicServer_DuoJin.cs             587 行  ← 夺金模式
  RoleLogicServer_DownHp.cs             520 行  ← 扣血计算
  RoleLogicServer_HideSeek.cs           421 行  ← 躲猫猫模式
  RoleLogicServer_Fly.cs                361 行  ← 飞行/跳伞
  RoleLogicServer_Misc.cs               320 行  ← 杂项 + InitAfkFeature + SetFirstLogin
  RoleLogicServer_Resurrection.cs       328 行  ← 复活机制
  RoleLogicServer_HeroCard.cs           294 行  ← 英雄身份卡
  RoleLogicServer_LockCamera.cs         291 行  ← 观战管理
  RoleLogicServer_BornPoint.cs          274 行  ← 出生点
  RoleLogicServer_UltraFight.cs         270 行  ← 奥特曼派对
  RoleLogicServer_AIEvent.cs            229 行  ← AI 事件
  RoleLogicServer_CheatCheck.cs         232 行  ← 外挂检测 + AceTick
  RoleLogicServer_Damage.cs             201 行  ← 伤害系统
  RoleLogicServer_Statistics.cs         197 行  ← 移动统计
  RoleLogicServer_Skill.cs              197 行  ← 技能服务端
  RoleLogicServer_Uprear.cs             189 行  ← 击飞/击退
  RoleLogicServer_Weak.cs               189 行  ← 虚弱状态
  RoleLogicServer_BadExpression.cs      164 行  ← 不良表达
  RoleLogicServer_Item.cs               153 行  ← 物品系统
  RoleLogicServer_DefusalMode.cs       1893 行  ← 拆弹模式
  RoleLogicServer_BladeBallMode.cs      132 行  ← 刀刃球模式
  RoleLogicServer_TeammateBehavior.cs   119 行  ← 队友行为
  RoleLogicServer_TeamMode.cs           115 行  ← 团队模式
  RoleLogicServer_Lobby.cs              286 行  ← 社交大厅
  RoleLogicServer_RecoverHp.cs          129 行  ← 自动回血
  RoleLogicServer_Network.cs             54 行  ← 网络同步
  RoleLogicServer_Knockout.cs            54 行  ← 淘汰模式
  RoleLogicServer_Property.cs            29 行  ← 属性管理
  RoleLogicServer_LookRole.cs            16 行  ← SetLookRole
  RoleLogicServer_Manager.cs             16 行  ← 管理器引用
  RoleLogicServer_FightClose.cs         120 行  ← 近战关闭
  RoleLogicServer_ItemSkin.cs             9 行  ← 物品皮肤数据
  RoleLogicServer_Pve.cs                177 行  ← PVE 模式

  # 独立文件（非 partial）
  RoleBulletInfo.cs                      ← 子弹统计数据类
  IRoleLogicServer.cs                    ← 服务端子循环接口（仅 RoleCheat 使用）
  RoleLogicServerComponent.cs            ← 服务端组件基类（位于 BattleRoleLogic/）
```

---

## 5. Phase 8: Feature → Component 统一（⏸ 暂停 — 已试点后用户回退）

> **目标**：将 `IRoleLogicFeature` / `AbsRoleLogicFeature` 系统合并到 `BattleRoleLogicComponent` 系统，消除架构冗余。
> **当前状态**：M-8.1/M-8.2 试点已执行并验证编译通过，但用户回退所有类体转换（ADR-20），方案暂停待重新评估。

### 5.1 背景分析

当前 BattleRoleLogic 上存在两套并行的扩展机制：

| 维度 | Feature 系统 | Component 系统 |
|------|-------------|---------------|
| 基类 | `AbsRoleLogicFeature` | `BattleRoleLogicComponent` |
| 生命周期 | `Init(BattleRoleLogic)` / `Clear()` | `Awake(IBattleSystem)` / `Start()` / `Clear()` |
| Update | ❌ 无内置，需手动 `roleLogic.AddUpdate` | ✅ 内置 `AddUpdate`/`RemoveUpdate` |
| 事件系统 | ❌ 无 | ✅ `Register`/`Unregister`/`Dispatcher` |
| 容器 | `RoleLogicFeatures`（Dictionary\<Type\>） | IBattleSystem 组件列表 |
| 查询 | `GetFeature<T>()` | `GetComponent<T>()` |
| 数量 | **33 个**（Server 20 + Client 13） | **35 个** |

**问题**：Feature 能力弱于 Component（无事件、无内置 Update），但两者生命周期高度重叠。维护两套系统增加认知负担。

**先例**：`BattleRoleLogicStaminaServer` 已从 Feature 成功迁移为 Component。

### 5.2 Feature 基类定义

```csharp
// Assets/Script/GamePlay/Base/IRoleLogicFeature.cs
public interface IRoleLogicFeature {
    void Init(BattleRoleLogic role);
    void Clear();
}

public abstract class AbsRoleLogicFeature : IRoleLogicFeature {
    protected BattleRoleLogic roleLogic;
    public void Init(BattleRoleLogic role) { roleLogic = role; OnInit(); }
    public void Clear() { OnRemove(); roleLogic = null; }
    protected virtual void OnInit() { }
    protected virtual void OnRemove() { }
}

public class RoleLogicFeatures : IDisposable {
    private Dictionary<Type, IRoleLogicFeature> features;
    public bool AddFeature<T>() where T : IRoleLogicFeature, new() { ... }
    public bool RemoveFeature<T>() where T : IRoleLogicFeature, new() { ... }
    public T GetFeature<T>() where T : IRoleLogicFeature { ... }
}
```

### 5.3 完整 Feature 清单

#### Server Feature（在 RoleLogicServer.Init() 中注册）

| # | Feature 类 | 条件 | 功能说明 |
|---|-----------|------|---------|
| 1 | ServerRoleLogicPveDataManager | PveRogueMode | PVE肉鸽数据管理（经验/奖励/关卡进度） |
| 2 | RoleTotemServer | PveRogueMode | 图腾系统（肉鸽天赋树） |
| 3 | RoleLogicWeakFeatureManager | !PveRogueMode | 倒地/虚弱状态管理（倒地计时+自动淘汰） |
| 4 | ServerTreasureManager | !PveRogueMode | 宝物拾取管理（宝箱位置+拾取记录） |
| 5 | RoleLogicGoldDashServer | GoldDashMode | 淘金冲刺模式逻辑（逃脱/开箱/金币） |
| 6 | RoleLogicWeaponHitRatioFeatureManager | GoldDashMode | 武器命中率统计（淘金模式专用埋点） |
| 7 | SausageServerRolePet | !GoldDashMode | 宠物系统（跟随/技能/目标选择） |
| 8 | RoleLogicResurrectionServer | 无条件 | 复活系统（复活点/援助复活/复活成功流程） |
| 9 | RoleLogicPowerFeatureManager | 无条件 | 角色属性管理（攻击/防御/速度等数值增减） |
| 10 | RoleLogicUprearFeatureManager | 无条件 | 扶起功能（扶起成功+回血+mood反馈） |
| 11 | ServerRoleLogicStateSyncFeatureManager | 无条件 | 状态同步管理（RoleSyncState→客户端同步） |
| 12 | ServerRolePowerSkillManager | 无条件 | 能量技能管理（超级格斗模式蓄能/释放） |
| 13 | RoleLogicStatisticsDataManager | 无条件 | 统计数据管理（击杀/伤害/存活等埋点数据） |
| 14 | RoleLogicBeAttackedFeatureManager | 无条件 | 受击数据记录（伤害来源/时间线/上报） |
| 15 | ServerRoleLogicAdsorbFeatureManager | 无条件 | 吸附功能（吸附/被吸附/吸附队列管理） |
| 16 | RoleLogicTrajectoryFeatureManager | 无条件 | 轨迹记录（位置采样+移动轨迹上报） |
| 17 | HandInHandServer | 无条件 | 手牵手功能（组队/跟随/同步动作） |
| 18 | RoleLogicPingManager | 无条件 | 网络延迟监测（Ping计算+高延迟标记） |
| 19 | RoleLogicDisconnectManager | !StartReport && !AI && !SocialLobby | 断线管理（断线检测+自动落地+超时淘汰） |
| 20 | ServerRoleKillScoreCalculator | ClassicMode | 击杀积分计算（经典模式专用排名积分） |

#### Client Feature（在 RoleLogicClient.Init() 中注册）

| # | Feature 类 | 条件 | 说明 |
|---|-----------|------|------|
| 1 | ClientRoleLogicStateSyncFeatureManager | 无条件 | 状态同步 |
| 2 | ClientRoleLogicRoleNetCheck | 无条件 | 网络检查 |
| 3 | RoleStateManager | 无条件 | 角色状态 |
| 4 | ClientRolePowerSkillManager | 无条件 | 力量技能 |
| 5 | HandInHandClient | 无条件 | 手牵手 |
| 6 | ClientRoleLogicAdsorbFeature | 无条件 | 吸附 |
| 7 | Clownskill2AreaRoleLogicClient | 无条件 | 小丑技能 |
| 8 | GunBayonetRoleLogicClient | 无条件 | 枪刺 |
| 9 | ClientRoleLogicPveDataManager | PveRogueMode | PVE 数据 |
| 10 | ClientTreasureManager | !PveRogueMode | 宝物 |
| 11 | ClientRoleLogicAFKFeature | LocalRole + TouchScreen | AFK 检测 |
| 12 | SausageClientRolePet | 无条件 | 宠物 |
| 13 | BattleRoleLogicStaminaClient | LocalRole + PowerBar | 体力条 |

### 5.4 外部引用影响评估（含试点实测数据）

Feature 的外部引用主要通过 `GetFeature<T>()` 访问：

| API | 使用量 | 影响说明 |
|-----|--------|---------|
| `roleLogic.AddFeature<T>()` | ~36 文件 | 注册点，改为 `AddComponent<T>()` |
| `roleLogic.GetFeature<T>()` | 大量（25KB+ 输出） | 查询点，改为 `GetComponent<T>()` |
| `roleLogic.RemoveFeature<T>()` | ~17 文件 | 移除点，改为 `RemoveComponent<T>()` |

> ⚠️ `GetFeature<T>()` 在外部使用广泛，是 Phase 8 最大工作量来源。
> 但替换模式统一（`GetFeature<T>()` → `GetComponent<T>()`），可脚本化批量处理。

#### M-8.1/M-8.2 试点实测外部引用数（编译验证）

| Feature | 外部 GetFeature 引用 | 备注 |
|---------|---------------------|------|
| RoleLogicResurrectionServer | 7 | explore 漏报为 0 |
| RoleLogicUprearFeatureManager | 1 | explore 漏报为 0 |
| ServerRolePowerSkillManager | 9 | explore 漏报为 0 |
| ServerRoleLogicAdsorbFeatureManager | 7 | explore 漏报为 0 |
| HandInHandServer | 22 (12内+10外) | explore 漏报为 0 |
| StatisticsDataManager / Trajectory / Power / StateSync / BeAttacked / Ping | 0 | 与 explore 结果一致 |

> **结论**：自动化引用计数不可靠，每次转换后必须编译验证。

### 5.5 迁移策略

**每个 Feature 的转换步骤（3 步）**：

1. **改基类**：`AbsRoleLogicFeature` → `BattleRoleLogicComponent`
   - `OnInit()` → `OnAwake()`
   - `OnRemove()` → `OnClear()`
   - `roleLogic` 已由基类提供（字段名相同）

2. **改注册方式**：`roleLogic.AddFeature<T>()` → `roleLogic.AddComponent<T>()`
   - 条件性 Feature 保持条件判断

3. **改查询方式**：`roleLogic.GetFeature<T>()` → `roleLogic.GetComponent<T>()`
   - 可脚本化批量替换

**分批策略**（降低风险）：

| 批次 | Feature 数 | 选择标准 | 外部引用预估 |
|------|-----------|---------|-------------|
| F-1 试点 | 2-3 个 | 无条件 + 外部引用少 | ~10 文件 |
| F-2 无条件批 | ~10 个 | 无条件注册的 Feature | ~50 文件 |
| F-3 条件批 | ~10 个 | 有条件注册的 Feature | ~30 文件 |
| F-4 收尾 | 剩余 | Client Feature | ~20 文件 |
| F-5 废弃接口 | 1 个 | 删除 `IRoleLogicFeature` / `RoleLogicFeatures` | ~5 文件 |

### 5.6 里程碑规划

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M-8.1 | Feature → Component 试点（3 个低风险 Feature） | ✅→🔄 已验证通过，用户回退 |
| M-8.2 | 无条件 Server Feature 批量转换（8 个） | ✅→🔄 已验证通过，用户回退 |
| M-8.3 | 条件性 Server Feature 转换 | ⬜ 暂停 |
| M-8.4 | Client Feature 转换 | ⬜ 暂停 |
| M-8.5 | 废弃 IRoleLogicFeature + RoleLogicFeatures 接口 | ⬜ 暂停 |

### 5.7 试点经验总结（M-8.1/M-8.2 回退后沉淀）

#### 已验证可行的技术点
- **3 步转换模式**有效：基类替换 → 生命周期映射 → 注册方式切换
- `roleLogic` 字段名两套基类完全兼容，无需改名
- `AddUpdate/RemoveUpdate` 在两套基类中签名一致

#### 需要桥接方法的 API
- `BattleMonoSystemBase.AddComponent<T>()` 是 `protected`，外部注册需在 BattleRoleLogic 上添加 `public new` 桥接
- `BattleMonoSystemBase.GetBattleComponent<T>()` 是 `protected`，外部查询需桥接
- 桥接方法已验证编译通过，但用户认为方案不够优雅（ADR-20）

#### 发现的问题
- **Bug#14**：explore agent 的 GetFeature 引用计数不可靠（漏报 Resurrection=7, Uprear=1, PowerSkill=9, Adsorb=7, HandInHand=22）→ **编译验证是唯一可信手段**
- **Bug#15**：`ServerRolePowerSkillManager` 缺少 `OnRemove()`，导致 Update 代理泄漏（原代码既有问题，未修复）
- **Bug**：`ServerRoleLogicStateSyncFeatureManager` 同样缺少 `OnRemove()`，Update 代理泄漏
- 部分 Feature 存在死代码 `private BattleWorld gameWorld` 字段（被基类属性遮蔽）

#### 用户关注点（待后续解决）
- 用户倾向引入 `InitData` 模式（类似 `ServerAIBehaviour.InitData : IComponentInitData`）用于组件间通信
- `IComponentInitData` 在当前代码库中不存在，需要新设计
- 当前 `GetBattleComponent<T>().Method()` 直接调用模式被认为耦合过重

---

## 6. Phase 9-10: 远期规划

### 6.1 Phase 9: 外部引用简化

在 BattleRoleLogic 上添加快捷属性，缩短访问链路：

**Top 5 高频访问**：

| 当前路径 | 频次 | 快捷属性 |
|---------|------|---------|
| `roleLogic.roleLogicClient.RoleClient` | 1,369 | `roleLogic.RoleClient` |
| `roleLogic.roleLogicServer.MyRoleCheat` | 320 | `roleLogic.ServerCheat` |
| `roleLogicClient.SetSkillIdByIndex` | 95 | — |
| `roleLogic.roleLogicServer.MyWarFlagData` | 89 | `roleLogic.WarFlag` |
| `roleLogic.roleLogicServer.roleLogicGoldDashServer` | 74 | `roleLogic.GoldDashServer` |

> 难度：🟢 低（纯增量，不破坏现有代码）

### 6.2 Phase 10: Server Partial 组件化（可选）

将 Server partial 文件中的独立模式模块提取为 RoleLogicServerComponent：

**强候选（20 个 partial）**：
DefusalMode(1893行), DataInfo(887), DuoJin(587), HideSeek(421), Fly(361),
Resurrection(328), LockCamera(291), BornPoint(274), UltraFight(270), AIEvent(229),
Lobby(286), Statistics(197), Uprear(189), Weak(189), BadExpression(164),
BladeBallMode(132), RecoverHp(129), TeammateBehavior(119), TeamMode(115), Knockout(54)

> 难度：🔴 高（需要 Facade 模式 + 事件系统，类似 BattleRoleLogic Phase 4 工作量）
> 当前不紧迫：Phase 7 已将 Server 主文件从 5,131→329 行，结构已清晰。

---

## 7. 风险与缓解

| 风险 | 严重度 | 缓解措施 |
|------|--------|---------|
| ~~Server 881 文件外部引用批量替换~~ | ~~🔴 高~~ | ✅ Phase 7 已完成，无需批量替换 |
| ~~`#if SERVER_LOGIC` 条件编译~~ | ~~🟡 中~~ | ✅ Phase 7 保留条件编译块 |
| ~~Server 主文件 4,462 行拆分复杂~~ | ~~🟡 中~~ | ✅ Phase 7 已从 5,131→329 行 |
| Feature→Component GetFeature 替换量大 | 🟡 中 | 脚本化批量替换，分批编译验证 |
| 条件性 Feature 注册逻辑复杂 | 🟡 中 | 保持原有条件判断，仅改注册 API |
| BattleRoleLogic 组件数膨胀（35+29=64） | 🟢 低 | Feature 本来就挂在 BattleRoleLogic 上，总量不变 |
| Facade 转发性能开销 | 🟢 低 | 热路径保留直调，仅低频走事件 |

---

## 8. 里程碑总览

| 里程碑 | 内容 | 文件改动估算 | 状态 |
|--------|------|------------|------|
| **Phase 6 — Client** | | | |
| M-6.0 | Client 架构基建（BattleLogicSystemBase + 文件整理） | ~15 文件 | ✅ 完成 |
| M-6.1 | Client BladeBall 组件化 | ~4 文件 | ✅ 完成 |
| ~~M-6.1a~~ | ~~Client 字段迁移到 BattleRoleLogic~~ | ~~3 文件~~ | ❌ 已废弃（决策15） |
| M-6.2 | Client 主文件瘦身（863→338行，新建5个partial） | 6 文件 | ✅ 完成 |
| M-6.3 | Push / Football 组件化评估（均不适合） | 0 文件 | ✅ 完成 |
| M-6.4 | 代码整理 + 字段/方法提取（338→158行） | 2 新文件 | ✅ 完成 |
| **Phase 7 — Server** | | | |
| M-7.1 | Server 子循环→Component（10/11 转换 + RoleCheat 保留） | ~22 文件 | ✅ 完成 |
| M-7.2 | Server 字段提取（~680行 → _Fields.cs） | 2 文件 | ✅ 完成 |
| M-7.3 | Server 主文件瘦身（5,131→329行，15个新partial） | ~15 文件 | ✅ 完成 |
| M-7.4 | Server 代码整理（doc注释 + 文件目录头 + 独立文件提取） | 3 文件 | ✅ 完成 |
| **Phase 8 — Feature 统一** | | | |
| M-8.1 | Feature→Component 试点（2-3 个低风险 Feature） | ~10 文件 | ⬜ |
| M-8.2 | 无条件 Server Feature 批量转换 | ~50 文件 | ⬜ |
| M-8.3 | 条件性 Server Feature 转换 | ~30 文件 | ⬜ |
| M-8.4 | Client Feature 转换 | ~20 文件 | ⬜ |
| M-8.5 | 废弃 IRoleLogicFeature + RoleLogicFeatures 接口 | ~5 文件 | ⬜ |
| **Phase 9 — 外部引用简化** | | | |
| M-9.1 | BattleRoleLogic 快捷属性（Top 5 高频路径） | ~5 文件 | ⬜ |
| **Phase 10 — Server Partial 组件化（可选）** | | | |
| M-10.1 | 模式相关 Partial → RoleLogicServerComponent | ~40 文件 | ⬜ |

---

## 附录：关键文件路径

| 文件 | 路径 | 说明 |
|------|------|------|
| BattleLogicSystemBase | `Host/Modules/BattleLogicSystemBase.cs` | 纯 C# IBattleSystem |
| BattleMonoSystemBase | `Host/Modules/BattleMonoSystemBase.cs` | MonoBehaviour IBattleSystem |
| IRoleLogicFeature | `Base/IRoleLogicFeature.cs` | Feature 基类 + 容器（Phase 8 废弃目标） |
| RoleLogicClientComponent | `Client/Modules/Role/RoleLogicClient/RoleLogicClientComponent.cs` | Client 组件基类 |
| RoleLogicServerComponent | `Host/Modules/Role/BattleRoleLogic/RoleLogicServerComponent.cs` | Server 组件基类（Phase 7 新增） |
| RoleLogicClientBladeBallComponent | `Host/Modules/Role/BattleRoleLogic/Component/RoleLogicClientBladeBallComponent.cs` | 已完成的 Client 组件 |
| RoleLogicClient 主文件 | `Client/Modules/Role/RoleLogicClient/RoleLogicClient.cs` | 158 行 |
| RoleLogicServer 主文件 | `Server/Modules/Role/RoleLogicServer.cs` | 329 行（Phase 7 从 5,131→329） |
| RoleBulletInfo | `Server/Modules/Role/RoleBulletInfo.cs` | 子弹统计数据（Phase 7 提取） |
| IRoleLogicServer | `Server/Modules/Role/IRoleLogicServer.cs` | 子循环接口（仅 RoleCheat 使用） |
