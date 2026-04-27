# 1 代架构痛击飞球/刀球（BladeBall）制作规范

> **适用范围**：BladeBall 痛击飞球 — 扩展飞球控制 / 新增技能 / 调整 Buff 系统
> **不适用**：通用模式框架 → 归 [[模式制作]]；Common 基础框架 → 归 [[CommonMode制作]]
> **参考实现**：mode-bladeball（65 文件，★★★ 复杂，含独立飞球控制系统）
> **公共框架依赖**：继承 [[CommonMode制作]]（ClientCommonManager / ServerCommonManager）而非直接继承 ModeManager

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientBladeBallModeMgr (Client 端痛击飞球主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallModeMgr.cs
  │  继承: ClientCommonManager ← ★ 继承 Common 而非 ModeManager
  │  职责: 飞球表现、技能操作、皮肤管理
  │
  ├── ClientBladeBallLogic      — 核心逻辑（飞球状态同步）
  ├── ClientBladeBallUILogic    — UI 逻辑（计分板/技能图标）
  ├── ClientBladeBallSkinLogic  — 皮肤逻辑（飞球外观）
  ├── ClientBladeBallSkillLogic — 技能逻辑（技能释放表现）
  ├── ClientBladeBallSkillOperate — 技能操作（输入处理）
  │
  ├── Stage 层（6 阶段）
  │     BornStage → ReadyStage → BattleStage → RoundOverStage → WaitStage → OverStage
  │
  └── ClientBladeBallModeData

ServerBladeBallModeMgr (Server 端痛击飞球主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeMgr.cs
  │  继承: ServerCommonManager ← ★ 继承 Common
  │
  ├── ServerBladeBallLogic           — 核心逻辑（飞球 AI/目标选择）
  ├── ServerBladeBallPointLogic      — 积分逻辑
  ├── ServerBladeBallRevengeLogic    — 复仇逻辑
  ├── ServerBladeBallRuleLogic       — 规则逻辑
  ├── ServerBladeBallModeStatisticsLogic — 统计
  │
  └── 飞球控制系统 ★★★ （独立子系统）
        ServerBladeBallController (服务端飞球控制器)
        ClientBladeBallController (客户端飞球控制器)
        ├── ServerBladeBallSpeedControl (球速控制)
        ├── ServerBladeBallBuffControl (Buff: 冻结/无敌/隐身)
        ├── ServerBladeBallPropertyControl (属性控制)
        └── 球体状态机（11 个状态）
              Appear / BeHit / BecauseWeak / Confused / Control
              HitRole / Move / None / ReadyMove / ...

网络层
    BladeBallC2S / BladeBallC2SMirror (客户端消息)
    BladeBallNetwork / BladeBallNetworkMirror (网络同步)

数据层
    ClientBladeBallModeData
    ServerBladeBallModeData
    BladeBallModeRebornRunningData (复活运行时数据)
    BattleCommonDynamicData_BladeBallMode (继承 Common 的动态数据)

配置层
    SOBladeBallModeData (主配置)
    SOBladeBallModeExtData (扩展配置)
    SOBladeBallModeMeleeData (近战配置)
    GameMode 枚举: Bladeballmode=24
```

### 1.2 Stage 阶段流转

```
6 阶段制（含 Wait 等待阶段）：

Born (出生)
  │  玩家在场景出生点生成
  │  初始化飞球控制器
  ↓
Ready (准备)
  │  等待所有玩家就绪
  │  飞球进入 None 状态
  ↓
Battle (战斗) ← 核心
  │  飞球激活 → Appear → ReadyMove → Move
  │  飞球自动追踪目标玩家
  │  玩家使用技能偏转/格挡飞球
  │  被飞球击中 → HitRole → 玩家淘汰
  │  Buff 系统：冻结（减速）/ 无敌（免疫）/ 隐身（不被追踪）
  │  球速随时间递增（SpeedControl）
  │  判定：仅剩 1 人存活 → RoundOver
  ↓
RoundOver (回合结束)
  │  显示回合胜者
  │  积分更新
  ↓
Wait (等待阶段) ← ★ BladeBall 独有
  │  短暂等待后进入下一回合
  │  复活数据初始化 (RebornRunningData)
  │  判定：达到回合数 → Over，否则 → Born
  ↓
Over (游戏结束)
    最终排名/积分展示
```

### 1.3 飞球状态机（11 个状态）

```
飞球状态机（ServerBladeBallController 管理）：

None (空状态)
  │  初始状态，球体不可见
  ↓
Appear (出现)
  │  球体从指定位置出现
  │  播放出现特效
  ↓
ReadyMove (准备移动)
  │  短暂停顿，选择目标
  │  SpeedControl 计算初始速度
  ↓
Move (移动/追踪)
  │  追踪目标玩家
  │  球速逐渐加速
  │  PropertyControl 计算伤害属性
  │  可被触发：
  │    ├── BeHit → 被格挡/偏转
  │    ├── HitRole → 击中玩家
  │    ├── Confused → 被技能干扰
  │    ├── Control → 被玩家控制
  │    └── BecauseWeak → 减弱状态
  ↓
BeHit (被击打)
  │  玩家成功格挡
  │  飞球改变方向，寻找新目标
  │  → 回到 ReadyMove
  ↓
HitRole (击中玩家)
  │  玩家被淘汰
  │  积分结算
  │  → 回到 ReadyMove（选择新目标）
  ↓
Confused (混乱)
  │  被技能干扰
  │  随机移动一段时间
  │  → 回到 Move
  ↓
Control (被控制)
  │  玩家使用控制技能
  │  飞球按玩家指令移动
  │  控制时间到 → 回到 Move
  ↓
BecauseWeak (减弱)
  │  特殊状态，球体伤害降低
  │  → 回到 Move
```

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOBladeBallModeData` | Resources/AB | Mgr.Init() |
| **扩展配置** | `SOBladeBallModeExtData` | Resources/AB | Mgr.Init() |
| **近战配置** | `SOBladeBallModeMeleeData` | Resources/AB | Battle |
| **飞球 Prefab** | 飞球模型 + 特效 | Addressable | Born |
| **飞球皮肤** | 皮肤资源 | SkinLogic | Born |
| **技能图标** | 技能 UI | UIManager | Battle |

### 1.5 禁止修改的文件

- **ClientCommonManager / ServerCommonManager** — Common 基础框架
- **GameMode.cs** 已有枚举值 `Bladeballmode=24`
- **BattleCommonDynamicData** 基础字段

---

## 二、新建/扩展 Checklist

### Phase 1：新增技能

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `ClientBladeBallSkillLogic.cs` | 修改 | 新增技能表现 |
| 2 | `ClientBladeBallSkillOperate.cs` | 修改 | 新增技能输入处理 |
| 3 | `ServerBladeBallLogic.cs` | 修改 | 新增技能判定逻辑 |
| 4 | 技能配置 | 新建/修改 | 技能参数（冷却/范围/持续时间） |

### Phase 2：扩展飞球控制

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 5 | `ServerBladeBallController.cs` | 修改 | 新增飞球状态 |
| 6 | `ServerBladeBallSpeedControl.cs` | 修改 | 调整球速曲线 |
| 7 | `ServerBladeBallPropertyControl.cs` | 修改 | 调整伤害/属性 |
| 8 | `ClientBladeBallController.cs` | 修改 | 对应客户端表现 |

### Phase 3：扩展 Buff 系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 9 | `ServerBladeBallBuffControl.cs` | 修改 | 新增 Buff 类型 |
| 10 | Buff 表现 | 修改 | 客户端 Buff 特效/UI |

### Phase 4：调整规则

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | `ServerBladeBallRuleLogic.cs` | 修改 | 胜负/淘汰规则 |
| 12 | `ServerBladeBallPointLogic.cs` | 修改 | 积分规则 |
| 13 | `ServerBladeBallRevengeLogic.cs` | 修改 | 复仇触发条件 |

---

## 三、配置文件详解

### 3.1 SOBladeBallModeData（主配置）

| 字段 | 类型 | 说明 |
|------|------|------|
| `initialBallSpeed` | float | 飞球初始速度 |
| `maxBallSpeed` | float | 飞球最大速度 |
| `speedAcceleration` | float | 球速加速率 |
| `ballDamage` | int | 飞球伤害 |
| `roundCount` | int | 总回合数 |
| `battleTime` | float | 回合时长 |
| `rebornTime` | float | Wait 阶段等待时间 |

### 3.2 SOBladeBallModeExtData（扩展配置）

| 字段 | 类型 | 说明 |
|------|------|------|
| `buffDuration_Freeze` | float | 冻结 Buff 持续时间 |
| `buffDuration_Invincible` | float | 无敌 Buff 持续时间 |
| `buffDuration_Invisible` | float | 隐身 Buff 持续时间 |
| `skillCooldown` | float[] | 各技能冷却时间 |
| `meleeRange` | float | 近战格挡范围 |

### 3.3 飞球控制器数据

```csharp
// 服务端飞球控制器
public class ServerBladeBallController {
    public StateMachine<BladeBallState> stateMachine;  // 11 状态
    public Transform target;          // 当前追踪目标
    public float currentSpeed;        // 当前球速
    public Vector3 direction;         // 飞行方向
    
    // 选择目标
    public BattleRoleLogic SelectTarget() {
        // 排除无敌/隐身玩家
        // 选择最近的存活玩家
    }
    
    // 被格挡
    public void OnBlocked(int blockerId) {
        stateMachine.ChangeState(BladeBallState.BeHit);
        target = SelectNewTarget(excludeId: blockerId);
    }
}

// 球速控制
public class ServerBladeBallSpeedControl {
    public float Calculate(float gameTime) {
        // 线性/曲线加速
        return Mathf.Min(initialSpeed + acceleration * gameTime, maxSpeed);
    }
}

// Buff 控制
public class ServerBladeBallBuffControl {
    public void ApplyBuff(int roleId, BuffType type) {
        switch (type) {
            case BuffType.Freeze:    // 冻结 - 减速
            case BuffType.Invincible: // 无敌 - 免疫击中
            case BuffType.Invisible:  // 隐身 - 不被飞球选中
        }
    }
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化（继承 Common）

```csharp
public class ServerBladeBallModeMgr : ServerCommonManager {
    
    public override void Init() {
        base.Init();  // ★ 调用 CommonManager 初始化
        
        data = new ServerBladeBallModeData();
        data.Config = LoadSOConfig<SOBladeBallModeData>();
        data.ExtConfig = LoadSOConfig<SOBladeBallModeExtData>();
        
        // 初始化飞球控制器
        ballController = new ServerBladeBallController();
        ballController.Init(data.Config);
        
        // 注册 Logic
        AddLogic(new ServerBladeBallLogic());
        AddLogic(new ServerBladeBallPointLogic());
        AddLogic(new ServerBladeBallRevengeLogic());
        AddLogic(new ServerBladeBallRuleLogic());
        AddLogic(new ServerBladeBallModeStatisticsLogic());
    }
}
```

### 4.2 飞球追踪与格挡

```csharp
// Battle Stage 中的飞球更新
public override void OnUpdate(float deltaTime) {
    base.OnUpdate(deltaTime);
    
    // 更新球速
    ballController.currentSpeed = speedControl.Calculate(gameTime);
    
    // 飞球移动
    if (ballController.stateMachine.CurrentState == BladeBallState.Move) {
        var target = ballController.target;
        var direction = (target.position - ball.position).normalized;
        ball.position += direction * ballController.currentSpeed * deltaTime;
        
        // 检测击中
        if (Vector3.Distance(ball.position, target.position) < hitRadius) {
            ballController.stateMachine.ChangeState(BladeBallState.HitRole);
            OnRoleHit(target.RoleId);
        }
    }
}

// 玩家格挡（近战操作）
public void OnPlayerBlock(int roleId) {
    if (!IsInBlockRange(roleId, ball.position)) return;
    
    // 格挡成功
    ballController.OnBlocked(roleId);
    
    // 通知客户端播放格挡特效
    SendRpc(new RpcBladeBallBlocked { roleId = roleId });
    
    // 积分奖励
    mgr.GetLogic<ServerBladeBallPointLogic>().AddBlockScore(roleId);
}
```

### 4.3 技能系统

```csharp
// 客户端技能操作
public class ClientBladeBallSkillOperate {
    
    public void OnSkillInput(int skillId) {
        // 检查冷却
        if (IsOnCooldown(skillId)) return;
        
        // 发送技能请求
        SendC2S(new BladeBallC2S {
            type = MsgType.UseSkill,
            skillId = skillId
        });
        
        // 开始冷却
        StartCooldown(skillId);
    }
}

// 服务端技能处理
public void OnSkillRequest(int roleId, int skillId) {
    switch (skillId) {
        case SkillId.Deflect:
            // 偏转 - 改变飞球方向
            ballController.Deflect(roleId);
            break;
        case SkillId.Shield:
            // 护盾 - 短暂无敌
            buffControl.ApplyBuff(roleId, BuffType.Invincible);
            break;
        case SkillId.Vanish:
            // 消失 - 隐身
            buffControl.ApplyBuff(roleId, BuffType.Invisible);
            break;
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 飞球穿墙

**现象**：飞球高速移动时穿过墙壁直接击中墙后的玩家

**根因**：高球速下每帧移动距离超过碰撞体厚度，物理检测遗漏

**解决方案**：
1. 使用 Raycast 代替直接位移，检测路径上的碰撞
2. 限制每帧最大移动距离（或使用子步进）
3. 墙壁碰撞体厚度加大

### 5.2 隐身玩家被飞球追踪

**现象**：使用隐身技能后飞球仍然追踪隐身玩家

**根因**：`SelectTarget()` 未过滤带有 Invisible Buff 的玩家

**解决方案**：
1. SelectTarget() 中添加过滤：
```csharp
var candidates = allRoles.Where(r => r.IsAlive && !buffControl.HasBuff(r.RoleId, BuffType.Invisible));
```
2. 如果当前目标隐身，立即切换目标

### 5.3 Mirror 协议版本不匹配

**现象**：BladeBallC2S 消息发送后服务端收到乱码

**根因**：BladeBallC2SMirror 与 BladeBallC2S 字段不同步，Mirror 网络层序列化不匹配

**解决方案**：
1. 确保 BladeBallC2S 和 BladeBallC2SMirror 字段完全一致
2. 修改消息结构后同时更新两个文件
3. 检查 NetworkMessageId 是否冲突

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `Bladeballmode=24` 无冲突
- [ ] Factory 双端已注册
- [ ] Mirror 协议编译正常

### 6.2 配置

- [ ] SOBladeBallModeData 球速/伤害参数合理
- [ ] SOBladeBallModeExtData Buff 时长合理
- [ ] 近战配置 meleeRange 合理

### 6.3 运行时

- [ ] 6 阶段正常流转
- [ ] 飞球追踪目标正确
- [ ] 格挡改变飞球方向
- [ ] 球速正确加速
- [ ] 3 种 Buff 效果正确（冻结/无敌/隐身）
- [ ] 技能释放/冷却正常
- [ ] 飞球 11 状态切换正确
- [ ] 复仇判定准确

### 6.4 兼容性

- [ ] 不影响 Common 基础框架
- [ ] 不影响其他继承 Common 的模式
- [ ] 飞球皮肤系统正常

依赖知识：[[模式制作]] · [[CommonMode制作]] · [[mode-bladeball]]
