# 1 代架构足球派对（FootballParty）制作规范

> **适用范围**：FootballParty 足球派对 — 扩展赛制规则 / 球物理调优 / 射门传球铲球系统 / 随机事件与 Buff
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-footballparty（59 文件，★★ 中等，7 Stage + 球物理状态机 + 贝塞尔传球 + 纯 PvP）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **GameMode 枚举**：`LimitedtimeFifamode=19`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientFootballMgr (Client 端主管理器)
  │  继承: ClientModeManager
  │  职责: 足球表现、射门蓄力 UI、计分板、特效管理
  │
  ├── Client Logic 层
  │     ClientFootballBallLogic      — 球表现 + 贝塞尔路径回放
  │     ClientFootballBallLogic_Other— 球辅助逻辑（旋转/弹跳表现）
  │     ClientFootballRoleLogic      — 角色动画/控球表现
  │     ClientFootballDataLogic      — 数据驱动 UI 刷新
  │     ClientFootballReportLogic    — 战报事件处理
  │     ClientFootballTerrainLogic   — 地形适配
  │     ClientFootballCheatCheck     — 客户端反作弊校验
  │
  ├── Mono 层
  │     ClientFootballController     — 球体 Mono 控制器
  │     ClientFootballDataDisplay    — 数据展示组件
  │
  ├── 特效管理
  │     ClientFootballGameEffectMgr  — 游戏特效（进球/铲球）
  │     ClientFootballBallEffectMgr  — 球体特效（拖尾/火焰）
  │
  ├── Stage 层（7 阶段，FootballStage 枚举）
  │     Born → Show → Camera → Ready → Battle → Closeup → Over
  │
  └── ClientFootballData

ServerFootballMgr (Server 端主管理器)
  │  继承: ServerModeManager
  │  职责: 权威判定、球物理状态机、进球/计分、回合管理
  │
  ├── Server Logic 层
  │     ServerFootballBallLogic      — 球物理状态机（核心）
  │     ServerFootballRoleLogic      — 角色持球/抢断判定
  │     ServerFootballEventLogic     — 随机事件系统（双倍得分等）
  │     ServerFootballBuffAreaLogic  — 场地 Buff 区域管理
  │     ServerFootballAwardLogic     — 奖励结算
  │     ServerFootballReportLogic    — 战报上报
  │     ServerFootballTerrainLogic   — 地形碰撞
  │     ServerFootballCheatCheck     — 服务端反作弊
  │     ServerFootballNsqDataLogic   — 数据上报
  │     ServerFootballStatisticsLogic— 统计系统
  │
  ├── Mono 层（碰撞检测）
  │     ServerFootballController     — 球体服务端控制器
  │     ServerFootballGoal           — 球门触发器（OnTriggerEnter 进球判定）
  │     ServerFootballOutside        — 出界处理
  │     ServerFootballWoodwork       — 门框碰撞
  │
  ├── Stage 层（与 Client 对称）
  │     Born → Show → Camera → Ready → Battle → Closeup → Over
  │
  └── ServerFootballData

Host 层（共享）
    AbsFootballController    — 球控制器基类
    FootBallNetwork          — 网络同步基础
    FootBallNetworkMirror    — Mirror 网络适配
    BeizerPathManager        — 贝塞尔曲线传球路径计算 ★
    FootballMonoManager      — Mono 生命周期管理
    FootballWall             — 墙壁碰撞处理
    FootballDefine           — 枚举/常量定义（FootballStage, FootBallState 等）
    FootballReportEventId    — 战报事件 ID 定义

配置
    SOFootballPartyConfig    — ScriptableObject 全局配置（射门/传球/球物理/球门等）

网络
    Proto_FootballParty           — 协议定义
    ProtoStruct_FootballRoleData  — 角色数据结构
    NetworkServer/Client_FootballParty      — 收发逻辑
    NetworkServer/Client_FootballParty_Base — 基类

UI
    FootBallPanelWin        — 胜利面板
    EventCell               — 随机事件单元格
    AssistInfo               — 助攻信息展示
    UIFootballController     — UI 控制器
    UIFootballStorage        — UI 数据缓存
    FootballHit              — 命中反馈
    TipsFootballMode         — 模式提示
