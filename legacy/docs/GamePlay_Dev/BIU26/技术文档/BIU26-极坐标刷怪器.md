# BIU26-极坐标刷怪器

> **文档版本**：v0.1（占位框架，等 GPO 工程师填充）
> **创建时间**：2026-03-28
> **负责 Agent**：GPO 工程师
> **Agent 定位**：[[GPO_Programmer]]（GPO 工程师进场后必须声明已熟读）
> **父文档**：`aigc/docs/Dev_Lead/BIU26/BIU26_开发计划.md`
> **状态**：⬜ 等 GPO 工程师填充

---

> ⚠️ **本框架由 DL（开发负责人）预填，GPO 工程师接手后须：**
> 1. 在文档顶部声明「已熟读 [[GPO_Programmer]]」
> 2. 将所有 `[GPO工程师填充]` 标记替换为实际内容
> 3. 完成后将状态改为 `✅ 已完成`

---

## S-02：参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| GPO 工程师 | 开发范例 | GPO 参考范例.md | [[GPO 参考范例]] |
| GPO 工程师 | 边界定义 | UGC GPO 内容边界定义.md | [[UGC GPO 内容边界定义]] |
| GPO 工程师 | 规则 | AIGC 会话调度规范.md | `aigc/harness/rules/AIGC 会话调度规范.md` |
| GPO 工程师 | 规则 | safety-rules.md | [[safety-rules]] |
| GPO 工程师 | 规则 | core-rules.md | [[GamePlay_Dev/core-rules]] |
| GPO 工程师 | 规则 | shader-code.md | [[shader-code]] |
| GPO 工程师 | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| GPO 工程师 | 规则 | gpo-code.md | [[gpo-code]] |

---

## S-03：功能需求

[GPO工程师填充] — 一句话描述：玩家拿到极坐标刷怪器后，小怪持续在玩家周围 4~12m 范围内刷出，随玩家移动动态更新刷怪圆心，保证始终有怪可打。

---

## S-04：功能定位

本文档覆盖 BIU26 Phase 1 **极坐标刷怪器 GPO** 全部职责：GPO 配表数据（GPOM_BIU26Set）、路由注册（Gpo/GpoTypeSet/IGPOM/Switch）、服务端刷怪 System（ServerBIU26SpawnerSystem + ServerBIU26MinionsSpawner）、客户端占位 System（ClientBIU26SpawnerSystem）、双 Prefab。**不包含**悬浮武器解锁逻辑（见 BIU26-模式系统.md）。

---

## S-05：文件清单

[GPO工程师填充，下方为 DL 预拟框架，GPO工程师确认后补全]

### 📋 配表层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Template/gpo/GPOM_BIU26Set.cs` | **新建**（手动编写，非 csv-gen） | 承载 BIU26 极坐标刷怪器 GPO struct（GPOM_BIU26Spawner）及其静态数据集 |
| `Assets/Scripts/Template/data/Gpo.cs` | **修改**（data 数组追加行） | 追加 `new Gpo(BIU26_SPAWNER_ID, ...)` 极坐标刷怪器数据行 |
| `Assets/Scripts/Template/gpo/GpoTypeSet.cs` | **修改**（追加常量） | 追加 `Id_BIU26Spawner` GPO 类型 ID 常量 |
| `Assets/Scripts/Template/gpo/IGPOM.cs` | **修改**（追加 switch case） | `GetGPOMData` 新增 `case GpoTypeSet.Id_BIU26Spawner:` 路由 |

### 🔀 路由注册层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs` | **修改**（追加 case） | `AddAIForGpoMTypeId` 新增 `case GpoTypeSet.Id_BIU26Spawner:` 分支，返回 `ServerBIU26SpawnerSystem` |
| `Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs` | **修改**（追加 case） | 同上，客户端侧新增对应分支，返回 `ClientBIU26SpawnerSystem` |

### 🖥️ 服务端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26SpawnerSystem.cs` | **新建** | 继承 `S_AI_Base`，极坐标刷怪器服务端 System，OnStart 挂载 `ServerBIU26MinionsSpawner` |
| `Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26MinionsSpawner.cs` | **新建** | 继承 `ServerNetworkComponentBase`，以玩家当前位置为圆心、内径4m/外径12m 动态计算刷怪位置 |

