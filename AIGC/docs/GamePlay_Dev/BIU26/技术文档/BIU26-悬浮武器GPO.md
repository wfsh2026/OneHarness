# BIU26-悬浮武器GPO 技术文档

---

## S-01：文档定位

本文档覆盖 BIU26 悬浮武器（FloatingWeapon）**独立 GPO 实现全流程**：GPOM 配表、路由注册、服务端 AI System（跟随玩家 + 自动锁敌 + Ability 开火）、客户端 System（视觉跟随 + 水平排列表现）、灰盒资源占位。  
**不包含**：子弹 Ability 内部实现（见 BIU26-悬浮武器Ability.md）；武器解锁触发逻辑（见 BIU26-模式系统.md）。

**父文档**：[BIU26_开发计划.md](../BIU26_开发计划.md)

---

## S-02：参考文档与边界定义

| 类型 | 文档路径 | 关键引用点 |
|------|---------|-----------|
| 开发范例 | [[GPO 参考范例]] | §4 服务端 System 生命周期；§5 客户端 System；`ServerAIFindInsightTarget` 初始化参数 |
| 开发范例 | [[Ability 系统开发范例文档]] | §七 7.1 AB_TrackingMissle（ConfigId 10040）；§八 PlayAbility 调用时序 |
| 边界定义 | `aigc/docs/GamePlay_Dev/biu2-framework/内容边界定义/UGC GPO内容边界定义.md` | GPO 禁止项：禁止在 Server System OnUpdate 中做重型物理检测（改用 FindInsightTarget 的 0.5s 轮询） |
| 边界定义 | `aigc/docs/Dev_Lead/BIU26/BIU26_开发计划.md` §8.2 | Phase 1 禁止项：不允许实现元素系统 / 缩圈 / PVP |
| 规则 | [[gpo-code]] | GPO 命名规范；Sign 注册流程；FuncID 核查要求 |

---

## S-03：架构概览（ASCII）

```
[服务端] ServerBIU26Mode.cs
    └─ (解锁事件) SM_AI.Event_AddAI { AISign = "BIU26_FloatingWeapon" }
         └─ ServerAIWorld → 路由表 case "BIU26_FloatingWeapon"
              └─ ServerBIU26FloatingWeaponSystem  (S_AI_Base)
                   │
                   ├─ [通用组件] ServerAIFindInsightTarget  (0.5s 轮询锁敌)
                   ├─ [通用组件] ServerAIMaster             (跟随玩家 MasterGPO)
                   ├─ [通用组件] ServerAIAttribute          (Atk/HP/Range)
                   └─ [定制组件] ServerBIU26FloatingWeaponAttack ★
                                  └─ 攻击间隔计时 → SM_Ability.PlayAbility
                                       └─ AB_TrackingMissle (ConfigId 10040)
                                            └─ [客户端] 子弹飞行表现

[客户端] ClientBIU26FloatingWeaponSystem  (C_AI_Base)
    └─ [通用组件] ClientAIMaster          (跟随位置同步)
    └─ [定制组件] ClientBIU26FloatingWeaponView ★
                   └─ SlotIndex → 计算水平排列 offset，Cube 灰盒占位
```

---

## S-04：功能边界

| 职责 | 由本 GPO 实现 | 由外部实现 |
|------|-------------|-----------|
| 解锁触发 + 计数 | ❌ | ✅ ServerBIU26FloatingWeaponManager（BIU26-模式系统.md） |
| 跟随玩家运动 | ✅ ServerAIMaster + GPO 框架跟随逻辑 | — |
| 自动锁敌 | ✅ ServerAIFindInsightTarget（0.5s 轮询） | — |
| 发射子弹（Ability 触发） | ✅ ServerBIU26FloatingWeaponAttack | — |
| 子弹伤害判定 | ❌ | ✅ AB_TrackingMissle 内部（BIU26-悬浮武器Ability.md） |
| 客户端视觉跟随 + 排列 | ✅ ClientBIU26FloatingWeaponView | — |
| 水平一排布局 offset 公式 | ✅ Client System（由 SlotIndex 决定位置） | — |

---

## S-05：涉及文件清单

