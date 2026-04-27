# BattleRoleLogic 重构 — 会话状态

> **功能**：BattleRoleLogic 组件化重构
> **当前阶段**：阶段 4D 完成（4D-1~4D-8b ✅，4D-9a ✅，4D-9b 暂缓）
> **最后更新**：2026-04-07
> **负责 Agent**：[DL]

---

## 当前进度

| 阶段 | 内容 | BattleRoleLogic.cs 行数 | 状态 |
|------|------|------------------------|------|
| **阶段 0（基准）** | 未改动 | 3503 行 | ✅ 基准 |
| **阶段 1** | 基础设施（继承链 + BattleRoleLogicComponent + BattleRoleLogicEvents）| 3515 行 | ✅ 完成 |
| **阶段 2** | 骨架 Partial 拆分（Fields / Init / Clear / TimeEvent）| **2095 行** | ✅ 完成（-40.2%）|
| ~~**阶段 3A/3B**~~ | ~~空壳 Component~~（已废弃）| 2095 行 | ⚠️ 废弃 — 空壳不计进度 |
| **目录文件改造** | BattleRoleLogic.cs 对齐 BattleRole.cs 模式（Awake/init骨架/AddComponents 迁入主文件 + 顶部索引注释）| **2186 行** | ✅ 完成（主文件暂增，4C 阶段再瘦身）|
| **阶段 4A** | 7 个 Partial 完整迁移（事件+Facade+Component 三步）| 目标 ~1200 行 | ✅ **7/7 完成** |
| **阶段 4B** | 大型 Partial — 4B-1 TeammateBehavior / 4B-2 States | 目标 ~700 行 | ✅ **完成** |
| **阶段 4C** | 主文件逻辑拆分 + 目录化 | **122 行** | ✅ **完成（-96.5%）** |
| **阶段 5** | 文件目录整理 | ~400 行（不变）| ⬜ 待开始 |

---

## ⚠️ 迁移的"完成"定义（三步缺一不可）

1. **事件定义** — 在 `BattleRoleLogicEvents.cs` 定义对应事件 struct
2. **Facade 替换** — Partial 文件改为单行 `Dispatcher` facade（枚举/顶层类型保留在文件顶部）
3. **Component 实现** — `OnAwake` 注册事件+逻辑，`OnClear` 反注册

> ⚠️ **枚举检查（每次迁移前必做）**：`grep "^public enum\|^public struct\|^public class" RoleLogic_XXX.cs`，有输出则保留在 Facade 文件顶部。

---

## 📉 行数记录

| 时间 | 里程碑 | 主文件行数 | 较基准减少 | 备注 |
|------|--------|-----------|-----------|------|
| 2026-04-01 | 阶段 0（基准）| **3503** | — | — |
| 2026-04-02 | 阶段 1 完成 | **3515** | +12 | 骨架增加 |
| 2026-04-02 | 阶段 2 完成 | **2095** | ▼ 1408（-40.2%）| Fields/Init/Clear/TimeEvent 迁出 |
| 2026-04-02 | 目录文件改造完成 | **2186** | ▼ 1317（-37.6%）| Awake/init骨架/AddComponents/Loop 迁入，暂增 91 行 |
| — | 阶段 4A 完成（预期）| ~1200 | ▼ 2303（-65.7%）| |
| — | 阶段 4B 完成（预期）| ~700 | ▼ 2803（-80.0%）| |
| 2026-04-03 | 阶段 4C 完成（4C-1~4C-12）| **339** | ▼ 3164（-90.3%）| 主文件逻辑全部提取 |
| 2026-04-03 | 主文件目录化完成 | **122** | **▼ 3381（-96.5%）** | Misc 拆分归档，BattleRoleLogic.cs 成纯目录 |
| — | 阶段 4D 完成（预期）| 122 | **▼ 3381（-96.5%）** | partial → Component 化（行数不变，逻辑内聚）|

---

## 文件现状快照（2026-04-02）

### 基础设施 & 骨架 Partial（已完成）

