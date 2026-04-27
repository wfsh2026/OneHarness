# BIU26-怪物GPO系统 技术文档

> **文档版本**：v1.1
> **创建时间**：2026-04-01
> **负责 Agent**：开发负责人 (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：[[BIU26_开发计划]]
> **状态**：⬜ 待开发（交由 GPO 工程师实现）

---

## 参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| 开发负责人 (DL) | 开发范例 | GPO 参考范例.md（BIU26FloatingWeapon 格式） | `Assets/Scripts/Template/gpo/GPOM_BIU26Set.cs` |
| 开发负责人 (DL) | 边界定义 | BIU26怪物设计.md（策划需求，无独立边界定义文件） | [[BIU26怪物设计]] |
| 开发负责人 (DL) | 规则 | AIGC 会话调度规范.md | `aigc/harness/rules/AIGC 会话调度规范.md` |
| 开发负责人 (DL) | 规则 | safety-rules.md | [[safety-rules]] |
| 开发负责人 (DL) | 规则 | core-rules.md | [[GamePlay_Dev/core-rules]] |
| 开发负责人 (DL) | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| 开发负责人 (DL) | 规则 | plan-doc.md | [[plan-doc]] |
| 开发负责人 (DL) | 规则 | gpo-code.md | [[gpo-code]] |

---

## 一、S-03 功能需求

**玩家体验**：在 BIU26 发育 + 缩圈 PVP 全程，怪物随玩家打怪行为和圈阶自然进化——普通的白灰小怪在第1圈收缩后进化为发蓝光的精英怪，第2圈后进化为金色轮廓的头目怪；所有档位怪物在靠近玩家（≤1.5m）时会持续造成接触伤害，让"积极割草清场"产生可见的难度差异。

---

## 二、S-04 功能定位

**职责边界**：本文档解决"BIU26三档怪物的GPO数据层、服务端行为层、客户端表现层、进化机制和近身伤害组件"的完整实现方案，覆盖从配表注册到 Prefab 占位的全链路，**不涉及**行为类型区分（冲锋/群涌/远程/坦克，Phase 3 实现）和元素属性（Phase 3 实现）。

---

## 三、S-05 文件清单

### 📋 配表层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Template/data/Gpo.cs` | **修改**（手动追加，非 csv-gen） | ① 修改 Id=102 行：GpoType 从 9→32，AssetSign 从 "Character"→"BIU26Minion_Normal"；② 追加 `new Gpo(104, 33, "BIU26精英怪", "BIU26_Minion_Elite", "BIU26Minion_Elite", "")`；③ 追加 `new Gpo(105, 34, "BIU26头目怪", "BIU26_Minion_Boss", "BIU26Minion_Boss", "")`；④ 追加常量 `Id_BIU26Minion_Elite=104` 和 `Id_BIU26Minion_Boss=105` |
| `Assets/Scripts/Template/data/GpoType.cs` | **修改**（手动追加，非 csv-gen） | 追加三个常量和 Data 行：`Id_BIU26Minion_Normal=32`、`Id_BIU26Minion_Elite=33`、`Id_BIU26Minion_Boss=34`；同步追加 `new GpoType(32/33/34, ...)` |
| `Assets/Scripts/Template/gpo/GPOM_BIU26MinionSet.cs` | **新建**（手动编写，非 csv-gen） | 包含三个 struct（`GPOM_BIU26Minion_Normal`/`Elite`/`Boss`）+ 对应 Set 静态类，字段含 Hp/Atk/MoveSpeedMultiplier |
| `Assets/Scripts/Template/gpo/IGPOM.cs` | **修改** | GetGPOMData switch 追加三个 case：`GpoTypeSet.Id_BIU26Minion_Normal`/`Elite`/`Boss` |

### 🔀 路由注册层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/ServerAIWorld_Switch.cs` | **修改** | AddAIForGpoMTypeId switch 追加三个 case → `ServerBIU26MinionNormalSystem`/`EliteSystem`/`BossSystem` |
| `Assets/Scripts/GamePlay/Client/AI/ClientAIWorld_Switch.cs` | **修改** | 同上，映射 → `ClientBIU26MinionSystem`（三档共用一个客户端 System） |

### 🖥️ 服务端 System 层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26MinionNormalSystem.cs` | **新建** | 继承 `S_AI_Base`，OnAwake 强转 `GPOM_BIU26Minion_Normal`，AddComponents 挂载 `ServerBIU26MinionContactDamage`（ATK=10, Radius=1.5m） |
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26MinionEliteSystem.cs` | **新建** | 继承 `S_AI_Base`，OnAwake 强转 `GPOM_BIU26Minion_Elite`，挂载 `ServerBIU26MinionContactDamage`（ATK=15, Radius=1.5m） |
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26MinionBossSystem.cs` | **新建** | 继承 `S_AI_Base`，OnAwake 强转 `GPOM_BIU26Minion_Boss`，挂载 `ServerBIU26MinionContactDamage`（ATK=22, Radius=1.5m） |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionContactDamage.cs` | **新建** | 继承 `ServerNetworkComponentBase`；每 0.5s 扫范围内 GPOType.Role GPO，对 ≤1.5m 内玩家造成 `(DamagePerSec × 0.5f)` 点伤害 |
| `Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs` | **修改** | 追加 `Event_ZoneShrinkPhaseStarted { int Phase }` 事件（由 ServerBIU26ZoneSystem 广播） |
| `Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26MinionsSpawner.cs` | **修改** | 注册监听 `SE_BIU26.Event_ZoneShrinkPhaseStarted`；Phase==1 时对 30-40% 普通怪执行 RemoveAI+AddAI（升为精英）；Phase==2 时对 30-40% 精英怪执行升级为头目 |

### 💻 客户端 System 层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26MinionSystem.cs` | **新建** | 继承 `C_AI_Base`，AddComponents 先调 base，OnStart 调 `CreateEntity(MData.AssetSign)` — 三档均用此 System，通过 AssetSign 区分 Prefab |

### 🎨 资产层（必须，灰盒阶段）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Bundle/GamePlay/AI/Server/BIU26MinionServer.prefab` | **新建** | 服务端 Capsule 占位，含 CapsuleCollider (r=0.3, h=1.0)，无 Renderer |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Normal.prefab` | **新建** | 灰白 Capsule，Scale (1,1,1)，挂载 BIU26Minion_Normal_Mat |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Elite.prefab` | **新建** | 蓝色 Capsule，Scale (1.4, 1.4, 1.4)，挂载 BIU26Minion_Elite_Mat |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Boss.prefab` | **新建** | 金色 Capsule，Scale (1.8, 1.8, 1.8)，挂载 BIU26Minion_Boss_Mat |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Normal_Mat.mat` | **新建** | URP/Lit，_BaseColor (0.85, 0.85, 0.85, 1)，无 Emission |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Elite_Mat.mat` | **新建** | URP/Lit，_BaseColor (0.3, 0.5, 1.0, 1)，Emission Color (0.3, 0.5, 1.0) × 2 |
| `Assets/Bundle/GamePlay/AI/Client/BIU26Minion_Boss_Mat.mat` | **新建** | URP/Lit，_BaseColor (1.0, 0.7, 0.1, 1)，Emission Color (1.0, 0.7, 0.1) × 3 |

---

## 四、S-06 ASCII 交互链路图

### 4.1 全系统初始化流程

```
[ServerBIU26Mode.OnStart()]
        │
        ▼
[SM_AI.Event_AddAI] → Sign="BIU26Spawner"
        │  极坐标刷怪器生成
        ▼
[ServerBIU26SpawnerSystem.AddComponents()]
        │  挂载 ServerBIU26MinionsSpawner
        │  MinionSign = "BIU26_Minion_Normal"
        ▼
[ServerBIU26MinionsSpawner.OnStart()]
        │  注册 SE_BIU26.Event_ZoneShrinkPhaseStarted
        ▼
[每 SpawnInterval 秒刷出普通怪]
        │  SM_AI.Event_AddAI → Sign="BIU26_Minion_Normal"
        ▼
[ServerAIWorld_Switch : case Id_BIU26Minion_Normal]
        │
        ▼
[ServerBIU26MinionNormalSystem.OnAwake()]
        │  AddComponent<ServerBIU26MinionContactDamage>({ATK=10, Radius=1.5m})
        │  base.AddComponents() → ServerAIHateTarget, ServerAIHurt, ServerAIDead 等
        ▼
[OnStart()] → CreateEntity("BIU26MinionServer")
        │  服务端 Capsule 实体激活
        ▼
[RPC 通知客户端] → ClientAIWorld_Switch : case Id_BIU26Minion_Normal
        │
        ▼
[ClientBIU26MinionSystem.OnStart()]
        │  CreateEntity("BIU26Minion_Normal")  ← 灰白 Capsule Prefab
        ▼
[怪物运行中]
```

### 4.2 近身持续掉血链路

```
[ServerBIU26MinionContactDamage.OnUpdate(dt)]
        │  _timer += dt
        │  if _timer < 0.5f → 跳过
        │  _timer = 0f
        ▼
[遍历 SM_GPO.GetGPOList()]
        │  过滤：GPOType != Role → continue
        │  过滤：Distance > ContactRadius → continue
        ▼
[每个满足条件的玩家 GPO]
        │  gpo.Dispatcher(new SE_GPO.Event_Hurt { ... })
        │  伤害值 = DamagePerSec × 0.5f（每 0.5s tick）
        ▼
[玩家扣血 + 飘血表现（由现有 ServerAIHurt 机制处理）]
```

### 4.3 进化机制链路（第1圈为例）

```
[ServerBIU26ZoneSystem]
        │  第1圈开始收缩
        │  MsgRegister.Dispatcher(new SE_BIU26.Event_ZoneShrinkPhaseStarted { Phase = 1 })
        ▼
[ServerBIU26MinionsSpawner（已注册监听）]
        │  evt.Phase == 1 → EvolveNormalToElite()
        ▼
[EvolveNormalToElite()]
        │  取存活普通怪列表 _normalMinionList
        │  随机取 30-40%（Mathf.RoundToInt(count × Random.Range(0.3f, 0.4f))）
        │  foreach selected:
        │     recordPos = gpo.GetPoint()
        │     SM_AI.Event_RemoveAI → 移除该普通怪 GPO
        │     SM_AI.Event_AddAI → Sign="BIU26_Minion_Elite"，Position=recordPos
        ▼
[ServerAIWorld_Switch : case Id_BIU26Minion_Elite]
        │
        ▼
[ServerBIU26MinionEliteSystem（HP=1250, ATK=15）]
        │  客户端收到 → CreateEntity("BIU26Minion_Elite")  ← 蓝色 1.4x Capsule
        ▼
[视觉：蓝色发光大型 Capsule 替换原灰白小 Capsule]
```

---

## 五、S-07 灰盒资源占位

| 档位 | 形状 | 颜色（_BaseColor RGBA） | 尺寸（Scale×基础Capsule） | 基础 Capsule 参数 | Emission | 挂点偏移 |
|------|------|----------------------|-------------------------|-----------------|---------|---------|
| 普通怪 | Capsule | (0.85, 0.85, 0.85, 1) 灰白 | Scale (1, 1, 1)，实际约 0.6m×1.8m | r=0.3m, h=1.8m | 无 | (0, 0, 0) 根节点 |
| 精英怪 | Capsule | (0.3, 0.5, 1.0, 1) 蓝 | Scale (1.4, 1.4, 1.4)，实际约 0.84m×2.52m | r=0.3m, h=1.8m | (0.3, 0.5, 1.0) × Intensity 2 | (0, 0, 0) 根节点 |
| 头目怪 | Capsule | (1.0, 0.7, 0.1, 1) 金 | Scale (1.8, 1.8, 1.8)，实际约 1.08m×3.24m | r=0.3m, h=1.8m | (1.0, 0.7, 0.1) × Intensity 3 | (0, 0, 0) 根节点 |

> ⚠️ 客户端 Prefab Scale 在 Prefab 根节点设置，不通过代码修改 Transform.localScale（保持与 S_AI_Base 的 EntityObj 生命周期一致）。

---

## 六、S-08 边界条件

### 6.1 依赖的外部接口

| 接口 | 来源 | 说明 |
|------|------|------|
| `SM_AI.Event_AddAI` | AIWorld 框架 | 生成/进化替换时使用；Sign 必须与 Gpo.cs Data 行完全匹配 |
| `SM_AI.Event_RemoveAI` | AIWorld 框架 | 进化替换时先移除旧 GPO |
| `SE_GPO.Event_Hurt` | GPO 框架 | 近身伤害发送；需确认 ServerAIHurt 参数格式（FuncID / ATK 传参方式） |
| `SE_BIU26.Event_ZoneShrinkPhaseStarted` | 本文档新增，由 ServerBIU26ZoneSystem 发送 | Phase=1 触发普通→精英进化；Phase=2 触发精英→头目进化 |
| `SM_GPO.GetGPOList()` 或 `aiSystem.GPOList` | GPO 框架 | 近身伤害扫描玩家时使用；过滤 GPOType.Role |
| `ServerAIWorld_Switch.AddAIForGpoMTypeId` | AIWorld 框架 | 路由注册，已有 case 格式参考 Id_BIU26WeaponPickup |
| `ClientAIWorld_Switch` | AIWorld 框架 | 客户端路由注册，同上 |

### 6.2 禁止做的事

| 禁止项 | 原因 |
|-------|------|
| **禁止**在进化时不先 RemoveAI 直接修改现有 GPO 的 GPOM 数据 | GPO 框架 GPOM 为只读 struct，进化必须走 RemoveAI→AddAI 替换路径 |
| **禁止**在 ContactDamage 组件的 OnUpdate 中每帧扫描（应 0.5s 节流） | 避免多只怪同帧扫描造成服务端性能峰值 |
| **禁止**在 GPOM_BIU26MinionSet.cs 中放游戏业务常量（如进化比例 0.3~0.4） | 业务常量属于 ServerBIU26MinionsSpawner 或 ServerBIU26Mode，不属于 GPOM 数据层 |
| **禁止**复用 GpoTypeSet.Id_Character=9 作为三档怪物的类型 | Id=102 原先用 Type=9 走 CharacterAI 路由，必须迁移到新专属 GpoType，否则无法使用专属行为组件 |
| **禁止** ClientBIU26MinionSystem 不调用 base.AddComponents() 就自行处理 | S_AI_Base / C_AI_Base 基类已有 ServerAIDead/Hurt 等必要组件 |
| **禁止**服务端 MinionServer.prefab 挂载 MeshRenderer / Light | 服务端 Prefab 只包含碰撞体和逻辑节点 |
| **禁止**在 ServerBIU26MinionsSpawner 进化方法中使用 Update 轮询 IsClear() 判断死亡 | 参见 gpo-code.md §十 AI 死亡位置捕获规范 |

### 6.3 边界文档引用

- [[gpo-code]] — GPO 开发完整规范
- [[BIU26怪物设计]] — 三档数值、进化比例、视觉规格

---

## 七、S-01 配表注册详细规格

### 7.1 GpoType.cs 追加（3 行）

```csharp
// GpoTypeSet 常量（追加在 Id_BIU26WeaponPickup=31 之后）
public const int Id_BIU26Minion_Normal = 32;
public const int Id_BIU26Minion_Elite  = 33;
public const int Id_BIU26Minion_Boss   = 34;

// Data 数组追加（在 BIU26WeaponPickup 行之后）
, new GpoType( 32, "BIU26普通怪", "BIU26Minion_Normal" )
, new GpoType( 33, "BIU26精英怪", "BIU26Minion_Elite" )
, new GpoType( 34, "BIU26头目怪", "BIU26Minion_Boss" )
```

### 7.2 Gpo.cs 修改（1 行修改 + 2 行追加）

```csharp
// ① 修改现有 Id=102 行（GpoType 9→32，AssetSign "Character"→"BIU26Minion_Normal"）
// 原行：new Gpo( 102, 9, "BIU26普通小怪", "BIU26_Minion_Normal", "Character", "" )
new Gpo( 102, 32, "BIU26普通小怪", "BIU26_Minion_Normal", "BIU26Minion_Normal", "" )

// ② 追加常量（在 Id_BIU26WeaponPickup=103 之后）
public const int Id_BIU26Minion        = 102;   // ← 已存在，保留
public const int Id_BIU26Minion_Elite  = 104;   // ← 新增
public const int Id_BIU26Minion_Boss   = 105;   // ← 新增

// ③ Data 数组追加
, new Gpo( 104, 33, "BIU26精英怪", "BIU26_Minion_Elite",  "BIU26Minion_Elite",  "" )
, new Gpo( 105, 34, "BIU26头目怪", "BIU26_Minion_Boss",   "BIU26Minion_Boss",   "" )
```

---

## 八、核心代码骨架

### 8.1 GPOM_BIU26MinionSet.cs（新建）

```csharp
// Assets/Scripts/Template/gpo/GPOM_BIU26MinionSet.cs
// 手工编写，非 csv-gen。格式参照 GPOM_BIU26Set.cs（FloatingWeapon）

namespace Sofunny.BiuBiuBiu2.Template {

    // ─── 普通怪 struct ───────────────────────────────────────────────────
    public struct GPOM_BIU26Minion_Normal : IGPOM {
        public readonly string AssetSign    { get; }
        public readonly int    Atk          { get; }  // 近身伤害/秒
        public readonly float  ContactRadius{ get; }  // 近身判定半径（m）
        public readonly int[]  GpoDropId    { get; }
        public readonly ushort GpoDropType  { get; }
        public readonly string GpoSoConfig  { get; }
        public readonly int[]  GpoTag       { get; }
        public readonly int    GpoType      { get; }
        public readonly int    Hp           { get; }
        public readonly int    Id           { get; }
        public readonly int    MatchMode    { get; }
        public readonly float  MoveSpeedMultiplier { get; }  // 移速倍率（普通=1.0）
        public readonly string Name         { get; }
        public readonly byte   Quality      { get; }
        public readonly string Sign         { get; }

        // GetXXX() 方法同 GPOM_BIU26FloatingWeapon，直接 return 字段
        public string GetAssetSign()   => AssetSign;
        public int[]  GetGpoDropId()   => GpoDropId;
        public ushort GetGpoDropType() => GpoDropType;
        public string GetGpoSoConfig() => GpoSoConfig;
        public int[]  GetGpoTag()      => GpoTag;
        public int    GetGpoType()     => GpoType;
        public int    GetId()          => Id;
        public int    GetMatchMode()   => MatchMode;
        public string GetName()        => Name;
        public byte   GetQuality()     => Quality;
        public string GetSign()        => Sign;

        public GPOM_BIU26Minion_Normal(
            string assetSign, int atk, float contactRadius,
            int[] gpoDropId, ushort gpoDropType, string gpoSoConfig,
            int[] gpoTag, int gpoType, int hp, int id, int matchMode,
            float moveSpeedMultiplier, string name, byte quality, string sign)
        {
            AssetSign            = assetSign;
            Atk                  = atk;
            ContactRadius        = contactRadius;
            GpoDropId            = gpoDropId;
            GpoDropType          = gpoDropType;
            GpoSoConfig          = gpoSoConfig;
            GpoTag               = gpoTag;
            GpoType              = gpoType;
            Hp                   = hp;
            Id                   = id;
            MatchMode            = matchMode;
            MoveSpeedMultiplier  = moveSpeedMultiplier;
            Name                 = name;
            Quality              = quality;
            Sign                 = sign;
        }
    }

    public static class GPOM_BIU26Minion_NormalSet {
        public const int    Id_BIU26Minion_Normal   = 102;
        public const string Sign_BIU26Minion_Normal  = "BIU26_Minion_Normal";

        public static readonly GPOM_BIU26Minion_Normal[] Data;

        static GPOM_BIU26Minion_NormalSet() {
            Data = new GPOM_BIU26Minion_Normal[] {
                // assetSign, atk, contactRadius, gpoDropId, gpoDropType, gpoSoConfig,
                // gpoTag, gpoType(=32), hp(=500), id(=102), matchMode, moveSpeedMul(=1.0f), name, quality, sign
                new GPOM_BIU26Minion_Normal(
                    "BIU26Minion_Normal", 10, 1.5f,
                    new int[]{}, 0, "",
                    new int[]{}, 32, 500, 102, 0,
                    1.0f, "BIU26普通怪", 1, "BIU26_Minion_Normal")
            };
        }

        public static GPOM_BIU26Minion_Normal GetGPOMByIdAndMatchMode(int id, int matchMode = 0) {
            foreach (var data in Data)
                if (data.Id == id && data.MatchMode == matchMode) return data;
            return default;
        }
    }

    // ─── 精英怪 struct（字段与 Normal 完全相同，数值不同）──────────────────
    public struct GPOM_BIU26Minion_Elite : IGPOM {
        // 字段声明同 GPOM_BIU26Minion_Normal（完全复制，GPO 工程师实现时展开）
        public readonly string AssetSign;
        public readonly int    Atk;
        public readonly float  ContactRadius;
        public readonly int[]  GpoDropId;
        public readonly ushort GpoDropType;
        public readonly string GpoSoConfig;
        public readonly int[]  GpoTag;
        public readonly int    GpoType;
        public readonly int    Hp;
        public readonly int    Id;
        public readonly int    MatchMode;
        public readonly float  MoveSpeedMultiplier;
        public readonly string Name;
        public readonly byte   Quality;
        public readonly string Sign;
        // GetXXX() 同 Normal
        public string GetAssetSign()   => AssetSign;
        public int[]  GetGpoDropId()   => GpoDropId;
        public ushort GetGpoDropType() => GpoDropType;
        public string GetGpoSoConfig() => GpoSoConfig;
        public int[]  GetGpoTag()      => GpoTag;
        public int    GetGpoType()     => GpoType;
        public int    GetId()          => Id;
        public int    GetMatchMode()   => MatchMode;
        public string GetName()        => Name;
        public byte   GetQuality()     => Quality;
        public string GetSign()        => Sign;
        // 构造函数同 Normal（参数列表相同，GPO 工程师实现时展开）
        public GPOM_BIU26Minion_Elite(
            string assetSign, int atk, float contactRadius,
            int[] gpoDropId, ushort gpoDropType, string gpoSoConfig,
            int[] gpoTag, int gpoType, int hp, int id, int matchMode,
            float moveSpeedMultiplier, string name, byte quality, string sign)
        { AssetSign=assetSign; Atk=atk; ContactRadius=contactRadius; GpoDropId=gpoDropId;
          GpoDropType=gpoDropType; GpoSoConfig=gpoSoConfig; GpoTag=gpoTag; GpoType=gpoType;
          Hp=hp; Id=id; MatchMode=matchMode; MoveSpeedMultiplier=moveSpeedMultiplier;
          Name=name; Quality=quality; Sign=sign; }
    }

    public static class GPOM_BIU26Minion_EliteSet {
        public const int    Id_BIU26Minion_Elite   = 104;
        public const string Sign_BIU26Minion_Elite  = "BIU26_Minion_Elite";

        public static readonly GPOM_BIU26Minion_Elite[] Data;

        static GPOM_BIU26Minion_EliteSet() {
            Data = new GPOM_BIU26Minion_Elite[] {
                // hp=1250(500×2.5), atk=15, moveSpeed=0.9f(-10%), gpoType=33, id=104
                new GPOM_BIU26Minion_Elite(
                    "BIU26Minion_Elite", 15, 1.5f,
                    new int[]{}, 0, "",
                    new int[]{}, 33, 1250, 104, 0,
                    0.9f, "BIU26精英怪", 2, "BIU26_Minion_Elite")
            };
        }

        public static GPOM_BIU26Minion_Elite GetGPOMByIdAndMatchMode(int id, int matchMode = 0) {
            foreach (var data in Data)
                if (data.Id == id && data.MatchMode == matchMode) return data;
            return default;
        }
    }

    // ─── 头目怪 struct（数值不同：HP=3000, ATK=22, 移速×0.8）───────────────
    public struct GPOM_BIU26Minion_Boss : IGPOM {
        public readonly string AssetSign;
        public readonly int    Atk;
        public readonly float  ContactRadius;
        public readonly int[]  GpoDropId;
        public readonly ushort GpoDropType;
        public readonly string GpoSoConfig;
        public readonly int[]  GpoTag;
        public readonly int    GpoType;
        public readonly int    Hp;
        public readonly int    Id;
        public readonly int    MatchMode;
        public readonly float  MoveSpeedMultiplier;
        public readonly string Name;
        public readonly byte   Quality;
        public readonly string Sign;
        public string GetAssetSign()   => AssetSign;
        public int[]  GetGpoDropId()   => GpoDropId;
        public ushort GetGpoDropType() => GpoDropType;
        public string GetGpoSoConfig() => GpoSoConfig;
        public int[]  GetGpoTag()      => GpoTag;
        public int    GetGpoType()     => GpoType;
        public int    GetId()          => Id;
        public int    GetMatchMode()   => MatchMode;
        public string GetName()        => Name;
        public byte   GetQuality()     => Quality;
        public string GetSign()        => Sign;
        public GPOM_BIU26Minion_Boss(
            string assetSign, int atk, float contactRadius,
            int[] gpoDropId, ushort gpoDropType, string gpoSoConfig,
            int[] gpoTag, int gpoType, int hp, int id, int matchMode,
            float moveSpeedMultiplier, string name, byte quality, string sign)
        { AssetSign=assetSign; Atk=atk; ContactRadius=contactRadius; GpoDropId=gpoDropId;
          GpoDropType=gpoDropType; GpoSoConfig=gpoSoConfig; GpoTag=gpoTag; GpoType=gpoType;
          Hp=hp; Id=id; MatchMode=matchMode; MoveSpeedMultiplier=moveSpeedMultiplier;
          Name=name; Quality=quality; Sign=sign; }
    }

    public static class GPOM_BIU26Minion_BossSet {
        public const int    Id_BIU26Minion_Boss   = 105;
        public const string Sign_BIU26Minion_Boss  = "BIU26_Minion_Boss";

        public static readonly GPOM_BIU26Minion_Boss[] Data;

        static GPOM_BIU26Minion_BossSet() {
            Data = new GPOM_BIU26Minion_Boss[] {
                // hp=3000(500×6), atk=22, moveSpeed=0.8f(-20%), gpoType=34, id=105
                new GPOM_BIU26Minion_Boss(
                    "BIU26Minion_Boss", 22, 1.5f,
                    new int[]{}, 0, "",
                    new int[]{}, 34, 3000, 105, 0,
                    0.8f, "BIU26头目怪", 3, "BIU26_Minion_Boss")
            };
        }

        public static GPOM_BIU26Minion_Boss GetGPOMByIdAndMatchMode(int id, int matchMode = 0) {
            foreach (var data in Data)
                if (data.Id == id && data.MatchMode == matchMode) return data;
            return default;
        }
    }
}
```

### 8.2 IGPOM.cs 追加（switch case）

```csharp
// 在 GetGPOMData() switch 中追加（在 BIU26WeaponPickup case 之后）：
case GpoTypeSet.Id_BIU26Minion_Normal:
    mData = GPOM_BIU26Minion_NormalSet.GetGPOMByIdAndMatchMode(gpoId, matchMode);
    break;
case GpoTypeSet.Id_BIU26Minion_Elite:
    mData = GPOM_BIU26Minion_EliteSet.GetGPOMByIdAndMatchMode(gpoId, matchMode);
    break;
case GpoTypeSet.Id_BIU26Minion_Boss:
    mData = GPOM_BIU26Minion_BossSet.GetGPOMByIdAndMatchMode(gpoId, matchMode);
    break;
```

### 8.3 ServerBIU26MinionNormalSystem.cs（代表性骨架，Elite/Boss 同理）

```csharp
// Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26MinionNormalSystem.cs
using Sofunny.BiuBiuBiu2.Template;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26MinionNormalSystem : S_AI_Base {
        private GPOM_BIU26Minion_Normal _useMData;

        protected override void OnAwake() {
            base.OnAwake();
            _useMData = (GPOM_BIU26Minion_Normal)MData;
            AddComponents();
        }

        protected override void AddComponents() {
            base.AddComponents();  // 必须先调 base：ServerAIDead/Hurt/HateTarget 等

            // 近身持续掉血
            AddComponent<ServerBIU26MinionContactDamage>(
                new ServerBIU26MinionContactDamage.InitData {
                    DamagePerSec  = _useMData.Atk,          // 10 HP/s
                    ContactRadius = _useMData.ContactRadius  // 1.5m
                });
        }

        protected override void OnStart() {
            base.OnStart();
            CreateEntity(_useMData.Sign + "Server");  // → "BIU26_Minion_NormalServer"
        }
    }
}
```

> **Elite / Boss System** 代码结构完全相同，仅强转类型为 `GPOM_BIU26Minion_Elite` / `GPOM_BIU26Minion_Boss`，并将 `CreateEntity` 的参数对应更新。

### 8.4 ServerBIU26MinionContactDamage.cs（骨架）

```csharp
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionContactDamage.cs

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26MinionContactDamage : ServerNetworkComponentBase {

        public struct InitData {
            public int   DamagePerSec;
            public float ContactRadius;
        }

        private int   _dmgPerSec;
        private float _radius;
        private float _tickInterval = 0.5f;
        private float _timer;

        protected override void OnInit(object initData) {
            var data = (InitData)initData;
            _dmgPerSec = data.DamagePerSec;
            _radius    = data.ContactRadius;
        }

        protected override void OnUpdate(float dt) {
            _timer += dt;
            if (_timer < _tickInterval) return;
            _timer = 0f;

            var selfPos  = iGPO.GetPoint();
            float dmgTick = _dmgPerSec * _tickInterval;   // = ATK × 0.5

            // 遍历全部 GPO，找范围内的玩家
            // ⚠️ GPO 工程师实现时按项目实际 API 调整（SM_GPO.GetGPOList() 或 aiSystem.GPOList）
            foreach (var gpo in SM_GPO.GetGPOList()) {
                if (gpo.GetGPOType() != GPOData.GPOType.Role) continue;
                if (gpo.HasTag(GamePlayTagData.TagEnum.HideEntity)) continue;  // 排除隐藏态角色
                if (UnityEngine.Vector3.Distance(selfPos, gpo.GetPoint()) > _radius) continue;

                // 发送伤害事件（具体参数格式见 SE_GPO.Event_Hurt 定义）
                gpo.Dispatcher(new SE_GPO.Event_Hurt {
                    ATK    = (int)dmgTick,
                    Source = iGPO
                });
            }
        }
    }
}
```

### 8.5 SE_BIU26.cs 追加事件

```csharp
// 在 SE_BIU26.cs 中追加（放在 Event_MinionKilled 之后）：

/// <summary>
/// 缩圈阶段开始事件（由 ServerBIU26ZoneSystem 在对应圈开始收缩时广播）
/// Phase = 1 → 普通怪30-40%升级为精英；Phase = 2 → 精英怪30-40%升级为头目
/// </summary>
public class Event_ZoneShrinkPhaseStarted : IWorldEvent {
    public int Phase;
}
```

### 8.6 ServerBIU26MinionsSpawner.cs 进化逻辑补充（核心片段）

```csharp
// 在 OnStart() / OnAwake() 中注册进化事件监听
MsgRegister.Register<SE_BIU26.Event_ZoneShrinkPhaseStarted>(OnZoneShrinkPhaseStarted);

// ─────────────────────────────────────────────
private void OnZoneShrinkPhaseStarted(SE_BIU26.Event_ZoneShrinkPhaseStarted evt) {
    switch (evt.Phase) {
        case 1: EvolveMinions(_normalMinionList, "BIU26_Minion_Elite"); break;
        case 2: EvolveMinions(_eliteMinionList,  "BIU26_Minion_Boss");  break;
    }
}

/// <summary>
/// 从 sourceList 中随机取 30-40% 的存活怪，替换为 targetSign 的新 GPO
/// </summary>
private void EvolveMinions(List<IGPO> sourceList, string targetSign) {
    // 清理已死亡/清除的 GPO 引用
    sourceList.RemoveAll(gpo => gpo == null || gpo.IsClear());

    int total  = sourceList.Count;
    float ratio = UnityEngine.Random.Range(0.3f, 0.4f);
    int   count = UnityEngine.Mathf.RoundToInt(total * ratio);

    // Fisher-Yates 随机采样
    var shuffled = new List<IGPO>(sourceList);
    for (int i = shuffled.Count - 1; i > 0; i--) {
        int j = UnityEngine.Random.Range(0, i + 1);
        (shuffled[i], shuffled[j]) = (shuffled[j], shuffled[i]);
    }

    for (int i = 0; i < count && i < shuffled.Count; i++) {
        var gpo = shuffled[i];
        var spawnPos = gpo.GetPoint();  // ✅ RemoveAI 前读取位置

        // Step 1: 移除旧 GPO
        MsgRegister.Dispatcher(new SM_AI.Event_RemoveAI { GPO = gpo });
        sourceList.Remove(gpo);

        // Step 2: 在原位置生成新档位 GPO
        MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
            Sign     = targetSign,
            Position = spawnPos,
            // Master / TeamId 等按现有 SpawnMinion() 逻辑填充
        });
        // 注意：新生成的 GPO 会通过 OR_CallBack 回调，在回调中将其加入对应列表
    }
}

// ─────────────────────────────────────────────
// 在 SpawnMinion() 的 OR_CallBack 中，根据 Sign 分类存入对应列表：
OR_CallBack = (IGPO ai) => {
    var sign = ai.GetMData().GetSign();
    if      (sign == "BIU26_Minion_Normal") _normalMinionList.Add(ai);
    else if (sign == "BIU26_Minion_Elite")  _eliteMinionList.Add(ai);
    else if (sign == "BIU26_Minion_Boss")   _bossMinionList.Add(ai);

    ai.MsgRegister.Register<SE_GPO.Event_SetIsDead>(_ => {
        _normalMinionList.Remove(ai);
        _eliteMinionList.Remove(ai);
        _bossMinionList.Remove(ai);
        // ... 触发 Event_MinionKilled 等现有逻辑
    });
};
```

### 8.7 ClientBIU26MinionSystem.cs（骨架）

```csharp
// Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26MinionSystem.cs
// 三档共用同一客户端 System，通过 MData.AssetSign 区分 Prefab

namespace Sofunny.BiuBiuBiu2.ClientGamePlay {
    public class ClientBIU26MinionSystem : C_AI_Base {

        protected override void AddComponents() {
            base.AddComponents();
            // 当前无定制客户端组件；Phase 3 可追加元素特效组件
        }

        protected override void OnStart() {
            base.OnStart();
            // MData.AssetSign 由服务端 GPOM 决定：
            //   普通 → "BIU26Minion_Normal" → BIU26Minion_Normal.prefab（灰白 Capsule）
            //   精英 → "BIU26Minion_Elite"  → BIU26Minion_Elite.prefab（蓝色 1.4x Capsule）
            //   头目 → "BIU26Minion_Boss"   → BIU26Minion_Boss.prefab（金色 1.8x Capsule）
            CreateEntity(MData.GetAssetSign());
        }
    }
}
```

---

## 九、现有 BIU26_Minion_Normal 平滑迁移方案（最小改动原则）

### 9.1 当前状态（迁移前）

```
Gpo.cs Id=102:  GpoType=9(Character),  Sign="BIU26_Minion_Normal", AssetSign="Character"
GpoTypeSet:     无 Id_BIU26Minion_Normal 常量
IGPOM.cs:       Id=102 走 case 9(Character) → GPOM_CharacterSet
ServerAIWorld_Switch: 无 BIU26Minion 专属 case，复用 Character route
ServerBIU26MinionsSpawner: MinionSign="BIU26_Minion_Normal"（不变，兼容）
```

### 9.2 迁移后状态

```
Gpo.cs Id=102:  GpoType=32(BIU26Minion_Normal), AssetSign="BIU26Minion_Normal" ← 改这两字段
GpoTypeSet:     Id_BIU26Minion_Normal=32（新增常量+Data行）
IGPOM.cs:       新增 case 32 → GPOM_BIU26Minion_NormalSet（不影响现有 case 9）
ServerAIWorld_Switch: 新增 case 32 → ServerBIU26MinionNormalSystem
ServerBIU26MinionsSpawner: MinionSign="BIU26_Minion_Normal"（不需修改）
```

### 9.3 迁移影响范围分析

| 变更项 | 影响 | 风险 |
|-------|------|------|
| Gpo.cs Id=102 GpoType 9→32 | 框架用 GpoType 查路由，路由切换到新 System | 低（旧 case 9 路由不再命中，但新 case 32 已注册） |
| AssetSign "Character"→"BIU26Minion_Normal" | 客户端 CreateEntity 加载不同 Prefab | 低（需确保 BIU26Minion_Normal.prefab 已创建） |
| ServerBIU26MinionNormalSystem 替代原 CharacterAI System | 行为组件重新挂载：base.AddComponents() 确保核心组件不丢失 | 低（S_AI_Base 基类已覆盖 Dead/Hurt/HateTarget 等）|
| IGPOM.cs 新增 case 32 | 不影响其他 GpoType 的路由 | 无 |

> **保险措施**：迁移后第一次运行前，在 ServerBIU26MinionNormalSystem.OnStart() 加一行 Debug.Log，确认 System 被正确调起。

---

## 十、S-09 验收标准

### 10.1 编译验收

- [ ] `GPOM_BIU26MinionSet.cs` 编译通过，无 CS 错误；三个 struct 均实现 `IGPOM` 接口（GetXXX 方法完整）
- [ ] `ServerBIU26MinionNormalSystem` / `EliteSystem` / `BossSystem` 编译通过，MData 强转无异常（OnAwake 不抛出 InvalidCastException）
- [ ] `ServerBIU26MinionContactDamage` 编译通过，OnInit / OnUpdate 方法正确重写
- [ ] `SE_BIU26.Event_ZoneShrinkPhaseStarted` 新增后整个 SE_BIU26.cs 编译通过
- [ ] 全项目编译 0 错误 0 警告（或不引入新 Warning）

### 10.2 功能验收（运行时）

- [ ] 进入 BIU26 模式，普通怪正常刷出：控制台输出 `[ServerBIU26MinionNormalSystem]` 日志（或可通过场景观察到灰白 Capsule 追玩家）
- [ ] 玩家站在怪物 1.5m 内持续 2 秒，HP 显示扣减；移出 1.5m 后停止扣血（验证 ContactDamage 生效）
- [ ] 玩家与普通怪保持 >1.5m 距离时，HP 不受怪物影响（验证 ContactDamage 不误触发）
- [ ] 精英怪 Prefab（蓝色 1.4x Capsule）、头目怪 Prefab（金色 1.8x Capsule）在客户端场景中目视可辨，体型差异明显

### 10.3 集成验收（进化机制）

- [ ] 手动触发 `SE_BIU26.Event_ZoneShrinkPhaseStarted { Phase=1 }`（可在 EditorMode 通过 Dispatcher 测试），场景内约 30-40% 的白色 Capsule 消失，同位置出现蓝色大型 Capsule（精英怪）
- [ ] 再触发 Phase=2，场景内约 30-40% 的蓝色 Capsule 替换为金色大型 Capsule（头目怪）
- [ ] 进化后的精英怪/头目怪近身伤害分别为 15/22 HP/s（可通过 Debug.Log 在 OnUpdate 确认 `_dmgPerSec` 字段值）
- [ ] 进化过程中无 NullReferenceException（存活列表正确清理已死 GPO）
- [ ] 进化时 ServerBIU26MinionsSpawner 的 `_normalMinionList` / `_eliteMinionList` 数量正确递减

### 10.4 行为类型验收（Phase 2.5 运行时行为）

- [ ] 进入 BIU26 模式，刷怪器按照 Rush 40% / Swarm 35% / Ranged 15% / Tank 10% 比例生成各类型小怪（可在 SpawnBatch 调用处 Debug.Log 验证 BehaviorTypeValue）；群涌型单次 SpawnBatch 可见 5-15 只同时出现
- [ ] 远程型小怪在玩家靠近至 15m 以内时发生主动后退行为（可通过观察移动方向向量确认：`ServerBIU26MinionRangedBehavior.SetMoveDir(-dir)` 被触发）；坦克型小怪以极慢速（≤1.5m/s）稳定推进，不闪避，可与冲锋型小怪的速度目视明显区分
- [ ] 四种行为类型的小怪均不引入新 NullReferenceException；行为组件 `OnInit` 中通过 `GetComponent<ServerAIHateTarget>()` 获取到有效引用（若返回 null 则在 OnUpdate 中安全跳过，无崩溃）

---

## 十一、S-10 行为类型系统（Phase 2.5）

### 11.1 行为类型 × 档位组合矩阵

以下矩阵列出 3 档 × 4 类型 = 12 种变体的实现计划：

| 行为类型 | Normal（第1档） | Elite（第2档） | Boss（第3档） |
|---------|---------------|--------------|-------------|
| **冲锋型 Rush** | ✅ Phase 2.5 实现 | ⬜ Phase 3 延伸 | ⬜ Phase 3 延伸 |
| **群涌型 Swarm** | ✅ Phase 2.5 实现 | ⬜ Phase 3 延伸 | ⬜ Phase 3 延伸 |
| **远程型 Ranged** | ✅ Phase 2.5 实现 | ⬜ Phase 3 延伸 | ⬜ Phase 3 延伸 |
| **坦克型 Tank** | ✅ Phase 2.5 实现 | ⬜ Phase 3 延伸 | ⬜ Phase 3 延伸 |

> Phase 2.5 仅实现 Normal 档的 4 种行为类型；Elite/Boss 档的行为差异（数值倍率 + 特殊技能）在 Phase 3 由行为组件支持档位参数后延伸。

---

### 11.2 文件清单补充

> 以下文件在原 §三 文件清单基础上追加，Phase 2.5 实现时需同步纳入执行计划。

#### 🖥️ 服务端行为组件（新增 4 个）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionRushBehavior.cs` | **新建** | 冲锋型行为组件：快速（8-10 m/s）直线追敌，靠 ContactDamage 实现近身高伤低频攻击 |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionSwarmBehavior.cs` | **新建** | 群涌型行为组件：慢速（2-3 m/s）聚集，由刷怪器 SpawnBatch 一次刷出 5-15 只 |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionRangedBehavior.cs` | **新建** | 远程型行为组件：维持 15-25m 距离，玩家靠近则主动后退；Phase 2.5 以接触型伤害替代投射物（Phase 3 接入 Ability 体系） |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionTankBehavior.cs` | **新建** | 坦克型行为组件：极慢（1-1.5 m/s）推进，共享大半径 `ServerBIU26MinionContactDamage`；前摇由动画/视觉表示（Phase 2.5 灰盒） |

#### 📋 配表层补充（GPOM_BIU26MinionSet.cs）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Template/gpo/GPOM_BIU26MinionSet.cs` | **修改** | 三个 struct 均追加 `BIU26MinionBehaviorType BehaviorTypeValue` 枚举字段（Rush/Swarm/Ranged/Tank） |

---

### 11.3 行为类型枚举定义

```csharp
// 追加到 GPOM_BIU26MinionSet.cs 顶部（与 struct 同命名空间）
namespace Sofunny.BiuBiuBiu2.Template {

    /// <summary>BIU26 小怪行为类型枚举</summary>
    public enum BIU26MinionBehaviorType : byte {
        Rush   = 0,  // 冲锋型：快速直线接近，高伤低频
        Swarm  = 1,  // 群涌型：慢速成群聚集，低伤范围
        Ranged = 2,  // 远程型：保持距离后退，远程干扰
        Tank   = 3,  // 坦克型：极慢推进，高血 AOE
    }
}
```

---

### 11.4 ASCII 链路图：行为组件决策流程（以冲锋型为例）

```
[ServerBIU26MinionNormalSystem.AddComponents()]
        │
        ├─ (base 已挂) ServerAIHateTarget ← 仇恨列表（自动选最近玩家）
        ├─ (base 已挂) ServerAIMove       ← 移动驱动
        ├─ ServerBIU26MinionContactDamage  ← 接触伤害（四种类型共用）
        │
        └─ 根据 MData.BehaviorTypeValue 挂载对应行为组件
                │
                ▼ case Rush
        [ServerBIU26MinionRushBehavior.OnUpdate()]
                │
                ├─ target ← ServerAIHateTarget.GetTarget()
                ├─ dir    = (target.pos - self.pos).normalized
                ├─ speed  = MoveSpeedMultiplier × Rush倍率（8-10 m/s）
                ├─ ServerAIMove.SetMoveDir(dir)
                │
                └─ dist ≤ 1.5m ？
                        │ YES → ContactDamage 生效（高伤低频由 DamagePerSec 控制）
                        └─ NO  → 继续追赶

                ▼ case Swarm
        [ServerBIU26MinionSwarmBehavior.OnUpdate()]
                │
                └─ 同上直线追敌，但 MoveSpeedMultiplier 对应慢速值（2-3 m/s）

                ▼ case Ranged
        [ServerBIU26MinionRangedBehavior.OnUpdate()]
                │
                ├─ dist < 15m → SetMoveDir(-dir)  后退
                ├─ dist > 25m → SetMoveDir( dir)  缓慢靠近
                └─ 15m≤dist≤25m → SetMoveDir(zero) 站立持续干扰
                                   （Phase 3 此处触发投射物 Ability）

                ▼ case Tank
        [ServerBIU26MinionTankBehavior.OnUpdate()]
                │
                └─ 极慢直线推进，不闪避；AOE 由大半径 ContactDamage 模拟
```

---

### 11.5 核心代码骨架（4 个 Behavior Component OnUpdate 骨架）

```csharp
// ==========================================
// 冲锋型 Rush
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionRushBehavior.cs
// ==========================================
using Sofunny.BiuBiuBiu2.Template;
namespace Sofunny.BiuBiuBiu2.GamePlay.Server {
    public class ServerBIU26MinionRushBehavior : ServerNetworkComponentBase {

        private ServerAIHateTarget      _hateTarget;
        private ServerAIMove            _aiMove;
        private GPOM_BIU26Minion_Normal _mData;

        public override void OnInit(IServerNetworkSystem system) {
            base.OnInit(system);
            _hateTarget = system.GetComponent<ServerAIHateTarget>();
            _aiMove     = system.GetComponent<ServerAIMove>();
            _mData      = (GPOM_BIU26Minion_Normal)system.MData;
        }

        public override void OnUpdate(float deltaTime) {
            var target = _hateTarget?.GetTarget();
            if (target == null) return;
            // Rush 速度：MoveSpeedMultiplier 作为基础，对应 8-10 m/s 区间
            var dir = (target.GetPoint() - system.GetPoint()).normalized;
            _aiMove.SetMoveDir(dir);
        }
    }
}

// ==========================================
// 群涌型 Swarm
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionSwarmBehavior.cs
// ==========================================
namespace Sofunny.BiuBiuBiu2.GamePlay.Server {
    public class ServerBIU26MinionSwarmBehavior : ServerNetworkComponentBase {

        private ServerAIHateTarget _hateTarget;
        private ServerAIMove       _aiMove;

        public override void OnInit(IServerNetworkSystem system) {
            base.OnInit(system);
            _hateTarget = system.GetComponent<ServerAIHateTarget>();
            _aiMove     = system.GetComponent<ServerAIMove>();
        }

        public override void OnUpdate(float deltaTime) {
            var target = _hateTarget?.GetTarget();
            if (target == null) return;
            // Swarm 慢速（2-3 m/s）直线聚集，靠 ContactDamage 堆叠群体伤害
            // ⚠️ 速度由 GPOM MoveSpeedMultiplier 低值（约 0.25-0.375×标准速度）控制
            var dir = (target.GetPoint() - system.GetPoint()).normalized;
            _aiMove.SetMoveDir(dir);
        }
    }
}

// ==========================================
// 远程型 Ranged
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionRangedBehavior.cs
// ==========================================
namespace Sofunny.BiuBiuBiu2.GamePlay.Server {
    public class ServerBIU26MinionRangedBehavior : ServerNetworkComponentBase {

        private const float kKeepDistMin = 15f;
        private const float kKeepDistMax = 25f;

        private ServerAIHateTarget _hateTarget;
        private ServerAIMove       _aiMove;

        public override void OnInit(IServerNetworkSystem system) {
            base.OnInit(system);
            _hateTarget = system.GetComponent<ServerAIHateTarget>();
            _aiMove     = system.GetComponent<ServerAIMove>();
        }

        public override void OnUpdate(float deltaTime) {
            var target = _hateTarget?.GetTarget();
            if (target == null) { _aiMove.SetMoveDir(UnityEngine.Vector3.zero); return; }

            float dist = UnityEngine.Vector3.Distance(target.GetPoint(), system.GetPoint());
            var   dir  = (target.GetPoint() - system.GetPoint()).normalized;

            if (dist < kKeepDistMin) {
                _aiMove.SetMoveDir(-dir);  // 玩家太近 → 主动后退
            } else if (dist > kKeepDistMax) {
                _aiMove.SetMoveDir(dir);   // 距离太远 → 缓慢靠近
            } else {
                // 在维持距离区间内 → 站立干扰
                // Phase 2.5：接触型伤害替代投射物
                // TODO Phase 3：此处触发 Ability 投射物攻击（参考 ServerBIU26FloatingWeaponAttack）
                _aiMove.SetMoveDir(UnityEngine.Vector3.zero);
            }
        }
    }
}

// ==========================================
// 坦克型 Tank
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26MinionTankBehavior.cs
// ==========================================
namespace Sofunny.BiuBiuBiu2.GamePlay.Server {
    public class ServerBIU26MinionTankBehavior : ServerNetworkComponentBase {

        private ServerAIHateTarget _hateTarget;
        private ServerAIMove       _aiMove;

        public override void OnInit(IServerNetworkSystem system) {
            base.OnInit(system);
            _hateTarget = system.GetComponent<ServerAIHateTarget>();
            _aiMove     = system.GetComponent<ServerAIMove>();
        }

        public override void OnUpdate(float deltaTime) {
            var target = _hateTarget?.GetTarget();
            if (target == null) return;
            // Tank 极慢推进（1-1.5 m/s），不闪避
            // AOE 伤害通过大半径 ContactDamage 模拟；前摇视觉由客户端动画处理（Phase 2.5 灰盒）
            var dir = (target.GetPoint() - system.GetPoint()).normalized;
            _aiMove.SetMoveDir(dir);
        }
    }
}
```

---

### 11.6 刷怪器比例配置

`ServerBIU26MinionsSpawner` SpawnBatch 时按以下比例随机挑选行为类型：

| 行为类型 | 出生比例 | 每批数量说明 |
|---------|---------|------------|
| 冲锋型 Rush | **40%** | 单只刷出 |
| 群涌型 Swarm | **35%** | 一次 SpawnBatch 5-15 只（`_swarmGroupSize` 随机区间 [5, 15]，默认值 8） |
| 远程型 Ranged | **15%** | 单只刷出 |
| 坦克型 Tank | **10%** | 单只刷出 |

> 群涌型的"5-15 只一组"通过刷怪器一次 `SpawnBatch` 实现，**不需要群体 AI 队伍逻辑**。

---

### 11.7 远程型攻击实现说明（Phase 2.5 灰盒）

> **远程投射物**需要 Ability 体系支持。Phase 2.5 暂不接入，采用以下替代方案：

| 阶段 | 实现方式 | 说明 |
|------|---------|------|
| **Phase 2.5（当前）** | 接触型伤害替代（共用 `ServerBIU26MinionContactDamage`，维持后退距离逻辑正常运行） | 远程型会"躲避"玩家并在玩家意外靠近时触发伤害，体现类型差异 |
| **Phase 3（待实现）** | 参考 `ServerBIU26FloatingWeaponAttack.cs` 攻击模式，或通过 Ability 体系发射投射物 | 届时在 `ServerBIU26MinionRangedBehavior.OnUpdate` 的"站立区间"分支中触发 `Event_UseAbility` |

---

## 十二、ADR-01 放弃原生 GPOM_Character 路由

| 项目 | 内容 |
|------|------|
| **决策** | Id=102 GpoType 从 9(Character) 改为 32(BIU26Minion_Normal)，不再复用通用 CharacterAI System |
| **原因** | 原生 CharacterAI 路由走 GPOM_CharacterSet，无法携带 Atk/ContactRadius/MoveSpeedMultiplier 等 BIU26 专属字段；且无法在 AddComponents 阶段挂载 ContactDamage 组件 |
| **用户授权** | 根据 active.md 2026-03-30 规范沉淀：Phase 2 怪物GPO系统决策——放弃原生 AI 怪物，改用 BIU26 专属 GPO 体系 |
| **影响范围** | 仅影响 BIU26 模式的小怪生成；不影响其他模式 Id_Character=9 的路由；ServerBIU26MinionsSpawner.MinionSign 无需修改 |

---

[SESSION_DELTA]
Agent：[DL]
决策/进展：完成 BIU26-怪物GPO系统.md 技术文档撰写，覆盖三档怪物配表注册、GPOM骨架、服务端System+ContactDamage组件、进化机制（RemoveAI→AddAI替换）、客户端视觉方案、灰盒资源规格、现有BIU26_Minion_Normal平滑迁移方案
文件变更：新建 [[BIU26-怪物GPO系统]]
需更新 active.md：是
更新内容：M-03 技术子文档索引中将"BIU26-怪物GPO系统.md（新）"状态从"🔄 文档生成中"改为"✅ 已完成 v1.0"；技术文档状态表同步更新