```

### 1.2 Stage 阶段流转

```
7 阶段制（FootballStage 枚举）：

Born (球员生成)
  │  按队伍分配出生点: Red=位置4-7, Blue=位置0-3
  │  bornGroupId = Random.Range(0, dividingLines.Length)
  ↓
Show (开场动画)
  │  展示双方阵容
  ↓
Camera (相机设置)
  │  切换足球模式专用相机
  ↓
Ready (倒计时准备)
  │  锁定玩家输入（禁止操作）
  │  重置球位 ResetBallPoint
  │  清除 Buff: BuffClear
  │  重置出生点: ResetBornPoint
  │  倒计时结束 → 解锁输入
  ↓
Battle (核心战斗) ← ★ 主玩法阶段
  │  球物理状态机驱动
  │  射门蓄力 / 传球贝塞尔 / 铲球抢断
  │  进球判定 → 触发 Closeup
  │  随机事件（ServerFootballEventLogic）
  │  Buff 区域（ServerFootballBuffAreaLogic）
  │  回合结束 → 换边 → 回到 Ready
  ↓
Closeup (进球特写)
  │  镜头跟踪进球瞬间
  │  播放进球特效
  │  → 回到 Ready（下一回合）
  ↓
Over (游戏结束)
    MVP / 最佳射手展示
    FootballRoleData 排名（score 降序）
```

### 1.3 球物理状态机

```
FootBallState 枚举：

None(0)
  │  初始状态
  ↓
Idle(1) ← 球静止/被持有
  ├──→ PathMove(2)         传球：贝塞尔曲线路径移动
  ├──→ Free(4)             射门后自由飞行
  └──→ CantController(3)   无敌期（射门/传球/铲球后不可抢）

CantController(3)
  │  持续约 2 秒
  │  期间任何角色无法拾取/抢断
  ↓