| 文件 | 行数 | 状态 |
|------|------|------|
| `BattleRoleLogic.cs`（主文件）| **2186** | 🔄 持续瘦身中（目录结构已对齐 BattleRole.cs）|
| `BattleRoleLogicComponent.cs` | 19 | ✅ 完成 |
| `BattleRoleLogicEvents.cs` | **442** | 🔄 随迁移填充（4D-1~6 新增 24 个事件）|
| `RoleLogic_Fields.cs` | 974 | ✅ 完成 |
| `RoleLogic_Init.cs` | **260** | ✅ 完成（辅助方法：InitRoleData / InitLoops / InitClient / InitServer）|
| `RoleLogic_Clear.cs` | 71 | ✅ 完成 |
| `RoleLogic_TimeEvent.cs` | 96 | ✅ 完成 |

### 阶段 4A — Component 迁移进度

| # | Component | Facade 文件 | Facade 行数 | Component 文件 | Component 行数 | 顶层类型 | 状态 |
|---|-----------|------------|------------|---------------|---------------|---------|------|
| 4A-1 | `RoleLogicLocalStatesComponent` | `RoleLogic_LocalStates.cs` | 101 | `Component/RoleLogicLocalStatesComponent.cs` | 88 | `LocalRoleSyncState` 枚举 | ✅ **完成** |
| 4A-2 | `RoleLogicLobbyComponent` | `RoleLogic_Lobby.cs` | 80 | `Component/RoleLogicLobbyComponent.cs` | 217 | 无 | ✅ **完成** |
| 4A-3 | `RoleLogicDataInfoComponent` | `RoleLogic_DataInfo.cs` | 10 | `Component/RoleLogicDataInfoComponent.cs` | 220 | 无 | ✅ **完成** |
| 4A-4 | `RoleLogicSkillComponent` | `RoleLogic_Skill.cs` | 97 | `Component/RoleLogicSkillComponent.cs` | 293 | 无 | ✅ **完成** |
| 4A-5 | `RoleLogicWeaponComponent` | `RoleLogic_Weapon.cs` | **46** | `Component/RoleLogicWeaponComponent.cs` | **258** | 无 | ✅ **完成** |
| 4A-6 | `RoleLogicDungeonComponent` | `RoleLogic_DungeonGame.cs` | **58** | `Component/RoleLogicDungeonComponent.cs` | **303** | 无 | ✅ **完成** |
| 4A-7 | `RoleLogicModeComponent` | `RoleLogic_Mode.cs`（161行）`RoleLogic_Knockout.cs`（8行） | 169 | `Component/RoleLogicModeComponent.cs` | **228** | 无（GoGoParty struct 保留为公共字段；BladeBall/FightClose 纯计算不迁）| ✅ **完成** |

### 阶段 4B — 大型 Partial 文件清理

| # | 文件 | 当前行 | 策略 | 状态 |
|---|------|--------|------|------|
| **4B-1** | `RoleLogic_TeammateBehavior.cs` | 122（已瘦） | 5 Component + Facade + Events 三步迁移 | ✅ **完成** |
| **4B-2** | `RoleLogic_States.cs` | 1347→613 | 枚举/struct 提取到新建 `RoleStateTypes.cs`（742行）；Partial 方法保留原文件；不事件化热路径 | ✅ **完成** |

> `RoleLogic_Fields.cs`（974行）视情况在 4C 合并处理。

---

### 阶段 4C — 主文件逻辑拆分（BattleRoleLogic.cs 2191行 → 目标 ~400行）

