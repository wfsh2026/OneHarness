# BattleRole.cs 组件化重构方案（修订版）

## 1. 背景与目标

### 现状（实测数据）
- `BattleRole.cs` 共 **4570 行**，是一个直接继承 `MonoBehaviour` 的巨型类
- 同目录下已有 32 个 `Role_XXX.cs` partial 文件，共 **17901 行**，合计 **22471 行**
- 逻辑混杂：初始化、显示、网络、音效、跳伞、装备等职责全部堆在一起
- BattleRole.cs 前 382 行几乎全是 `public` 字段/属性声明，被几十个外部类直接引用
- 路径：Assets\Script\GamePlay\Host\Modules\Role\BattleRole.cs

### 目标
- 将 `BattleRole` 转变为一个**轻量容器（Orchestrator）**，只负责持有引用和管理组件生命周期
- 各职责域拆成独立的 **纯 C# 组件类**，每个文件 300~500 行，职责单一
- 组件生命周期命名与 `Biubiubiu2` 框架保持一致（`OnAwake` / `OnStart` / `OnClear` / `AddUpdate`）
- 对 AI 生成友好：每个组件文件独立、上下文清晰、无隐式全局依赖
- 为后续迁移至 Biubiubiu2 新架构做准备（换基类即可，业务代码不动）

---

## 2. 整体架构层级

与 Biubiubiu2 完整对照：

| Biubiubiu2 | 本框架 | 说明 |
|---|---|---|
| `IBattleSystem`（接口） | `IBattleSystem` | 对外契约，定义系统能力（含事件系统） |
| `SystemBase`（抽象基类） | `BattleSystemBase` | 承载组件管理 + 事件系统，**新增** |
| `SystemBase_Event`（事件系统） | `BattleSystemBase` 内置 | 简化版事件系统，用泛型字典实现 |
| `C_Character_Base` | `BattleRole` | 继承基类，只写装配逻辑 |
| `ComponentBase` | `BattleComponent` | 通用组件根基类（含事件快捷方法），**新增** |
| `ClientCharacterComponent` | `BattleRoleComponent` | 角色专属组件基类，**新增** |

> **与二代的根本差异**：二代 `SystemBase` 是纯 C# class，本框架 `BattleSystemBase` 必须是 `MonoBehaviour`（BattleRole 挂载在 Unity 预制体上）。

层级关系图：

```
IBattleSystem（接口，含 AddUpdate + 事件系统）
    └── BattleSystemBase（抽象基类，MonoBehaviour）  ← 组件管理 + 事件总线在这里
            └── BattleRole（MonoBehaviour）           ← 只写 AddComponents() 装配
```

```
BattleComponent（通用组件基类，纯 C# class，提供事件快捷方法）
    └── BattleRoleComponent（角色组件基类，提供 role/roleLogic/roleNet 快捷访问）
            └── BattleRoleSkinComponent / BattleRoleFlyComponent / ...（具体组件）
```

---

## 3. 新增文件：组件基础设施

### 3.1 `IBattleSystem.cs` ⭐ 核心新增

**路径：** `Assets/Script/GamePlay/Host/Modules/IBattleSystem.cs`

系统接口，定义所有系统对外暴露的能力契约。组件只依赖此接口，不依赖任何具体类。

> **修订说明**：原方案只有 `AddUpdate/RemoveUpdate`，缺少事件系统。二代 `SystemBase` 的核心能力是 `Register/Unregister/Dispatcher` 事件总线，这是组件间通信的唯一通道。现已补全。

```csharp
using System;

/// <summary>
/// 战斗系统接口
/// 对标 Biubiubiu2 中 SystemBase 对外暴露的能力契约
/// 包含：Update 注册 + 事件系统
/// </summary>
public interface IBattleSystem {
    // ---- Update 注册 ----
    void AddUpdate(Action<float> action);
    void RemoveUpdate(Action<float> action);

    // ---- 事件系统（对标 SystemBase_Event 的 Register/Dispatcher） ----
    void Register<T>(Action<T> handler) where T : struct;
    void Unregister<T>(Action<T> handler) where T : struct;
    void Dispatcher<T>(T evt) where T : struct;
}
```

### 3.2 `BattleSystemBase.cs` ⭐ 核心新增

**路径：** `Assets/Script/GamePlay/Host/Modules/BattleSystemBase.cs`

**组件管理能力的真正载体**。对标 Biubiubiu2 的 `SystemBase` + `SystemBase_Event`，承载 `AddComponent<T>`、组件列表管理、Update 驱动、事件系统等通用能力。

`BattleRole` 不再自己持有这些逻辑——继承此基类即可获得全套组件管理能力，未来其他系统（载具、道具等）也可以继承它。

> **修订说明**：新增事件系统（Register/Unregister/Dispatcher），对标二代 `SystemBase_Event.cs`。采用简化版泛型字典实现，暂不支持优先级（二代的优先级在一代场景下用不上）。

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// 战斗系统基类（MonoBehaviour）
/// 对标 Biubiubiu2 SystemBase + SystemBase_Event
/// 承载通用组件管理能力 + 事件系统，业务类继承此基类即可
/// </summary>
public abstract class BattleSystemBase : MonoBehaviour, IBattleSystem {

    private readonly List<BattleComponent> _components = new List<BattleComponent>();
    private readonly List<Action<float>> _updateList = new List<Action<float>>();
    private readonly List<BattleComponent> _pendingStart = new List<BattleComponent>();

    // 事件系统（简化版，对标 SystemBase_Event）
    private readonly Dictionary<Type, Delegate> _eventHandlers = new Dictionary<Type, Delegate>();

    // ---- IBattleSystem 实现：Update 注册 ----

    public void AddUpdate(Action<float> action) {
        if (!_updateList.Contains(action))
            _updateList.Add(action);
    }

    public void RemoveUpdate(Action<float> action) {
        _updateList.Remove(action);
    }

    // ---- IBattleSystem 实现：事件系统 ----

    public void Register<T>(Action<T> handler) where T : struct {
        var key = typeof(T);
        if (_eventHandlers.TryGetValue(key, out var existing)) {
            _eventHandlers[key] = Delegate.Combine(existing, handler);
        } else {
            _eventHandlers[key] = handler;
        }
    }

    public void Unregister<T>(Action<T> handler) where T : struct {
        var key = typeof(T);
        if (_eventHandlers.TryGetValue(key, out var existing)) {
            var result = Delegate.Remove(existing, handler);
            if (result == null)
                _eventHandlers.Remove(key);
            else
                _eventHandlers[key] = result;
        }
    }

    public void Dispatcher<T>(T evt) where T : struct {
        if (_eventHandlers.TryGetValue(typeof(T), out var handler)) {
            ((Action<T>)handler)?.Invoke(evt);
        }
    }

