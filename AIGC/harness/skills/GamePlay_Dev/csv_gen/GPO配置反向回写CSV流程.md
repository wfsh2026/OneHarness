# GPO 配置反向回写 CSV 流程

> **适用场景**：在代码中手动新建了 GPO 模板（GPOM_XXX.cs），需要将其数据反向写入策划配置表，让 csv-gen 自动生成并管理该文件。
> **目录**：`E:\CSVFile\csv-file\data\`

---

## 一、背景与核心原则

项目中所有 GPO（Game Play Object）模板代码都由 **csv-gen 工具**根据策划配置表自动生成。手动编写的 GPOM 文件在 csv-gen 重新运行后会被**覆盖或删除**。

**正确流程**：先写配置表 → csv-gen 自动生成代码  
**反向修复流程**：手动代码先跑通验证 → 再回写 CSV → 删除手动文件 → 验证 csv-gen 生成结果

---

## 二、涉及的配置文件

| 文件 | 作用 |
|------|------|
| `gpo_type.csv` | GPO 类型注册（每种 GPO 类型一行） |
| `gpo.csv` | GPO 实例注册（每个 GPO 一行，关联类型） |
| `gpo_attr_type.csv` | GPO 属性类型定义（GPOM struct 字段的来源） |
| `gpo_attr.csv` | GPO 实例的属性值配置（生成 GPOM struct 的 Data 数组内容） |
| `map.csv` | **地图注册**（新增地图时同步填写，不在 GPO 表中） |

> `map.csv` 不属于 GPO 体系，但坦克大战等功能同时新增地图，需一并回写，否则 `MapSet.Id_XXX` 常量不会生成。

---

## 三、步骤详解

### Step 1：在 `gpo_type.csv` 注册新 GPO 类型

格式：`id \t name \t sign`

- `id`：全局唯一整数，从现有最大值 +1 分配
- `name`：中文名称
- `sign`：英文唯一标识（用于代码引用）

**示例（机械臂副枪）：**
```
53	机械臂副枪	Hero10MechanicalArm
```

> ⚠️ `gpo_type.id` 同时也是 `gpo.gpo_type`，**两者必须一致**。

---

### Step 2：在 `gpo.csv` 注册 GPO 实例

格式：`id \t gpo_type \t name \t sign \t asset_sign \t desc \t gpo_tag`

- `id`：GPO 实例唯一 ID（同一 gpo_type 下有多个实例时，各实例 id 各不相同，**不强制等于 gpo_type.id**）
- `gpo_type`：对应 `gpo_type.id`
- `sign`：唯一标识，与代码中 `GPOM_XXXSet.Sign_XXX` 保持一致
- `asset_sign`：客户端 Entity 资源路径中的 SkinSign（灰盒阶段可留空）
- `desc`：描述（可选）
- `gpo_tag`：标签数组（无标签填空）

**示例（单实例，id 与 gpo_type.id 相同）：**
```
53	53	机械臂副枪	Hero10MechanicalArm		英雄10大招期间召唤的机械臂副枪	
```

**示例（同一 gpo_type 下多实例，如坦克基地 type=30）：**
```
9001	30	坦克大乱斗-红方基地	TankBattle_RedBase	TankBattle_RedBase	坦克大乱斗红方基地	
9002	30	坦克大乱斗-蓝方基地	TankBattle_BlueBase	TankBattle_BlueBase	坦克大乱斗蓝方基地	
```

> ⚠️ 同一 gpo_type 下存在多个 GPO 实例（如红蓝基地）时，csv-gen 只生成**一个 Set 类**（`GPOM_TankBaseSet`），Data 数组包含所有实例。不要为每个实例重复新增 gpo_type。

---

### Step 3：识别哪些字段需要在 `gpo_attr_type.csv` 新增

对比手动写的 GPOM struct 字段与 `gpo_attr_type.csv` 现有字段：

- **已存在的通用字段**（hp、atk、move_speed、quality 等）→ 直接在 Step 4 引用，不需要新增
- **GPOM 独有的业务字段**（如 `DamageRatio`、`AttackRange`、`MaxFlyHeight` 等）→ 需要先在此新增

格式：`id \t name \t sign \t value_type \t is_default`

- `id`：现有最大值 +1
- `sign`：字段名（snake_case），csv-gen 用它生成 C# 属性名（转为 PascalCase）
- `value_type`：`int` / `float` / `string` / `byte` / `[]int` / `ushort`
- `is_default`：是否为 IGPOM 接口的内置字段（通常填 `false`）

**示例（新增副枪伤害系数）：**
```
48	副枪伤害修正系数	damage_ratio	float	false
```

> `sign=damage_ratio` → csv-gen 生成 `public float DamageRatio { get; }`

---

### Step 4：在 `gpo_attr.csv` 配置 GPO 实例的属性值

格式：`id \t gpo_id \t match_mode \t gpo_attr_type \t value`

- `id`：全局唯一，从现有最大值 +1
- `gpo_id`：对应 `gpo.id`
- `match_mode`：0 = 通用（所有模式），其他值对应特定游戏模式
- `gpo_attr_type`：对应 `gpo_attr_type.id`
- `value`：属性值

**示例（为机械臂配置 damage_ratio=0.5）：**
```
1177	53	0	48	0.5
```

---

## 四、什么时候不需要写 gpo_attr

以下类型的 GPO **不需要** gpo_attr 行：

- 所有业务行为都由代码 Component 控制，没有独立的 HP/ATK/AI 行为树
- 不参与 AI 战斗（不索敌、不自主攻击）
- 没有独立的移动速度（跟随宿主）

机械臂副枪只配置了 `damage_ratio`，其余属性（hp=0、无 ai_behavior）均无需配置，保留为默认值。

---

## 五、验证 csv-gen 生成结果

运行 csv-gen 后检查：

```
✅ GPOM_Hero10MechanicalArm.cs 是否自动生成
✅ struct 中是否包含 DamageRatio 字段
✅ IGPOM.cs 的 GetGPOMData switch 是否自动补上对应 case
✅ GpoType.cs 中 Id_Hero10MechanicalArm = 53 是否存在
✅ Gpo.cs 中 new Gpo(53, ...) 是否存在
```

---

## 六、机械臂副枪实战记录（完整配置）

| 文件 | 新增行 |
|------|--------|
| `gpo_type.csv` | `53 \t 机械臂副枪 \t Hero10MechanicalArm` |
| `gpo.csv` | `53 \t 53 \t 机械臂副枪 \t Hero10MechanicalArm \t （空）\t 英雄10大招... \t （空）` |
| `gpo_attr_type.csv` | `48 \t 副枪伤害修正系数 \t damage_ratio \t float \t false` |
| `gpo_attr.csv` | `1177 \t 53 \t 0 \t 48 \t 0.5` |

---

## 七、常见陷阱

| 陷阱 | 说明 |
|------|------|
| `gpo_type.id` ≠ `gpo.gpo_type` | 两者必须对应，否则 csv-gen 无法关联 |
| 手动写的 GPOM 文件被覆盖 | csv-gen 每次运行都会重新生成，手动文件必须先回写 CSV |
| 新字段忘记在 `gpo_attr_type` 注册 | csv-gen 不认识该字段，不会生成对应属性 |
| `gpo_attr.id` 重复 | 会导致 csv-gen 报错，需确保全局唯一 |
| `match_mode=0` vs 特定模式 | 0 表示通用配置，如果游戏有多个模式需要不同数值则需要多行 |
| **csv-gen 重新生成后类名/常量名改变** | AI 手写的命名可能不符合 csv-gen 规范，重新生成后名称会变。回写 CSV 并运行 csv-gen 后，**必须全局搜索旧类名/常量名**，修复所有引用。常见变化：`GPOM_TankBattleSet` → `GPOM_TankBaseSet`，手写常量 `BaseMaxHp` 在生成版中消失 |
| 文档示例中的 id 会随项目推进过期 | 本文档的示例 id（如 `gpo_attr.id=1177`）仅为说明格式，**实际操作时必须读取当前 CSV 末尾行确认最新 id**，不得直接使用文档示例中的数字 |
| 漏写 `map.csv` | 新增地图时仅写 GPO 表，遗漏 map.csv，导致 `MapSet.Id_XXX` 常量不生成 |

---

## 八、csv-gen 重生成后的命名修复流程

> 适用于：AI 手写 GPOM 的命名与 csv-gen 规范不符，回写 CSV 并重新生成后出现编译报错。

**规范说明**：csv-gen 按 `gpo_type.sign` 生成类名（如 sign=`TankBase` → `GPOM_TankBase` / `GPOM_TankBaseSet`），常量名按 `gpo.sign` 转 PascalCase 生成（如 sign=`TankBattle_RedBase` → `Id_TankBattleRedBase`）。手写版若使用不同命名则会在重生成后失效。

**修复步骤**：

1. **对比新旧文件差异**：`git show <commit> --stat` 查看 csv-gen 生成了哪些新文件、删了哪些旧文件
2. **找出名称变化**：重点关注类名（`GPOM_XXXSet`）、常量名（`Id_XXX`、`Sign_XXX`、手写业务常量如 `BaseMaxHp`）
3. **全局搜索旧名**：在 `Assets\Scripts` 下搜索所有旧名引用
4. **逐一修复**：
   - 类名替换：直接 replaceAll
   - 手写常量消失（如 `BaseMaxHp`）：改为从 Data 读取，如 `GPOM_TankBaseSet.GetGPOMByIdAndMatchMode(GPOM_TankBaseSet.Id_TankBattleRedBase).Hp`
5. **验证**：确认无残留引用后等待 Unity 编译通过

**本次坦克大战实际变化记录**：

| 旧名（AI 手写） | 新名（csv-gen 生成） | 影响文件 |
|---|---|---|
| `GPOM_TankBattleSet` | `GPOM_TankBaseSet` | `ServerTankBattleMode.cs` |
| `GPOM_TankBattle`（struct） | `GPOM_TankBase` | 同上 |
| `GPOM_TankBattleSet.BaseMaxHp` | 无对应常量，改为 `.GetGPOMByIdAndMatchMode(...).Hp` | 同上（6 处） |
| `Id_TankBattle_RedBase` | `Id_TankBattleRedBase` | 无外部引用，仅 Template 内 |
| `Id_TankBattle_BlueBase` | `Id_TankBattleBlueBase` | 同上 |
