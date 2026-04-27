# GPO 开发规范

> 本文件专注于 GPO（Game Play Object）类型的开发规范。
> 通用 Entity 构建规范（HitType/SetGameObjectEntity/OnSetEntityObj/Scale/Prefab加载路径）见 `core-rules.md §第四部分（Rule 11-19）`。
> 参考范例：[[GPO 参考范例]]

## ⚠️ 强制工具规则

> **新建 GPO 类型时，AI 必须调用以下工具：**
> 1. `aigc/harness/tools/codegen/gpom-gen.sh` — 生成 GPOM 模板数据文件
> 2. `aigc/harness/tools/codegen/gpo-gen.sh` — 生成 Server/Client AI System + 所有注册（默认 Graybox 占位体，可用 `--shape`/`--size`/`--color` 定制，或 `--model` 指定模型路径关闭 Graybox）
> 3. `aigc/harness/tools/codegen/component-gen.sh` — 生成 GPO 专属 Component 模板（`--type ai`），优先使用 `--template` 参数选择预置模板：
>    - `findtarget` — 周期索敌
>    - `lifetime` — 倒计时自毁
>    - `move` — 方向移动 + iEntity.SetPoint
>    - `rotate` — A→B 旋转插值 + iEntity.SetRota
>    - `scale` — A→B 缩放插值 + iEntity.SetLocalScale
>
> 禁止手动创建 GPOM struct、ServerAI/ClientAI System，或手动修改 GpoType.cs / Switch / IGPOM 注册文件。
> 仅在修改已有 GPO 的业务逻辑（如 AddComponents 内容）时可直接编辑。
> 详见 [[codegen/README]]。

## 📌 按需加载子文件

| 场景 | 加载文件 |
|------|---------|
| 开发 SceneGPO（基地/可破坏掩体/触发区域） | `gpo-code-scenegpo.md` |

---

## 一、新建 GPO 必须创建的文件清单

> 基于炮台类 GPO（MachineGun）范例总结，适用于所有新增 AI GPO 类型。
> **开发前必须确认以下所有文件是否均已规划在执行计划中。**

### 📋 配表层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/Template/gpo/GPOM_XXX.cs` | **新建**（按 GoldenEgg 格式手写） | GPO 模板数据类（struct + 静态数据集），字段与 GPOM_GoldenEgg.cs 完全一致 |
| `Assets/Scripts/Template/data/Gpo.cs` | **修改**：data 数组新增一行 | GPO 数据行注册，填 Id/Sign/Name 等 |
| `Assets/Scripts/Template/gpo/GpoTypeSet.cs` | **修改**：新增常量 `Id_XXX` | GPO 类型 ID 常量 |
| `Assets/Scripts/Template/gpo/IGPOM.cs` | **修改**：GetGPOMData switch 新增 case | GPO 类型路由注册 |

> **注意**：`GpoTypeSet.Id_XXX`（类型路由 ID）和 `GpoSet.Id_XXX`（数据行 ID）是**两个不同的值**，不可混淆。

---

### 📄 GPOM_XXX.cs 唯一标准格式

所有 GPOM 文件只有**一种格式**，以 `GPOM_GoldenEgg.cs` 为标准模板：

```csharp
// 参照：Assets/Scripts/Template/gpo/GPOM_GoldenEgg.cs
namespace Sofunny.BiuBiuBiu2.Template {

    // 1. 数据结构体（固定字段，不可增减）
    public struct GPOM_XXX : IGPOM {
        public readonly string AssetSign { get; }
        public readonly int[] GpoDropId { get; }
        public readonly ushort GpoDropType { get; }
        public readonly string GpoSoConfig { get; }
        public readonly int[] GpoTag { get; }
        public readonly int GpoType { get; }
        public readonly int Hp { get; }
        public readonly int Id { get; }
        public readonly int MatchMode { get; }
        public readonly string Name { get; }
        public readonly byte Quality { get; }
        public readonly string Sign { get; }
        // GetXXX() 方法同 GoldenEgg，直接 return 字段
        public GPOM_XXX(string assetSign, ...) { /* 同 GoldenEgg */ }
    }

    // 2. 静态数据集（Id/Sign 常量 + Data 数组 + GetGPOMByIdAndMatchMode）
    public static class GPOM_XXXSet {
        public const int    Id_XXX   = 9000;
        public const string Sign_XXX = "XXX";
        // ⚠️ 禁止在此放游戏业务逻辑常量（如 BuffDuration、SpawnTimes），
        //    这些属于模式代码（ServerXXXMode.cs），不属于 GPO 数据模板
        public static readonly GPOM_XXX[] Data;
        static GPOM_XXXSet() {
            Data = new GPOM_XXX[] { new GPOM_XXX(...) };
        }
        public static GPOM_XXX GetGPOMByIdAndMatchMode(int id, int matchMode = 0) {
            foreach (GPOM_XXX data in Data)
                if (data.Id == id && data.MatchMode == matchMode) return data;
            return default;
        }
    }
}
```