    // ---- 组件管理（对标 SystemBase.AddComponent<T>） ----

    protected T AddComponent<T>() where T : BattleComponent, new() {
        var component = new T();
        _components.Add(component);
        component.Awake(this);
        _pendingStart.Add(component);
        return component;
    }

    /// <summary>
    /// 获取已添加的组件（对标 SystemBase.GetComponent<T>）
    /// </summary>
    protected T GetBattleComponent<T>() where T : BattleComponent {
        for (int i = 0; i < _components.Count; i++) {
            if (_components[i] is T comp) return comp;
        }
        return null;
    }

    // 在 Update 驱动开头处理延迟 Start（对标 SystemBase.InvokeComponentStart）
    protected void DriveComponents(float deltaTime) {
        InvokeComponentStart();
        for (int i = 0; i < _updateList.Count; i++) {
            _updateList[i]?.Invoke(deltaTime);
        }
    }

    private void InvokeComponentStart() {
        if (_pendingStart.Count == 0) return;
        for (int i = 0; i < _pendingStart.Count; i++) {
            _pendingStart[i].Start();
        }
        _pendingStart.Clear();
    }

    protected void ClearAllComponents() {
        for (int i = _components.Count - 1; i >= 0; i--) {
            _components[i].Clear();
        }
        _components.Clear();
        _updateList.Clear();
        _pendingStart.Clear();
        _eventHandlers.Clear();
    }
}
```

### 3.3 `BattleComponent.cs` ⭐ 核心新增

**路径：** `Assets/Script/GamePlay/Host/Modules/BattleComponent.cs`

通用组件根基类，对标 Biubiubiu2 的 `ComponentBase`。不只角色组件用，未来载具、道具组件也继承它。

> **修订说明**：新增事件系统快捷方法（Register/Unregister/Dispatcher），与二代 `ComponentBase` 能力对等。

```csharp
using System;

/// <summary>
/// 通用战斗组件基类（纯 C# class）
/// 对标 Biubiubiu2 ComponentBase
/// </summary>
public abstract class BattleComponent {

    protected bool isClear = false;

    // 与 Biubiubiu2 ComponentBase.mySystem 命名完全一致
    protected IBattleSystem mySystem { get; private set; }

    // ---- 框架驱动，业务层不要重写 ----

    public void Awake(IBattleSystem system) {
        this.mySystem = system;
        OnAwake();
    }

    public void Start() {
        if (isClear) return;
        OnStart();
    }

    public void Clear() {
        if (isClear) return;
        OnClear();
        isClear = true;
        mySystem = null;
    }

    // ---- 业务层重写这三个 ----

    protected virtual void OnAwake() { }
    protected virtual void OnStart() { }
    protected virtual void OnClear() { }

    // ---- Update 注册快捷方法 ----

    protected void AddUpdate(Action<float> action) {
        mySystem?.AddUpdate(action);
    }

    protected void RemoveUpdate(Action<float> action) {
        mySystem?.RemoveUpdate(action);
    }

    // ---- 事件系统快捷方法（对标 ComponentBase 的 Register/Dispatcher） ----

    protected void Register<T>(Action<T> handler) where T : struct {
        mySystem?.Register(handler);
    }

    protected void Unregister<T>(Action<T> handler) where T : struct {
        mySystem?.Unregister(handler);
    }

    protected void Dispatcher<T>(T evt) where T : struct {
        mySystem?.Dispatcher(evt);
    }
}
```

### 3.4 `BattleRoleComponent.cs` ⭐ 核心新增

**路径：** `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleComponent.cs`

角色专属组件基类，对标 Biubiubiu2 的 `ClientCharacterComponent`。在通用 `BattleComponent` 基础上，提供快捷访问 `BattleRole` 及其子系统的能力。

> **修订说明**：新增 `roleNet` 快捷访问，角色组件内高频使用网络接口。

```csharp
/// <summary>
/// BattleRole 专属组件基类（纯 C# class）
/// 对标 Biubiubiu2 ClientCharacterComponent
/// 子类可直接访问 role、roleLogic、roleNet、gameWorld 等高频引用
/// </summary>
public abstract class BattleRoleComponent : BattleComponent {

    protected BattleRole role { get; private set; }
    protected BattleRoleLogic roleLogic => role?.MyRoleLogic;
    protected StartGame startGame => role?.MyStartGame;
    protected BattleWorld gameWorld => startGame?.MyGameWorld;
    protected RoleNet roleNet => roleLogic?.MyRoleNet;

    // Awake 入参是 BattleRole，向上转型为 IBattleSystem 传给基类
    // BattleRole 继承 BattleSystemBase，BattleSystemBase 实现 IBattleSystem
    public void Awake(BattleRole battleRole) {
        this.role = battleRole;
        base.Awake(battleRole);
    }

    protected override void OnClear() {
        role = null;
    }
}
```

### 3.5 `BattleRoleEvents.cs` ⭐ 核心新增

**路径：** `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleEvents.cs`

集中定义 BattleRole 系统内的所有事件 struct。对标二代 `SE_Character.cs` / `CE_Character.cs` 的职责——**一个文件看到所有可用事件**。

> **说明**：二代使用 `ISystemEvent` + `int ID` 机制（`GamePlayEvent.ReadonlySystemEventID<T>()`），本框架简化为纯 `struct`（通过泛型 `Register<T>` / `Dispatcher<T>` where T : struct 分发，Key 是 Type 而非 int）。结构上对齐，但无需复刻 ID 基础设施。
> 
> **事件内容随组件拆分逐步补充**：阶段 2/3/4 每拆出一个组件，如需组件间通信就在此文件新增对应事件定义。阶段 1 只建空壳。

```csharp
/// <summary>
/// BattleRole 系统事件定义
/// 对标 Biubiubiu2 的 SE_Character / CE_Character
/// 所有 BattleRole 组件间通信事件集中定义在此
/// 
/// 使用方式：
///   注册：Register<BattleRoleEvents.SkinChanged>(OnSkinChanged);
///   派发：Dispatcher(new BattleRoleEvents.SkinChanged { SkinSign = "xxx" });
/// </summary>
public static class BattleRoleEvents {

    // ═══════════════════════════════════════════
    // 皮肤/换装
    // ═══════════════════════════════════════════
    
    /// <summary>
    /// 皮肤更新事件（由 SkinComponent 派发，ShowComponent 等监听）
    /// </summary>
    public struct SkinChanged {
        public string SkinSign;
    }

    // ═══════════════════════════════════════════
    // 显示/隐藏
    // ═══════════════════════════════════════════
    
    /// <summary>
    /// 角色显隐状态变化
    /// </summary>
    public struct VisibilityChanged {
        public bool IsVisible;
    }

    // ═══════════════════════════════════════════
    // 状态变化
    // ═══════════════════════════════════════════

