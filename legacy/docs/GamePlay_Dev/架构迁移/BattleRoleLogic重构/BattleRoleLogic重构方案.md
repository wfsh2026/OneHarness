# BattleRoleLogic.cs 组件化重构方案

> **文档版本**：v3.1（补充 Phase 6-7 完成记录，更新继承关系和文件结构）
> **创建时间**：2026-04-01
> **最后更新**：2026-04-14
> **负责 Agent**：[DL] 开发负责人
> **Agent 定位**：[[Dev_Lead]]（已熟读）

---

## 参考文档

| 类别 | 文件 | 路径 |
|------|------|------|
| 范例（已完成的同类重构）| BattleRole 重构方案 | [[BattleRole重构方案]] |
| 进度跟踪 | 会话状态 | `aigc/harness/session-state/BattleRoleLogic重构/active.md` |
| Client/Server 打散 | 子系统打散方案 | [[RoleLogic子系统打散方案]] |
| 规则 | 开发核心规则 | [[GamePlay_Dev/core-rules]] |
| 规则 | 安全规则 | [[safety-rules]] |

---

## 1. 背景与目标

### 1.1 现状（Phase 1-5 已全部完成 ✅）

| 维度 | 改造前 | 当前 |
|------|--------|------|
| `BattleRoleLogic.cs` 主文件 | 3,503 行 | **122 行**（▼ 96.5%）|
| BattleRoleLogic Component | 0 | **24 个完整实现** |
| Partial 文件 | 18 个（原始实现）| 全部改为 Facade / 骨架 |
| 事件系统 | 空 | `BattleRoleLogicEvents.cs` 200+ 事件 |
| 文件目录 | 散落在 Role/ 根目录 | 集中在 `BattleRoleLogic/` 子目录 |

### 1.2 目标（✅ 已达成）

- ✅ **主文件** `BattleRoleLogic.cs` → **122 行**（超额完成 ~400 行目标）
- ✅ **Partial 文件全部 Facade 化**：仅保留 `Fields / Init / Clear / TimeEvent` 四个骨架 partial
- ✅ **24 个 Component 完整实现**，职责单一
- ✅ **外部接口零破坏**：所有公开方法保留 Facade
- ✅ **与 BattleRole 架构完全对称**：同一套 `BattleMonoSystemBase / BattleComponent`

---

### 1.3 阶段完成记录

| 阶段 | 内容 | 主文件行数 |
|------|------|-----------|
| Phase 1 | 基础设施（改继承链 + BattleRoleLogicComponent + BattleRoleLogicEvents） | 3,515 |
| Phase 2 | 骨架 Partial 拆分（Fields/Init/Clear/TimeEvent） | 2,095 |
| Phase 3 | 已废弃（空壳不计进度） | — |
| Phase 4A | 7 个 Partial → Component 完整迁移 | ~1,200 |
| Phase 4B | 大型 Partial 迁移（States/TeammateBehavior） | ~700 |
| Phase 4C | 主文件 12 个子模块提取 | 339 |
| Phase 4D | 13 个 Partial 事件化（Facade 完成） | **122** |
| Phase 5 | 枚举提取 + 死代码清理 + BattleSystemBase→BattleMonoSystemBase 改名 + 目录重组 | **122** |
| Phase 6 | Client 打散 — BattleLogicSystemBase 新建 + RoleLogicClient 继承迁移 + BladeBall Component | **122** |
| Phase 7 | Server 打散 — RoleLogicServer 继承迁移 + 10 个 RoleLogicServerComponent + 字段/方法提取 | **122** |
| Phase 8 | Feature→Component 统一（试点→回退→⏸ 暂停）| **122** |

---

## 2. 核心架构（已达成，对标 BattleRole）

| 维度 | BattleRole（参照标准）| BattleRoleLogic（✅ 已达成）|
|------|----------------------|---------------------------|
| **主文件行数** | **338 行** | **122 行** ✅ |
| **Component 数** | **40+ 个** | **24 个完整实现** ✅ |
| **Partial 文件** | 全部 Dispatcher Facade | **全部 Facade 化** ✅ |
| **TimeEvent** | `Dispatcher(new Event())` 调用链 | **全部事件化** ✅ |
| **事件文件** | `BattleRoleEvents.cs` 200+ 事件 | **`BattleRoleLogicEvents.cs` 200+ 事件** ✅ |

---

## 3. 继承关系

