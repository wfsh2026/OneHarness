# 1 代架构自定义房间阵营对抗（CustomRoomCamp）制作规范

> **适用范围**：CustomRoomCamp 自定义房间阵营对抗模式 — 新增阵营规则 / 扩展自定义设置 / 新增奖励逻辑
> **不适用**：通用模式框架 → 归 [[模式制作]]；标准 TeamMode → 归 [[TeamMode制作]]
> **参考实现**：mode-customroomcamp（13 文件，★ 最简化设计，典型极简模式参考）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage 基类 / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientCustomRoomCampMgr (Client 端自定义房间主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/ClientCustomRoomCampMgr.cs
  │  继承: ClientModeManager
  │  职责: 自定义房间客户端入口，最简 Stage 管理
  │
  ├── Stage 层（仅 3 个，最简设计）
  │     ClientCustomRoomCampBornStage
  │     ClientCustomRoomCampBattleStage
  │     ClientCustomRoomCampOverStage
  │
  └── ClientCustomRoomCampData
        职责: 客户端数据（含 RoleNumData 阵营人数信息）

ServerCustomRoomCampMgr (Server 端自定义房间主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/ServerCustomRoomCampMgr.cs
  │  继承: ServerModeManager
  │  职责: 自定义房间服务端入口，阵营管理，胜负判定
  │
  ├── ServerCustomRoomCampRoleLogic
  │     职责: 角色阵营分配，GetUniteRoleNum() 获取各阵营人数
  │
  ├── ServerCustomRoomCampAwardLogic
  │     职责: 奖励结算
  │
  └── ServerCustomRoomCampNsqDataLogic
        职责: NSQ 数据上报

ServerCustomRoomCampData
  │  职责: 服务端运行时数据

SOCustomRoomCampData (ScriptableObject)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/CustomRoomCamp/
  │  职责: 模式配置
```

### 1.2 Stage 阶段流转

```
3 阶段制（最简化设计）：

Born (出生阶段)
  │  所有玩家按阵营在出生点生成
  │  触发: OnEnterBattle() 回调
  ↓
Battle (战斗阶段)
  │  自由对战，按自定义房间设定的规则进行
  │  支持:
  │    ├── 阵营分组（2+ 阵营）
  │    ├── 玩家动态加入 (AddRole/OnRoleAdd)
  │    └── 重登处理 (OnReLogin)
  ↓
Over (游戏结束)
    结算数据，返回房间
```

### 1.3 继承与复用关系

```
ClientModeManager (框架基类)
    │
    ├── ClientCustomRoomCampMgr (最简实现)
    │     特点：无 Logic 模块注册（所有逻辑在 Stage 中）
    │
    └── 其他 ModeMgr (标准实现，有 Logic 注册)

ServerModeManager (框架基类)
    │
    └── ServerCustomRoomCampMgr
          特点：仅 3 个 Logic（Role/Award/Nsq）
          极简设计，适合玩家自由对战场景
```

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/CustomRoomCamp/*.asset` | Resources/AB | Mgr.Init() |
| **房间设置 UI** | `Assets/ToBundle/UGUI/Windows/CustomRoom/` | UIManager.Open() | 房间创建时 |
| **战斗 HUD** | 复用通用 War UI | UIManager | BattleStage.OnEnter() |
| **自定义规则配置** | `Assets/ToBundle/Config/Txt/CustomRoom.txt` | ConfigManager | 初始化 |

### 1.5 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 已有枚举值 `CampCustomized=42` — 不可修改
- **CustomRoom.txt** 的已有字段 — 仅可追加新字段

---

## 二、新建/扩展 Checklist

### Phase 1：模式注册（已完成，扩展时跳过）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Host/Mode/GameMode.cs` | 已有 | `CampCustomized = 42` |
| 2 | `ClientModeFactory.cs` | 已有 | `AddFeature<ClientCustomRoomCampMgr>()` |
| 3 | `ServerModeFactory.cs` | 已有 | `AddFeature<ServerCustomRoomCampMgr>()` |

### Phase 2：新增阵营规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | `ServerCustomRoomCampRoleLogic.cs` | 修改 | 新增阵营分配逻辑（如 3 阵营、随机分配） |
| 5 | `ClientCustomRoomCampData.cs` | 修改 | 新增阵营数据字段 |
| 6 | `SOCustomRoomCampData.asset` | 修改 | 新增阵营配置参数 |

### Phase 3：新增 Logic 模块（如需要）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 7 | `Server/Modules/Mode/CustomRoomCamp/Server{LogicName}Logic.cs` | 新建 | 服务端 Logic |
| 8 | `Client/Modules/Mode/CustomRoomCamp/Client{LogicName}Logic.cs` | 新建 | 客户端 Logic（如需要） |
| 9 | `ServerCustomRoomCampMgr.cs` | 修改 | Init() 中 AddLogic() |

### Phase 4：扩展自定义设置

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 10 | `CustomRoom.txt` | 修改 | 追加新配置字段 |
| 11 | 对应 Config 类 | 修改 | 解析新字段 |
| 12 | 房间设置 UI | 修改 | 新增设置选项 |

### Phase 5：新增胜利条件

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 13 | `ServerCustomRoomCampMgr.cs` | 修改 | Battle Stage 中新增胜利判定条件 |
| 14 | `ServerCustomRoomCampAwardLogic.cs` | 修改 | 新胜利条件的奖励 |
| 15 | `ClientCustomRoomCampOverStage.cs` | 修改 | 新结算显示 |

---

## 三、配置文件详解

### 3.1 GameMode 枚举

```csharp
public enum GameMode {
    // ...
    CampCustomized = 42,  // 自定义房间阵营对抗
    // ...
}
```

### 3.2 SOCustomRoomCampData

**路径**：`Assets/ToBundle/ScriptableObject/Mode/CustomRoomCamp/SOCustomRoomCampData.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `maxTeamCount` | int | 最大阵营数（默认 2） |
| `maxPlayerPerTeam` | int | 每阵营最大人数 |
| `battleTime` | float | 战斗时长（秒） |
| `respawnEnabled` | bool | 是否允许重生 |
| `respawnTime` | float | 重生等待时间 |
| `friendlyFire` | bool | 是否开启友军伤害 |

### 3.3 CustomRoom.txt 配置

**路径**：`Assets/ToBundle/Config/Txt/CustomRoom.txt`

```
# 自定义房间规则配置
# 格式: 字段名\t值
MaxPlayer	16
MinPlayer	2
TeamMode	camp        # camp=阵营对抗
MapPool	    map1,map2   # 可用地图列表
WeaponRule	all         # all=全武器, pistol=仅手枪
```

### 3.4 客户端/服务端数据类

```csharp
// ClientCustomRoomCampData
public class ClientCustomRoomCampData {
    public SOCustomRoomCampData Config;
    public RoleNumData roleNumData;  // 各阵营人数
    
    public struct RoleNumData {
        public int team1Count;
        public int team2Count;
        // 按需扩展
    }
}

// ServerCustomRoomCampData
public class ServerCustomRoomCampData {
    public Dictionary<int, List<BattleRoleLogic>> teamRoles;  // 阵营 → 角色列表
    public float battleTimer;
    public bool isGameOver;
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化（极简模式范本）

**文件**：`ClientCustomRoomCampMgr.cs`

```csharp
public class ClientCustomRoomCampMgr : ClientModeManager {
    
    private ClientCustomRoomCampData data;
    
    public override void Init() {
        base.Init();
        data = new ClientCustomRoomCampData();
        data.Config = LoadSOConfig<SOCustomRoomCampData>();
    }
    
    // 极简：仅 3 个 Stage
    protected override void InitStage() {
        AddStage(new ClientCustomRoomCampBornStage());
        AddStage(new ClientCustomRoomCampBattleStage());
        AddStage(new ClientCustomRoomCampOverStage());
    }
    
    // 无独立 Logic 注册 — 逻辑直接在 Stage 中处理
}
```

### 4.2 角色阵营管理（Server）

**文件**：`ServerCustomRoomCampRoleLogic.cs`

```csharp
public class ServerCustomRoomCampRoleLogic : ServerLogicBase {
    
    // 角色加入
    public void AddRole(BattleRoleLogic role) {
        int teamId = AssignTeam(role);
        role.TeamId = teamId;
        data.teamRoles[teamId].Add(role);
        
        OnRoleAdd(role);  // 回调通知
    }
    
    // 阵营分配策略：人数最少的阵营优先
    private int AssignTeam(BattleRoleLogic role) {
        int minTeam = 0;
        int minCount = int.MaxValue;
        
        foreach (var kvp in data.teamRoles) {
            if (kvp.Value.Count < minCount) {
                minCount = kvp.Value.Count;
                minTeam = kvp.Key;
            }
        }
        return minTeam;
    }
    
    // 获取阵营人数
    public int GetUniteRoleNum(int teamId) {
        return data.teamRoles.ContainsKey(teamId) 
            ? data.teamRoles[teamId].Count 
            : 0;
    }
    
    // 重登处理
    public void OnReLogin(BattleRoleLogic role) {
        // 恢复阵营信息
        role.TeamId = GetSavedTeamId(role.RoleId);
        OnEnterBattle(role);
    }
}
```

### 4.3 战斗阶段（最简 Stage 实现）

**文件**：`ServerCustomRoomCampBattleStage.cs`

```csharp
public class ServerCustomRoomCampBattleStage : StageBase {
    
    public override void OnEnter() {
        base.OnEnter();
        // 启动战斗计时
        mgr.Data.battleTimer = mgr.Data.Config.battleTime;
    }
    
    public override void OnUpdate(float deltaTime) {
        // 倒计时
        mgr.Data.battleTimer -= deltaTime;
        
        // 时间耗尽 → 结束
        if (mgr.Data.battleTimer <= 0) {
            mgr.ChangeStage(CustomRoomCampStage.Over);
            return;
        }
        
        // 检查是否某阵营全灭
        foreach (var team in mgr.Data.teamRoles) {
            if (IsTeamAllDead(team.Value)) {
                mgr.ChangeStage(CustomRoomCampStage.Over);
                return;
            }
        }
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 自定义房间玩家加入后没有阵营

**现象**：后加入的玩家在战斗中没有阵营颜色，被双方都当作敌人

**根因**：
- `ServerCustomRoomCampRoleLogic.AddRole()` 在 Battle Stage 开始后才被调用
- 但 TeamId 的网络同步在 Born Stage 批量发送，Battle 阶段新加入的角色错过了同步

**解决方案**：
1. AddRole() 中在分配 TeamId 后立即发送 TargetRpc 给该玩家
2. 同时通过 Rpc 广播给所有玩家更新阵营列表
3. 客户端 OnRoleAdd 回调中刷新阵营 UI

### 5.2 重登后金钱/装备丢失

**现象**：掉线重连后玩家身上的武器和金钱归零

**根因**：
- OnReLogin() 仅恢复了 TeamId，未恢复装备和金钱状态
- 自定义房间不走标准 BuyWeaponControl 流程

**解决方案**：
1. ServerCustomRoomCampData 中保存每个玩家的 WeaponList 和 Money
2. OnReLogin() 中从保存数据恢复角色状态
3. 使用 TargetRpc 将恢复数据发送给重连客户端

### 5.3 房间人数不平衡

**现象**：一方 6 人另一方 2 人，体验极差

**根因**：
- AssignTeam() 仅在加入时分配，未考虑中途退出导致的人数失衡
- 无自动平衡机制

**解决方案**：
1. 增加 `CheckTeamBalance()` 在每回合开始前检查
2. 提供「自动平衡」选项：将多出的玩家移至少人队伍
3. 人数差超过设定阈值时禁止新玩家加入多人阵营

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `CampCustomized=42` 无冲突
- [ ] Factory 双端已注册
- [ ] 所有 Stage/Logic 类编译通过

### 6.2 配置

- [ ] SOCustomRoomCampData 参数合理
- [ ] CustomRoom.txt 解析正确
- [ ] 阵营数 ≥ 2，且每阵营人数上限合理

### 6.3 运行时

- [ ] 3 阶段正常流转（Born → Battle → Over）
- [ ] 阵营分配正确（人数均衡）
- [ ] 动态加入/退出不影响游戏
- [ ] 重登后阵营/状态恢复
- [ ] 计时正确，时间到自动结束
- [ ] 结算数据正确显示

### 6.4 兼容性

- [ ] 不影响其他自定义房间模式
- [ ] 不影响标准匹配模式
- [ ] 房间设置 UI 正确反映所有选项

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-customroomcamp]] · [[网络消息制作]]