> ⚠️ **`Assets/Bundle/Configs/Gpo/` 目录不存在**，任何 Agent 都不可在此路径下创建文件。GPOM_XXX.cs 是直接手写 C#，无需 CSV 源文件。

---

### 🔌 路由注册层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/ServerAIWorld_Switch.cs` | **修改**：AddAIForGpoMTypeId switch 新增 case | 服务端 GPO 类型路由 |
| `Assets/Scripts/GamePlay/Client/AI/ClientAIWorld_Switch.cs` | **修改**：同上 | 客户端 GPO 类型路由 |

---

### 🖥️ 服务端 System 层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerAIXXXSystem.cs` | **新建** | 继承 `S_AI_Base`，OnAwake 强转 MData，AddComponents 先调 base |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIXXXAttack.cs` | **新建**（若有定制攻击） | 继承 `ServerNetworkComponentBase`，实现攻击/开火逻辑 |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIXXXHeadRota.cs` | **新建**（若有旋转同步） | 炮塔/头部旋转计算 + Rpc 同步 |

---

### 💻 客户端 System 层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientAIXXXSystem.cs` | **新建** | 继承 `C_AI_Base`，AddComponents 先调 base，OnStart 调 CreateEntity |
| `Assets/Scripts/GamePlay/Client/AI/Components/ClientAIXXXAttack.cs` | **新建**（若有定制开火表现） | 特效、音效、动画播放 + 玩家输入处理 |
| `Assets/Scripts/GamePlay/Client/AI/Components/ClientAIXXXHeadRota.cs` | **新建**（若有旋转接收） | 接收 Rpc，平滑 Slerp 到目标角度 |

---

### 📡 网络协议层（按需）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/Message/Network/6_Proto_AI.cs` | **修改**：新增 `Rpc_SyncXXXRota` struct（分配新 FuncID） | GPO 专属旋转/状态同步协议（若旋转方式与现有不同） |
| `Assets/Scripts/GamePlay/Client/Network/Component/ClientNetworkSerialize.cs` | **修改**：UnSerializeBuffer switch 新增 case | 新 Proto 必须注册，否则 RPC 静默失败 |

---

### 🎨 资产层（必须，灰盒阶段可延后）

| 资产 | 说明 |
|------|------|
| `AI/Server/XXXServer.prefab` | 服务端 Entity Prefab（含碰撞体、骨骼节点，不含 Renderer） |
| `AI/Client/XXX.prefab` | 客户端 Entity Prefab（含 Renderer、Animator、特效挂点） |
| `Effects/fx_xxx_fire.prefab` | 攻击特效（PrefabPool 管理） |

---

## 二、AIEntity 构建顺序（多层级时）

> **来源：赛博炮台开发复盘（2026-03-25）**

`AIEntity.Awake` 收集所有子节点的 `HitType`。**必须在所有子节点挂载完成后，最后添加 AIEntity**。

```csharp
// ❌ 错误：子节点尚未创建时就添加 AIEntity
root.AddComponent<AIEntity>();
var headGo = new GameObject("Head");   // ← AIEntity 已执行 Awake，收集不到

// ✅ 正确：先组装所有子节点，最后添加 AIEntity
var root = new GameObject("Turret");
root.AddComponent<HitType>().Part = GPOData.PartEnum.RootBody;
var headGo = new GameObject("Head");
headGo.transform.SetParent(root.transform, false);
headGo.AddComponent<HitType>().Part = GPOData.PartEnum.Head;
// ... 其他子节点 ...
root.AddComponent<AIEntity>();   // ← 最后添加
SetGameObjectEntity(root, StageData.GameWorldLayerType.AI);
```

---

## 三、GPO 类型注册（配表层）