| # | 模块 | 覆盖行范围 | 目标产出文件 | 状态 |
|---|------|-----------|------------|------|
| **4C-1** | 背包/道具 | OnPickItem、addPickItem、removePickItem、countNowPackNum 等（~545-1060行） | `RoleLogic_Inventory.cs` | ✅ **完成**（2191→1620行）|
| **4C-2** | 移动/物理 | mainMove、MoveDir、countMoveDir、SetCar 等（~384-524行） | `RoleLogic_Move.cs` | ✅ **完成**（1620→1455行）|
| **4C-3** | 救援/复活 | UpdateUprearRole、ServerUprearRoleId、StopResurrecueOther（~249-1200行） | `RoleLogic_Uprear.cs` | ✅ **完成**（1455→1366行）|
| **4C-4** | AI 逻辑 | aiEvent、GetAILockTargetRole、setAILockRole、CheckAIUseWeapon 等 | `RoleLogic_AI.cs` | ✅ **完成**（1366→1261行）|
| **4C-5** | 重连逻辑 | OnRoleReconnect / OnReconnectVoice / RoleReconnectCancelAidmeiState / RoleReconnectCloseSandState / SetRoleConnectGmeVoice | `RoleLogic_Reconnect.cs` | ✅ **完成**（1261→1174行） |
| **4C-6** | 地面检测 | GetRoleGroundForAutoId / GetRoleDownGroundPointForAutoId / IsContinueCheck / DownGroundPoint | `RoleLogic_Ground.cs` | ✅ **完成**（1174→1127行） |
| **4C-7** | 游泳/水下 | GetIsSwim / GetIsUnderWater / GetIsDiving / GetIsUnderWaterDiving | `RoleLogic_Swim.cs` | ✅ **完成**（1127→1096行） |
| **4C-8** | 指令系统 | AddInstruction / HasInstruction / RemoveInstruction / TeamAICmdCreateAndDropItem | `RoleLogic_Instruction.cs` | ✅ **完成**（1096→1016行） |
| **4C-9** | 状态同步 | CheckRoleInWuLinArea / UpNowPoint / stateSync / noNetStateSync / ResetProperty（行 123-397）| `RoleLogic_StateSync.cs` | ✅ **完成**（1016→745行）|
| **4C-10** | 物理/推人/速度 | countMoveSpeedValue / PushRoleStateTimeEvent / SetPushRoleMoveDir / CheckTransFer / GetMoveSpeed / CheckMoveSpeed | `RoleLogic_Physics.cs` | ✅ **完成**（745→576行）|
| **4C-11** | 跳跃/足球 | GetJumpConfigValueByType / GetFootBallJumpArea / CheckFootBallMoveArea / CheckFootBallJumpArea / GetSpecialMoveData | `RoleLogic_Jump.cs` | ✅ **完成**（576→431行）|
| **4C-12** | HP 管理 | ServerChangeRoleMaxHp / OnSetHp / OnSetMaxHp | `RoleLogic_HP.cs` | ✅ **完成**（431→339行）|

---

### 阶段 4D — Partial 文件 Component 化（直接逻辑 → Dispatcher 事件架构）

| # | 优先级 | Partial 文件 | 行数 | 候选 Component 名 | 策略 |
|---|--------|------------|------|-----------------|------|
| 4D-1 | 🟢 优先 | `RoleLogic_Swim.cs` | 31 | `RoleLogicSwimComponent` | 4个只读查询 | ✅ **完成**（+4事件，编译通过）|
| 4D-2 | 🟢 优先 | `RoleLogic_Ground.cs` | 22 | `RoleLogicGroundComponent` | hitList/groundPoint/射线落地 | ✅ **完成**（+3事件，编译通过）|
| 4D-3 | 🟢 优先 | `RoleLogic_Instruction.cs` | 36 | `RoleLogicInstructionComponent` | sendInstructions + TeamAI物品 | ✅ **完成**（+6事件，编译通过）|
| 4D-4 | 🟡 中等 | `RoleLogic_HP.cs` | 99 | `RoleLogicHPComponent` | HP管理，边界清晰 | ✅ **完成**（+3事件，CallBack模式处理setter返回值）|
| 4D-5 | 🟡 中等 | `RoleLogic_Reconnect.cs` | 97 | `RoleLogicReconnectComponent` | 重连逻辑，相对独立 | ✅ **完成**（+3事件，跨模块私有方法内联）|
| 4D-6 | 🟡 中等 | `RoleLogic_AI.cs` | 107 | `RoleLogicAIComponent` | AI逻辑块 | ✅ **完成**（+5事件，组件内部xxxInternal()复用）|
| 4D-7 | 🔴 暂缓 | `RoleLogic_Physics.cs` | 176→57 | `RoleLogicPhysicsComponent` | 6事件，简单字段留Facade | ✅ **完成** |
| 4D-8a | ✅ | `RoleLogic_Jump.cs` | 151→34 | `RoleLogicJumpComponent` | 跳跃配置+特殊移动数据（2方法） |
| 4D-8b | ✅ | _(同上Facade)_ | _(同上)_ | `RoleLogicFootballAreaComponent` | 足球区域检测（3方法） |
| 4D-9a | ✅ | `RoleLogic_StateSync.cs` | 280→214 | `RoleLogicWuLinComponent` | 武林客栈区域检测（已提取） |
| 4D-9b | 🔴 暂缓 | _(同上Facade)_ | _(剩余)_ | — | UpNowPoint/stateSync/noNetStateSync 耦合太深 |


---

## 门控记录