```
IBattleSystem（接口：AddUpdate/RemoveUpdate/Register/Unregister/Dispatcher）
  ├── BattleMonoSystemBase (MonoBehaviour + IBattleSystem)  ← 原 BattleSystemBase，Phase 5 改名
  │     ├── BattleRoleLogic (主角色逻辑系统，122 行，24 个 Component) ✅
  │     └── BattleRole (角色表现系统，338 行，40+ Component) ✅
  └── BattleLogicSystemBase (纯 C# + IBattleSystem)  ← Phase 6 新建
        ├── RoleLogicClient (客户端子系统，1 个自管组件) ✅ Phase 6
        └── RoleLogicServer (服务端子系统，10 个自管组件 + 33 Feature) ✅ Phase 7

BattleComponent（纯 C# 组件基类）
    ├── BattleRoleComponent（BattleRole 专属）
    │       └── [40+ 个完整 Component]
    ├── BattleRoleLogicComponent（BattleRoleLogic 专属）
    │       └── [24 个完整 Component] ✅
    ├── RoleLogicClientComponent（RoleLogicClient 专属）  ← Phase 6 新建
    │       └── RoleLogicClientBladeBallComponent ✅
    └── RoleLogicServerComponent（RoleLogicServer 专属）  ← Phase 7 新建
            └── [10 个已完成的 Component] ✅
```

---

## 4. 事件系统：作用、边界与规范

> **这是 v2.0 相较 v1.0 最重要的补充。v1.0 完全忽略了事件系统的设计，导致建出来的 Component 只是空壳。**

### 4.1 事件系统的作用

事件系统（`BattleRoleLogicEvents`）解决的核心问题是：**组件解耦**。

在拆分前，`BattleRoleLogic` 的方法直接在文件内相互调用，如：

```csharp
// 拆分前：BattleRoleLogic.cs 内部直接调用
public void CmdPickItem(PickItemNet item) {
    addPickItem(item);          // 直接调用 Inventory 方法
    CmdClearRoleSkill();        // 直接调用 Skill 方法
    SetWeaponState();           // 直接调用 Weapon 方法
}
```

拆分后，`CmdPickItem` 在 `RoleLogicInventoryComponent` 里，它不能直接访问 `RoleLogicSkillComponent` 或 `RoleLogicWeaponComponent`。事件系统负责桥接：

```csharp
// 拆分后：通过事件通信
// RoleLogicInventoryComponent 内部
private void OnPickItem(BattleRoleLogicEvents.PickItem evt) {
    addPickItem(evt.item);
    Dispatcher(new BattleRoleLogicEvents.ClearRoleSkill());   // 通知 SkillComponent
    Dispatcher(new BattleRoleLogicEvents.RefreshWeaponState()); // 通知 WeaponComponent
}
```

**总结：事件系统是组件间通信的唯一渠道，它的存在让每个 Component 对其他 Component 无感知。**

### 4.2 事件系统的边界（什么场景用，什么场景不用）

| 场景 | 是否走事件 | 理由 |
|------|-----------|------|
| **Component A 触发 Component B 的行为** | ✅ 必须走事件 | 组件间解耦的核心场景 |
| **`timeEvent()` 骨架驱动各组件的帧更新** | ✅ 走事件（`Dispatcher(new XxxTimeEvent())`）| 与 BattleRole 保持一致 |
| **外部系统调用 `roleLogic.SetState(...)` 等公共方法** | ✅ Facade 方法体内走 `Dispatcher` | 外部 API 不变，内部走事件 |
| **Component 内部的私有方法相互调用** | ❌ 不走事件 | 同一组件内部直接调用即可 |
| **Component 读取 `roleLogic` 上的公共字段**（如 `roleLogic.AutoRoleId`）| ❌ 不走事件 | 只读字段直接访问，过度设计 |
| **Component 通过 `AddUpdate` 注册自身帧逻辑** | ❌ 不走事件 | `AddUpdate` 本身就是帧驱动机制 |

### 4.3 三种事件类型

参照 `BattleRoleEvents.cs` 成熟模式，`BattleRoleLogicEvents` 包含三类事件：

#### 类型 1：命令事件（写操作，触发某个行为）

```csharp
public static class BattleRoleLogicEvents {

    /// <summary>命令：清除角色技能状态</summary>
    public struct ClearRoleSkill { }

    /// <summary>命令：拾取物品</summary>
    public struct PickItem {
        public PickItemNet item;
        public bool isAutoPick;
    }

    /// <summary>命令：设置同步状态位</summary>
    public struct SetSyncState {
        public RoleSyncState state;
        public bool value;
    }
}
```

#### 类型 2：查询事件（读操作，通过 CallBack 返回数据）

