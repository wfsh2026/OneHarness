# 镜头系统 + 辅助瞄准开发规则

> **适用场景**：涉及镜头行为修改 / 辅助瞄准新增或配置 / 新模式接入镜头系统
> **关键文件**：
> - `Assets/Scripts/GamePlay/Client/Camera/Componet/CameraAimAssist.cs`
> - `Assets/Scripts/Template/data/AimAssist.cs`（由 csv-gen 生成，禁止手动改此文件）
> - `Assets/Scripts/Template/data/GpoAimAssist.cs`（同上，csv-gen 生成）
> - `Assets/Scripts/Message/GamePlay/Client/World/CM_Camera.cs`（镜头消息定义）

---

## 一、镜头系统架构概览

```
CameraSystem（镜头总入口）
├── CameraMove         — 镜头移动（位置跟随）
├── CameraRota         — 镜头旋转（输入处理）
├── CameraAimAssist    — 辅助瞄准（减速 + 吸附）← 本文档重点
├── CameraFar          — 镜头远近（距离控制）
├── CameraShake        — 镜头震动
├── CameraCollisionHandler — 碰撞处理
├── CameraAutoLockTarget   — 自动锁定目标（独立模块）
├── GetCameraVisibleGPO    — 可见GPO检测
└── GetCameraCenterGPO     — 中心GPO检测（用于辅助瞄准目标选取）
```

---

## 二、辅助瞄准系统（CameraAimAssist）

### 2.1 系统原理（双层控制）

辅助瞄准 = **减速层** + **吸附层**，两层独立计算，共同作用于每帧的镜头旋转 Delta。

```
玩家输入 Delta
    │
    ▼
[减速层] 若 slowDownGpo 在减速判定圈内：
    finalDelta = Delta × (1 - slowDownRate × pow)
    // pow 越小(越靠近中心) → 减速越强
    │
    ▼
[输出] CM_Camera.SetDelta（最终镜头旋转量）

[吸附层] 独立运行（每帧更新 cameraLockRate）：
    通过 CE_Camera.GetCameraScrollSpeedRate 供 CameraRota 读取
    控制镜头"跟随"目标移动的程度
```

### 2.2 判定圈计算方式（重要）

辅助瞄准**不用"屏幕距离"判断**，而是用**世界坐标中的物理半径**转换为角度：

```csharp
// GetGpoAngle 中：
maxAngle = Vector3.Angle(targetDir, targetDir + new Vector3(0, radius, 0));
// radius = GpoAimAssist.LockMaxRadius 或 SlowDownMaxRadius
// 含义：目标头顶竖直向上 radius 米处形成的角度 = 判定圈"角半径"
```

**含义**：
- `LockMaxRadius = 1.0f` → 目标上方 1m 对应的张角 = 吸附判定圈
- `SlowDownMaxRadius = 1.2f` → 目标上方 1.2m 对应的张角 = 减速判定圈
- 距离越远 → 同等物理半径对应的角度越小 → **辅助越难触发**

### 2.3 吸附系数与转速的关系

| 转速区间 | 吸附系数（cameraLockRate） |
|---------|--------------------------|
| ≤ 50°/s（慢速）| `CameraLowLockRate = 0.2`（较强吸附）|
| 50-400°/s（中速）| 线性插值 `[0.2 → 0]` |
| ≥ 400°/s（快速）| `CameraHighLockRate = 0.0`（完全跟随，吸附最强）|

> ⚠️ 注意：转速越"高"，吸附系数越低（0 = 完全跟随目标，不是"不跟随"）

### 2.4 减速系数与转速的关系

| 转速区间 | 减速系数（cameraSlowDownRate） |
|---------|-------------------------------|
| ≤ 50°/s | `CameraLowSlowDownRate = 0.5`（减速50%）|
| 50-400°/s | 线性插值 `[1.0 → 0.5]` |
| ≥ 400°/s | `CameraHighSlowDownRate = 0.2`（减速20%）|

---

## 三、新 GPO 接入辅助瞄准的完整步骤（必读）

> **新GPO必须在 GpoAimAssist 配置表中注册，否则会报 LogError 并使用兜底半径2m**

### 步骤 1：确定 GPO 的 GpoTypeId

在 `Template/data/Gpo.cs` 或 `GpoTypeSet` 中找到你的 GPO ID 的整数值。

### 步骤 2：在 GpoAimAssist.cs 配置表末尾追加行

⚠️ **`GpoAimAssist.cs` 由 csv-gen 自动生成，需通过 CSV 源文件修改，不能手动改 .cs 文件！**

找到 CSV 源文件（通常在 `Assets/CSVData/` 或 `TextToolDatas/` 目录下），追加一行：

```csv
Id,LockMaxRadius,SlowDownMaxRadius,GpoTypeId
{下一个空闲ID},{吸附半径},{减速半径},{你的GpoTypeId}
```

**参考数值选择**：