Idle(1)  回到可控状态
```

### 1.4 预制体与资源加载

| 资源 | 加载方式 | 时机 |
|------|---------|------|
| **SOFootballPartyConfig** | SO 配置 | Init() |
| **足球 Prefab** | Addressable | Born |
| **球门（含梯形碰撞体）** | GoalData.AssetsName | Born |
| **球场** | Scene | Born |
| **计分板 / 事件 UI** | UIManager | Battle |

---

## 二、新建/扩展 Checklist

### Phase 1：调整赛制规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | SOFootballPartyConfig | 修改 | 回合时长 / 队伍配置 / 得分倍率 |
| 2 | ServerFootballData | 修改 | Round 计数 / 换边逻辑 |

### Phase 2：扩展球物理

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 3 | ServerFootballBallLogic | 修改 | FootBallState 状态转换 / 速度衰减 |
| 4 | AbsFootballController | 修改 | 控球跟随插值 / 旋转扭矩 |
| 5 | SOFootballPartyConfig | 修改 | ballControllerMoveLerp / ballRigidMoveLerp 等 |

### Phase 3：射门/传球/铲球

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | ServerFootballBallLogic | 修改 | CmdShoot 力度计算 / 仰角限制 |
| 7 | BeizerPathManager | 修改 | 传球曲线控制点 / 高度比例 |
| 8 | ServerFootballRoleLogic | 修改 | CmdSlideTackleBall 铲球判定 |

### Phase 4：新增随机事件/Buff

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | ServerFootballEventLogic | 修改 | 新增事件类型 / 触发条件 / 持续时间 |
| 10 | ServerFootballBuffAreaLogic | 修改 | Buff 区域位置 / 效果 |

### Phase 5：新增 Logic

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | 新 Client/Server Logic | 新建 | 双端对称，分别注册到 Mgr.Init() |
| 12 | ClientFootballMgr / ServerFootballMgr | 修改 | Init() 中注册新 Logic |

---

## 三、配置文件详解

### 3.1 SOFootballPartyConfig 核心字段

#### 射门系统

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `shootDefaultSpeed` | float | 10 | 射门默认初速度 |
| `shootStoreAddSpeed` | float | 5 | 蓄力每秒增加速度 |
| `shootMaxStorageTime` | float | 5 | 最大蓄力时间（秒） |
| `shootOffsetAngle` | float | 0 | 射门角度偏移 |
| `shootMaxAngle` | float | 75 | 最大射门仰角 |
| `shootMinAngle` | float | 20 | 最小射门仰角 |
| `shootFallDownSpeed` | float | 6 | 空中球下坠速度 |
| `shootBicycleKickHeight` | float | 4 | 倒挂金钩触发高度阈值 |
| `shootBicycleKickAddSpeed` | float | 5 | 倒挂金钩额外加速 |
| `shootBicycleKickMaxSpeed` | float | 50 | 倒挂金钩最大速度上限 |
| `assistDuration` | float | 2f | 助攻判定时间窗口（秒） |

#### 传球系统（贝塞尔曲线）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `passBallAngleLimit` | float | 30 | 传球锥角（度） |
| `passBallDistanceLimit` | float | 50 | 最大传球距离 |
| `passBallDefaultPointHeight` | float | 5f | 短传曲线控制点高度 |
| `passBallMaxPointHeight` | float | 15f | 长传曲线控制点高度 |
| `passBallBeizerSpeed` | float | 0.2f | 贝塞尔路径移动速度 |
| `passBallBeizerCount` | float | 0.5f | 路径采样密度 |
| `passBallTargetDistance` | Vector2 | — | 传球距离范围 (min, max) |
| `passBallNoTargetMetaCheckDistance` | float | — | 无队友目标时检测敌人距离 |

#### 球物理

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `checkControllerBallHeight` | float | 0 | 吸球高度判定 |
| `checkControllerBallDistance` | float | 2 | 持球吸附判定距离 |
| `ballPositionScale` | float | 2 | 控球时位置系数 |
| `ballPositionOffset` | Vector3 | (0,1,0) | 控球位置偏移 |
| `ballControllerMoveLerp` | float | 0.2f | 控球跟随插值速度 |
| `ballRigidMoveLerp` | float | 0.2f | 自由球物理插值速度 |
| `ballControllerRotateTorque` | float | 5 | 控球旋转扭矩 |
| `ballRotateMaxMoveSpeed` | float | 50 | 旋转最大速度阈值 |
| `ballMaxBoundsArrays` | Vector3[] | — | 球活动区域上界 |
| `ballMinBoundsArrays` | Vector3[] | — | 球活动区域下界 |

#### 球门配置（GoalData 结构体）

| 字段 | 类型 | 说明 |
|------|------|------|
| `AssetsName` | string | 球门预制体名 |
| `GoalPos` | Vector3 | 球门位置（Left: 35.4,14.7,-102 / Right: 35.4,14.7,-243） |
| `GoalScale` | Vector3 | 球门缩放 |
| `ColliderPos` | Vector3 | 碰撞体中心位置 |
| `ColliderTopWidth` | float | 梯形碰撞体上宽 |
| `ColliderBottomWidth` | float | 梯形碰撞体下宽 |
| `ColliderHeight` | float | 梯形碰撞体高度 |
| `JumpLevel` | float | 球门跳跃层级 |
| `IntoGoalEffect` | string | 进球特效名 |

#### 碰撞与控制

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `touchWallControllerTime` | float | 0.2f | 碰墙后不可控时间（秒） |

### 3.2 计分规则

| 行为 | 分值 | 说明 |
|------|------|------|
| 进球 (goal) | +10 | 射门进球得分 |
| 助攻 (assist) | +5 | assistDuration 时间窗口内的传球者 |
| 抢断 (snatch/schange) | +1 | 成功铲球夺球 |
| 乌龙球 | -10 | 射手队伍 == 球门队伍时判定 |
| 双倍得分事件 | ×2 | scoreScale=2，由随机事件触发 |

### 3.3 角色数据结构

```csharp
// ProtoStruct_FootballRoleData
struct FootballRoleData {
    int roleId;       // 角色 ID
    int goal;         // 进球数
    int score;        // 总分
    int assist;       // 助攻数
    int schange;      // 抢断数
    bool isRedTeam;   // 队伍标识
}
```

---

## 四、关键代码修改点

### 4.1 进球判定（ServerFootballGoal）

```csharp
// ServerFootballGoal.cs — OnTriggerEnter 检测球进入球门区域
// GoalType 枚举: Red / Blue