| 文件路径 | 操作类型 | 说明 |
|---------|---------|------|
| `Assets/Scripts/Template/gpo/GPOM_BIU26FloatingWeapon.csv` | **新建（配表）** | GPO 模板配表，csv-gen 生成 .cs |
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26FloatingWeaponSystem.cs` | **新建** | 服务端 AI System，继承 S_AI_Base |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26FloatingWeaponAttack.cs` | **新建** | 定制攻击组件，含锁敌+PlayAbility |
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientBIU26FloatingWeaponSystem.cs` | **新建** | 客户端 AI System，继承 C_AI_Base |
| `Assets/Scripts/GamePlay/Client/AI/Components/ClientBIU26FloatingWeaponView.cs` | **新建** | 客户端视觉跟随+水平排列组件 |
| `Assets/Scripts/GamePlay/Server/AI/World/ServerAIWorld_Switch.cs` | **修改** | 在 switch-case 中增加 `GpoTypeSet.Id_BIU26FloatingWeapon` 路由 |
| `Assets/Scripts/GamePlay/Client/AI/World/ClientAIWorld_Switch.cs` | **修改** | 在 switch-case 中增加对应客户端路由 |
| `Assets/Scripts/Template/GpoTypeSet.cs` | **修改** | 新增 `Id_BIU26FloatingWeapon` 常量 |
| `Assets/Prefabs/AI/Server/BIU26FloatingWeaponServer.prefab` | **新建（灰盒）** | 服务端碰撞体 Prefab（灰盒 Cube） |
| `Assets/Prefabs/AI/Client/BIU26FloatingWeapon.prefab` | **新建（灰盒）** | 客户端渲染 Prefab（品质分档灰盒 Cube） |

---

## S-06：ASCII 交互链路图

### 链路一：服务端 FloatingWeapon GPO AI 攻击链路

```
ServerBIU26FloatingWeaponAttack.OnUpdate(delta)
    ├─ intervalTimer += delta
    ├─ intervalTimer < AttackInterval? → 等待下帧
    │
    ├─ intervalTimer >= AttackInterval
    │       ↓
    │   target = 订阅 SE_AI.Event_SetInsightTarget 获得的最近目标
    │   (由 ServerAIFindInsightTarget 每 0.5s 更新)
    │
    ├─ target == null? → 重置计时器，等待下次锁敌
    │
    └─ target != null
            intervalTimer = 0
            MsgRegister.Dispatcher(new SM_Ability.PlayAbility {
                AbilitySign = AB.AB_BIU26FloatingWeaponBullet,
                InData = new AbilityInData {
                    // [预留桩：等 Ability 工程师确认 AbilityIn_TrackingMissle 字段名]
                    In_StartPoint = thisGPOTransform.position,
                    In_TargetGPO  = target,
                }
            })
                └─ [Ability] AB_TrackingMissle 弹道飞行 → 命中目标 → 扣血
                        └─ [客户端] RPC 广播子弹飞行 + 爆炸特效
```

### 链路二：客户端视觉排列

```
[服务端] TargetRpc_AddAI { aiSkinSign = "BIU26FloatingWeapon", slotIndex = N }
    └─ [客户端] ClientAIWorld_Switch → ClientBIU26FloatingWeaponSystem
         └─ ClientBIU26FloatingWeaponView.OnSetEntityObj()
              └─ slotIndex 读取（由 TargetRpc_AddAI.ExtraData 携带）
                   └─ 计算 localPosition offset:
                        offsetX = (slotIndex - (totalCount-1)/2.0f) * spacing (0.7m)
                        offsetY = 0.8m
                        offsetZ = -1.5m（玩家后方）
                   └─ Cube 灰盒放置在玩家 MasterGPO 的对应偏移位置
                        (通过 ClientAIMaster 跟随主人位移)
