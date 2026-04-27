# 1 代架构进化死斗（EvoDeathMatch）制作规范

> **适用范围**：EvoDeathMatch 团队激斗进阶版 — 扩展积分进化 / 疯狂阶段 / 奖励激活系统
> **不适用**：通用模式框架 → 归 [[模式制作]]；标准 TeamMode → 归 [[TeamMode制作]]
> **参考实现**：mode-evodeathmatch（31 文件，★ 中等，含进化机制和疯狂阶段）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **标记机制**：使用 `IsEvoDeathMatch` 标记与标准 TeamMode 区分，GameMode 枚举使用 `PartyMode`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientEvoDeathMatchMgr (Client 端进化死斗主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/ClientEvoDeathMatchMgr.cs
  │  继承: ClientModeManager
  │  职责: 进化死斗客户端入口，积分进度展示，疯狂阶段表现
  │
  ├── ClientEvoDeathLogic
  │     职责: 核心逻辑（进化状态/积分更新/技能解锁）
  │
  ├── ClientEvoDeathMapLogic
  │     职责: 地图逻辑，战场配置读取
  │
  ├── ClientEvoDeathScore
  │     职责: 积分 UI 显示，localScore/maxScore 展示
  │
  ├── Stage 层（4 阶段）
  │     BornStage → StartStage → StageStage → OverStage
  │
  └── ClientEvoDeathMatchData
        含: LocalScore / MaxScore 等

ServerEvoDeathMatchMgr (Server 端进化死斗主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/ServerEvoDeathMatchMgr.cs
  │  继承: ServerModeManager
  │
  ├── ServerEvoDeathLogic      — 核心逻辑（进化/疯狂阶段控制）
  ├── ServerEvoDeathNsqData    — NSQ 数据上报
  ├── ServerEvoDeathBorn       — 出生控制
  ├── ServerEvoDeathRole       — 角色管理（含 AI 飞行）
  ├── ServerEvoDeathDead       — 死亡管理
  ├── ServerEvoDeathScore      — 积分管理（核心系统）
  └── ServerEvoDeathCall       — 召唤/进化触发

数据层
  │  ClientEvoDeathMatchData (LocalScore/MaxScore)
  │  ServerEvoDeathMatchData (MapIndex/BattleTime/...)
  │
  └── SOEvoDeathMatch (主配置)
      SOEvoDeathBattlePoint (战场点配置)
      路径: Assets/ToBundle/ScriptableObject/Mode/EvoDeathMatch/ (6 个配置文件)

标记机制
    IsEvoDeathMatch = true  ← 区分标准 TeamMode
    GameMode 枚举使用 PartyMode（共享枚举值）
```

### 1.2 Stage 阶段流转

```
4 阶段制（含疯狂阶段动态触发）：

Born (出生阶段)
  │  按队伍分配出生点
  │  加载 SOEvoDeathMatch + SOEvoDeathBattlePoint
  ↓
Start (开始阶段)
  │  显示对战信息
  │  初始化积分系统
  │  重置进化状态
  ↓
Stage (战斗阶段) ← 核心
  │  常规战斗：
  │    ├── 击杀得分 → localScore++
  │    ├── 积分达到阈值 → 触发进化（解锁武器/能力）
  │    │     Level 1: 空投武器（基础强化）
  │    │     Level 2: 高级头甲（防御强化）
  │    │     Level 3: 强力道具（终极形态）
  │    └── 所有玩家积分总和超阈值 → CheckCrazyStage()
  │  疯狂阶段：
  │    ├── 得分翻倍
  │    ├── 刷新速度加快
  │    └── 特效/音效增强
  │  判定：
  │    ├── 时间到 → Over
  │    └── 某队积分达标 → Over
  ↓
Over (游戏结束)
    汇总最终积分，排名展示
    AI 飞行离场动画
```

### 1.3 进化等级系统

```
积分阈值 → 进化等级：

Level 0 (初始)
  │  基础武器、无额外能力
  │  localScore < threshold_1
  ↓
Level 1 (空投武器)
  │  达到 threshold_1 → 解锁空投武器
  │  获得随机强力武器
  ↓
Level 2 (高级头甲)
  │  达到 threshold_2 → 解锁高级防具
  │  头盔 + 护甲等级提升
  ↓
Level 3 (强力道具)
  │  达到 threshold_3 → 终极形态
  │  获得特殊道具（如无敌盾/瞬移）

★ 进化是单向的，死亡不会降级
★ 每个等级的奖励由 SOEvoDeathMatch 配置
```

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/EvoDeathMatch/` (6 个) | Resources/AB | Mgr.Init() |
| **战场配置** | `SOEvoDeathBattlePoint` | Resources/AB | Born |
| **进化特效** | 升级光效 / 解锁动画 | EffectManager | 达到阈值时 |
| **疯狂模式** | 全屏滤镜 / 增强音效 | PostProcess | CheckCrazyStage() |

### 1.5 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 中 `PartyMode` 枚举值 — EvoDeathMatch 共用此值，通过 IsEvoDeathMatch 标记区分
- **SOGameSetting** 全局设置 — 仅可读取，不可修改

---

## 二、新建/扩展 Checklist

### Phase 1：调整进化阈值

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `SOEvoDeathMatch.asset` | 修改 | 调整 3 级进化积分阈值/奖励内容 |
| 2 | `SOEvoDeathBattlePoint.asset` | 修改 | 调整战场出生点/区域 |

### Phase 2：新增 Logic

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 3 | `Client/Modules/Mode/EvoDeathMatch/Client{LogicName}.cs` | 新建 | 客户端 Logic |
| 4 | `Server/Modules/Mode/EvoDeathMatch/Server{LogicName}.cs` | 新建 | 服务端 Logic |
| 5 | `ClientEvoDeathMatchMgr.cs` | 修改 | Init() 注册 |
| 6 | `ServerEvoDeathMatchMgr.cs` | 修改 | Init() 注册 |

### Phase 3：扩展疯狂阶段

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 7 | `ServerEvoDeathLogic.cs` | 修改 | CheckCrazyStage() 条件/效果 |
| 8 | `ClientEvoDeathLogic.cs` | 修改 | 疯狂阶段视觉/音效表现 |

### Phase 4：扩展召唤系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `ServerEvoDeathCall.cs` | 修改 | 新增召唤条件/召唤物 |
| 10 | 客户端表现 | 修改 | 召唤特效/动画 |

### Phase 5：AI 飞行系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | `ServerEvoDeathRole.cs` | 修改 | OnSetAiFly() AI 飞行行为 |
| 12 | AI 配置 | 修改 | 飞行路径/速度参数 |

---

## 三、配置文件详解

### 3.1 SOEvoDeathMatch

**路径**：`Assets/ToBundle/ScriptableObject/Mode/EvoDeathMatch/SOEvoDeathMatch.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `scoreThreshold_1` | int | Level 1 进化积分阈值 |
| `scoreThreshold_2` | int | Level 2 进化积分阈值 |
| `scoreThreshold_3` | int | Level 3 进化积分阈值 |
| `crazyStageThreshold` | int | 疯狂阶段总积分阈值 |
| `crazyScoreMultiplier` | float | 疯狂阶段积分倍率 |
| `battleTime` | float | 战斗时长 |
| `level1Rewards` | int[] | Level 1 奖励武器 ID 列表 |
| `level2Rewards` | int[] | Level 2 奖励装备 ID 列表 |
| `level3Rewards` | int[] | Level 3 奖励道具 ID 列表 |

### 3.2 SOEvoDeathBattlePoint

| 字段 | 类型 | 说明 |
|------|------|------|
| `mapIndex` | int | 地图索引 |
| `spawnPoints` | Transform[] | 出生点列表 |
| `itemSpawnAreas` | Rect[] | 道具刷新区域 |
| `aiFlyPaths` | Vector3[][] | AI 飞行路径 |

### 3.3 核心数据类

```csharp
// 客户端数据
public class ClientEvoDeathMatchData {
    public SOEvoDeathMatch Config;
    public int LocalScore;              // 本地积分
    public int MaxScore;                // 最高积分（排行榜用）
    public int CurrentLevel;            // 当前进化等级 (0-3)
    public bool IsCrazyStage;           // 是否进入疯狂阶段
}

// 服务端数据
public class ServerEvoDeathMatchData {
    public int MapIndex;                // 当前地图
    public float BattleTime;            // 剩余战斗时间
    public Dictionary<int, int> RoleScores;    // 角色积分
    public Dictionary<int, int> RoleLevels;    // 角色进化等级
    public bool IsCrazyStage;                  // 疯狂阶段标记
    public int TotalScore;                     // 全场总积分
}
```

---

## 四、关键代码修改点

### 4.1 积分进化判定

**文件**：`ServerEvoDeathScore.cs`

```csharp
public class ServerEvoDeathScore : ServerLogicBase {
    
    public void AddScore(int roleId, int score) {
        // 疯狂阶段积分翻倍
        if (data.IsCrazyStage) {
            score = (int)(score * data.Config.crazyScoreMultiplier);
        }
        
        data.RoleScores[roleId] += score;
        data.TotalScore += score;
        
        int newScore = data.RoleScores[roleId];
        int curLevel = data.RoleLevels[roleId];
        
        // 检查进化
        if (curLevel < 3 && newScore >= data.Config.scoreThreshold_3) {
            EvolveRole(roleId, 3);
        } else if (curLevel < 2 && newScore >= data.Config.scoreThreshold_2) {
            EvolveRole(roleId, 2);
        } else if (curLevel < 1 && newScore >= data.Config.scoreThreshold_1) {
            EvolveRole(roleId, 1);
        }
        
        // 检查疯狂阶段
        mgr.GetLogic<ServerEvoDeathLogic>().CheckCrazyStage();
        
        // 同步积分给客户端
        SyncScoreData(roleId, newScore);
    }
    
    private void EvolveRole(int roleId, int level) {
        data.RoleLevels[roleId] = level;
        
        // 发放对应等级奖励
        int[] rewards = level switch {
            1 => data.Config.level1Rewards,
            2 => data.Config.level2Rewards,
            3 => data.Config.level3Rewards,
            _ => Array.Empty<int>()
        };
        
        foreach (int rewardId in rewards) {
            GiveReward(roleId, rewardId);
        }
        
        // 通知客户端播放进化特效
        SendRpc(new RpcEvolve { roleId = roleId, level = level });
    }
}
```

### 4.2 疯狂阶段触发

**文件**：`ServerEvoDeathLogic.cs`

```csharp
public class ServerEvoDeathLogic : ServerLogicBase {
    
    public void CheckCrazyStage() {
        if (data.IsCrazyStage) return;  // 已在疯狂阶段
        
        // 全场总积分超过阈值 → 进入疯狂阶段
        if (data.TotalScore >= data.Config.crazyStageThreshold) {
            data.IsCrazyStage = true;
            
            // 全体通知
            SendRpcToAll(new RpcCrazyStage { 
                enabled = true,
                scoreMultiplier = data.Config.crazyScoreMultiplier
            });
            
            // 加速道具刷新
            AccelerateItemSpawn();
            
            Log.Info("[EvoDeathMatch] 疯狂阶段已激活！总积分: " + data.TotalScore);
        }
    }
}
```

### 4.3 IsEvoDeathMatch 标记

```csharp
// 模式注册时设置标记
public class ServerEvoDeathMatchMgr : ServerModeManager {
    
    public override void Init() {
        base.Init();
        
        // ★ 关键标记：区分标准 TeamMode
        GameData.IsEvoDeathMatch = true;
        
        data = new ServerEvoDeathMatchData();
        data.Config = LoadSOConfig<SOEvoDeathMatch>();
        
        AddLogic(new ServerEvoDeathLogic());
        AddLogic(new ServerEvoDeathBorn());
        AddLogic(new ServerEvoDeathRole());
        AddLogic(new ServerEvoDeathDead());
        AddLogic(new ServerEvoDeathScore());
        AddLogic(new ServerEvoDeathCall());
        AddLogic(new ServerEvoDeathNsqData());
    }
    
    public override void Destroy() {
        GameData.IsEvoDeathMatch = false;  // 清除标记
        base.Destroy();
    }
}
```

### 4.4 AI 飞行系统

**文件**：`ServerEvoDeathRole.cs`

```csharp
public class ServerEvoDeathRole : ServerLogicBase {
    
    // AI 飞行行为（结束时的离场动画）
    public void OnSetAiFly(int aiRoleId) {
        var aiRole = mgr.GetRole(aiRoleId);
        if (aiRole == null) return;
        
        // 获取飞行路径
        var flyPath = data.Config.battlePoint.aiFlyPaths[aiRoleId % pathCount];
        
        // 启动飞行动画
        aiRole.StartFlyPath(flyPath, flySpeed, () => {
            // 飞行结束后移除 AI
            mgr.RemoveRole(aiRoleId);
        });
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 IsEvoDeathMatch 标记未清除

**现象**：退出 EvoDeathMatch 后进入其他模式，行为异常

**根因**：Mgr.Destroy() 中未重置 `GameData.IsEvoDeathMatch = false`

**解决方案**：
1. 在 Destroy() 中显式清除标记
2. 在其他模式 Init() 中检查并重置标记（防御性编程）
3. 使用模式切换统一清理机制

### 5.2 进化等级跳级

**现象**：玩家积分瞬间很高，直接从 Level 0 跳到 Level 3，跳过了 Level 1/2 的奖励

**根因**：AddScore() 中的等级检查是 if-else if 链，一次只升一级

**解决方案**：
1. 使用 while 循环检查，允许连续升级：
```csharp
while (curLevel < 3) {
    int nextThreshold = GetThreshold(curLevel + 1);
    if (newScore >= nextThreshold) {
        curLevel++;
        EvolveRole(roleId, curLevel);
    } else break;
}
```
2. 确保每级奖励都发放，不会跳过

### 5.3 疯狂阶段积分翻倍计算错误

**现象**：疯狂阶段后积分增长过快或不按倍率计算

**根因**：`crazyScoreMultiplier` 被错误地应用了多次（比如 Score Logic 和 Kill Logic 各乘一次）

**解决方案**：
1. 积分倍率只在 `AddScore()` 入口统一应用一次
2. 其他 Logic 调用 `AddScore(roleId, rawScore)` 传原始分
3. 添加单元测试验证倍率计算

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 使用 `PartyMode` 枚举 + `IsEvoDeathMatch` 标记
- [ ] Factory 双端已注册
- [ ] 不与标准 TeamMode 枚举冲突

### 6.2 配置

- [ ] SOEvoDeathMatch 3 级进化阈值递增
- [ ] SOEvoDeathBattlePoint 出生点/区域合理
- [ ] 疯狂阶段阈值 > Level 3 阈值 × 玩家数

### 6.3 运行时

- [ ] 4 阶段正常流转（Born→Start→Stage→Over）
- [ ] 积分正确累计
- [ ] 3 级进化正确触发（含跳级场景）
- [ ] 疯狂阶段正确激活（积分翻倍/刷新加速）
- [ ] AI 飞行离场正常
- [ ] 死亡不降级

### 6.4 兼容性

- [ ] 不影响标准 TeamMode
- [ ] IsEvoDeathMatch 标记正确设置/清除
- [ ] 退出后不残留状态

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-evodeathmatch]] · [[TeamMode制作]]