void OnTriggerEnter(Collider other) {
    // 1. 确认碰撞物是足球
    // 2. 判定乌龙球：射手队伍 == 球门所属队伍 → isOwnGoal = true, score = -1
    // 3. 正常进球：对方球门 → scoreScale（双倍事件期间 = 2）
    // 4. 助攻链：从 Stack<AssistData> 取 assistDuration 内的传球者
    // 5. 发送 RpcBallIntoGoal（含 assists 数组 + isOwnGoal 标志）
    // 6. 发送 RpcScore（红蓝队分数 + 全角色 FootballRoleData）
    // 7. 切换到 Closeup 阶段
}
```

### 4.2 射门蓄力

```csharp
// 客户端通过 CmdShoot 发送射门请求
// 参数: 力度(force), 方向(direction), 蓄力时间(chargeTime)

// 服务端计算:
// finalSpeed = shootDefaultSpeed + shootStoreAddSpeed * chargeTime
// chargeTime 上限 = shootMaxStorageTime
// 仰角限制: clamp(angle, shootMinAngle, shootMaxAngle)
// 倒挂金钩: 若球高度 > shootBicycleKickHeight
//   → speed += shootBicycleKickAddSpeed
//   → clamp(speed, 0, shootBicycleKickMaxSpeed)

// 射门后球状态: FootBallState.Free → CantController（不可抢期）
```

### 4.3 贝塞尔曲线传球（BeizerPathManager）

```csharp
// BeizerPathManager.GetPath(start, end) 生成二次贝塞尔路径
// P(t) = (1-t)² · P0 + 2(1-t)t · P1 + t² · P2
//
// 控制点 P1 计算:
//   x, z = 起终点中点
//   y = 根据距离比例在 passBallDefaultPointHeight(5f) ~ passBallMaxPointHeight(15f) 间插值

// CmdPassBall 参数: 传球者ID, 目标ID, 终点坐标, 移动方向
// 传球条件: 锥角 < passBallAngleLimit(30°), 距离 < passBallDistanceLimit(50)
// 传球后球状态: FootBallState.PathMove → CantController
```

### 4.4 铲球抢断

```csharp
// CmdSlideTackleBall — 铲球请求
// CmdBeSlideTackleRole — 被铲球通知

// 成功铲球: 球从被铲者转移到铲球者
//   → schange(抢断) 计数 +1
//   → 球进入 CantController 状态（2 秒不可再抢）
```

### 4.5 回合换边

```csharp
// ServerFootballData.Round 记录当前回合数
// 每回合结束 → Closeup → Ready（重新开始）
//
// Ready 阶段重置流程:
// 1. BuffClear()           — 清除所有 Buff
// 2. ResetBornPoint()      — 重新分配出生点
// 3. ResetBallPoint()      — 球回中场
// 4. 锁定玩家输入          — 倒计时期间禁止操作
// 5. 倒计时结束 → 解锁输入 → 进入 Battle
//
// 出生点分配:
//   bornGroupId = Random.Range(0, dividingLines.Length)
//   Red 队: 位置 4-7
//   Blue 队: 位置 0-3
```

### 4.6 网络同步（Mirror）

```csharp
// ─── Cmd（客户端 → 服务端）───
// CmdShoot(force, direction, chargeTime)   — 射门
// CmdPassBall(passerId, targetId, endPos, moveDir)  — 传球
// CmdSlideTackleBall(...)                  — 铲球
// CmdBeSlideTackleRole(...)                — 被铲球
// CmdFootBallRoleState(...)                — 角色状态