    /// <summary>
    /// 角色状态变化（如：倒地、复活等）
    /// </summary>
    public struct StateChanged {
        public int OldState;
        public int NewState;
    }

    // ═══════════════════════════════════════════
    // 以下事件在阶段 2/3/4 拆组件时逐步补充
    // ═══════════════════════════════════════════
    
    // 飞行状态变化
    // public struct FlyStateChanged { ... }
    
    // 载具上下车
    // public struct CarStateChanged { ... }
    
    // 装备显示更新
    // public struct EquipDisplayChanged { ... }
    
    // ... 更多事件随组件拆分逐步添加 ...
}
```

> **与二代对照示例：**
> 
> ```
> // 二代写法：
> SE_Character.StandTypeChange evt = new SE_Character.StandTypeChange();
> evt.StandType = CharacterData.StandType.Stand;
> Dispatcher(evt);
> 
> // 一代对等写法：
> Dispatcher(new BattleRoleEvents.StateChanged { OldState = 0, NewState = 1 });
> ```

---

## 4. 改动：BattleRole.cs 瘦身

### 4.0 BattleRole.cs 最终保留内容分析

> **修订说明**：原方案预估 BattleRole.cs 最终降至 ~150 行，过于乐观。实际分析后调整为 **~400 行**。

**必须保留在 BattleRole.cs 的内容：**

| 类别 | 预估行数 | 原因 |
|------|---------|------|
| public 字段/属性声明 | ~180 行 | `role.MyRoleSkill`、`role.UserWeapon`、`role.HeadEquipPart` 等被大量外部代码直接访问（RoleNet、PlayerOperateController、WarCamera 等几十个类），迁移会导致全项目级联修改 |
| Init() 骨架 | ~40 行 | 基础引用赋值 + AddComponents() 调用 |
| Clear() 骨架 | ~30 行 | ClearAllComponents() + 必须手动清理的部分 |
| TimeEvent() 骨架 | ~30 行 | 前置守卫判断 + DriveComponents() |
| AddComponents() | ~50 行 | 组件装配清单 |
| Unity 回调 + 工具方法 | ~40 行 | OnDisable、坐标转换等多组件共用的工具方法 |
| **合计** | **~370-420 行** | |

**不可拆分的硬底线：~255 行**

| 内容 | 行数 | 不可拆的原因 |
|------|------|------------|
| public 字段声明（当前 L1-382） | ~180 行（去除空行/注释） | 外部直接 `role.XXX` 访问，迁移需全项目改 |
| Init() 中基础赋值 | ~20 行 | 组件装配前必须先有这些引用 |
| TimeEvent() 前置守卫 | ~15 行 | 全局状态检查，不属于任何单一组件 |
| RoleTransformPoint 等坐标工具 | ~30 行 | 被 Init/Clear/多个组件共用 |
| IsClear 标记 + OnDisable | ~10 行 | MonoBehaviour 生命周期 |

### 4.1 BattleRole 继承 BattleSystemBase

```csharp
// 改动前
public partial class BattleRole : MonoBehaviour { ... }

// 改动后
public partial class BattleRole : BattleSystemBase { ... }
// BattleSystemBase 已继承 MonoBehaviour 并实现 IBattleSystem
// BattleRole 无需再自己实现任何组件管理逻辑
```

### 4.2 Init() 和 Clear() 改造

`BattleRole` 里**不再有**任何组件列表、AddComponent、Update 驱动代码，全部由基类提供。

**改动前（Init 内部直接散乱调用）：**
```csharp
public void Init(Vector3 pos) {
    // 200+ 行，各种初始化混杂
    MyRoleSkill = new RoleSkill();
    MyRoleSkill.Init(this);
    MyRoleEffect.Init(this);
    // ...几十行类似的...
}
```

**改动后（Init 职责收窄为基础赋值 + 组件装配）：**
```csharp
public void Init(Vector3 pos) {
    // 保留必须在此阶段处理的基础引用赋值（约 30 行）
    mStartGame = MyRoleLogic.MyStartGame;
    gameWorld = mStartGame.MyGameWorld;
    MyTransform = transform;
    MyGameObj = gameObject;

    // 组件装配，清晰可读，AddComponent 来自 BattleSystemBase
    AddComponents();

    // 剩余不可组件化的逻辑（约 20 行）
    RoleTransformPoint(pos);
}

private void AddComponents() {
    AddComponent<BattleRoleSkinComponent>();
    AddComponent<BattleRoleFlyComponent>();
    AddComponent<BattleRoleShowComponent>();
    AddComponent<BattleRoleEquipComponent>();
    AddComponent<BattleRolePositionComponent>();
    AddComponent<BattleRoleNetworkComponent>();
    AddComponent<BattleRoleCombatComponent>();
    AddComponent<BattleRoleSideAimComponent>();
    AddComponent<BattleRoleEnergyBattleComponent>();
    // ... 按需增删，条件装配直接写 if
}
```

**改动后（Clear 瘦身）：**
```csharp
public void Clear(bool removeAllSkin) {
    IsClear = true;
    ClearAllComponents(); // 来自 BattleSystemBase，一行搞定

    // 保留必须手动处理的部分
    if (MyRoleControl != null) {
        MyRoleControl.clear(removeAllSkin);
    }
}
```

**改动后（TimeEvent 改造）：**

> **修订说明**：原方案暗示 TimeEvent 可直接替换为 DriveComponents，实际不可行。当前 TimeEvent() 有 ~100 行前置守卫逻辑（IsClear 判断、IsLocalRole/IsAI/OtherRole 分支等），且内部按角色类型分支执行不同逻辑。**策略：TimeEvent() 保留为调度入口，内部逐步收窄，末尾调用 DriveComponents()。**

```csharp
public void TimeEvent() {
    // 前置守卫（必须保留，不属于任何单一组件）
    if (IsClear || ...) return;

    // 驱动所有组件的 Update（来自 BattleSystemBase）
    DriveComponents(TimeData.deltaTime);
}
```

---

## 5. 完整组件文件清单

路径统一放在：`Assets/Script/GamePlay/Host/Modules/Role/Component/`

来源分两类：**BattleRole.cs 内的逻辑** 和 **现有 Role_XXX.cs partial 文件**。所有 partial 文件最终全部消除，统一变成独立组件。

### 5.1 来自 BattleRole.cs 的拆分（新拆）

| 组件文件 | 职责 | 来源行范围 | 预计行数 |
|---------|------|-----------|---------|
| `BattleRoleSkinComponent.cs` | 换装数据、皮肤更新 | 849–944 | ~120 |
| `BattleRoleFlyComponent.cs` | 飞机跳伞、降落伞、滑翔、滑索 | 945–1060, 3095–3385 | ~350 |
| `BattleRoleShowComponent.cs` | 角色显示/隐藏、遮挡判断 | 1817–2138 | ~320 |
| `BattleRoleCarSyncComponent.cs` | 载具上下车状态同步 | 2139–2258 | ~120 |
| `BattleRoleStateSyncComponent.cs` | 状态同步（圣剑/复活/队伍） | 2258–2567 | ~300 |
| `BattleRolePositionComponent.cs` | 坐标检查、地形检测、高度点 | 2567–3092 | ~500 |
| `BattleRoleEquipComponent.cs` | 装备显示（头盔/防弹衣/背包） | 4200–4640 | ~440 |
| `BattleRoleSideAimComponent.cs` | 侧身 + 抬枪逻辑 | 3891–4148 | ~260 |
| `BattleRoleNetworkComponent.cs` | 心跳、Ping、RTT、重连检测 | 1696–1815, 4149–4198 | ~200 |
| `BattleRoleBuffComponent.cs` | Buff 上传、CmdBuff 系列 | 3767–3890 | ~125 |
| `BattleRoleCombatComponent.cs` | 近战/投掷物/使用道具 | 3387–3630 | ~240 |
| `BattleRoleEnergyBattleComponent.cs` | 能源争夺战专属逻辑 | 4640–4788 | ~150 |
| `BattleRoleEngageComponent.cs` | 交战数据统计 | 4790–4971 | ~180 |

### 5.2 来自现有 Role_XXX.cs 的迁移（partial → Component）

现有 32 个 partial 文件共 **17901 行**，全部消除，迁移为独立组件。
大文件（>500 行）内部已有 `#region` 分区，按区再拆为子组件。

