# 1 代架构只管向上（OnlyUp）制作规范

> **适用范围**：OnlyUp 只管向上模式 — 新增关卡/扩展吸附检查点/调整攀爬规则/宝箱与陷阱系统
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-onlyup（237 文件，★★★★ 复杂，垂直攀爬 + 吸附系统 + 动态关卡加载 + 宝箱/陷阱/AFK/马里奥彩蛋）
> **公共框架依赖**：[[模式制作]]（AbsModeManager / AbsModeData / AbsModeStage / AbsModeLogic）
> **GameMode 枚举**：`OnlyUp=40`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientOnlyUpMgr (Client 端只管向上主管理器)
  │  继承: AbsModeManager
  │  职责: 攀爬表现、吸附同步、关卡动态加载、跳跃预测线、排名展示
  │
  ├── Client Logic 层（12 个）
  │     RoleLogic          — 角色管理（生成/销毁/模型显隐）
  │     BornLogic          — 出生/死亡/复活流程
  │     TimerLogic         — 关卡计时器（开始/暂停/结束）
  │     AdsorbLogic        — ★ 吸附系统（检查点触发/玩家携带）
  │     ArtSettingLogic    — 美术设置（SO 驱动的视觉参数）
  │     EffectLogic        — 特效管理（死亡/复活/过关特效）
  │     CheatLogic         — 反作弊（客户端校验）
  │     ChestLogic         — 宝箱交互（开启/奖励表现）
  │     TimeRecordLogic    — 时间记录（历史最佳管理）
  │     LevelConfigLogic   — 关卡配置加载
  │     LevelLayerLogic    — 关卡层管理（动态层级切换）
  │     LevelLoaderMgrLogic — ★ 关卡动态加载管理器
  │
  ├── LevelLoader 子系统（7 个加载器）
  │     AbsClientOnlyUpLevelLoader  — 抽象基类
  │     ├── LevelMapLoader          — 地图 Prefab 加载/卸载
  │     ├── LevelTimerLoader        — 计时触发区域
  │     ├── LevelDeadAreaLoader     — 死亡区域
  │     ├── LevelMustPassLoader     — 必经区域
  │     ├── LevelCantPassLoader     — 禁区
  │     └── LevelNameCardLoader     — 关卡名牌
  │
  ├── Level Object Pool
  │     ClientOnlyUpLevelObj         — 关卡对象封装
  │     ClientOnlyUpLevelObjPool     — 客户端对象池
  │     OnlyUpLevelObjPool           — 通用对象池
  │
  ├── Stage 层（3 阶段）
  │     ClientOnlyUpBornStage → ClientOnlyUpGameStage → ClientOnlyUpOverStage
  │
  ├── SO 数据
  │     SOOnlyUpArtSettings   — 美术参数
  │     SOOnlyUpEffectData    — 特效配置
  │
  ├── Network
  │     NetworkClient_OnlyUp_Base → NetworkClient_OnlyUp
  │
  └── ClientOnlyUpData

ServerOnlyUpMgr (Server 端只管向上主管理器)
  │  继承: AbsModeManager
  │  职责: 关卡进度权威判定、吸附验证、死亡/复活仲裁、排名计算
  │
  ├── Server Logic 层（16 个）
  │     RoleLogic          — 角色管理
  │     BornLogic          — ★ 出生/死亡/复活权威逻辑
  │     TimerLogic         — 计时权威（防篡改）
  │     AdsorbLogic        — ★ 吸附权威（检查点验证/携带判定）
  │     AwardLogic         — 奖励发放
  │     CheatLogic         — 反作弊服务端校验
  │     ChestLogic         — 宝箱验证/奖励发放
  │     LevelConfigLogic   — 关卡配置
  │     LevelRefreshLogic  — 关卡刷新
  │     TimeRecordLogic    — 时间记录权威
  │     AFKLogic           — ★ AFK 挂机检测
  │     MaorioLogic        — 马里奥彩蛋逻辑
  │     NsqDataLogic       — 数据上报
  │     SaveLevelLogic     — 关卡进度持久化
  │     StatisticsLogic    — 统计
  │     TrapLogic          — ★ 陷阱系统
  │
  ├── SO 数据
  │     SOOnlyUpModeData    — 模式主配置
  │     SOOnlyUpLevelData   — 关卡数据（SubLevelData）
  │     SOOnlyUpTrapData    — 陷阱配置
  │
  ├── Network
  │     NetworkServer_OnlyUp_Base → NetworkServer_OnlyUp
  │
  └── ServerOnlyUpData