// ─── Rpc（服务端 → 客户端）───
// RpcFootballSetState(...)         — 球状态同步
// RpcShoot(...)                    — 射门表现
// RpcPassBall(...)                 — 传球表现
// RpcBallIntoGoal(assists[], isOwnGoal)  — 进球通知
// RpcScore(redScore, blueScore, allRoleData[])  — 计分同步

// ─── SyncVar（Mirror 持续同步）───
// ballState     — 当前 FootBallState
// speed         — 球速度
// controllerId  — 当前持球者 ID
```

---

## 五、常见问题与踩坑记录

### 5.1 球体穿墙/穿门

**现象**：大力射门时球穿过球门网或 FootballWall

**根因**：高速运动物体的连续碰撞检测（CCD）未启用

**解决方案**：Rigidbody.CollisionDetectionMode = ContinuousDynamic；同时检查 ServerFootballWoodwork/FootballWall 的碰撞层级设置

### 5.2 碰墙后无敌期丢控

**现象**：球碰墙后短暂不可控，玩家以为 Bug

**根因**：`touchWallControllerTime = 0.2f` 设计如此，碰墙后进入 CantController 状态

**解决方案**：这是预期行为。若需调整，修改 SOFootballPartyConfig.touchWallControllerTime

### 5.3 传球贝塞尔曲线精度

**现象**：长传球弧线过高或过低，传球不自然

**根因**：控制点高度由 `passBallDefaultPointHeight` 和 `passBallMaxPointHeight` 线性插值，距离极端时效果差

**解决方案**：调整 SOFootballPartyConfig 中 passBallDefaultPointHeight(5f) / passBallMaxPointHeight(15f) 的比例；检查 `passBallBeizerSpeed` 采样密度

### 5.4 助攻链追踪遗漏

**现象**：明显的助攻传球未被记录

**根因**：`assistDuration = 2f`，超过 2 秒的传球-射门链不计助攻；Stack\<AssistData\> 在球状态切换时可能被清空

**解决方案**：适当增大 assistDuration；确保 CantController → Idle 转换时不清空助攻栈

### 5.5 乌龙球判定争议

**现象**：球被铲后方向改变进入己方球门，判定铲球者乌龙

**根因**：进球判定只看 lastShooter/lastController 的队伍与球门队伍是否相同

**解决方案**：确认 lastController 更新时机；铲球成功后 controllerId 已切换到铲球者，此时进入己方球门确实应判乌龙

### 5.6 Ready 阶段玩家提前移动

**现象**：倒计时未结束玩家已可操作

**根因**：Ready Stage 的 OnEnter 中锁定输入指令未正确下发或被覆盖

**解决方案**：确保 Ready.OnEnter() 中锁定输入在 BuffClear/ResetBornPoint 之后执行，避免重置流程覆盖锁定状态

---

## 六、验收标准

- [ ] 7 阶段（Born→Show→Camera→Ready→Battle→Closeup→Over）正常流转
- [ ] 球物理状态机（None→Idle→PathMove/Free/CantController）转换正确
- [ ] 射门蓄力：力度随蓄力时间线性增长，上限 shootMaxStorageTime
- [ ] 倒挂金钩：球高度 > shootBicycleKickHeight 时触发额外加速
- [ ] 传球贝塞尔曲线：锥角/距离限制有效，弧线高度合理
- [ ] 铲球抢断：球权正确转移，CantController 无敌期生效
- [ ] 进球判定：OnTriggerEnter 准确，乌龙球 (-10) 正确识别
- [ ] 助攻链：assistDuration 窗口内传球者正确记录
- [ ] 计分同步：RpcScore 红蓝分数 + 全角色数据一致
- [ ] 回合换边：Ready 阶段完整重置（Buff/出生点/球位/输入锁定）
- [ ] 随机事件：双倍得分等事件正确触发与结束
- [ ] Buff 区域：区域进出判定正确，效果生效/失效
- [ ] 碰撞处理：出界(Outside)/门框(Woodwork)/墙壁(Wall) 反弹正常
- [ ] 纯 PvP：无 AI 守门员，所有角色均为真实玩家

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-footballparty]]
