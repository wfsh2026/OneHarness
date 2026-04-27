# BIU26-武器升品质系统

> **文档版本**：v1.0
> **创建时间**：2026-03-30
> **负责 Agent**：开发负责人 (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：[[BIU26_开发计划]]
> **状态**：⬜ 待开发

---

## S-02 参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| 开发负责人 (DL) | 开发范例 | 暂无 | — |
| 开发负责人 (DL) | 边界定义 | 暂无 | — |
| 开发负责人 (DL) | 规则 | AIGC 会话调度规范.md | `AIGC/AIGC 会话调度规范.md` |
| 开发负责人 (DL) | 规则 | safety-rules.md | [[safety-rules]] |
| 开发负责人 (DL) | 规则 | core-rules.md | [[GamePlay_Dev/core-rules]] |
| 开发负责人 (DL) | 规则 | shader-code.md | [[shader-code]] |
| 开发负责人 (DL) | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| 开发负责人 (DL) | 规则 | plan-doc.md | [[plan-doc]] |
| 开发负责人 (DL) | 现有代码 | ServerBIU26FloatingWeaponManager.cs | `Assets/Scripts/GamePlay/Server/GPO/Components/` |
| 开发负责人 (DL) | 现有代码 | GPOM_BIU26FloatingWeaponSet.cs（含在 GPOM_BIU26Set.cs） | `Assets/Scripts/Template/gpo/GPOM_BIU26Set.cs` |
| 开发负责人 (DL) | 现有代码 | ServerBIU26FloatingWeaponSystem.cs | `Assets/Scripts/GamePlay/Server/AI/Systems/` |
| 开发负责人 (DL) | 现有代码 | SE_BIU26.cs | `Assets/Scripts/Message/GamePlay/Server/System/` |

---

## S-01 / S-03 背景与目标（功能需求）

**背景**：BIU26 Phase 2.5 需求。当玩家已解锁 6 把悬浮武器（`MaxWeaponCount = 6`）后，小怪死亡不再掉落新武器拾取物，而是改为随机升级现有武器的品质，以维持"还在变强"的持续成长感直到全员金质。

**玩家体验**：满编（6把）后继续击杀小怪，仍有概率看到某把悬浮武器变为蓝色（伤害明显提升），最终全部升为金色，感受到"已经无敌"的爽感顶峰。

---

## S-04 功能定位

本文档负责 **武器满载后的品质升级系统**，职责边界为：

- `ServerBIU26FloatingWeaponManager`：入口判断（满编分支）+ 升品质概率+保底逻辑
- `GPOM_BIU26FloatingWeaponSet`：新增蓝质/金质数据条目
- `SE_BIU26`：新增 `Event_FloatingWeaponAdded` 事件用于追踪活跃武器 IGPO

**不涉及**：武器攻击逻辑、移动跟随逻辑、拾取物逻辑（已在其他文档覆盖）。

---

## S-03（扩展）架构概览：武器品质状态机

```
        hit minion
            │
     ┌──────▼──────┐
     │ weaponCount  │
     │  < Max(6)?  │
     └──────┬──────┘
        YES │           NO（满编）
            │           │
       掉落拾取物     ┌──▼──────────────────────┐
       （现有逻辑）   │ 检查所有武器是否全为金质   │
                      └──────────┬──────────────┘
                          全金质  │  有非金质
                            │    │
                      满品质退出  │
                                 ▼
                    ┌────────────────────────┐
                    │  概率/保底判断          │
                    │  _noUpgradeCount >= 5? │
                    │  OR Random <= chance?  │
                    └────────┬───────────────┘
                       未触发 │         触发
                             │         │
                    _noUpgrade++    ┌───▼───────────────────┐
                    chance += 0.05  │ 选目标武器             │
                                   │ 保底→最低品质武器       │
                                   │ 否则→随机非金质武器     │
                                   └───────────┬───────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │ RemoveAI(旧IGPO)     │
                                    │ AddMasterAI(升品质Sign)│
                                    │ 回调更新_activeWeapons │
                                    └─────────────────────┘


品质状态机：
  white (q=1, atk=100) ──→ blue (q=2, atk=150) ──→ gold (q=3, atk=250)
                                                         ↑
                                                     不可超过（上限）
```

---

## S-05 涉及文件清单

### 📋 配表层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Template/gpo/GPOM_BIU26Set.cs` | **修改** | 在 `GPOM_BIU26FloatingWeaponSet.Data` 追加蓝质（Id=106）和金质（Id=107）两条新 GPOM 条目；新增 `Id_BIU26FloatingWeapon_Blue = 106`、`Sign_BIU26FloatingWeapon_Blue`、`Id_BIU26FloatingWeapon_Gold = 107`、`Sign_BIU26FloatingWeapon_Gold` 常量 |
| `Assets/Scripts/Template/data/Gpo.cs` | **修改**（csv-gen 生成，追加行）| 追加 `new Gpo(30, 106, "BIU26蓝质悬浮武器", "BIU26FloatingWeapon_Blue", "BIU26FloatingWeapon_Blue", "")` 和 `new Gpo(30, 107, "BIU26金质悬浮武器", "BIU26FloatingWeapon_Gold", "BIU26FloatingWeapon_Gold", "")` |

### 🔀 路由注册层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| 无需修改 | — | 蓝质/金质武器 GpoType 均为 30，与白质共用已注册的 `case GpoTypeSet.Id_BIU26FloatingWeapon` 路由分支 |

### 🖥️ 服务端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26FloatingWeaponManager.cs` | **修改** | 重构 `OnMinionKilled`：满编时分支到 `TryUpgradeWeaponQuality()`；新增字段 `_activeWeapons`、`_upgradeChance`、`_noUpgradeCount`、`_masterPlayerGPO`；新增方法 `TryUpgradeWeaponQuality`、`UpgradeWeapon`、`OnFloatingWeaponAdded` |
| `Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerBIU26Mode.cs` | **修改** | 在 `OnAddCharacterCallBack` 的初始武器召唤 `OR_CallBack` 中追加广播 `SE_BIU26.Event_FloatingWeaponAdded`，确保初始第1把武器也进入 `_activeWeapons` 追踪池 |
| `Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs` | **修改** | 追加 `Event_FloatingWeaponAdded`（`IWorldEvent`），携带 `IGPO WeaponGPO` 字段，用于让 Manager 追踪活跃悬浮武器 IGPO 引用 |
| `Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26WeaponPickupZone.cs` | **修改** | 在 `SM_AI.Event_AddMasterAI` 的 `OR_CallBack` 中追加 `MsgRegister.Dispatcher(new SE_BIU26.Event_FloatingWeaponAdded { WeaponGPO = ai.iGPO })` |

### 💻 客户端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26FloatingWeaponSystem.cs` | **复用（不修改）** | `CreateEntity(AttributeData.SkinSign)` 按 AssetSign 加载 Prefab，蓝质/金质自动加载对应 Prefab，无需修改 |

### 🎨 资产层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Bundle/GamePlay/AI/Client/BIU26FloatingWeapon_Blue.prefab` | **新建** | 蓝质武器客户端 Prefab（Capsule 占位，挂 BIU26FloatingWeapon_Blue_Mat.mat） |
| `Assets/Bundle/GamePlay/AI/Client/BIU26FloatingWeapon_Blue_Mat.mat` | **新建** | URP/Lit 材质，`_BaseColor RGBA (0.3, 0.5, 1.0, 1.0)`，Metallic=0.8 |
| `Assets/Bundle/GamePlay/AI/Client/BIU26FloatingWeapon_Gold.prefab` | **新建** | 金质武器客户端 Prefab（Capsule 占位，挂 BIU26FloatingWeapon_Gold_Mat.mat） |
| `Assets/Bundle/GamePlay/AI/Client/BIU26FloatingWeapon_Gold_Mat.mat` | **新建** | URP/Lit 材质，`_BaseColor RGBA (1.0, 0.8, 0.1, 1.0)`，Metallic=1.0 |

---

## S-05（扩展）核心逻辑设计

### 5.1 整体判断分支

`OnMinionKilled` 新增满载分支：

```
if (weaponCount < MaxWeaponCount) → 原有掉落拾取物逻辑（不变）
else                              → TryUpgradeWeaponQuality()
```

### 5.2 概率体系（与武器解锁共用参数）

| 参数 | 值 | 说明 |
|------|-----|------|
| `BaseDropChance` | 0.2f | 基础触发概率 20% |
| `DropChanceStep` | 0.05f | 每次未触发累加量 +5% |
| 重置时机 | 触发时 | 回到 20% |
| 最大累积次数 | 16次 | 20% + 16×5% = 100%（理论最大值） |

> 概率体系复用 `BaseDropChance`/`DropChanceStep` 常量，实际用独立字段 `_upgradeChance`，不与武器解锁阶段的 `dropChance` 混用。

### 5.3 保底机制（用户决策 D1：连续5次未升必升）

| 字段 | 初始值 | 更新规则 |
|------|--------|---------|
| `_noUpgradeCount` | 0 | 每次未触发升品质 +1；触发时归零 |
| 保底条件 | `_noUpgradeCount >= 5` | 强制触发，选择品质最低的武器升级 |

### 5.4 目标武器选择算法

```
普通升级（随机）：
  candidates = _activeWeapons.Where(slot => slot.Quality < QualityGold)
  target     = candidates[Random.Range(0, candidates.Count)]

保底升级（最低品质优先）：
  target = _activeWeapons.Min(slot => slot.Quality)  // 选品质值最小的
  若多把同品质，随机选一把
```

### 5.5 IGPO 追踪方案

Manager 无法直接访问子 GPO System，因此通过新事件追踪：

1. `ServerBIU26WeaponPickupZone` 召唤武器后广播 `SE_BIU26.Event_FloatingWeaponAdded`
2. Manager 在 `OnFloatingWeaponAdded` 中追加 `WeaponSlot { Gpo = e.WeaponGPO, Quality = QualityWhite }`
3. 升品质时：RemoveAI 旧 IGPO → AddMasterAI 新 Sign → OR_CallBack 中更新 slot

---

## S-06 ASCII 交互链路图（升品质完整链路）

```
玩家击杀小怪
     │
     ▼
ServerBIU26MinionsSpawner
     │ MsgRegister.Dispatcher(Event_MinionKilled)
     ▼
ServerBIU26FloatingWeaponManager.OnMinionKilled()
     │ weaponCount >= 6
     │
     ▼
TryUpgradeWeaponQuality()
     │ 检查全金质 / 概率/保底 判断
     │
     ▼
UpgradeWeapon(slotIndex)
     │
     ├─ MsgRegister.Dispatcher(SM_AI.Event_RemoveAI { GpoId })
     │       │
     │       ▼
     │  ServerAIWorld 销毁旧武器 GPO
     │       │
     │       ▼
     │  TargetRpc_RemoveAI → 客户端 ClientBIU26FloatingWeaponSystem 销毁旧实体
     │
     └─ MsgRegister.Dispatcher(SM_AI.Event_AddMasterAI {
            AISign = "BIU26FloatingWeapon_Blue",
            MasterGPO = _masterPlayerGPO,
            StartPoint = oldPos,
            OR_CallBack = ai => { _activeWeapons[idx] = new WeaponSlot{Gpo=ai.iGPO, Quality=2} }
        })
               │
               ▼
        ServerAIWorld 生成新武器 GPO
        → ServerBIU26FloatingWeaponSystem.OnAwake()
          (useMData.Atk = 150 for blue)
               │
               ▼
        RPC 同步 → ClientBIU26FloatingWeaponSystem
          CreateEntity("BIU26FloatingWeapon_Blue")
          加载蓝色 Prefab，视觉即时切换
```

---

## S-07 灰盒资源占位

| 视觉对象 | 形状 | 颜色（_BaseColor RGBA） | 尺寸 | 挂点偏移（相对 GPO 根节点） |
|---------|------|----------------------|------|--------------------------|
| 蓝质悬浮武器 Prefab | Capsule | `(0.3, 0.5, 1.0, 1.0)` 蓝色高光 | 0.5m × 1.0m × 0.5m（与白质相同） | `(0, 0, 0)`（跟随主人，偏移由 Move 组件管理） |
| 金质悬浮武器 Prefab | Capsule | `(1.0, 0.8, 0.1, 1.0)` 金色高亮 | 0.5m × 1.0m × 0.5m（与白质相同） | `(0, 0, 0)`（跟随主人，偏移由 Move 组件管理） |

> 注：形状/尺寸与白质武器保持一致，仅以材质颜色区分品质档次。Metallic 值：蓝质 0.8，金质 1.0（全金属反射）。

---

## S-06（扩展）代码骨架

```csharp
// Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26FloatingWeaponManager.cs
// 新增/修改部分（在原有字段和方法基础上追加）

public class ServerBIU26FloatingWeaponManager : ComponentBase {
    // ── 原有常量（不变）──────────────────────────────────────
    private const int   MaxWeaponCount  = 6;
    private const float BaseDropChance  = 0.2f;
    private const float DropChanceStep  = 0.05f;

    // ── 品质常量 ─────────────────────────────────────────────
    private const byte  QualityWhite = 1;
    private const byte  QualityBlue  = 2;
    private const byte  QualityGold  = 3;
    private const int   MaxNoUpgrade = 5;

    // ── 原有字段（不变）──────────────────────────────────────
    private int   weaponCount = 1;
    private float dropChance  = BaseDropChance;
    private int   ownerTeamId = 1;

    // ── 新增字段 ─────────────────────────────────────────────
    private struct WeaponSlot { public IGPO Gpo; public byte Quality; }
    private readonly List<WeaponSlot> _activeWeapons  = new List<WeaponSlot>();
    private float _upgradeChance  = BaseDropChance;
    private int   _noUpgradeCount = 0;
    private IGPO  _masterPlayerGPO;

    // ── 生命周期 ─────────────────────────────────────────────
    protected override void OnAwake() {
        Register<SE_Mode.Event_AddCharacterFinish>(OnFirstCharacterJoin);
        MsgRegister.Register<SE_BIU26.Event_MinionKilled>(OnMinionKilled);
        MsgRegister.Register<SE_BIU26.Event_FloatingWeaponAdded>(OnFloatingWeaponAdded);
    }

    protected override void OnClear() {
        Unregister<SE_Mode.Event_AddCharacterFinish>(OnFirstCharacterJoin);
        MsgRegister.Unregister<SE_BIU26.Event_MinionKilled>(OnMinionKilled);
        MsgRegister.Unregister<SE_BIU26.Event_FloatingWeaponAdded>(OnFloatingWeaponAdded);
    }

    private void OnFirstCharacterJoin(ISystemMsg body, SE_Mode.Event_AddCharacterFinish e) {
        ownerTeamId      = e.Data.CharacterGPO.GetTeamID();
        _masterPlayerGPO = e.Data.CharacterGPO; // 新增：记录玩家 IGPO 供升品质 AddMasterAI 使用
        Unregister<SE_Mode.Event_AddCharacterFinish>(OnFirstCharacterJoin);
    }

    // ── 武器 IGPO 追踪 ───────────────────────────────────────
    private void OnFloatingWeaponAdded(SE_BIU26.Event_FloatingWeaponAdded e) {
        _activeWeapons.Add(new WeaponSlot { Gpo = e.WeaponGPO, Quality = QualityWhite });
    }

    // ── 主入口：击杀小怪 ─────────────────────────────────────
    private void OnMinionKilled(SE_BIU26.Event_MinionKilled e) {
        if (weaponCount < MaxWeaponCount) {
            // 原有逻辑：概率/保底掉落拾取物
            if (Random.value <= dropChance) {
                dropChance = BaseDropChance;
                SpawnPickup(e.DeathPoint);
            } else {
                dropChance += DropChanceStep;
            }
            return;
        }
        // 满编：尝试升品质
        TryUpgradeWeaponQuality();
    }

    // ── 升品质主逻辑 ─────────────────────────────────────────
    private void TryUpgradeWeaponQuality() {
        // 若所有武器均为金质，不再触发任何逻辑
        bool anyNonGold = false;
        foreach (var slot in _activeWeapons) {
            if (slot.Gpo != null && slot.Quality < QualityGold) { anyNonGold = true; break; }
        }
        if (!anyNonGold) return;

        bool forceUpgrade = (_noUpgradeCount >= MaxNoUpgrade);
        bool doUpgrade    = forceUpgrade || (Random.value <= _upgradeChance);

        if (doUpgrade) {
            _upgradeChance  = BaseDropChance;
            _noUpgradeCount = 0;
            int targetIdx   = forceUpgrade ? GetLowestQualitySlotIndex() : GetRandomNonGoldSlotIndex();
            if (targetIdx >= 0) UpgradeWeapon(targetIdx);
        } else {
            _upgradeChance  += DropChanceStep;
            _noUpgradeCount += 1;
        }
    }

    // ── 执行升品质：RemoveAI + AddMasterAI ───────────────────
    private void UpgradeWeapon(int slotIndex) {
        WeaponSlot slot     = _activeWeapons[slotIndex];
        byte       newQuality = (byte)(slot.Quality + 1); // white→blue→gold
        string     newSign    = GetSignForQuality(newQuality);
        Vector3    pos        = slot.Gpo.GetPoint();

        // 清空 slot（防止在回调前被重复选中）
        _activeWeapons[slotIndex] = default;

        // 销毁旧武器 GPO
        MsgRegister.Dispatcher(new SM_AI.Event_RemoveAI { GpoId = slot.Gpo.GetGpoID() });

        // 生成升品质后的新武器 GPO
        int capturedIdx = slotIndex;
        MsgRegister.Dispatcher(new SM_AI.Event_AddMasterAI {
            AISign     = newSign,
            MasterGPO  = _masterPlayerGPO,
            StartPoint = pos,
            OR_CallBack = ai => {
                _activeWeapons[capturedIdx] = new WeaponSlot { Gpo = ai.iGPO, Quality = newQuality };
            },
        });
    }

    // ── 辅助方法 ─────────────────────────────────────────────
    private static string GetSignForQuality(byte quality) {
        switch (quality) {
            case QualityBlue: return GPOM_BIU26FloatingWeaponSet.Sign_BIU26FloatingWeapon_Blue;
            case QualityGold: return GPOM_BIU26FloatingWeaponSet.Sign_BIU26FloatingWeapon_Gold;
            default:          return GPOM_BIU26FloatingWeaponSet.Sign_BIU26FloatingWeapon;
        }
    }

    private int GetLowestQualitySlotIndex() {
        int idx = -1; byte minQ = byte.MaxValue;
        for (int i = 0; i < _activeWeapons.Count; i++) {
            var s = _activeWeapons[i];
            if (s.Gpo != null && s.Quality < QualityGold && s.Quality < minQ) { minQ = s.Quality; idx = i; }
        }
        return idx;
    }

    private int GetRandomNonGoldSlotIndex() {
        var candidates = new List<int>();
        for (int i = 0; i < _activeWeapons.Count; i++) {
            var s = _activeWeapons[i];
            if (s.Gpo != null && s.Quality < QualityGold) candidates.Add(i);
        }
        return candidates.Count > 0 ? candidates[Random.Range(0, candidates.Count)] : -1;
    }

    // ── 原有 SpawnPickup（不变）─────────────────────────────
    private void SpawnPickup(Vector3 pos) {
        MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
            AISign     = GPOM_BIU26WeaponPickupSet.Sign_BIU26WeaponPickup,
            StartPoint = pos,
            OR_GpoType = GPOData.GPOType.AI,
            OR_TeamId  = ownerTeamId,
        });
        weaponCount++;
    }
}
```

```csharp
// Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs
// 追加新事件（在现有两个事件后追加）

public static class SE_BIU26 {
    // ... 原有 Event_MinionKilled, Event_ZoneStageChanged（不变） ...

    /// <summary>
    /// 悬浮武器 GPO 被成功召唤时广播（WeaponPickupZone AddMasterAI 回调中派发）
    /// Manager 订阅此事件以维护 _activeWeapons 列表
    /// </summary>
    public struct Event_FloatingWeaponAdded : GamePlayEvent.IWorldEvent {
        private static readonly int _id = GamePlayEvent.ReadonlyWorldEventID<Event_FloatingWeaponAdded>();
        public int GetID() => _id;
        public IGPO WeaponGPO; // 已激活的悬浮武器 IGPO
    }
}
```

```csharp
// Assets/Scripts/Template/gpo/GPOM_BIU26Set.cs（GPOM_BIU26FloatingWeaponSet 类，追加部分）
// 追加常量与数据条目

public static class GPOM_BIU26FloatingWeaponSet {
    // 原有
    public const int    Id_BIU26FloatingWeapon        = 101;
    public const string Sign_BIU26FloatingWeapon      = "BIU26FloatingWeapon";

    // 新增
    public const int    Id_BIU26FloatingWeapon_Blue   = 106;
    public const string Sign_BIU26FloatingWeapon_Blue = "BIU26FloatingWeapon_Blue";
    public const int    Id_BIU26FloatingWeapon_Gold   = 107;
    public const string Sign_BIU26FloatingWeapon_Gold = "BIU26FloatingWeapon_Gold";

    static GPOM_BIU26FloatingWeaponSet() {
        Data = new GPOM_BIU26FloatingWeapon[] {
            // 白质（原有，quality=1, atk=100）
            new GPOM_BIU26FloatingWeapon("BIU26FloatingWeapon", 100, 0.4f, 50f, new int[]{}, 0, "",
                new int[]{}, 30, 0, 101, 0, 50f, "BIU26悬浮武器", 1, "BIU26FloatingWeapon"),
            // 蓝质（新增，quality=2, atk=150）
            new GPOM_BIU26FloatingWeapon("BIU26FloatingWeapon_Blue", 150, 0.4f, 50f, new int[]{}, 0, "",
                new int[]{}, 30, 0, 106, 0, 50f, "BIU26蓝质悬浮武器", 2, "BIU26FloatingWeapon_Blue"),
            // 金质（新增，quality=3, atk=250）
            new GPOM_BIU26FloatingWeapon("BIU26FloatingWeapon_Gold", 250, 0.4f, 50f, new int[]{}, 0, "",
                new int[]{}, 30, 0, 107, 0, 50f, "BIU26金质悬浮武器", 3, "BIU26FloatingWeapon_Gold"),
        };
    }
}
```

---

## S-07（扩展）数值说明

| 品质 | Quality 值 | 攻击力（Atk） | 倍率 | Sign | GPO Id |
|------|-----------|--------------|------|------|--------|
| 白质（white） | 1 | 100 | ×1.0 | `BIU26FloatingWeapon` | 101 |
| 蓝质（blue） | 2 | 150 | ×1.5 | `BIU26FloatingWeapon_Blue` | 106 |
| 金质（gold） | 3 | 250 | ×2.5 | `BIU26FloatingWeapon_Gold` | 107 |

> **数值来源**：用户决策 **B7**（`aigc/harness/session-state/BIU26/active.md`，2026-03-28 记录）。
> 攻击间隔（0.4s）和攻击距离（50m）三档相同，品质差异仅体现在 Atk 上。

---

## S-08 边界条件

### 外部依赖接口

| 接口 | 来源 | 用途 |
|------|------|------|
| `SM_AI.Event_RemoveAI { GpoId }` | `SM_AI.cs` | 销毁旧武器 GPO |
| `SM_AI.Event_AddMasterAI { AISign, MasterGPO, OR_CallBack }` | `SM_AI.cs` | 召唤升品质后的新武器 GPO |
| `IGPO.GetPoint()` | `IGPO` 接口 | 获取旧武器当前位置，传给新武器作 StartPoint |
| `IGPO.GetGpoID()` | `IGPO` 接口 | 获取运行时整数 ID，传给 Event_RemoveAI.GpoId |
| `IAI.iGPO` | `IAI` 接口 | OR_CallBack 中获取新武器的 IGPO 引用 |
| `SE_BIU26.Event_FloatingWeaponAdded` | 本文档新增 | WeaponPickupZone → Manager 单向广播 |

### 禁止事项

- ❌ **禁止**在 `OnMinionKilled` 未满编时调用 `TryUpgradeWeaponQuality()`（两阶段必须互斥）
- ❌ **禁止**在未等待 `OR_CallBack` 返回前操作 `_activeWeapons[slotIndex]`（slot 已在调用前置 default）
- ❌ **禁止**对 quality >= QualityGold 的武器执行 UpgradeWeapon（Guard 在 TryUpgrade 中已覆盖）
- ❌ **禁止**在不持有 `_masterPlayerGPO` 时调用 UpgradeWeapon（OnFirstCharacterJoin 未触发的极端情况：AddMasterAI 需要 MasterGPO，若为 null 会导致跟随逻辑失效）

### 边界定义文档引用

- 武器概率数值决策：`aigc/harness/session-state/BIU26/active.md` → 用户决策 D1、B7
- 悬浮武器 GPO 架构：[[BIU26-悬浮武器GPO]]
- 拾取物 GPO 架构（WeaponPickupZone）：[[BIU26-模式系统]]

---

## S-09 验收标准

### 9.1 编译验收

- [ ] `SE_BIU26.Event_FloatingWeaponAdded` 新增后，`SE_BIU26.cs` 编译通过，无报错
- [ ] `GPOM_BIU26FloatingWeaponSet` 追加蓝质/金质条目后，`GPOM_BIU26Set.cs` 编译通过，无报错
- [ ] `ServerBIU26FloatingWeaponManager.cs` 重构后编译通过，0 个错误，0 个与品质系统相关的警告
- [ ] `Gpo.cs` 追加 Id=106/107 后，相关使用处（`GetGPOMByIdAndMatchMode`）编译通过

### 9.2 功能验收（运行时）

- [ ] 武器数量未满 6 把时，`TryUpgradeWeaponQuality()` 不被调用（可通过日志确认 `OnMinionKilled` 走入 `return` 分支）
- [ ] 武器数量 = 6 把后，击杀小怪触发 `TryUpgradeWeaponQuality()`，有概率（约 20% 初始）选一把白质武器升为蓝质（日志可见 `UpgradeWeapon` 调用）
- [ ] 连续 5 次未触发升品质后，第 6 次击杀必触发保底升级（`_noUpgradeCount` 达 5，`forceUpgrade = true`，`GetLowestQualitySlotIndex()` 命中）
- [ ] 所有武器均为金质时，`TryUpgradeWeaponQuality()` 执行 `anyNonGold=false` 直接 `return`，不再发送任何事件（日志无 `UpgradeWeapon` 输出）
- [ ] 升品质后新武器 Atk = 150（蓝质）或 250（金质），通过 `ServerAIAttribute` 可读出正确数值

### 9.3 集成验收（跨模块联动）

- [ ] `ServerBIU26WeaponPickupZone` 召唤武器后广播 `Event_FloatingWeaponAdded`，`ServerBIU26Mode` 在初始武器生成回调中同样广播；满编拾取完 6 把后 `_activeWeapons.Count == 6`（全部追踪）
- [ ] `SM_AI.Event_RemoveAI` 发出后，客户端对应 `ClientBIU26FloatingWeaponSystem` 实体消失；`SM_AI.Event_AddMasterAI` 发出后，客户端加载蓝质/金质 Prefab，视觉颜色切换正确（蓝色 or 金色 Capsule）
- [ ] 升品质后新武器仍跟随玩家（`ServerBIU26FloatingWeaponMove` 正常运行，MasterGPO 正确传入）并自动锁敌攻击（`ServerBIU26FloatingWeaponAttack` 正常运行）