Host 端（共享抽象层）
    AbsOnlyUpModeData             — 双端共享数据抽象
    AbsOnlyUpLevelConfigLogic     — 关卡配置共享逻辑
    AbsOnlyUpRoleTimeRecordLogic  — 时间记录共享逻辑
    BattleRoleOnlyUpComponent     — 角色组件（跳跃预测/着陆线渲染）
    OnlyUpRoleLevelTime           — 关卡时间数据
    OnlyUpSubLevelTime            — 子关卡时间数据

继承关系：
    AbsModeManager    → ClientOnlyUpMgr / ServerOnlyUpMgr
    AbsModeData       → AbsOnlyUpModeData → ClientOnlyUpData / ServerOnlyUpData
    AbsModeLogic      → 所有 Logic
    AbsModeStage      → 所有 Stage
    BattleRoleComponent → BattleRoleOnlyUpComponent
```

### 1.2 Stage 阶段流转

```
3 阶段制（OnlyUpModeStage 枚举）：

Born (0)
  │  玩家在起点生成
  │  初始化关卡配置 + 加载关卡层 Prefab
  │  设置出生点（BornPoint）
  │  初始化吸附系统（AdsorbLogic）
  ↓
Game (1) ← 核心
  │  垂直攀爬玩法：
  │    ├── 跳跃/攀爬向上，BattleRoleOnlyUpComponent 渲染着陆预测线
  │    ├── 进入 TriggerStartTimer 区域 → 开始关卡计时
  │    ├── 到达检查点 → AdsorbAction.TriggerSave 保存进度
  │    ├── 进入 DeadArea → RoleDead → 1秒后复活到上次检查点
  │    ├── 宝箱交互（ChestLogic）→ 奖励
  │    ├── 陷阱触发（TrapLogic）→ Buff/伤害
  │    ├── 玩家可吸附/携带其他玩家（Adsorb cooperative）
  │    ├── AFK 检测 → 超时处理
  │    └── 实时排名（ParentLevel → SubLevel → TimeAtLevel 排序）
  │  判定：到达最终关卡 / battleTime 到期 → Over
  ↓
Over (2)
    结算排名 + 奖励发放（AwardLogic）
    统计上报（StatisticsLogic / NsqDataLogic）
    关卡进度保存（SaveLevelLogic）