```csharp
    /// <summary>查询：获取当前武器列表（CallBack 返回结果）</summary>
    public struct QueryWeapons {
        public System.Action<System.Collections.Generic.List<PickItemNet>> CallBack;
    }

    /// <summary>查询：获取某个状态位（参照 BattleRoleEvents.QueryEngagementEnemys）</summary>
    public struct QuerySyncState {
        public RoleSyncState state;
        public System.Action<bool> CallBack;
    }
```

#### 类型 3：时序事件（TimeEvent 骨架派发，驱动各组件帧更新）

```csharp
    // TimeEvent 骨架中派发，各 Component 监听并执行自己的帧逻辑
    public struct StateSync { }           // 状态同步帧
    public struct NoNetStateSync { }      // 无网状态同步帧
    public struct MoveCalcTimeEvent { }   // 移动计算帧
    public struct InventoryTimeEvent { }  // 背包检测帧
```

### 4.4 Facade 模式（外部接口零破坏）

Partial 文件从"原始实现"改为"Dispatcher Facade"，这是外部接口零破坏的关键：

```csharp
// 拆分前：RoleLogic_Skill.cs（原始实现，300行）
public partial class BattleRoleLogic {
    public void CmdClearRoleSkill() {
        // 100行逻辑...
    }
}

// 拆分后：RoleLogic_Skill.cs（Facade，3行）
public partial class BattleRoleLogic {
    public void CmdClearRoleSkill()
        => Dispatcher(new BattleRoleLogicEvents.ClearRoleSkill());
}
// 真正的逻辑迁移到 RoleLogicSkillComponent.cs
```

**外部调用方（`roleLogic.CmdClearRoleSkill()`）无需任何改动。**

### 4.5 事件命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 命令事件 | 动词 + 名词（PascalCase）| `PickItem`、`ClearRoleSkill`、`SetSyncState` |
| 查询事件 | `Query` + 名词 | `QueryWeapons`、`QuerySyncState` |
| 时序事件 | 系统名 + `TimeEvent` | `MoveCalcTimeEvent`、`StateSync` |

---

## 5. 完整迁移流程（每个 Component 必须走完的 3 步）

以 `RoleLogicSkillComponent` 迁移 `RoleLogic_Skill.cs` 为例：

### Step 1：在 `BattleRoleLogicEvents.cs` 定义事件

```csharp
public static class BattleRoleLogicEvents {

    /// <summary>命令：清除角色技能</summary>
    public struct ClearRoleSkill { }

    /// <summary>命令：设置技能状态</summary>
    public struct SetSkillState {
        public int skillId;
        public bool active;
    }
    
    // ... 其他 Skill 相关事件
}
```

### Step 2：将 Partial 文件改为 Facade

```csharp
// RoleLogic_Skill.cs（改造后，全文约 20 行）
public partial class BattleRoleLogic {
    public void CmdClearRoleSkill()
        => Dispatcher(new BattleRoleLogicEvents.ClearRoleSkill());

    public void SetSkillState(int skillId, bool active)
        => Dispatcher(new BattleRoleLogicEvents.SetSkillState { skillId = skillId, active = active });

    // ... 所有公开方法改为单行 Dispatcher Facade
}
```

### Step 3：在 Component 中实现逻辑

```csharp
// RoleLogicSkillComponent.cs（实现所有 Skill 逻辑）
public class RoleLogicSkillComponent : BattleRoleLogicComponent {

    // 私有状态字段（从 RoleLogic_Fields.cs 迁入）
    private SkillData _skillData;
    // ...

    protected override void OnAwake() {
        Register<BattleRoleLogicEvents.ClearRoleSkill>(OnClearRoleSkill);
        Register<BattleRoleLogicEvents.SetSkillState>(OnSetSkillState);
        AddUpdate(OnUpdate);
    }

    protected override void OnClear() {
        Unregister<BattleRoleLogicEvents.ClearRoleSkill>(OnClearRoleSkill);
        Unregister<BattleRoleLogicEvents.SetSkillState>(OnSetSkillState);
        RemoveUpdate(OnUpdate);
        base.OnClear();
    }

    private void OnUpdate(float dt) {
        // 原 Skill 帧逻辑
    }

    private void OnClearRoleSkill(BattleRoleLogicEvents.ClearRoleSkill evt) {
        // 原 CmdClearRoleSkill() 的 100 行逻辑
    }

    private void OnSetSkillState(BattleRoleLogicEvents.SetSkillState evt) {
        // 原 SetSkillState() 逻辑
    }
}
```

---

## 6. 组件规划（完整清单）— ✅ 全部完成