### 💻 客户端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26SpawnerSystem.cs` | **新建** | 继承 `C_AI_Base`，极坐标刷怪器客户端 System（无视觉表现，仅实体占位） |

### 🎨 资产层

| 资产路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Prefabs/AI/Server/BIU26SpawnerServer.prefab` | **新建** | 极坐标刷怪器服务端 Prefab（空节点 + 碰撞体占位） |
| `Assets/Prefabs/AI/Client/BIU26Spawner.prefab` | **新建** | 极坐标刷怪器客户端 Prefab（空节点，无 Renderer） |

---

## S-06：ASCII 交互链路图

[GPO工程师填充，下方为 DL 预拟刷怪链路]

### 极坐标刷怪链路

```
[服务端] ServerBIU26MinionsSpawner.OnUpdate(delta)
    ├─ 游戏状态 != RoundStart → 跳过
    ├─ ownerGPO == null 或已清理 → 跳过
    ├─ livingCount >= maxLiving → 跳过
    ├─ spawnerTimer += delta
    ├─ spawnerTimer < spawnInterval → 等待
    │       ↓ 超时
    ├─ spawnerTimer = 0
    ├─ ownerPos = ownerGPO.GetPoint()
    ├─ 极坐标随机采样:
    │     angle = Random(0, 360°) * Deg2Rad
    │     r     = Random(innerRadius=4, outerRadius=12)
    │     spawnPos = ownerPos + (cos(angle)*r, 0, sin(angle)*r)
    ├─ MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
    │       AISign = "BIU26_Minion_Normal",  // [GPO工程师确认此 Sign]
    │       StartPoint = spawnPos,
    │       OR_CallBack = ai => {
    │           livingCount++
    │           监听小怪死亡 → livingCount--
    │                        → ownerGPO.Dispatcher(SE_BIU26.Event_MinionKilled)
    │       }
    │   })
    └─ 下帧继续
```

---

## S-07：灰盒资源占位

[GPO工程师填充]

| 对象 | 灰盒形状 | 颜色（_BaseColor RGBA） | 尺寸 | 挂点偏移 |
|------|---------|----------------------|------|---------|
| 小怪（普通） | Capsule | (0.5, 0.5, 0.5, 1.0) 灰色 | 高1.8m，半径0.4m | N/A（独立 GPO） |
| 小怪（精英） | Capsule | (0.2, 0.4, 1.0, 1.0) 蓝色 | 高2.2m，半径0.5m | N/A |
| 小怪（头目） | Capsule | (1.0, 0.7, 0.0, 1.0) 金色 | 高3.0m，半径0.7m | N/A |

---

## S-08：边界条件

[GPO工程师填充，下方为 DL 预拟]

### 8.1 依赖的外部接口

| 接口 | 来源 | 说明 |
|------|------|------|
| `SM_AI.Event_AddAI` | 现有框架 | 刷怪调用；AISign 需与小怪配表对齐 |
| `SE_GPO.Event_SetOnDeadCallBack` | 现有框架（待核查） | 小怪死亡回调；**GPO工程师必须在开发前核查此接口是否存在** |
| `SE_BIU26.Event_MinionKilled` | 本计划新建 | 通知玩家 GPO 上的 FloatingWeaponManager |
| ownerGPO（玩家 GPO） | BIU26Mode 传入 | Spawner 生成时通过 InitData 绑定玩家 GPO |

### 8.2 禁止做的事

| 禁止项 | 原因 |
|--------|------|
| 修改任何 Base 类源码 | 违反 safety-rules.md |
| 在现有 ServerGPOSpawnerWaveMainLoop 上直接改逻辑 | 影响其他模式刷怪系统 |
| 将极坐标刷怪器逻辑混入 ServerBIU26Mode | 职责分离原则 |

### 8.3 边界文档引用

- [[safety-rules]]
- [[UGC GPO 内容边界定义]]

---

## S-09：验收标准

[GPO工程师填充，下方为 DL 预拟]

### 9.1 编译验收

- [ ] `GPOM_BIU26Set.cs` 新建后编译通过，无报错
- [ ] `Gpo.cs` / `GpoTypeSet.cs` / `IGPOM.cs` 追加行后编译通过
- [ ] Switch 路由两处追加 case 后，现有所有 GPO 路由不受影响

### 9.2 功能验收（运行时）

- [ ] 玩家入局后，小怪持续在其周围 4~12m 范围内刷出（可通过 Gizmos 或 Debug.DrawLine 在 Scene 视图确认刷怪圆圈）
- [ ] 玩家移动 20m 后，新一批小怪以新位置为圆心刷出（不再以初始位置为圆心）
- [ ] 场景内同时存活小怪数量不超过 maxLiving 上限

### 9.3 集成验收

- [ ] `ServerAIWorld_Switch` + `ClientAIWorld_Switch` 新增 case 不影响现有所有 GPO 类型正常路由
- [ ] 小怪死亡后，`SE_BIU26.Event_MinionKilled` 正确触发，玩家 GPO 上的 FloatingWeaponManager 收到通知

---

## 附录：骨架代码（DL 预拟）

### ServerBIU26MinionsSpawner.cs

```csharp
// Assets/Scripts/GamePlay/Server/AI/Components/GPOSpawner/ServerBIU26MinionsSpawner.cs
// 职责：以绑定玩家位置为圆心，在 [innerRadius, outerRadius] 极坐标范围内动态刷出小怪

