# 1 代架构新手训练营（RookieCamp）制作规范

> **适用范围**：RookieCamp 新手训练营 — 新增训练步骤 / 扩展引导任务 / 调整 AI 训练对手
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-rookiecamp（68 文件，★★ 中等，Step 步骤系统 + 任务链，以客户端逻辑为主）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **GameMode 枚举**：`RookieCamp`

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientRookieCampMgr (Client 端新手训练营主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/ClientRookieCampMgr.cs
  │  继承: ClientModeManager
  │  ★ 客户端为主（63/68 文件在 Client 端）
  │
  ├── Logic 层（3 个）
  │     ClientRookieCampAILogic      — AI 训练对手
  │     ClientRookieCampLevelLogic   — 关卡逻辑
  │     ClientRookieCampTaskLogic    — 任务追踪
  │
  ├── Config 层（18 个 SO 配置类）★★
  │     SORookieCampLevelConfig / SORookieCampLevelData / SORookieCampLevelStepConfig
  │     SORookieCampCreateCarInfo / SORookieCampSceneItem
  │     SORookieCampStepAIBornConfig / SORookieCampStepAiUseItem
  │     SORookieCampStepCarMove / SORookieCampStepCarPivot
  │     SORookieCampStepFire / SORookieCampStepGameEnd
  │     SORookieCampStepGrowthTip / SORookieCampStepJumpFly
  │     SORookieCampStepMoveTarget / SORookieCampStepPickItem
  │     SORookieCampStepShootGame / SORookieCampStepSpeedGame
  │     SORookieCampStepUprear
  │
  ├── Step 层（15 个步骤脚本）★★★（核心系统）
  │     RookieCampStepBase (基类)
  │     RookieCampStepFactory (工厂)
  │     ├── RookieCampStepFire           — 射击训练
  │     ├── RookieCampStepMoveTarget     — 移动到目标
  │     ├── RookieCampStepPickItem       — 拾取物品
  │     ├── RookieCampStepFlyJump        — 飞行/跳跃
  │     ├── RookieCampStepCarMove        — 载具驾驶
  │     ├── RookieCampStepShootGame      — 射击小游戏
  │     ├── RookieCampStepSpeedGame      — 竞速小游戏
  │     ├── RookieCampStepUprear         — 扶起队友
  │     ├── RookieCampStepUseMedicine    — 使用药品
  │     ├── RookieCampStepGrowthTip      — 成长提示
  │     ├── RookieCampStepIDCard         — 身份牌
  │     ├── RookieCampStepLook           — 观察目标
  │     └── RookieCampStepGameEnd        — 游戏结束
  │
  ├── Task 层（2 个任务脚本）
  │     RookieCampMainTask   — 主任务
  │     RookieCampSubTask    — 子任务
  │
  ├── Tool 层（7 个编辑器/场景工具）
  │     RookieCampLevelDataMono / RookieCampSceneItemMono
  │     RookieCampSceneItemPointMono / RookieCampAIBornConfigMono
  │     RookieCampAIBornDataConfigMono / RookieCampCarData / RookieCampCarPivotData
  │
  ├── Other 层（触发器/条件/工厂等）
  │     IRookieCampTrigger / RookieCampCondition
  │     RookieCampStartTrigger / RookieCampEndTrigger / RookieCampEventTrigger
  │     RookieCampCarTrigger / RookieCampMoveCheckPoint / RookieCampMoveTargetPath
  │     RookieCampEnemyFactory / RookieCampOperateManager / RookieCampPreload
  │     RookieCampAIBornData / RookieCampDefine
  │
  ├── Stage 层（3 阶段）
  │     InitStage → PlayStage → OverStage
  │
  └── ClientRookieCampData

ServerRookieCampMgr (Server 端新手训练营 — 极简)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/ServerRookieCampMgr.cs
  │  继承: ServerModeManager
  │  ★ 仅 5 个文件（大部分逻辑在客户端）
  │
  ├── Stage: InitStage → PlayStage → OverStage
  └── ServerRookieCampData

配置资源
    86 个 SO 文件 in Assets/ToBundle/ScriptableObject/Mode/RookieCamp/
    19 个特效文件 in Assets/ToBundle/Effect/RookieCamp/
```

### 1.2 Stage 与 Step 双层驱动

```
Stage 层（宏观流程 — 3 阶段）：
  Init → Play → Over

Step 层（微观引导 — 15 种步骤类型）：
  ★ 这是 RookieCamp 的核心设计 — Stage 内嵌 Step 链

PlayStage 内部流程：
  ┌─────────────────────────────────────────┐
  │  Step 1: MoveTarget (移动到指定位置)       │
  │  Step 2: PickItem (拾取武器)              │
  │  Step 3: Fire (射击训练)                  │
  │  Step 4: FlyJump (跳跃/飞行)              │
  │  Step 5: UseMedicine (使用药品)           │
  │  Step 6: Uprear (扶起队友)               │
  │  Step 7: CarMove (载具驾驶)              │
  │  Step 8: ShootGame (射击小游戏)           │
  │  ...                                     │
  │  Step N: GameEnd (训练结束)               │
  └─────────────────────────────────────────┘

  RookieCampStepFactory.Create(stepType)
    → 返回对应 RookieCampStepBase 子类
    → 每步独立的完成条件（RookieCampCondition）
    → 完成后自动推进下一步
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **关卡配置** | `SORookieCampLevelConfig` (86 SO) | Resources/AB | Init |
| **步骤配置** | `SORookieCampStepXxx` (多个) | Resources/AB | PlayStage |
| **AI 出生配置** | `SORookieCampStepAIBornConfig` | Resources/AB | AI 步骤 |
| **特效** | `Assets/ToBundle/Effect/RookieCamp/` | Addressable | 按需 |
| **场景物品** | `RookieCampSceneItemMono` | 场景内 | Init |

---

## 二、新建/扩展 Checklist

### Phase 1：新增训练步骤

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `RookieCampStep{Name}.cs` | 新建 | 继承 `RookieCampStepBase` |
| 2 | `SORookieCampStep{Name}.cs` | 新建 | 步骤配置 SO |
| 3 | `RookieCampStepFactory.cs` | 修改 | 注册新步骤类型 |
| 4 | 关卡 SO 数据 | 修改 | 在关卡配置中添加新步骤 |

### Phase 2：扩展引导任务

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `RookieCampMainTask.cs` | 修改 | 新增主任务节点 |
| 6 | `RookieCampSubTask.cs` | 修改 | 新增子任务 |
| 7 | `ClientRookieCampTaskLogic.cs` | 修改 | 任务流程 |

### Phase 3：扩展 AI 对手

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `ClientRookieCampAILogic.cs` | 修改 | AI 行为扩展 |
| 9 | `RookieCampEnemyFactory.cs` | 修改 | 新增 AI 类型 |
| 10 | AI 配置 SO | 新建 | AI 数值 |

---

## 三、配置文件详解

### 3.1 关卡配置体系（18 种 SO 类型，86 个实例）

**SO 层级关系**：

```
SORookieCampLevelConfig（关卡主入口）
  ├── bornPoint / bornAngle           — 玩家出生点
  ├── autoQuitGameTime                — 超时退出
  ├── isBlockCustomKey                — 屏蔽自定义按键
  ├── teamAISign / aiBornPoint        — 队友AI出生
  ├── wallSign                        — 引导墙效果
  └── stepList[] → SORookieCampLevelStepConfig（步骤序列）
        ├── stepId / stepType          — 步骤ID+类型
        ├── startDelayTime             — 延迟启动
        ├── taskList[]                 — 关联任务ID列表
        ├── validStateList[]           — 允许的角色状态（位标记）
        ├── isBlockMode                — true=黑名单/false=白名单
        └── stepData[] → 各类型专属SO
```

**18 种 SO 配置类型**：

| SO 类型 | 关键字段 | 用途 |
|---------|---------|------|
| `SORookieCampLevelConfig` | bornPoint, stepList[], teamAISign | 关卡主配置 |
| `SORookieCampLevelData` | itemConfig, bornConfig, startTrigger, endTrigger | 关卡通用数据 |
| `SORookieCampLevelStepConfig` | stepId, stepType, taskList[], validStateList[] | 步骤配置 |
| `SORookieCampStepFire` | setRoleHpTime, roleHpValue, bornConfig, aiHpValue | 射击训练参数 |
| `SORookieCampStepMoveTarget` | pathSign, buffMoveRate, instructionIndex | 移动目标参数 |
| `SORookieCampStepPickItem` | taskSign, aiItemPoint, itemPoint, randRadius | 拾取物品参数 |
| `SORookieCampStepCarMove` | maxShowCount, specialPrefabSign, normalPrefabSign, pivotConfig | 载具路径 |
| `SORookieCampStepCarPivot` | pivotList[] (position, rotation) | 路径点列表 |
| `SORookieCampStepJumpFly` | flyCameraAngle, jumpTime, targetPoint, roleLandPoint, preloadRange | 跳伞参数 |
| `SORookieCampStepGameEnd` | bornConfig, instructionTime | 最终战斗 |
| `SORookieCampStepGrowthTip` | growthTipId | 引导图片（Lua调用） |
| `SORookieCampStepShootGame` | bornConfig, isShowLock | 射击小游戏 |
| `SORookieCampStepSpeedGame` | levelData, isMarkEndPoint | 竞速小游戏 |
| `SORookieCampStepAIBornConfig` | ConfigList[] (RookieCampAIBornConfig) | AI批量出生 |
| `SORookieCampStepUprear` | instructionIndex, moveDist | 救援训练 |
| `SORookieCampStepAiUseItem` | aiUseItemData[], useItemCD | AI用药演示 |
| `SORookieCampCreateCarInfo` | carSign, startPos, startAngle | 载具生成 |
| `SORookieCampSceneItem` | items[] (SceneItemData) | 场景固定物品 |

### 3.2 Step 基类与生命周期

```csharp
// RookieCampStepBase.cs — 真实接口
public class RookieCampStepBase {
    public string stepId;                        // 唯一步骤ID
    public RookieCampStepType stepType;           // 步骤类型枚举
    public float startDelayTime;                  // 延迟启动秒数
    public RookieCampRoleState[] validStateList;   // 允许状态列表
    public bool isBlockMode;                      // 黑名单/白名单模式
    public string[] taskList;                     // 关联任务ID

    public virtual void Init(SORookieCampLevelStepConfig config);  // 初始化
    protected virtual void StartStep();    // 延迟后启动
    public virtual void OnUpdate(float delta);   // 帧更新
    protected virtual void EndStep();      // 完成 → 发 RookieCampStepEnd
    public virtual void Clear();           // 清理
}
```

**步骤流转**：
```
ClientRookieCampLevelLogic 遍历 stepList
  → Step.Init() 注册消息
  → 等待 startDelayTime
  → Step.StartStep() 启动关联任务
  → 任务完成 → OnEndTask() 延迟 0.1s
  → Step.EndStep() → 发送 RookieCampStepEnd(stepId)
  → 下一步骤自动激活
```

### 3.3 任务系统（10 种子任务）

**主任务 → 子任务结构**：

```csharp
// RookieCampTaskConfig.txt 字段
id | name | desc | tip | star | isKeyTask | audioId | subTask[]

// 子任务类型枚举（RookieCampDefine.cs）
public enum RookieCampTaskType {
    MoveToPoint,     // 到达检查点
    Look,            // 转动视角 > 0.5度
    PickItem,        // 拾取指定物品
    Kill,            // 击杀N个敌人
    Reload,          // 换弹
    Uprear,          // 救援队友
    UseItem,         // 使用指定物品
    Time,            // 限时存活
    HeadKill,        // 爆头击杀N个
    MoveToCarEndPoint // 到达载具终点
}
```

**完成判定流程**：
```
子任务监听特定消息（如 RookieCampEnterCheckPoint / RookieCampRoleAIDead）
  → 满足条件 → SubTask.IsFinish = true
  → 所有子任务完成 → MainTask.OnSubTaskEnd()
  → 奖励星星（config.star > 0）
  → 关键任务标记（config.isKeyTask → RookieCampEndKeyTask）
  → 通知步骤 → RookieCampEndTask
```

---

## 四、关键代码修改点

### 4.1 13 种训练步骤详解

**步骤枚举**（实际 13 种，WaitPlayer=0 不使用）：

```csharp
public enum RookieCampStepType {
    WaitPlayer = 0,  // 占位符（不使用）
    GrowthTip,       // 引导Tip — 调用Lua显示图片
    FlyJump,         // 跳伞训练 — 跟随AI队长+锁定镜头
    Look,            // 转动视角 — 检测相机角度变化
    MoveTarget,      // 移动到目标 — 路径指引+检查点
    PickItem,        // 拾取物品 — AI演示+物品高亮
    Fire,            // 射击训练 — 刷敌人AI+设玩家HP
    Uprear,          // 救助队友 — AI倒地+玩家学救援
    UseMedicine,     // 使用药品 — AI演示用药时机
    CarMove,         // 载具关卡 — 路径点导航+起终点触发
    GameEnd,         // 游戏结算 — 刷多波敌人+AI无敌演示
    ShootGame,       // 射击小游戏 — EnemyFactory+锁定UI
    SpeedGame,       // 竞速小游戏 — 关卡起终点
    IDCard,          // 身份卡技能 — 装备首个技能+无敌Buff
}
```

**新建步骤模板**：

```csharp
// 1. 在 Step/ 目录新建 RookieCampStep{Name}.cs
public class RookieCampStepNewType : RookieCampStepBase {
    private SORookieCampStepNewType stepData;

    public override void Init(SORookieCampLevelStepConfig config) {
        base.Init(config);
        stepData = config.stepData[0] as SORookieCampStepNewType;
    }

    protected override void StartStep() {
        base.StartStep();
        // 显示引导UI
        ShowUiTips(true);
        // AI行为设置
        if (stepData.instructionIndex >= 0) {
            TeamRoleAI.ClientLogic.GetFeature<ClientRoleAISocialFeature>()
                .ShowAiInstruction(TeamRoleAI.Id, 2, TeamRoleAI.Name,
                    stepData.instructionIndex);
        }
    }

    protected override void EndStep() {
        ShowUiTips(false);
        base.EndStep();
    }
}

// 2. 在 RookieCampStepFactory.CreateStep() 中注册
case RookieCampStepType.NewType:
    step = new RookieCampStepNewType();
    break;
```

### 4.2 触发器系统（5 种触发器）

```csharp
// IRookieCampTrigger 接口（Other/IRookieCampTrigger.cs）
public interface IRookieCampTrigger {
    bool IsHitHide { get; }          // 触发后隐藏
    bool IsHitRoleAI { get; }        // AI是否触发碰撞
    Transform MyTransform { get; }   // 触发器位置
    void SetTriggerData(RookieCampLevelTrigger data);
}

// 触发器数据结构（SO）
public struct RookieCampLevelTrigger {
    public string sign;              // 特效预制体ID
    public Vector3 point;            // 世界坐标
    public Vector3 angle;            // 旋转
    public Vector3 scale;            // 缩放
    public int hitLayerMask;         // 碰撞层（1<<roleLayer）
    public bool isHitHide;           // 触发后自动隐藏
    public bool isHitRoleAI;         // AI碰撞开关
}
```

**5 种触发器**：

| 触发器 | 类 | 发出的消息 | 用途 |
|--------|---|----------|------|
| 开始触发器 | `RookieCampStartTrigger` | `RookieCampCountTimeState.Start` | 训练入口 |
| 结束触发器 | `RookieCampEndTrigger` | `RookieCampCountTimeState.End` | 关卡完成 |
| 事件触发器 | `RookieCampEventTrigger` | `OnEnterAction()` 回调 | 通用碰撞区域 |
| 移动检查点 | `RookieCampMoveCheckPoint` | `RookieCampEnterCheckPoint(pointId)` | 路径导航点 |
| 载具触发器 | `RookieCampCarTrigger` | `RookieCampCarMoveEnterTrigger(triggerId)` | 载具交互 |

**触发流程**（以 MoveTarget 步骤为例）：
```
Step.StartStep() → 加载路径特效(pathSign)
  → 路径包含 RookieCampMoveCheckPoint 组件
  → 玩家进入碰撞体 → OnTriggerEnter()
  → 检查 Layer + AI忽略 + 无拾取冲突
  → OnEnterAction() → Dispatch(RookieCampEnterCheckPoint, pointId)
  → 检查点更新视觉（隐藏/显示节点）
  → 最后一个检查点 → Step.EndStep() → 下一步骤
```

### 4.3 AI 行为系统

**AI 出生配置**：

```csharp
// SORookieCampStepAIBornConfig.cs
public struct RookieCampAIBornConfig {
    public string Sign;                         // AI标识（如"rookie_beginner_1"）
    public Vector3 BornPoint;                   // 刷新位置
    public Vector3 BornAngle;                   // 刷新朝向
    public float BornTime;                      // 延迟时间

    public RookieAIActionConfig[] ActionConfigs; // 行为序列
}

// AI 行为配置
public struct RookieAIActionConfig {
    public byte actionType;          // Move / Pick / Fire / LookAt
    public Vector3[] vec3Values;     // 目标位置数组
    public byte moveType;            // Once / Loop / PingPong
    public bool isLookMove;          // 移动时锁定看玩家
    public bool isRandJump;          // 随机跳跃
    public byte lookType;            // 相对玩家 / 绝对位置
}
```

**AI 行为脚本（RoleAIRookieData Feature）**：

| 方法 | 功能 |
|------|------|
| `SetPathMove()` | AI沿路径点移动 |
| `SetFireTarget()` | AI锁定目标射击 |
| `SetPickItemList()` | AI按序拾取物品 |
| `SetMoveTarget()` | AI移动到指定点 |

**⚠️ 重要：AI 难度是静态的**
- 每个步骤的 AI 行为由 `RookieAIActionConfig` 预设
- **无动态技能检测或适配**
- 难度仅在切换步骤时改变（不同步骤使用不同 AI 配置）
- 玩家进度通过任务完成时间和星星追踪，但**不回馈到 AI**

### 4.4 角色状态控制

**22 种可控状态（位标记）**：

```csharp
public enum RookieCampRoleState {
    Move, Look, Jump, Prone, Crouch, ShowBag, ShowWeaponUI,
    UseMedicine, HoldXcc, Fire, UseStunt, Uprear, SideShoot,
    TopShoot, Skill, UseCar, UseCarrier, ShowAim, ShowPickUp,
    ShowEquipHp, HeavyAttack, AutoPick, Map
}

// 条件判定（RookieCampCondition.cs）
public static bool IsValid(RookieCampRoleState state) {
    if (WarData.IsRookieCampMode) {
        bool result = GetBitsResult(stateFlag, 1 << (int)state);
        return isBlockMode ? !result : result;  // 黑名单反转
    }
    return true;
}
```

- `isBlockMode = true`：validStateList 中的状态被**禁止**（黑名单）
- `isBlockMode = false`：validStateList 中的状态被**允许**（白名单）
- 用于精确控制每个步骤中玩家可做的操作

### 4.5 引导 UI 系统

**11 种 UI 引导类型**：

```csharp
public enum RookieCampUiType {
    Move, Jump, JumpUp, Look, PickUp, Shoot,
    Aim, Reload, Consumables, Uprear, Skill
}

// 步骤中控制显示/隐藏
controller.SetRookieCampUiInfo(RookieCampUiType.Move, true);   // 高亮移动按钮
controller.SetRookieCampUiInfo(RookieCampUiType.Shoot, true);  // 高亮射击按钮
```

**引导图片展示**（GrowthTip 步骤）：
```csharp
// 调用 Lua 函数显示教程图片
GlobalCallLua.Instance.onOpenBeginnerGrowthTip?.Invoke(
    growthTipId,   // 教程图片ID（SO配置）
    EndStep        // 用户关闭后回调
);
```

---

## 五、常见问题与踩坑记录

### 5.1 步骤跳过导致后续步骤无法触发

**现象**：玩家快速通过某步骤后下一步骤不触发

**根因**：`RookieCampStepBase.IsComplete()` 在 OnEnter 同帧返回 true，导致跳过 OnUpdate

**解决方案**：OnEnter 后至少等 1 帧再检查 IsComplete，或在 IsComplete 中加入最小停留时间

### 5.2 AI 对手不按预期行为

**现象**：训练 AI 不攻击玩家或行为不符合教程需求

**根因**：`SORookieCampStepAIBornConfig` 中 AI 类型或行为树配置错误

**解决方案**：检查 `RookieCampEnemyFactory` 创建的 AI 是否使用了正确的行为配置

### 5.3 关卡 SO 配置过多难以管理

**现象**：86 个 SO 文件，修改某步骤参数时难以找到对应文件

**根因**：配置粒度过细，每个步骤单独一个 SO

**解决方案**：使用 `RookieCampLevelDataMono` 编辑器工具统一管理，不直接编辑单个 SO

---

## 六、验收标准

- [ ] 3 阶段正常流转
- [ ] 15 种步骤类型全部可执行
- [ ] 步骤工厂正确创建所有类型
- [ ] 步骤间自动推进（完成条件 → 下一步）
- [ ] AI 训练对手行为正确
- [ ] 引导 UI 正确显示/隐藏
- [ ] 86 个 SO 配置加载无报错
- [ ] 场景触发器正确触发

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-rookiecamp]]