| 原 partial 文件 | 行数 | 迁移为组件 | 是否再拆 |
|----------------|------|-----------|---------|
| `Role_HitPart.cs` | 2180 | `BattleRoleHitPartComponent.cs` | ✅ 拆为：主流程 / 魔刀 / 重击 / AI攻击 / 近战模型 / 预输入 共6个子组件 |
| `Role_Item.cs` | 1747 | `BattleRoleItemComponent.cs` | ✅ 拆为：道具使用 / 展示道具 共2个子组件 |
| `Role_Fire.cs` | 1423 | `BattleRoleFireComponent.cs` | ✅ 拆为：主流程 / 暗器 / 榴弹 / 蓄力射击 / 预输入 共5个子组件 |
| `Role_Move.cs` | 1342 | `BattleRoleMoveComponent.cs` | ✅ 拆为：移动 / AddForce / 姿态控制 / BoxingTrampolineFly 共4个子组件 |
| `Role_Weapon.cs` | 1178 | `BattleRoleWeaponComponent.cs` | 保持单组件（内部结构较内聚） |
| `Role_State.cs` | 1135 | `BattleRoleStateComponent.cs` | 保持单组件 |
| `Role_Collider.cs` | 1104 | `BattleRoleColliderComponent.cs` | 保持单组件 |
| `Role_Animation.cs` | 1040 | `BattleRoleAnimationComponent.cs` | ✅ 拆为：基础动画 / 特殊状态动画 共2个子组件 |
| `Role_Sound.cs` | 972 | `BattleRoleSoundComponent.cs` | 保持单组件 |
| `Role_Camera.cs` | 970 | `BattleRoleCameraComponent.cs` | 保持单组件 |
| `Role_Jump.cs` | 760 | `BattleRoleJumpComponent.cs` | 保持单组件 |
| `Role_UprearRole.cs` | 734 | `BattleRoleUprearComponent.cs` | 保持单组件 |
| `Role_SqParachute.cs` | 522 | `BattleRoleSqParachuteComponent.cs` | 保持单组件 |
| `Role_WolfParty.cs` | 443 | `BattleRoleWolfPartyComponent.cs` | 保持单组件 |
| `Role_Sliding.cs` | 421 | `BattleRoleSlidingComponent.cs` | 保持单组件 |
| `Role_Dance.cs` | 384 | `BattleRoleDanceComponent.cs` | 保持单组件 |
| `Role_Hurt.cs` | 377 | `BattleRoleHurtComponent.cs` | 保持单组件 |
| `Role_SneakSand.cs` | 355 | `BattleRoleSneakSandComponent.cs` | 保持单组件 |
| `Role_DefusalMode.cs` | 331 | `BattleRoleDefusalModeComponent.cs` | 保持单组件 |
| `Role_Reload.cs` | 278 | `BattleRoleReloadComponent.cs` | 保持单组件 |
| `Role_HideSeek.cs` | 162 | `BattleRoleHideSeekComponent.cs` | 保持单组件 |
| `Role_OnlyUp.cs` | 157 | `BattleRoleOnlyUpComponent.cs` | 保持单组件 |
| `Role_Dragon.cs` | 122 | `BattleRoleDragonComponent.cs` | 保持单组件 |
| `Role_Sit.cs` | 89 | `BattleRoleSitComponent.cs` | 保持单组件 |
| `Role_Mark.cs` | 81 | `BattleRoleMarkComponent.cs` | 保持单组件 |
| `Role_CheckSceneItem.cs` | 77 | `BattleRoleCheckSceneItemComponent.cs` | 保持单组件 |
| `Role_Robot.cs` | 64 | `BattleRoleRobotComponent.cs` | 保持单组件 |
| `Role_ATEvent.cs` | 56 | → 合并入 `BattleRoleStateComponent.cs` | 太小，合并更合适 |
| `Role_CheckBombArea.cs` | 42 | → 合并入 `BattleRolePositionComponent.cs` | 太小，合并更合适 |
| `Role_BladeBallMode.cs` | 42 | `BattleRoleBladeBallModeComponent.cs` | 保持单组件 |
| `Role_Network.cs` | 33 | → 合并入 `BattleRoleNetworkComponent.cs` | 太小，合并更合适 |
| `Role_MovePlatform.cs` | 26 | → 合并入 `BattleRoleMoveComponent.cs` | 太小，合并更合适 |

---

## 5.5 组件通信规范（事件驱动模式）⭐

### 核心原则

**组件间必须完全通过事件通信，禁止直接引用和方法调用。**

这是 Biubiubiu2 架构的核心设计理念，确保组件的独立性和可测试性。

### 5.5.1 错误做法 ❌

```csharp
// ❌ 错误：在 BattleRole 中保存组件引用
private BattleRoleEngageComponent engageComponent;

private void AddComponents() {
    engageComponent = AddComponent<BattleRoleEngageComponent>();  // 错误！
}

// ❌ 错误：直接调用组件方法
public void UpdateEngageEnemyState(bool isEngage, Role role) {
    engageComponent?.UpdateState(isEngage, role);  // 错误！
}

// ❌ 错误：直接访问组件属性
public List<Role> myEngagementEnemys => engageComponent?.engagementEnemys ?? new List<Role>();  // 错误！
```

