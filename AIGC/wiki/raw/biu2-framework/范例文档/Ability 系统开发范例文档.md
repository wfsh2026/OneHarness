# Ability 系统（AB/AE）开发范例文档

> **用途**：本文件用于指导 AI / 程序在现有框架内扩展 Ability（AB/AE）能力。  
> **代码库**：`G:\BiuBiuBiu2-MiniGame\Assets\Scripts`  
> **命名空间**：`Sofunny.BiuBiuBiu2.ServerGamePlay` / `Sofunny.BiuBiuBiu2.ClientGamePlay`

> **前置阅读**：使用本范例前，仍需先读取 [[knowledge/system-map]] 与 [[GamePlay_Dev/core-rules]]。  
> **文档定位**：本文件是 Ability 系统的开发范例，不替代边界定义文档；涉及能力边界、跨系统归属时，以 system-map.md 与边界定义文档为准。

---

## 一、系统概述

Ability 系统分为两条主线：

- **AB（Ability）**：主动行为、一次性行为、触发器行为（如子弹、爆炸、位移、召唤）。
- **AE（AbilityEffect）**：持续效果（如 DoT、加速、减速、加攻、禁技能等）。

核心设计原则：

- **Server 决策，Client 表现**：服务端负责逻辑与生命周期；客户端负责表现与局部裁剪。
- **数据驱动**：`AbilityM_XXX + CSV` 为参数来源，运行时通过 `Select()` 异步读取。
- **统一调度入口**：统一进入 `SM_Ability.PlayAbility` / `SM_Ability.PlayAbilityEffect`。
- **类型分发**：由 `ServerAbilityManager_SwitchAB/AE` 和 `ClientAbilityManager_SwitchAB/AE` 完成路由。

---

## 二、整体架构图