using UnityEngine;
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Message;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26MinionsSpawner : ServerNetworkComponentBase {

        public struct InitData : SystemBase.IComponentInitData {
            public IGPO   OwnerGPO;
            public string MinionSign;   // TODO：等 GPO 工程师确认后填入
            public float  InnerRadius;  // 默认 4m
            public float  OuterRadius;  // 默认 12m
            public float  SpawnInterval;// 默认 1.5s
            public int    MaxLiving;    // 默认 20
        }

        private IGPO   ownerGPO;
        private string minionSign;
        private float  innerRadius, outerRadius, spawnInterval;
        private int    maxLiving;
        private float  timer       = 0f;
        private int    livingCount = 0;

        protected override void OnAwake() {
            base.OnAwake();
            var init     = (InitData)initDataBase;
            ownerGPO     = init.OwnerGPO;
            minionSign   = init.MinionSign;
            innerRadius  = init.InnerRadius   > 0 ? init.InnerRadius   : 4f;
            outerRadius  = init.OuterRadius   > 0 ? init.OuterRadius   : 12f;
            spawnInterval= init.SpawnInterval > 0 ? init.SpawnInterval : 1.5f;
            maxLiving    = init.MaxLiving     > 0 ? init.MaxLiving     : 20;
        }

        protected override void OnStart() { base.OnStart(); AddUpdate(OnUpdate); }
        protected override void OnClear() { base.OnClear(); RemoveUpdate(OnUpdate); ownerGPO = null; }

        private void OnUpdate(float delta) {
            if (ModeData.PlayGameState != ModeData.GameStateEnum.RoundStart) return;
            if (ownerGPO == null || ownerGPO.IsClear()) return;
            if (livingCount >= maxLiving) return;
            timer += delta;
            if (timer < spawnInterval) return;
            timer = 0f;
            SpawnMinion();
        }

        private void SpawnMinion() {
            var   ownerPos = ownerGPO.GetPoint();
            float angle    = Random.Range(0f, 360f) * Mathf.Deg2Rad;
            float r        = Random.Range(innerRadius, outerRadius);
            var   spawnPos = new Vector3(ownerPos.x + Mathf.Cos(angle) * r, ownerPos.y, ownerPos.z + Mathf.Sin(angle) * r);

            MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
                AISign      = string.IsNullOrEmpty(minionSign) ? "BIU26_Minion_Normal" : minionSign,
                StartPoint  = spawnPos,
                OR_GpoType  = GPOData.GPOType.AI,
                OR_CallBack = ai => {
                    livingCount++;
                    ai.Dispatcher(new SE_GPO.Event_SetOnDeadCallBack {
                        CallBack = killerGPO => {
                            livingCount--;
                            ownerGPO?.Dispatcher(new SE_BIU26.Event_MinionKilled { KillerGPO = killerGPO });
                        }
                    });
                }
            });
        }
    }
}
```

---

*文档版本 v0.1（占位框架） — BIU26-极坐标刷怪器，2026-03-28（DL 预填，等 GPO 工程师接手）*
