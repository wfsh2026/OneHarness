# 1 代架构回合制 1V1（TurnBasedMode1V1）制作规范

> **适用范围**：TurnBasedMode1V1 PK 之王 1V1 模式 — 新增回合规则 / 扩展武器轮换 / 调整 AI 对手
> **不适用**：通用模式框架 → 归 [[模式制作]]；斗牛模式 → 归 [[BullFighting制作]]（复用本模式 RoleLogic）
> **参考实现**：mode-turnbased（20 文件，★ 简单，经典 1V1 回合制模式）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage 基类 / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientTurnBasedMode1v1Mgr (Client 端 1V1 主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1v1/ClientTurnBasedMode1v1Mgr.cs
  │  继承: ClientModeManager
  │  职责: 回合制客户端入口，Stage 管理，回合数据显示
  │
  ├── ClientTurnBasedMode1v1RoleLogic
  │     职责: 角色逻辑（出生/死亡/重生），★ 被 BullFighting 模式复用
  │
  ├── ClientTurnBasedMode1v1MapLogic
  │     职责: 地图逻辑，出生点分配
  │
  ├── Stage 层（4 阶段）
  │     TurnBasedMode1v1BornStage → RoundStartStage → RoundEndStage → OverStage
  │
  └── ClientTurnBasedMode1v1Data
        职责: 客户端数据，含 Config 引用

ServerTurnBasedMode1V1Mgr (Server 端 1V1 主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/ServerTurnBasedMode1V1Mgr.cs
  │  继承: ServerModeManager
  │  职责: 回合制服务端入口，对战判定，回合推进
  │
  ├── ServerTurnBasedMode1v1RoleLogic
  │     职责: 角色管理，GetEnemy() 获取对手
  │
  ├── ServerTurnBasedModeAILogic
  │     职责: AI 对手控制（无真人匹配时）
  │
  ├── ServerTurnBasedMode1v1AwardLogic
  │     职责: 胜利/失败奖励结算
  │
  ├── ServerTurnBasedMode1v1StatisticsLogic
  │     职责: 战绩统计（胜场数/连胜数）
  │
  └── ServerTurnBasedMode1v1NsqDataLogic
        职责: NSQ 数据上报

ServerTurnBasedMode1V1Data
  │  方法: GetEnemy() / GetWinTimes() / CurRound
  │
  └── SOTurnBasedMode1V1Data (ScriptableObject)
        路径: Assets/ToBundle/ScriptableObject/Mode/TurnBased/
        含: 回合时间 / 等待时间 / 总回合数

SOGunfightRoundData (54 个回合武器配置文件)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/GunfightRound/
  │  职责: 每回合的武器轮换规则

TurnBasedMode1v1Stage (共享枚举)
  │  路径: Host 层
  │  职责: 阶段 ID 定义（Born/RoundStart/RoundEnd/Over）
```

### 1.2 Stage 阶段流转

```
4 阶段制（纯回合制，无商店）：

Born (出生阶段)
  │  两名玩家（或玩家 vs AI）在对称出生点生成
  ↓
RoundStart (回合开始)
  │  分配本回合武器（按 SOGunfightRoundData 配置轮换）
  │  开始回合计时 (RoundTime)
  │  判定条件：
  │    ├── 一方死亡 → 进入 RoundEnd
  │    └── 时间耗尽 → 进入 RoundEnd（存活方胜）
  ↓
RoundEnd (回合结束)
  │  显示回合结果（胜/负）
  │  更新连胜计数 (WinTimes / ContinueWinTimes)
  │  等待 RoundEndWaitTime 后进入下一回合
  │  判定：
  │    ├── 未达总回合数 → 回到 RoundStart
  │    └── 达到总回合数 → 进入 Over
  ↓
Over (游戏结束)
    汇总胜负，显示最终结果
    处理排名/赛季积分
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/TurnBased/*.asset` | Resources/AB | Mgr.Init() |
| **回合武器配置** | `Assets/ToBundle/ScriptableObject/Mode/GunfightRound/` (54 个) | Resources/AB | RoundStart |
| **回合 HUD** | 复用通用 War UI + 自定义回合计数 | UIManager | Stage.OnEnter() |
| **角色动画** | `Assets/ToBundle/Role/Controllers/War/TimeMode/` | AnimController | Born |

### 1.4 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 已有枚举值 `Turnbased=33`
- **SOGunfightRoundData** 的已有回合数据 — 仅可追加新文件

---

## 二、新建/扩展 Checklist

### Phase 1：调整回合规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `SOTurnBasedMode1V1Data.asset` | 修改 | 调整 RoundTime / RoundEndWaitTime / TotalRounds |
| 2 | `SOGunfightRoundData` | 新建/修改 | 新增回合武器配置文件 |

### Phase 2：扩展 Logic 模块

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 3 | `Client/Modules/Mode/TurnBasedMode1v1/Logic/Client{LogicName}Logic.cs` | 新建 | 客户端新 Logic |
| 4 | `Server/Modules/Mode/TurnBasedMode1V1/Logic/Server{LogicName}Logic.cs` | 新建 | 服务端新 Logic |
| 5 | 对应 Mgr.cs | 修改 | Init() 中注册新 Logic |

### Phase 3：扩展 AI 对手

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | `ServerTurnBasedModeAILogic.cs` | 修改 | 调整 AI 行为（难度/策略/武器使用） |
| 7 | AI 配置 SO | 修改 | 新增 AI 等级配置 |

### Phase 4：新增重登/断线重连支持

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `ServerTurnBasedMode1V1Data` | 修改 | RoleReLogin 处理 |
| 9 | 对应客户端 | 修改 | BattleDownTime 同步 / 连胜数恢复 |

---

## 三、配置文件详解

### 3.1 SOTurnBasedMode1V1Data

**路径**：`Assets/ToBundle/ScriptableObject/Mode/TurnBased/SOTurnBasedMode1V1Data.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `roundTime` | float | 单回合战斗时间（秒，默认 60） |
| `roundEndWaitTime` | float | 回合间等待时间（秒，默认 5） |
| `totalRounds` | int | 总回合数（默认 5） |
| `winRoundsToWin` | int | 胜场数达标即为总冠军 |
| `enableAI` | bool | 是否在无对手时启用 AI |
| `aiDifficulty` | int | AI 难度等级 |

### 3.2 SOGunfightRoundData（武器轮换配置）

**路径**：`Assets/ToBundle/ScriptableObject/Mode/GunfightRound/` (54 个文件)

```csharp
[CreateAssetMenu]
public class SOGunfightRoundData : ScriptableObject {
    public int roundIndex;           // 回合序号
    public int[] weaponIds;          // 本回合可用武器 ID 列表
    public int[] equipmentIds;       // 本回合装备 ID 列表
    public bool isRandomWeapon;      // 是否随机分配武器
    public int ammoCount;            // 弹药数量
}
```

### 3.3 核心数据类

```csharp
// 服务端数据
public class ServerTurnBasedMode1V1Data {
    public SOTurnBasedMode1V1Data Config;
    public int CurRound;                    // 当前回合
    public float RoundTimer;                // 回合剩余时间
    
    // 获取对手
    public BattleRoleLogic GetEnemy(int roleId) {
        // 两人模式，返回另一个玩家
    }
    
    // 获取胜场数
    public int GetWinTimes(int roleId) {
        return winTimesDict[roleId];
    }
    
    // 连胜数据
    public int TurnBasedMode1v1WinTimes;
    public int TurnBasedMode1v1ContinueWinTimes;
}

// 客户端数据
public class ClientTurnBasedMode1v1Data {
    public SOTurnBasedMode1V1Data Config;
    public int MyWins;
    public int EnemyWins;
    public int CurrentRound;
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化

**文件**：`ClientTurnBasedMode1v1Mgr.cs`

```csharp
public class ClientTurnBasedMode1v1Mgr : ClientModeManager {
    
    public override void Init() {
        base.Init();
        data = new ClientTurnBasedMode1v1Data();
        data.Config = LoadSOConfig<SOTurnBasedMode1V1Data>();
        
        // 注册 Logic
        AddLogic(new ClientTurnBasedMode1v1RoleLogic());
        AddLogic(new ClientTurnBasedMode1v1MapLogic());
    }
    
    protected override void InitStage() {
        AddStage(new ClientTurnBasedMode1v1BornStage());
        AddStage(new ClientTurnBasedMode1v1RoundStartStage());
        AddStage(new ClientTurnBasedMode1v1RoundEndStage());
        AddStage(new ClientTurnBasedMode1v1OverStage());
    }
}
```

### 4.2 回合推进逻辑（Server）

**文件**：`ServerTurnBasedMode1V1Mgr.cs`

```csharp
// RoundStart Stage 中的判定
public override void OnUpdate(float deltaTime) {
    data.RoundTimer -= deltaTime;
    
    // 一方死亡
    if (IsAnyRoleDead()) {
        var winner = GetAliveRole();
        data.winTimesDict[winner.RoleId]++;
        data.TurnBasedMode1v1ContinueWinTimes++;
        ChangeStage(TurnBasedMode1v1Stage.RoundEnd);
        return;
    }
    
    // 时间耗尽 — 双方存活则判定生命值高者胜
    if (data.RoundTimer <= 0) {
        var winner = GetHigherHpRole();
        data.winTimesDict[winner.RoleId]++;
        ChangeStage(TurnBasedMode1v1Stage.RoundEnd);
    }
}

// RoundEnd Stage 中的下一回合判定
public void OnRoundEndComplete() {
    data.CurRound++;
    
    // 检查是否有玩家达到胜场要求
    if (HasPlayerWonMatch()) {
        ChangeStage(TurnBasedMode1v1Stage.Over);
    } else {
        // 下一回合
        ChangeStage(TurnBasedMode1v1Stage.RoundStart);
    }
}
```

### 4.3 武器轮换

```csharp
// RoundStart Stage OnEnter 中分配武器
public override void OnEnter() {
    base.OnEnter();
    
    // 加载本回合武器配置
    var roundData = LoadGunfightRoundData(data.CurRound);
    
    foreach (var role in allRoles) {
        // 清空上回合武器
        role.ClearInventory();
        
        // 分配本回合武器
        if (roundData.isRandomWeapon) {
            int weaponId = roundData.weaponIds[Random.Range(0, roundData.weaponIds.Length)];
            role.GiveWeapon(weaponId, roundData.ammoCount);
        } else {
            foreach (int weaponId in roundData.weaponIds) {
                role.GiveWeapon(weaponId, roundData.ammoCount);
            }
        }
    }
    
    // 重置回合计时
    data.RoundTimer = data.Config.roundTime;
}
```

### 4.4 RoleLogic（被 BullFighting 复用）

**文件**：`ClientTurnBasedMode1v1RoleLogic.cs`

```csharp
// ★ 此 Logic 被 BullFighting 模式直接复用
public class ClientTurnBasedMode1v1RoleLogic : ClientLogicBase {
    
    public override void Init() {
        // 注册角色相关事件
        RegisterEvent(EventId.OnRoleSpawn, OnRoleSpawn);
        RegisterEvent(EventId.OnRoleDead, OnRoleDead);
    }
    
    private void OnRoleDead(int roleId) {
        // 显示死亡 UI
        // 等待回合结束
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 回合开始后双方武器相同

**现象**：两个玩家在同一回合拿到了完全相同的武器，缺乏对抗趣味

**根因**：SOGunfightRoundData 的 `isRandomWeapon=false` 且 weaponIds 只有一种武器

**解决方案**：
1. 检查 SOGunfightRoundData 配置，确保每回合至少 2 种武器或开启随机
2. 如果策划要求"镜像对称"（双方同武器），这是正常设计
3. 如需差异化，设置 `isRandomWeapon=true` 并提供多武器池

### 5.2 AI 对手不开枪或行为异常

**现象**：当匹配不到真人时 AI 对手站着不动或不攻击

**根因**：`ServerTurnBasedModeAILogic` 的 AI 行为树未正确加载或武器使用逻辑缺失

**解决方案**：
1. 确认 AI 配置 SO 中的难度参数合理
2. 检查 AI 是否在 RoundStart 中正确获取了本回合武器
3. AI 的射击频率/瞄准精度应根据难度等级调整

### 5.3 连胜数断线后丢失

**现象**：玩家断线重连后连胜数归零

**根因**：RoleReLogin 处理中未同步 ContinueWinTimes

**解决方案**：
1. ServerTurnBasedMode1V1Data 保存 per-role 连胜数据
2. RoleReLogin 回调中恢复：BattleDownTime + WinTimes + ContinueWinTimes
3. 通过 TargetRpc 将恢复数据发给重连客户端

### 5.4 回合结束后角色位置未重置

**现象**：新回合开始时玩家还在上回合的死亡位置

**根因**：RoundStart.OnEnter() 中未调用角色重生重置位置

**解决方案**：
1. RoundStart.OnEnter() 中重新分配出生点
2. 调用 role.Respawn(spawnPoint) 重置位置/生命值/状态
3. 确保先重生再分配武器

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `Turnbased=33` 无冲突
- [ ] Factory 双端已注册

### 6.2 配置

- [ ] SOTurnBasedMode1V1Data 参数合理
- [ ] SOGunfightRoundData 54 个文件格式正确
- [ ] 武器 ID 在 WeaponConfig 中存在

### 6.3 运行时

- [ ] 4 阶段正常流转（Born→RoundStart→RoundEnd→Over 循环）
- [ ] 武器轮换正确，每回合武器按配置分配
- [ ] 一方死亡正确判定回合胜负
- [ ] 时间耗尽正确判定
- [ ] 连胜数正确累计
- [ ] AI 对手行为正常
- [ ] 断线重连后数据恢复

### 6.4 兼容性

- [ ] 不影响 BullFighting 模式（复用 RoleLogic）
- [ ] 不影响其他 1V1 模式
- [ ] 自定义房间可启用

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-turnbased]] · [[BullFighting制作]]