**问题**：
- 组件之间形成强耦合，违背了组件独立性原则
- 无法独立测试组件
- 组件的添加/删除会破坏引用
- 不符合 Biubiubiu2 的架构理念

### 5.5.2 正确做法 ✅

#### 第一步：定义事件（在 BattleRoleEvents.cs）

```csharp
// 文件：Assets/Script/GamePlay/Host/Modules/Role/BattleRoleEvents.cs

public static class BattleRoleEvents {
    
    // ══════════════════════════════════════
    // 命令事件（写操作）
    // ══════════════════════════════════════
    
    /// <summary>
    /// 更新交战状态
    /// </summary>
    public struct UpdateEngageState {
        public bool isEngage;
        public Role targetRole;
    }
    
    /// <summary>
    /// 开始能源注入
    /// </summary>
    public struct StartEnergyInject {
        public float duration;
    }
    
    // ══════════════════════════════════════
    // 查询事件（读操作，带 CallBack）
    // ══════════════════════════════════════
    
    /// <summary>
    /// 查询当前交战敌人列表
    /// </summary>
    public struct QueryEngagementEnemys {
        public Action<List<Role>> CallBack;
    }
    
    /// <summary>
    /// 查询能源注入进度
    /// </summary>
    public struct QueryEnergyProgress {
        public Action<float> CallBack;  // 返回 0-1 的进度值
    }
}
```

**规则**：
- 命令事件（写操作）：只包含数据字段
- 查询事件（读操作）：必须包含 `Action<T> CallBack` 字段
- 所有事件都是 `struct`，确保值类型语义
- 事件命名：命令用动词（Update/Start/Stop），查询用 Query 前缀

#### 第二步：组件监听事件

```csharp
// 文件：Assets/Script/GamePlay/Host/Modules/Role/Component/BattleRoleEngageComponent.cs

public class BattleRoleEngageComponent : BattleRoleComponent {
    
    private List<Role> engagementEnemys = new List<Role>();
    
    protected override void OnAwake() {
        base.OnAwake();
        
        // 注册命令事件
        Register<BattleRoleEvents.UpdateEngageState>(OnUpdateEngageState);
        
        // 注册查询事件
        Register<BattleRoleEvents.QueryEngagementEnemys>(OnQueryEngagementEnemys);
    }
    
    protected override void OnClear() {
        base.OnClear();
        
        // 注销事件
        Unregister<BattleRoleEvents.UpdateEngageState>(OnUpdateEngageState);
        Unregister<BattleRoleEvents.QueryEngagementEnemys>(OnQueryEngagementEnemys);
    }
    
    // ──────────────────────────────────────
    // 事件处理函数（全部私有）
    // ──────────────────────────────────────
    
    /// <summary>
    /// 处理命令事件：更新交战状态
    /// </summary>
    private void OnUpdateEngageState(BattleRoleEvents.UpdateEngageState evt) {
        if (evt.isEngage) {
            if (!engagementEnemys.Contains(evt.targetRole)) {
                engagementEnemys.Add(evt.targetRole);
            }
        } else {
            engagementEnemys.Remove(evt.targetRole);
        }
    }
    
    /// <summary>
    /// 处理查询事件：返回交战敌人列表
    /// </summary>
    private void OnQueryEngagementEnemys(BattleRoleEvents.QueryEngagementEnemys evt) {
        // 立即调用 CallBack 返回数据（同步）
        evt.CallBack.Invoke(engagementEnemys);
    }
}
```

**关键点**：
- 所有事件处理函数都是 `private`，组件不对外暴露任何 public 方法
- 查询事件通过调用 `evt.CallBack.Invoke(data)` 同步返回数据
- 在 OnAwake 中注册，在 OnClear 中注销

#### 第三步：BattleRole 调度事件

```csharp
// 文件：Assets/Script/GamePlay/Host/Modules/Role/BattleRole.cs

public partial class BattleRole : BattleSystemBase {
    
    // ──────────────────────────────────────
    // 组件装配（不保存引用）
    // ──────────────────────────────────────
    
    private void AddComponents() {
        AddComponent<BattleRoleEngageComponent>();  // ✅ 不保存返回值
        AddComponent<BattleRoleEnergyBattleComponent>();
        // ... 其他组件
    }
    
    // ──────────────────────────────────────
    // 公共接口（门面模式，对外保持兼容）
    // ──────────────────────────────────────
    
    /// <summary>
    /// 更新与目标角色的交战状态
    /// </summary>
    public void UpdateEngageEnemyState(bool isEngage, Role role) {
        // ✅ 通过事件调度
        Dispatcher(new BattleRoleEvents.UpdateEngageState {
            isEngage = isEngage,
            targetRole = role
        });
    }
    
    /// <summary>
    /// 获取当前正在交战的敌人列表
    /// </summary>
    public List<Role> myEngagementEnemys {
        get {
            List<Role> result = null;
            
            // ✅ 通过查询事件获取数据
            Dispatcher(new BattleRoleEvents.QueryEngagementEnemys {
                CallBack = (data) => result = data
            });
            
            return result ?? new List<Role>();
        }
    }
}
```

**关键点**：
- BattleRole 不保存任何组件引用
- 所有公共方法都转发为事件调度
- 查询操作通过 CallBack 同步获取数据（在同一帧内完成）
- Lambda 表达式捕获局部变量 `result` 来接收数据

### 5.5.3 查询事件的执行流程

```
┌─────────────────┐
│  调用端 (BattleRole)  │
│  发起查询          │
└────────┬────────┘
         │ 1. Dispatcher(Query { CallBack = ... })
         ▼
┌─────────────────┐
│  事件系统         │
│  分发到监听者     │
└────────┬────────┘
         │ 2. 触发注册的处理函数
         ▼
┌─────────────────┐
│  组件 (Component) │
│  evt.CallBack.Invoke(data)  │
└────────┬────────┘
         │ 3. 立即回调（同步）
         ▼
┌─────────────────┐
│  调用端 Lambda   │
│  result = data   │
└─────────────────┘
         │ 4. 完成赋值
         ▼
      返回 result
```

**执行时序**：
1. 调用端发送查询事件，事件中包含 CallBack 函数
2. 事件系统立即分发给注册的组件
3. 组件处理函数调用 `evt.CallBack.Invoke(data)`
4. 调用端的 Lambda 立即执行，捕获返回值
5. 整个过程在同一帧内完成，是同步的

### 5.5.4 实际案例参考（来自 Biubiubiu2）

#### 案例 1：SE_AI.Event_GetFollowList（查询跟随 AI 列表）