> ⚠️ **重要区分（新增，2026-03 Bug 复盘）**
>
> | 注册文件 | 适用范围 | 说明 |
> |---------|---------|------|
> | `Gpo.cs` 数据行 | **每一个新 GPO 实例都必须** | 无论是否复用已有 GpoType，每个新的 GPO Sign/Id 都必须在 data 数组中注册一行。缺失会导致 `GetGPOMData(sign)` 返回 null → NullReferenceException |
> | `IGPOM.cs` 路由 | **仅新增 GPO 类型（新 GpoTypeSet.Id_XXX）时** | 如果复用已有类型（如复用 T-GoldenEgg），IGPOM.cs 无需修改 |
>
> **典型错误案例（坦克大乱斗 Phase 3）**：SuperBuff 复用了 T-GoldenEgg 类型，开发 Agent 误以为 Gpo.cs 无需修改，导致 `GetGPOMData("SuperBuff")` 返回 null，运行时崩溃。

新增 GPO 类型时，**必须同时**完成以下两处注册，缺少任一会导致运行时报错：

### 3.1 Gpo.cs — 数据行注册

```csharp
// Assets/Scripts/Template/data/Gpo.cs — data 数组
new Gpo(100, 23, "赛博炮台", "CyberBattery", "CyberBattery", "赛博炮台"),
// 第一个参数 Id 必须与 GPOM_XXX.Id 完全一致
```

### 3.2 IGPOM.cs — 类型路由注册

```csharp
// Assets/Scripts/Template/gpo/IGPOM.cs → GetGPOMData switch
case GpoTypeSet.Id_CyberBattery:
    mData = GPOM_CyberBatterySet.GetGPOMByIdAndMatchMode(gpoId, matchMode);
    break;
```

---

## 四、S_AI_Base 默认已挂载的组件（无需重复添加）

继承 `S_AI_Base` 的 System 自动获得以下组件：

| 组件 | 职责 |
|------|------|
| `ServerAIDead` | 死亡流程（通知客户端、延迟销毁） |
| `ServerAIMaster` | 主人绑定（召唤者 GPO） |
| `ServerAIHateTarget` | 仇恨列表 |
| `ServerAIHurt` | 受伤处理 |
| `KnockbackGPO` | 击退 |
| `StrikeFlyGPO` | 击飞 |
| `ServerGPOAttackProtect` | 生成后无敌保护期 |
| `ServerGPOShowEntity` | 显隐同步 |
| `ServerAIPatrolPoint` | 巡逻点 |
| `ServerGPOAbilityEffect` | Ability 效果接收 |
| `ServerAIQuality` | 品质等级调整 |
| `ServerGPODropItem` | 死亡掉落道具 |

---

## 四点五、GPOType 枚举的实际含义（2026-03-27 坦克大乱斗沉淀）

> **关键踩坑：GPOType.AI ≠ 所有服务端 AI 单位**

| GPOType | 对应生成方式 | 典型示例 |
|---------|------------|---------|
| `GPOType.AI` | `SM_AI.Event_AddAI`（普通 AI） | 野怪、炮台、场景 AI |
| `GPOType.MasterAI` | `SM_AI.Event_AddMasterAI`（主控 AI） | **坦克（ServerTankBattleMode 用 AddMasterAI 生成）** |
| `GPOType.RoleAI` | `SM_AI.Event_AddAI`（人形 AI） | 模拟真人角色的 AI |
| `GPOType.Role` | 玩家角色 GPO | 玩家本体 |
| `GPOType.SceneElement` | 场景 SceneGPO | 基地、可破坏掩体、Buff 刷新点 |

**常见错误**：在拾取/碰撞检测中用 `GPOType.AI` 过滤坦克 → 坦克实际是 `MasterAI`，过滤失效。

**正确做法（坦克大乱斗 SuperBuff 拾取范例）**：
```csharp
// ❌ 错误：用 AI 类型过滤，遗漏 MasterAI 的坦克
if (gpo.GetGPOType() != GPOData.GPOType.AI) continue;

// ✅ 正确：只排除不需要的类型（SceneElement），其余均保留
if (gpo.GetGPOType() == GPOData.GPOType.SceneElement) continue;
```

**生成方式决定 GPOType**：
- `AddMasterAI`（`SM_AI.Event_AddMasterAI`）→ `GPOType.MasterAI`
- `AddAI`（`SM_AI.Event_AddAI`）→ `GPOType.AI`
- 场景放置的 SceneGPOEntity → `GPOType.SceneElement`

