# 1 代架构团队对战（TeamMode）制作规范

> **适用范围**：TeamMode 团队激斗 — 新增队伍规则 / 扩展变身/复仇系统 / 调整重生机制
> **不适用**：通用模式框架 → 归 [[模式制作]]；Common 基础框架 → 归 [[CommonMode制作]]
> **参考实现**：mode-teammode（32 文件，★★ 中等，Logic 数量最多 12 个）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientTeamModeMgr (Client 端团队对战主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/ClientTeamModeMgr.cs
  │  继承: ClientModeManager
  │  职责: 团队对战客户端入口，Stage 管理，团队数据展示
  │
  ├── ClientTeamModeRuleLogic
  │     职责: 规则逻辑，连杀计数/显示
  │
  ├── ClientTeamModeSceneLogic
  │     职责: 场景逻辑，RemoveSceneParts()（按配置移除场景元素）
  │
  ├── Stage 层（5 阶段 + Running 阶段）
  │     BornStage → ReadyStage → RunningStage → RoundOverStage → OverStage
  │
  ├── ClientTeamModeUtil (工具类)
  │     职责: 客户端辅助方法
  │
  └── ClientTeamModeData
        职责: 含 SOTeamModeConfigData 引用

ServerTeamModeMgr (Server 端团队对战主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/ServerTeamModeMgr.cs
  │  继承: ServerModeManager
  │  职责: 团队对战服务端入口，12 个 Logic 管理
  │
  ├── ServerTeamModeWeaponLogic     — 武器系统
  ├── ServerTeamModeRuleLogic       — 规则引擎（胜负/计分）
  ├── ServerTeamModeJoinLogic       — 动态加入（中途补人）
  ├── ServerTeamModeAwardLogic      — 奖励结算
  ├── ServerTeamModeStatisticsLogic — 战绩统计
  ├── ServerTeamModeNsqDataLogic    — NSQ 上报
  ├── ServerTeamModeRebornLogic     — 重生机制
  ├── ServerTeamModeTransformLogic  — 变身/形态
  ├── ServerTeamModeRevengeLogic    — 复仇机制
  ├── ServerTeamModeTestLogic       — 测试逻辑
  ├── ModeTimerLogic                — 时间控制
  └── TeamModeUtil                  — 工具方法

数据层
  │  ClientTeamModeData (包含 SOTeamModeConfigData)
  │  ServerTeamModeData
  │
  └── SOTeamModeConfigData (ScriptableObject)
        路径: Assets/ToBundle/ScriptableObject/Mode/TeamMode/
        含: SuperKillNum / LegendaryKillNum / UpLookMoveTime / NeedRemoveSceneParts

消息系统（高频同步）
    OnSyncTeamModeData / OnSyncRoleStatisticsDatas / OnSyncAllRoleStatisticsDatas
    OnSyncRoundData / OnSyncAllRoundDatas / OnBeforeRoleRemove
```

### 1.2 Stage 阶段流转

```
5 阶段制 + Running 战斗阶段（含回合循环）：

Born (出生阶段)
  │  玩家按队伍分配出生点
  │  加载 SOTeamModeConfigData
  │  RemoveSceneParts() 按配置移除场景元素
  ↓
Ready (准备阶段)
  │  等待所有玩家就绪
  │  显示队伍信息/地图概览
  │  MoveAnimTime 相机动画
  ↓
Running (战斗运行阶段) ← ★ TeamMode 独有
  │  核心战斗循环
  │  动态加入（中途补人 JoinLogic）
  │  变身触发（TransformLogic）
  │  复仇判定（RevengeLogic）
  │  重生计数（RebornLogic）
  │  连杀检测（SuperKill / LegendaryKill）
  │  高频同步（每帧 StatisticsData 更新）
  │  判定条件：
  │    ├── 回合时间到 → RoundOver
  │    └── 某队积分达标 → RoundOver
  ↓
RoundOver (回合结束)
  │  显示回合结算
  │  MVP 展示
  │  判定：
  │    ├── 未达总回合数 → Born（下一回合）
  │    └── 达到总回合数 → Over
  ↓
Over (游戏结束)
    最终排名/赛季积分处理
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/TeamMode/` | Resources/AB | Mgr.Init() |
| **防守点配置** | `SOTeamModeDefensePointData` | Resources/AB | Ready |
| **动画控制器** | `Assets/ToBundle/Role/Controllers/War/TimeMode/` | AnimController | Born |
| **指令音效** | `InstructionSoundConfig` | AudioManager | Running |
| **连杀特效** | SuperKill/LegendaryKill UI | UIManager | Running |

### 1.4 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 已有枚举值 `TeamMode`
- **DMInfo** 基础结构 — 仅可扩展，不可修改已有字段

---

## 二、新建/扩展 Checklist

### Phase 1：调整团队规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `SOTeamModeConfigData.asset` | 修改 | 调整 SuperKillNum / LegendaryKillNum / 回合数 |
| 2 | `SOTeamModeDefensePointData.asset` | 修改 | 调整防守点位置/属性 |

### Phase 2：新增 Logic

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 3 | `Client/Modules/Mode/TeamMode/Logic/Client{LogicName}Logic.cs` | 新建 | 客户端 Logic |
| 4 | `Server/Modules/Mode/TeamMode/Logic/Server{LogicName}Logic.cs` | 新建 | 服务端 Logic |
| 5 | `ClientTeamModeMgr.cs` | 修改 | Init() 注册 |
| 6 | `ServerTeamModeMgr.cs` | 修改 | Init() 注册 |

### Phase 3：扩展变身/复仇系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 7 | `ServerTeamModeTransformLogic.cs` | 修改 | 新增变身条件/效果 |
| 8 | `ServerTeamModeRevengeLogic.cs` | 修改 | 新增复仇触发规则 |
| 9 | 对应客户端表现 | 修改 | 变身/复仇 UI 和特效 |

### Phase 4：调整重生机制

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 10 | `ServerTeamModeRebornLogic.cs` | 修改 | 重生时间/次数/条件 |
| 11 | 出生点配置 | 修改 | 重生位置规则 |

### Phase 5：扩展数据同步

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 12 | 消息定义 | 新建 | 新增 OnSync{XXX}Data 消息 |
| 13 | `ServerTeamModeStatisticsLogic.cs` | 修改 | 新增统计维度 |

---

## 三、配置文件详解

### 3.1 SOTeamModeConfigData

**路径**：`Assets/ToBundle/ScriptableObject/Mode/TeamMode/SOTeamModeConfigData.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `SuperKillNum` | int | 超级连杀阈值（如连续击杀 5 人） |
| `LegendaryKillNum` | int | 传奇连杀阈值（如连续击杀 10 人） |
| `UpLookMoveTime` | float | 相机上移动画时间（回合开始前的俯瞰） |
| `NeedRemoveSceneParts` | string[] | 需要移除的场景部件名称列表 |
| `roundCount` | int | 总回合数 |
| `roundTime` | float | 每回合时长 |
| `teamSize` | int | 每队人数 |
| `rebornTime` | float | 重生等待时间 |
| `maxRebornCount` | int | 最大重生次数 |
| `scoreToWin` | int | 获胜积分 |

### 3.2 SOTeamModeDefensePointData

**路径**：`Assets/ToBundle/ScriptableObject/Mode/TeamMode/`

| 字段 | 类型 | 说明 |
|------|------|------|
| `pointId` | int | 防守点 ID |
| `position` | Vector3 | 位置坐标 |
| `radius` | float | 范围半径 |
| `captureTime` | float | 占领时间 |
| `scorePerSecond` | int | 每秒积分 |

### 3.3 核心数据类

```csharp
// 客户端
public class ClientTeamModeData {
    public SOTeamModeConfigData Config;
    public int MyTeamScore;
    public int EnemyTeamScore;
    public int MyKills;
    public int MyDeaths;
    public int CurrentRound;
}

// 服务端
public class ServerTeamModeData {
    public Dictionary<int, int> TeamScores;        // 队伍 → 积分
    public Dictionary<int, int> RoleKills;         // 角色 → 击杀数
    public Dictionary<int, int> RoleDeaths;        // 角色 → 死亡数
    public Dictionary<int, int> RoleRebornCount;   // 角色 → 已重生次数
    public int CurRound;
    public float RoundTimer;
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化（12 个 Logic 注册）

**文件**：`ServerTeamModeMgr.cs`

```csharp
public class ServerTeamModeMgr : ServerModeManager {
    
    public override void Init() {
        base.Init();
        data = new ServerTeamModeData();
        data.Config = LoadSOConfig<SOTeamModeConfigData>();
        
        // 12 个 Logic — 注册顺序影响 Update 调用顺序
        AddLogic(new ServerTeamModeWeaponLogic());
        AddLogic(new ServerTeamModeRuleLogic());
        AddLogic(new ServerTeamModeJoinLogic());
        AddLogic(new ServerTeamModeAwardLogic());
        AddLogic(new ServerTeamModeStatisticsLogic());
        AddLogic(new ServerTeamModeNsqDataLogic());
        AddLogic(new ServerTeamModeRebornLogic());
        AddLogic(new ServerTeamModeTransformLogic());
        AddLogic(new ServerTeamModeRevengeLogic());
        AddLogic(new ServerTeamModeTestLogic());
        AddLogic(new ModeTimerLogic());
    }
    
    // 场景元素移除（按配置）
    private void RemoveSceneParts() {
        foreach (var partName in data.Config.NeedRemoveSceneParts) {
            var obj = GameObject.Find(partName);
            if (obj != null) obj.SetActive(false);
        }
    }
}
```

### 4.2 动态加入机制

**文件**：`ServerTeamModeJoinLogic.cs`

```csharp
public class ServerTeamModeJoinLogic : ServerLogicBase {
    
    // 中途加入处理
    public void OnPlayerJoin(BattleRoleLogic newRole) {
        // 分配到人数少的队伍
        int team = GetTeamWithFewerPlayers();
        newRole.SetTeam(team);
        
        // 初始化武器/装备
        mgr.GetLogic<ServerTeamModeWeaponLogic>().GiveDefaultWeapons(newRole);
        
        // 同步当前回合数据给新玩家
        SyncCurrentRoundData(newRole);
        
        // 重新平衡队伍
        RebalanceTeams();
    }
    
    private int GetTeamWithFewerPlayers() {
        // 遍历所有队伍，返回人数最少的队伍 ID
        return teamSizes.OrderBy(t => t.Value).First().Key;
    }
}
```

### 4.3 连杀系统

```csharp
// ServerTeamModeRuleLogic 中的连杀判定
public void OnRoleKill(int killerId, int victimId) {
    data.RoleKills[killerId]++;
    
    // 更新连杀计数
    int streak = UpdateKillStreak(killerId);
    
    // DMInfo 连杀播报
    if (streak >= data.Config.LegendaryKillNum) {
        SendRpc(RpcType.LegendaryKill, killerId, streak);
        DMInfo.LegendaryKillNum++;
    } else if (streak >= data.Config.SuperKillNum) {
        SendRpc(RpcType.SuperKill, killerId, streak);
        DMInfo.SuperKillNum++;
    }
    
    // 复仇判定
    mgr.GetLogic<ServerTeamModeRevengeLogic>().CheckRevenge(killerId, victimId);
    
    // 积分更新
    data.TeamScores[GetTeam(killerId)] += killScoreValue;
    
    // 同步给所有客户端
    SyncAllRoleStatisticsData();
}
```

### 4.4 变身系统

**文件**：`ServerTeamModeTransformLogic.cs`

```csharp
public class ServerTeamModeTransformLogic : ServerLogicBase {
    
    // 变身触发条件检查
    public override void OnUpdate(float deltaTime) {
        foreach (var role in mgr.GetAllRoles()) {
            if (ShouldTransform(role)) {
                TriggerTransform(role);
            }
        }
    }
    
    private bool ShouldTransform(BattleRoleLogic role) {
        // 连杀达标 / 特殊条件达成
        return GetKillStreak(role.RoleId) >= transformThreshold;
    }
    
    private void TriggerTransform(BattleRoleLogic role) {
        // 切换角色形态
        role.SetTransformState(true);
        // 增强属性
        role.SetAttackMultiplier(transformBonus);
        // 通知客户端播放变身特效
        SendRpc(new RpcTransform { roleId = role.RoleId, type = TransformType.SuperForm });
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 Logic 注册顺序导致 Update 时序问题

**现象**：变身判定在击杀统计之前执行，导致连杀数不准确

**根因**：AddLogic() 注册顺序决定 Update() 调用顺序，如果 TransformLogic 注册在 StatisticsLogic 之前，则连杀数还未更新就触发变身检查

**解决方案**：
1. 确保 StatisticsLogic 注册在 TransformLogic 之前
2. 或在 TransformLogic 中使用事件驱动（OnKillEvent）而非 Update 轮询
3. 添加注释标明注册顺序的依赖关系

### 5.2 中途加入的玩家数据不同步

**现象**：中途加入的玩家看不到当前回合积分和击杀信息

**根因**：JoinLogic 只初始化了武器，未调用 `SyncCurrentRoundData()`

**解决方案**：
1. JoinLogic.OnPlayerJoin() 中必须调用：
   - SyncCurrentRoundData() — 当前回合数据
   - SyncAllRoleStatisticsData() — 全员统计
   - SyncTeamScores() — 队伍积分
2. 按照先分配队伍 → 发武器 → 同步数据的顺序执行

### 5.3 NeedRemoveSceneParts 配置的场景元素找不到

**现象**：RemoveSceneParts() 运行时 `GameObject.Find()` 返回 null

**根因**：
- 场景元素名称拼写错误
- 场景元素在 Awake 时被其他脚本重命名
- 多场景模式下元素在子场景中未加载

**解决方案**：
1. 使用 tag 或 layer 替代名称查找（更可靠）
2. 在 ReadyStage.OnEnter() 后再执行移除（确保场景加载完毕）
3. 添加 warning log 提示未找到的元素名

### 5.4 高频同步导致网络带宽过高

**现象**：TeamMode 服务器带宽明显高于其他模式

**根因**：OnSyncRoleStatisticsDatas / OnSyncAllRoleStatisticsDatas 每次击杀都全量同步

**解决方案**：
1. 使用增量同步：仅发送变化的角色数据
2. 降低同步频率：非关键数据 1 秒同步一次而非每帧
3. 使用 dirty flag 标记需要同步的数据

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `TeamMode` 无冲突
- [ ] Factory 双端已注册
- [ ] 12 个 Logic 全部编译通过

### 6.2 配置

- [ ] SOTeamModeConfigData 连杀/回合/队伍参数合理
- [ ] SOTeamModeDefensePointData 位置/属性合理
- [ ] NeedRemoveSceneParts 中的名称在场景中存在

### 6.3 运行时

- [ ] 5 阶段正常流转（Born→Ready→Running→RoundOver→Over）
- [ ] 队伍分配正确（平均分人）
- [ ] 中途加入的玩家数据同步完整
- [ ] 连杀播报正确触发（SuperKill/LegendaryKill）
- [ ] 变身系统正常触发/解除
- [ ] 复仇判定准确
- [ ] 重生时间/次数正确
- [ ] 回合积分正确累计

### 6.4 兼容性

- [ ] 不影响其他团队类模式
- [ ] DMInfo 数据正确
- [ ] 自定义房间可启用
- [ ] 排位/赛季积分正确

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-teammode]]
