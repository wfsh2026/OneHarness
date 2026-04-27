# BIU26-缩圈系统

> **文档版本**：v1.0
> **创建时间**：2026-03-29
> **负责 Agent**：开发负责人 (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：[[BIU26_开发计划]]
> **状态**：⬜ 待开发

---

## S-02：参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| 开发负责人 (DL) | 开发范例 | 模式参考范例.md | [[模式参考范例]] |
| 开发负责人 (DL) | 边界定义 | 模式系统内容边界定义.md | [[模式系统内容边界定义]] |
| 开发负责人 (DL) | 规则 | AIGC 会话调度规范.md | `aigc/harness/rules/AIGC 会话调度规范.md` |
| 开发负责人 (DL) | 规则 | safety-rules.md | [[safety-rules]] |
| 开发负责人 (DL) | 规则 | core-rules.md | [[GamePlay_Dev/core-rules]] |
| 开发负责人 (DL) | 规则 | shader-code.md | [[shader-code]] |
| 开发负责人 (DL) | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| 开发负责人 (DL) | 规则 | plan-doc.md | [[plan-doc]] |
| 开发负责人 (DL) | 规则 | mode-code.md | [[mode-code]] |

---

## S-03：功能需求

游戏进行到约 2 分钟时，玩家发现场景中出现一个可见的圆形安全区边界。随着时间推进，安全区在 2:30 开始生效——站在圈外的玩家每秒会受到持续 HP 扣减，产生「我要赶紧进圈」的移动压力。每当玩家率先进入新安全圈，获得一笔金币奖励，形成割草发育与战略移动的抉择张力。三圈收缩最终将所有玩家强制聚集，促成终局对抗。

---

## S-04：功能定位

本文档覆盖 BIU26 Phase 2 的**缩圈规则层**：游戏时序驱动（ZoneStage 状态机）、圈外持续伤害（HP 扣减）、进圈金币奖励、客户端安全区边界视觉。**不包含** PVP 伤害（框架原生支持，无需开发）、地图布局（见 BIU26-场景建设.md，ZoneMarker 已在场景中）。

---

## S-05：文件清单

### 🖥️ 服务端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerBIU26ZoneSystem.cs` | **新建** | Zone 时序状态机 + 圈外 HP 持续伤害 + 进圈金币判断 |
| `Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerBIU26Mode.cs` | **修改** | `OnAddCharacterCallBack` 中追加 `AddComponent<ServerBIU26ZoneSystem>()` |
| `Assets/Scripts/Message/GamePlay/Server/System/SE_BIU26.cs` | **修改** | 追加 `Event_ZoneStageChanged`（通知客户端显示哪一圈边界）|

### 💻 客户端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/Mode/Components/ClientBIU26ZoneSystem.cs` | **新建** | 接收 `Event_ZoneStageChanged` RPC → 更新场景 ZoneVisual LineRenderer 半径并显示 |

### 🔀 路由注册层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Message/GamePlay/Proto/17_Proto_BIU26.cs` | **修改** | 追加 `Func_BIU26ZoneStageChanged` FuncID 常量 |

---

## S-06：ASCII 交互链路图

```
[ServerBIU26ZoneSystem.OnUpdate]
       │
       │ 游戏时间到达阶段阈值
       ▼
 ZoneStage 状态机推进
 (SAFE → ZONE1_WARN → ZONE1_ACTIVE → ...)
       │
       ├─→ [Dispatcher Event_ZoneStageChanged]
       │      → Proto_BIU26 RPC
       │      → ClientBIU26ZoneSystem.OnZoneStageChanged()
       │      → 更新 LineRenderer 圆圈半径并显示/隐藏
       │
       └─→ [圈外伤害(ACTIVE阶段)]
              每 1s 遍历所有玩家
              DistanceTo(ZoneCenter) > ZoneRadius?
              是 → HurtPlayer(player, dmg)
              否 → 无操作

[ServerBIU26ZoneSystem.OnTriggerEnter / 位置检测]
       │ 玩家进入更小安全区（位置从圈外→圈内穿越）
       ▼
  CoinManager.AddCoin(player, 10)
  → Proto 广播 ClientCoinHUD 更新
```

> ZoneMarker（Zone_Outer/Mid/Inner）已在客户端场景，圆心 = 地图 (0,0,0)，半径参考场景 Collider 设置（服务端按相同半径数值做距离检测）。

---

## S-07：灰盒资源占位

| 视觉元素 | 形状 | 颜色（_BaseColor RGBA） | 尺寸/参数 | 挂点/说明 |
|---------|------|----------------------|----------|----------|
| 安全区边界圆圈 | LineRenderer 360段圆形 | 白色 (1,1,1,0.8) → 进入 ACTIVE 变红 (1,0,0,0.8) | 半径 = 当前安全圈半径 | 世界坐标 Y=0.1（略高于地面），挂点 ZoneVisual_Outer/Mid/Inner |

> Phase 2 仅需线框圆圈占位；Phase 3+ 可替换为投影纹理/粒子效果。

---

## S-08：边界条件

### 依赖的外部接口

| 依赖 | 说明 |
|------|------|
| `CoinManager.AddCoin(playerId, amount)` | Phase 1 已实现，进圈时调用 |
| `ZoneMarker.Zone_Inner/Mid/Outer` 的 Collider 半径 | 在客户端场景 BIU26_Dev.unity 中已配置，服务端用同等半径数值 |
| `HurtPlayer / 伤害接口` | 圈外持续伤害，需确认框架的玩家持续伤害调用方式（参考模式参考范例） |

### 禁止事项

- 禁止将 ZoneSystem 注册为独立 GPO（它是 Mode 级 ComponentBase，通过 `ServerBIU26Mode.AddComponent<>()` 挂载）
- 禁止在 Component 内部调用 `AddComponent`（违反 core-rules Rule 1.1）
- 禁止修改 ZoneMarker 场景对象的 Collider 半径（它们是场景建设工程师管理的范围）

### Phase 2 附加任务：清理 ZoneMarker Collider

ZoneMarker（OuterZone_Visual / TransitionZone_Visual / CenterZone_Visual）上的 Collider 应**删除**：
- 纯视觉对象不需要 Collider
- Zone 逻辑全部由 `ServerBIU26ZoneSystem` 做服务端距离检测，无需 Trigger 回调
- 删除后不影响客户端 LineRenderer 视觉显示

> 执行：由场景建设工程师在 Phase 2 开发阶段同步完成（BIU26_Dev.unity，删除三个 ZoneMarker 子对象上的 SphereCollider / BoxCollider 组件）。

---

## S-09：验收标准

### 9.1 编译验收

- [ ] `ServerBIU26ZoneSystem.cs`、`ClientBIU26ZoneSystem.cs` 新建后编译 0 错误
- [ ] `SE_BIU26.Event_ZoneStageChanged`、`Proto_BIU26.Func_BIU26ZoneStageChanged` 追加后编译 0 错误

### 9.2 功能验收（运行时）

- [ ] 游戏开始 2:00 后，客户端显示 Zone_Outer 白色圆圈边界
- [ ] 2:30 后，站在 Zone_Outer 边界外的玩家每秒 HP -1%（控制台日志或血条可见）
- [ ] 4:00 后，Zone_Mid 边界出现；4:30 圈外 -2%HP/s
- [ ] 6:00 后，Zone_Inner 边界出现；6:30 圈外 -4%HP/s
- [ ] 圈外伤害颜色提示：圆圈线框在 ACTIVE 阶段变为红色

### 9.3 集成验收（与其他模块联动）

- [ ] 玩家从 Zone_Outer 外进入 Zone_Outer 内，`CoinManager` 加 +8~12 金币，`ClientCoinHUD` 数值跳动可见
- [ ] 多人测试（≥2 人）：圈外伤害各自独立计算，圈内玩家不受影响
- [ ] 缩圈期间 FloatingWeaponManager 解锁/刷怪逻辑继续正常运行，不受 ZoneSystem 干扰

---

## 附：ZoneStage 状态机设计

```csharp
public enum ZoneStage
{
    SAFE,           // 0:00 ~ 2:00
    ZONE1_WARN,     // 2:00 边界显示，尚未伤害
    ZONE1_ACTIVE,   // 2:30 圈外开始 -1%HP/s
    ZONE2_WARN,     // 4:00 Zone_Mid 边界显示
    ZONE2_ACTIVE,   // 4:30 圈外 -2%HP/s
    ZONE3_WARN,     // 6:00 Zone_Inner 边界显示
    ZONE3_ACTIVE,   // 6:30 圈外 -4%HP/s（最终圈）
}

// 时间阈值（秒）
private static readonly float[] StageThresholds = { 0f, 120f, 150f, 240f, 270f, 360f, 390f };

// 各圈参数
// Zone1 (Outer): radius = 40f, dmg = 0.01f × maxHP/s
// Zone2 (Mid):   radius = 25f, dmg = 0.02f × maxHP/s
// Zone3 (Inner): radius = 12f, dmg = 0.04f × maxHP/s
// （具体半径以场景 ZoneMarker Collider 为准）
```

---

*文档版本 v1.0 — BIU26 Phase 2 缩圈系统，2026-03-29*