```text
┌──────────────────────────────────────────────────────────────────────┐
│                          技能/武器/事件触发层                          │
│  SE_Skill.Event_CastAbility / SE_Weapon.Event_PlayFireAbility / 其他   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ 派发
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     服务端世界事件层（SM_Ability）                      │
│   PlayAbility / PlayAbilityEffect / RemoveAbility                    │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       ServerAbilityManager                            │
│  1) MData.Select() 2) SwitchAB/AE 3) AddSystem<SAB/SAE_XXXSystem>     │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│         S_Ability_Base + Component 组合（ServerAbilitySync 等）         │
│                生成 Proto_Ability.TargetRpc_PlayAbility               │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      网络协议层（Proto_Ability*）                       │
│   3_Proto_Ability + 14_Proto_AbilityAB_Auto + 15_Proto_AbilityAE_Auto │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        ClientAbilityManager                           │
│   反序列化 protoDoc -> SwitchAB/AE -> CAB/CAE（或通用表现）              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 三、Server / Client 职责划分

| 职责 | Server | Client |
|------|--------|--------|
| 触发合法性与技能执行 | ✅ | ❌ |
| 伤害/治疗/属性结算 | ✅ | ❌ |
| AB/AE 生命周期管理 | ✅ | ❌ |
| Ability 实例 ID 分配 | ✅ | ❌ |
| 网络广播与重连补发 | ✅ | ❌ |
| 收包反序列化与对象创建 | ❌ | ✅ |
| 特效/模型/动画/UI 表现 | ❌ | ✅ |
| 表现数量裁剪（性能） | ❌ | ✅（`ClientAbilityManager.CheckSystemDic`） |

---

## 四、核心类结构

### 4.1 服务端

| 类名 | 路径 | 职责 |
|------|------|------|
| `ServerAbilityManager` | `GamePlay\Server\Ability\ServerAbilityManager.cs` | Ability 总入口：监听 `SM_Ability`，创建/删除系统 |
| `ServerAbilityManager_SwitchAB` | `GamePlay\Server\Ability\ServerAbilityManager_SwitchAB.cs` | AB TypeID 路由到 `SAB_XXXSystem` |
| `ServerAbilityManager_SwitchAE` | `GamePlay\Server\Ability\ServerAbilityManager_SwitchAE.cs` | AE TypeID 路由到 `SAE_XXXSystem` |
| `S_Ability_Base` | `GamePlay\Server\Ability\S_Ability_Base.cs` | Server AB/AE 基类，持有 `AbilityId/ConfigID/RowId/FireGPO/TargetGPO` |
| `ServerAbilitySync` | `GamePlay\Server\Ability\Component\ServerAbilitySync.cs` | 短效 AB 的网络下发组件 |
| `ServerGPOSkillAbilityCaster` | `GamePlay\Server\GPO\Components\ServerGPOSkillAbilityCaster.cs` | 技能组件中常见 Ability 触发入口 |

### 4.2 客户端

| 类名 | 路径 | 职责 |
|------|------|------|
| `ClientAbilityManager` | `GamePlay\Client\Ability\ClientAbilityManager.cs` | 监听网络，创建/移除客户端 Ability 系统 |
| `ClientAbilityManager_SwitchAB` | `GamePlay\Client\Ability\ClientAbilityManager_SwitchAB.cs` | AB protoID -> `CAB_XXXSystem` |
| `ClientAbilityManager_SwitchAE` | `GamePlay\Client\Ability\ClientAbilityManager_SwitchAE.cs` | AE protoID -> `CAE_XXXSystem` |
| `C_Ability_Base` | `GamePlay\Client\Ability\C_Ability_Base.cs` | 客户端 Ability 基类，负责实体创建与销毁 |
| `ClientAbilitySystem` | `GamePlay\Client\Ability\ClientAbilitySystem.cs` | 管理 `ClientNetworkAbilitySync` 组件 |

---

## 五、消息与协议层

### 5.1 世界事件（World）

| 消息 | 文件 | 作用 |
|------|------|------|
| `SM_Ability.PlayAbility` | `Message\GamePlay\Server\World\SM_Ability.cs` | 触发 AB |
| `SM_Ability.PlayAbilityEffect` | 同上 | 触发 AE |
| `SM_Ability.RemoveAbility` | 同上 | 请求移除 Ability |
| `CM_Ability.RemoveAbility` | `Message\GamePlay\Client\World\CM_Ability.cs` | 客户端外部触发移除 |

### 5.2 系统事件（System）

| 消息 | 文件 | 作用 |
|------|------|------|
| `SE_Ability.RPCAbility` | `Message\GamePlay\Server\System\SE_Ability.cs` | 由 AB/AE 系统请求网络下发 |
| `SE_AbilityEffect.Event_ResetAbilityEffect` | `Message\GamePlay\Server\System\SE_AbilityEffect.cs` | AE 重置刷新 |
| `CE_Ability.PlayAbility/RemoveAbility` | `Message\GamePlay\Client\System\CE_Ability.cs` | 客户端系统内创建与移除 |

### 5.3 网络协议（Proto）

| 协议 | 文件 | 说明 |
|------|------|------|
| `Proto_Ability` | `Message\Network\3_Proto_Ability.cs` | 通用容器协议（含 `TargetRpc_PlayAbility`） |
| `Proto_AbilityAB_Auto` | `Message\Network\14_Proto_AbilityAB_Auto.cs` | AB FuncID 与反序列化入口 |
| `Proto_AbilityAE_Auto` | `Message\Network\15_Proto_AbilityAE_Auto.cs` | AE FuncID 与反序列化入口 |
| `Rpc_XXX` | `Message\Network\Ability\AB\` / `AE\` | 具体类型的数据结构 |

---

## 六、数据与配置层

### 6.1 配置索引

| 文件 | 作用 |
|------|------|
| `Data\Configs\Ability\AbilityConfig_AutoGenerated.cs` | AB ConfigId（10000+）与 `AB_XXX` 常量 |
| `Data\Configs\Ability\AbilityEffectConfig_AutoGenerated.cs` | AE ConfigId（20000+）与 `AE_XXX` 常量 |
| `Data\AbilityData.cs` | `IAbilityMData / IAbilityInData` 等接口与基类 |

### 6.2 模板与 CSV

| 类型 | 路径 |
|------|------|
| AB 模板类 | `Data\Configs\Ability\AB\TemplateM\AbilityM_XXX.cs` |
| AE 模板类 | `Data\Configs\Ability\AE\TemplateM\AbilityM_XXX.cs` |
| Select 代码 | `Data\Configs\Ability\AB\TemplateM\Select\` / `AE\TemplateM\Select\` |
| AB CSV | `Assets\Bundle\Configs\Ability\AB\AbilityM_XXX.csv` |
| AE CSV | `Assets\Bundle\Configs\Ability\AE\AbilityM_XXX.csv` |

---

## 七、AB / AE 类型总览表（含主要字段与用途）

> 说明：以下为常用高频类型的范例总览；表中仅列仓库内已核实的关键字段，完整全集以  
> `AbilityConfig_AutoGenerated.cs` / `AbilityEffectConfig_AutoGenerated.cs`、对应 `AbilityM_*.cs` 与 `AbilityIn_*.cs` 为准。

### 7.1 AB（主动行为）高频类型

| ConfigId | TypeID | 主要字段（示例） | 主要用途 |
|----------|--------|------------------|----------|
| `10005` | `AB_Bullet` | `M_EffectSign` `M_Power` `M_HitEffect` + `In_StartPoint/In_TargetPoint/In_Speed` | 标准子弹、命中触发后续逻辑 |
| `10010` | `AB_Explosive` | `M_LifeTime` `M_PlayEffectAbility` + `In_Range` `In_Hurt` | 范围爆炸、AOE 伤害 |
| `10018` | `AB_Missile` | `M_Power` `M_HitAbility` `M_LifeTime` | 导弹飞行+命中触发 |
| `10040` | `AB_TrackingMissle` | `M_TrackSpeed` `M_LockSpeed` `M_MoveDistance` | 自动追踪目标 |
| `10008` | `AB_Displacement` | `M_DisplacementSpeed` `M_DisplacementHeight` `M_IsHitGPOStop` | 位移/突进 |
| `10006` | `AB_Charge` | `M_ChargeInitSpeed` `M_ChargeTargetSpeed` `M_ChargeTogetSpeedDuration` | 冲锋持续运动 |
| `10022` | `AB_PlayAbilitiesAfterLowHp` | `M_LowHpRatio` `M_PlayAbilities` | 低血触发技能链 |
| `10021` | `AB_PlayAbilitiesAfterKillRole` | `M_PlayAbilities` | 击杀触发技能链 |
| `10036` | `AB_SummonAIByHeroAttr` | `M_SummonAISign` `M_SummonAIId` `M_SummonNum` | 召唤单位 |
| `10031` | `AB_RepeatBomb` | `M_BombCount` `M_BombInterval` `M_AreaEffect`（其余范围参数继承自 `AbilityM_Bomb`） | 多段范围轰炸 |

### 7.2 AE（持续效果）高频类型

| ConfigId | TypeID | 主要字段（示例） | 主要用途 |
|----------|--------|------------------|----------|
| `20001` | `AE_HurtGPOByTime` | `M_LifeTime` `M_DeltaTime` `M_DamageType` | 持续伤害（燃烧/中毒） |
| `20020` | `AE_SkillHurtGPOByTime` | `M_LifeTime` `M_DeltaTime` | 技能触发型 DoT |
| `20010` | `AE_RecoverGPOHpByTime` | `M_RecoverDelayTime` `M_RecoverRatio` | 持续回血 |
| `20006` | `AE_MoveSpeedRate` | `M_SpeedRate` `M_LifeTime` | 速度增减益 |
| `20007` | `AE_MoveSpeedRateByTime` | `M_InitSpeedRate` `M_TargetSpeedRate` `M_ReachTargetSpeedRateTime` `M_LifeTime` | 限时速度效果 |
| `20016` | `AE_WeaponATKAddRate` | `M_AddRate` `M_LifeTime` | 武器增伤 |
| `20003` | `AE_MaxHpRate` | `M_MaxHpRate` `M_LifeTime` | 最大生命值提升 |
| `20017` | `AE_SkillDisabled` | `M_LifeTime` | 沉默/禁技能 |
| `20009` | `AE_ProtectGPO` | `M_FollowFXRowId` `M_ProtectDuration` | 护盾/减伤 |
| `20015` | `AE_SkillCDRecoverRate` | `M_RecoverRate` `M_DamageRecoverRate` `M_SkillIndex` `M_LifeTime` | 冷却恢复加速 |

---

## 八、核心流程

### 8.1 AB 触发时序（技能释放）

```text
SE_Skill.Event_CastAbility
  -> ServerGPOSkillAbilityCaster.OnCastAbility
  -> SM_Ability.PlayAbility
  -> ServerAbilityManager.OnPlayAbilityCallBack
      -> MData.Select()
      -> HandleAbilityABType()
      -> AddSystem<SAB_XXXSystem>
  -> SAB_XXXSystem 通过 SE_Ability.RPCAbility
  -> ServerAbilitySync -> TargetRpc_PlayAbility(protoDoc)
  -> ClientAbilityManager 创建 CAB_XXXSystem
