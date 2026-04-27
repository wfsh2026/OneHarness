# 1 代架构淘汰赛（Knockout）制作规范

> **适用范围**：Knockout 淘汰赛 — 新增赛制 / 扩展 Node 关卡 / 调整竞速/生存规则
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-knockout（125 文件，★★★★ 复杂，ExtendGameWorldFeature + Node 编辑器 + 4 赛制 + 14 Server Logic）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **架构差异**：⚠️ 使用 `ExtendGameWorldFeature` + `AbsKnockoutPlaying` + KnockoutLogicMgr/DataMgr
> **GameMode 枚举**：`LimitedtimeKnockout=14`
> **Proto API_ID**: 22

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientKnockoutPlaying (Client 端淘汰赛主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutPlaying.cs
  │  继承: AbsKnockoutPlaying（非 ClientModeManager）
  │  架构: ExtendGameWorldFeature
  │
  ├── Client Logic（11 个）
  │     ClientKnockoutMainLogic        — 主逻辑协调
  │     ClientKnockoutDeadCheckLogic   — 死亡区域检测
  │     ClientKnockoutBornCheckLogic   — 出生点检测
  │     ClientKnockoutItemLogic        — 道具管理
  │     ClientKnockoutBoxLogic         — 箱子交互
  │     ClientKnockoutSyncTimeLogic    — 时间同步
  │     ClientKnockoutHeartbeatLogic   — 心跳包
  │     ClientKnockoutMusicLogic       — 音乐播放
  │     ClientKnockoutCameraLogic      — 摄像机控制
  │     ClientKnockoutEffectLogic      — 特效处理
  │     ClientKnockoutUILogic          — UI 更新
  │
  └── Client Data

ServerKnockoutPlaying (Server 端淘汰赛主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutPlaying.cs
  │  继承: AbsKnockoutPlaying
  │
  ├── Server Logic（14 个）★★★
  │     ServerKnockoutMainLogic          — 主逻辑
  │     ServerKnockoutBornLogic          — 玩家出生
  │     ServerKnockoutWinCheckLogic      — 胜利判定
  │     ServerKnockoutTimeCheckLogic     — 超时检测
  │     ServerKnockoutCheckOnlineLogic   — 在线检查
  │     ServerKnockoutCompetitionLogic   — 竞技管理
  │     ServerKnockoutItemLogic          — 道具逻辑
  │     ServerKnockoutPropsLogic         — 道具属性
  │     ServerKnockoutHeartbeatLogic     — 心跳管理
  │     ServerKnockoutReportNsqLogic     — NSQ 上报
  │     ServerKnockoutReportLogLogic     — 日志上报
  │     ServerKnockoutCheatCheckLogic    — 反作弊 ★
  │     ├── 赛制 Logic（4 种）★★ 核心
  │     │     ServerKnockoutSpeedLogic          — 竞速模式
  │     │     ServerKnockoutSpeedVictoryLogic   — 竞速决胜
  │     │     ServerKnockoutSurvivalLogic       — 生存模式
  │     │     ServerKnockoutSurvivalVictoryLogic — 生存决胜
  │
  └── Server Data

Host 层 — AbsKnockoutPlaying ★★
    KnockoutLogicMgr — 逻辑管理器（IKnockoutLogic 接口）
    KnockoutDataMgr  — 数据管理器
    TimerRegister    — 定时器注册

    Knockout.cs — Node 编辑器系统根类 ★★★

Node 编辑器系统（关卡设计核心）
    节点类型:
      Area / Box / Point / Group / Trap
      ChestPoint / ItemPoint / PvePoint / RoleAIPoint
    父节点容器:
      BirthNodeParent / DeadNodeParent / ItemNodeParent
      等 11 个 NodeParent
    数据类:
      KnockoutData / AreaData / BoxData / PointData
      CheatAreaData / KnockoutDataMgr

道具系统
    ClientKnockoutItemLogic / ServerKnockoutItemLogic
    KnockoutRandomItem — 随机道具
    KnockoutItemMessage — 道具消息

配置
    SOKnockoutConfig.asset — 主配置
    SOKnockoutRule.asset — 赛制规则基类
    SOKnockoutSpeedRule.asset / SOKnockoutSurvivalRule.asset
    Fog 效果配置（11 个）
    Screen 设置（20 个）
    关卡数据 Root_Knockout_*.txt
```

### 1.2 Stage 与赛制系统

```
4 Stage + 4 赛制交叉设计：

KnockoutStage 枚举（线性）:
  Init(1) → Show(2) → Start(3) → GameOver(4)

KnockoutPlaying 枚举（赛制类型 — 在 Start 阶段内）:
  Speed(0)           — 竞速局：谁先到终点谁赢
  SpeedVictory(1)    — 竞速决胜局：淘汰赛竞速
  Survival(2)        — 生存局：在地图上存活
  SurvivalVictory(3) — 生存决胜局：最终生存者

流程：
Init (初始化)
  │  加载 Node 关卡数据
  │  初始化所有节点
  ↓
Show (展示)
  │  关卡预览
  │  赛制说明
  ↓
Start (开始) ← 核心
  │  根据 KnockoutPlaying 枚举选择赛制 Logic:
  │    Speed → ServerKnockoutSpeedLogic
  │    SpeedVictory → ServerKnockoutSpeedVictoryLogic
  │    Survival → ServerKnockoutSurvivalLogic
  │    SurvivalVictory → ServerKnockoutSurvivalVictoryLogic
  │
  │  ServerKnockoutPlayingLogicFactory.InitKnockoutPlayingLogic()
  │  → 动态添加对应赛制 Logic
  │
  │  判定：胜利条件满足 → GameOver
  ↓
GameOver (结束)
    结算/排名/淘汰名单
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOKnockoutConfig.asset` | Resources/AB | Init |
| **赛制规则** | `SOKnockoutSpeedRule/SurvivalRule.asset` | Resources/AB | Init |
| **关卡 Node 数据** | `Root_Knockout_*.txt` | TextAsset | Init |
| **Fog 效果** | 11 个 Fog 配置 | Resources/AB | Show |
| **Screen 设置** | 20 个 Art/Game 设置 | Resources/AB | Show |
| **道具** | 随机道具 Prefab | Addressable | Start |

---

## 二、新建/扩展 Checklist

### Phase 1：新增赛制

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `KnockoutPlaying` 枚举 | 修改 | 新增赛制枚举值 |
| 2 | `ServerKnockout{Type}Logic.cs` | 新建 | 实现 IKnockoutLogic |
| 3 | `ServerKnockoutPlayingLogicFactory` | 修改 | 注册新赛制 |
| 4 | `SOKnockout{Type}Rule.asset` | 新建 | 赛制规则 SO |

### Phase 2：扩展 Node 关卡

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | 新 Node 类型 | 新建 | 继承节点基类 |
| 6 | 新 NodeParent | 新建 | 节点容器 |
| 7 | `Root_Knockout_*.txt` | 新建 | 关卡数据文件 |
| 8 | Node 编辑器 | 修改 | 新节点的编辑器支持 |

### Phase 3：扩展道具

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `KnockoutRandomItem` | 修改 | 新随机道具 |
| 10 | `ClientKnockoutItemLogic` | 修改 | 客户端道具表现 |
| 11 | `ServerKnockoutItemLogic` | 修改 | 服务端道具逻辑 |

---

## 三、配置文件详解

### 3.1 赛制规则配置

```csharp
// SOKnockoutRule — 赛制规则基类
public class SOKnockoutRule : ScriptableObject {
    public float timeLimit;           // 时间限制
    public int maxPlayers;            // 最大人数
    public int eliminateCount;        // 每轮淘汰数
}

// SOKnockoutSpeedRule — 竞速规则
public class SOKnockoutSpeedRule : SOKnockoutRule {
    public float finishLineDistance;  // 终点距离
    public int topNQualify;           // 前 N 名晋级
}

// SOKnockoutSurvivalRule — 生存规则
public class SOKnockoutSurvivalRule : SOKnockoutRule {
    public float shrinkInterval;      // 缩圈间隔
    public float shrinkSpeed;         // 缩圈速度
}
```

### 3.2 Txt 配置表

| 配置 | 字段 | 说明 |
|------|------|------|
| `KnockoutTableConfig` | Id, MatchMode, GameMode, GameName | 赛制主表 |
| `KnockoutRuleTableConfig` | 赛制规则参数 | 规则详情 |
| `KnockoutUICloneObjConfig` | UI 克隆对象配置 | UI 模板 |
| `KnockoutUIObjConfig` | UI 对象配置 | UI 布局 |

---

## 四、关键代码修改点

### 4.1 赛制工厂模式

```csharp
// 赛制 Logic 动态注册
public class ServerKnockoutPlayingLogicFactory {
    public static void InitKnockoutPlayingLogic(
        KnockoutPlaying playingType, KnockoutLogicMgr logicMgr) {
        
        switch (playingType) {
            case KnockoutPlaying.Speed:
                logicMgr.AddLogic(new ServerKnockoutSpeedLogic());
                break;
            case KnockoutPlaying.SpeedVictory:
                logicMgr.AddLogic(new ServerKnockoutSpeedVictoryLogic());
                break;
            case KnockoutPlaying.Survival:
                logicMgr.AddLogic(new ServerKnockoutSurvivalLogic());
                break;
            case KnockoutPlaying.SurvivalVictory:
                logicMgr.AddLogic(new ServerKnockoutSurvivalVictoryLogic());
                break;
        }
    }
}
```

### 4.2 IKnockoutLogic 接口

```csharp
public interface IKnockoutLogic {
    void Init(AbsKnockoutPlaying mgr);
    void OnUpdate(float dt);
    void OnStageChange(KnockoutStage stage);
    void Clear();
}

// 新赛制实现
public class ServerKnockout{Type}Logic : IKnockoutLogic {
    public void Init(AbsKnockoutPlaying mgr) {
        // 初始化赛制规则
    }
    public void OnStageChange(KnockoutStage stage) {
        if (stage == KnockoutStage.Start) {
            // 开始赛制逻辑
        }
    }
}
```

### 4.3 Node 编辑器关卡加载

```csharp
// 从 txt 文件加载 Node 关卡数据
public void LoadKnockoutLevel(string levelName) {
    var txtData = Resources.Load<TextAsset>($"Root_Knockout_{levelName}");
    var rootNode = Knockout.Deserialize(txtData);
    
    // 遍历节点树
    foreach (var node in rootNode.Children) {
        switch (node.Type) {
            case NodeType.Area:
                CreateArea(node as AreaData);
                break;
            case NodeType.Trap:
                CreateTrap(node as TrapData);
                break;
            // ...
        }
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 Node 关卡加载顺序导致节点缺失

**现象**：某些陷阱节点在加载后不可见

**根因**：子节点先于父节点加载，父节点容器未初始化

**解决方案**：确保 NodeParent 先初始化，再加载子节点（拓扑排序或两遍加载）

### 5.2 赛制切换时 Logic 未正确清理

**现象**：从竞速局切换到生存局后仍有竞速计时

**根因**：`ServerKnockoutPlayingLogicFactory` 添加新 Logic 但未清理旧 Logic

**解决方案**：在 `InitKnockoutPlayingLogic()` 开头先 `ClearPlayingLogics()`

### 5.3 死亡区域检测在高速移动时失效

**现象**：玩家高速冲过死亡区域但未被判定死亡

**根因**：`ClientKnockoutDeadCheckLogic` 使用 OnTriggerEnter 检测，高速物体穿透

**解决方案**：使用射线检测或将 Rigidbody 设为 ContinuousDynamic

### 5.4 反作弊误判

**现象**：正常玩家被 `ServerKnockoutCheatCheckLogic` 误判为作弊

**根因**：`CheatAreaData` 定义的安全区域太小，正常移动偶尔超出边界

**解决方案**：增大安全区域容差值，添加连续违规次数阈值

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] IKnockoutLogic 接口正确实现

### 6.2 赛制

- [ ] 4 种赛制正确切换（Speed/SpeedVictory/Survival/SurvivalVictory）
- [ ] 赛制工厂正确注册/清理
- [ ] 竞速终点判定正确
- [ ] 生存缩圈正确

### 6.3 Node 关卡

- [ ] Node 数据正确加载（txt → 节点树）
- [ ] 所有节点类型正确创建
- [ ] 死亡区域检测正常
- [ ] 出生点分配正确

### 6.4 道具与反作弊

- [ ] 随机道具生成正常
- [ ] 反作弊检测准确（低误判率）
- [ ] Proto 22 协议正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-knockout]]