### 6.1 基础设施文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `BattleRoleLogicComponent.cs` | ✅ 已完成 | 组件基类（19 行） |
| `BattleRoleLogicEvents.cs` | ✅ 已完成 | 事件定义（200+ 事件） |
| `BattleMonoSystemBase.cs` | ✅ 已完成 | 原 BattleSystemBase，Phase 5 改名 |
| `BattleLogicSystemBase.cs` | ✅ 已完成 | 纯 C# IBattleSystem，Phase 6 新建 |
| `RoleLogicClientComponent.cs` | ✅ 已完成 | RoleLogicClient 组件基类，Phase 6 新建 |

### 6.2 骨架 Partial 文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `RoleLogic_Fields.cs` | ✅ 已完成（974 行）| 公共字段声明 |
| `RoleLogic_Init.cs` | ✅ 已完成（313 行）| `init()` 辅助方法 |
| `RoleLogic_Clear.cs` | ✅ 已完成（71 行）| `clear()` 辅助方法 |
| `RoleLogic_TimeEvent.cs` | ✅ 已完成（96 行）| `timeEvent()` 分支 |

### 6.3 来自 Partial 文件的 Component 迁移 — ✅ 全部完成

| 目标 Component | 来源 Partial | 来源行数 | 迁移阶段 | 状态 |
|--------------|------------|---------|---------|------|
| `RoleLogicSkillComponent` | `RoleLogic_Skill.cs` | 206 | **4A** | ✅ 完成 |
| `RoleLogicWeaponComponent` | `RoleLogic_Weapon.cs` | 224 | **4A** | ✅ 完成 |
| `RoleLogicLobbyComponent` | `RoleLogic_Lobby.cs` | 112 | **4A** | ✅ 完成 |
| `RoleLogicLocalStatesComponent` | `RoleLogic_LocalStates.cs` | 105 | **4A** | ✅ 完成 |
| `RoleLogicDataInfoComponent` | `RoleLogic_DataInfo.cs` | 180 | **4A** | ✅ 完成 |
| `RoleLogicDungeonComponent` | `RoleLogic_DungeonGame.cs` | 272 | **4A** | ✅ 完成 |
| `RoleLogicModeComponent` | `RoleLogic_Mode.cs` + 4 个小文件合并 | 310+90 | **4A** | ✅ 完成 |
| `RoleLogicStateComponent` | `RoleLogic_States.cs`（枚举另提取）| 1345 | **4B** | ✅ 完成 |
| `RoleLogicTeammateBehaviorComponent` | `RoleLogic_TeammateBehavior.cs` | 1197 | **4B** | ✅ 完成 |

### 6.4 来自主文件的拆分 — ✅ 全部完成

| 目标 Component | 职责 | 预估行数 | 迁移阶段 | 状态 |
|--------------|------|---------|---------|------|
| `RoleLogicInventoryComponent` | 背包/装备/拾取物管理 | ~450 行 | **4C** | ✅ 完成 |
| `RoleLogicMoveComponent` | 移动方向/载具/移速计算 | ~250 行 | **4C** | ✅ 完成 |
| `RoleLogicNetworkComponent` | 网络重连/丢包/GME 语音 | ~150 行 | **4C** | ✅ 完成 |
| `RoleLogicAIComponent` | AI 行为驱动与武器选择 | ~110 行 | **4C** | ✅ 完成 |
| `RoleLogicUprearComponent` | 扶人/被救逻辑 | ~90 行 | **4C** | ✅ 完成 |

### 6.5 枚举提取 — ✅ 完成

| 文件 | 状态 | 说明 |
|------|------|------|
| `RoleLogicEnums.cs` | ✅ 已完成 | 从 `RoleLogic_States.cs` 提取 `RoleSyncState / RoleLocalState / RoleCmdState` 等枚举 |

### 6.6 当前文件结构（✅ Phase 7 完成）