| 门控 | 结果 | 时间 |
|------|------|------|
| Round 1: 设计文档输出后 | ✅ 通过 | 2026-04-01 |
| Round 2: 方案 v2.0 整理后 | ✅ 通过 | 2026-04-02 |
| p5 Phase 5 完成门控 | ✅ 通过 | 2026-04-07 |

## 主进度

| # | Agent | 内容 | 状态 |
|---|-------|------|------|
| ㉓ [项目负责人] | active.md 重组（添加 session-sync.sh 7 个锚点节） | ✅ |
| ㉔ [DL] | 4D-7 Physics 组件迁移完成（Events+Facade+Component） | ✅ |
| ㉕ [DL] | 4D-8 Jump Component 迁移完成（5事件+Facade+Component+注册） | ✅ |
| ㉖ [DL] | 4D-9a WuLin Component 迁移完成（1事件+Facade+Component+注册，3字段迁移） | ✅ |
| ㉗ [DL] | 4D-10 Move 组件完成（RoleLogicMoveComponent 4 handlers，169→~80行） | ✅ |
| ㉘ [DL] | 4D-11 Weapon 组件补充完成（+4 handlers, +shootTime字段, 145→108行） | ✅ |
| ㉙ [DL] | 4D-12 Uprear 组件完成（RoleLogicUprearComponent 2 handlers, 93→12行） | ✅ |
| ㉚ [项目负责人] | 4D-13 Ground 确认已完成（之前批次已迁移），4D 补充迁移全部完成 | ✅ |
| ㉛ [DL] | Phase 5 完成：LocalRoleSyncState→RoleLogicEnums.cs, checkUserWeaponTime死代码清理 | ✅ |
| ㉜ [DL] | 目录重组：BattleRoleLogic文件迁移到BattleRoleLogic/子目录，编译通过 | ✅ |
| ㉝ [DL] | 补移RoleLogic_MOOD.cs到BattleRoleLogic/目录 | ✅ |
| ㉞ [DL] | Phase 6-1: Client 字段迁移完成 — 40 个公开字段/属性迁移到 RoleLogic_ClientFields.cs，RoleLogicClient 改为转发属性，编译通过 | ✅ |
| ㉟ [DL] | Phase 6 策略变更：回滚 6-1 字段迁移，改为 Partial→Component 抽取方案（保留 RoleLogicClient/Server 类） | ✅ |
| ㊱ [DL] | C-1 BladeBall Component 完成：276行→组件(260行)+门面(30行)，编译通过 | ✅ |
| ㊲ [DL] | RoleLogicClient 目录化整理完成: 主文件1992→864行, 12个文件 | ✅ |
| ㊳ [DL] | BattleLogicSystemBase架构 + BladeBall迁移到RoleLogicClient | ✅ |
| ㉓ [DL] | Phase 6-1 Client 字段迁移完成：35个字段/属性从 RoleLogicClient 迁移到 BattleRoleLogic partial (RoleLogic_ClientFields.cs)，RoleLogicClient 保留转发属性，MSBuild 编译通过 0 错误 0 外部改动 | ✅ |
| ㊴ [DL] | 回滚误操作的 Phase 6-1 字段迁移：删除 RoleLogic_ClientFields.cs，恢复 RoleLogicClient.cs 原始字段声明，编译通过 0 错误。策略确认：保留 RoleLogicClient/Server，按决策15继续 Partial→Component 抽取 | ✅ |
| ㊵ [DL] | 更新打散方案文档 v1.1：修正行数(864→739)、标记字段迁移废弃、明确决策15后计划 | ✅ |
| ㊶ [DL] | M-6.2 完成: 主文件863→338行, 新建5个partial(ModeCheck/RoleDisplay/NetCheck/Skill/Misc), 编译0错误 | ✅ |
| ㊷ [DL] | M-6.3 评估完成: Push已通过RoleLogicPhysicsComponent事件化(无需再组件化), Football纯生命周期辅助(不适合). Phase 6 Client侧工作完成 | ✅ |
| ㊼ [DL] | M-7.2 Server字段提取: RoleLogicServer_Fields.cs (678行), 主文件5131→4527行 | ✅ |
| ㊼ [DL] | M-7.2 Server字段提取完成 | ✅ |
| ㊽ [DL] | M-7.3 Server方法群组提取完成: 12个新partial, 主文件5131→369行 | ✅ |
| ㊾ [DL] | M-7.4 代码整理完成: XML doc目录头(37文件) + Init/OnUpdate来源注释, 主文件432行 | ✅ |
| ㉓ [DL] | M-7.1 Server 子循环→Component 转换完成: 7/7 ✅ 候选已全部转为 BattleRoleLogicComponent (Batch1: RoleCarSkin/RoleDinoSkin/RoleSkinChangeSkin, Batch2: AutoTestRoleData/RoleLogicCarShift/BattleRoleLogicStaminaServer/RoleLogicLimitedRedPackets), 剩余4个子循环(RoleSkillServer⚠️/RoleCheat❌/RoleKillInfo⚠️/WarFlagData⚠️)不转换 | ✅ |
| ㉔ [DL] | Batch 3 完成: WarFlagData + RoleSkillServer → BattleRoleLogicComponent, 文件移至BattleRoleLogic/目录. IRoleLogicServer 9/11 已转换, 仅剩 RoleCheat(❌) + RoleKillInfo(待定) | ✅ |
| ㉓ [DL] | RoleLogicServer→BattleLogicSystemBase迁移完成 | ✅ |
| ㉔ [DL] | RoleKillInfo(627行)→RoleLogicServerComponent转换完成, 编译0错误 | ✅ |
| ㉕ [DL] | RoleLogicServer主文件瘦身: 437→329行, 对齐Client格式 | ✅ |
| ㉖ [DL] | Phase 8方案分析+技术文档v2.0: 4个并行分析任务(Partial/Feature/外部引用), 文档新增Phase 8/9/10规划, 确定Feature→Component统一为下一阶段 | ✅ |
| ㉗ [DL] | M-8.1 试点完成: 3个Feature→Component转换(StatisticsDataManager/TrajectoryFeatureManager/PowerFeatureManager), AddComponent公共桥接方法, 编译0错误 | ✅ |
| ㉘ [DL] | M-8.2完成: 5个无条件Server Feature→Component转换(Resurrection/Uprear/StateSync/BeAttacked/Ping), 含GetFeature→GetBattleComponent外部引用修复, 编译通过0错误 | ✅ |
| 28 [DL] | M-8.2: 5 Feature to Component done, build pass | ✅ |
| 29 [DL] | M-8.2 done: 3 external-ref Features converted (PowerSkill/Adsorb/HandInHand), 28 GetFeature refs replaced, build pass 0 errors | ✅ |
| 30 [DL] | Feature→Component reverted by user, AddFeature/AddComponent comments added to RoleLogicServer(20 features) and verified | ✅ |