```

---

## S-07：灰盒资源占位

| 对象 | 灰盒形状 | 颜色（_BaseColor RGBA） | 尺寸 | 水平排列 offset 公式 |
|------|---------|----------------------|------|---------------------|
| 悬浮武器（白质 Lv.1-2） | Cube | (0.8, 0.8, 0.8, 1.0) 浅灰 | 0.3×0.3×0.3 m | 见链路二 |
| 悬浮武器（蓝质 Lv.3-4） | Cube | (0.2, 0.5, 1.0, 1.0) 蓝色 | 0.42×0.42×0.42 m | 见链路二 |
| 悬浮武器（金质 Lv.5-6） | Cube | (1.0, 0.8, 0.0, 1.0) 金色 | 0.6×0.6×0.6 m | 见链路二 |

**水平排列 offset 公式**（后方 N 把，从中心向两侧均匀展开）：
```
offsetX(i) = (i - (N-1)/2.0f) * spacing   // spacing = 0.7m, i = slotIndex
offsetY    = 0.8f
offsetZ    = -1.5f  // 玩家后方
```

---

## S-08：边界条件与骨架代码

### 8.1 GPOM 配表关键字段

| 字段名 | 建议值 | 说明 |
|-------|-------|------|
| `Id` | `TBD（GPO工程师分配）` | `GpoTypeSet.Id_BIU26FloatingWeapon` 对应值 |
| `Sign` | `"BIU26FloatingWeapon"` | Prefab 路径中的资产名 |
| `Atk` | `300` | 单次子弹伤害基数（策划后续调参） |
| `AttackRange` | `15f` | FindInsightTarget 检测半径 |
| `AttackIntervalTime` | `1.5f` | 每把武器每 1.5 秒发射一次（策划调参） |
| `MaxAttackDistance` | `15f` | 最大射程 |
| `Quality` | `1` | Phase 1 固定白质，后续按 slotIndex 分档 |

### 8.2 ServerBIU26FloatingWeaponSystem.cs 骨架

```csharp
// Assets/Scripts/GamePlay/Server/AI/Systems/ServerBIU26FloatingWeaponSystem.cs
// 职责：悬浮武器 GPO 服务端 AI System
// 参考：ServerAIMachineGunSystem.cs（结构模板）；ServerUAVMove.cs（MasterGPO 跟随）
// 决策归档：方案B（独立GPO，参考UAV）

using Sofunny.BiuBiuBiu2.CoreGamePlay;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26FloatingWeaponSystem : S_AI_Base {
        private GPOM_BIU26FloatingWeapon useMData;

        protected override void OnAwake() {
            useMData = (GPOM_BIU26FloatingWeapon)MData;
            AddComponents();
        }

        protected override void AddComponents() {
            base.AddComponents();  // S_AI_Base 默认通用组件

            AddComponent<ServerAIAttribute>(new ServerGPOAttribute.InitData {
                ATK          = useMData.Atk,
                AttackRange  = useMData.AttackRange,
                MaxHp        = useMData.Hp,
            });

            AddComponent<ServerAIFindInsightTarget>(new ServerAIFindInsightTarget.InitData {
                CheckDistance        = useMData.MaxAttackDistance,
                LayerMask            = LayerData.ServerLayerMask | LayerData.DefaultLayerMask,
                IgnoreTeamId         = TeamId,
                IgnoreCollierTrigger = false,
            });

            AddComponent<ServerBIU26FloatingWeaponAttack>();
        }

        protected override void OnStart() {
            base.OnStart();
            CreateEntity(useMData.Sign + "Server");  // 加载 BIU26FloatingWeaponServer Prefab
        }
    }
}
```

### 8.3 ServerBIU26FloatingWeaponAttack.cs 骨架

```csharp
// Assets/Scripts/GamePlay/Server/AI/Components/ServerBIU26FloatingWeaponAttack.cs
// 职责：定时触发 Ability 攻击，锁敌目标由 ServerAIFindInsightTarget 提供
// 参考：ServerAITrackingMissleAttack.cs（UAV 子弹攻击组件）

