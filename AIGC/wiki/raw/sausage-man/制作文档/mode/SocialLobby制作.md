# 1 代架构互动大厅（SocialLobby）制作规范

> **适用范围**：SocialLobby 互动大厅 — 新增小游戏 / 扩展社交互动 / 调整 NPC 事件
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-sociallobby（56 文件，★★ 中等，含射击/转圈/迷你组队等子玩法，C/S/H 三端）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **GameMode 枚举**：`InteractionSpace=25`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientSocialLobbyMgr (Client 端互动大厅主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/ClientSocialLobbyMgr.cs
  │  继承: ClientModeManager
  │
  ├── Logic 层
  │     ClientSocialLobbyGroupLogic     — 分组/组队
  │     ClientSocialLobbyInitItemLogic  — 场景物品初始化
  │
  ├── Other 子系统 ★（21 个文件 — 大厅特色系统）
  │     ├── PlayerSceneAvatar            — 玩家场景化身
  │     ├── LobbyChangeSceneCmpt        — 切换场景组件
  │     ├── LobbyEventNpc               — 事件 NPC
  │     │
  │     ├── MiniGameTeam/               — 迷你组队游戏
  │     │     ClientMiniGameTeamData
  │     │
  │     ├── RedPacketRain/              — 红包雨活动 ★
  │     │     RedPacketRainNpcHelper / RedPacketRainNpcModel
  │     │     RedPacketRainPoint / WealthGodNpcHelper
  │     │
  │     └── ShootGame/                  — 射击小游戏 ★★（14 个文件）
  │           SocialLobbyShootGameMono / SocialLobbyShootGameMonoTool
  │           SocialLobbyShootGameCheckPointMono / DeadArea / EndArea
  │           RankArea / RebornArea / ScorePointMono / StartArea
  │           TargetMono / TriggerArea / ItemGroupMono
  │           ILobbyShootGameMonoObj (接口)
  │
  ├── Stage 层（3 阶段）
  │     InitStage → RunningStage → OverStage
  │
  └── ClientSocialLobbyData

ServerSocialLobbyMgr (Server 端互动大厅主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/ServerSocialLobbyMgr.cs
  │  继承: ServerModeManager
  │
  ├── Logic 层
  │     ServerSocialLobbyEventLogic     — 活动事件管理
  │     ServerSocialLobbyGroupLogic     — 组队
  │     ServerSocialLobbyInitItemLogic  — 场景物品
  │     ServerSocialLobbyRoleLogic      — 角色管理
  │
  ├── Other 子系统
  │     ServerLobbyEventData            — 活动数据
  │     ├── CircleGame/                 — 转圈游戏
  │     │     ServerSocialLobbyCircleGameManager
  │     ├── MiniGameTeam/               — 迷你组队
  │     │     IMiniGameMgr / ServerMiniGameTeamData
  │     └── ShootGame/                  — 射击小游戏（服务端）
  │           IServerLobbyShootGameFeature / ServerLobbyShootGameCopy
  │           ServerLobbyShootGameCopy_Log / _Rank / _Role / _State
  │           ServerLobbyShootGamePlayerData / RankData
  │           RebornPoint / ScorePoint / TargetPoint / CheckPoint
  │
  └── ServerSocialLobbyData

Host 层
    LobbyMiniGameHelper          — 迷你游戏辅助
    MiniGameTeamPlayerData       — 组队玩家数据
    SocialLobbyDefine            — 大厅常量定义

ExtendGameWorldFeature 层 ★
    Client:
      ClientLobbyPKFeatureManager        — 大厅 PK 系统
      ClientSocialLobbyMiniGameTeamManager — 迷你组队管理
      ClientSocialLobbyShootGameManager  — 射击游戏管理
    Server:
      ServerLobbyPKFeatureManager
      ServerSocialLobbyCircleGameRankManager
      ServerSocialLobbyMiniGameTeamManager
      ServerSocialLobbyShootGameManager
```

### 1.2 Stage 阶段流转

```
3 阶段制（社交模式简洁设计）：

Init (初始化)
  │  加载大厅场景
  │  初始化 NPC / 场景物品
  │  初始化小游戏系统
  ↓
Running (运行中) ← 核心（长期状态）
  │  自由社交活动：
  │    ├── 玩家自由走动/交互
  │    ├── NPC 事件触发（活动/红包雨）
  │    ├── 小游戏入口（射击/转圈/PK/迷你组队）
  │    ├── 场景化身系统
  │    └── 无明确胜负条件
  ↓
Over (结束)
    退出大厅
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **大厅配置** | `SOSocialLobbyConfig` | Resources/AB | Init |
| **NPC 配置** | LobbyEventNpc 数据 | 场景内 | Init |
| **射击游戏场景** | ShootGame 区域 Prefab | 场景内 | Init |
| **红包雨资源** | 红包/财神模型 + 特效 | Addressable | 活动触发 |
| **迷你游戏** | MiniGame Prefab | Addressable | 按需 |

---

## 二、新建/扩展 Checklist

### Phase 1：新增小游戏

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | 新 MiniGame 目录 | 新建 | Client/Server 双端 |
| 2 | `IMiniGameMgr` | 实现 | 新小游戏管理器 |
| 3 | ExtendFeatureManager | 新建 | 注册到 GameWorld |
| 4 | 场景 Mono 组件 | 新建 | 场景交互入口 |

### Phase 2：扩展 NPC 事件

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `LobbyEventNpc.cs` | 修改 | 新增 NPC 类型 |
| 6 | `ServerLobbyEventData` | 修改 | 新活动数据 |
| 7 | `ServerSocialLobbyEventLogic` | 修改 | 新事件处理 |

### Phase 3：扩展射击小游戏

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | ShootGame Mono 组件 | 新建 | 新射击元素 |
| 9 | `IServerLobbyShootGameFeature` | 实现 | 服务端逻辑 |
| 10 | 积分/排行配置 | 修改 | 调整规则 |

---

## 三、配置文件详解

### 3.1 核心配置（SOSocialLobbyConfig）

```csharp
// Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/SOSocialLobbyConfig.cs
[CreateAssetMenu(menuName = "War/SocialLobby/SOSocialLobbyConfig")]
public class SOSocialLobbyConfig : ScriptableObject {
    [Header("==================== 玩家相关配置 ====================")]
    [Tooltip("玩家无敌Buff")]       public string invincibleBuff;
    [Tooltip("重置坐标冷却时间")]   public int resetPosCoolTime = 10;
    [Tooltip("清理重连时间")]       public int clearReconnectTime = 1;
    [Tooltip("断线清理玩家时间")]   public int disconnectRoleTime = 10;

    [Header("==================== 战场相关配置 ====================")]
    [Tooltip("关闭入口时间")]       public int removeRoomTime;
    [Tooltip("战场时长")]           public int gameTimeMax;
    [Tooltip("没有玩家关闭时间")]   public int noRoleCloseTime = 30;
    [Tooltip("服务器关闭时间")]     public int serverCloseTime = 10;
}
```

**Asset 路径**：`Assets/ToBundle/ScriptableObject/Mode/SocialLobby/SOSocialLobbyConfig.asset`

### 3.2 射击小游戏配置

| 配置类 | 关键字段 | 用途 |
|--------|---------|------|
| `BSOLobbyShootGame` | `GameSign`, `rankingID`, `GameRuleText`, `CheckPointList`, `RebornList`, `ScorePointList` | 射击游戏 Buff SO |
| `BSLobbyShootGameServer` | `Config`(BSOLobbyShootGame), `MyBuffBox` | 服务端射击副本 Buff |

**射击场景组件系统**（14 个 Mono 脚本，全部实现 `ILobbyShootGameMonoObj` 接口）：

```
ILobbyShootGameMonoObj (接口)
  ├── SocialLobbyShootGameStartArea    — 开始区域
  ├── SocialLobbyShootGameEndArea      — 结束区域
  ├── SocialLobbyShootGameDeadArea     — 死亡区域
  ├── SocialLobbyShootGameRebornArea   — 重生区域
  ├── SocialLobbyShootGameCheckPointMono — 检查点
  ├── SocialLobbyShootGameTargetMono   — 射击目标
  ├── SocialLobbyShootGameScorePointMono — 得分点
  ├── SocialLobbyShootGameRankArea     — 排行区域
  └── SocialLobbyShootGameTriggerArea  — 触发区域

SocialLobbyShootGameMono       — 主控脚本
SocialLobbyShootGameMonoTool   — 编辑器工具
SocialLobbyShootGameItemGroupMono — 物品组管理
```

### 3.3 核心枚举定义

```csharp
// Assets/Script/GamePlay/Host/Modules/Mode/SocialLobby/SocialLobbyDefine.cs

// 射击游戏状态
enum LobbyShootGameState {
    None  = 0,   // 游戏未激活
    Wait,        // 倒计时等待
    Start,       // 游戏进行中
    End          // 游戏结束
}

// 射击游戏类型
enum LobbyShootGameType {
    Score = 0,   // 计分模式
    Time  = 1,   // 计时模式
}

// 射击游戏结束条件
enum LobbyShootGameEndCond {
    Time     = 0,   // 时间到
    Complete = 1,   // 全部完成
    Dead     = 2,   // 死亡结束
}

// 加入游戏结果
enum LobbyJoinGameResult {
    Success       = 0,
    GameNotExist  = 1,
    GameFull      = 2,
    AlreadyInGame = 3,
    InPkState     = 4,
    GameStarted   = 5,
}

// 开始游戏结果
enum LobbyStartGameResult {
    Success          = 0,
    NotEnoughPlayers = 1,
    NotLeader        = 2,
    GameNotExist     = 3,
    AlreadyStarted   = 4,
    InCooldown       = 5,
    NotReady         = 6,
}
```

### 3.4 关联配置系统

| 配置系统 | 用途 | 使用位置 |
|---------|------|---------|
| `ItemTabBaseConfig` | 头像图标映射 | `PlayerSceneAvatar:48` |
| `ImageConfig` | 图集配置 | `PlayerSceneAvatar:57` |
| `RedPacketRainConfig` | 红包雨事件调度 | `ServerSocialLobbyEventLogic:54` |
| `PickItemDataConfig` | 道具/Buff 映射 | `ServerLobbyEventData:99` |
| `InteractiveActionConfig` | NPC 互动动作定义 | 事件系统 |
| `SOLobbyPKConfig` | PK 系统配置 | PK 对战 |
| `SOLobbyArtConfig` | 美术/视觉设置 | 场景美化 |

### 3.5 角色同步状态标志

| RoleSyncState 标志 | 含义 | 使用场景 |
|-------------------|------|---------|
| `IsPlayShootGame` | 正在射击游戏中 | 限制同时参与其他活动 |
| `IsPlayCircleGame` | 正在转圈游戏中 | 同上 |
| `IsInPkState` | PK 对战中 | 阻止加入小游戏 |
| `IsOnline` | 在线状态 | 断线检测 |
| `IsHandInHand` | 手牵手状态 | 社交互动 |
| `IsUserCar` | 使用载具中 | 切场景限制 |
| `IsHookFly` | 飞行中 | 切场景限制 |
| `IsLobbyGroupLeader` | 组队队长 | 组队权限 |

---

## 四、关键代码修改点

### 4.1 三阶段生命周期（Init → Running → Over）

```csharp
// 服务端阶段系统
// ServerSocialLobbyInitStage — 极短初始化（0.1s 延迟后进入 Running）
// ServerSocialLobbyRunningStage — 核心长期运行阶段
// ServerSocialLobbyOverStage — 清理退出

// Running 阶段核心循环（ServerSocialLobbyRunningStage:27-103）
void OnUpdate(float delta) {
    // 1. 检查 GameState == ServerClose → OnQuit()
    // 2. 检查 removeRoomTime 超时 → UnetRemoveRoom()（关闭入口）
    // 3. 检查 closeTime 超时 → OnQuit()
    // 4. 检查无人时间 → 关闭房间
}
```

**房间关闭逻辑**：
- 当 `roleCnt <= 1` 且超过 `noRoleCloseTime`(30s) → 移除房间入口
- `removeRoomTime` 到达 → 不再接受新玩家
- `serverCloseTime`(10s) 后 → 完全关闭

### 4.2 射击小游戏状态机

```csharp
// ServerLobbyShootGameCopy 通过 partial class 拆分：
// _State — 状态机管理
// _Rank  — 排行榜
// _Role  — 角色管理
// _Log   — 日志记录

// 状态流转（ServerLobbyShootGameCopy_State.cs:3-48）
// None ──(创建游戏)──→ Wait
// Wait ──(config.StartWaitTime 结束)──→ Start
// Start ──(timer 结束 / 完成 / 死亡)──→ End
// End ──(timer 结束)──→ None

// 状态同步（TargetRpc 逐个发送给参与者）
private void SyncGameState() {
    foreach (var playerData in nowPlayList) {
        gameWorld.TargetRpc(new Proto_Lobby.TargetRpcLobbyShootGameSyncState {
            buffId    = ownBuffId,
            gameId    = gameInstId,
            gameState = (int)gameState,
            startTime = stateStartTime,
            endTime   = stateEndTime
        }, role.MyRoleNet);
    }
}
```

**3 种结束条件**：
- `LobbyShootGameEndCond.Time` — 时间到自动结束
- `LobbyShootGameEndCond.Complete` — 全部检查点/目标完成
- `LobbyShootGameEndCond.Dead` — 进入死亡区域

### 4.3 红包雨事件系统

```csharp
// 服务端事件状态机（ServerLobbyEventData.cs:127-131）
enum ServerLobbyEventState {
    None,    // 事件结束
    Start,   // 等待开始
    Finish   // 运行中，等待结束
}

// NPC 状态机（RedPacketRainNpcModel — 6 状态）
enum RedPacketRainNpcState {
    Init,      // 初始化
    Born,      // 入场动画
    Move,      // 移动到目标位置
    WaitDrop,  // 准备动画
    Drop,      // 投放红包
    End        // 退场动画
}
```

**事件驱动流程**：
1. `RedPacketRainConfig` 定义事件调度时间
2. `ServerSocialLobbyEventLogic` 监听触发
3. 创建 NPC 模型 → 6 状态依次执行
4. `PickItemDataConfig` 配置掉落道具映射

### 4.4 组队系统

```csharp
// 客户端组队数据
public class ClientMiniGameTeamData {
    public bool IsPrivate;       // 队伍可见性
    public bool IsSelfTeam;      // 是否自己的队伍
    public bool IsGameStart;     // 游戏已开始
    public int CreateTime;       // 创建时间戳
    public int MaxPlayerNum;     // 最大人数

    // 从网络消息构造
    public ClientMiniGameTeamData(Proto_Lobby.TargetRpcLobbyMiniGameTeamInfo teamInfo) {
        TeamID       = teamInfo.teamId;
        GameSign     = teamInfo.gameSign;
        CreateTime   = teamInfo.createTime;
        MaxPlayerNum = teamInfo.maxPlayerNum;
    }
}

// 队员数据
public class MiniGameTeamPlayerData {
    public bool IsTeamLeader;    // 是否队长
    public bool IsPrepare;       // 准备状态
    public int TeamIndex;        // 队伍编号
    public int JoinTime;         // 加入时间
}
```

**组队同步**：`ClientSocialLobbyGroupLogic` 通过 `CmdLobbyGroupInfo` 向服务端发送组队信息（groupId + players）。

### 4.5 断线检测与重连

```csharp
// ServerSocialLobbyRoleLogic — 每秒检测一次
private const int CHECK_TICK_TIME = 1;

private void CheckDisconnect(BattleRoleLogic role, SOSocialLobbyConfig config) {
    // 阶段 1：清理重连信息（offLineTime > clearReconnectTime）
    if (role.roleLogicServer.offLineTime > config.clearReconnectTime &&
        !role.roleLogicServer.IsClearReconnect) {
        ServerGrpcManager.SendClearTheReconnectionInformation(role, gameWorld);
    }

    // 阶段 2：彻底断线（offLineTime > disconnectRoleTime）
    if (role.roleLogicServer.offLineTime > config.disconnectRoleTime) {
        role.SetState(RoleSyncState.IsOnline, false);
        role.MyRoleNet = null;
        startGame.DisconnectRole(role);
    }
}

// 角色退出大厅
public void RoleExitLobby(BattleRoleLogic roleLogic) {
    ServerGrpcManager.SendClearTheReconnectionInformation(roleLogic, gameWorld);
    gameWorld.MyStartGame.DisconnectRole(roleLogic);
}
```

**断线超时参数**：
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `clearReconnectTime` | 1s | 超时后清理重连信息 |
| `disconnectRoleTime` | 10s | 超时后强制断线 |

### 4.6 玩家场景化身系统（PlayerSceneAvatar）

**核心规则**：游戏头像与 TapTap 头像互斥

```csharp
// PlayerSceneAvatar 通过 ItemTabBaseConfig 和 ImageConfig 加载头像
// 两种头像来源不可同时显示：
// - 游戏内装扮头像（fashionId 映射）
// - TapTap 社交头像（外部 URL 加载）
// 切换时需要清理旧头像资源
```

### 4.7 新增小游戏注册模板

```csharp
// 1. 实现 IMiniGameMgr 接口
public class ServerLobby{NewGame}Manager : IMiniGameMgr {
    public void OnInit() { /* 初始化 */ }
    public void OnUpdate(float dt) { /* 帧更新 */ }
    public void OnPlayerJoin(int roleId) { /* 玩家加入 */ }
    public void OnPlayerLeave(int roleId) { /* 玩家离开 */ }
}

// 2. 在 ServerSocialLobbyMgr 注册
public override void InitLogic() {
    base.InitLogic();
    AddLogic(new ServerSocialLobbyEventLogic());     // 事件系统
    AddLogic(new ServerSocialLobbyGroupLogic());     // 组队系统
    // 新增：AddLogic(new ServerLobby{NewGame}Logic());
}

// 3. 添加网络协议
// 在 Proto_Lobby 中添加对应的 TargetRpc/Cmd 消息
// 射击游戏参考：TargetRpcLobbyShootGameSyncState
// 转圈游戏参考：CircleGame 相关 RPC
```

---

## 五、常见问题与踩坑记录

### 5.1 大厅场景加载卡顿

**现象**：进入互动大厅时长时间黑屏

**根因**：大厅场景资源（NPC/装饰/小游戏区域）同时加载

**解决方案**：分区域延迟加载，玩家靠近时才加载远处区域

### 5.2 红包雨活动大量玩家时同步异常

**现象**：多人同时抢红包时部分玩家显示不一致

**根因**：红包雨事件触发和拾取判定在服务端，但网络延迟导致客户端表现不同步

**解决方案**：红包拾取使用服务端权威判定 + 客户端预测显示

### 5.3 射击小游戏检查点遗漏

**现象**：玩家通过检查点但未被记录

**根因**：`SocialLobbyShootGameCheckPointMono` 碰撞器太小或朝向不对

**解决方案**：增大 Trigger 范围，使用 BoxCollider 替代 SphereCollider

---

## 六、验收标准

- [ ] 3 阶段正常流转
- [ ] NPC 交互正常
- [ ] 射击小游戏完整流程（进入/射击/得分/排行）
- [ ] 红包雨活动正常触发和拾取
- [ ] 迷你组队游戏正常
- [ ] 转圈游戏正常
- [ ] PK 系统正常
- [ ] 场景切换正常（LobbyChangeSceneCmpt）
- [ ] 多人同步正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-sociallobby]]
