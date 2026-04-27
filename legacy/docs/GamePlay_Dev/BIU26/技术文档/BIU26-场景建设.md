y# BIU26-场景建设

> **文档版本**：v0.2（DL 根据 BIU26地图设计.md 补全场景结构图）
> **创建时间**：2026-03-28
> **负责 Agent**：场景建设工程师
> **Agent 定位**：[[Scene_Builder]]（场景建设工程师进场后必须声明已熟读）
> **父文档**：`aigc/docs/Dev_Lead/BIU26/BIU26_开发计划.md`
> **状态**：🔄 DL 代理创建双场景灰盒（Unity MCP），场景工程师接手后确认坐标+完善细节

---

> ⚠️ **本框架由 DL（开发负责人）预填，场景建设工程师接手后须：**
> 1. 在文档顶部声明「已熟读 [[Scene_Builder]]」
> 2. 将所有 `[场景工程师填充]` 标记替换为实际内容
> 3. 完成后将状态改为 `✅ 已完成`

---

## S-02：参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| 场景建设工程师 | 开发范例 | 暂无 | — |
| 场景建设工程师 | 边界定义 | 暂无 | — |
| 场景建设工程师 | 规则 | AIGC 会话调度规范.md | `aigc/harness/rules/AIGC 会话调度规范.md` |
| 场景建设工程师 | 规则 | safety-rules.md | [[safety-rules]] |
| 场景建设工程师 | 规则 | shader-code.md | [[shader-code]] |
| 场景建设工程师 | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| 场景建设工程师 | 规则 | scene-code.md | [[scene-code]] |

---

## S-03：功能需求

[场景工程师填充] — 一句话描述：为 BIU26 Phase 1 提供可运行的双场景（客户端 + 服务端），玩家进入后可在 120m×120m 灰盒平坦地形内测试完整的发育循环。

---

## S-04：功能定位

本文档覆盖 BIU26 Phase 1 **场景建设**全部职责：客户端测试场景（BIU26_Dev.unity）和服务端测试场景（BIU26_Dev_Server.unity）。**职责边界**：仅负责场景文件本身；GPO Spawner 等对象由 `ServerBIU26Mode.OnStart()` 代码动态生成，不手动拖放到 Hierarchy。

---

## S-05：文件清单

[场景工程师填充，下方为 DL 预拟框架]

### 🗺️ 场景层

| 资产路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scenes/Runtime/BIU26_Dev.unity` | **新建** | BIU26 客户端开发测试场景（含地形、摄像机、UI Canvas）；Phase 1 用 120m×120m 平坦地形灰盒 |
| `Assets/Scenes/Runtime/ServerBIU26_Dev.unity` | **新建** | BIU26 服务端测试场景；由 `Tools/功能/场景/服务器场景转换`（ServerSceneOptimizer）从客户端场景生成，自动剥离 Renderer，设置 SceneGPOEntity.IsServer=true |

### 📋 场景配置层（按需）

| 资产路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Bundle/Configs/Scene/MapBIU26_Dev_01.asset` | **新建**（若需要）| 场景配置 SO（Mode ID / 出生点 / AI 刷新点） |

---

## S-06：ASCII 交互链路图

### 预期场景设计结构图（基于 BIU26地图设计.md v0.1）

```
═══════════════════════════════════════════════════════
  BIU26 地图俯视布局（120m × 120m 正方形）
═══════════════════════════════════════════════════════

  N
  ▲
  │
  │    ┌──────────────────────────────────────┐
  │    │  [外围区A] NW象限，开阔草地/沙地      │
  │    │  掩体：稀疏（每100㎡约1-2个小石块）   │
  │    │  怪物：普通怪为主，白质武器掉落        │
  │    │                                      │
  │    │     ┌────────────────────────┐       │
  │    │     │  [过渡区] 混合地形圆环  │       │
  │    │     │  掩体：中等（箱子/建筑）│       │
  │    │     │  怪物：普通+精英混合    │       │
  │    │     │  ┌──────────────────┐  │       │
  │    │     │  │  [中心富集区]    │  │       │
  │    │     │  │  约 30m × 30m    │  │       │
  │    │     │  │  🏛️ 地标建筑     │  │       │
  │    │     │  │  高8-10m，全图可见│  │       │
  │    │     │  │  精英+头目怪     │  │       │
  │    │     │  │  蓝质/金质掉落   │  │       │
  │    │     │  │  掩体：极少      │  │       │
  │    │     │  └──────────────────┘  │       │
  │    │     └────────────────────────┘       │
  │    │                                      │
  │    │  [外围区B/C/D] 另外3个象限（同A）    │
  │    └──────────────────────────────────────┘
  │
  └─────────────────────────────────────────────► E

═══════════════════════════════════════════════════════
  安全圈收缩阶段（圆心固定在地图正中心）
═══════════════════════════════════════════════════════

  时间线：
    0:00~2:30  初始圈（半径约60m，覆盖全图）
    2:30~4:00  第1圈（半径→37m，约60%面积）  外围区进圈 ←
    4:00~5:30  第2圈（半径→26m，约30%面积）  过渡区进圈 ←
    5:30~7:00  第3圈（半径→13m，约10%面积）  中心决战  ←

  视觉：圈边缘蓝色光墙（玩家无需看小地图即可感知方向）
```