```

### 1.3 预制体与资源加载（★）

| 资源 | 类型 | 加载方式 | 时机 |
|------|------|---------|------|
| **SOOnlyUpModeData** | SO | AB 加载 | Init() |
| **SOOnlyUpLevelData** | SO（含 SubLevelData） | AB 加载 | Init() |
| **SOOnlyUpTrapData** | SO | AB 加载 | Init() |
| **SOOnlyUpArtSettings** | SO（美术参数） | AB 加载 | Init() |
| **SOOnlyUpEffectData** | SO（特效配置） | AB 加载 | Init() |
| **LayerPrefabName** | 关卡层 Prefab | 动态加载/对象池 | Game 阶段按距离 |
| **DeadArea / MustPass / CantPass** | 关卡区域 | LevelLoader 动态生成 | Game 阶段按距离 |

### 1.4 网络协议（Proto_OnlyUp, API_ID=51）

| 消息 | ID | 方向 | 内容 |
|------|-----|------|------|
| CmdGetProps | 51001 | C→S | boxId, boxType, pos, sign（宝箱交互） |
| RpcRoleDead | 51002 | S→C | roleId（广播死亡） |
| RpcRoleRevive | 51003 | S→C | roleId, pos, rot, parentLevel, subLevel（广播复活） |
| CmdTriggerDead | 51004 | C→S | 客户端触发死亡区域 |
| RpcRoleLevelData | 51005 | S→C | OnlyUpRoleLevelData 结构（进度同步） |
| CmdStartTimer | 51006 | C→S | 开始关卡计时 + cheatData |
| RpcAdsorberAction | — | S→C | 吸附动作同步（AdsorbAction 枚举） |
| RpcRoleTransToTargetLevel | — | S→C(Target) | 确认关卡转移 |
| TargetRpcSyncAllRoleLevelData | — | S→C(Target) | 同步所有玩家进度 |
| TargetRpcSyncRoleLevelTimeData | — | S→C(Target) | 同步计时记录 |

### 1.5 UI 层（18 个面板/组件）

| 分组 | 类名 | 职责 |
|------|------|------|
| **游戏中** | OnlyUpGamingWin | 主游戏 HUD |
| | OnlyUpGamingAdsorbWidget | 吸附/携带状态提示 |
| | OnlyUpTailWidget | 尾部信息组件 |
| | OnlyUpWatchWidget | 观战组件 |
| | OnlyUpTreasure | 宝箱主面板 |
| | OnlyUpTreasureInfosWidget | 宝箱详情 |
| | OnlyUpCarryTips | 携带提示 |
| | OnlyUpParentLevelFinishWidget | 大关完成弹窗 |
| **记录** | OnlyUpRecordWin | 记录主面板 |
| | OnlyUpLevelRecord | 关卡记录 |
| | OnlyUpRecordItem | 记录条目 |
| | OnlyUpRecordTotalTimeItem | 总时间条目 |
| **排名** | OnlyUpPlayersInfoWin | 排名主面板 |
| | OnlyUpPlayersWidget | 玩家列表 |
| | OnlyUpPlayerCardWidget | 玩家卡片 |
| | OnlyUpPlayerInfoReportWidget | 举报面板 |
| | OnlyUpPlayerInfoItem | 玩家信息条目 |
| | OnlyUpTailPlayerInfoItem | 尾部玩家信息 |

Controller 层：OnlyUpGamingController / OnlyUpPlayersInfoController / OnlyUpRecordController

---

## 二、新建/扩展 Checklist

### Phase 1：新增关卡

| # | 文件/系统 | 操作 | 说明 |
|---|----------|------|------|
| 1 | SOOnlyUpLevelData | 修改 | 新增 SubLevelData 条目（配置 DeadArea/BornPoint/Timer 区域等） |
| 2 | OnlyUpLevelConfig 表 | 修改 | 新增关卡行（level/root_level/levelName/levelNum） |
| 3 | 关卡 Prefab（LayerPrefabName） | 新建 | 制作关卡层预制体 |
| 4 | SOOnlyUpModeData | 修改 | 更新 maxParentLevelCount / openParentLevelCount |

### Phase 2：扩展吸附/检查点

| # | 文件/系统 | 操作 | 说明 |
|---|----------|------|------|
| 5 | AbsOnlyUpLevelConfigLogic | 修改 | 调整检查点判定逻辑 |
| 6 | Server/ClientAdsorbLogic | 修改 | 新增 AdsorbAction 类型或携带规则 |
| 7 | SubLevelData.BornPoint | 修改 | 调整检查点位置 |

### Phase 3：宝箱/陷阱/特殊系统

| # | 文件/系统 | 操作 | 说明 |
|---|----------|------|------|
| 8 | OnlyUpCrateConfig 表 | 修改 | 新增宝箱奖励配置 |
| 9 | SOOnlyUpTrapData | 修改 | 新增陷阱类型/Buff |
| 10 | ServerOnlyUpTrapLogic | 修改 | 陷阱触发逻辑 |
| 11 | ServerOnlyUpChestLogic | 修改 | 宝箱验证/发放 |

### Phase 4：关卡加载器扩展

| # | 文件/系统 | 操作 | 说明 |
|---|----------|------|------|
| 12 | AbsClientOnlyUpLevelLoader | 继承 | 新建加载器子类 |
| 13 | LevelLoaderMgrLogic | 修改 | 注册新加载器 |
| 14 | ClientOnlyUpLevelObjPool | 修改 | 对象池适配新类型 |

---

## 三、配置文件详解

### 3.1 SOOnlyUpModeData（模式主配置）

| 字段 | 类型 | 说明 |
|------|------|------|
| `maxParentLevelCount` | int | 总大关数 |
| `openParentLevelCount` | int | 当前已开放大关数 |
| `rangeLoadCount` | int | 预加载范围（±N 个关卡） |
| `bornConfigSign` | string | 出生配置 Sign |
| `closeWarStartTime` | float | 自动关闭战斗的延迟时间（秒） |
| `battleTime` | float | 总战斗时长（秒） |
| `LayerPrefabName` | string | 关卡层 Prefab 名称 |
| `SpeedUpAreaBuff` | int | 加速区域 Buff ID |
| `LowGravityAreaBuff` | int | 低重力区域 Buff ID |
| `ChestBuffSign` | string | 宝箱 Buff Sign |
| `trapConfigSign` | string | 陷阱配置 Sign |
| `trapBuffSign` | string | 陷阱伤害 Buff Sign |
| `CloseTeamMatchRemindTime` | float | 自动匹配截止提醒时间 |
| `CloseTeamMatchPlayerNum` | int | 最少玩家数（低于则关闭匹配） |
| `CloseTipCountDown` | float | 关闭倒计时提示（秒） |
| `ServerStopTime` | float | 强制关闭延迟（秒） |

### 3.2 SOOnlyUpLevelData — SubLevelData（关卡子数据）

| 字段 | 类型 | 说明 |
|------|------|------|
| `SubLevelIndex` | int | 子关卡索引 |
| `PassLevelMinTime` | float | 通关最短合法时间（反作弊用） |
| `DeadAreas` | List\<AreaData\> | 死亡区域列表 |
| `BornPoint` | List\<PointData\> | 检查点/复活位置列表 |
| `TriggerStartTimer` | AreaData | 计时开始触发区 |
| `TriggerEndTimer` | AreaData | 计时结束触发区 |
| `MustPassAreas` | List\<AreaData\> | 必经路径区域 |
| `CantPassAreas` | List\<AreaData\> | 禁区列表 |
| `ChestPoints` | List\<ChestData\> | 宝箱位置及配置 |
| `Equips` | List\<EquipData\> | 关卡装备/武器配置 |
| `CanHoldAttack` | bool | 是否允许蓄力攻击 |
| `LevelNameCard` | AreaData | 关卡名牌区域 |

### 3.3 SOOnlyUpTrapData（陷阱配置）

由 `trapConfigSign` 索引，定义陷阱类型、触发条件、对应 Buff（`trapBuffSign`）。与 ServerOnlyUpTrapLogic 配合使用。

### 3.4 Excel 配置表

#### OnlyUpConfig（模式主表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 主键 |
| `game_selection_id` | int | 游戏选择 ID |
| `rankings_id` | int | 排行榜 ID |
| `is_difficult` | bool | 是否困难模式 |
| `sign` | string | 配置 Sign |

#### OnlyUpLevelConfig（关卡表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 主键 |
| `only_up_id` | int | 关联 OnlyUpConfig.id |
| `level` | int | 关卡编号 |
| `root_level` | int | 所属大关编号 |
| `item_id` | int | 奖励物品 ID |
| `item_num` | int | 奖励数量 |
| `server_type` | int | 服务端类型 |
| `levelName` | string | 关卡显示名 |
| `levelNum` | int | 关卡内编号 |

#### OnlyUpCrateConfig（宝箱表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 主键 |
| `war_chest_award_id` | int | 战斗宝箱奖励 ID |
| `chest_award` | string | 宝箱奖励配置 |
| `server_type` | int | 服务端类型 |
| `match_mode` | int | 匹配模式 |

### 3.5 玩家数据（PlayerOnlyUpModeInfo）

| 字段 | 类型 | 说明 |
|------|------|------|
| `OnlyUpId` | int | 当前 OnlyUp 配置 ID |
| `RootLevelTimeRecords` | List | 大关时间记录 |
| `RootLevel` | int | 当前大关 |
| `OpenCrateIdList` | List | 已开启宝箱 ID 列表 |
| `LevelTimeRecords` | List | 关卡时间记录 |

---

## 四、关键代码解析

### 4.1 吸附/检查点系统（Adsorb System）★核心

吸附系统是 OnlyUp 的核心，负责检查点记录、关卡进度管理和玩家携带。

**数据结构 — OnlyUpRoleLevelData（ProtoStruct）：**

```csharp
// 每个玩家的关卡进度（服务端权威，通过 RpcRoleLevelData 同步）
struct OnlyUpRoleLevelData {
    int AutoRoleId;          // 角色 ID
    byte CurrentParentLevel; // 当前大关
    byte CurrentSubLevel;    // 当前小关
    byte LastParentLevel;    // 上一个检查点大关
    byte LastSubLevel;       // 上一个检查点小关
    byte MaxParentLevel;     // 历史最高大关
    byte MaxSubLevel;        // 历史最高小关
}
```

**AdsorbAction 枚举（驱动状态机）：**

```csharp
enum AdsorbAction {
    StartTimer,    // 进入 TriggerStartTimer 区域 → 开始该关卡计时
    EndTimer,      // 进入 TriggerEndTimer 区域 → 结束该关卡计时
    TriggerSave,   // 到达检查点 → 保存 Last/Max 进度（服务端持久化）
    RoleDead,      // 进入 DeadArea → 触发死亡流程
    RoleRevive,    // 复活完成 → 恢复到上次检查点
}
```

**携带机制**：玩家可吸附/携带其他玩家（cooperative），被携带者跟随携带者移动。死亡时需处理携带链——携带者死亡则被携带者也死亡（见 §5.1）。

### 4.2 坠落/重生逻辑（服务端权威）

```
完整流程（ServerOnlyUpBornLogic.RoleDead）：