```csharp
// 事件定义（SE_AI.cs）
public struct Event_GetFollowList : GamePlayEvent.ISystemEvent {
    public Action<List<IAI>> CallBack;
}

// 组件端处理（ServerGPOAIMaster.cs）
private void OnGetFollowListCallBack(ISystemMsg body, SE_AI.Event_GetFollowList ent) {
    ent.CallBack.Invoke(followMonsterList);  // 直接返回列表
}

// 调用端（其他组件）
Dispatcher(new SE_AI.Event_GetFollowList {
    CallBack = (list) => {
        // 处理返回的 list
    }
});
```

#### 案例 2：SE_AI.Event_GetArmedCustomData（查询武装配置）

```csharp
// 事件定义（SE_AI.cs）
public struct Event_GetArmedCustomData : GamePlayEvent.ISystemEvent {
    public Action<bool, MonsterArmedCustom> CallBack;  // 多个参数
}

// 组件端处理（ServerSausageCharacterAIAttribute.cs）
private void GetArmedCustomCfgCallBack(ISystemMsg body, SE_AI.Event_GetArmedCustomData ent) {
    ent.CallBack.Invoke(isInit, customCfg);  // 返回两个参数
}

// 调用端（ServerSniperFireCycle.cs）
Dispatcher(new SE_AI.Event_GetArmedCustomData {
    CallBack = ResetAttackCountDown  // 直接传入方法引用
});

private void ResetAttackCountDown(bool isInit, MonsterArmedCustom cfg) {
    // 处理逻辑
}
```

### 5.5.5 修正要点总结

如果发现代码违反了事件驱动原则，需要：

1. **修改 BattleSystemBase.AddComponent**
   ```csharp
   // ❌ 当前（返回引用）
   protected T AddComponent<T>() where T : BattleComponent, new() { ... return component; }
   
   // ✅ 应该（不返回）
   protected void AddComponent<T>() where T : BattleComponent, new() { ... }
   ```

2. **移除组件引用**
   ```csharp
   // ❌ 删除所有类似代码
   private BattleRoleXxxComponent xxxComponent;
   xxxComponent = AddComponent<...>();
   ```

3. **补充事件定义**
   - 在 `BattleRoleEvents.cs` 中为每个组件定义命令和查询事件

4. **重写组件内部**
   - 所有 public 方法改为 private 事件处理函数
   - 在 OnAwake 中 Register 事件
   - 在 OnClear 中 Unregister 事件

5. **修改调用代码**
   - 将方法调用改为 `Dispatcher(new Event { ... })`
   - 属性访问改为查询事件 + CallBack

---

## 6. 组件写法范例

以 `BattleRoleSkinComponent` 为例，展示标准写法：

```csharp
// 文件：Assets/Script/GamePlay/Host/Modules/Role/Component/BattleRoleSkinComponent.cs

/// <summary>
/// 角色换装组件
/// 负责：皮肤初始化、皮肤更新、护甲时装切换
/// </summary>
public class BattleRoleSkinComponent : BattleRoleComponent {

    private bool isInitSkin = false;
    private string nowArmoredVestsSign;

    protected override void OnAwake() {
        // 注册事件监听（对应 Biubiubiu2 中 OnAwake 的语义）
    }

    protected override void OnStart() {
        // 触发初始皮肤状态
    }

    protected override void OnClear() {
        base.OnClear(); // 调用 BattleRoleComponent.OnClear 清空 role 引用
        isInitSkin = false;
        nowArmoredVestsSign = null;
    }

    public void SetInitSkin() { ... }
    public void SetSkinInfo(FashionData.FashionPart data) { ... }
    public void UpdateSkin(FashionData.FashionPart data) { ... }
    public void UpdateDownloadSkin(FashionData.FashionPart data) { ... }
}
```

---

## 6.5 改造后 BattleRole.cs 最终结构预览

```csharp
[SymbolObfus]
public partial class BattleRole : BattleSystemBase {
    
    // ═══════════════════════════════════════════
    // 第一部分：公共字段/属性（~180 行）
    // 这些被大量外部代码引用，暂不迁移
    // ═══════════════════════════════════════════
    public BattleRoleLogic MyRoleLogic { get; set; }
    public RoleNet MyRoleNet => MyRoleLogic.MyRoleNet;
    public RoleControl MyRoleControl;
    public WeaponControl UserWeapon;
    public HitPart UserHitPart;
    // ... 其余 public 字段保持不变 ...
    
    // ═══════════════════════════════════════════
    // 第二部分：Init() 骨架（~40 行）
    // ═══════════════════════════════════════════
    public void Init(Vector3 pos) {
        // 基础引用赋值（必须最先）
        mStartGame = MyRoleLogic.MyStartGame;
        gameWorld = mStartGame.MyGameWorld;
        MyTransform = transform;
        MyGameObj = gameObject;
        
        // 装配组件
        AddComponents();
        
        // 不可组件化的收尾
        RoleTransformPoint(pos);
    }
    
    // ═══════════════════════════════════════════
    // 第三部分：AddComponents()（~50 行）
    // ═══════════════════════════════════════════
    private void AddComponents() {
        // 来自 BattleRole.cs 的拆分
        AddComponent<BattleRoleSkinComponent>();
        AddComponent<BattleRoleFlyComponent>();
        AddComponent<BattleRoleShowComponent>();
        AddComponent<BattleRoleCarSyncComponent>();
        AddComponent<BattleRoleStateSyncComponent>();
        AddComponent<BattleRolePositionComponent>();
        AddComponent<BattleRoleEquipComponent>();
        AddComponent<BattleRoleSideAimComponent>();
        AddComponent<BattleRoleNetworkComponent>();
        AddComponent<BattleRoleBuffComponent>();
        AddComponent<BattleRoleCombatComponent>();
        AddComponent<BattleRoleEngageComponent>();
        
        // 条件装配
        if (WarData.IsEnergyBattleMode())
            AddComponent<BattleRoleEnergyBattleComponent>();
        
        // 来自 Role_XXX.cs partial 的迁移
        AddComponent<BattleRoleMoveComponent>();
        AddComponent<BattleRoleJumpComponent>();
        AddComponent<BattleRoleFireComponent>();
        // ... 按迁移进度逐步添加 ...
    }
    
    // ═══════════════════════════════════════════
    // 第四部分：Clear()（~30 行）
    // ═══════════════════════════════════════════
    public void Clear(bool removeAllSkin) {
        IsClear = true;
        ClearAllComponents();
        // 必须手动处理的
        MyRoleControl?.clear(removeAllSkin);
        gameWorld = null;
        mStartGame = null;
    }
    
    // ═══════════════════════════════════════════
    // 第五部分：TimeEvent()（~30 行）
    // ═══════════════════════════════════════════
    public void TimeEvent() {
        // 前置守卫（必须保留，不属于任何单一组件）
        if (IsClear || ...) return;
        
        // 驱动所有组件
        DriveComponents(TimeData.deltaTime);
    }
    
    // ═══════════════════════════════════════════
    // 第六部分：工具/快捷方法（~40 行）
    // ═══════════════════════════════════════════
    public void RoleTransformPoint(Vector3 point) { ... }
    public Vector3 GetRelativePos(Vector3 pos) { ... }
    private void OnDisable() { ... }
}
```