```
Assets/Script/GamePlay/Host/Modules/Role/
├── BattleMonoSystemBase.cs             ← ✅ MonoBehaviour 基类（原 BattleSystemBase，Phase 5 改名）
├── BattleLogicSystemBase.cs            ← ✅ 纯 C# 基类（Phase 6 新建，供 Client/Server 使用）
├── IBattleSystem.cs                    ← ✅ 接口
├── BattleComponent.cs                  ← ✅ 组件框架基类
├── BattleRoleLogicComponent.cs         ← ✅ BattleRoleLogic 组件基类
├── BattleRoleLogicEvents.cs            ← ✅ 事件定义（200+ 事件）
├── BattleRoleLogic.cs                  ← ✅ 主文件（122 行）
│
└── BattleRoleLogic/
    ├── RoleLogicEnums.cs               ← ✅ 枚举定义
    ├── RoleLogic_Fields.cs             ← ✅ 骨架 Partial
    ├── RoleLogic_Init.cs               ← ✅ 骨架 Partial
    ├── RoleLogic_Clear.cs              ← ✅ 骨架 Partial
    ├── RoleLogic_TimeEvent.cs          ← ✅ 骨架 Partial
    ├── RoleLogic_New.cs                ← ✅ Feature API（AddFeature/GetFeature/RemoveFeature）
    ├── RoleLogic_*.cs                  ← ✅ 各 Facade Partial
    ├── RoleLogicClientComponent.cs     ← ✅ Phase 6 Client 组件基类
    ├── RoleLogicServerComponent.cs     ← ✅ Phase 7 Server 组件基类
    │
    └── Component/
        └── [24 个已完成的 BattleRoleLogicComponent]

Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/
├── RoleLogicClient.cs                  ← ✅ Phase 6 客户端子系统壳
├── RoleLogicClient_*.cs                ← ✅ 各 Partial 文件（方法保留在壳内）
└── Component/
    └── RoleLogicClientBladeBallComponent.cs ← ✅ Phase 6

Assets/Script/GamePlay/Server/Modules/Role/
├── RoleLogicServer.cs                  ← ✅ Phase 7 服务端子系统壳（含功能注释）
├── RoleLogicServer_*.cs                ← ✅ 各 Partial 文件（字段/方法提取）
└── Component/
    └── [10 个已完成的 RoleLogicServerComponent] ← ✅ Phase 7
```

---

## 7. 最终形态：BattleRoleLogic.cs 当前内容（✅ 已达成）

```csharp
[SymbolObfus]
public partial class BattleRoleLogic : BattleMonoSystemBase {  // ← 已改名

    public void init(BattleWorld gameWorld) {
        // ... 基础赋值
        AddComponents();
    }

    private void AddComponents() {
        // 24 个组件注册
        AddComponent<RoleLogicSkillComponent>();
        AddComponent<RoleLogicWeaponComponent>();
        // ... (24 个)
    }

    public void clear(bool removeAllSkin) {
        ClearAllComponents();
    }

    public void timeEvent() {
        if (_isInit == false || GameData.IsUnloading) return;
        TimeEventBody();
        DriveComponents(TimeData.deltaTime);
    }
}
// 实际 122 行
```

---

## 8. 关键风险与缓解（回顾）

| 风险 | 状态 | 缓解结果 |
|------|------|---------|
| **Partial 顶部的枚举/类型丢失** | ✅ 已解决 | `RoleLogicEnums.cs` 统一存放 |
| **枚举全局引用** | ✅ 已解决 | 不改类型名，0 外部改动 |
| **`#if SERVER_LOGIC`** | ✅ 已解决 | 保留条件编译块 |
| **外部接口破坏** | ✅ 已解决 | 所有方法保留 Facade |
| **空壳 Component 误判** | ✅ 已解决 | v2.0 定义清晰，全部补充完整实现 |
| **`RoleLogic_New.cs`** | ✅ 已解决 | 已渐进废弃 |

---

## 9. 验收标准 — ✅ 全部达标

### 9.1 每个 Component 迁移验收

- [x] `BattleRoleLogicEvents.cs` 中定义了对应事件 struct
- [x] Partial 文件改为单行 Facade（`=> Dispatcher(new Event{...})`）
- [x] Component 的 `OnAwake` 完成 `Register + AddUpdate`，`OnClear` 完成 `Unregister + RemoveUpdate`
- [x] Component 包含原 partial 文件的完整逻辑实现

### 9.2 整体验收

- [x] `BattleRoleLogic.cs` 主文件 ≤400 行（实际 **122 行**）
- [x] 所有 Partial 文件改为 Facade / 骨架
- [x] `BattleRoleLogicEvents.cs` 覆盖所有跨组件通信场景
- [x] 编译通过，无报错
- [x] 所有 `#if SERVER_LOGIC` 条件编译块正确保留

---

## 10. 后续规划

> BattleRoleLogic 本体重构（Phase 1-5）已完成。子系统打散（Phase 6-7）已完成。
> Feature → Component 统一（Phase 8）已试点后暂停，详见：
> 📄 [[RoleLogic子系统打散方案]]（v2.1，§5）
>
> **当前架构总览**：
> - BattleRoleLogic 主体：122 行 + 24 Component ✅
> - RoleLogicClient 子系统：生命周期壳 + 1 Component + 13 Feature ✅
> - RoleLogicServer 子系统：生命周期壳 + 10 Component + 20 Feature ✅
> - Feature 系统（33 个）：保持 `AbsRoleLogicFeature` 基类，待 Phase 8 重新评估后统一
