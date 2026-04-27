# 1 代架构 PVE 肉鸽（PveRogue）制作规范

> **适用范围**：PveRogue PVE 肉鸽模式 — 新增怪物类型 / 扩展图腾系统 / 调整掉落商店
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-pverogue（~21 文件 + 大量子系统，★★★ 复杂，含怪物AI/图腾/掉落系统）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientPveRogueMgr (Client 端 PVE 肉鸽主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/ClientPveRogueMgr.cs
  │  继承: ClientModeManager
  │
  ├── ClientPveRogueRoleLogic       — 角色管理
  ├── ClientPveRogueMonsterLogic    — 怪物显示
  ├── ClientPveRogueLootLogic       — 掉落物处理
  ├── ClientPveRogueTerrainLogic    — 地形/场景
  ├── ClientPveRogueTimelineLogic   — 时间轴/事件
  ├── ClientModeInvincibleLogic     — 无敌模式
  │
  ├── 怪物子系统
  │     ClientPveMonster (基类)
  │     ClientPveMonsterDragon (龙 Boss)
  │     ClientPveMonster_Display / _DownHp / _Move
  │     ClientPveMonDownHpEffectMgr
  │
  ├── Stage: Born → Battle → Over
  └── ClientPveRogueData

ServerPveRogueMgr (Server 端 PVE 肉鸽主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/ServerPveRogueMgr.cs
  │  继承: ServerModeManager
  │
  ├── ServerPveRogueStatisticsLogic  — 统计
  ├── ServerPveRogueRoleLogic        — 角色
  ├── ServerPveRogueNsqDataLogic     — NSQ
  ├── ServerPveRogueAwardLogic       — 奖励
  ├── ServerPveRogueMonsterLogic     — 怪物逻辑
  ├── ServerPveRogueGameplayLogic    — 核心玩法 ★
  ├── ServerPveRogueShoppingLogic    — 商店
  ├── ServerPveRogueLootLogic        — 掉落
  ├── ServerPveRogueTerrainLogic     — 地形
  ├── ServerPveRogueTimelineLogic    — 时间轴
  ├── ServerPveRogueTestLogic        — DEBUG 测试
  │
  ├── 怪物子系统
  │     ServerPveMonster (基类)
  │     ServerPveMonster_AIBehavior / _Move / _Skill / _Target
  │
  ├── 掉落子系统
  │     ServerPveDropItemData / ServerPveDropItemMgr / ServerPveDropItemPickMgr
  │
  └── ServerPveRogueData

Host 层定义
    PveRogueDefine.cs (所有枚举和数据结构)
    PveGameStateType: Born(0) → Prepare(1) → Battle(2) → Rest(3) →
                      BeforeBattle(4) → AfterBattle(5) → Result(6) → End(7)
    PveBattleResultType: Playing / GameOver / KeyMonster / TimeEnd
    PveMonsterType: Fighter / Bomber / Shooter / Tank / Dragon
    PveMonsterSubType: Normal / Elite / Boss

图腾系统 ★★
    RoleTotemServer / PveTotemEffect / PveTotemConditionDispatcher
    PveTotemConditionRegister / CustomTotemCheck / CustomTotemTrigger
    23 个图腾 Buff

PVE 专属 Buff（42 个）
    增强: BSPveAddAttr / BSPveAddHp / BSPveShield
    进度: BSPveAddAbilityDuration / BSPveResetSkillCD
    图腾: 23 个图腾效果 Buff
    地牢: 8 个地牢机制 Buff

配置: Assets/ToBundle/ScriptableObject/Mode/PveRogue/ (96+ SO 文件)
```

### 1.2 Stage 阶段流转

```
3 Stage + 8 GameState（内嵌状态机）：

Stage 层：Born → Battle → Over

GameState 流转（在 Battle Stage 内）：
  Prepare (准备)
    │  选择图腾/初始装备
    ↓
  Battle (战斗)
    │  怪物波次攻击
    │  掉落物拾取
    │  图腾效果触发
    │  判定: 击杀关键怪物 / 全灭 / 时间到
    ↓
  Rest (休息)
    │  商店选择奖励
    │  恢复生命值
    ↓
  BeforeBattle → Battle → AfterBattle (循环多波次)
    ↓
  Result (结算) → End (结束)
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOPveRogueConfig` | Resources/AB | Init() |
| **玩法配置** | `SOPveRogueGameplayConfig` | Resources/AB | Init() |
| **怪物资源** | 各怪物 Prefab + AI 配置 | Addressable | Battle |
| **图腾配置** | 23 个图腾 Buff 配置 | Resources/AB | Prepare |
| **掉落物** | 武器/图腾/Buff Prefab | ItemPool | Battle |
| **角色控制器** | `Assets/ToBundle/Role/Controllers/War/PveMode/` | AnimController | Born |

---

## 二、新建/扩展 Checklist

### Phase 1：新增怪物类型

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `PveRogueDefine.cs` | 修改 | 新增 PveMonsterType 枚举 |
| 2 | `ServerPveMonster` 子类 | 新建 | 新怪物服务端逻辑 |
| 3 | `ClientPveMonster` 子类 | 新建 | 新怪物客户端表现 |
| 4 | AI 行为配置 | 新建 | 新怪物 AI 行为树 |
| 5 | SO 配置 | 新建 | 新怪物数值/掉落 |

### Phase 2：扩展图腾系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 6 | 新图腾 Buff | 新建 | 继承 PveTotemEffect |
| 7 | `PveTotemConditionRegister` | 修改 | 注册新条件 |
| 8 | `CustomTotemCheck` | 新建 | 新触发条件 |
| 9 | 图腾 SO 配置 | 新建 | 新图腾数值 |

### Phase 3：扩展掉落/商店

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 10 | `ServerPveRogueLootLogic.cs` | 修改 | 新增掉落规则 |
| 11 | `ServerPveRogueShoppingLogic.cs` | 修改 | 新增商品 |
| 12 | `ServerPveDropItemMgr.cs` | 修改 | 新增掉落物类型 |

---

## 三、配置文件详解

### 3.1 核心配置（96+ SO 文件）

| SO 类型 | 路径 | 关键字段 | 说明 |
|---------|------|---------|------|
| `SOPveRogueConfig` | `UI/War/SO/Mode/PveRogue/` | bornConfigSign, shieldBuff, roleSkillConfigs[], uprearHpValue, autoUprearTime, soDropConfig, gameplayConfigList[], restTime, prepareTime | 主控配置 — 技能/掉落/BGM/波次全局设定 |
| `SOPveRogueGameplayConfig` | 同上 | gameplayType, playTime, endCountdown, earlyCloseCond, keyMonsterType, isPlayEnterAnimation, sceneConfigSign, newSoPveRogueBornConfigs[] | 单局玩法 — 怪物刷新/时间/提前结束条件 |
| `SOPveRogueBornConfig` | 同上 | id, buffSign, bornPoints[], bornInterval, bornRadius, bornTimes[], isGroupBorn, isReborn | 旧版怪物刷新（已被 NewSO 替代） |
| `SOPveRoguePointConfig` | 同上 | points[] (PveRoguePoint), activeTime (Vector2) | 刷新点激活时间范围 |
| `SOPveDropConfig` | 同上 | DropConfigs[] → ItemType/DropMonsterTypes[]/DropRatio/AutoPickInterval/PickSound | 掉落概率表 — 经验/血量/技能掉落 |
| `SOPveCameraTween` | 同上 | position (SOTweenParam), rotation (SOTweenParam) | 战斗镜头动画 |
| `PveMonsterConfig` | `Config/` (txt) | Sign, Hp, Shield, Speed, Exp, Skill1_ID~Skill5_ID, Skill1_InitCD~Skill5_InitCD, Skill1_CD~Skill5_CD, Skill1_Power[]~Skill5_Power[] | 怪物数值 — 每种怪最多5个技能+冷却+威力数组 |
| `PveModeConfig` | `Config/` (txt) | 难度键 = `{PveModeType}_{PveDiffLevel}` | 难度缩放 — HP倍率/经验比/波次参数 |
| `PveShopConfig` | `Config/` (txt) | round, refreshCost, ItemCnt, hasHeal, healName | 关间商店 — 刷新费用/物品数/治疗选项 |
| `PveItemOutputConfig` | `Config/` (txt) | weight_0~weight_9 (10个权重列) | 商品概率 — 武器/图腾按权重随机选取 |

### 3.2 核心枚举

```csharp
// 怪物类型（7种）
public enum PveMonsterType {
    Fighter = 0,   // 战士（近战）
    Bomber,        // 投弹手（手雷）
    Shooter,       // 射手（远程）
    Tank,          // 肉盾（高HP）
    Dragon,        // 呆呆龙Boss
    Exploder,      // 自爆怪
    Bubbles        // 泡泡怪
}
public enum PveMonsterSubType { Normal, Elite, Boss }

// 怪物签名（12种实体）
public enum PveMonsterSign {
    PveMonster_Fighter, PveMonster_Bomber, PveMonster_Shooter, PveMonster_Tank,
    PveMonster_BubbleShooter, PveMonster_ExplodeBall,
    PveEliteMonster_Fighter, PveEliteMonster_Bomber, PveEliteMonster_Shooter,
    PveEliteMonster_Tank, PveEliteMonster_BubbleShooter,
    PveBossMonster_Dragon
}

// 游戏阶段（8种）
public enum PveGameStateType {
    Born = 0, Prepare, Battle, Rest, BeforeBattle, AfterBattle, Result, End
}

// 掉落物类型
public enum PveDropItemType { Exp, Hp, Skill }

// 提前结束条件
public enum PveGameplayEarlyCloseCondType { None, KeyMonsterDie }
```

### 3.3 图腾效果类型（23+ 类别）

```csharp
// 角色属性（1-100）
HpMax, ShieldMax, MoveSpeed, DamageToAllType, SkillDuration ...

// 武器属性（101-200）
WeaponDamage, FireDeployTime, MagazineCapacity, SteelBulletDamage ...

// 特殊属性（201-300）
DashDistance, RunHitWeak, BombRange, ShootNoCostBullet, ImmuneAnyHarm ...

// 对怪伤害（301-400）
DamageToMonsterFighter, DamageToMonsterBomber, DamageToMonsterBoss ...

// 经验获取（401-450）
KillMonsterDropExtraExpProbability, ExpFromPickItem
```

**图腾触发器（25+ 种）**：Jump, DownHp, DashFinish, MonsterDownHp, Weak, HitPartAttackOnce, BulletHitEnd, KillMonster, KillEliteMonster, ShootOnce, Reloading, PickExp, SecondJump, DashStart, ShieldBroken 等

**图腾叠加规则**：
- 键值 = `(effectType << 16) + buffId`，按键存入 `Dictionary<int, List<PveTotemEffect>>`
- 计算顺序：Base → Percent → LastMultiplier（`TotemAddValueType` 枚举）
- 上限保护：`HpMaxLimit`, `ShieldMaxLimit`, `ShieldHitStopTime`

### 3.4 掉落配置详解

```csharp
// SOPveDropConfig.DropConfig 结构
public class DropConfig {
    public PveDropItemType ItemType;              // 掉落类型（Exp/Hp/Skill）
    public List<PveMonsterSubType> DropMonsterTypes;  // 哪些怪掉落
    public float DropRatio;                       // 掉落概率 0~1
    public bool IsReceiveOnRoundEnd;              // 回合结束自动拾取
    public float AutoClearTime;                   // 消失时间（0=不消失）
    public float ItemDropDistance;                // 拾取范围（默认 2f）
    public AnimationCurve PickCurveData;          // 抛物线轨迹
    public Vector3 CreatePosOffset;               // 相对怪物偏移
    public string PickSound;                      // 拾取音效
}
```

---

## 四、关键代码修改点

### 4.1 怪物系统（7 类型 × 3 子类型）

**怪物 AI 行为核心路径**：`GamePlay/Server/Modules/Mode/PveRogue/Logic/`

```csharp
// 怪物技能配置读取（每怪最多 5 个技能）
// PveMonsterConfig.txt 字段
Sign | Hp | Shield | Speed | Exp
| Skill1_ID | Skill1_InitCD | Skill1_CD | Skill1_Power[]
| Skill2_ID | Skill2_InitCD | Skill2_CD | Skill2_Power[]
| ... (最多 Skill5)
```

**7 种怪物行为特征**：

| 怪物类型 | Sign | 行为 | 技能特点 |
|---------|------|------|---------|
| Fighter | `PveMonster_Fighter` | 近战冲锋 | 近距攻击+冲撞 |
| Bomber | `PveMonster_Bomber` | 投掷手雷 | 范围AOE+弧线弹道 |
| Shooter | `PveMonster_Shooter` | 远程射击 | 保持距离+精准射击 |
| Tank | `PveMonster_Tank` | 高血量前排 | 护盾+嘲讽 |
| Dragon | `PveBossMonster_Dragon` | Boss阶段 | 多阶段技能+全屏攻击 |
| Exploder | `PveMonster_ExplodeBall` | 自爆冲撞 | 接近后引爆+范围伤害 |
| Bubbles | `PveMonster_BubbleShooter` | 泡泡射击 | 减速debuff+连射 |

**精英/Boss 子类型**：
- Normal（普通）→ Elite（精英：HP/伤害倍率提升）→ Boss（Boss：独立行为树+多阶段）
- 精英怪 Sign 前缀 `PveEliteMonster_`，Boss 前缀 `PveBossMonster_`

### 4.2 图腾系统（23 个 Buff SO）

**核心架构**：`BSOTotemAdd*.cs`（23 个 ScriptableObject 子类）

```csharp
// 图腾 Buff 基类
public class BSOPveTotemBuff : ScriptableObject {
    public PveTotemEffectType effectType;     // 效果类型枚举
    public PveTotemTriggerType triggerType;   // 触发条件
    public float[] values;                    // 数值参数
    public float duration;                    // 持续时间
    public int maxStack;                      // 最大叠加层数
}
```

**23 个图腾 Buff SO 实例**：

| Buff SO | 效果 | 触发器 |
|---------|------|--------|
| BSOTotemAddAttr | 永久属性提升 | 无（选择即生效） |
| BSOTotemAddComeOn | 加油buff（移速+攻速） | 击杀怪物时 |
| BSOTotemAddGrievedPotion | 苦药buff（受伤回血） | DownHp（血量低于阈值） |
| BSOTotemAddHotMuzzle | 火热枪口（射击加成） | ShootOnce（每次射击） |
| BSOTotemAddIronEgg | 铁蛋buff（护盾增强） | ShieldBroken |
| BSOTotemAddGearUp | 整装待发（换弹强化） | Reloading |
| BSOTotemAddAngryRoar | 怒吼buff（范围减益） | DownHp |
| BSOTotemAddIronHead | 铁头buff（爆头伤害+1） | HitPartAttackOnce（爆头时） |
| BSOTotemAddPoisonBullet | 毒弹（持续伤害） | BulletHitEnd |
| BSOTotemAddSteelBullet | 钢弹（穿透伤害） | ShootOnce |
| BSOTotemAddBombardment | 轰炸（范围伤害） | KillMonster |
| BSOTotemAddBloodDrink | 吸血（击杀回血） | KillMonster |
| 其他 11 个 | 详见 `SO/Mode/PveRogue/` | 各类触发器 |

**叠加计算公式**：

```csharp
// 键值 = (effectType << 16) + buffId → 同类型同ID叠加
Dictionary<int, List<PveTotemEffect>> totemEffects;

// 计算顺序
float baseValue = originalStat;
float result = baseValue;
result += sumOf(Base类加值);           // 1. 固定加值
result *= (1 + sumOf(Percent类));      // 2. 百分比加成
result *= lastMultiplier;              // 3. 最终倍率（仅取最后一个）
```

### 4.3 房间推进与难度缩放

**阶段流转**（每回合 3 阶段）：

```
BornStage → BattleStage → OverStage
   ↓            ↓            ↓
  刷怪准备     战斗倒计时    结算/商店

// 8 个 GameState 细分
Born → Prepare → BeforeBattle → Battle → AfterBattle → Rest → Result → End
```

**难度缩放公式**：
- 经验比：`ExpRoundRatio`（每回合递增，鼓励后期图腾选取）
- 怪物属性按 `PveDiffLevel` 缩放（1~5 难度等级）
- Boss 每 N 回合出现一次，属性按回合数线性增长

### 4.4 商店系统

```csharp
// PveShopConfig.txt — 回合间商店
Round | RefreshCost | ItemCnt | HasHeal | HealName
  1   |     100     |    3    |  true   | "Heal_Small"
  2   |     150     |    4    |  true   | "Heal_Medium"
  ...

// PveItemOutputConfig.txt — 10 权重列选品
// weight_0 ~ weight_9: 每列一个物品池，按权重随机
// 商品 = 武器 + 图腾，同一商品不重复出现
```

### 4.5 掉落与拾取

```csharp
// 掉落生成（击杀时）
public void OnMonsterDead(ServerPveMonster monster) {
    foreach (var dropConfig in soDropConfig.DropConfigs) {
        // 检查怪物子类型是否在掉落列表中
        if (!dropConfig.DropMonsterTypes.Contains(monster.SubType)) continue;
        // 概率判定
        if (Random.value > dropConfig.DropRatio) continue;
        // 创建掉落物（带抛物线轨迹）
        var dropItem = CreateDropItem(
            dropConfig.ItemType,
            monster.Position + dropConfig.CreatePosOffset,
            dropConfig.PickCurveData  // AnimationCurve 控制弧线
        );
        dropItem.AutoClearTime = dropConfig.AutoClearTime;
        dropItem.PickDistance = dropConfig.ItemDropDistance;
    }
}

// 3 种掉落物类型
// Exp  — 经验球（蓝色），直接增加角色经验
// Hp   — 血包（红色），恢复生命值
// Skill — 技能球（金色），充能大招
```

### 4.6 PVE 专属 Buff 系统（43 种）

| 分类 | 数量 | 示例 |
|------|------|------|
| 玩家角色 Buff | 9 | 移速加成、伤害加成、护盾恢复、无敌、吸血 |
| 怪物技能 Buff | 24 | 减速、冰冻、眩晕、击退、灼烧、中毒、标记 |
| 图腾专属 Buff | 10 | 钢弹穿透、毒弹DoT、爆头加成、换弹加速 |

**Buff 生命周期**：创建 → Apply → Tick(duration) → Remove
- 与主 Buff 系统共用 `MyBuffControl`
- 通过 `PlayBuff(buffSign, roleId)` 统一接口

---

## 五、常见问题与踩坑记录

### 5.1 怪物 AI 行为树在高波次卡顿

**现象**：后期高波次怪物数量多时 AI 行为树 Tick 导致帧率下降

**根因**：每帧每个怪物都执行完整行为树，高数量时 O(n) 开销大

**解决方案**：
1. AI Tick 分帧执行（每帧只更新一部分怪物）
2. 简单怪物使用状态机替代行为树
3. 远离玩家的怪物降低 Tick 频率

### 5.2 图腾 Buff 叠加导致数值溢出

**现象**：多个增伤图腾叠加后伤害值异常巨大

**根因**：图腾 Buff 之间是乘法叠加而非加法

**解决方案**：
1. 设置最大增伤上限（如 500%）
2. 使用加法叠加或设计衰减公式
3. 在 PveTotemEffect 基类中添加上限检查

### 5.3 掉落物过多导致性能问题

**现象**：Boss 战后大量掉落物导致客户端卡顿

**根因**：每个掉落物都是独立 GameObject，未使用对象池

**解决方案**：
1. `ServerPveDropItemMgr` 使用对象池
2. 设置场景最大掉落物数量
3. 掉落物超时自动消失

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] PveRogueDefine 枚举正确

### 6.2 运行时

- [ ] 8 个 GameState 正常流转
- [ ] 怪物生成/AI/死亡正常
- [ ] 图腾条件触发正确
- [ ] 掉落物拾取/商店购买正常
- [ ] Boss 战正常
- [ ] 时间轴事件正确触发

### 6.3 兼容性

- [ ] 42 个 PVE Buff 不影响其他模式 Buff
- [ ] 掉落系统不影响通用 ItemPool

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-pverogue]]