using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Message;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26FloatingWeaponAttack : ServerNetworkComponentBase {

        private GPOM_BIU26FloatingWeapon useMData;
        private IEntity currentTarget;
        private float intervalTimer = 0f;

        protected override void OnAwake() {
            var aiSystem = (S_AI_Base)mySystem;
            useMData = (GPOM_BIU26FloatingWeapon)aiSystem.MData;

            // 订阅寻敌结果
            mySystem.Register<SE_AI.Event_SetInsightTarget>(OnInsightTargetChanged);
        }

        protected override void OnClear() {
            mySystem.Unregister<SE_AI.Event_SetInsightTarget>(OnInsightTargetChanged);
        }

        private void OnInsightTargetChanged(ISystemMsg msg, SE_AI.Event_SetInsightTarget evt) {
            currentTarget = evt.TargetGPO;
        }

        protected override void OnUpdate(float delta) {
            if (currentTarget == null) return;

            intervalTimer += delta;
            if (intervalTimer < useMData.AttackIntervalTime) return;

            intervalTimer = 0f;
            MsgRegister.Dispatcher(new SM_Ability.PlayAbility {
                AbilitySign = AB.AB_BIU26FloatingWeaponBullet, // [预留桩：等 Ability 工程师确认常量]
                InData = new AbilityInData {
                    // [预留桩：等 Ability 工程师确认 AbilityIn_TrackingMissle 字段名]
                    // In_StartPoint = GetEntityTransform().position,
                    // In_TargetGPO  = currentTarget,
                }
            });
        }
    }
}
```

### 8.4 ClientBIU26FloatingWeaponView.cs 骨架

```csharp
// Assets/Scripts/GamePlay/Client/AI/Components/ClientBIU26FloatingWeaponView.cs
// 职责：接收 slotIndex，在客户端计算水平排列 offset，持续跟随主人位置

using UnityEngine;
using Sofunny.BiuBiuBiu2.CoreGamePlay;

namespace Sofunny.BiuBiuBiu2.ClientGamePlay {
    public class ClientBIU26FloatingWeaponView : ClientNetworkComponentBase {

        private const float OffsetY     = 0.8f;
        private const float OffsetZ     = -1.5f;
        private const float SlotSpacing = 0.7f;

        private int slotIndex = 0;

        // slotIndex 从 TargetRpc_AddAI.ExtraData 读取（由 ClientBIU26FloatingWeaponSystem 设置）
        public void SetSlotIndex(int index) {
            slotIndex = index;
            UpdateLocalOffset();
        }

        private void UpdateLocalOffset() {
            // 总数量从主人 GPO 的 FloatingWeaponCount 属性获取（或由服务端 RPC 同步）
            // Phase 1 暂时用固定 slotIndex 作为偏移计算，总数量后续接入
            float offsetX = slotIndex * SlotSpacing; // 简化版，正式版见链路二公式
            if (iEntity?.GetEntityObj() is { } go) {
                go.transform.localPosition = new Vector3(offsetX, OffsetY, OffsetZ);
            }
        }
    }
}
```

### 8.5 禁止项

| 禁止行为 | 原因 |
|---------|------|
| 在 OnUpdate 中做球形检测（Physics.OverlapSphere） | 应使用 ServerAIFindInsightTarget 的 0.5s 轮询，避免每帧重型物理检测 |
| 直接操作主人 GPO 的 Transform | 应通过 ServerAIMaster 绑定关系 + GPO 框架自动跟随，不直接改主人位置 |
| 客户端 FloatingWeaponView 做伤害判定 | 伤害判定必须在服务端 Ability 内完成 |
| FuncID 与现有协议冲突 | 合并前必须核查 GpoTypeSet.cs 中已用 ID 列表 |

---

## S-09：验收标准

| 层次 | 验收项 | 验证方式 |
|------|-------|---------|
| 编译 | 所有新 .cs 文件无编译错误 | Unity Editor 控制台 |
| 编译 | `GpoTypeSet.Id_BIU26FloatingWeapon` 常量定义正确 | 代码审查 |
| 功能 | 解锁后服务端生成独立 FloatingWeapon GPO（不依附玩家 Component） | 服务端日志 |
| 功能 | FloatingWeapon GPO 持续跟随玩家后方水平排列 | 客户端目视验证（灰盒）|
| 功能 | GPO 每 1.5s 自动对 15m 内最近敌方 GPO 发射子弹 | 服务端日志 + 目视 |
| 功能 | 子弹命中目标正常扣血 | 观察目标血量变化 |
| 集成 | 6 把武器全部解锁后，排列间距均匀 | 目视验证 |
| 集成 | 替换已有武器时，旧 GPO 销毁、新 GPO 生成（Phase 2 功能，Phase 1 不要求） | N/A |

---

*文档版本 v0.1 — BIU26-悬浮武器GPO，GPO 工程师待填充（骨架由 DL 预置）*
