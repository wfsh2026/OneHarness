# 1 代架构极速淘金（GoldDash-Fast）制作规范

> **适用范围**：GoldDash-Fast 极速淘金模式 — GoldDash 的 Best-of-X 回合制竞技变体
> **不适用**：完整版 GoldDash → 归 [[GoldDash制作]]；通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-golddash-fast（22+ 自有文件 + 复用 GoldDash ~40 个 Logic，★★ 中等复杂度，GoldDash 子类变体）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **特殊依赖**：**继承** [[GoldDash制作]] 的管理器（ServerGoldDashMgr / ClientGoldDashMgr），复用其大量 Logic

---

## 一、架构概述

### 1.1 核心类依赖

```
★ 关键设计：FastGoldDash 不是独立模式，是 GoldDash 的子类变体

ServerFastGoldDashMgr : ServerGoldDashMgr  ← 继承 GoldDash 主管理器
  ├── ServerFastGoldDashData / EventId
  ├── Stage（5）: Born → [Shop → RoundStart → RoundEnd]×N → Over
  ├── Override Logic（6）: BornLogic, RoleLogic, AwardLogic, NsqDataLogic, StatisticsLogic, LookLogic
  └── 新增 Logic（3）: SkillLogic, ShopLogic, AirWallLogic

ClientFastGoldDashMgr : ClientGoldDashMgr  ← 继承 GoldDash 主管理器
  ├── ClientFastGoldDashData / EventId / FastGoldDashModeStage(enum)
  ├── Stage（5）: Born / Shop / RoundStart / RoundEnd / Over
  └── Logic: ClientFastGoldDashPanelLogic（回合 UI 面板）

Host 端（4）: HostFastGoldDashClass / RoleShopInfo / RoleSkillsInfo / ShopSuitInfo
Config（4）: GoldDashFastSportsSuitConfig / ContentConfig / Partial×2
SO: SOFastGoldDashConfig
```

#### 复用的 GoldDash Logic（Server 端 32 个）

以下 32 个 Logic 通过继承 ServerGoldDashMgr 直接复用，**不做修改**：

> MapIconLogic, SceneLogic, ItemEntryLogic, ItemCreateLogic, RoleInitLogic, DeadLogic, RoleLogic, RandomBoxLogic, BoxLogic, EscapePointLogic, BoxCreateLogic, EscapePointCreateLogic, NsqDataLogic, GameOverLogic, ModeAwardLogic, PortablePointLogic, Sausage2Logic, AirThrowLogic, PickAuthoringLogic, KeyRoomLogic, BossAllocateLogic, AICreateLogic, MapMonsterLogic, StatisticsLogic, BackpackFullLogic, SimulateOpenBoxLogic, InteractTreasuryHouseLogic, InteractableLogic, LoginErrorLogic, RewardTaskLogic, TutorialLogic, BossJokerLogic
>
> （均带 `ServerGoldDash` 前缀）

#### 被移除的 GoldDash 特性（14 个）

**Server 端移除（4）**：BornLogic（→FastBornLogic替代）、LookLogic（→FastLookLogic替代）、**AltarLogic**（祭坛不适用回合制）、**InGameEventTrack**（事件系统不适用）

**Client 端移除（10）**：AltarLogic、RookieGuideLogic、RunningStage（→回合阶段替代）、InGameEventMgr、MermaidTaskTipsLogic、InGameTaskMgr、RoleLogic、SceneLogic、**BlackMarketLogic**、**BossRushLogic**

### 1.2 Stage 阶段流转

```
GoldDash:     Born → Running → Over（线性单局）
FastGoldDash: Born → [Shop → RoundStart → RoundEnd]×N → Over（回合循环）

Born → 初始化，分配出生点（BornGroupDatas），加载 SOFastGoldDashConfig
  ↓
┌─ 回合循环（最多 MaxRoundTimes=7）──────────────────┐
│ Shop(25s) → 购买装备(SuitConfig) / 技能 / 免费刷新1次 │
│ RoundStart(90s) → 空气墙激活 / 击杀助攻开箱 → 积分   │
│ RoundEnd → 结果2s + 积分5s → 先赢3局? Over : Shop   │
└───────────────────────────────────────────────────┘
  ↓
Over → 最终排名 / 奖励结算(AwardLogic) / NSQ上报 / 结果显示2s
```