## 文档产出清单

| 文档 | 路径 | 状态 |
|------|------|------|
| RoleLogicPhysicsComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicPhysicsComponent.cs` | ✅ |
| RoleLogicJumpComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicJumpComponent.cs` | ✅ |
| RoleLogicFootballAreaComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicFootballAreaComponent.cs` | ✅ |
| RoleLogicWuLinComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicWuLinComponent.cs` | ✅ |
| RoleLogicMoveComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/` | ✅ |
| RoleLogicUprearComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/Component/` | ✅ |
| RoleLogicEnums.cs | `Assets/Script/GamePlay/Host/Modules/Role/` | ✅ |
| 重构进度计划.md v3.0 | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` | ✅ |
| RoleLogic_ClientFields.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` | ✅ |
| RoleLogic_ClientFields.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` | ❌ 已回滚 |
| 重构进度计划.md v4.0 | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` | ✅ |
| RoleLogicClientBladeBallComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/` | ✅ |
| RoleLogicClient_MoveSpeed.cs | `RoleLogicClient/` | ✅ |
| RoleLogicClient_Push.cs | `RoleLogicClient/` | ✅ |
| RoleLogicClient_IdCardSkin.cs | `RoleLogicClient/` | ✅ |
| BattleLogicSystemBase.cs | `Assets/Script/GamePlay/Host/Modules/BattleLogicSystemBase.cs` | ✅ |
| RoleLogicClientComponent.cs | `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClientComponent.cs` | ✅ |
| BattleRoleLogic重构方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/BattleRoleLogic重构方案.md` | ✅ 已更新(v3.0合并) |
| 重构进度计划.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` | ❌ 已删除(合并入方案) |
| RoleLogic子系统打散方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` | ✅ 新建 |
| 重构进度计划.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` | ❌ 已删除(合并入方案v3.0) |
| RoleLogic子系统打散方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` | ✅ 已更新(新增§2.4 Feature系统分析) |
| RoleLogic_ClientFields.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` | ✅ |
| RoleLogic_ClientFields.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` | ❌ 已回滚删除 |
| RoleLogic子系统打散方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` | ✅ 已更新(v1.1 修正行数+废弃字段迁移+明确后续计划) |
| "RoleLogicClient_ModeCheck.cs" | `"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_ModeCheck.cs"` | "✅ |
| "RoleLogicClient_RoleDisplay.cs" | `"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_RoleDisplay.cs"` | "✅ |
| "RoleLogicClient_NetCheck.cs" | `"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_NetCheck.cs"` | "✅ |
| "RoleLogicClient_Skill.cs" | `"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Skill.cs"` | "✅ |
| "RoleLogicClient_Misc.cs" | `"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Misc.cs"` | "✅ |
| 7个Server Component文件 | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/` | ✅ |
| WarFlagData.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/WarFlagData.cs` | ✅ |
| RoleSkillServer.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleSkillServer.cs` | ✅ |
| RoleLogicServerComponent.cs | `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicServerComponent.cs` | ✅ |
| RoleBulletInfo.cs | `Assets/Script/GamePlay/Server/Modules/Role/RoleBulletInfo.cs` | ✅ |
| IRoleLogicServer.cs | `Assets/Script/GamePlay/Server/Modules/Role/IRoleLogicServer.cs` | ✅ |
| RoleLogic子系统打散方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` | ✅ v2.0更新 |
| RoleLogic子系统打散方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` | ✅ v2.1 |
| BattleRoleLogic重构方案.md | `aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/BattleRoleLogic重构方案.md` | ✅ v3.1 |

