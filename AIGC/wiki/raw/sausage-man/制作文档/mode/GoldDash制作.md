# 1 代架构淘金热/撤离（GoldDash）制作规范

> **适用范围**：GoldDash 淘金热/撤离模式 — 新增 Boss / 扩展撤离点 / 调整宝箱/黑市/祭坛
> **不适用**：通用模式框架 → 归 [[模式制作]]；快速撤离变体 → 归 [[GoldDashFast制作]]
> **参考实现**：mode-golddash（251 文件，★★★★★ 最复杂，26 Client Logic + 43 Server Logic + 多专属子系统）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **GameMode 枚举**：`GoldDash=2`
> **Proto API_ID**: 52

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientGoldDashMgr (Client 端淘金热主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/ClientGoldDashMgr.cs
  │  继承: ClientModeManager（79 行，26 个 Logic，3 个 Stage）
  │  核心属性: ClientGoldDashData data, ClientGoldDashBackpack Backpack
  │
  ├── Client Logic（26 个）★★★★
  │     ├── 核心系统
  │     │   ClientGoldDashBornLogic          — 出生点管理
  │     │   ClientGoldDashRoleLogic          — 角色逻辑
  │     │   ClientGoldDashSceneLogic         — 场景管理
  │     │   ClientGoldDashGameOverMsgLogic   — 游戏结束信息
  │     │
  │     ├── 撤离系统
  │     │   ClientGoldDashEscapePointLogic   — 撤离点 UI/进出检测 ★
  │     │
  │     ├── 背包/金库系统
  │     │   ClientGoldDashBackpack           — 背包管理（容量/装备/武器部件）★
  │     │   ClientGoldDashBlackMarketLogic   — 黑市随机事件
  │     │
  │     ├── 宝箱系统
  │     │   ClientGoldDashBoxLogic           — 宝箱状态/UI
  │     │
  │     ├── 祭坛/Boss
  │     │   ClientGoldDashAltarLogic         — 祭坛系统
  │     │   ClientGoldDashBossRushLogic      — Boss Rush 模式
  │     │
  │     ├── 怪物/AI
  │     │   ClientGoldDashMonsterLogic       — 怪物显示/标记
  │     │   ClientGoldDashSausage2Logic      — 特殊角色逻辑
  │     │
  │     ├── 任务/事件
  │     │   ClientGoldDashInGameEventMgr     — 游戏内事件
  │     │   ClientGoldDashInGameTaskMgr      — 游戏内任务
  │     │   ClientGoldDashMermaidTaskTipsLogic — 人鱼任务提示
  │     │
  │     ├── 引导/教程
  │     │   ClientGoldDashRookieGuideLogic   — 新手引导
  │     │   ClientGoldDashTutorialLogic      — 教程主逻辑
  │     │   ClientGoldDashTutorialMap/Escape/AIBattle — 教程分支
  │     │
  │     ├── 表现
  │     │   ClientGoldDashDeadModelLogic     — 死亡模式特效
  │     │   ClientGoldDashMapInfoLogic       — 地图信息 UI
  │     │   ClientGoldDashItemOutLineLogic   — 物品轮廓渲染
  │     │   ClientGoldDashAirdropLogic       — 空投系统
  │     │   ClientGoldDashKeyRoomLogic       — 关键房间交互
  │     │
  │     └── 15+ 其他 Logic
  │
  ├── Stage（3 阶段）
  │     BornStage → RunningStage → OverStage
  │
  └── ClientGoldDashData（含 6 个 SO 配置引用）

ServerGoldDashMgr (Server 端淘金热主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/ServerGoldDashMgr.cs
  │  继承: ServerModeManager（107 行，43 个 Logic，3 个 Stage）
  │
  ├── Server Logic（43 个）★★★★★（全项目最多）
  │     ├── 核心系统
  │     │   ServerGoldDashRoleInitLogic       — 角色初始化
  │     │   ServerGoldDashDeadLogic           — 死亡/复活
  │     │   ServerGoldDashGameOverLogic       — 游戏结束判定
  │     │   ServerGoldDashModeAwardLogic      — 奖励计算
  │     │   ServerGoldDashStatisticsLogic     — 统计系统 ★
  │     │   ServerGoldDashNsqDataLogic        — NSQ 同步
  │     │   ServerGoldDashLookLogic           — 房间查询
  │     │
  │     ├── 撤离系统
  │     │   ServerGoldDashEscapePointLogic         — 撤离逻辑/判定 ★
  │     │   ServerGoldDashEscapePointCreateLogic   — 撤离点生成/位置分配
  │     │
  │     ├── 宝箱系统 ★★
  │     │   ServerGoldDashBoxLogic            — 宝箱逻辑（掉落/保护）
  │     │   ServerGoldDashBoxCreateLogic      — 宝箱创建/位置
  │     │   ServerGoldDashRandomBoxLogic      — 随机宝箱
  │     │   ServerGoldDashItemEntryLogic      — 物品注入
  │     │   宝箱子类型: Common/Boss/DeadBox/Drone/AirThrow/Jrone
  │     │
  │     ├── Boss 系统 ★★
  │     │   ServerGoldDashBossAllocateLogic   — Boss 分配/随机化
  │     │   ServerGoldDashBossJokerLogic      — Joker Boss
  │     │   ServerGoldDashBossOctopusLogic    — Octopus Boss
  │     │   ServerGoldDashBossAirWallLogic    — Boss 空气墙
  │     │   ServerGoldDashBossRushLogic       — Boss Rush 模式
  │     │
  │     ├── AI/怪物系统
  │     │   ServerGoldDashAICreateLogic       — AI 敌人创建
  │     │   ServerGoldDashMapMonsterLogic     — 怪物地图分布
  │     │   ServerAIFightSessionComponent     — AI 战斗会话
  │     │   PveAIBehaviorHelper              — AI 行为树
  │     │
  │     ├── 祭坛/黑市
  │     │   ServerGoldDashAltarLogic          — 祭坛 Boss 覆盖
  │     │   ServerGoldDashBlackMarketLogic    — 黑市事件/金价
  │     │
  │     ├── 可交互系统
  │     │   ServerGoldDashInteractableLogic   — 可交互物体
  │     │   ServerGoldDashInteractTreasuryHouseLogic — 金库互动
  │     │
  │     ├── 游戏事件
  │     │   ServerGoldDashInGameEventMgr      — 事件管理
  │     │   ServerGoldDashMermaidTaskDriver   — 人鱼任务
  │     │   ServerInGameEventConditionLogic   — 条件判定
  │     │   事件类型: SearchClue/MonsterSquad/MoreRewards
  │     │
  │     └── 20+ 其他 Logic（结算/空投/难度/等）
  │
  └── ServerGoldDashData（含 5 个 SO 配置引用）

Host 层
    Proto_GoldDash — 网络协议（API_ID=52，30+ 消息）
    HostFastGoldDashRoleShopInfo / HostFastGoldDashRoleSkillsInfo
    HostFastGoldDashShopSuitInfo

继承关系
    FastGoldDash(快速撤离) 继承 GoldDash:
      ClientFastGoldDashMgr → ClientGoldDashMgr
      ServerFastGoldDashMgr → ServerGoldDashMgr
      复用 70% Logic + 4 个专属 Logic
```

### 1.2 Stage 阶段流转

```
3 阶段制（简洁但内容最丰富）：

Born (出生)
  │  初始化地形
  │  加载配置（6 个 SO）
  │  生成角色
  │  关闭补人
  │  SimulateOpenBox
  │  发送 Grpc 消息
  ↓
Running (运行中) ← 核心（所有子系统活跃）
  │  ┌─ 撤离系统: 撤离点生成 → 进入检测 → 撤离判定
  │  ├─ 宝箱系统: 随机生成 → 开启 → 掉落
  │  ├─ Boss 系统: Boss 分配 → Boss 战 → Boss Rush
  │  ├─ AI 系统: AI 创建 → 行为树 → 战斗
  │  ├─ 祭坛: Boss 属性覆盖
  │  ├─ 黑市: 金价波动 → 交易
  │  ├─ 事件: 人鱼任务 / 搜索线索 / 怪物小队
  │  ├─ 空投: 空投投放 → 争夺
  │  └─ 金库: 互动 → 收益
  │  判定：GameOver 条件满足
  ↓
Over (结束)
    结算清理
    统计数据上报
    奖励计算
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOGoldDashModeConfig` | Resources/AB | Init |
| **物品点位** | `SOGoldDashItemPoint` | Resources/AB | Init |
| **背包配置** | `SOGoldDashBackpackFullRatio` | Resources/AB | Init |
| **小地图** | `SOGoldDashMiniMapArea` | Resources/AB | Init |
| **Boss Rush** | `SOGoldDashBossRush` | Resources/AB | Running |
| **可交互物** | `SOGoldDashInteractPropPos` | Resources/AB | Running |
| **AI 配置** | `SOGoldDashAIConfig` | Resources/AB | Running |
| **可交互数据** | `SOGoldDashInteractData` | Resources/AB | Running |
| **新手积分** | `SOGoldDashBeginnerScore` | Resources/AB | Running |
| **过渡积分** | `SOGoldDashAdaptScore` | Resources/AB | Running |
| **温暖值** | `SOGoldDashEncourageScore` | Resources/AB | Running |
| **祭坛 Boss** | `AltarMatchModeConfig` | Resources/AB | Running |

---

## 二、新建/扩展 Checklist

### Phase 1：新增 Boss

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `ServerGoldDashBoss{Name}Logic.cs` | 新建 | Boss 逻辑 |
| 2 | `ServerGoldDashBossAllocateLogic.cs` | 修改 | 注册新 Boss |
| 3 | `AltarMatchModeConfig` | 修改 | 祭坛 Boss 配置 |
| 4 | Boss Prefab + AI | 新建 | 模型/动画/行为树 |

### Phase 2：扩展撤离系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `ServerGoldDashEscapePointCreateLogic` | 修改 | 新撤离点位置 |
| 6 | `ServerGoldDashEscapePointLogic` | 修改 | 撤离规则 |
| 7 | `ClientGoldDashEscapePointLogic` | 修改 | 撤离 UI |

### Phase 3：扩展宝箱类型

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | 新宝箱子类型 | 新建 | 继承宝箱基类 |
| 9 | `ServerGoldDashBoxCreateLogic` | 修改 | 生成规则 |
| 10 | `ServerGoldDashBoxLogic` | 修改 | 掉落表 |

### Phase 4：新增游戏事件

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | 事件 Driver | 新建 | 类似 MermaidTaskDriver |
| 12 | `ServerGoldDashInGameEventMgr` | 修改 | 注册新事件 |
| 13 | `ServerInGameEventConditionLogic` | 修改 | 触发条件 |

---

## 三、配置文件详解

### 3.1 Client 配置引用（6 个 SO）

| SO 类型 | 字段名 | 说明 |
|---------|--------|------|
| `SOGoldDashModeConfig` | Config | 模式主配置 |
| `SOGoldDashItemPoint` | ItemPointConfig | 物品点位 |
| `SOGoldDashBackpackFullRatio` | BackpackConfig | 背包满度比例 |
| `SOGoldDashMiniMapArea` | MiniMapAreaConfig | 小地图区域 |
| `SOGoldDashBossRush` | BossRushConfig | Boss Rush 参数 |
| `SOGoldDashInteractPropPos` | InteractPropPos | 可交互物位置 |

### 3.2 Server 配置引用（5 个 SO）

| SO 类型 | 字段名 | 说明 |
|---------|--------|------|
| `SOGoldDashAIConfig` | GoldDashAIConfig | AI 行为配置 |
| `SOGoldDashInteractData` | GoldDashInteractData | 可交互数据 |
| `SOGoldDashBeginnerScore` | BeginnerScoreConfig | 新手积分配置 |
| `SOGoldDashAdaptScore` | AdaptScoreConfig | 过渡局积分 |
| `SOGoldDashEncourageScore` | EncourageScore | 温暖值积分 |

### 3.3 难度系统

```csharp
public enum GoldDashModeDifficultType {
    Easy,       // 简单 — 低等级玩家
    Normal,     // 普通
    Hard,       // 困难
    Extreme     // 极限
}
```

---

## 四、关键代码修改点

### 4.1 撤离流程

```csharp
// 服务端撤离判定
public class ServerGoldDashEscapePointLogic {
    public void OnPlayerEnterEscapePoint(int roleId) {
        // CmdEnterOrQuitEscapePoint → 进入撤离区
        escapeData[roleId].isInArea = true;
        escapeData[roleId].enterTime = Time.time;
        
        // 广播其他玩家
        SendRpc(new RpcEnterOrQuitEscapePoint { roleId = roleId, enter = true });
    }
    
    public void CheckEscapeSuccess(int roleId) {
        if (escapeData[roleId].stayTime >= config.escapeTime) {
            // 撤离成功！
            var reward = CalculateReward(roleId);
            SendRpc(new RpcGoldDashEscapeSuccess { roleId = roleId, reward = reward });
            OnPlayerEscaped(roleId);
        }
    }
}
```

### 4.2 宝箱系统

```csharp
// 宝箱子类型系统
public enum GoldDashBoxType {
    Common,     // 普通宝箱
    Boss,       // Boss 宝箱
    DeadBox,    // 死亡掉落箱
    Drone,      // 无人机宝箱
    AirThrow,   // 空投箱
    Jrone       // 特殊宝箱
}

// 死亡保护机制
public void OnPlayerDead(int roleId) {
    var deadBox = CreateBox(GoldDashBoxType.DeadBox, roleId);
    deadBox.protectionTime = 30f;  // 30 秒保护
    deadBox.contents = player.Backpack.Items;
}
```

### 4.3 Boss 分配

```csharp
public class ServerGoldDashBossAllocateLogic {
    public void AllocateBoss() {
        var availableBosses = new List<BossType> {
            BossType.Joker,
            BossType.Octopus,
            // 新 Boss 在此注册
        };
        
        // 随机分配 Boss
        var selected = availableBosses[Random.Range(0, availableBosses.Count)];
        
        // 祭坛覆盖检查
        if (altarConfig.HasOverride(matchMode)) {
            selected = altarConfig.GetOverrideBoss(matchMode);
        }
        
        SpawnBoss(selected);
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 撤离点位置与安全区冲突

**现象**：撤离点生成在缩圈外或不可达区域

**根因**：`ServerGoldDashEscapePointCreateLogic` 的位置算法未考虑动态安全区

**解决方案**：生成撤离点时检查安全区边界，确保在当前安全区内且可达

### 5.2 宝箱保护机制导致资源堆积

**现象**：大量死亡掉落箱 30 秒保护后无人拾取，场景内宝箱过多

**根因**：`DeadBox` 保护期结束后仍然存在，无超时清理

**解决方案**：DeadBox 设置总存活时间（如 120 秒），超时自动销毁

### 5.3 Boss 分配后玩家断线重连 Boss 消失

**现象**：重连后 Boss 不在场景中

**根因**：Boss 实体在 Server 存在但重连时 Client 未收到 Boss 创建消息

**解决方案**：重连时从 ServerGoldDashData 完整同步所有活跃 Boss 状态

### 5.4 43 个 Server Logic 初始化顺序依赖

**现象**：某些 Logic 初始化时依赖的其他 Logic 尚未初始化

**根因**：Logic 添加顺序不当，存在隐式依赖

**解决方案**：明确 Logic 初始化顺序文档，或使用延迟初始化（LazyInit）模式

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error（251 文件）
- [ ] 所有 SO 配置引用正确

### 6.2 核心系统

- [ ] 3 阶段正常流转
- [ ] 撤离系统：撤离点生成/进入/停留/撤离成功
- [ ] 宝箱系统：6 种类型正确生成/开启/掉落
- [ ] 死亡掉落箱 30 秒保护机制

### 6.3 Boss 系统

- [ ] Boss 分配正确（Joker/Octopus）
- [ ] 祭坛 Boss 属性覆盖
- [ ] Boss Rush 模式
- [ ] Boss 空气墙正常

### 6.4 经济系统

- [ ] 背包管理（容量/装备/武器部件）
- [ ] 黑市金价波动/交易
- [ ] 金库互动
- [ ] 积分计算（新手/过渡/温暖值）

### 6.5 其他

- [ ] AI 敌人行为正常
- [ ] 游戏内事件触发（人鱼/搜索/怪物小队）
- [ ] 新手引导/教程完整
- [ ] Proto 52 协议正常（30+ 消息）
- [ ] 难度等级正确影响

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-golddash]] · [[GoldDashFast制作]]