```

### 8.2 AE 触发时序（命中挂 Buff）

```text
SM_Ability.PlayAbilityEffect
  -> ServerAbilityManager.OnPlayAbilityEffectCallBack
      -> MData.Select()
      -> 查询 TargetGPO 是否已有同 ConfigID + RowId
          -> 已有：SetFireGPO + ResetEffect()
          -> 没有：AddSystem<SAE_XXXSystem> 后 ResetEffect()
  -> 同步到客户端（按具体系统实现）
```

### 8.3 关键触发代码片段

```csharp
// AB
MsgRegister.Dispatcher(new SM_Ability.PlayAbility {
    FireGPO = iGPO,
    MData = playMData,
    InData = inData,
    OR_CallBack = system => { /* 可选：记录 abilityId 与 skillIndex 映射 */ }
});

// AE
MsgRegister.Dispatcher(new SM_Ability.PlayAbilityEffect {
    FireGPO = fireGpo,
    TargetGPO = targetGpo,
    MData = effectMData,
    InData = effectInData
});
```

### 8.4 同步策略说明

- 默认短效 AB 走 `S_Ability_Base -> ServerAbilitySync -> SE_Ability.RPCAbility -> Proto_Ability.TargetRpc_PlayAbility` 链路。
- 需要重连恢复或常驻同步的 Ability，不应只依赖 `ServerAbilitySync`；应按现有范例改为挂接 `ServerNetworkSync`。
- 新增同步方案时，不扩展新框架，优先复用现有 `ServerAbilitySync` / `ServerNetworkSync` 组合。

---

## 九、代码生成链路（AbilityEditor）

编辑器：`Assets\Editor\AbilityEditor\AbilityEditor.cs`

`GenerateAllCode()` 的关键步骤：

1. `GenerateAbilityConfigFile()`：生成 `AbilityConfig_AutoGenerated.cs` / `AbilityEffectConfig_AutoGenerated.cs`
2. `GenerateServerSystem(template)`：生成 `SAB_XXXSystem` / `SAE_XXXSystem`
3. `GenerateClientSystem(template)`：仅当模板 `IsSyncCreateCAB = true`
4. `GenerateServerManagerSwitch(skillTemplates)`：生成服务端 AB/AE Switch
5. `GenerateClientManagerSwitch(skillTemplates)`：生成客户端 Switch
6. `GenerateNetworkMessages(skillTemplates)`：生成 `Proto_AbilityAB_Auto` / `Proto_AbilityAE_Auto`
7. `GenerateAbilityCsvFile(currentMTemplate)`：生成 CSV
8. `GenerateAbilitySelectCode(currentMTemplate)`：生成 Select 查询逻辑

> 实践建议：新增 Ability 优先走 AbilityEditor，避免手工改 AutoGenerated 造成索引漂移。

---

## 十、新增 AB 类型完整流程（实操）

### 10.1 建模板

- 在 `Data\Configs\Ability\AB\TemplateM\` 新建 `AbilityM_XXX.cs`
- 定义 `M_` 字段（模板参数）
- 如需运行时参数，定义 `AbilityIn_XXX`（`In_` 字段）

### 10.2 生成代码

- 打开 AbilityEditor 选择 AB
- 配置同步策略 `IsSyncCreateCAB`
- 执行全量生成

### 10.3 配置数据

- 在 `Assets\Bundle\Configs\Ability\AB\AbilityM_XXX.csv` 增加数据行
- 校验 `ID / RowSign / M_*` 与模板字段一致

### 10.4 业务接入

在触发点派发 `SM_Ability.PlayAbility` 并传入 `MData/InData`。

### 10.5 验证

- Server 是否命中 AB case
- Client 是否创建对应 `CAB_XXXSystem`（若需同步）
- 生命周期结束是否正常移除

---

## 十一、新增 AE 类型完整流程（实操）

### 11.1 建模板

- 在 `Data\Configs\Ability\AE\TemplateM\` 新建 `AbilityM_XXX.cs`
- 一般至少需要 `M_LifeTime` 与核心效果字段

### 11.2 生成代码

- AbilityEditor 生成 `SAE_XXXSystem`、AE 配置索引、协议

### 11.3 业务接入

通过 `SM_Ability.PlayAbilityEffect` 触发到目标 GPO。

### 11.4 去重验证

同一 `TargetGPO + ConfigID + RowId` 再触发应走 `ResetEffect()`，不重复创建实例。

### 11.5 客户端验证

- 若该 AE 有专用表现，验证 `ClientAbilityManager_SwitchAE` 能路由到 `CAE_XXXSystem`
- 若无专用表现，验证通用逻辑不会报错

---

## 十二、典型组合范例

### 12.1 燃烧弹

- AB：`AB_Bullet`
- AE：`AE_HurtGPOByTime`
- 描述：命中时挂 DoT，持续扣血

### 12.2 低血狂怒

- AB：`AB_PlayAbilitiesAfterLowHp`
- AE：`AE_MoveSpeedRate` + `AE_WeaponATKAddRate`
- 描述：低血阈值触发，短时加速并增伤

### 12.3 范围减速

- AB：`AB_Explosive`
- AE：`AE_MoveSpeedRateByTime`
- 描述：AOE 命中后施加减速

### 12.4 击杀回能（示意）

- AB：`AB_KillRecoverSkillCD`
- AE（可选叠加）：`AE_SkillCDRecoverRate`
- 描述：击杀瞬时返还 + 阶段性冷却恢复增益

---

## 十三、调试与排错清单

### 13.1 触发不生效

- 检查是否派发了 `SM_Ability.PlayAbility / PlayAbilityEffect`
- 检查 `MData.Select()` 是否成功（CSV 是否存在该行）
- 检查 Server Switch 是否有对应 case

### 13.2 客户端无表现

- 检查是否发送了 `Proto_Ability.TargetRpc_PlayAbility`
- 检查 `Proto_AbilityAB_Auto/AE_Auto` 是否有对应 `FuncID`
- 检查 Client Switch 是否创建了对应系统

### 13.3 AE 重复异常

- 正确行为：同配置刷新，不新增实例
- 若出现叠加，重点查触发参数是否真同 `ConfigID + RowId + TargetGPO`

### 13.4 生命周期残留

- 检查是否派发 `SM_Ability.RemoveAbility`
- 检查 `TimeReduce` 回调是否被覆盖/漏注册

---

## 十四、验收标准（提交前）

- 触发链路完整可跑通：入口 -> Server -> Proto -> Client
- 日志无关键错误（缺 case、缺配置、反序列化失败）
- 索引一致：Config、Switch、Proto、CSV 对齐
- AE 去重行为符合预期
- 常驻能力重连恢复符合设计（使用 `ServerNetworkSync` 时必须验证）

---

## 十五、实现约束（必须遵守）

- 不修改 `S_Ability_Base.cs`、`C_Ability_Base.cs`、`ServerAbilityManager.cs`、`ClientAbilityManager.cs` 的架构基线逻辑
- 不新增新的框架父类；沿用 `System + Component + Event + Proto + Config` 现有体系
- 优先使用 AbilityEditor 生成，避免手工维护 AutoGenerated
- System 负责组合组件与调度，复杂逻辑落在 Component
- 命名与索引遵循现有规范：AB（10000+）、AE（20000+）