---

## 四点六、载具模式架构：角色与载具 GPO 同坐标问题（2026-03-27 沉淀）

> **适用场景**：任何"玩家角色骑乘/驾驶载具（坦克/载具等）"的实现模式

### 架构说明

坦克大乱斗中，玩家驾驶坦克时实际上存在**两个 GPO**：

| GPO | 类型 | 状态 | 说明 |
|-----|------|------|------|
| 角色 GPO（Role、RoleAI） | `GPOType.Role、GPOType.RoleAI` | **HideEntity = true**（隐藏） | 玩家的真实 GPO，隐藏在坦克下 |
| 坦克 GPO（MasterAI） | `GPOType.MasterAI` | 可见，正常运动 | 玩家实际操控的载具 |

两个 GPO 的**坐标几乎相同**（角色 GPO 跟随坦克移动）。

### 对范围检测的影响

任何基于坐标进行的范围检测（如 Buff 拾取、AOE 伤害、区域触发）如果直接遍历 `SM_GPO.GetGPOList` 中的所有 GPO，**会同时命中角色和坦克两个 GPO**。

**必须加 HideEntity 过滤**：

```csharp
// ✅ 正确：排除隐藏状态（角色在载具内部时 HideEntity=true）
if (gpo.HasTag(GamePlayTagData.TagEnum.HideEntity)) continue;
```

### 完整过滤链路（SuperBuff 拾取范例）

```csharp
if (gpo.GetGpoID() == iGPO.GetGpoID()) continue;                       // 排除自身
if (gpo.GetGPOType() == GPOData.GPOType.SceneElement) continue;         // 排除场景元素
if (gpo.HasTag(GamePlayTagData.TagEnum.HideEntity)) continue;            // 排除隐藏状态角色
// 此时剩余的 GPO 才是真正可见的、可交互的单位
```

### ReLife vs UpHP 区别（顺带沉淀）

| 事件 | 适用场景 | 说明 |
|------|---------|------|
| `SE_GPO.Event_ReLife` | **死亡后复活** | 会清除 isDead 标记，再调 UpHP；对存活 GPO 调用行为不确定 |
| `SE_GPO.Event_UpHP` | **直接加血**（含满血回复） | 安全，随时可调，Buff 拾取等场景用这个 |

---

## 五、常用可复用组件（避免重复造轮子）

| 需求 | 优先复用 | 挂载方式 |
|------|---------|---------|
| 炮台/固定单位贴地 | `ServerTurretSetToGround` | AddComponent |
| 视野内自动寻敌 | `ServerAIFindInsightTarget` | AddComponent + InitData |
| 随移动平台移动 | `ServerAIMovingPlatformTargetMove` | AddComponent |
| 计时消亡 | `ServerSummonedAILifeTime` | AddComponent |
| 行为树伤害倍率 | `ServerAIPlayAbilityByBehaviourLevel` | AddComponent |

---

## 六、GPO Component 编码规范

> **完整规范见 `core-rules.md §第二章 Rule 1-4`**，适用于所有 GPO Component（PGC + UGC）。核心三条摘要：

- **C-1**（Rule 2）：Component 所有成员一律 `private`，仅继承自基类的生命周期函数保留 `protected override`
- **C-2**（Rule 3）：外部参数通过 `InitData` struct 注入（`OnStart` 中读取），**禁止** public Init 方法
- **C-3**（Rule 4 / Rule 13）：`AddUpdate` 必须在 `OnSetEntityObj` 中注册，**禁止**在 `OnAwake` / `OnStart` 中调用

---

## 六点五、AI GPO 血量注意事项（ServerAIAttribute）

**每个需要 HP 的 AI GPO，必须在 `AddComponents()` 中显式添加 `ServerAIAttribute`。**

`S_AI_Base.AddComponents()` 默认**不包含**任何属性组件，不添加则无 `Event_DownHP` 监听者，HP 永远不减。

```csharp
protected override void AddComponents() {
    base.AddComponents();  // ✅ 必须首行调用
    // ✅ 必须显式添加，否则受击无效果
    AddComponent<ServerAIAttribute>(new ServerGPOAttribute.InitData {
        MaxHp = useMData.GetHp()
    });
}
```

---

## 七、SceneGPO 开发