---

## 7. 迁移策略（渐进式，不破坏现有功能）

### 阶段划分

```
阶段 1（基础设施）   ──→  阶段 2（低风险组件）   ──→  阶段 3（高复杂组件）   ──→  阶段 4（清除 partial）
新增 IBattleSystem        迁移 BattleRole.cs 内      迁移坐标检测、状态同步       迁移所有 Role_XXX.cs
新增 BattleSystemBase     独立职责块                  迁移飞行跳伞、网络心跳       消除全部 partial 文件
新增 BattleComponent      验证生命周期正确性           BattleRole.cs 降至 ~400 行   最终只剩 System + Components
改造 BattleRole 继承链
```

**各阶段 BattleRole.cs 行数预期：**

| 阶段 | 内容 | BattleRole.cs 预估行数 |
|------|------|----------------------|
| 阶段 0（当前） | 未改动 | 4570 行 |
| 阶段 1（基础设施） | 新增 5 个基础文件（IBattleSystem / BattleSystemBase / BattleComponent / BattleRoleComponent / BattleRoleEvents），改继承链，不动业务 | 4570 行（不变） |
| 阶段 2（低风险拆分） | 从 BattleRole.cs 拆出 13 个组件 | ~400 行 |
| 阶段 3（partial 迁移-小文件） | 迁移 <500 行的 partial 文件 | ~400 行（不变） |
| 阶段 4（partial 迁移-大文件） | 迁移 >500 行的 partial 文件 | ~400 行（不变） |
| **最终** | 所有 partial 消除 | **~400 行** |

### 阶段 1：基础设施（不改任何现有逻辑）

1. 新建 `IBattleSystem.cs`（系统接口，含事件系统）
2. 新建 `BattleSystemBase.cs`（组件管理 + 事件总线）
3. 新建 `BattleComponent.cs`（通用组件基类，含事件快捷方法）
4. 新建 `BattleRoleComponent.cs`（角色组件基类）
5. 新建 `BattleRoleEvents.cs`（事件定义集合，初始为空壳/示例）
6. `BattleRole` 改为继承 `BattleSystemBase`（原 `MonoBehaviour` 能力由基类保留）
7. **此阶段不迁移任何逻辑，只加骨架，现有业务代码完全不动**

### 阶段 2：BattleRole.cs 内的逻辑拆分（低风险，依赖少）

按顺序迁移 BattleRole.cs 内的独立职责块：
- `BattleRoleSkinComponent`（换装，依赖少，逻辑独立）
- `BattleRoleEquipComponent`（装备显示，读状态为主）
- `BattleRoleEnergyBattleComponent`（模式专属，有 `#region` 边界清晰）
- `BattleRoleEngageComponent`（交战统计，完全独立）
- `BattleRoleBuffComponent`（Buff 上传，接口清晰）
- `BattleRolePositionComponent`、`BattleRoleFlyComponent`、`BattleRoleShowComponent` 等

每迁移一个后，在 `AddComponents()` 中加一行 `AddComponent<T>()`，对应逻辑从 `BattleRole.cs` 中删除。

### 阶段 3：高复杂逻辑拆分

- `BattleRoleNetworkComponent`（心跳/Ping/RTT，需保证消息注册/反注册正确）
- `BattleRoleStateSyncComponent`（跨多个状态机，需梳理依赖顺序）

### 阶段 4：Role_XXX.cs partial 文件全部迁移（最终清除 partial）

按文件大小从小到大推进，降低每次改动风险：

**小文件优先（<100 行，直接合并或转换）：**
`Role_MovePlatform` → `BattleRoleMoveComponent`
`Role_Network` → `BattleRoleNetworkComponent`
`Role_CheckBombArea` → `BattleRolePositionComponent`
`Role_ATEvent` → `BattleRoleStateComponent`
`Role_BladeBallMode` → `BattleRoleBladeBallModeComponent`
`Role_Robot` → `BattleRoleRobotComponent`

**中文件（100~500 行，直接转组件）：**
`Role_Dragon` / `Role_Sit` / `Role_Mark` / `Role_CheckSceneItem`
`Role_HideSeek` / `Role_OnlyUp` / `Role_Reload` / `Role_DefusalMode`
`Role_SneakSand` / `Role_Hurt` / `Role_Dance` / `Role_Sliding`
`Role_WolfParty` / `Role_SqParachute`

**大文件（>500 行，内部再拆子组件）：**
`Role_UprearRole` / `Role_Jump` → 单组件
`Role_Camera` / `Role_Sound` → 单组件
`Role_State` / `Role_Collider` → 单组件
`Role_Weapon` → 单组件
`Role_Animation`（1143行）→ 拆为基础动画 + 特殊状态动画
`Role_Move`（1525行）→ 拆为移动 / AddForce / 姿态控制 / BoxingTrampolineFly
`Role_Weapon`（1334行）→ 单组件
`Role_Fire`（1661行）→ 拆为主流程 / 暗器 / 榴弹 / 蓄力射击 / 预输入
`Role_Item`（2012行）→ 拆为道具使用 / 展示道具
`Role_HitPart`（2413行）→ 拆为主流程 / 魔刀 / 重击 / AI攻击 / 近战模型 / 预输入

---

## 8. 不迁移进组件的内容

以下内容建议**保留在 `BattleRole.cs` 主文件**，不做迁移：

| 内容 | 原因 |
|------|------|
| `public` 字段引用（`MyRoleControl`、`MyRoleSkill` 等） | 大量外部代码直接访问，迁移代价极高 |
| `Init(Vector3 pos)` / `Clear()` 主框架 | 容器本身的装配入口 |
| `TimeEvent()` 主调度框架 | 保留为驱动入口，内部调用 `DriveComponents()` |
| `MyTransform` / `MyGameObj` 等基础缓存 | 全局共享，各组件通过 `role.MyTransform` 访问 |
| Unity 回调（`OnDisable` 等） | MonoBehaviour 生命周期必须在主类 |

---

## 9. 预期收益

| 指标 | 改造前 | 改造后 |
|------|--------|--------|
| `BattleRole.cs` 行数 | 4570 行 | ~400 行（纯装配 + 公共字段） |
| `Role_XXX.cs` partial 文件 | 32 个，共 17901 行 | 全部消除 |
| 总代码量变化 | 22471 行堆在 BattleRole 体系 | 拆为 50+ 个组件，单文件 ≤500 行 |
| 新增模式时改动范围 | 全局 `if (WarData.IsXxxMode)` 散落 | 只需新增组件，在 `AddComponents()` 条件装配 |
| AI 生成单组件代码 | 需要加载 5000+ 行上下文 | 单文件 300~500 行，上下文独立 |
| 框架复用 | 无 | `BattleSystemBase` 可供载具/道具等所有系统复用 |
| 迁移至 Biubiubiu2 成本 | 极高（需整体重写） | 极低（换基类即可，业务代码不动） |

