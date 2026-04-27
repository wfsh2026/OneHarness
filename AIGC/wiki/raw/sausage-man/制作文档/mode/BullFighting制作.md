# 1 代架构斗牛/枪王之王（BullFighting）制作规范

> **适用范围**：BullFighting 枪王之王模式 — 扩展回合规则 / 新增商店商品 / 调整 AI 策略
> **不适用**：通用模式框架 → 归 [[模式制作]]；纯 1V1 回合制 → 归 [[TurnBasedMode制作]]
> **参考实现**：mode-bullfighting（23 文件，★ 简单，带商店的回合制 PK 模式）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **特殊依赖**：复用 [[TurnBasedMode制作]] 的 `ClientTurnBasedMode1v1RoleLogic`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientBullFightingModeMgr (Client 端枪王之王主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/ClientBullFightingModeMgr.cs
  │  继承: ClientModeManager
  │  职责: 枪王之王客户端入口，6 阶段 Stage 管理
  │
  ├── ClientTurnBasedMode1v1RoleLogic ← ★ 复用 TurnBased 的 RoleLogic
  │     路径: Client/Modules/Mode/TurnBasedMode1v1/Logic/
  │     职责: 角色出生/死亡/重生（跨模式复用）
  │
  ├── ClientBullFightingModeMapLogic
  │     职责: 地图逻辑，出生点分配
  │
  ├── Stage 层（6 阶段，含 Info 和 Shop）
  │     BornStage → InfoStage → ShopStage → RoundStartStage → RoundEndStage → OverStage
  │
  └── ClientBullFightingModeData
        职责: 客户端数据

ServerBullFightingModeMgr (Server 端枪王之王主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/ServerBullFightingModeMgr.cs
  │  继承: ServerModeManager
  │  ⚠️ 注意：Server 目录名为 BullFighting/（无 Mode 后缀），Client 为 BullFightingMode/
  │
  ├── ServerBullFightingModeRoleLogic
  │     职责: 角色管理，阵营分配
  │
  ├── ServerBullFightingModeAILogic
  │     职责: AI 对手控制
  │
  ├── ServerBullFightingModeAwardLogic
  │     职责: 奖励结算
  │
  ├── ServerBullFightingModeStatisticsLogic
  │     职责: 战绩统计（连赢/连胜）
  │
  └── ServerBullFightingModeNsqDataLogic
        职责: NSQ 数据上报

BullFightingModeStage (共享枚举 - 客户端预加载)
  │  阶段: Born=0, Info, Shop, RoundStart, RoundEnd, Over

SOBullFightingModeData (主配置)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/BullFighting/

SOGunfightRoundData (54 个回合武器配置 — 与 TurnBased 共享)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/GunfightRound/
```

### 1.2 Stage 阶段流转

```
6 阶段制（含独有 Info 和 Shop 阶段）：

Born (出生阶段)
  │  两人在对称出生点生成
  ↓
Info (信息展示阶段) ← ★ BullFighting 独有
  │  展示对手信息、历史战绩、连胜数据
  │  DMInfo 更新玩家列表
  ↓
Shop (商店阶段) ← ★ BullFighting 独有
  │  玩家购买额外装备/道具
  │  使用回合奖金进行购买
  ↓
RoundStart (回合开始)
  │  分配本回合武器（按 SOGunfightRoundData）
  │  开始回合计时
  │  判定：一方死亡或时间耗尽
  ↓
RoundEnd (回合结束)
  │  显示回合结果，更新连胜数
  │  TurnBasedMode1v1WinTimes / ContinueWinTimes 更新
  │  判定：达到总回合数 → Over，否则 → Info（下一回合）
  ↓
Over (游戏结束)
    汇总最终结果，排名/赛季处理
```

### 1.3 与 TurnBased 的差异对比

| 特性 | TurnBased | BullFighting |
|------|-----------|-------------|
| Stage 数量 | 4 (Born→Round→RoundEnd→Over) | 6 (含 Info + Shop) |
| 商店 | 无 | 有 |
| 信息展示 | 无 | 有 (DMInfo) |
| RoleLogic | 自有 | 复用 TurnBased 的 |
| AI | 基础 | 独立 AILogic |
| 连胜 | 基础计数 | SuperKillNum / LegendaryKillNum |
| GameMode 枚举 | Turnbased=33 | Bullfighting=43 |
| Client 目录 | TurnBasedMode1v1/ | BullFightingMode/ |
| Server 目录 | TurnBasedMode1V1/ | BullFighting/（⚠️ 无 Mode 后缀） |

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/BullFighting/` | Resources/AB | Mgr.Init() |
| **回合武器配置** | `Assets/ToBundle/ScriptableObject/Mode/GunfightRound/` (54 个) | Resources/AB | RoundStart |
| **对手信息 UI** | 专属 InfoPanel | UIManager.Open() | InfoStage.OnEnter() |
| **商店 UI** | 购买面板 | UIManager.Open() | ShopStage.OnEnter() |
| **调试信息** | DMInfo (Debug Mode Info) | 内部调试 | 开发阶段 |

### 1.5 禁止修改的文件

- **ClientTurnBasedMode1v1RoleLogic.cs** — 跨模式复用，修改会影响 TurnBased
- **GameMode.cs** 已有枚举值 `Bullfighting=43`
- **SOGunfightRoundData** 已有配置 — 仅可追加

---

## 二、新建/扩展 Checklist

### Phase 1：调整回合规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `SOBullFightingModeData.asset` | 修改 | 调整回合时间/总回合数/连杀阈值 |
| 2 | `SOGunfightRoundData` | 新建 | 新增武器轮换配置 |

### Phase 2：扩展商店系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 3 | `ClientBullFightingModeShopStage.cs` | 修改 | 商品列表/价格调整 |
| 4 | 商店 UI Prefab | 修改 | 新增商品展示槽位 |
| 5 | `ServerBullFightingModeAwardLogic.cs` | 修改 | 调整回合奖金（影响购买力） |

### Phase 3：新增 Logic

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | `Client/Logic/Client{LogicName}Logic.cs` | 新建 | 客户端新 Logic |
| 7 | `Server/Logic/Server{LogicName}Logic.cs` | 新建 | 服务端新 Logic |
| 8 | 对应 Mgr.cs | 修改 | Init() 注册 |

### Phase 4：调整 AI

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `ServerBullFightingModeAILogic.cs` | 修改 | AI 策略/难度/购买行为 |
| 10 | AI 配置 | 修改 | 新增 AI 等级参数 |

### Phase 5：新增连杀特效/播报

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | DMInfo 相关代码 | 修改 | 新增 SuperKill/LegendaryKill 阈值 |
| 12 | 连杀 UI/音效 | 新建 | 连杀达标时的表现 |

---

## 三、配置文件详解

### 3.1 SOBullFightingModeData

**路径**：`Assets/ToBundle/ScriptableObject/Mode/BullFighting/SOBullFightingModeData.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `roundTime` | float | 单回合时间（秒） |
| `roundEndWaitTime` | float | 回合间等待时间 |
| `totalRounds` | int | 总回合数 |
| `shopTime` | float | 商店阶段时长 |
| `infoDisplayTime` | float | 信息展示时长 |
| `superKillNum` | int | 超级连杀阈值（如 3 连胜） |
| `legendaryKillNum` | int | 传奇连杀阈值（如 5 连胜） |
| `startMoney` | int | 初始金钱 |
| `roundWinMoney` | int | 回合胜利奖金 |
| `killMoney` | int | 击杀奖金 |

### 3.2 DMInfo（调试模式信息）

```csharp
// DMInfo 用于开发调试，显示当前对战状态
public class DMInfo {
    public int SuperKillNum;           // 超级连杀次数
    public int LegendaryKillNum;       // 传奇连杀次数
    
    // 更新玩家列表
    public void UpdatePlayerList(List<BattleRoleLogic> roles) {
        // 刷新 Debug UI 中的玩家信息
    }
}
```

### 3.3 连杀数据

```csharp
// 客户端数据
public class ClientBullFightingModeData {
    public SOBullFightingModeData Config;
    public int MyWins;
    public int MyConsecutiveWins;       // 连胜数
    public int EnemyWins;
    public int CurrentRound;
    public int Money;                   // 当前金钱
}

// 服务端数据
public class ServerBullFightingModeData {
    public int CurRound;
    public Dictionary<int, int> WinTimes;
    public Dictionary<int, int> ContinueWinTimes;
    public Dictionary<int, int> PlayerMoney;
    
    // 连杀标记
    public int TurnBasedMode1v1WinTimes;
    public int TurnBasedMode1v1ContinueWinTimes;
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化（含 RoleLogic 复用）

**文件**：`ClientBullFightingModeMgr.cs`

```csharp
public class ClientBullFightingModeMgr : ClientModeManager {
    
    public override void Init() {
        base.Init();
        data = new ClientBullFightingModeData();
        data.Config = LoadSOConfig<SOBullFightingModeData>();
        
        // ★ 复用 TurnBased 的 RoleLogic
        AddLogic(new ClientTurnBasedMode1v1RoleLogic());
        AddLogic(new ClientBullFightingModeMapLogic());
    }
    
    protected override void InitStage() {
        AddStage(new ClientBullFightingModeBornStage());
        AddStage(new ClientBullFightingModeInfoStage());     // ★ 独有
        AddStage(new ClientBullFightingModeShopStage());     // ★ 独有
        AddStage(new ClientBullFightingModeRoundStartStage());
        AddStage(new ClientBullFightingModeRoundEndStage());
        AddStage(new ClientBullFightingModeOverStage());
    }
}
```

### 4.2 InfoStage（信息展示）

**文件**：`ClientBullFightingModeInfoStage.cs`

```csharp
public class ClientBullFightingModeInfoStage : StageBase {
    
    public override void OnEnter() {
        base.OnEnter();
        // 显示对手信息面板
        var enemy = mgr.Data.GetEnemy();
        UIManager.Open<BullFightingInfoPanel>(new InfoPanelData {
            enemyName = enemy.Name,
            enemyWins = mgr.Data.EnemyWins,
            myWins = mgr.Data.MyWins,
            currentRound = mgr.Data.CurrentRound
        });
        
        // DMInfo 更新
        DMInfo.UpdatePlayerList(mgr.GetAllRoles());
    }
    
    public override void OnExit() {
        UIManager.Close<BullFightingInfoPanel>();
        base.OnExit();
    }
}
```

### 4.3 连杀判定（Server）

```csharp
// ServerBullFightingModeMgr 中的回合结束处理
public void OnRoundEnd(int winnerId) {
    var data = serverData;
    data.WinTimes[winnerId]++;
    data.ContinueWinTimes[winnerId]++;
    
    // 检查连杀成就
    int consecutive = data.ContinueWinTimes[winnerId];
    
    if (consecutive >= data.Config.legendaryKillNum) {
        // 传奇连杀播报
        SendRpc(RpcType.LegendaryKill, winnerId);
    } else if (consecutive >= data.Config.superKillNum) {
        // 超级连杀播报
        SendRpc(RpcType.SuperKill, winnerId);
    }
    
    // 失败方重置连胜
    var loserId = GetOtherRole(winnerId);
    data.ContinueWinTimes[loserId] = 0;
}
```

---

## 五、常见问题与踩坑记录

### 5.1 RoleLogic 修改影响 TurnBased

**现象**：修改 BullFighting 的角色行为后，TurnBased 模式也受到影响

**根因**：BullFighting 复用了 `ClientTurnBasedMode1v1RoleLogic`，不是独立副本

**解决方案**：
1. 如果修改是通用的（两个模式都需要），直接在原 Logic 中修改
2. 如果修改是 BullFighting 专属的，创建 `ClientBullFightingModeRoleLogic` 继承原 Logic 并 override
3. 绝不要在原 Logic 中加 `if (gameMode == BullFighting)` 条件判断

### 5.2 Client/Server 目录名不一致

**现象**：新建文件时放错目录

**根因**：Client 端目录名为 `BullFightingMode/`，Server 端为 `BullFighting/`（无 Mode 后缀），命名不一致

**解决方案**：
1. 新建 Client 文件 → `Client/Modules/Mode/BullFightingMode/`
2. 新建 Server 文件 → `Server/Modules/Mode/BullFighting/`
3. 注意 asmdef / csproj 引用路径正确

### 5.3 商店购买后武器与回合武器冲突

**现象**：商店购买了手枪，但 RoundStart 分配了步枪，玩家持有两把武器

**根因**：RoundStart 的武器分配未清空商店购买的武器

**解决方案**：
1. RoundStart.OnEnter() 中先 `role.ClearInventory()` 清空所有武器
2. 然后分配本回合标准武器
3. 商店购买的应是「消耗品/装备」而非武器，避免冲突

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `Bullfighting=43` 无冲突
- [ ] Factory 双端已注册
- [ ] 复用的 TurnBased RoleLogic 编译正常

### 6.2 配置

- [ ] SOBullFightingModeData 参数合理
- [ ] SOGunfightRoundData 共享配置格式正确
- [ ] 连杀阈值设置合理（SuperKill < LegendaryKill）

### 6.3 运行时

- [ ] 6 阶段正常流转（Born→Info→Shop→RoundStart→RoundEnd→Over）
- [ ] Info 阶段正确展示对手信息
- [ ] 商店购买正常，金钱扣除正确
- [ ] 武器轮换正确
- [ ] 连杀播报在正确阈值触发
- [ ] AI 对手购买行为合理

### 6.4 兼容性

- [ ] 不影响 TurnBased 模式（共享 RoleLogic）
- [ ] 不影响 SOGunfightRoundData 共享配置
- [ ] 自定义房间可启用

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-bullfighting]] · [[TurnBasedMode制作]]