| 目标体型 | LockMaxRadius | SlowDownMaxRadius |
|---------|--------------|-----------------|
| 小型（≤0.6x Capsule）| 0.8 | 1.0 |
| 标准（1x Capsule）| 1.0 | 1.2 |
| 大型（Boss级）| 1.5 | 2.6 |
| 极小/不需要辅助 | 0.1 | 0.1 |

### 步骤 3：重新生成 .cs 数据文件

运行 csv-gen 工具生成新的 `GpoAimAssist.cs`，或直接在 `.cs` 末尾的 `Data` 数组追加一行（**仅临时调试可用，正式代码必须走csv流程**）。

### 步骤 4：（可选）模式入场时切换 AimAssist 配置

若新模式需要不同的辅助强度（如 PvP 弱化辅助、PvE 强化辅助）：

```csharp
// 在 ClientBIU26Mode.OnEnter 中发送：
MsgRegister.Dispatcher(new CM_Camera.SetAimAssistConfig {
    Config = AimAssistSet.GetAimAssistById(2) // 使用不同的配置ID
});
// 模式退出时恢复：
MsgRegister.Dispatcher(new CM_Camera.SetAimAssistConfig {
    Config = AimAssistSet.GetAimAssistById(1) // 恢复默认
});
```

### 步骤 5：（可选）动态调整判定圈大小

```csharp
// 放大吸附判定圈（适合快节奏模式）
MsgRegister.Dispatcher(new CM_Camera.SetLockCircleRadiusScale { Scale = 1.5f });
// 放大减速判定圈
MsgRegister.Dispatcher(new CM_Camera.SetSlowDownCircleRadiusScale { Scale = 1.5f });
// 恢复默认
MsgRegister.Dispatcher(new CM_Camera.SetLockCircleRadiusScale { Scale = 1f });
```

---

## 四、关闭辅助瞄准的方法

| 场景 | 实现方式 |
|------|---------|
| 彻底关闭（不需要辅助的GPO）| 配置 `LockMaxRadius = 0.1, SlowDownMaxRadius = 0.1`（极小判定圈）|
| 模式级别关闭（如PvP对玩家）| 玩家GPO不在 GpoAimAssist 表中，系统会报 LogError。应用 `GodMode` Tag 也会自动跳过 |
| 临时禁用 | 发送 `SetLockCircleRadiusScale { Scale = 0 }` 和 `SetSlowDownCircleRadiusScale { Scale = 0 }` |

**系统自动跳过的情况**（`UpdateSlowDownGpo` 中实现）：
- 目标 GPO 已清除（`IsClear()`）
- 目标有 `GodMode` Tag（无敌状态）
- 目标有 `Dead` Tag（已死亡）
- 目标不在减速判定圈范围内

---

## 五、常用消息速查（CM_Camera 相关）

| 消息类 | 方向 | 用途 |
|--------|------|------|
| `CM_Camera.SetAimAssistConfig` | 外部 → CameraAimAssist | 切换辅助瞄准配置（模式入场/退出时用）|
| `CM_Camera.SetLockCircleRadiusScale` | 外部 → CameraAimAssist | 动态缩放吸附判定圈 |
| `CM_Camera.SetSlowDownCircleRadiusScale` | 外部 → CameraAimAssist | 动态缩放减速判定圈 |
| `CM_Camera.GetCameraLockRate` | 外部 → CameraAimAssist | 查询当前帧吸附系数（调试用）|
| `CM_Camera.GetGpoIsInAimValid` | 外部 → CameraAimAssist | 查询某 GPO 是否在判定圈内 |
| `CM_Camera.FindCenterGPOInFrontForLockRadius` | CameraAimAssist → 系统 | 内部：查找准星前方最近 GPO |

---

## 六、注意事项 & 常见错误

| ⚠️ 问题 | 原因 | 解决方案 |
|---------|------|---------|
| 控制台报 `gpo 辅助瞄准表未配置, id X` | 新 GPO 没有在 GpoAimAssist 表中注册 | 按步骤2~3在表中追加该 GPO 的配置行 |
| 新模式 PvP 阶段辅助瞄准对玩家生效 | 玩家 GPO 如果在表里（且无 GodMode/Dead Tag），会被当做辅助目标 | 玩家 GPO 不应加入 GpoAimAssist 表，或在 PvP 模式入场时 SetLockCircleRadiusScale=0 |
| 辅助强度在快速转镜时突然变弱 | 正常设计：高转速时吸附系数降低（避免对快速追踪的玩家造成"卡镜"感）| 无需修复，如需改变强度比例，修改 AimAssist 配置的中速插值范围 |
| GpoAimAssist.cs 手动修改后被覆盖 | csv-gen 重新生成覆盖手改 | 永远通过 CSV 源文件修改，再走 csv-gen 流程 |

---

*由 [DL] 整理，2026-03-27。后续镜头模块有新 API 时，由相关开发人员更新此文档。*