1. 角色进入 DeadArea → CmdTriggerDead(51004) 上报
2. 服务端校验 CheckCanTrans（反作弊，验证关卡转移合法性）
3. 执行死亡：
   ├── 清理关卡装备
   ├── 设置 IsDead = true
   ├── 清除移动 Buff
   ├── 如果该角色正在被携带 → 携带者也执行死亡
   └── 如果该角色正在携带别人 → 检查是否同关卡，决定是否连锁死亡
4. RpcRoleDead(51002) 广播死亡
5. 等待 1 秒
6. 复活：
   ├── 读取 LastParentLevel / LastSubLevel → 获取 BornPoint 位置
   ├── 传送角色到检查点
   └── CommonResurrection 通用复活流程
7. RpcRoleRevive(51003) 广播复活（含 pos/rot/parentLevel/subLevel）

客户端表现（ClientOnlyUpBornLogic）：
  - 收到 RpcRoleDead → 隐藏角色模型 + 暂停计时器 + 播放死亡特效
  - 收到 RpcRoleRevive → 显示角色模型 + 传送 + 恢复计时器
```

### 4.3 关卡动态加载（Level Loader System）

LevelLoaderMgrLogic 管理 7 种加载器，基于玩家当前关卡位置按距离动态加载/卸载：

| 加载器 | 职责 | 距离控制 |
|--------|------|---------|
| **LevelMapLoader** | 地图 Prefab 加载/卸载 | UnloadLastMapLevel=2, PreLoadLastMapLevel=7 |
| **LevelTimerLoader** | 计时触发区域生成 | 跟随 Map 加载 |
| **LevelDeadAreaLoader** | 死亡区域生成 | 跟随 Map 加载 |
| **LevelMustPassLoader** | 必经路径区域 | 跟随 Map 加载 |
| **LevelCantPassLoader** | 禁区生成 | 跟随 Map 加载 |
| **LevelNameCardLoader** | 关卡名牌 | 跟随 Map 加载 |
| **LevelObjPool** | 对象池回收/复用 | 全局管理 |

**加载策略**：以当前关卡为中心，前后 `rangeLoadCount` 个关卡保持加载。超出 `UnloadLastMapLevel` 距离的关卡自动卸载并回池，`PreLoadLastMapLevel` 范围内的关卡预加载。

### 4.4 排名系统

```
排名排序规则（多级排序）：
  1. CurrentParentLevel — 大关越高越靠前
  2. CurrentSubLevel   — 同大关下小关越高越靠前
  3. TimeAtLevel       — 同关卡下用时越短越靠前

