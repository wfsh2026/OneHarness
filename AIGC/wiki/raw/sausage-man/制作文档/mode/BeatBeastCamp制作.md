# 1 代架构暴打猛兽营（BeatBeastCamp）制作规范

> **适用范围**：BeatBeastCamp 暴打猛兽营 — 新增 Boss / 扩展关卡触发器 / 调整怪物掉落
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-beatbeastcamp（78 文件，★★ 中等，PvE Boss 挑战 + GameTrigger 系统 + 关卡设计编辑器，C/S/H 三端）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **GameMode 枚举**：`BeatCamp=45`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientBeatBeastCampMgr (Client 端暴打猛兽营主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/ClientBeatBeastCampMgr.cs
  │  继承: ClientModeManager
  │
  ├── Logic 层（6 个）
  │     ClientBeastCampLevelLogic         — 关卡管理
  │     ClientBeastGameTriggerMgrLogic    — 触发器管理 ★
  │     ClientBeatBeastCampBornLogic      — 出生逻辑
  │     ClientBeatBeastCampMapLoadLogic   — 地图加载
  │     ClientBeatBeastCampRoleLogic      — 角色管理
  │     ClientSceneMonoUpdateManager      — 场景 Mono 更新
  │
  ├── GameTriggerRunner 层（4 个 — Client 端触发执行）
  │     BeastTriggerCreateAwardRunner        — 创建奖励
  │     BeastTriggerCreateGoldRunnerClient   — 创建金币
  │     BeastTriggerCreateMonsterRunnerClient — 创建怪物
  │     BeastTriggerCreateTargetRunnerClient  — 创建目标
  │
  ├── Mono 层（24 个 — 场景编辑器组件）★★
  │     ├── 关卡设计编辑器
  │     │     BeastCampLevelDesignMenu       — 编辑器菜单
  │     │     BeastCampLevelDesignAIConfig   — AI 配置编辑
  │     │     BeastCampLevelDesignSkillConfig — 技能配置编辑
  │     │
  │     ├── LevelDesignDataMarker/（17 个关卡数据标记）
  │     │     LevelDesignDataManager         — 数据管理器
  │     │     LevelDesignDataMarker          — 通用标记基类
  │     │     AINodeDataMarker / AirWallAreaDataMarker
  │     │     BornPointDataMarker / ChestDataMarker
  │     │     DeadAreaDataMarker / GoldDataMaker
  │     │     LevelAreaDataMarker / LockBuffDataMarker
  │     │     MonsterCoinDataMaker / ParentLevelDataMarker
  │     │     PointDataMarker / SkillConfigDataMarker
  │     │     StarDataMaker / SubLevelDataMarker
  │     │     TransportPointDataMarker / TriggerDataMaker
  │     │
  │     └── 场景组件
  │           BeastCampChangeSceneComponent  — 场景切换
  │           BeastCampLockItem              — 锁定物品
  │
  ├── Stage 层（3 阶段）
  │     BornStage → GameStage → OverStage
  │
  └── ClientBeatBeastCampData / ClientBeatBeastCampEventId

ServerBeatBeastCampMgr (Server 端暴打猛兽营)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/ServerBeatBeastCampMgr.cs
  │  继承: ServerModeManager
  │
  ├── Logic 层（8 个）
  │     ServeBeastCampStatisticsLogic       — 统计数据
  │     ServerBeastCampMonsterDropLogic     — 怪物掉落 ★
  │     ServerBeastGameTriggerMgrLogic      — 触发器管理
  │     ServerBeatBeastCampBornLogic        — 出生
  │     ServerBeatBeastCampLevelLogic       — 关卡
  │     ServerBeatBeastCampMonsterLogic     — 怪物管理 ★
  │     ServerBeatBeastCampNsqDataLogic     — NSQ
  │     ServerBeatBeastCampRoleLogic        — 角色
  │
  ├── GameTriggerRunner 层（3 个 — Server 端触发执行）
  │     BeastTriggerCreateGoldRunnerServer
  │     BeastTriggerCreateMonsterRunnerServer
  │     BeastTriggerCreateTargetRunnerServer
  │
  ├── SOData（2 个配置类）
  │     SOBeatBeastCampConfig / SOBeatBeastCampLevelConfig
  │
  └── SeverBeatBeastCampData / ServerBeatBeastCampEventId

Host 层 ★★（19 个文件 — 关卡触发器系统核心）
    BeastCampMonsterDefine            — 怪物定义
    HostBeastCampLevelLogic           — 关卡逻辑（Host 端）
    
    GameTriggerRunner/（17 个触发器脚本）
      BeastCodeBlockMgr / BeastCodeBlockTrigger
      BeastGameMoveRotate / BeastGameTrigger / BeastGameTriggerManager
      BeastGoldTrigger / BeastStarTrigger / BeastTriggerLightOnBlock
      
      SOBeastTrigger/（SO 触发器配置 — 8 种类型）
        SOBeastTriggerBase (基类)
        SOBeastTriggerArea / SOBeastCollectionSpawn
        SOBeastTriggerCreateAward / SOBeastTriggerCreateGold
        SOBeastTriggerCreateMonster / SOBeastTriggerCreateTarget
        SOBeastTriggerMove / SOBeastTriggerRotation

配置资源
    63 个 SO 文件 in Assets/ToBundle/ScriptableObject/Mode/BeatBeastCamp/
    角色控制器 in Assets/ToBundle/Role/Controllers/War/TimeModeBeastCamp/
    特效 in Assets/ToBundle/Effect/Mode/BeatBeastCamp/
```

### 1.2 GameTrigger 系统（核心）

```
BeatBeastCamp 的 GameTrigger 三端协作架构：

Host 端（定义 + 配置 — 17 文件）
  │  SOBeastTriggerBase → 8 种 SO 触发器类型
  │  BeastGameTriggerManager → 管理所有触发器实例
  │  BeastGameTrigger → 单个触发器逻辑
  │
  ├── 触发条件：区域进入 / 时间 / 击杀数 / 拾取
  └── 触发结果：创建怪物 / 创建金币 / 创建奖励 / 移动/旋转

Client 端（表现执行 — 4 Runner）
  │  BeastTriggerCreateAwardRunner → 奖励表现
  │  BeastTriggerCreateGoldRunnerClient → 金币特效
  │  BeastTriggerCreateMonsterRunnerClient → 怪物生成表现
  │  BeastTriggerCreateTargetRunnerClient → 目标表现
  │
  └── ClientBeastGameTriggerMgrLogic → 管理 Client Runner

Server 端（逻辑执行 — 3 Runner）
  │  BeastTriggerCreateGoldRunnerServer → 金币数据
  │  BeastTriggerCreateMonsterRunnerServer → 怪物创建
  │  BeastTriggerCreateTargetRunnerServer → 目标创建
  │
  └── ServerBeastGameTriggerMgrLogic → 管理 Server Runner
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOBeatBeastCampConfig` (63 SO) | Resources/AB | Init |
| **关卡配置** | `SOBeatBeastCampLevelConfig` | Resources/AB | Init |
| **怪物资源** | 各种 Boss/小怪 Prefab | Addressable | GameStage |
| **角色控制器** | `War/TimeModeBeastCamp/` | AnimController | Born |
| **特效** | `Effect/Mode/BeatBeastCamp/` | Addressable | 按需 |

---

## 二、新建/扩展 Checklist

### Phase 1：新增 Boss 类型

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `BeastCampMonsterDefine.cs` | 修改 | 新增怪物类型枚举 |
| 2 | 怪物 SO 配置 | 新建 | Boss 数值/技能/AI |
| 3 | `ServerBeatBeastCampMonsterLogic` | 修改 | Boss 逻辑 |
| 4 | Boss Prefab | 新建 | 模型/动画/特效 |

### Phase 2：扩展关卡触发器

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `SOBeastTrigger{Type}.cs` | 新建 | 继承 SOBeastTriggerBase |
| 6 | `BeastTriggerCreate{Type}Runner` | 新建 | Client/Server 双端 Runner |
| 7 | `BeastGameTriggerManager` | 修改 | 注册新触发器 |
| 8 | 新 DataMarker | 新建 | 场景编辑器标记 |

### Phase 3：扩展掉落

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `ServerBeastCampMonsterDropLogic` | 修改 | 新掉落规则 |
| 10 | 掉落 SO 配置 | 新建 | 掉落表 |

---

## 三、配置文件详解

### 3.1 SO 触发器配置体系

```
SOBeastTriggerBase (基类)
  │  triggerType: TriggerType      — 触发类型
  │  condition: TriggerCondition   — 触发条件
  │  delay: float                  — 延迟时间
  │
  ├── SOBeastTriggerArea           — 区域触发
  ├── SOBeastCollectionSpawn       — 收集物生成
  ├── SOBeastTriggerCreateAward    — 奖励创建
  ├── SOBeastTriggerCreateGold     — 金币创建
  ├── SOBeastTriggerCreateMonster  — 怪物创建
  ├── SOBeastTriggerCreateTarget   — 目标创建
  ├── SOBeastTriggerMove           — 移动触发
  └── SOBeastTriggerRotation       — 旋转触发
```

### 3.2 关卡数据标记系统

| DataMarker 类型 | 用途 |
|----------------|------|
| `BornPointDataMarker` | 玩家出生点 |
| `AINodeDataMarker` | AI 路径节点 |
| `ChestDataMarker` | 宝箱位置 |
| `MonsterCoinDataMaker` | 怪物金币 |
| `TransportPointDataMarker` | 传送点 |
| `DeadAreaDataMarker` | 死亡区域 |
| `AirWallAreaDataMarker` | 空气墙 |
| `LevelAreaDataMarker` | 关卡区域 |
| `SubLevelDataMarker` | 子关卡 |

---

## 四、关键代码修改点

### 4.1 新增 SO 触发器

```csharp
// 1. 新触发器配置
[CreateAssetMenu(menuName = "BeatBeastCamp/Trigger/{Type}")]
public class SOBeastTrigger{Type} : SOBeastTriggerBase {
    public {TypeSpecificData} data;
    
    public override void Execute(BeastGameTrigger trigger) {
        // 执行触发逻辑
    }
}

// 2. 对应的三端 Runner
// Host 端由 SOBeastTriggerBase 统一处理
// Client 端
public class BeastTriggerCreate{Type}RunnerClient {
    public void OnTrigger(TriggerData data) {
        // 客户端表现
    }
}
// Server 端
public class BeastTriggerCreate{Type}RunnerServer {
    public void OnTrigger(TriggerData data) {
        // 服务端逻辑
    }
}
```

### 4.2 关卡数据标记使用

```csharp
// 在场景编辑器中放置 DataMarker，运行时由 LevelDesignDataManager 收集
public class LevelDesignDataManager : MonoBehaviour {
    public void CollectAllMarkers() {
        var markers = FindObjectsOfType<LevelDesignDataMarker>();
        foreach (var marker in markers) {
            switch (marker.DataType) {
                case BeastCampLevelDesignDataType.BornPoint:
                    bornPoints.Add(marker.transform.position);
                    break;
                case BeastCampLevelDesignDataType.Monster:
                    monsterSpawns.Add(marker.GetComponent<AINodeDataMarker>());
                    break;
                // ...
            }
        }
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 触发器执行顺序不一致

**现象**：同一区域多个触发器执行顺序在不同端不一致

**根因**：`BeastGameTriggerManager` 遍历顺序依赖 Dictionary（无序）

**解决方案**：触发器添加优先级字段，按优先级排序执行

### 5.2 Boss 战怪物数量过多导致卡顿

**现象**：Boss 召唤大量小怪后帧率骤降

**根因**：每个小怪都有独立的 AI + 动画 + 碰撞

**解决方案**：设置最大同屏怪物数量，远处怪物使用 LOD 或简化表现

### 5.3 DataMarker 场景修改后配置丢失

**现象**：编辑器中修改 DataMarker 位置后，运行时位置不对

**根因**：DataMarker 数据在 SO 和场景 Mono 中双重存储，修改时只改了一处

**解决方案**：使用 `LevelDesignDataManager` 统一管理，运行时从场景 Mono 实时读取

---

## 六、验收标准

- [ ] 3 阶段正常流转
- [ ] GameTrigger 三端触发器正确执行
- [ ] Boss 战完整流程
- [ ] 怪物掉落正常
- [ ] 关卡 DataMarker 正确加载
- [ ] 8 种 SOBeastTrigger 类型正确触发
- [ ] 金币/星星/宝箱收集正常
- [ ] 场景切换正常

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-beatbeastcamp]]
