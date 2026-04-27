# 1 代架构冲冲派对（GoGoParty）制作规范

> **适用范围**：GoGoParty 冲冲派对/闯关模式 — 新增关卡 / 扩展奖励箱 / 自定义迷你游戏
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-gogoparty（36 文件，★★ 中等，含闯关/奖励箱/回放系统）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientGoGoPartyModeMgr (Client 端冲冲派对主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/ClientGoGoPartyModeMgr.cs
  │  继承: ClientModeManager
  │  职责: 闯关表现、奖励箱拾取、弹幕展示
  │
  ├── ClientGoGoPartyModeActionLogic   — 动作逻辑（跑/跳/冲刺）
  ├── ClientGoGoPartyModeAwardBoxLogic — 奖励箱客户端表现
  ├── ClientGoGoPartyModeBornLogic     — 出生逻辑
  ├── ClientGoGoPartyModeEffectLogic   — 效果逻辑（特效/粒子）
  ├── ClientGoGoPartyModeRoleLogic     — 角色逻辑
  │
  ├── Stage 层（3 阶段 — 最简化）
  │     BornStage → GameStage → OverStage
  │
  ├── Mono 组件
  │     AwardBoxTriggerMono (奖励箱碰撞触发)
  │     AwardDanmuUI (弹幕 UI)
  │     GoGoPartyPrizeWall (奖品墙展示)
  │     OpenAwardBoxUI (开箱 UI)
  │
  └── ClientGoGoPartyModeData

ServerGoGoPartyModeMgr (Server 端冲冲派对主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/ServerGoGoPartyModeMgr.cs
  │  继承: ServerModeManager
  │
  ├── ServerGoGoPartyModeActionLogic    — 动作判定
  ├── ServerGoGoPartyModeAwardBoxLogic  — 奖励箱服务端管理
  ├── ServerGoGoPartyModeBornLogic      — 出生控制
  ├── ServerGoGoPartyModeMiniGameLogic  — ★ 迷你游戏逻辑
  ├── ServerGoGoPartyModeTeamLogic      — 团队逻辑
  ├── ServerGoGoPartyModeRoleLogic      — 角色管理
  ├── ServerGoGoPartyModeAFKLogic       — ★ 挂机检测
  ├── ServerGoGoPartyModeNsqDataLogic   — NSQ 上报
  ├── ServeGoGoPartyModeStatisticsLogic — 统计（⚠️ 注意类名 Serve 非 Server）
  └── ServerGoGoPartyReplayLogic        — ★ 回放系统

事件系统
    ClientGoGoPartyModeEventId (客户端事件 ID)
    ServerGoGoPartyModeEventId (服务端事件 ID)

配置层
    SOGoGoPartyModeConfig (主配置)
    SOGoGoPartyModeAwardBoxConfig (奖励箱配置)
    SOGoGoPartyModeEffectConfig (效果配置)
    GameMode 枚举: GogoParty=47
```

### 1.2 Stage 阶段流转

```
3 阶段制（极简设计）：

Born (出生阶段)
  │  玩家在起点生成
  │  初始化关卡/迷你游戏
  │  加载奖品墙 (GoGoPartyPrizeWall)
  ↓
Game (游戏阶段) ← 核心
  │  闯关流程：
  │    ├── 玩家跑酷/跳跃/冲刺通过障碍
  │    ├── 触碰奖励箱 (AwardBoxTriggerMono)
  │    │     → 打开奖励箱 (OpenAwardBoxUI)
  │    │     → 获得奖励
  │    ├── 迷你游戏关卡 (MiniGameLogic)
  │    │     → 特殊关卡内嵌小游戏
  │    ├── 团队合作/竞争 (TeamLogic)
  │    └── 弹幕互动 (AwardDanmuUI)
  │  挂机检测 (AFKLogic)
  │  回放录制 (ReplayLogic)
  │  判定条件：
  │    ├── 某玩家到达终点 → Over
  │    └── 时间到 → Over
  ↓
Over (游戏结束)
    排名展示（按到达顺序/分数）
    奖品墙结算
    回放可查看
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOGoGoPartyModeConfig` | Resources/AB | Mgr.Init() |
| **奖励箱配置** | `SOGoGoPartyModeAwardBoxConfig` | Resources/AB | Born |
| **效果配置** | `SOGoGoPartyModeEffectConfig` | Resources/AB | Game |
| **奖励箱 Prefab** | 含 AwardBoxTriggerMono 的预制体 | 场景内 | Born |
| **奖品墙** | GoGoPartyPrizeWall Prefab | Addressable | Born |
| **弹幕 UI** | AwardDanmuUI | UIManager | Game |

### 1.4 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 已有枚举值 `GogoParty=47`
- **AwardBoxTriggerMono** 基础碰撞逻辑 — 仅可扩展

---

## 二、新建/扩展 Checklist

### Phase 1：新增关卡

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | 关卡场景文件 | 新建 | 新关卡 .unity 文件 |
| 2 | 关卡配置 | 修改 | SOGoGoPartyModeConfig 添加新关卡引用 |
| 3 | 奖励箱配置 | 修改 | 新关卡的奖励箱位置/内容 |
| 4 | 障碍物/机关 | 新建 | 场景内的交互元素 |

### Phase 2：扩展奖励箱

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `SOGoGoPartyModeAwardBoxConfig` | 修改 | 新增奖励类型 |
| 6 | `ServerGoGoPartyModeAwardBoxLogic.cs` | 修改 | 新增奖励判定逻辑 |
| 7 | `ClientGoGoPartyModeAwardBoxLogic.cs` | 修改 | 新增奖励展示 |
| 8 | `OpenAwardBoxUI` | 修改 | 新增开箱动画/样式 |

### Phase 3：新增迷你游戏

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `ServerGoGoPartyModeMiniGameLogic.cs` | 修改 | 新增迷你游戏规则 |
| 10 | 迷你游戏 UI | 新建 | 对应客户端界面 |
| 11 | 迷你游戏配置 | 新建 | 游戏参数 SO |

### Phase 4：扩展回放系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 12 | `ServerGoGoPartyReplayLogic.cs` | 修改 | 录制新数据类型 |
| 13 | 回放播放器 | 修改 | 对应新数据的播放 |

---

## 三、配置文件详解

### 3.1 SOGoGoPartyModeConfig

| 字段 | 类型 | 说明 |
|------|------|------|
| `levels` | LevelConfig[] | 关卡列表配置 |
| `gameTime` | float | 总游戏时长 |
| `afkTimeout` | float | 挂机判定超时（秒） |
| `maxPlayers` | int | 最大玩家数 |
| `enableReplay` | bool | 是否启用回放 |
| `enableDanmu` | bool | 是否启用弹幕 |

### 3.2 SOGoGoPartyModeAwardBoxConfig

| 字段 | 类型 | 说明 |
|------|------|------|
| `boxId` | int | 奖励箱 ID |
| `rewardType` | RewardType | 奖励类型（金币/道具/时装碎片） |
| `rewardAmount` | int | 奖励数量 |
| `spawnChance` | float | 出现概率 |
| `respawnTime` | float | 重新出现间隔 |

### 3.3 核心 Mono 组件

```csharp
// 奖励箱碰撞触发器
public class AwardBoxTriggerMono : MonoBehaviour {
    public int boxId;
    public SOGoGoPartyModeAwardBoxConfig config;
    
    private void OnTriggerEnter(Collider other) {
        // 玩家触碰 → 发送拾取请求
        if (other.TryGetComponent<BattleRoleController>(out var role)) {
            SendPickupRequest(role.RoleId, boxId);
        }
    }
}

// 弹幕 UI
public class AwardDanmuUI : MonoBehaviour {
    public void ShowDanmu(string message, Color color) {
        // 在屏幕上显示弹幕消息
        // 滚动动画
    }
}

// 奖品墙
public class GoGoPartyPrizeWall : MonoBehaviour {
    public void InitPrizes(List<PrizeData> prizes) {
        // 初始化奖品展示
        // 3D 物品陈列
    }
    
    public void OnPrizeWon(int prizeId, int roleId) {
        // 奖品被获得的动画
    }
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化

```csharp
public class ServerGoGoPartyModeMgr : ServerModeManager {
    
    public override void Init() {
        base.Init();
        data = new ServerGoGoPartyModeData();
        data.Config = LoadSOConfig<SOGoGoPartyModeConfig>();
        
        // 10 个 Logic
        AddLogic(new ServerGoGoPartyModeActionLogic());
        AddLogic(new ServerGoGoPartyModeAwardBoxLogic());
        AddLogic(new ServerGoGoPartyModeBornLogic());
        AddLogic(new ServerGoGoPartyModeMiniGameLogic());
        AddLogic(new ServerGoGoPartyModeTeamLogic());
        AddLogic(new ServerGoGoPartyModeRoleLogic());
        AddLogic(new ServerGoGoPartyModeAFKLogic());
        AddLogic(new ServerGoGoPartyModeNsqDataLogic());
        AddLogic(new ServeGoGoPartyModeStatisticsLogic()); // ⚠️ 类名拼写
        AddLogic(new ServerGoGoPartyReplayLogic());
    }
}
```

### 4.2 迷你游戏系统

```csharp
public class ServerGoGoPartyModeMiniGameLogic : ServerLogicBase {
    
    // 关卡内嵌迷你游戏
    public void StartMiniGame(int miniGameType) {
        switch (miniGameType) {
            case MiniGameType.Quiz:
                // 答题挑战
                StartQuiz();
                break;
            case MiniGameType.RhythmGame:
                // 音乐节奏
                StartRhythm();
                break;
            case MiniGameType.Puzzle:
                // 解谜
                StartPuzzle();
                break;
        }
    }
    
    private void StartQuiz() {
        // 发送题目给所有玩家
        // 答对加速/答错减速
    }
}
```

### 4.3 挂机检测

```csharp
public class ServerGoGoPartyModeAFKLogic : ServerLogicBase {
    private Dictionary<int, float> lastActionTime = new();
    
    public void OnPlayerAction(int roleId) {
        lastActionTime[roleId] = Time.time;
    }
    
    public override void OnUpdate(float deltaTime) {
        float now = Time.time;
        foreach (var (roleId, lastTime) in lastActionTime) {
            if (now - lastTime > data.Config.afkTimeout) {
                // 标记挂机
                OnPlayerAFK(roleId);
            }
        }
    }
    
    private void OnPlayerAFK(int roleId) {
        // 踢出/AI 接管/标记
        Log.Info($"[GoGoParty] 玩家 {roleId} 挂机超时");
    }
}
```

### 4.4 回放系统

```csharp
public class ServerGoGoPartyReplayLogic : ServerLogicBase {
    private List<ReplayFrame> frames = new();
    
    public override void OnUpdate(float deltaTime) {
        if (!data.Config.enableReplay) return;
        
        // 录制帧数据
        var frame = new ReplayFrame {
            timestamp = gameTime,
            rolePositions = CaptureRolePositions(),
            events = CaptureEvents()
        };
        frames.Add(frame);
    }
    
    public ReplayData GetReplayData() {
        return new ReplayData { frames = frames.ToArray() };
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 类名拼写不一致

**现象**：找不到 `ServerGoGoPartyModeStatisticsLogic` 类

**根因**：实际类名为 `ServeGoGoPartyModeStatisticsLogic`（缺少 r），历史遗留拼写错误

**解决方案**：
1. 使用现有类名 `ServeGoGoPartyModeStatisticsLogic`，不要改名（会影响序列化）
2. 新建类时使用正确拼写 `Server...`
3. 在代码注释中标注此拼写问题

### 5.2 奖励箱碰撞触发多次

**现象**：玩家触碰奖励箱后，触发多次拾取事件，获得多份奖励

**根因**：OnTriggerEnter 在物理帧率高时可能多次触发，或 OnTriggerStay 也被监听

**解决方案**：
1. 添加 `isPickedUp` 标记，首次触发后设为 true
2. 服务端校验：相同 boxId 只能被拾取一次
3. 拾取后立即禁用 Collider：`GetComponent<Collider>().enabled = false;`

### 5.3 回放数据量过大

**现象**：长时间比赛的回放数据占用大量内存

**根因**：每帧录制所有玩家位置 + 事件，未做压缩/采样

**解决方案**：
1. 降低录制频率：每 3 帧录制一次
2. 使用增量录制：只记录位移变化
3. 设置最大帧数上限，超过后丢弃最早的帧

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `GogoParty=47` 无冲突
- [ ] Factory 双端已注册
- [ ] Mono 组件编译正常

### 6.2 配置

- [ ] SOGoGoPartyModeConfig 关卡/时间参数合理
- [ ] SOGoGoPartyModeAwardBoxConfig 奖励配置合理
- [ ] 挂机超时合理（不要太短误判）

### 6.3 运行时

- [ ] 3 阶段正常流转（Born→Game→Over）
- [ ] 奖励箱拾取正常（无重复拾取）
- [ ] 迷你游戏正确启动/结算
- [ ] 弹幕系统正常显示
- [ ] 挂机检测正确触发
- [ ] 回放录制/播放正常
- [ ] 团队协作/竞争正常

### 6.4 兼容性

- [ ] 不影响其他模式
- [ ] 新关卡不影响已有关卡
- [ ] 奖品墙展示正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-gogoparty]]