## 关键决策

| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|
| 1 | 继承链 | BattleRoleLogic 继承 BattleSystemBase | 2026-04-01 |
| 2 | 组件基类 | BattleRoleLogicComponent 继承 BattleComponent | 2026-04-01 |
| 3 | 迁移完成定义 | 三步缺一不可：事件定义 + Facade 替换 + Component 实现 | 2026-04-02 |
| 4 | 空壳 Component | 3A/3B 建的 7 个空壳保留，阶段 4A 时按三步补充实现 | 2026-04-02 |
| 5 | 枚举处理（阶段 5 前） | Partial 顶层枚举保留在 Facade 文件顶部，阶段 5 统一迁到 RoleLogicEnums.cs | 2026-04-02 |
| 6 | 枚举处理（阶段 5） | 新建 RoleLogicEnums.cs，不改类型名，零外部改动 | 2026-04-02 |
| 7 | Facade 策略 | 方法体改为单行 Dispatcher，签名不变，外部调用方不动 | 2026-04-02 |
| 8 | 事件系统边界 | 组件间通信走事件；组件内部直调；只读字段直接访问 | 2026-04-02 |
| 9 | States 热路径不事件化 | GetState/SetState 每帧数百次调用，Dispatcher 代价过高；States 用类型提取代替事件化 | 2026-04-11 |
| 10 | Component Register API | BattleRoleLogicComponent 基类提供 Register/Unregister | 2026-04-11 |
| 11 | TeammateBehavior 拆分 | 1197行原文件 → 5 Component（Behavior/Move/Fire/Weapon/Action），每个 ≤300行 | 2026-04-11 |
| 12 | 目录文件模式 | 主文件对齐 BattleRole.cs：Awake/init骨架/AddComponents 在主文件 | 2026-04-02 |
| 13 | Component 基类访问 | BattleRoleLogicComponent 里访问 StartGame 用 startGame（小写），不是 MyStartGame | 2026-04-02 |
| 10 | 4D-8 Jump组件职责拆分 | 拆分为 JumpComponent（跳跃配置+特殊移动）+ FootballAreaComponent（足球区域检测），职责更纯粹 | 2026-04-07 |
| 14 | Server/Client 打散方案选择 | 方案A：全面打散 RoleLogicServer(~10,720行) 和 RoleLogicClient(~2,553行) 融入 BattleRoleLogic，消除中间层。先Client后Server，代理过渡+批量替换 | 2026-04-07 |
| 15 | Phase 6 策略变更：保留 RoleLogicClient/Server | 不删除 RoleLogicClient 和 RoleLogicServer，保留为生命周期壳 + 字段容器。Partial 逻辑抽取为 BattleRoleLogicComponent 子类，通过 AddComponent 注册。Phase 6-1 字段迁移已回滚。 | 2026-04-07 |
| 16 | 服务端Component注册位置 | 从BattleRoleLogic.AddComponents()迁移到RoleLogicServer.AwakeInit(), 通过公开的RegisterComponent<T>()代理方法注册. 服务端关注点内聚在RoleLogicServer中. | 2026-04-08 |
| 17 | RoleLogicServer继承BattleLogicSystemBase | RoleLogicServer改为继承BattleLogicSystemBase,与RoleLogicClient对称. 新增RoleLogicServerComponent基类, 9个服务端组件改为继承此类. 组件由RoleLogicServer自管理. | 2026-04-08 |
| 18 | Feature→Component转换桥接方案 | 在BattleRoleLogic(RoleLogic_New.cs)添加public new AddComponent<T>()桥接方法,暴露protected基类方法供RoleLogicServer/Client.Init外部注册. 与AddFeature并存,后续Feature全部转换后废弃AddFeature | 2026-04-08 |
| 20 | 用户回退所有Feature→Component类体转换 | 保留AddFeature注册不变,仅添加功能注释,Feature→Component转换方案暂停待重新评估 | 2026-04-08 |

