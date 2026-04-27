# UGC GPO 内容边界定义

> **版本**：v0.5（覆盖全部 16 种 GPO 类型，扩展模板库至5大类14个UGC可用模板，完善意图识别映射表）
> **定位**：本文档定义了 UGC 玩家通过 AI 聊天创建/修改 GPO（GamePlayObject）时，AI 所能操作的内容范围、参数边界与合法性验证规则。
> **使用对象**：负责处理 UGC 请求的 AI Agent。玩家不直接阅读本文档。

---

## 目录

1. [总则](#1-总则)
2. [UGC 可用 GPO 模板库](#2-ugc-可用-gpo-模板库)
3. [属性参数规范](#3-属性参数规范)
4. [行为预设包](#4-行为预设包)
5. [AI 意图识别增强规则](#5-ai-意图识别增强规则)
6. [意图理解规范](#6-意图理解规范)
7. [AI 处理流程](#7-ai-处理流程)
8. [附录：Component 代码模板](#8-附录component-代码模板)
9. [待确认项（需策划确认）](#9-待确认项需策划确认)

---

## 1. 总则

### 1.1 AI 可以做什么

UGC 玩家通过 AI 聊天，可以创建或修改 **GPO（游戏可玩对象）**，具体包括：

| 操作类型 | 说明 | 示例 | 需修改的文件 |
|---------|------|------|------------|
| **调参** | 修改现有 GPO 模板的属性数值 | "把坦克血量改成 5000" | 仅 `GPOM_{Type}.cs` 配置 |
| **换行为** | 为现有 GPO 模板添加定制 Component | "让炮台会在低血时隐身" | 新增 `ServerAI{Type}Custom{Behavior}.cs` + System OnAwake |
| **基于模板创建新 GPO** | 在现有类型下新增一条 GPOM 数据（不新建类型） | "创建一个叫'寒冰炮台'的新炮台" | 新增 GPOM 数据行 + 可选定制 Component |
| **自动生成模板数据** | 缺少模板数据时，AI 可自行根据需求生成 | "创建全新数值的坦克怪" | 参照同类型已有数据行，AI 自动生成并注释"待策划校验" |
| **组件内嵌入常量参数** | 无法从模板读取某参数时，直接在 Component 里用常量 | 某 GPOM 没有对应字段 | 在 Component 内定义 `private const float xxx = N;` |

**唯一限制：** 不修改框架层/底层代码（Base类、Manager类、World类、Switch分发类）。此规则已在`core-rules.md`明确，本文档不重复约束。

**工程上已支持的特殊能力（可在任意模板的 Component 里使用）：**

| 能力 | 工程机制 | 实现文件 |
|------|---------|---------|
| **临时隐身/出现** | `HideEntity` Tag + `SE_Entity.Event_IsShowEntity` | `ServerGPOShowEntity.cs` |
| **死亡不消失（复活）** | `SE_AI.Event_DisabledDeadToRemove` + 重置 HP 逻辑 | `ServerAIDead.cs` |
| **无敌** | `GodMode` Tag | T-SceneGPO 天然支持；其他类型也可通过 Tag 实现 |
| **计时消亡** | `ServerSummonedAILifeTime` + `LifeDuration` 字段 | 已有组件 |
| **多阶段（TimeLine）** | 定制 TimeLine Component 监听 HP/时间阈值，事件通知 | 详见第4章 B09 |
| **召唤其他 GPO** | `SM_AI.Event_AddAI` 消息 | 详见第8章 8.2 |

---

### 1.2 GPO 数据三层结构

每个 GPO 的数据由三部分构成，AI 需要理解各层的职责和使用方式：

| 数据层 | 类型 | 来源/位置 | 包含内容 | AI 如何使用 |
|--------|------|---------|---------|------------|
| **MData** | `IGPOM` | `Assets/Scripts/Template/gpo/GPOM_XXXSet.cs` | 静态属性（HP、ATK、Speed、Sign 等）| 生成/修改数据行；System 内通过 `MData.GetXxx()` 读取 |
| **InData** | `IGPOInData` | 运行时调用方传入 | 出生点位置、队伍ID 等 | 通常不需要修改，系统自动处理 |
| **SoData** | `ScriptableObject` | `Assets/Bundle/Configs/AI/*.asset` | 扩展配置（波次组、复杂行为参数）| 仅 GPOSpawner 等特定类型需要生成；System 内通过 `SoData` 属性访问 |

**注意：** 如果 MData 中没有所需字段，AI 可以直接在 Component 里写常量（而不是强行往 GPOM 加字段）：
```csharp
// 示例：GPOM 没有"隐身触发 HP 百分比"字段时，直接在 Component 里用常量
private const float HIDE_HP_THRESHOLD = 0.3f; // 血量低于 30% 触发隐身
```

**SoData 使用情况（当前）：**
- **T-GPOSpawner（刷怪器）**：必须有对应的 `.asset` 文件，定义 WaveGroups（波次组）
  - 文件位置：`Assets/Bundle/Configs/AI/GpoSpawner/`
  - 文件名通过 GPOM 的 `GpoSoConfig` 字段关联
- **其他类型**：`GpoSoConfig` 字段存在但均为空，不需要 SO 配置

**GPOSpawner SO 配置结构（示例）：**
```yaml
WaveGroups:
- GroupSign: Wave1
  WaveInfos:
  - AISign: GoldenEgg      # 要生成的 GPO Sign
    SpawnCount: 16          # 数量
    DelayTime: 0            # 延迟（秒）
  MinRange: 0
  MaxRange: 200             # 刷新半径（米）
  NeedPrevSpawnGPOAllDead: 0  # 1=前一波全死后才刷下一波
  DelaySpawnTime: 0         # 本波延迟（秒）
```

> **UGC 生成 GPOSpawner 时**：同时生成 GPOM 数据行 + SO 波次配置文件。SO 文件结构固定，AI 可根据玩家描述自动生成（如"每40秒刷16个金蛋，分3波"）。

---

## 2. UGC 可用 GPO 模板库

> 数据来源：`GpoTypeSet.cs` + `ServerAIWorld_Switch.cs` + `ClientAIWorld_Switch.cs`，共 16 种已实现 GPO 类型。
> 按使用场景分为 5 个大类，覆盖全部 UGC 创作场景。

### 2.1 分类总览

#### 🔴 A类：地面主动战斗型（4种）

| 模板ID | 名称 | GpoTypeSet | 核心攻击组件 | 特点 | 状态 |
|--------|------|-----------|------------|------|------|
| `T-Tank` | 坦克 | `Id_Tank=1` | `ServerAITankAttack` | 通用地面战斗，行为树驱动 | 🟢 稳定 |
| `T-FeiYu` | 飞鱼 | `Id_FeiYu=2` | `AIFocusGunAttack` | 聚焦枪攻击，轻量型 | 🟢 稳定 |
| `T-WuGui` | 乌龟 | `Id_WuGui=3` | `AIRPGAttack` | RPG/远程弹药攻击，重甲型 | 🟢 稳定 |
| `T-SwordTiger` | 剑齿虎 | `Id_SwordTiger=5` | `AISwordTigerAttack` | 近战高速，可驾驶载具 | 🟢 稳定 |

**共同 GPOM 字段：** `Hp` `Atk` `AttackIntervalTime` `AttackRange` `MaxAttackDistance` `MoveSpeed` `RotaSpeed` `Quality` `AiBehavior` `PetBehavior`

---

#### 🟠 B类：空中飞行战斗型（2种）

| 模板ID | 名称 | GpoTypeSet | 核心特点                                       | 状态 |
|--------|------|-----------|--------------------------------------------|------|
| `T-Helicopter` | 直升机 | `Id_Helicopter=6` | 可被玩家驾驶，飞行+攻击，`MaxFlyHeight`控制高度            | 🟢 稳定 |
| `T-UAV` | 无人机 | `Id_Uav=7` | 全自动飞行，悬浮跟随物体，追踪导弹攻击，支持 `LifeDuration` 计时消亡 | 🟢 稳定 |

**GPOM 特有字段：**
- Helicopter：`MaxFlyHeight` `HeightAdjustSpeed`（可驾驶）
- UAV：`MaxFlyHeight` `HeightAdjustSpeed` `LifeDuration`

---

#### 🟡 C类：固定炮台型（3种）

| 模板ID | 名称 | GpoTypeSet | 特点 | 状态 |
|--------|------|-----------|------|------|
| `T-MachineGun` | 重型防御机枪 | `Id_MachineGun=8` | 高频连射，可被玩家驾驶，无自主移动 | 🟢 稳定 |
| `T-Turret` | 轻型炮台（召唤） | `Id_Turret=13` | 玩家技能召唤，HP继承召唤者 | 🟢 稳定 |
| `T-MissileBattery` | 导弹炮台（召唤） | `Id_MissileBattery=14` | 追踪导弹，`LifeDuration`计时消失，`MaxTargetNum`多目标 | 🟢 稳定 |

**GPOM 特有字段：**
- MachineGun：`MaxAttackDistance`（超远射程）
- Turret/MissileBattery：`GpoHpInheritRatio` `GpoAtkInheritRatio` `BulletType` `MaxTargetNum` `LifeDuration`

---

#### 🔵 D类：BOSS 型（1种）

| 模板ID | 名称 | GpoTypeSet | 特点 | 状态 |
|--------|------|-----------|------|------|
| `T-RexKing` | 霸王龙 | `Id_RexKing=4` | 专属动画+多技能攻击，高血高攻，BOSS等级 | 🟢 稳定 |

---

#### 🟢 E类：场景/特殊型（6种）

| 模板ID | 名称 | GpoTypeSet | 特点 | 状态 |
|--------|------|-----------|------|------|
| `T-SceneGPO` | 场景物件 | `Id_SceneGpo=17` | 自带 GodMode（无敌），场景交互 | 🟢 稳定 |
| `T-GoldenEgg` | 金蛋 | `Id_GoldenEgg=10` | 只有 HP，无攻击/移动，用于抢夺/保护类玩法 | 🟢 稳定 |
| `T-GPOSpawner` | GPO 生成器 | `Id_Gpospawner=12` | 生成其他 GPO，`TargetGpoId`指定生成目标 | 🟢 稳定 |
| `T-Shield` | 护盾 | `Id_Shield=22` | 跟随召唤者，`ScaleSize`控制大小，`LifeDuration`计时 | 🟢 稳定 |
| `T-Character` | 角色AI | `Id_Character=9` | 全功能人形AI，40+组件，**仅限 PGC/高级 UGC** | 🔐 PGC专用 |
| `T-Dummy` | 假人 | `Id_Dummy=11` | 训练靶，无战斗AI，用于测试，**非战斗用途** | 🔬 非战斗 |

> **状态说明：** 🟢 稳定 = UGC 可直接使用；🔐 PGC专用 = 需要高级权限，UGC 不应自行生成；🔬 非战斗 = 特殊用途，不用于战斗 GPO 设计。

### 2.2 UGC 使用建议

| 使用场景 | 推荐模板 |
|---------|---------|
| 创建追击攻击玩家的怪物 | T-Tank / T-FeiYu / T-WuGui / T-SwordTiger |
| 创建飞行单位 | T-UAV（自动）/ T-Helicopter（可驾驶）|
| 创建固定防御炮台 | T-MachineGun（地图固定）|
| 创建玩家召唤的炮台 | T-Turret / T-MissileBattery |
| 创建 BOSS | T-RexKing |
| 创建无法被攻击的装饰/机关 | T-SceneGPO |
| 创建需要争夺/保护的目标物 | T-GoldenEgg |
| 创建刷怪系统 | T-GPOSpawner |
| 创建护盾类召唤物 | T-Shield |

---

## 3. 属性参数规范

### 3.1 各模板允许的属性范围

> ⚠️ **AI 必须将玩家描述的数值裁剪到以下范围内**，超出范围不报错，但自动调整并告知玩家。
> 数据来源：GPOM_*.cs 字段定义 + 范例文档默认值推算。

#### A类 地面战斗型：T-Tank / T-FeiYu / T-WuGui（字段来自 GPOM_Tank/GPOM_FeiYu/GPOM_WuGui）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| 血量 | `Hp` | 100 | 30000 | 3000 | 生命值 |
| 攻击力 | `Atk` | 10 | 500 | 100 |  |
| 攻击间隔 | `AttackIntervalTime` | 0.3 | 5.0 | 1.5 | 秒，越小越快 |
| 攻击范围 | `AttackRange` | 1.0 | 30.0 | 8.0 | 米 |
| 移动速度 | `MoveSpeed` | 0.5 | 12.0 | 4.0 | 米/秒 |
| 旋转速度 | `RotaSpeed` | 30 | 360 | 120 | 度/秒 |
| 最大射程 | `MaxAttackDistance` | 5.0 | 80.0 | 30.0 | 米 |
| 品质 | `Quality` | 1(Normal) | 3(Elite) | 1 | 不允许直接设为 4(Boss) |

#### A类 近战高速型：T-SwordTiger（字段来自 GPOM_SwordTiger）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 |
|------|-------|-------|-------|-------|
| 血量 | `Hp` | 200 | 20000 | 2000 |
| 攻击力 | `Atk` | 20 | 600 | 150 |
| 移动速度 | `MoveSpeed` | 2.0 | 18.0 | 8.0 |
| 旋转速度 | `RotaSpeed` | 60 | 720 | 200 |

#### B类 飞行战斗型：T-UAV（字段来自 GPOM_Uav）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| 血量 | `Hp` | 200 | 15000 | 2000 | 飞行单位通常更脆 |
| 攻击力 | `Atk` | 10 | 300 | 80 |  |
| 移动速度 | `MoveSpeed` | 2.0 | 20.0 | 8.0 | 飞行速度可以更快 |
| 飞行高度 | `MaxFlyHeight` | 3.0 | 30.0 | 8.0 | 最大飞行高度（米） |
| 高度调整速度 | `HeightAdjustSpeed` | 0.5 | 5.0 | 1.0 | 升降速度 |
| 最大射程 | `MaxAttackDistance` | 5.0 | 60.0 | 25.0 |  |
| 存活时长 | `LifeDuration` | 0（永久）| 300 | 0 | 秒，0=不限时 |

#### B类 飞行可驾驶型：T-Helicopter（字段来自 GPOM_Helicopter）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 |
|------|-------|-------|-------|-------|
| 血量 | `Hp` | 500 | 20000 | 5000 |
| 攻击力 | `Atk` | 20 | 400 | 120 |
| 飞行高度 | `MaxFlyHeight` | 5.0 | 50.0 | 15.0 |
| 高度调整速度 | `HeightAdjustSpeed` | 0.5 | 5.0 | 1.5 |

#### C类 固定炮台型：T-MachineGun（字段来自 GPOM_MachineGun）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| 血量 | `Hp` | 500 | 50000 | 8000 |  |
| 攻击力 | `Atk` | 10 | 800 | 200 |  |
| 攻击间隔 | `AttackIntervalTime` | 0.05 | 3.0 | 0.5 | 机枪型可以很短 |
| 最大射程 | `MaxAttackDistance` | 10.0 | 150.0 | 100.0 | 炮台射程更远 |
| 攻击范围 | `AttackRange` | 5.0 | 80.0 | 20.0 |  |

> 注意：GPOM_MachineGun 无 MoveSpeed / AiBehavior 字段，固定炮台不可设置移动速度。

#### C类 召唤炮台型：T-Turret / T-MissileBattery（字段来自 GPOM_Turret/GPOM_MissileBattery）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| HP继承比 | `GpoHpInheritRatio` | 0.1 | 2.0 | 1.0 | 召唤者HP×比例 |
| ATK继承比 | `GpoAtkInheritRatio` | 0.1 | 2.0 | 1.0 | 召唤者ATK×比例 |
| 最大目标数 | `MaxTargetNum` | 1 | 8 | 1 | 同时攻击目标数 |
| 存活时长 | `LifeDuration` | 5 | 120 | 30 | 秒，0=永久（慎用）|

#### D类 BOSS 型：T-RexKing（字段来自 GPOM_RexKing）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| 血量 | `Hp` | 5000 | 200000 | 50000 | BOSS 必须有高血量 |
| 攻击力 | `Atk` | 100 | 2000 | 500 |  |
| 移动速度 | `MoveSpeed` | 1.0 | 8.0 | 3.0 | BOSS 通常慢一些 |
| 旋转速度 | `RotaSpeed` | 30 | 180 | 90 |  |
| 品质 | `Quality` | 4(Boss) | 4(Boss) | 4 | BOSS 固定品质 4 |

#### E类 特殊型：T-GoldenEgg（字段来自 GPOM_GoldenEgg）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| 血量 | `Hp` | 100 | 100000 | 5000 | 唯一可调字段 |

> 注意：GoldenEgg **无** Atk / MoveSpeed / AiBehavior 字段，只能被攻击，不会主动反击。

#### E类 护盾型：T-Shield（字段来自 GPOM_Shield）

| 属性 | 字段名 | 最小值 | 最大值 | 默认值 | 描述 |
|------|-------|-------|-------|-------|------|
| HP继承比 | `GpoHpInheritRatio` | 0.1 | 3.0 | 1.0 |  |
| 护盾尺寸 | `ScaleSize` | 0.5 | 5.0 | 1.0 | 缩放倍率 |
| 存活时长 | `LifeDuration` | 3 | 60 | 10 | 秒 |

### 3.2 品质等级与属性乘数

玩家可以用"普通/精英/BOSS"来描述品质，AI 根据品质对默认值进行乘数调整：

| 玩家描述 | AIQuality | HP 乘数 | ATK 乘数 | 说明 |
|---------|-----------|---------|---------|------|
| 普通/小怪 | `Normal = 1` | ×1.0 | ×1.0 | 默认值 |
| 精英/强力 | `Senior = 2` | ×2.5 | ×1.8 | 中等难度 |
| 王者/首领 | `Elite = 3` | ×5.0 | ×3.0 | 高难度 |
| Boss/最强 | `Boss = 4` | ×15.0 | ×6.0 | 使用 T-RexKing 模板 |

---

## 4. 行为预设包

> 玩家不需要知道行为树节点或 Component 细节，只需要描述"想要什么行为"，AI 根据以下预设包匹配并组合。
>
> ### ⚠️ 行为树修改强制规则（不可绕过）
>
> **AI 永远不得直接编辑 BehaviorDesigner 的 `.asset` 文件或 `.txt` 行为树 JSON 文件。**
>
> 当 UGC 需要新的行为逻辑时，AI 必须：
> 1. **生成一个 GPO 专属 C# Component 文件**（命名规范见 V09）实现该行为逻辑
> 2. **在对应 System 的 `OnAwake` 中 `AddComponent<新组件>()`** 挂载
> 3. **附带一段注释说明**：若将此行为迁移到正式行为树，对应的节点结构是什么（供程序参考）
>
> **原因：** 行为树 JSON 结构复杂，字段映射容易出错，且修改后需要人工验收才能上正式环境。Component 代码有编译检查，更可靠。
>
> **正式迁移注释示例（AI 生成 Component 时必须附带）：**
> ```csharp
> // [行为树迁移说明] 本 Component 实现的逻辑，如需迁移到 BehaviorDesigner 行为树：
> // 结构：Sequence
> //   ├── Condition: ConditionHpThreshold（HP < 30%）
> //   └── Action: ActionAwayFromTargetGpoGroup（远离仇恨目标）
> // 迁移后可删除本 Component，由行为树统一管理。
> ```

### 4.1 预设包总览

| 预设ID | 行为名称 | 玩家描述关键词 | 实现方式 |
|--------|---------|-------------|---------|
| `B01` | 警戒巡逻 | 巡逻、守卫、来回走、看守 | `ServerAIBehaviour`（行为树）+ `ServerAIPatrolPoint` |
| `B02` | 发现追击攻击 | 追人、攻击、见人就打、主动出击 | `ServerAIBehaviour`（行为树）+ 对应 Attack 组件 |
| `B03` | 固守阵地攻击 | 不追人、原地攻击、防守、守卫 | `ServerAIFindInsightTarget` + 对应 Attack 组件（无移动） |
| `B04` | 低血逃跑 | 血量低逃跑、胆小、逃跑 | 定制 Component：监听 HP 事件，低于阈值触发远离行为 |
| `B05` | 召唤援军 | 叫救兵、召唤小弟、增援 | `ServerGPOSkillCallAI` + GPOSpawner 配置 |
| `B06` | 定时触发 | 周期攻击、定时爆炸、计时 | 定制 Component：使用 `ConditionIsTimeLimit` 节点或定时器 |
| `B07` | 存活计时 | 消失、限时、倒计时消亡 | `ServerSummonedAILifeTime`（已有组件）+ `LifeDuration` 字段 |
| `B08` | 被攻击反击 | 被打才打人、反击、防御反击 | 定制 Component：监听 `ServerAIHurt` 事件后发动攻击 |
| `B09` | 多阶段（BOSS专用）| 多阶段、变身、阶段切换、越打越强 | 定制 TimeLine Component（`ServerAI{Type}TimeLine.cs`）监听 HP 阈值，通过事件通知其他组件切换攻击/移动/动画；完全不依赖行为树 |

### 4.2 预设包组合规则

- **最多组合 3 个预设包**（避免行为树过于复杂且不可预测）
- **必须包含至少 1 个攻击相关预设**（除 T05 场景交互型外）
- **以下预设包互斥**，不能同时选择：

| 互斥组 | 原因 |
|--------|------|
| `B02（追击）` + `B03（固守）` | 行为逻辑矛盾 |
| `B04（逃跑）` + `B07（狂暴）` | 低血时行为冲突 |

### 4.3 各模板支持的预设包

| 模板 | 支持的预设包 | 不支持 |
|------|------------|--------|
| T-Tank / T-FeiYu / T-WuGui | B01 B02 B03 B04 B05 B06 B08 | — |
| T-SwordTiger | B02 B04 B05 B06 B08 | B01 B03（高速近战，不擅长固守）|
| T-Helicopter | B01 B02 B06 | B03 B04 B05（可驾驶，AI 行为受限）|
| T-UAV | B01 B02 B03 B04 B06 B07 B08 | B05 |
| T-MachineGun | B03 B06 B08 | B01 B02 B04 B05（固定，不能移动）|
| T-Turret / T-MissileBattery | B03 B07 B08 | B01 B02 B04 B05（固定，召唤物）|
| T-RexKing | B02 B03 B05 B06 B08 **B09** | B01 B04（BOSS 不逃跑）|
| T-SceneGPO | B06 B08 | B01 B02 B03 B04 B05 B07 |
| T-GoldenEgg | B06 B08 | B01 B02 B03 B04 B05（无攻击/移动）|
| T-GPOSpawner | B06 B07 | B01 B02 B03 B04 B05 B08（元GPO，只负责生成）|
| T-Shield | B07 | B01 B02 B03 B04 B05 B06 B08（护盾无攻击逻辑）|

### 4.4 预设包参数边界参考

> 使用预设包时，以下关键参数的合理范围。超出极限值会影响服务器性能或游戏体验，AI 应主动提示。

| 预设 | 关键参数 | 推荐范围 | 极限值 | 注意事项 |
|------|---------|---------|-------|---------|
| **B01** 警戒巡逻 | 巡逻半径 | 5 ~ 30 m | 100 m | 过大时 AI 可能脱离战斗区域 |
| **B01** 警戒巡逻 | 巡逻间隔 | 1 ~ 10 s | 0.1 s | 间隔过短会导致 AI 频繁转向 |
| **B02** 发现追击 | 感知范围 `DetectRange` | 10 ~ 60 m | 200 m | 过大时地图所有 AI 同时激活 |
| **B04** 低血逃跑 | 触发 HP 百分比 | 10% ~ 40% | 5%（下限）/ 60%（上限）| 低于 5% 几乎不会触发；高于 60% 等于大部分时间都在逃 |
| **B04** 低血逃跑 | 逃离距离 | 10 ~ 40 m | 100 m | 过远时 AI 会跑出地图边界 |
| **B05** 召唤援军 | 单次召唤数量 | 1 ~ 5 | 20 | 超过 20 会造成同屏单位过多，帧率下降 |
| **B05** 召唤援军 | 召唤冷却时间 | 10 ~ 60 s | 3 s（最短）| 低于 3s 会快速刷满地图 |
| **B06** 定时触发 | 触发间隔 | 2 ~ 30 s | 0.5 s（最短）| 低于 0.5s 会对服务器 Tick 产生压力 |
| **B07** 存活计时 | `LifeDuration` | 10 ~ 120 s | 5 s（最短）/ 600 s（最长）| 0 = 永久存在，召唤物慎用 |
| **B09** 多阶段 | 阶段触发 HP 阈值 | 每阶段差 ≥ 15% | 10%（最低阈值）| 阈值差太小时阶段切换过于频繁，难以感知 |



> 本章替代原"内容合法性验证"章节。
> 核心目标：帮助 AI 更准确地将玩家的自然语言转化为可执行的游戏内容，而不是设置限制。

### 5.1 量词与程度词的数值映射

玩家经常用模糊程度词描述属性。AI 应将以下词汇映射为具体数值（基于对应模板的默认值）：

| 程度词 | 数值倍率（相对默认值） | 示例（Tank HP 默认 3000） |
|--------|---------------------|------------------------|
| 一点点强 / 稍微厉害 | ×1.3 | → 3900 |
| 比较强 / 强一些 | ×2.0 | → 6000 |
| 很强 / 挺强的 | ×3.0 | → 9000 |
| 非常强 / 超级强 | ×5.0 | → 15000 |
| 最强 / 无敌 / 超级无敌 | ×10.0（取模板最大值） | → 30000（不超上限） |
| 很弱 / 弱鸡 | ×0.3 | → 900 |
| 比较脆 / 容易死 | ×0.5 | → 1500 |

> 注：程度词叠加时取最高一档，不做累加（"非常非常强" = ×10.0，不是 ×25.0）

### 5.2 外观/风格词 → GPO 类型匹配

玩家可能用外观或世界观词汇描述 GPO，AI 应匹配到最接近的模板：

| 玩家描述词 | 推荐模板 | 匹配理由 |
|-----------|---------|---------|
| 机器人、战车、铁甲、钢铁怪、普通怪 | T-Tank | 通用地面战斗 |
| 小鱼、快速小怪、轻型单位 | T-FeiYu | 轻量型聚焦攻击 |
| 乌龟、厚甲怪、慢速重型、远程炮击 | T-WuGui | RPG弹药远程 |
| 老虎、猛兽、近战狂暴、高速斩击 | T-SwordTiger | 高速近战+可驾驶 |
| 飞碟、飞行器、无人机、侦察机 | T-UAV | 自动飞行追踪 |
| 直升机、武装飞机、可驾驶飞行器 | T-Helicopter | 飞行+可玩家驾驶 |
| 炮台、机枪塔、防御工事（地图固定）| T-MachineGun | 固定地图高频射击 |
| 炮塔（玩家放的）、召唤炮台 | T-Turret | 技能召唤，继承属性 |
| 导弹、追踪炮台（玩家放的）| T-MissileBattery | 召唤型追踪导弹 |
| Boss、首领、大魔王、最终形态 | T-RexKing | BOSS级 |
| 宝箱、补给、道具箱、按钮 | T-SceneGPO | 场景互动，无敌 |
| 金蛋、争夺目标、需要保护的物体 | T-GoldenEgg | 只有HP，供争夺 |
| 刷怪点、波次怪、召唤器 | T-GPOSpawner | 生成其他GPO |
| 护盾、防护罩（玩家召唤）| T-Shield | 跟随玩家的护盾 |
| 龙、怪兽（地面移动）| T-Tank 或 T-SwordTiger + 外观注释 | 地面移动单位 |
| 飞龙、飞天怪兽 | T-UAV 或 T-Helicopter + 外观注释 | 飞行单位 |

### 5.3 行为意图 → 预设包匹配

玩家描述的行为意图通常不会直接使用预设包名称，AI 需要进行语义映射：

| 玩家描述 | 匹配预设 | 优先级 |
|---------|---------|--------|
| 看到人就追、主动找人打、见人就攻击 | B02 发现追击 | 高 |
| 不动、固定守在这里、只打来的人 | B03 固守阵地 | 高 |
| 随机走动、在这个区域晃 | B01 警戒巡逻 | 中 |
| 快死了/血少就跑、胆小、会逃跑 | B04 低血逃跑 | 中 |
| 叫救兵、召唤更多、呼叫援军 | B05 召唤援军 | 中 |
| 定时炸弹、每 X 秒攻击、周期触发 | B06 定时触发 | 中 |
| 一段时间后消失、临时存在、有寿命 | B07 存活计时 | 低 |
| 被打才还手、反击、不主动攻击 | B08 被攻击反击 | 低 |
| 隐身消失后再出现、周期隐现 | 定制 Component（隐现逻辑）| 特殊 |
| 死了又活、复活、重新出现 | 定制 Component（复活逻辑）| 特殊 |

### 5.4 复合描述的拆解方式

当玩家一次性描述多个属性 + 行为时，AI 的拆解顺序：

```
Step 1：先确定模板类型（地面/飞行/炮台/Boss/场景）
Step 2：提取所有属性词 → 套用 5.1 程度词映射 → 得到数值
Step 3：提取所有行为词 → 套用 5.3 预设包映射 → 得到行为列表
Step 4：如果行为无法用预设包覆盖 → 标记为"需要定制 Component"
Step 5：汇总生成确认摘要（见第 7 章）
```

**拆解示例 1：**
```
玩家：「我想要一个血超厚的飞行机器人，发现玩家就追，快死了会临时隐身」

Step 1：飞行 → T-UAV
Step 2：血超厚 → Hp = 默认 2000 × 5.0 = 10000
Step 3：发现玩家就追 → B02（发现追击）
        快死了会临时隐身 → 定制 Component（监听 HP 低于 30%，切换 HideEntity Tag）
Step 4：隐身是定制逻辑 → 生成 ServerAIUavCustomLowHpHide.cs
Step 5：输出确认摘要
```

**拆解示例 2（复合 BOSS + 多阶段 + 召唤）：**
```
玩家：「我想要一个超强 BOSS，血量越少越疯狂，到快死的时候会召唤一堆小怪，
       最后阶段变成黑色并且攻击速度翻倍」

Step 1：BOSS + 超强 → T-RexKing，Hp = 默认 50000 × 5.0 = 250000
Step 2：血量越少越疯狂 → B09（多阶段 TimeLine），设 3 个阶段：
        - 阶段1（HP > 60%）：正常行为
        - 阶段2（HP 30%~60%）：MoveSpeed × 1.5，AttackInterval × 0.7
        - 阶段3（HP < 30%）：触发最终阶段
Step 3：到快死召唤小怪 → B05，在 TimeLine 阶段2触发时调用 SM_AI.Event_AddAI
Step 4：最后阶段攻击速度翻倍 + 外观变黑 →
        定制 Component（ServerAIRexKingCustomFinalPhase.cs）：
        - 监听 TimeLine 阶段3事件
        - 攻击间隔参数降为原来的 0.5 倍
        - 发送外观变色消息（需客户端 Component 配合）
Step 5：输出确认摘要，提示外观"变成黑色"需要确认是否有对应美术资源或使用程序化颜色
```

### 5.5 技术安全底线（唯一不可绕过的规则）

以下规则是**技术层面**的约束，与游戏平衡无关，不可绕过：

| 规则 | 原因 |
|------|------|
| 定制 Component 必须在 `OnAwake` 注册事件，`OnClear` 必须注销 | 防止内存泄漏（代码规范 R15） |
| 不得在 `Update` 中使用 `new` / `GetComponent` / LINQ | 性能规范（代码规范 R9） |
| 定制 Component 必须有 `namespace Sofunny.BiuBiuBiu2.ServerGamePlay` | 命名规范 |
| 不得修改 Base 类 / Manager 类 / World 类 | 架构边界（代码规范 R2） |
| 不得直接修改 `ServerAIWorld_Switch.cs` / `ClientAIWorld_Switch.cs` | UGC 边界规则（见 1.1）|

---

## 6. 意图理解规范

### 6.1 玩家语言 → 设计意图映射表

AI 应将玩家的口语描述映射为具体的模板选择和参数。

| 玩家说 | 映射的设计意图 | 推荐模板 | 推荐预设 |
|--------|-------------|---------|---------|
| "追着玩家打的怪" | 追击+攻击 | T-Tank / T-FeiYu | B02 |
| "快速冲刺砍人的怪" | 高速近战追击 | T-SwordTiger | B02 |
| "厚甲用炮打人的怪" | 重甲远程 | T-WuGui | B02 |
| "固定不动的炮台" | 固守+范围攻击 | T-MachineGun | B03 |
| "空中飞来飞去的" | 飞行+巡逻/攻击 | T-UAV | B01+B02 |
| "玩家可以开的飞机" | 可驾驶飞行器 | T-Helicopter | - |
| "超强的 BOSS" | 高属性+专属攻击 | T-RexKing | B02 |
| "多阶段BOSS / 越打越厉害" | 多阶段 TimeLine 控制 | T-RexKing | B02+B09 |
| "玩家放的炮台" | 召唤固定炮 | T-Turret / T-MissileBattery | B03 |
| "追踪导弹炮" | 召唤追踪炮 | T-MissileBattery | - |
| "护盾球（玩家技能）"| 召唤防护罩 | T-Shield | - |
| "刷怪的机器/刷新点" | 波次生成器 | T-GPOSpawner | - |
| "需要争夺/保护的目标" | 只有 HP 的目标物 | T-GoldenEgg | - |
| "机关/宝箱/不能打碎" | 无敌交互物件 | T-SceneGPO | - |
| "血少但很快的小怪" | 低HP+高速追击 | T-FeiYu | B02 |
| "会叫救兵的怪" | 追击+低血召唤 | T-Tank + B05 | B02+B05 |
| "被打才还手的机关" | 交互+反击 | T-SceneGPO | B08 |
| "定时消失的陷阱" | 计时消亡 | T-UAV / T-MissileBattery | B07 |
| "打不死的怪" | → 高血量（不是无敌）| 对应模板 | 自动裁剪 |
| "会飞还能追人还能召唤" | 多行为组合 | T03 | B02+B05（最多3个）|

### 6.2 模糊意图处理规范

当玩家描述无法明确映射时，AI 必须**主动提问**，而不是猜测：

**触发追问的条件：**
- 描述里没有提到任何攻击/防御/行为词汇
- 描述的行为互斥（见 4.2）
- 需要玩家确认数值（如"很强"不够精确）

**追问格式示例：**
```
玩家："我要一个很厉害的怪"
AI："好的！我需要确认几点：
    1. 它是地面的还是飞行的？（地面推荐坦克型，飞行推荐无人机型）
    2. 它主动追玩家，还是待在原地攻击接近的玩家？
    3. 你说的"很厉害"大概是多厉害？（普通怪×3倍？还是BOSS级？）"
```

**⚠️ 禁止猜测规则：以下场景必须追问，禁止自行选择**

| 歧义场景 | AI 必须问的问题 | ❌ 禁止的做法 |
|---------|--------------|-------------|
| "会隐身的怪" | "是低血量触发隐身，还是周期性隐现，还是被打时隐身？" | 直接选"低血量"最常见的那种 |
| "会逃跑的怪" | "是快死了才逃，还是一被发现就逃，还是攻击后逃？" | 默认为"低血量逃跑"（B04）|
| "很强的技能" | "是攻击力高、血量多、还是有特殊行为（比如多阶段）？" | 把所有属性都调到最大 |
| "会变身的 BOSS" | "分几个阶段？每个阶段在多少血量触发？" | 默认3阶段各33% |
| "召唤援军" | "召唤什么类型的援军？几只？冷却多少秒？" | 默认召唤Tank，数量2，冷却30s |
| "固定炮台但又能追人" | "是固定位置旋转攻击，还是会移动到玩家附近？（二者互斥）" | 选其中一个不告知玩家 |

**禁止的处理方式：**
- ❌ 直接用"最强配置"生成，然后被平衡规则拒绝
- ❌ 生成一个"合理猜测"但不告知玩家做了哪些假设
- ❌ 遇到歧义直接选一个"感觉合理"的实现，事后才告知玩家

### 6.3 特殊描述处理

| 玩家描述 | 识别方式 | AI 响应 |
|---------|---------|---------|
| "无敌" / "不能死"（战斗型）| 转化为极高属性 | "我帮你设置成最高血量，让它非常难被击败！" |
| "无敌" / "不能死"（场景物件）| T05 模板天然支持 | 直接使用 GodMode Tag，无需特殊处理 |
| "隐身" | 定制 Component（HideEntity） | "我可以让它在某些条件下隐身（比如低血量触发、周期隐现），你希望什么时候隐身？" |
| "复活" / "死了再生" | 定制 Component（DisableDeadRemove + 重生逻辑）| "我可以让它复活，你希望复活几次？每次复活多少血量？" |
| "一枪秒人" | ATK 设为极高值 | 直接生成，按玩家意图执行 |
| "100 个小弟" | GPOSpawner 波次配置 | "我帮你配置生成 100 个，不过同屏太多可能会有卡顿，你想一次性全出还是分批刷新？" |
| "会说话" / "有台词" | 超出 GPO 范围 | "对话系统目前不在 GPO 的能力范围内，但我可以给它添加攻击时的音效触发" |
| "打不死" | 等同"无敌" | 设为模板最高 HP 值 |

---

## 7. AI 处理流程

收到 UGC 玩家的 GPO 创建请求后，AI 按以下步骤处理：

```
Step 1：意图理解
  读取玩家描述 → 提取：类型词、属性词、行为词
  如有歧义 → 跳转至「追问流程」（6.2）

Step 2：模板匹配
  根据类型词 → 选择最合适的模板（参照 2.1 分类总览）
  不确定时优先选 T-Tank（通用性最强）

Step 3：属性解析
  将玩家描述的属性词转为具体数值（参照 3.1 和 3.2）
  未提及的属性使用默认值

Step 4：行为预设匹配
  将玩家描述的行为词映射到 B01–B08 预设包
  检查互斥和支持表（4.2、4.3）

Step 5：合法性验证
  按第 5 章全部规则逐项检查
  有问题 → 自动裁剪并记录调整原因

Step 6：生成确认摘要
  向玩家展示：
  - 你要创建的是：[模板名称]
  - 名字：[玩家给的名字 / AI 建议名]
  - 属性：血量 [X]，攻击力 [X]，速度 [X]
  - 行为：[行为包名称列表]
  - 如有调整：说明哪里被调整了和原因
  - 询问：「确认生成吗？」

Step 7：生成内容
  确认后 →
  a. 生成 GPOM 配置数据行（参照同类型已有数据格式，注明"待策划校验"）
  b. 如有定制行为 → 生成 ServerAI{Type}Custom{Behavior}.cs Component 文件
  c. 美术资产：优先复用同类型现有 AssetSign；无可用资产时自动使用 Box/Sphere 占位
  告知玩家：「已创建完成，外观暂用占位模型，美术后续可替换」
```

---

## 8. 附录：Component 代码模板

> 所有 UGC 定制 Component 必须遵循此模板结构。

### 8.1 标准 Custom Component 模板

**命名规范：** `ServerAI{GpoType}Custom{BehaviorName}.cs`
例：`ServerAITankCustomLowHpFlee.cs`、`ServerAIRexKingTimeLine.cs`

```csharp
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.ServerMessage;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {

    // [行为树迁移说明] 本 Component 实现的逻辑，如需迁移到 BehaviorDesigner 行为树：
    // 结构：Sequence
    //   ├── Condition: ConditionHpThreshold（HP < XX%）
    //   └── Action: ActionXXX（具体行为描述）
    // 迁移后可删除本 Component，由行为树统一管理。
    public class ServerAI{GpoType}Custom{BehaviorName} : ComponentBase {

        protected override void OnAwake() {
            Register<SE_AI.Event_SetHp>(OnHpChanged); // 事件注册放在 OnAwake
        }

        protected override void OnStart() {
            // 启动逻辑（可选）
        }

        protected override void OnClear() {
            Unregister<SE_AI.Event_SetHp>(OnHpChanged); // 必须注销，对应 OnAwake 里的注册
        }

        private void OnHpChanged(SE_AI.Event_SetHp evt) {
            // 业务逻辑写在 Component 里，不能放到 System 里
            // 禁止在此方法里 new / GetComponent / LINQ（性能规范 R9）
        }
    }
}
```

### 8.2 召唤援军（B05）的实际调用方式

> 来源：`ServerAIWaveSpawner.cs` 中确认的机制

通过 `SM_AI.Event_AddAI` 全局消息生成新 GPO：

```csharp
// 在 Component 内部调用（如低血量触发）
MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
    AISign = "reinforcement_tank",          // 要召唤的 GPO 的 Sign（GPOM 配置里的 Sign 字段）
    StartPoint = mySystem.GetPosition(),    // 召唤位置，通常在自身附近
    OR_GpoType = GPOData.GPOType.AI         // AI 类型
});
```

**B05 需要的配置文件：**
- `GPOM_Tank`（或对应类型）：新增一条援军 GPO 数据行，配置好 `Sign` 字段
- 调用 Component 里引用该 `Sign` 字符串

---

## 9. 已决策项归档

| # | 问题 | 决策 | 状态 |
|---|------|------|------|
| V03 | 第 3.1 章各模板属性数值范围是否与线上数值体系匹配？ | **AI 直接根据 UGC 用户需求生成，无需对齐线上数值体系。** 数值由用户意图驱动，AI 在合理范围内自由裁量。 | ✅ 已决策 |
| V04 | UGC 是否可以从零动态创建新 SceneGPO？ | 当前架构不支持。动态拼装需新建 DynamicSceneGPOLoader，后续单开任务。**当前 AI 仅可描述布局意图，不生成可执行 SceneGPO 实例。** | 🟢 架构已明确，单独立项 |

---

*文档版本：v1.3（向 Ability 文档对齐补强：① 模板库新增稳定性状态列；② 第4章新增预设包参数边界表；③ 5.4节新增复合 BOSS 拆解示例；④ 6.2节强化歧义处理规则，加入"禁止猜测"明确场景表）*
