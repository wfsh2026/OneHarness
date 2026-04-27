# BIU26-元素反应系统 技术文档

> **文档版本**：v1.2
> **创建时间**：2026-04-01
> **负责 Agent**：开发负责人 (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：[[BIU26_开发计划]]
> **前置文档**：[[BIU26-元素系统基础]]（Phase 3 必须完成）
> **状态**：⬜ 待开发（Phase 3 验收通过后启动）

---

## 参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| 开发负责人 (DL) | 开发范例 | BIU26-元素系统基础.md（`ServerBIU26ElementManager` 架构参考） | [[BIU26-元素系统基础]] |
| 开发负责人 (DL) | 边界定义 | 暂无（元素反应无独立边界定义文件，以本文档 §八 边界条件为准） | — |
| 开发负责人 (DL) | 规则 | AIGC 会话调度规范.md | `aigc/harness/rules/AIGC 会话调度规范.md` |
| 开发负责人 (DL) | 规则 | safety-rules.md | [[safety-rules]] |
| 开发负责人 (DL) | 规则 | core-rules.md | [[GamePlay_Dev/core-rules]] |
| 开发负责人 (DL) | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| 开发负责人 (DL) | 规则 | plan-doc.md | [[plan-doc]] |
| 开发负责人 (DL) | 规则 | gpo-code.md | [[gpo-code]] |

---

## 一、S-03 功能需求

**玩家体验**：当玩家搭配了两种不同元素的悬浮武器同时对一个目标攻击时，会触发显著的组合反应——火+冰触发蒸汽爆裂（清除燃烧层并爆炸 AOE），火+电触发感电燃烧（DOT伤害提升80%并持续弹射4秒），冰+电触发超导连锁（弹射范围从3m扩至8m，覆盖目标从3变7）。同时装备2把或以上同元素武器可获得状态效率加成。玩家开始主动规划武器阵容，体验策略深度。

---

## 二、S-04 功能定位

本文档在 Phase 3（`ServerBIU26ElementManager` 已实现）的基础上，扩展**元素反应触发逻辑**和**同元素增强**：

- 三种元素反应（Fire×Ice / Fire×Electric / Ice×Electric）的检测和爆发效果
- 同元素 ≥2 把武器时，状态施加效率 +50%、持续时间 +30%
- 客户端接收反应触发 RPC，播放三种不同的视觉爆发效果（灰盒颜色闪烁）

**不包含**：Phase 3 的基础状态效果（在元素系统基础文档中已定义）、怪物元素克制、元素克制对 Minion（后续迭代）。

---

## 三、S-05 文件清单

### 📋 数据枚举层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs` | **修改** | 追加 `BIU26ReactionType` 枚举（FireIce=1 蒸发爆裂, FireElectric=2 感电燃烧, IceElectric=3 超导连锁）；追加 `Event_ElementReactionTriggered`（TargetGPO, ReactionType, TriggerPosition）|

### 🔀 路由注册层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Message/Network/9_Proto_Mode.cs` | **修改** | 追加 `Rpc_BIU26ElementReactionTriggered`（FuncID=30，targetGpoId:int, reactionType:byte, posX/posY/posZ:float）；在 `GetProtoDoc()` switch 追加 case 30 |

### 🖥️ 服务端 System 层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26ElementManager.cs` | **修改** | 在 `OnWeaponFiredAtTarget()` 中追加反应检测逻辑（§六代码骨架）；追加同元素增强系数计算；追加三种反应触发方法 `TriggerVaporize/ElectroBurn/Superconduct`；追加 `_reactionStates` 字典跟踪感电燃烧持续状态 |

### 💻 客户端 System 层（必须）

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/Mode/Components/ClientBIU26ElementStatusView.cs` | **修改** | 在 `OnSetNetwork()` 追加注册 `Rpc_BIU26ElementReactionTriggered.ID`；接收后调用 `PlayReactionEffect(reactionType, targetGpoId, pos)` 触发颜色闪烁/缩放动画（灰盒）|

---

## 四、S-06 ASCII 交互链路图

```
─── 元素反应检测链路（扩展 Phase 3 的 OnWeaponFiredAtTarget）─────

[SE_BIU26.Event_WeaponFiredAtTarget] 进入 ServerBIU26ElementManager
    element = _weaponElements[weaponGpoId]
    tid = targetGPO.GetGpoID()
      │
      ▼
【同元素增强系数计算】
    sameElementCount = 持有 element 的武器数量（_weaponElements 中）
    boostMultiplier  = sameElementCount >= 2 ? 1.5f : 1.0f   // 效率+50%
    durationMult     = sameElementCount >= 2 ? 1.3f : 1.0f   // 持续+30%
      │
      ▼
【应用基础状态（使用 boostMultiplier / durationMult 调整后的值）】
    (已有 Phase 3 逻辑，参数乘系数后传入)
      │
      ▼
【反应检测：目标上是否存在另一种元素的活跃状态？】
    hasBurn    = targetGPO.HasTag(GamePlayTagData.TagEnum.BIU26Burning)
    hasFreeze  = targetGPO.HasTag(GamePlayTagData.TagEnum.BIU26Frozen)
    hasElectroBurn = _reactionStates.ContainsKey(tid) && _reactionStates[tid].IsElectroBurn
      │
      ├─ Fire + 已有冰冻(hasFreeze)   → TriggerVaporize(targetGPO, tid)
      ├─ Ice  + 已有燃烧(hasBurn)    → TriggerVaporize(targetGPO, tid)
      ├─ Fire + 已有感电燃烧(hasElectroBurn) → TriggerElectroBurn(targetGPO, tid)
      ├─ Electric + 已有燃烧         → TriggerElectroBurn(targetGPO, tid)
      ├─ Ice  + 已有感电燃烧(hasElectroBurn) → TriggerSuperconduct(targetGPO, tid)
      └─ Electric + 已有冰冻         → TriggerSuperconduct(targetGPO, tid)
      │
      ▼
【广播反应 RPC 给客户端】
    Rpc(Rpc_BIU26ElementReactionTriggered{targetGpoId, reactionType, pos})

─── 三种反应效果详情 ──────────────────────────────────────────────

[TriggerVaporize]  火+冰 → 蒸发爆裂
    清除目标 burnStacks (重置为0)
    清除目标 freezeValues (重置为0)
    AOE damage: 扫描 VaporizeRadius=5m 内所有角色
      └→ 各扣 VaporizeDamage=80 伤害（固定值，非百分比）
    向目标自身加 KnockbackForce（via SE_GPO.Event_Knockback，如框架支持）

[TriggerElectroBurn]  火+电 → 感电燃烧
    _burnStacks[tid] 伤害乘以 1.8（+80% DOT）
    _reactionStates[tid] = {IsElectroBurn=true, Duration=4f}
    在 4 秒内每次电弧弹射 ArcRadius 从 3→3m（不变），但传播 DOT 效果
      └→ 弹射目标也获得 1 层燃烧（传播机制）

[TriggerSuperconduct]  冰+电 → 超导连锁
    清除目标 freezeValues（重置为0，但保留减速debuff）
    _reactionStates[tid] = {IsSuperconduct=true, Duration=5f}
    覆盖电弧参数：SuperconductArcRadius=8m，SuperconductMaxTargets=7

─── 同元素增强 ────────────────────────────────────────────────────

[ServerBIU26ElementManager.CountActiveWeaponsOfElement(element)]
    遍历 _weaponElements → count elements matching target type
    count >= 2 → return 1.5f / 1.3f multipliers
    count  = 1 → return 1.0f / 1.0f

─── 客户端反应视觉 ────────────────────────────────────────────────

[ClientBIU26ElementStatusView.PlayReactionEffect()]
    FireIce(蒸发爆裂)  → 目标白色高亮闪烁 0.3s + 材质快速缩放 1→1.2→1
    FireElectric(感电) → 目标橙紫交替闪烁 4s（每秒交替一次）
    IceElectric(超导)  → 目标蓝白闪烁 0.5s + 颜色渐变恢复
```

---

## 五、S-07 灰盒资源占位

| 视觉元素 | 形状 | 颜色（MaterialPropertyBlock _BaseColor）| 持续时间 | 说明 |
|---------|------|----------------------------------------|---------|------|
| 蒸发爆裂 | 目标模型 | 白色高亮 (1,1,1,1) 闪烁 | 0.3s 单次 | `ClientBIU26ElementStatusView` 通过 Update 临时覆盖颜色后还原 |
| 感电燃烧 | 目标模型 | 橙 (1.0, 0.4, 0) ↔ 紫 (0.6, 0, 1.0) 交替 | 4s 循环 | 每1s切换颜色 |
| 超导连锁 | 目标模型 | 蓝白 (0.3, 0.9, 1) 闪烁 + 渐变恢复 | 0.5s 单次 | 闪烁后 0.5s 内颜色线性插值恢复原色 |
| 蒸发 AOE 范围 | 无（Phase 3.5 灰盒不加范围圈） | — | — | Phase 4 再考虑 AOE 圆圈视觉 |

> Phase 3.5 仅需颜色表现，粒子爆炸、音效等留后续迭代。

---

## 六、核心数值设计

```csharp
// 新增常量（追加到 ServerBIU26ElementManager）
private const float VaporizeRadius         = 5f;    // 蒸发爆裂 AOE 范围
private const int   VaporizeDamage         = 80;    // 蒸发爆裂固定伤害
private const float ElectroBurnDuration    = 4f;    // 感电燃烧持续时间
private const float ElectroBurnDotMult     = 1.8f;  // DOT 提升倍率
private const float SuperconductDuration   = 5f;    // 超导连锁持续时间
private const float SuperconductArcRadius  = 8f;    // 超导弹射范围（替代普通3m）
private const int   SuperconductMaxTargets = 7;     // 超导最多弹射目标数
private const float SameElementEfficiency  = 1.5f;  // 同元素 ≥2 把：效率+50%
private const float SameElementDuration    = 1.3f;  // 同元素 ≥2 把：持续+30%
```

---

## 七、代码骨架（新增/修改部分）

```csharp
// ── 追加到 ServerBIU26ElementManager ──────────────────────────

// 反应状态跟踪（per target）
private struct ReactionState {
    public bool  IsElectroBurn;   // 感电燃烧激活（4s内弹射传DOT）
    public bool  IsSuperconduct;  // 超导连锁激活（8m弹射，7目标）
    public float Duration;        // 剩余持续时间
}
private Dictionary<int, ReactionState> _reactionStates = new();

// ── 修改 OnWeaponFiredAtTarget：追加同元素加成 + 反应检测 ─────

private void OnWeaponFiredAtTarget(SE_BIU26.Event_WeaponFiredAtTarget e) {
    // (原有 Phase 3 逻辑之前，先计算同元素加成系数)
    int sameCount      = CountActiveWeaponsOfElement(element);
    float effMult      = sameCount >= 2 ? SameElementEfficiency : 1f;
    float durMult      = sameCount >= 2 ? SameElementDuration   : 1f;
    // 将 effMult/durMult 传入 Burn/Freeze/Arc 方法的伤害量/持续时间计算中
    // (省略已有逻辑，仅展示新增部分)

    // 反应检测
    CheckAndTriggerReaction(e.WeaponGPO, e.TargetGPO, element, tid);
}

private void CheckAndTriggerReaction(IGPO weaponGPO, IGPO targetGPO,
    SE_BIU26.BIU26ElementType newElement, int tid) {

    // 通过 HasTag 查询元素状态，无需访问 Manager 内部字典
    bool hasBurn    = targetGPO.HasTag(GamePlayTagData.TagEnum.BIU26Burning);
    bool hasFreeze  = targetGPO.HasTag(GamePlayTagData.TagEnum.BIU26Frozen);
    bool hasElectroBurn = _reactionStates.TryGetValue(tid, out var rs) && rs.Duration > 0;

    SE_BIU26.BIU26ReactionType reaction = SE_BIU26.BIU26ReactionType.None;

    switch (newElement) {
        case SE_BIU26.BIU26ElementType.Fire when hasFreeze:
        case SE_BIU26.BIU26ElementType.Ice  when hasBurn:
            TriggerVaporize(targetGPO, tid);
            reaction = SE_BIU26.BIU26ReactionType.FireIce;
            break;
        case SE_BIU26.BIU26ElementType.Fire     when hasElectroBurn:
        case SE_BIU26.BIU26ElementType.Electric when hasBurn:
            TriggerElectroBurn(targetGPO, tid);
            reaction = SE_BIU26.BIU26ReactionType.FireElectric;
            break;
        case SE_BIU26.BIU26ElementType.Ice      when hasElectroBurn:
        case SE_BIU26.BIU26ElementType.Electric when hasFreeze:
            TriggerSuperconduct(targetGPO, tid);
            reaction = SE_BIU26.BIU26ReactionType.IceElectric;
            break;
    }

    if (reaction == SE_BIU26.BIU26ReactionType.None) return;

    var pos = targetGPO.GetPoint();
    Rpc(new Proto_Mode.Rpc_BIU26ElementReactionTriggered {
        targetGpoId  = tid,
        reactionType = (byte)reaction,
        posX = pos.x, posY = pos.y, posZ = pos.z,
    });
}

private void TriggerVaporize(IGPO targetGPO, int tid) {
    _burnStacks.Remove(tid);
    _burnTimers.Remove(tid);
    _freezeValues.Remove(tid);
    _freezeDurations.Remove(tid);
    // 移除冻结 AbilityEffect handle（否则减速 debuff 残留）
    if (_freezeEffects.TryGetValue(tid, out var fx)) { fx?.Remove(); _freezeEffects.Remove(tid); }

    if (characters == null) return;
    var center = targetGPO.GetPoint();
    foreach (var c in characters) {
        var gpo = c.CharacterGPO;
        if (gpo == null || gpo.IsClear()) continue;
        if (gpo.HasTag(GamePlayTagData.TagEnum.Dead)) continue;
        if (Vector3.Distance(gpo.GetPoint(), center) > VaporizeRadius) continue;
        gpo.Dispatcher(new SE_GPO.Event_DownHP { DownHp = VaporizeDamage, AttackGPO = targetGPO });
    }
}

private void TriggerElectroBurn(IGPO targetGPO, int tid) {
    // 提升 DOT 倍率（记录在 _reactionStates，OnUpdate 的 burn tick 读取）
    _reactionStates[tid] = new ReactionState { IsElectroBurn = true, Duration = ElectroBurnDuration };
}

private void TriggerSuperconduct(IGPO targetGPO, int tid) {
    _freezeValues.Remove(tid);
    _freezeDurations.Remove(tid);
    // 移除冻结 AbilityEffect handle（超导连锁清除冰冻状态）
    if (_freezeEffects.TryGetValue(tid, out var fx)) { fx?.Remove(); _freezeEffects.Remove(tid); }
    _reactionStates[tid] = new ReactionState { IsSuperconduct = true, Duration = SuperconductDuration };
}

private int CountActiveWeaponsOfElement(SE_BIU26.BIU26ElementType element) {
    int count = 0;
    foreach (var kv in _weaponElements)
        if (kv.Value == element) count++;
    return count;
}

// OnUpdate 修改：UpdateReactionStates + 感电燃烧对 BurnDamage 的影响
private void UpdateBurnDamage(float dt) {
    // (原有逻辑) ...
    // 新增：若目标有 ElectroBurn 状态，dmg *= ElectroBurnDotMult
    if (_reactionStates.TryGetValue(tid, out var rs) && rs.IsElectroBurn && rs.Duration > 0) {
        dmg = Mathf.RoundToInt(dmg * ElectroBurnDotMult);
    }
}

private void UpdateReactionStates(float dt) {
    var toRemove = new List<int>();
    foreach (var key in new List<int>(_reactionStates.Keys)) {
        var state = _reactionStates[key];
        state.Duration -= dt;
        if (state.Duration <= 0f) {
            toRemove.Add(key);
        } else {
            _reactionStates[key] = state;
        }
    }
    foreach (var id in toRemove) _reactionStates.Remove(id);
}

// ApplyArcBounce 修改：若目标存在超导，使用扩展参数
private void ApplyArcBounce(IGPO weaponGPO, IGPO primaryTarget) {
    var tid = primaryTarget.GetGpoID();
    float arcR    = (_reactionStates.TryGetValue(tid, out var rs) && rs.IsSuperconduct)
                    ? SuperconductArcRadius : ArcRadius;
    int   maxTgts = (_reactionStates.TryGetValue(tid, out var rs2) && rs2.IsSuperconduct)
                    ? SuperconductMaxTargets : ArcMaxTargets;
    // (原有弹射逻辑，用 arcR 和 maxTgts 替代常量)
}
```

---

## 八、S-08 边界条件

### 依赖的外部接口

| 依赖 | 说明 |
|------|------|
| `ServerBIU26ElementManager`（Phase 3） | Phase 3.5 是对其的扩展，**必须** Phase 3 编译通过后才能在此基础上修改 |
| `SE_BIU26.BIU26ElementType` | Phase 3 已定义，Phase 3.5 只追加 `BIU26ReactionType` 枚举 |
| `SE_GPO.Event_DownHP` | 蒸发 AOE 使用，与 Phase 3 的燃烧 DOT 调用方式一致 |
| `SE_BIU26.Event_WeaponFiredAtTarget` | Phase 3 已实现，Phase 3.5 在 `OnWeaponFiredAtTarget()` 末尾追加反应检测 |

### 反应触发优先级规则

- 每帧只检测一次反应（不会一帧同时触发多个反应）
- 优先顺序：**蒸发爆裂 > 感电燃烧 > 超导连锁**（switch 顺序决定）
- 反应触发后不立即清除对应元素状态，由各 Trigger 方法自行决定是否清除

### 禁止事项

- **禁止** 对 Minion GPO 触发元素反应（Phase 3.5 仅限玩家 vs 玩家场景）
- **禁止** 同时叠加多个反应状态——新反应触发时必须覆盖旧反应状态
- **禁止** 蒸发 AOE 对触发者自身造成伤害（用 `if (gpo == weaponGPO.GetMasterGPO()) continue` 跳过）
- **禁止** Phase 3.5 文档对应的代码在 Phase 3 `ServerBIU26ElementManager` 未实现的情况下开发

---

## 九、S-09 验收标准

### 9.1 编译验收

- [ ] `SE_BIU26.cs` 追加 `BIU26ReactionType` 枚举后编译 0 错误
- [ ] `9_Proto_Mode.cs` 追加 FuncID=30 的 `Rpc_BIU26ElementReactionTriggered` 及 `GetProtoDoc()` case 后编译 0 错误
- [ ] 修改后的 `ServerBIU26ElementManager.cs` 编译 0 错误
- [ ] 修改后的 `ClientBIU26ElementStatusView.cs` 编译 0 错误

### 9.2 功能验收（运行时）

- [ ] 火武器命中已被冰武器冰冻的目标，触发蒸发爆裂：冰冻状态立即清除，5m内所有角色各受 80 伤害（控制台日志可见），客户端对应目标白色闪烁
- [ ] 电武器命中燃烧目标，触发感电燃烧：接下来 4 秒内 DOT 伤害为正常的 1.8 倍（控制台伤害数值可对比）
- [ ] 超导连锁触发后，弹射范围显示为 8m（可在日志打印 arcR 值确认），目标数最多 7 个
- [ ] 同元素 ≥2 把：Burn DOT 伤害 = stacks × 5 × 1.5 = 正常的1.5倍（日志可见）；冻结积累速度 +50%（触发冻结需 `100/1.5≈67` 次命中而非 4 次）

### 9.3 集成验收（与其他模块联动）

- [ ] 游戏结束后，`_reactionStates` 字典清空，无残留状态影响下局
- [ ] Phase 3 基础状态效果（Burn/Freeze/Arc）在 Phase 3.5 开发后仍正常独立运作，反应不破坏基础状态的独立逻辑
- [ ] 6把武器全混合元素时（如2火2冰2电），三种反应均可正常触发，不互相阻塞

---

*文档版本 v1.2 — BIU26 Phase 3.5 元素反应系统，2026-04-01 同步更新：状态检测改为 HasTag，反应触发清除冻结时 Remove AbilityEffect handle*