## Bug 记录

| # | 现象 | 根因 | 修复 | 状态 |
|---|------|------|------|------|
| 14 | CS0507: cannot change access modifiers when overriding protected inherited member | OnAwake/OnClear基类为protected，新组件误用public override | 改为protected override | ✅ |
| 15 | CS2001 BattleRoleComponent.cs not found | Role目录孤立meta文件 | 删除orphan meta | ✅ |
| 14 | explore agent报告Resurrection/Uprear GetFeature=0,实际有7+1个外部调用 | 引用计数搜索遗漏或统计错误 | 编译报错暴露,手动grep确认并修复8处GetFeature→GetBattleComponent | ✅ |
| 15 | ServerRolePowerSkillManager missing OnRemove, Update delegate leak | Original Feature never had OnRemove impl | Added OnClear with RemoveUpdate(OnUpdate) in Component conversion | ✅ |

## 规范沉淀

1. **迁移前必须检查 Partial 顶层类型**：4A-1 迁移时 LocalRoleSyncState 枚举被误删，导致全项目 CS0246
2. **主文件必须参照 BattleRole.cs 模式**：原无目录结构，Awake/init/AddComponents 扎堆在 Init partial
3. **init() 细节拆成命名辅助方法**：直接迁入主文件 init() 含业务细节会导致主文件再度膨胀
4. **Component 内禁止使用 MyStartGame**：应使用基类 startGame 属性（否则 CS0103）
5. **字段声明不要在同一 partial class 里写两遍**：birthIslandSetting/bornData 重复声明 → CS0102
6. **Component 内访问字段必须使用公开属性**：private 字段对 Component 不可见（isLocalRole→IsLocalRole 等）
8. **BattleRoleLogicComponent 的 OnAwake/OnClear 继承自 BattleComponent，访问修饰符为 protected，新组件必须用 protected override 而非 public override**

## ⚠️ 遗留待确认

- 4D-7/8/9（Physics/Jump/StateSync）暂缓，待评估是否 Phase 5 前尝试

---

## 回滚参考

> 路径：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/Back/`

| 备份文件 | 行数 |
|---------|------|
| `BattleRoleLogic.cs` | 3496 |
| `RoleLogic_States.cs` | 1345 |
| `RoleLogic_TeammateBehavior.cs` | 1197 |
| `RoleLogic_Mode.cs` | 310 |
| `RoleLogic_DungeonGame.cs` | 272 |
| `RoleLogic_Weapon.cs` | 224 |
| `RoleLogic_Skill.cs` | 206 |
| `RoleLogic_DataInfo.cs` | 180 |
| `RoleLogic_Lobby.cs` | 112 |
| `RoleLogic_LocalStates.cs` | 105 |
| `RoleLogic_New.cs`（原名 `RoleLogic_Lifecycle.cs`）| 66 |

---

## Background Agent 记录

| agent_id | 任务描述 | 预期产出 | 启动时间 | 状态 |
|----------|---------|---------|---------|------|
| — | — | — | — | — |
� | — | — | — |