### 1.3 预制体与资源加载

| 资源 | SO/Config | 加载时机 |
|------|-----------|---------|
| **模式核心配置** | `SOFastGoldDashConfig` | Init() |
| **商店套装** | `GoldDashFastSportsSuitConfig` | Shop 阶段 |
| **套装内容** | `GoldDashFastSportsSuitContentConfig` | Shop 阶段 |
| **GoldDash 共享资源** | 继承父类自动加载 | Init() |

### 1.4 禁止修改的文件

- **GoldDash 父类文件** — ServerGoldDashMgr / ClientGoldDashMgr 及其 Logic 不可修改
- **GameMode.cs** 已有枚举值
- **复用的 32 个 Server Logic** — 通过继承复用，禁止为 Fast 修改原版

---

## 二、新建/扩展 Checklist

### Phase 1：核心框架（6 文件）

| # | 文件 | 说明 |
|---|------|------|
| 1 | `SOFastGoldDashConfig.asset` | 回合时间/积分/商店参数 |
| 2 | `ServerFastGoldDashMgr.cs` | 继承 ServerGoldDashMgr，注册 Stage 和 Logic |
| 3 | `ClientFastGoldDashMgr.cs` | 继承 ClientGoldDashMgr，注册 Stage 和 Logic |
| 4 | `ServerFastGoldDashData.cs` | 回合状态、积分、商店数据 |
| 5 | `ClientFastGoldDashData.cs` | 客户端回合数据 |
| 6 | `FastGoldDashModeStage.cs` | 枚举: Born/Shop/RoundStart/RoundEnd/Over |

### Phase 2：Stage 层（10 文件）

| # | 文件 | 说明 |
|---|------|------|
| 7-11 | Server 5 个 Stage | BornStage / ShopStage(25s) / RoundStartStage(90s) / RoundEndStage / OverStage |
| 12-16 | Client 5 个 Stage | 客户端阶段表现（与 Server 对应） |

### Phase 3：Logic 层（10 文件）

| # | 文件 | 类型 | 说明 |
|---|------|------|------|
| 17 | `ServerFastGoldDashBornLogic` | override | 回合重置出生 |
| 18 | `ServerFastGoldDashRoleLogic` | override | 每回合角色管理 |
| 19 | `ServerFastGoldDashAwardLogic` | override | 回合制奖励 |
| 20 | `ServerFastGoldDashNsqDataLogic` | override | 回合 NSQ 上报 |
| 21 | `ServerFastGoldDashStatisticsLogic` | override | 回合 + 系列统计 |
| 22 | `ServerFastGoldDashLookLogic` | override | 回合观战 |
| 23 | `ServerFastGoldDashSkillLogic` | **新增** | 商店阶段技能管理 |
| 24 | `ServerFastGoldDashShopLogic` | **新增** | 装备/技能购买 |
| 25 | `ServerFastGoldDashAirWallLogic` | **新增** | 回合间空气墙 |
| 26 | `ClientFastGoldDashPanelLogic` | **新增** | 回合 UI 面板 |

### Phase 4：Host 与 Config（6 文件）

| # | 文件 | 说明 |
|---|------|------|
| 27-30 | Host 4 个文件 | Class / RoleShopInfo / RoleSkillsInfo / ShopSuitInfo |
| 31-32 | Config 2 个文件 | GoldDashFastSportsSuitConfig / ContentConfig |

---

## 三、配置文件详解