### 场景层级结构（场景工程师搭建参考）

#### 客户端场景：BIU26_Dev.unity

```
BIU26_Dev (Scene Root)
├── Environment/
│   ├── Terrain_Client (120m×120m，灰盒平坦地形)
│   │    └── 材质：(0.5, 0.7, 0.4, 1.0) 草绿灰
│   ├── CenterLandmark/
│   │    └── Landmark_GrayBox (Cube，约 8m×8m×10m，金色标识)
│   │         位置：(0, 0, 0)（地图正中心）
│   ├── ZoneMarkers/ （Phase 1 开发用，Release 前删除）
│   │    ├── OuterZone_Visual   半径60m圆圈标线（Gizmo/Line）
│   │    ├── TransitionZone_Visual 半径30m
│   │    └── CenterZone_Visual  半径15m
│   └── Lighting/
│        └── DirectionalLight
├── Gameplay/
│   ├── SpawnPoints/
│   │   ├── SpawnPoint_NW (约 -40, 0, 40)   [场景工程师确认]
│   │   ├── SpawnPoint_NE (约  40, 0, 40)
│   │   ├── SpawnPoint_SW (约 -40, 0,-40)
│   │   └── SpawnPoint_SE (约  40, 0,-40)
│   └── Canvas/
│       └── HUD_Root (ClientBIU26CoinHUD 挂载点)
├── Camera/
│   └── Main Camera
└── Managers/（BIU26 客户端入口，具体类名由 DL 补充）
```

#### 服务端场景：ServerBIU26_Dev.unity

```
ServerBIU26_Dev (Scene Root)
├── Colliders/
│   └── Terrain_Server (Plane，无 Renderer，120m×120m 碰撞体)
│        → 用于刷怪 SpawnPos 射线检测落地
├── Boundary/
│   └── Boundary_Collider (Cube 空心，120m×120m×10m)
│        → 防止 GPO 刷到地图外
├── GameMode/
│   └── ServerBIU26Mode_Entry (ServerBIU26Mode 挂载点)
└── SpawnPoints/  （坐标与客户端场景对应）
    ├── SpawnPoint_NW (-40, 0, 40)  [场景工程师确认]
    ├── SpawnPoint_NE ( 40, 0, 40)
    ├── SpawnPoint_SW (-40, 0,-40)
    └── SpawnPoint_SE ( 40, 0,-40)
```

---

## S-07：灰盒资源占位

| 对象 | 灰盒形状 | 颜色（_BaseColor RGBA） | 尺寸 | 挂点偏移 |
|------|---------|----------------------|------|---------|
| 地形（客户端） | Plane/Terrain | (0.5, 0.7, 0.4, 1.0) 草绿灰 | 120m×120m | N/A |
| 地形（服务端碰撞体） | Plane | 无 Renderer | 120m×120m | N/A |

---

## S-08：边界条件

[场景工程师填充]

### 8.1 关键坐标（场景工程师填入）

| 位置 | 名称 | 世界坐标 (x, y, z) |
|------|------|-----------------|
| SpawnPoint_NW | (-40, 0, 40)（建议，场景工程师确认） |
| SpawnPoint_NE | (40, 0, 40)（建议，场景工程师确认） |
| SpawnPoint_SW | (-40, 0, -40)（建议，场景工程师确认） |
| SpawnPoint_SE | (40, 0, -40)（建议，场景工程师确认） |
| 场景中心 | Center | (0, 0, 0)（建议） |
| 场景边界 | Boundary | 120m×120m（建议） |

### 8.2 禁止做的事

| 禁止项 | 原因 |
|--------|------|
| 在场景中手动拖放 GPO / Spawner 对象 | 刷怪器等对象由 ServerBIU26Mode.OnStart() 代码动态生成 |
| 修改任何 Base 类源码 | 违反 safety-rules.md |
| 与已有场景命名冲突 | 可能导致 Build 资源覆盖 |

### 8.3 边界文档引用

- [[safety-rules]]
- [[scene-code]]

---

## S-09：验收标准

[场景工程师填充，下方为 DL 预拟]

### 9.1 编译验收

- [ ] `BIU26_Dev.unity` 和 `BIU26_Dev_Server.unity` 添加到 Build Settings 后编译通过
- [ ] 无缺失资源引用警告

### 9.2 功能验收（运行时）

- [ ] 客户端场景在 Unity Editor Play Mode 下可单独运行，地形加载正常，摄像机正常
- [ ] 服务端场景可被框架正确识别，`ServerBIU26Mode` 挂载点存在且可激活
- [ ] 双场景配对运行时，玩家出生在预设出生点，坐标不为 (0,0,0)

### 9.3 集成验收

- [ ] BIU26 场景运行不影响其他已有 GameMode Scene
- [ ] Build Settings 中新增 BIU26 场景后，整体 Build 通过，无报错

---

*文档版本 v0.2（DL 补全场景结构图） — BIU26-场景建设，2026-03-28*