> SceneGPO（基地/可破坏掩体/触发区域/Buff刷新点）的详细规范已抽离至独立文件。  
> **开发 SceneGPO 时必须加载**：[[gpo-code-scenegpo]]

**速查**：SceneGPO 所有 GPOM 共用 `Id_BaseSceneGpo`（框架硬编码），自定义属性（HP等）通过 `SceneGPOBase` 子类字段实现；服务端场景 Layer 必须为 `ServerLayer`（Layer 8）。

---

## 八、⚠️ 新建 GPO 完成后必须执行：更新功能清单（强制）

> **此步骤不可跳过**，与提交代码同等优先级。

当任意新 GPO 类型开发完成并通过[项目负责人] Round 3 审核后，**GPO 工程师必须立即**在以下文件的"项目已有 GPO 功能清单"表格末尾追加新条目：

**目标文件**：[[GPO_Programmer]]（末尾"📦 项目已有 GPO 功能清单"章节）

**追加格式**：
```
| `Id_XXX` | `ServerAIXXXSystem` | `ClientAIXXXSystem` | [一句话功能描述] | [类型：AI怪物/AI Boss/炮台/场景物件/召唤单位/训练用/生成器/功能单位] |
```

**检查项（完成前自查）**：
- [ ] `GpoTypeSet.Id_XXX` 常量名与表格 ID 列一致
- [ ] Server 和 Client 系统类名填写准确
- [ ] 类型分类与现有条目保持一致
- [ ] 表格追加在现有最后一行之后（不替换已有内容）

> **违反此规则的代价**：下一个开发同类功能的 Agent 无法发现已有实现，导致重复造轮子。
> **[项目负责人]注意**：Round 3 验收前，检查 GPO_Programmer.md 功能清单是否已更新，未更新不得通过。

---

## 九、客户端 Attribute 组件选择

> `ClientAIAttribute` 强转 `InData`，若服务端未设置 `OR_InData` 则 NullReferenceException。

| 条件 | 使用组件 |
|------|---------|
| 服务端设置了 `OR_InData` | `ClientAIAttribute` |
| 服务端**未设置** `OR_InData` | `ClientGPOAttribute` ⚠️ |

**快速判断**：服务端 OnStart/生成代码中有 `OR_InData = new ...` → 用 `ClientAIAttribute`；没有 → 用 `ClientGPOAttribute`。

---

## 十、AI 死亡位置捕获

> **禁止 Update 轮询** `IsClear()` 来获取死亡位置——GPO 清除后 `GetPoint()` 返回 `Vector3.zero`。

**正确方式**：在召唤 `OR_CallBack` 中注册 `SE_GPO.Event_SetIsDead`，于 GPO 清除前读取位置：

```csharp
OR_CallBack = (IGPO ai) => {
    ai.MsgRegister.Register<SE_GPO.Event_SetIsDead>(evt => {
        Vector3 deathPos = ai.GetPoint();          // ✅ 此时 GPO 尚存，位置可读
        ai.MsgRegister.Unregister<SE_GPO.Event_SetIsDead>(...);
    });
}
```

**时序**：`SE_GPO.Event_SetIsDead` → ServerAIDead.OnDead → `SM_AI.Event_RemoveAI`（清除）。事件在清除前触发。

---

## 十一、IGPO 接口限制与跨 GPO 查询

> `IGPO` 是数据接口，**不能反向获取 System**（不存在 `GetGPO()` 反向方法，强转编译失败）。

| 需求 | 正确方式 |
|------|---------|
| 判断 GPO 类型 | `gpo.GetMData().GetSign()` 与常量比较 |
| 获取 GPO 的 Master | `gpo.Dispatcher(new SE_AI.Event_GetMasterGPO { CallBack = m => master = m })` |
| 获取同类 GPO 数量 | 遍历 `aiSystem.GPOList`，用 `GetMData().GetSign()` 过滤 |

**`SE_AI.Event_GetMasterGPO` 是同步事件**（`ServerAIMaster` 处理，回调同帧触发），可在 foreach 循环中安全使用。

**自组织 Slot 公式**（同类 GPO 居中排列，如悬浮武器；适用于数量有上限的场景）：
```
slotIndex = 同类 + 同Master 且 GpoId < 自身 的数量
offsetX   = (slotIndex - (totalCount - 1) * 0.5f) * SlotSpacing
```
