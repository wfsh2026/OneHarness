# BIU26-模式系统

> **文档版本**：v1.0
> **创建时间**：2026-03-28
> **负责 Agent**：开发负责人 (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：`aigc/docs/Dev_Lead/BIU26/BIU26_开发计划.md`
> **状态**：✅ DL 已编写

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

玩家进入 BIU26 局内后，在约 2~3 分钟的发育期内，通过击杀自动围绕自身刷出的小怪，逐步从 0 把悬浮武器成长至 6 把；每新增一把悬浮武器即刻可见火力密度提升，感受到持续上升的碾压割草感；同时金币随击杀积累，死亡时转移 50% 给击杀者，形成经济博弈基础。

---

## S-04：功能定位

本文档覆盖 BIU26 Phase 1 **模式系统层**全部职责：BIU26 GameMode 入口（ServerBIU26Mode）、悬浮武器解锁计数与 GPO 生成调度（FloatingWeaponManager）、金币经济（CoinManager），以及对应客户端表现组件与网络协议。**不包含**极坐标刷怪器 GPO 配表（见 BIU26-极坐标刷怪器.md）、悬浮武器 GPO 配表+AI攻击逻辑（见 BIU26-悬浮武器GPO.md）、子弹 Ability 内部实现（见 BIU26-悬浮武器Ability.md）、场景建设（见 BIU26-场景建设.md）。

---

## S-05：文件清单

### 📋 配表层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Template/data/ModeData.cs` | **修改**（ModeEnum 新增枚举值） | 新增 `ModeBIU26 = XX`（枚举整数，确认后填入） |
| `Assets/Scripts/Template/data/ModeData.cs` | **修改**（`Init()` switch 新增 case） | 配置 RoundWinState、ScoreChannelDatas 等 BIU26 模式参数 |
| `Assets/Scripts/Template/data/Mode.cs` | **修改**（ModeSet 新增 Id 常量 + data 数组追加行） | `Id_ModeBIU26` 常量 + BIU26 数据行（StartModeDownTime ≥ 10f） |
| `Assets/Scripts/Template/data/AiLevel.cs` | **修改**（新增 gameMode 对应数据行） | 测试 ID 使用 10001-19999 区间 |

### 🔀 路由注册层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/Mode/ServerModeSystem.cs` | **修改**（`InitModeComponent()` switch 新增 case） | 注册 `ServerBIU26Mode` |
| `Assets/Scripts/GamePlay/Client/Mode/ClientModeSystem.cs` | **修改**（`InitModeComponent()` switch 新增 case） | 注册 `ClientBIU26Mode`（若有客户端专属表现） |
| `Assets/Scripts/GamePlay/Client/Network/Component/ClientNetworkSerialize.cs` | **修改**（追加 case） | `UnSerializeBuffer` switch 新增 BIU26 两个 Proto 的 case |

### 🖥️ 服务端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerBIU26Mode.cs` | **新建** | 继承 `ComponentBase`，BIU26 模式主循环：玩家入局时初始化刷怪器 GPO、金币组件、悬浮武器管理器 |
| `Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26FloatingWeaponManager.cs` | **新建** | 挂载在玩家 GPO 下，管理 0→6 把悬浮武器解锁计数、保底逻辑、**触发生成独立 FloatingWeapon GPO**（见 BIU26-悬浮武器GPO.md） |
| `Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26CoinManager.cs` | **新建** | 挂载在玩家 GPO 下，管理金币：击杀小怪加金币、死亡扣50%并转移给击杀者 |

### 💻 客户端 System 层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/GamePlay/Client/GPO/Components/ClientBIU26CoinHUD.cs` | **新建** | 监听金币变更 RPC，用 `OnGUI` 渲染金币数量显示（不依赖 TextMeshPro/UGUI，参考 AimAssistDebugOnGUI.cs） |

### 📡 网络协议层

| 文件路径 | 操作 | 说明 |
|---------|------|------|
| `Assets/Scripts/Message/Network/17_Proto_BIU26.cs` | **新建** | BIU26 专属协议：`Rpc_SyncCoin`（金币同步）。悬浮武器 GPO 同步走 GPO 框架自有协议，无需在此新建 |

---

## S-06：ASCII 交互链路图

### 链路一：悬浮武器解锁 → 生成独立 FloatingWeapon GPO

```
[服务端] 小怪被击杀
    └─ ServerBIU26FloatingWeaponManager.OnMinionKilled()
         ├─ killCount++ / guaranteeCounter++
         ├─ weaponCount < 6 AND (概率触发 OR 保底触发)?
         │       ↓ 是
         │   guaranteeCounter = 0
         │   weaponCount++
         │   ─── 生成一个独立 FloatingWeapon GPO ───
         │   MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
         │       AISign     = "BIU26_FloatingWeapon",  // GPO 工程师确认此 Sign
         │       OR_CallBack = weaponGPO => {
         │           // FloatingWeapon GPO 自带 ServerAIFindInsightTarget
         │           // + ServerBIU26FloatingWeaponAttack（见 BIU26-悬浮武器GPO.md）
         │           // 它会自动跟随玩家并自动攻击附近目标
         │       }
         │   })
         │   Rpc(new Proto_BIU26.Rpc_SyncCoin { ... })  // 仅金币同步走此协议
         └─ 无武器解锁，仅进入金币结算
```

> ⚠️ **悬浮武器的攻击链路（锁敌 + Ability 开火）完整定义在 BIU26-悬浮武器GPO.md §S-06**，本文档不重复。

### 链路三：金币死亡转移

```
[服务端] ServerBIU26CoinManager.OnPlayerDead(killerGPO)
    ├─ lostCoins = currentCoins * 0.5f
    ├─ currentCoins -= lostCoins
    ├─ killerGPO.Dispatcher(SE_BIU26.Event_AddCoin { amount = lostCoins })
    │       └─ killerGPO 上 CoinManager 加金币 + Rpc_SyncCoin 给击杀者客户端
    └─ Rpc(Rpc_SyncCoin { coin = currentCoins }) → 通知死者客户端
```

---

## S-07：灰盒资源占位

| 对象 | 灰盒形状 | 颜色（_BaseColor RGBA） | 尺寸 | 挂点偏移 |
|------|---------|----------------------|------|---------|
| 金币（地面掉落） | Sphere | (1.0, 0.85, 0.0, 1.0) 黄色 | 半径 0.2m | N/A（独立落地） |

> 悬浮武器灰盒定义（Cube 白/蓝/金三档颜色 + 水平一排排列 offset 公式）见 **BIU26-悬浮武器GPO.md §S-07**。

---

## S-08：边界条件

### 8.1 依赖的外部接口

| 接口 | 来源 | 说明 |
|------|------|------|
| `SM_AI.Event_AddAI` | 现有框架 | 刷怪调用；需确认 AISign 在 BIU26 小怪配表注册后才可用 |
| `SE_BIU26.Event_MinionKilled` | **本计划新建** | 小怪死亡 → 玩家 GPO 事件总线，需与 GPO 工程师对齐 |
| `SE_GPO.Event_SetOnDeadCallBack` | 现有框架（待核查） | 小怪死亡回调；GPO 工程师开发前必须核查接口是否存在 |
| `SM_Ability.PlayAbility` | 现有 Ability 框架 | 悬浮武器开火；AB Sign 为预留桩，等 Ability 工程师提供 |
| `ServerAIFindInsightTarget` | 现有 GPO 组件 | 锁敌逻辑；`ServerBIU26FloatingWeaponAttack` 内部参考此类 API |

### 8.2 禁止做的事

| 禁止项 | 原因 |
|--------|------|
| 修改任何 Base 类源码 | 违反 safety-rules.md 约束 |
| 在 `ServerGPOFollowPoint` 上直接改逻辑 | 影响现有 UAV 系统 |
| Phase 1 实现元素系统 / 缩圈 / PVP | 超出 Phase 1 范围 |
| FuncID 与现有协议冲突 | 会导致 RPC 解析错误；合并前必须核查已用 ID 列表 |

### 8.3 边界文档引用

- [[safety-rules]]
- [[模式系统内容边界定义]]
- [[BIU26原型开发启动包]] §五（Phase 1 范围）

---

## S-09：验收标准

### 9.1 编译验收

- [ ] 所有新建文件编译通过，无报错（除 TODO 标注外）
- [ ] 修改文件（ModeData.cs / Mode.cs / ModeSystem / ClientNetworkSerialize）编译通过，不影响现有系统
- [ ] `17_Proto_BIU26.cs` 注册到 `ClientNetworkSerialize.cs` 后编译通过

### 9.2 功能验收（运行时）

- [ ] 击杀第 10 只小怪时，服务端保底触发，悬浮武器数量从 N 变为 N+1，日志输出 `[BIU26] 玩家解锁第 X 把悬浮武器`
- [ ] 6 把悬浮武器全部解锁后，继续击杀小怪不再新增武器（上限保护生效）
- [ ] 悬浮武器客户端视觉：1把时居中后方；3把时水平均匀排列；6把时均匀排布约0.7m间隔
- [ ] 玩家A被玩家B击杀时，A的金币减少50%，B的金币增加对应数值，双方 HUD 均正确更新
- [ ] 击杀小怪后金币数增加，HUD 实时显示
- [ ] `ServerBIU26FloatingWeaponAttack` 调用 Ability 开火时，目标 GPO HP 减少（AB Sign 预留桩填充后验证）

### 9.3 集成验收（与其他模块联动）

- [ ] BIU26 Scene 在 Unity Editor 中可单独运行（Play Mode），不影响其他已有 GameMode Scene
- [ ] `ClientNetworkSerialize.cs` 追加 case 后，现有 RPC 协议均可正常解析（非 BIU26 场景无 RPC 报错）
- [ ] BIU26 模式路由注册不影响其他模式（ServerModeSystem / ClientModeSystem 回归正常）

---

## 附录：骨架代码

### ServerBIU26FloatingWeaponManager.cs

```csharp
// Assets/Scripts/GamePlay/Server/GPO/Components/ServerBIU26FloatingWeaponManager.cs
// 职责：挂载在玩家 GPO 下，管理悬浮武器解锁计数，解锁时调用 SM_AI.Event_AddAI 生成独立 FloatingWeapon GPO
// 参考：ServerUAVMove.cs（MasterGPO 跟随逻辑），UAV GPO 配表（SM_AI.Event_AddAI 用法）
// 决策归档：方案B（独立GPO，参考UAV，与 BIU26-悬浮武器GPO.md 配合）

using UnityEngine;
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Message;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerBIU26FloatingWeaponManager : ServerNetworkComponentBase {

        private const int   MaxWeaponCount     = 6;
        private const int   GuaranteeKillCount = 10;    // 每10只保底1把
        private const float WeaponUnlockChance = 0.15f; // 15% 概率

        private int weaponCount      = 0;
        private int killCount        = 0;
        private int guaranteeCounter = 0;

        protected override void OnAwake() {
            base.OnAwake();
            mySystem.Register<SE_BIU26.Event_MinionKilled>(OnMinionKilled);
        }

        protected override void OnClear() {
            base.OnClear();
            mySystem.Unregister<SE_BIU26.Event_MinionKilled>(OnMinionKilled);
        }

        private void OnMinionKilled(ISystemMsg msg, SE_BIU26.Event_MinionKilled ent) {
            killCount++;
            guaranteeCounter++;

            if (weaponCount >= MaxWeaponCount) return;

            bool shouldUnlock = (guaranteeCounter >= GuaranteeKillCount)
                                || (Random.value < WeaponUnlockChance);
            if (!shouldUnlock) return;

            guaranteeCounter = 0;
            weaponCount++;

            // 生成独立 FloatingWeapon GPO（方案B，参考UAV）
            MsgRegister.Dispatcher(new SM_AI.Event_AddAI {
                AISign    = "BIU26_FloatingWeapon", // GPO 工程师在 GPOM 配表中注册
                ExtraData = weaponCount - 1,        // slotIndex 供 Client GPO 计算排列 offset
            });

            Debug.Log($"[BIU26] 玩家解锁第 {weaponCount} 把悬浮武器（独立GPO），总击杀数: {killCount}");
        }
    }
}
```

### Proto_BIU26.cs

```csharp
// Assets/Scripts/Message/Network/17_Proto_BIU26.cs
// 职责：BIU26 专属 RPC 协议定义
// 注意：悬浮武器 GPO 的网络同步由 GPO 框架自动处理，无需在此定义
// TODO: FuncID 必须在项目已有最大值基础上分配新 ID（GPO 工程师负责核查 FuncID 不冲突）

namespace Sofunny.BiuBiuBiu2.NetworkMessage {
    public class Proto_BIU26 {

        /// <summary>服务端 → 客户端：同步玩家金币数量</summary>
        public struct Rpc_SyncCoin : IProto_Doc {
            public static readonly ushort ID = 30001; // TODO: 核查实际可用 FuncID
            public ushort FuncID => ID;
            public int coin;  // 当前金币数量
        }
    }
}
```

---

*文档版本 v1.1 — BIU26-模式系统，更新：架构决策变更 悬浮武器改为独立 GPO 方案，移除 FloatingWeaponAttack/LayoutPoint 组件，协议简化为仅 Rpc_SyncCoin*
