# 1 代架构通用模式基础框架（CommonMode）制作规范

> **适用范围**：CommonMode 通用模式框架 — 新增 Control / 扩展购买系统 / 定制统计系统 / 新建继承模式
> **不适用**：模式级框架（ClientModeManager/ServerModeManager） → 归 [[模式制作]]；具体子模式 → 归各自制作文档
> **参考实现**：mode-common（38 文件，★★ 框架级，被多个模式继承）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **被继承者**：ClassicMode · TeamMode · DefusalMode · BullFighting · CustomRoom 等

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientCommonManager (Client 端通用模式管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/CommonMode/ClientCommonManager.cs
  │  继承: ClientModeManager
  │  职责: 加载 MVP 配置、战斗数据同步、场景加载管理
  │  ★ 框架类 — 不直接使用，由子模式继承
  │
  ├── ClientCommonUtil (客户端工具类)
  │     职责: 通用辅助方法
  │
  ├── 标准 Stage 层（5 阶段，可被子模式扩展）
  │     ClientCommonReadyStage → ClientCommonBornStage → ClientCommonBattleStage
  │     → ClientCommonRoundOverStage → ClientCommonOverStage
  │
  └── ClientCommonModeData
        职责: 客户端通用数据

ServerCommonManager (Server 端通用模式管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/CommonMode/ServerCommonManager.cs
  │  继承: ServerModeManager
  │  职责: 状态机管理、出生点管理、通用控制
  │  ★ 框架类 — 被 DefusalMode, TeamMode, BladeBall 等继承
  │
  ├── 状态机框架
  │     ControlMachine<ServerCommonManager>
  │       ├── ControlBase<T> (通用控制基类)
  │       │     抽象: Init() / OnUpdate() / End()
  │       ├── ServerCommonBuyWeaponControl (购买武器控制)
  │       └── ServerCommonUtilControl (工具控制)
  │
  ├── 标准 Stage 层（5 阶段）
  │     ServerCommonReadyStage → ServerCommonBornStage → ServerCommonBattleStage
  │     → ServerCommonRoundOverStage → ServerCommonOverStage
  │
  ├── ServerCommonStatisticsControl (统计系统)
  │     个人统计: Dictionary<int, StatisticsPersonalData>
  │     轰炸统计: StatisticsBlastBombData
  │     事件: OnStatisticsKillData / BodyData / DamageData / ShootData / BlastBombInstallData
  │
  └── ServerCommonUtil (服务端工具类)

状态机架构 ★
  │  StateBase (状态基类)
  │  IState (状态接口)
  │  StateMachine<T>
  │    方法: AddState() / GetState() / ChangeState()
  │
  └── ControlMachine<T>
        管理多个 ControlBase 实例
        方法: AddControl() / GetControl<T>() / OnUpdate()

数据系统（自动同步 ★）
  │  BattleCommonDynamicData (Serializable, 自动同步)
  │    字段: Round / ReadyTiming / BattleTiming / GameTiming
  │          GameWinTeam / RoundWinTeam / BattleCommonTeamInfos
  │    方法: TriggerAutoSend()
  │
  ├── BattleCommonStaticData (静态数据)
  │
  └── ServerCommonModeData / ClientCommonModeData

专属 Mono
    BlastBombAreaMono (轰炸区域渲染/碰撞)

配置
    SOCommonModeBattleConfigData (战斗配置)
    SOCommonModeMvpConfigData (MVP 配置)
    路径: Assets/ToBundle/ScriptableObject/CommonMode/
```

### 1.2 继承关系图

```
ClientModeManager                       ServerModeManager
      │                                       │
ClientCommonManager ★                  ServerCommonManager ★
      │                                       │
      ├── ClientDefusalModeMgr         ├── ServerDefusalModeMgr
      ├── ClientTeamModeMgr            ├── ServerTeamModeMgr  
      ├── ClientBladeBallModeMgr       ├── ServerBladeBallModeMgr
      ├── ClientClassicModeMgr         ├── ServerClassicModeMgr
      └── ... 其他继承模式              └── ... 其他继承模式

⚠️ 注意: 并非所有模式都继承 CommonManager
   - GoldDash → 直接继承 ClientModeManager
   - TurnBased → 直接继承 ClientModeManager
   - UltraFight → 直接继承 ClientModeManager
```

### 1.3 标准 5 阶段流转

```
CommonMode 标准 5 阶段（子模式可添加/替换阶段）：

Ready (准备阶段)
  │  ReadyTiming 倒计时
  │  等待玩家就绪
  ↓
Born (出生阶段)
  │  分配出生点（按队伍/阵营）
  │  初始化角色状态
  ↓
Battle (战斗阶段)
  │  BattleTiming 倒计时
  │  ControlMachine 驱动各 Control
  │  统计系统收集数据
  ↓
RoundOver (回合结束)
  │  计算 RoundWinTeam
  │  展示回合数据
  │  Round++ 
  │  判定：未达最大回合 → Ready
  ↓
Over (游戏结束)
    计算 GameWinTeam
    MVP 展示
    数据上报

子模式扩展方式：
  DefusalMode: +ShopStage(Born后) +WinWaitStage(Battle后)
  TeamMode: +RunningStage(替换Battle)
  BladeBall: +WaitStage(RoundOver后)
```

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **战斗配置** | `Assets/ToBundle/ScriptableObject/CommonMode/SOCommonModeBattleConfigData.asset` | Resources/AB | Init() |
| **MVP 配置** | `Assets/ToBundle/ScriptableObject/CommonMode/SOCommonModeMvpConfigData.asset` | Resources/AB | Over |
| **轰炸区域** | BlastBombAreaMono Prefab | 场景内 | Battle |

### 1.5 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 上层基类
- **BattleCommonDynamicData** 已有字段 — 仅可扩展，不可改名/删除
- **StateBase / IState / StateMachine** — 状态机核心，任何修改影响所有继承模式

---

## 二、新建/扩展 Checklist

### Phase 1：新建继承 CommonMode 的子模式

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Client/Modules/Mode/{ModeName}/Client{ModeName}Mgr.cs` | 新建 | 继承 `ClientCommonManager` |
| 2 | `Server/Modules/Mode/{ModeName}/Server{ModeName}Mgr.cs` | 新建 | 继承 `ServerCommonManager` |
| 3 | `Host/Mode/GameMode.cs` | 修改 | 新增枚举值 |
| 4 | `ClientModeFactory.cs` | 修改 | 注册新模式 |
| 5 | `ServerModeFactory.cs` | 修改 | 注册新模式 |

### Phase 2：新增 Control

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | `Server/Modules/Mode/CommonMode/Control/ServerCommon{ControlName}Control.cs` | 新建 | 继承 `ControlBase<ServerCommonManager>` |
| 7 | `ServerCommonManager.cs` | 修改 | ControlMachine.AddControl() 注册 |

### Phase 3：扩展购买系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `ServerCommonBuyWeaponControl.cs` | 修改 | 新增武器/道具/装备类型 |
| 9 | 对应客户端购买 UI | 修改 | 展示新商品 |

### Phase 4：扩展统计系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 10 | `ServerCommonStatisticsControl.cs` | 修改 | 新增统计事件类型 |
| 11 | `StatisticsPersonalData` | 修改 | 新增统计字段 |

### Phase 5：自定义 Stage（子模式）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 12 | `Client{ModeName}{StageName}Stage.cs` | 新建 | 继承通用 Stage 或新建 |
| 13 | `Server{ModeName}{StageName}Stage.cs` | 新建 | 服务端 Stage |
| 14 | 对应 Mgr.InitStage() | 修改 | 注册新 Stage |

---

## 三、配置文件详解

### 3.1 SOCommonModeBattleConfigData

**路径**：`Assets/ToBundle/ScriptableObject/CommonMode/SOCommonModeBattleConfigData.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `readyTime` | float | 准备阶段时长 |
| `battleTime` | float | 战斗阶段时长 |
| `roundCount` | int | 总回合数 |
| `roundOverTime` | float | 回合结束展示时长 |
| `teamCount` | int | 队伍数量 |
| `teamSize` | int | 每队人数 |
| `enableBuyWeapon` | bool | 是否启用购买系统 |
| `startMoney` | int | 初始金钱 |
| `killMoney` | int | 击杀奖金 |
| `roundWinMoney` | int | 回合胜利奖金 |

### 3.2 SOCommonModeMvpConfigData

| 字段 | 类型 | 说明 |
|------|------|------|
| `mvpConditions` | MvpCondition[] | MVP 评选条件列表 |
| `mvpAnimDuration` | float | MVP 展示动画时长 |
| `mvpCameraConfig` | CameraConfig | MVP 展示相机配置 |

### 3.3 BattleCommonDynamicData（自动同步 ★）

```csharp
// ★ 此类标记为 Serializable，修改字段会自动触发网络同步
[Serializable]
public class BattleCommonDynamicData {
    public int Round;                      // 当前回合数
    public float ReadyTiming;              // 准备阶段剩余时间
    public float BattleTiming;             // 战斗阶段剩余时间  
    public float GameTiming;               // 总游戏时间
    public int GameWinTeam;                // 最终获胜队伍
    public int RoundWinTeam;               // 本回合获胜队伍
    public BattleCommonTeamInfo[] BattleCommonTeamInfos;  // 队伍信息数组
    
    // ★ 触发自动同步（修改字段后必须调用）
    public void TriggerAutoSend() {
        // 标记数据脏，下一帧同步给所有客户端
        isDirty = true;
    }
}

// 队伍信息
[Serializable]
public class BattleCommonTeamInfo {
    public int TeamId;
    public int Score;
    public int RoundWins;
    public int PlayerCount;
}
```

### 3.4 状态机框架

```csharp
// 控制基类
public abstract class ControlBase<T> where T : ServerCommonManager {
    protected T mgr;
    
    public abstract void Init();
    public abstract void OnUpdate(float deltaTime);
    public abstract void End();
}

// 控制机器（管理多个 Control）
public class ControlMachine<T> where T : ServerCommonManager {
    private List<ControlBase<T>> controls = new List<ControlBase<T>>();
    
    public void AddControl(ControlBase<T> control) {
        controls.Add(control);
        control.Init();
    }
    
    public C GetControl<C>() where C : ControlBase<T> {
        return controls.OfType<C>().FirstOrDefault();
    }
    
    public void OnUpdate(float deltaTime) {
        foreach (var control in controls)
            control.OnUpdate(deltaTime);
    }
}

// 状态基类
public abstract class StateBase {
    public abstract void OnEnter();
    public abstract void OnUpdate(float deltaTime);
    public abstract void OnExit();
}

// 状态机
public class StateMachine<T> {
    private Dictionary<int, StateBase> states;
    private StateBase currentState;
    
    public void AddState(int id, StateBase state) { states[id] = state; }
    public StateBase GetState(int id) { return states[id]; }
    
    public void ChangeState(int id) {
        currentState?.OnExit();
        currentState = states[id];
        currentState?.OnEnter();
    }
}
```

---

## 四、关键代码修改点

### 4.1 新建继承模式（完整模板）

```csharp
// === Client 端 ===
public class ClientMyNewModeMgr : ClientCommonManager {
    
    public override void Init() {
        base.Init();  // ★ 必须调用 base — 加载 CommonMode 配置
        
        // 加载子模式自有配置
        myData = LoadSOConfig<SOMyNewModeData>();
    }
    
    protected override void InitStage() {
        // 可复用 Common 的 Stage，也可替换
        AddStage(new ClientCommonReadyStage());    // 复用
        AddStage(new ClientCommonBornStage());     // 复用
        AddStage(new ClientMyNewModeBattleStage()); // 替换
        AddStage(new ClientCommonRoundOverStage()); // 复用
        AddStage(new ClientCommonOverStage());     // 复用
    }
}

// === Server 端 ===
public class ServerMyNewModeMgr : ServerCommonManager {
    
    public override void Init() {
        base.Init();  // ★ 加载 CommonMode 配置 + 初始化 ControlMachine
        
        // 添加自有 Control
        controlMachine.AddControl(new ServerMyNewModeSpecialControl());
        
        // 注册自有 Logic
        AddLogic(new ServerMyNewModeCustomLogic());
    }
}
```

### 4.2 新建 Control

```csharp
public class ServerCommonMyNewControl : ControlBase<ServerCommonManager> {
    
    public override void Init() {
        // 初始化自定义控制逻辑
    }
    
    public override void OnUpdate(float deltaTime) {
        // 每帧更新
        // 可通过 mgr 访问 ServerCommonManager 的所有方法和数据
    }
    
    public override void End() {
        // 清理
    }
}

// 注册
// 在 ServerCommonManager.Init() 或子类 Init() 中：
controlMachine.AddControl(new ServerCommonMyNewControl());
```

### 4.3 购买系统扩展

**文件**：`ServerCommonBuyWeaponControl.cs`

```csharp
public class ServerCommonBuyWeaponControl : ControlBase<ServerCommonManager> {
    
    // 处理购买请求
    public void OnBuyRequest(int roleId, int itemId, int itemType) {
        var role = mgr.GetRole(roleId);
        int price = GetPrice(itemId);
        
        if (role.Money < price) {
            SendBuyResult(roleId, BuyResult.NotEnoughMoney);
            return;
        }
        
        role.Money -= price;
        
        switch (itemType) {
            case ItemType.Weapon:
                role.GiveWeapon(itemId);
                break;
            case ItemType.Equipment:
                role.GiveEquipment(itemId);
                break;
            case ItemType.Consumable:
                role.GiveConsumable(itemId);
                break;
        }
        
        SendBuyResult(roleId, BuyResult.Success);
    }
    
    // 回合开始时重置金钱
    public void OnRoundStart() {
        foreach (var role in mgr.GetAllRoles()) {
            role.Money += mgr.DynamicData.RoundWinTeam == role.TeamId 
                ? mgr.Config.roundWinMoney 
                : 0;
        }
    }
}
```

### 4.4 统计系统扩展

```csharp
// ServerCommonStatisticsControl 中的事件注册
public override void Init() {
    // 注册统计事件
    RegisterEvent(EventId.OnKill, (data) => {
        var killData = (KillEventData)data;
        UpdatePersonalStat(killData.killerId, s => s.Kills++);
        UpdatePersonalStat(killData.victimId, s => s.Deaths++);
    });
    
    RegisterEvent(EventId.OnDamage, (data) => {
        var dmgData = (DamageEventData)data;
        UpdatePersonalStat(dmgData.attackerId, s => s.TotalDamage += dmgData.damage);
    });
    
    RegisterEvent(EventId.OnShoot, (data) => {
        var shootData = (ShootEventData)data;
        UpdatePersonalStat(shootData.roleId, s => s.ShotsFired++);
    });
    
    // ★ 新增统计维度示例
    RegisterEvent(EventId.OnHeadshot, (data) => {
        var hsData = (HeadshotEventData)data;
        UpdatePersonalStat(hsData.roleId, s => s.Headshots++);
    });
}
```

---

## 五、常见问题与踩坑记录

### 5.1 子模式未调用 base.Init()

**现象**：子模式启动后 ControlMachine 为 null，购买系统不工作

**根因**：子模式 Init() 中未调用 `base.Init()`，导致 CommonMode 的初始化未执行

**解决方案**：
1. 子模式 Init() 第一行必须是 `base.Init();`
2. 代码审查时重点检查继承模式的 Init() 链

### 5.2 BattleCommonDynamicData 修改后未 TriggerAutoSend

**现象**：服务端修改了数据，但客户端没有更新

**根因**：修改 DynamicData 字段后忘记调用 `TriggerAutoSend()`

**解决方案**：
1. 每次修改 DynamicData 字段后必须调用 `TriggerAutoSend()`
2. 或封装 setter 方法，内部自动触发同步：
```csharp
public void SetRound(int round) {
    dynamicData.Round = round;
    dynamicData.TriggerAutoSend();
}
```

### 5.3 Control 与 Logic 职责混淆

**现象**：开发者不知道新功能应该做成 Control 还是 Logic

**根因**：CommonMode 同时有 ControlMachine（Control 模式）和 AddLogic（Logic 模式），容易混淆

**解决方案**：
- **Control** = CommonMode 层面的通用功能（购买/统计/工具），被所有继承模式共享
- **Logic** = 子模式特有功能（特殊规则/独特玩法），仅在该模式使用
- 经验法则：如果功能只有 1 个模式用 → Logic；多个模式共用 → Control

### 5.4 Stage 替换后丢失通用逻辑

**现象**：子模式用自定义 Stage 替换 CommonBattleStage 后，通用战斗逻辑丢失

**根因**：自定义 Stage 未继承 CommonBattleStage，而是直接继承 StageBase

**解决方案**：
1. 自定义 Stage 继承对应的 Common Stage：
```csharp
public class ClientMyModeBattleStage : ClientCommonBattleStage {
    public override void OnEnter() {
        base.OnEnter();  // 保留通用逻辑
        // 添加自定义逻辑
    }
}
```
2. 如果确实不需要通用逻辑，明确文档说明

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] ControlBase / ControlMachine 泛型编译正常
- [ ] 所有继承模式编译不受影响

### 6.2 配置

- [ ] SOCommonModeBattleConfigData 参数合理
- [ ] SOCommonModeMvpConfigData MVP 条件合理

### 6.3 运行时

- [ ] 标准 5 阶段流转正常（Ready→Born→Battle→RoundOver→Over）
- [ ] ControlMachine 正确驱动所有 Control
- [ ] 购买系统正常（金钱扣除/商品发放/回合重置）
- [ ] 统计系统正确收集数据
- [ ] BattleCommonDynamicData 自动同步正常
- [ ] MVP 计算和展示正确

### 6.4 兼容性

- [ ] DefusalMode / TeamMode / BladeBall 等继承模式正常
- [ ] 新增 Control 不影响已有 Control
- [ ] Stage 替换不破坏通用流程
- [ ] BlastBombAreaMono 渲染/碰撞正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-common]] · [[DefusalMode制作]] · [[TeamMode制作]]