服务端：TimeRecordLogic 维护每个角色的关卡时间记录（OnlyUpRoleLevelTime / OnlyUpSubLevelTime）
客户端：OnlyUpPlayersInfoWin + OnlyUpPlayersWidget 实时渲染排名列表
同步：TargetRpcSyncAllRoleLevelData 全量同步 / RpcRoleLevelData 增量同步
```

### 4.5 跳跃预测（BattleRoleOnlyUpComponent）

```
BattleRoleOnlyUpComponent（继承 BattleRoleComponent）：
  - RaySphereCast 向下 25f 距离检测着陆点
  - 渲染着陆预测线 + 粒子特效
  - 仅在 IsJump == true && IsSneakSand == false 时激活
  - 帮助玩家判断跳跃落点，降低操作难度
```

### 4.6 反作弊（双端校验）

```
ServerOnlyUpCheatLogic / ClientOnlyUpCheatLogic 协同：
  - CheckCanTrans: 校验关卡转移合法性（防止跳关）
  - PassLevelMinTime: 每个子关卡有最短通关时间（SOOnlyUpLevelData）
  - CmdStartTimer(51006) 携带 ProtoStruct_OnlyUpCheatData 供服务端验证
```

---

## 五、常见问题与踩坑记录

### 5.1 携带者连锁死亡

**现象**：被携带的玩家进入 DeadArea，携带者不应该死但也被杀了

**根因**：ServerOnlyUpBornLogic.RoleDead 中的携带链处理——被携带者死亡会反向触发携带者死亡，且未检查携带者是否在安全区域

**解决方案**：死亡前先断开携带关系（AdsorbLogic 解除吸附），再对各角色独立判定是否在 DeadArea。修改携带链处理需同时更新双端 AdsorbLogic

### 5.2 关卡预加载距离不当导致卡顿

**现象**：玩家快速上升时出现短暂卡顿/白屏

**根因**：`rangeLoadCount` 设置过小，或 `PreLoadLastMapLevel`（默认 7）不够。快速移动时新关卡加载不及时

**解决方案**：根据关卡 Prefab 大小调整 `rangeLoadCount` 和 `PreLoadLastMapLevel`。大型关卡层需增加预加载距离。使用 LevelObjPool 对象池减少 Instantiate 开销

### 5.3 AFK 挂机检测误判

**现象**：玩家在困难区域反复尝试跳跃，被 AFK 系统误踢

**根因**：ServerOnlyUpAFKLogic 仅检测关卡进度变化，未考虑玩家有在活跃移动但未推进关卡的情况

**解决方案**：AFK 检测应结合位置变化 + 关卡进度双维度判断，纯位移但无进度推进不应立即判定为 AFK

### 5.4 陷阱 Buff 与关卡装备交互异常

**现象**：触发陷阱后玩家装备消失或 Buff 叠加错误

**根因**：ServerOnlyUpTrapLogic 施加的 `trapBuffSign` 与关卡装备的 Buff 存在冲突，死亡时清理装备逻辑未正确处理陷阱 Buff 残留

**解决方案**：陷阱 Buff 使用独立通道，死亡清理时区分关卡装备 Buff 和陷阱 Buff。修改 BornLogic.RoleDead 的清理顺序

### 5.5 检查点跳过导致坠落到底部

**现象**：玩家爬到很高但坠落后回到起点而非最近检查点

**根因**：TriggerSave 区域（SubLevelData.BornPoint）碰撞器太小，玩家跳跃轨迹跳过了触发区

**解决方案**：加大 BornPoint 触发区域覆盖范围；或在 MustPassAreas 配合强制触发检查点保存

### 5.6 移动平台同步不一致

**现象**：客户端看到平台在 A 位置，服务端判定在 B 位置

**根因**：平台动画/Tween 未在服务端同步

**解决方案**：平台位置由服务端驱动，客户端插值跟随

---

## 六、验收标准

- [ ] 3 阶段（Born → Game → Over）正常流转
- [ ] 吸附系统正确记录检查点（AdsorbAction 全枚举覆盖）
- [ ] 坠落后正确复活到最近检查点（LastParentLevel/LastSubLevel）
- [ ] 携带者连锁死亡逻辑正确（断开 → 独立判定）
- [ ] 实时排名按 ParentLevel → SubLevel → Time 正确排序
- [ ] 关卡动态加载/卸载无卡顿（LevelLoader 7 种加载器正常工作）
- [ ] 对象池正确回收/复用（ClientOnlyUpLevelObjPool）
- [ ] 宝箱交互正确（CmdGetProps → 服务端验证 → 奖励发放）
- [ ] 陷阱触发正确（TrapLogic + trapBuffSign）
- [ ] AFK 检测不误判活跃玩家
- [ ] 反作弊双端校验通过（CheckCanTrans + PassLevelMinTime）
- [ ] 网络协议完整（API_ID=51，10 条消息全覆盖）
- [ ] 跳跃预测线正确渲染（BattleRoleOnlyUpComponent）
- [ ] 马里奥彩蛋正常触发（MaorioLogic）
- [ ] 关卡进度持久化正确（SaveLevelLogic）

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-onlyup]]