### 3.1 SOFastGoldDashConfig

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `BornGroupDatas` | `List<FastGoldDashAreaData>` | — | 出生区域配置 |
| `bornConfigSign` | string | — | 出生配置标识 |
| `WinTimes` | int | 3 | Best-of-X 胜场数 |
| `MaxRoundTimes` | int | 7 | 最大回合数 |
| `RoundShopTime` | int | 25 | 商店时长(秒) |
| `RoundFightTime` | int | 90 | 战斗时长(秒) |
| `FreeTime` | int | 1 | 每回合免费刷新次数 |
| `ChestItemSign` | string | — | 逃脱必需道具 |
| `DefaultSuitId` | int | 52 | 默认装备 ID |
| `DefaultPoint` | int | 50 | 每回合基础分 |
| `KillPoint` | int | 10 | 击杀得分 |
| `AssistPoint` | int | 5 | 助攻得分 |
| `WinRoundPoint` | `List<int>` | — | 胜利回合额外分 |
| `LoseRoundPoint` | `List<int>` | — | 失败回合保底分 |
| `OpenLockChainBoxPoint` | int | 20 | 开箱者加分 |
| `OpenLockChainBoxTeammatePoint` | int | 15 | 开箱队友加分 |
| `FirstPickItemPoint` | int | 15 | 首次拾取加分 |
| `RoundEndShowResultTime` | int | 2 | 回合结果显示(秒) |
| `RoundEndShowScoreTime` | int | 5 | 回合积分显示(秒) |
| `RoundOverShowResultTime` | int | 2 | 系列赛结果显示(秒) |

### 3.2 GoldDashFastSportsSuitConfig

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | ushort | 套装 ID |
| `name` | string | 套装名称 |
| `score` | int | 关联分数（购买所需） |
| `is_lucky` | bool | 幸运标记（特殊套装） |
| `suit_type` | sbyte | 装备类型分类 |
| `weight` | int | 商店刷新权重 |
| `level` | int | 套装等级 |

### 3.3 GoldDash vs FastGoldDash 差异对比表

| 特性 | GoldDash | FastGoldDash |
|------|----------|--------------|
| **游戏结构** | 单局连续 | Best-of-X 回合赛 |
| **最大时长** | 1 长局 | 多回合，最多 7 回合 |
| **战斗时间** | 可变 | 固定 90 秒/回合 |
| **商店阶段** | 无 | 25 秒，1 次免费刷新 |
| **阶段流程** | Born → Running → Over | Born → [Shop → Round]×N → Over |
| **祭坛 (Altar)** | ✅ 有 | ❌ 移除 |
| **新手引导** | ✅ 有 | ❌ 移除 |
| **游戏内事件** | ✅ 复杂事件系统 | ❌ 移除 |
| **美人鱼任务** | ✅ 有 | ❌ 移除 |
| **黑市** | ✅ 有 | ❌ 移除 |
| **Boss Rush** | ✅ 有 | ❌ 移除 |
| **积分系统** | 复杂多因素 | 简化（击杀/助攻/回合胜负） |
| **宝箱逃脱** | 可选 | **必需**（ChestItemSign） |
| **空气墙** | Boss 区域 | 回合增强版（AirWallLogic） |

---

## 四、关键代码修改点

### 4.1 Mgr 继承结构

```csharp
// ★ 继承 ServerGoldDashMgr，不是 ServerModeManager
public class ServerFastGoldDashMgr : ServerGoldDashMgr {
    // 自动获得父类 32 个 Logic
    // Override: BornLogic, RoleLogic, AwardLogic, NsqDataLogic, StatisticsLogic, LookLogic
    // 新增: SkillLogic, ShopLogic, AirWallLogic
    // Stage: BornStage → ShopStage → RoundStartStage → RoundEndStage → OverStage
}

public class ClientFastGoldDashMgr : ClientGoldDashMgr {
    // 移除: AltarLogic, RookieGuideLogic, RunningStage 等 10+ 父类特性
    // 新增: ClientFastGoldDashPanelLogic（回合 UI）
}
```

### 4.2 回合循环核心（RoundEndStage 判定）

```csharp
// RoundEndStage 核心：判定回合胜负 + 循环/结束
// 伪代码示意（基于真实架构）

// 回合结束时：
// 1. 显示回合结果（RoundEndShowResultTime = 2s）
// 2. 显示积分面板（RoundEndShowScoreTime = 5s）
// 3. 判定：
//    if (某方 winCount >= WinTimes=3) → OverStage
//    else if (currentRound >= MaxRoundTimes=7) → OverStage（按总积分）
//    else → ShopStage（下一回合）
```