---

## 10. 文件结构预览（改造后最终形态）

**改造前（BattleRole 体系）：**
```
Role/
├── BattleRole.cs          4570 行  ← 巨型主文件
├── Role_HitPart.cs        2180 行
├── Role_Item.cs           1747 行
├── Role_Fire.cs           1423 行
├── Role_Move.cs           1342 行
├── ...（共 32 个 partial 文件，合计 17901 行）
└── 总计：~22471 行，全部是 partial class BattleRole
```

**改造后（最终形态）：**
```
GamePlay/Host/Modules/
├── IBattleSystem.cs                         ← 系统接口（含事件系统）
├── BattleSystemBase.cs                      ← 组件管理基类 + 事件总线
├── BattleComponent.cs                       ← 通用组件基类（含事件快捷方法）
└── Role/
    ├── BattleRole.cs                        ← ~400 行，公共字段 + 装配逻辑
    ├── BattleRoleComponent.cs               ← 角色组件基类
    ├── BattleRoleEvents.cs                  ← 事件定义集合（对标 SE_Character/CE_Character）
    └── Component/
        │
        │  # 来自 BattleRole.cs 的拆分
        ├── BattleRoleSkinComponent.cs
        ├── BattleRoleFlyComponent.cs
        ├── BattleRoleShowComponent.cs
        ├── BattleRoleCarSyncComponent.cs
        ├── BattleRoleStateSyncComponent.cs
        ├── BattleRolePositionComponent.cs
        ├── BattleRoleEquipComponent.cs
        ├── BattleRoleSideAimComponent.cs
        ├── BattleRoleNetworkComponent.cs
        ├── BattleRoleBuffComponent.cs
        ├── BattleRoleCombatComponent.cs
        ├── BattleRoleEnergyBattleComponent.cs
        ├── BattleRoleEngageComponent.cs
        │
        │  # 来自 Role_XXX.cs 的迁移
        ├── BattleRoleHitPartComponent.cs        （主流程）
        ├── BattleRoleHitPartMachetteComponent.cs（魔刀）
        ├── BattleRoleHitPartHeavyComponent.cs   （重击）
        ├── BattleRoleHitPartAIComponent.cs      （AI攻击）
        ├── BattleRoleHitPartMeleeModelComponent.cs（近战模型）
        ├── BattleRoleHitPartPreInputComponent.cs（预输入）
        ├── BattleRoleItemComponent.cs
        ├── BattleRoleItemShowComponent.cs
        ├── BattleRoleFireComponent.cs
        ├── BattleRoleFireDarkWeaponComponent.cs （暗器）
        ├── BattleRoleFireGrenadeComponent.cs    （榴弹）
        ├── BattleRoleFireChargeComponent.cs     （蓄力射击）
        ├── BattleRoleMoveComponent.cs
        ├── BattleRoleMoveForceComponent.cs      （AddForce）
        ├── BattleRoleMovePostureComponent.cs    （姿态控制）
        ├── BattleRoleWeaponComponent.cs
        ├── BattleRoleStateComponent.cs
        ├── BattleRoleColliderComponent.cs
        ├── BattleRoleAnimationComponent.cs
        ├── BattleRoleAnimationSpecialComponent.cs
        ├── BattleRoleSoundComponent.cs
        ├── BattleRoleCameraComponent.cs
        ├── BattleRoleJumpComponent.cs
        ├── BattleRoleUprearComponent.cs
        ├── BattleRoleSqParachuteComponent.cs
        ├── BattleRoleWolfPartyComponent.cs
        ├── BattleRoleSlidingComponent.cs
        ├── BattleRoleDanceComponent.cs
        ├── BattleRoleHurtComponent.cs
        ├── BattleRoleSneakSandComponent.cs
        ├── BattleRoleDefusalModeComponent.cs
        ├── BattleRoleReloadComponent.cs
        ├── BattleRoleHideSeekComponent.cs
        ├── BattleRoleOnlyUpComponent.cs
        ├── BattleRoleDragonComponent.cs
        ├── BattleRoleSitComponent.cs
        ├── BattleRoleMarkComponent.cs
        ├── BattleRoleCheckSceneItemComponent.cs
        ├── BattleRoleRobotComponent.cs
        └── BattleRoleBladeBallModeComponent.cs
```

---

## 11. 风险说明

| 风险点 | 说明 | 缓解方式 |
|--------|------|---------|
| 现有 `public` 字段外部访问 | 外部代码通过 `role.MyRoleSkill` 等直接访问，组件内部数据不对外暴露 | 组件内的对外数据仍通过 `BattleRole` 上的属性暴露；public 字段本阶段保留在 BattleRole.cs |
| `BattleRole` 改继承链 | 原继承 `MonoBehaviour`，改为继承 `BattleSystemBase` 需确认无其他隐式依赖 | `BattleSystemBase` 同样继承 `MonoBehaviour`，Unity 生命周期不受影响 |
| TimeEvent 驱动链改变 | 原来 `TimeEvent()` 直接调用各方法，改为组件 Update 后执行顺序需保持一致 | 阶段 1 先建立 `DriveComponents()`，阶段 2 再逐步迁移 |
| **TimeEvent 执行顺序**（新增） | 原 TimeEvent() 内部各方法调用有严格顺序依赖（如 RoleShowEvent 必须在 CheckRoleShow 之前） | 组件 AddUpdate 的注册顺序即执行顺序，迁移时保持 AddComponents 顺序与原调用顺序一致 |
| partial 跨文件字段依赖 | 部分 `Role_XXX.cs` 中的字段被其他 partial 文件直接读写 | 迁移时梳理字段归属，共享字段保留在 BattleRole.cs，组件通过 `role.XXX` 访问 |
| **条件装配时机**（新增） | 部分逻辑只在特定模式下存在（如 EnergyBattle） | AddComponents 中用 if 条件装配，与二代 CharacterLocalSystem 模式一致 |
| 大文件内部拆分边界 | `Role_HitPart.cs`（2180行）、`Role_Fire.cs`（1423行）内部 #region 虽有分区，但方法间仍有调用 | 优先拆纯数据域和工具方法，主流程保留在主组件，子组件通过事件/接口通信 |
| Init 顺序依赖 | 部分初始化有先后顺序依赖 | `AddComponents()` 中保持顺序，每个组件的 `OnAwake` 不调用其他组件方法 |
