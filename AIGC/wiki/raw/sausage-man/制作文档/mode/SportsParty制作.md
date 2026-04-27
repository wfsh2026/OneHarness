# 1 代架构运动派对（SportsParty）制作规范

> **适用范围**：SportsParty 运动派对 — 新增竞技地图 / 扩展回合机制 / 调整商店系统
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-sportsparty（68 文件，★★★ 复杂，ExtendGameWorldFeature 架构 + 8-Stage + 多地图 + 商店经济）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **架构差异**：⚠️ 不使用 ClientModeManager，使用 `ExtendGameWorldFeature` + `AbsSportsPartyMgr` 基类

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientSportsPartyMgr (Client 端运动派对主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyMgr.cs
  │  继承: AbsSportsPartyMgr（非 ClientModeManager）
  │  架构: ExtendGameWorldFeature
  │
  ├── Logic 层（5 个）
  │     ClientSportsPartyMainLogic      — 主逻辑协调
  │     ClientSportsPartySyncLogic      — 数据同步
  │     ClientSportsPartyLodMapLogic    — 地图 LOD 管理
  │     ClientSportsPartyShoppingLogic  — 商店 UI 交互
  │     ClientSportsPartyRoundLogic     — 回合管理
  │
  └── SportsPartyMainData（客户端数据）

ServerSportsPartyMgr (Server 端运动派对主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyMgr.cs
  │  继承: AbsSportsPartyMgr
  │
  ├── Logic 层（13 个）★★
  │     ServerSportsPartyMainLogic        — 主逻辑（阶段监听）
  │     ServerSportsPartyTimeLogic        — 时间管理
  │     ServerSportsPartyRoleLogic        — 角色管理
  │     ServerSportsPartyRoundLogic       — 回合逻辑
  │     ServerSportsPartyCoinLogic        — 金币经济 ★
  │     ServerSportsPartyMapLogic         — 地图管理/随机化
  │     ServerSportsPartyShoppingLogic    — 商店逻辑
  │     ServerSportsPartyFightLogic       — 战斗逻辑
  │     ServerSportsPartyGameOverLogic    — 游戏结束
  │     ServerSportsPartyReLoginLogic     — 重连处理
  │     ServerSportsPartyStatisticsLogic  — 统计数据
  │     ServerSportsPartyCheckCheatLogic  — 反作弊
  │     ServerSportsPartyWaitLogic        — 等待逻辑
  │
  └── ServerSportsPartyData

Host 层 — AbsSportsPartyMgr
  │  路径: Assets/Script/GamePlay/Host/Modules/SportsParty/AbsSportsPartyMgr.cs
  │  双 Manager 架构:
  │    SportsPartyDataMgr（数据管理器）
  │    SportsPartyLogicMgr（逻辑管理器）
  │    ISportsPartyMgr（接口约束）
  │
  └── 团队数据: teams Dictionary (team_id → win_point)

专属 Buff 系统
    BSSportsPartyChestClient / BSSportsPartyChestServer — 宝箱 Buff
    BSSportsPartyCoinClient / BSSportsPartyCoinServer   — 金币 Buff
    配置: PB_SportsPartyChest.asset / PB_SportsPartyCoin.asset

多地图系统 ★★
    SOCombatIsland.asset    — 战斗岛
    SORainbowIsland.asset   — 彩虹岛
    SOSupernovaStar.asset   — 超新星
    RandGameArea() — 地图随机化方法
```

### 1.2 Stage 阶段流转

```
8 阶段制（模式最多的 Stage 设计之一）：

GameStart (0)
  │  游戏启动
  ↓
Wait (1)
  │  等待所有玩家
  ↓
TeamShow (2)
  │  队伍展示/阵容预览
  ↓
RoundStart (3) ← 多回合循环入口
  │  新回合开始
  │  随机选择地图
  ↓
Shopping (4) ← ★ 商店经济阶段
  │  玩家使用金币购买装备
  │  CmdSportsPartyReplaceEquip → 购买请求
  │  SportsPartyCoinMessageData → 金币同步
  ↓
Fight (5) ← 核心战斗
  │  团队竞技
  │  宝箱 Buff + 金币 Buff
  │  胜场统计
  │  判定：回合结束 → RoundOver
  ↓
RoundOver (6)
  │  回合结算
  │  胜方积分
  │  判定：是否还有回合 → 有:RoundStart / 无:GameOver
  ↓
GameOver (7)
    最终结算
    MVP 展示
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **服务器配置** | `ServerSportsPartyConfig.asset` | Resources/AB | Init |
| **地图配置** | 3 个地图 SO（CombatIsland/Rainbow/Supernova） | Resources/AB | RoundStart |
| **Buff 配置** | `PB_SportsPartyChest/Coin.asset` | Resources/AB | Fight |
| **掉落物配置** | `SOMonsterItem_SportsParty.asset` | Resources/AB | Fight |
| **地图 Buff 分组** | `PlayBoxBuffGroup/*.asset` (6 个) | Resources/AB | RoundStart |

---

## 二、新建/扩展 Checklist

### Phase 1：新增竞技地图

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `SO{MapName}.asset` | 新建 | 新地图配置 SO |
| 2 | 地图场景 | 新建 | Unity 场景文件 |
| 3 | `ServerSportsPartyMapLogic` | 修改 | 注册新地图到随机池 |
| 4 | `ClientSportsPartyLodMapLogic` | 修改 | 新地图 LOD |

### Phase 2：扩展商店商品

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | 商品配置 | 修改 | 新装备/消耗品 |
| 6 | `ServerSportsPartyShoppingLogic` | 修改 | 购买验证 |
| 7 | `ClientSportsPartyShoppingLogic` | 修改 | 商店 UI |

### Phase 3：新增 Buff 类型

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `BSSportsParty{Buff}Client.cs` | 新建 | 客户端 Buff |
| 9 | `BSSportsParty{Buff}Server.cs` | 新建 | 服务端 Buff |
| 10 | `PB_SportsParty{Buff}.asset` | 新建 | Buff SO 配置 |

---

## 三、配置文件详解

### 3.1 服务器主配置（ServerSportsPartyConfig）

```csharp
// Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyConfig.cs
[CreateAssetMenu(menuName = "War/Mode/ServerSportsPartyConfig")]
public sealed class ServerSportsPartyConfig : ScriptableObject {
    public List<SportsPartyStage> sportsPartyStages;   // 8 阶段时间配置
    public List<SportsPartyRound> sportsPartyRounds;   // 各回合胜利奖励
    public uint maxCoinNum;                             // 金币上限
    public uint killReward;                             // 击杀奖励金币
    public int bulletNum = 240;                         // 步枪子弹数
    public int pistolBulletNum = 90;                    // 手枪子弹数
    public string defaultPistolSign = "P18C";           // 默认手枪 Sign
    public RoundItem[] roundItem;                       // 回合初始装备
    public int bondageNum = 5;                          // 绷带数量
    public List<string> glass;                          // 瞄准镜列表
    public int MaxScore = 25200;                        // Elo 积分上限
    public FactorItem[] factorItems;                    // 模式系数（跨模式匹配用）

    [Serializable]
    public sealed class SportsPartyStage {
        public string stageName;    // 阶段名称
        public float waitTime;      // 阶段持续秒数
    }

    [Serializable]
    public sealed class SportsPartyRound {
        public int round;           // 回合编号
        public uint reward;         // 胜方奖励金币
    }

    [Serializable]
    public struct RoundItem {
        public string head;    // 头部装备 Sign
        public string pack;    // 背包装备 Sign
        public string armor;   // 护甲装备 Sign
    }

    [Serializable]
    public struct FactorItem {
        public WarData.GameMode gameMode;
        public float factor;   // Elo 计算系数
    }
}
```

> **注意**：地图信息通过 `SportsPartyMapInfo`（MonoBehaviour，挂载于场景）管理，使用 `Dictionary<string, Dictionary<int, GameObject>>` 按地图名和索引存储地图对象，而非独立 SO 配置。

### 3.2 8-Stage 阶段流转枚举

```csharp
// Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyDefine.cs
public enum SportsPartyStage {
    GameStart  = 0,   // 游戏开始初始化
    Wait       = 1,   // 等待玩家就绪
    TeamShow   = 2,   // 阵容展示
    RoundStart = 3,   // 回合开始
    Shopping   = 4,   // 商店购买阶段
    Fight      = 5,   // 战斗阶段
    RoundOver  = 6,   // 回合结算
    GameOver   = 7,   // 全局结算
}
```

**阶段流转链**（`ServerSportsPartyTimeLogic` 硬编码）：

```
GameStart → Wait → TeamShow → RoundStart → Shopping → Fight → RoundOver
                                   ↑                              │
                                   └──────── 循环至 maxRounds ────┘
                                                                  ↓
                                                              GameOver
```

每个阶段的持续时间从 `ServerSportsPartyConfig.sportsPartyStages[i].waitTime` 读取。

### 3.3 金币经济系统

| 金币来源 | 实现 | 说明 |
|---------|------|------|
| 击杀敌人 | `ServerSportsPartyCoinLogic` | 固定 `killReward` 值 |
| 地图拾取 | `BSSportsPartyCoinServer` | 距离 < `pickRange` 触发，奖励 `coinNum` |
| 宝箱 | `BSSportsPartyChestServer` | Init 时在 `lockPoints` 生成视觉效果 |
| 回合胜利 | `SportsPartyRound.reward` | 按回合编号递增 |

| 金币消耗 | CMD 消息 | 说明 |
|---------|---------|------|
| 替换装备 | `CmdSportsPartyReplaceEquip`（24002） | 替换当前武器 |
| 购买道具 | `CmdSportPartyBuyItem`（24005） | 购买消耗品 |
| 出售道具 | `CmdSportPartySellItem`（24006） | 回收金币 |
| 升级武器 | `CmdSportsPartyUpgradeWeapon`（24007） | 武器升阶 |
| 降级武器 | `CmdSportsPartyDemotionWeapon`（24008） | 武器降阶（可能自动触发） |

> **金币上限**：`maxCoinNum` 防止无限堆积，所有金币变动通过 `TargetRpcSportsPartyCoinChange` 同步到客户端。

### 3.4 地图配置（3 张竞技地图）

| 地图索引 | 地图名 | 场景 Prefab Key |
|---------|--------|----------------|
| 0 | CombatIsland | 战斗岛 |
| 1 | RainbowIsland | 彩虹岛 |
| 2 | SupernovaStar | 超新星 |

- **随机选择**：`ServerSportsPartyMapLogic` 从 3 张地图中随机（不重复上一张）
- **LOD 加载**：`ClientSportsPartyLodMapLogic` 负责地图 LOD 管理
- **出生点**：每张地图按队伍索引（红/蓝）配置不同出生位置

### 3.5 网络协议表（Proto_SportsParty，API_ID = 24）

#### 服务端 → 客户端（RPC/TargetRpc）

| 消息名 | ID | 用途 | 关键字段 |
|--------|-----|------|---------|
| `RpcSendSportsPartyGameOverData` | 24001 | 游戏结束广播 | `SportsPartyGameOverSyncMessageData` |
| `TargetRpcSportsPartyLookLogin` | 24003 | 观战者登录 | `SportsPartyLookLoginMessageData` |
| `RpcSendCompensateTeam` | 24004 | 罚时队伍列表 | `compensateTeam: string[]` |
| `TargetRpcSportsPartyLevel` | 24009 | 装备等级更新 | `autoRoleId, autoId, level` |
| `RpcSportsPartyStageChange` | 24010 | **阶段切换** | `stage: SportsPartyStage` |
| `RpcSportsPartyCoinPickup` | 24011 | 金币拾取事件 | `SportsPartyCoinMessageData` |
| `RpcSportsPartyRoundChange` | 24012 | **回合更新** | `SportsPartyRoundSyncMessageData` |
| `TargetRpcSportsPartyCoinChange` | 24013 | 个人金币同步 | `SportsPartyCoinSyncMessageData` |
| `RpcSportPartyMaxNum` | 24014 | 队伍最大人数 | `num, mapIndex, endTime` |
| `RpcSportsPartyShoppingEndTime` | 24015 | 商店倒计时 | `endTime: long` |
| `TargetRpcSportsPartyReLoginData` | 24016 | **重连数据** | `SportsPartyReLoginMessageData` |

#### 客户端 → 服务端（CMD）

| 消息名 | ID | 用途 | 关键字段 |
|--------|-----|------|---------|
| `CmdSportsPartyReplaceEquip` | 24002 | 装备替换 | `buyStruct, playerId` |
| `CmdSportPartyBuyItem` | 24005 | 购买道具 | `buyStruct, playerId, coin` |
| `CmdSportPartySellItem` | 24006 | 出售道具 | `sellStruct, playerId, coin` |
| `CmdSportsPartyUpgradeWeapon` | 24007 | 武器升级 | `buyStruct, playerId, coin` |
| `CmdSportsPartyDemotionWeapon` | 24008 | 武器降级 | `buyStruct, playerId, coin` |

### 3.6 服务端消息常量（ServerConstants）

| 常量范围 | 说明 | 示例 |
|---------|------|------|
| 300001-300009 | 阶段与核心事件 | `OnSportsPartyStageChange`(300001)、`OnSportsPartyReLogin`(300009) |
| 310001-310012 | 商店与经济事件 | `OnSportsPartyCoinPickup`(310001)、`OnSportsPartyReplaceEquip`(310012) |

---

## 四、关键代码修改点

### 4.1 ExtendGameWorldFeature 架构（与 ModeManager 不同）

```csharp
// SportsParty 不使用 ClientModeManager，使用 ExtendGameWorldFeature
public abstract class AbsSportsPartyMgr {
    protected SportsPartyDataMgr dataMgr;   // 数据管理
    protected SportsPartyLogicMgr logicMgr; // 逻辑管理
    
    // 服务端 13 个 Logic：Main/Time/Role/Round/Coin/Map/Shopping/Fight/
    //                    GameOver/ReLogin/Statistics/CheckCheat/Wait
    // 客户端 5 个 Logic：Main/Sync/LodMap/Shopping/Round
}
```

### 4.2 阶段流转引擎（ServerSportsPartyTimeLogic）

```csharp
// 硬编码阶段流转映射
private readonly Dictionary<int, int> nextStageDict = new Dictionary<int, int> {
    { (int)SportsPartyStage.GameStart, (int)SportsPartyStage.Wait },
    { (int)SportsPartyStage.Wait,      (int)SportsPartyStage.TeamShow },
    { (int)SportsPartyStage.TeamShow,  (int)SportsPartyStage.RoundStart },
    { (int)SportsPartyStage.RoundStart,(int)SportsPartyStage.Shopping },
    { (int)SportsPartyStage.Shopping,  (int)SportsPartyStage.Fight },
    { (int)SportsPartyStage.RoundOver, (int)SportsPartyStage.RoundStart },  // 循环
};

// 阶段切换：从 SO 配置读取 waitTime，计算结束时间后广播
private void IntoNextStage(SportsPartyStage stage) {
    waitTimes.TryGetValue((int)stage, out var waitTime);
    stageEndTime = sportsPartyMgr.GameWorld.MyStartGame.ServerTime + (int)waitTime;
    mainData.SetSportsPartyStage(stage);
    sportsPartyMgr.DispatchMessage(ServerConstants.OnSportsPartyStageChange, stage);
    ServerSportsPartyNet.SendSportsPartyStageChange(sportsPartyMgr, stage);
}
```

> **新增阶段**：修改 `nextStageDict` 添加新的阶段跳转，并在 SO 配置中添加对应 waitTime。

### 4.3 积分与 MVP 系统

```csharp
// 积分公式（Elo 类型）— SportPartyGameScoreFormulaUtil
var totalScore = SportPartyGameScoreFormulaUtil.GetTotalScore(
    WarData.GameMode.SportsPartyMode,
    roleLogic,           // 角色数据
    winTeamPlayerCount,  // 胜队人数
    teamRank             // 队伍排名
);
// totalScore 上限 = ServerSportsPartyConfig.MaxScore (25200)
```

**MVP 评选规则**（`ServerSportsPartyGameOverLogic`，多级排序）：

1. 击杀数（kills）— 最高优先
2. 伤害量（damage）— 次优先
3. 助攻数（assists）— 第三优先
4. 死亡数（deaths）— 最少优先（反向排序）

### 4.4 地图加载与出生点

```csharp
// 客户端 LOD 地图加载 — ClientSportsPartyLodMapLogic
// 使用 SportsPartyMapInfo（场景 MonoBehaviour）管理地图对象
// Dictionary<string, Dictionary<int, GameObject>> 按地图名+索引存储

// 出生点按队伍分配
// 红队/蓝队各有独立 birthPosition 列表，按 mapIndex 索引
```

**3 张地图的随机规则**：`ServerSportsPartyMapLogic` 在每回合开始时随机选择，排除上一回合使用的地图，确保不连续重复。

### 4.5 重连恢复系统（ServerSportsPartyReLoginLogic）

```csharp
// 玩家重连 — 完整恢复所有状态
public void ReLogin(RoleNet roleNet) {
    var data = new SportsPartyReLoginMessageData {
        stage            = mainData.Stage,                    // 当前阶段
        compensateTeams  = mainData.GetCompensateTeam(),      // 罚时队伍
        coinSyncData     = GetCoinSyncMessageData(playerId),  // 恢复金币（含各奖励类型明细）
        roundSyncData    = GetRoundSyncMessageData(),         // 恢复回合（胜利点数/当前回合/开始时间）
        gameOverSyncData = GetGameOverSyncMessageData(),      // 恢复结算数据
        mapIndex         = sportsPartyMgr.GameWorld.SportsPartyIndex,
    };
    ServerSportsPartyNet.SendSportsPartyReLoginData(sportsPartyMgr, roleNet, data);
}

// 观战者登录 — 精简数据
public void LookLogin(RoleNet roleNet) {
    var data = new SportsPartyLookLoginMessageData {
        stage         = mainData.Stage,
        roundSyncData = GetRoundSyncMessageData(),
        mapIndex      = sportsPartyMgr.GameWorld.SportsPartyIndex,
        shoppingEndTime = sportsPartyMgr.GetSportsPartyLogic<ServerSportsPartyShoppingLogic>()
            .shoppingEndTime,
    };
    // 通过 TargetRpc 发送
}
```

**重连数据结构**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `stage` | `SportsPartyStage` | 当前阶段 |
| `compensateTeams` | `string[]` | 罚时队伍 ID |
| `coinSyncData` | `SportsPartyCoinSyncMessageData` | 总金币 + 各奖励类型明细 |
| `roundSyncData` | `SportsPartyRoundSyncMessageData` | 各队胜利点数、当前回合、开始时间、胜方 |
| `gameOverSyncData` | `SportsPartyGameOverSyncMessageData` | 结算数据（可为空） |
| `mapIndex` | `int` | 当前地图索引 |

### 4.6 金币 Buff 系统（战场拾取）

```csharp
// BSSportsPartyCoinServer — 地图金币拾取
public override void OnUpdate() {
    foreach (var roleLogic in onlineRoleLogics) {
        if (roleLogic.GetState(RoleSyncState.IsWeak)) continue;  // 倒地不可拾取
        
        var distance = Vector3.Distance(roleLogic.NowPoint, MyBuffBox.nowPoint);
        if (distance < buffSOData.pickRange) {
            // 触发 OnSportsPartyCoinPickup 消息
            MyBuffBox.isClear = true;  // 销毁 Buff 盒子
        }
    }
}

// BSSportsPartyChestServer — 宝箱
public override void Init(BuffSystemBase buffSystem) {
    // 在 lockPoints 位置播放 goodsBoxSign 视觉效果
    MyBuffControl.PlayBuff(buffSOData.goodsBoxSign, MyBuffBox.lockPoints, 0, 0, "");
}

// BSSportsPartyChestClient — 客户端宝箱（小地图标记）
public override void Init(BuffSystemBase buffSystem) {
    // 通过 OnSportsPartyMapInfoShow 消息在小地图显示宝箱图标
    var data = new SportsPartyMapInfoMessageData {
        buffId = MyBuffBox.autoBuffId,
        mapInfoBoxSign = buffSOData.mapInfoBoxSign,
        point = MyBuffBox.lockPoints[0]
    };
}
```

---

## 五、常见问题与踩坑记录

### 5.1 回合间地图切换加载卡顿

**现象**：RoundOver → RoundStart 切换地图时长时间黑屏

**根因**：整个地图场景卸载+加载

**解决方案**：使用 LOD 系统（`ClientSportsPartyLodMapLogic`）预加载下一张地图

### 5.2 商店购买后金币不同步

**现象**：购买装备后金币显示错误

**根因**：Client 直接扣除金币但 Server 购买失败后未回滚

**解决方案**：Client 使用乐观更新 + Server 确认回调，失败时回滚

### 5.3 多回合积分累计错误

**现象**：多回合后某队伍积分与实际不符

**根因**：`teams Dictionary` 在重连 (`ReLoginLogic`) 后未正确同步

**解决方案**：重连时从 Server 完整同步团队数据

---

## 六、验收标准

- [ ] 8 阶段正常流转
- [ ] 多回合循环正确（RoundStart → Shopping → Fight → RoundOver → 循环）
- [ ] 3 张地图随机选择且不连续重复
- [ ] 商店购买/出售正常
- [ ] 金币经济正确（获取/消耗/同步）
- [ ] 团队积分正确累计
- [ ] 宝箱/金币 Buff 正常
- [ ] 重连后状态正确恢复
- [ ] 反作弊检测正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-sportsparty]]