### 4.3 积分与商店系统

```csharp
// === 积分规则（SOFastGoldDashConfig）===
// 每回合基础分：DefaultPoint = 50
// 击杀：KillPoint = 10 | 助攻：AssistPoint = 5
// 开箱：OpenLockChainBoxPoint = 20（开箱者）/ 15（队友）
// 首次拾取：FirstPickItemPoint = 15
// 胜利/失败回合额外分：WinRoundPoint / LoseRoundPoint（List，按回合数递增）

// === 商店时序（ShopStage + ShopLogic）===
// 1. 进入 ShopStage，倒计时 RoundShopTime = 25s
// 2. ShopLogic 提供装备列表（GoldDashFastSportsSuitConfig，按 weight 加权随机）
// 3. 玩家可免费刷新 FreeTime=1 次，购买套装扣积分 score
// 4. SkillLogic 管理技能选择，默认装备 DefaultSuitId = 52
// 5. 倒计时结束 → RoundStartStage
```

---

## 五、常见问题与踩坑记录

### 5.1 回合状态重置

**现象**：新回合角色状态/道具/位置未清理
**根因**：父类 Logic 只设计单局运行，无回合重置
**方案**：FastBornLogic 每回合重置出生；FastRoleLogic 每回合角色添加/移除；注意 Shop→RoundStart 时序：先重置再激活

### 5.2 商店刷新时序

**现象**：ShopStage 倒计时结束时购买操作导致数据不一致
**根因**：ShopLogic 购买与 Stage 切换竞态
**方案**：切换前锁定购买；`RoundShopTime=25s` 结束后拒绝请求；`FreeTime=1` 每回合重置

### 5.3 空气墙碰撞

**现象**：AirWallLogic 激活/关闭时角色卡墙或穿透
**根因**：空气墙激活时机与回合切换不同步
**方案**：RoundStart 激活、RoundEnd 关闭；激活前推离角色；客户端同步渲染

### 5.4 GoldDash Logic 配置兼容

**现象**：复用的 32 个父类 Logic 读取 GoldDash 配置，部分参数不匹配
**根因**：父类 Logic 引用 ServerGoldDashMgr 的 Data/Config
**方案**：FastData 必须兼容父类接口；专有配置放 SOFastGoldDashConfig；被移除特性确保 Logic 不注册

### 5.5 Best-of-X 边界

**现象**：WinTimes=3 / MaxRoundTimes=7，统计分异常
**方案**：确保 `MaxRoundTimes >= WinTimes*2-1`；优先检查 WinTimes 达标；极端情况按总积分判胜

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error / GameMode 枚举无冲突
- [ ] Factory 双端已注册（ServerFastGoldDashMgr / ClientFastGoldDashMgr）
- [ ] 继承链：ServerFastGoldDashMgr → ServerGoldDashMgr → ServerModeManager

### 6.2 配置

- [ ] SOFastGoldDashConfig 全字段（WinTimes=3/MaxRoundTimes=7/积分参数）
- [ ] GoldDashFastSportsSuitConfig 含默认套装 id=52
- [ ] RoundShopTime=25s / RoundFightTime=90s 生效

### 6.3 运行时

- [ ] 5 阶段回合循环：Born → [Shop → RoundStart → RoundEnd]×N → Over
- [ ] Best-of-3 + 最多7回合判定正确
- [ ] 商店购买/免费刷新/默认装备正常
- [ ] 积分累计正确（击杀10/助攻5/开箱20·15/首拾取15/基础50）
- [ ] 空气墙与回合同步 / 宝箱逃脱正常

### 6.4 兼容性

- [ ] 不影响 GoldDash（父类 Logic 未修改）
- [ ] 复用 32 个 Logic 正常 / 移除的 14 特性无空引用
- [ ] Host 端数据序列化正确

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-golddash-fast]] · [[GoldDash制作]]
