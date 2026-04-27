
**背景**：[DL] 执行任务

**推理**：batch conversion verified

**结论**：M-8.2: 5 Feature to Component done, build pass — ✅

---

## [2026-04-08 17:30:46] 文档: BattleRoleLogic重构方案.md

**背景**：文档状态变更

**推理**：Added Phase 6-7-8 to completion table, updated inheritance diagram with RoleLogicServer, updated file structure with Server layout

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/BattleRoleLogic重构方案.md` — ✅ v3.1

---

## [2026-04-08 17:20:59] 文档: RoleLogic子系统打散方案.md

**背景**：文档状态变更

**推理**：Phase 8 status updated, Feature list annotated, trial experience documented

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` — ✅ v2.1

---

## [2026-04-08 17:17:11] 进度: Feature→Component reverted by user, AddFeature/AddComponent comments added to RoleLogicServer(20 features) and verified

**背景**：[DL] 执行任务

**推理**：User decided to revert class body changes, keep only comments for now

**结论**：Feature→Component reverted by user, AddFeature/AddComponent comments added to RoleLogicServer(20 features) and verified — ✅

---

## [2026-04-08 17:17:11] ADR#20: 用户回退所有Feature→Component类体转换

**背景**：用户回退所有Feature→Component类体转换

**推理**：用户对转换方案有新想法(InitData模式等),先完成注释再决定新方案

**结论**：保留AddFeature注册不变,仅添加功能注释,Feature→Component转换方案暂停待重新评估

---

## [2026-04-08 16:46:44] ADR#19: 已转换Feature的外部GetFeature调用如何处理

**背景**：已转换Feature的外部GetFeature调用如何处理

**推理**：GetBattleComponent在BattleMonoSystemBase上也是protected,需要与AddComponent相同的public new桥接模式

**结论**：在BattleRoleLogic(RoleLogic_New.cs)添加public new GetBattleComponent<T>()桥接方法,与AddComponent桥接对称,替换外部GetFeature调用

---

## [2026-04-08 16:46:35] Bug#14 修复

**背景**：explore agent报告Resurrection/Uprear GetFeature=0,实际有7+1个外部调用

**推理**：引用计数搜索遗漏或统计错误

**结论**：编译报错暴露,手动grep确认并修复8处GetFeature→GetBattleComponent

---

## [2026-04-08 16:38:35] ADR#18: Feature→Component转换桥接方案

**背景**：Feature→Component转换桥接方案

**推理**：AddComponent在BattleMonoSystemBase上是protected(组件只应由系统内部添加),但Feature迁移需要从外部(RoleLogicServer)注册. 选择public new而非修改基类,影响范围最小

**结论**：在BattleRoleLogic(RoleLogic_New.cs)添加public new AddComponent<T>()桥接方法,暴露protected基类方法供RoleLogicServer/Client.Init外部注册. 与AddFeature并存,后续Feature全部转换后废弃AddFeature

---

## [2026-04-08 16:38:25] 进度: M-8.1 试点完成: 3个Feature→Component转换(StatisticsDataManager/TrajectoryFeatureManager/PowerFeatureManager), AddComponent公共桥接方法, 编译0错误

**背景**：[DL] 执行任务

**推理**：Feature→Component转换模式验证: 基类AbsRoleLogicFeature→BattleRoleLogicComponent, 生命周期OnInit→OnAwake+OnRemove→OnClear, 注册AddFeature→AddComponent. 发现AddComponent是protected, 在RoleLogic_New.cs添加public new桥接. 转换模式成熟可批量推广

**结论**：M-8.1 试点完成: 3个Feature→Component转换(StatisticsDataManager/TrajectoryFeatureManager/PowerFeatureManager), AddComponent公共桥接方法, 编译0错误 — ✅

---

## [2026-04-08 15:55:42] 进度: Phase 8方案分析+技术文档v2.0: 4个并行分析任务(Partial/Feature/外部引用), 文档新增Phase 8/9/10规划, 确定Feature→Component统一为下一阶段

**背景**：[DL] 执行任务

**推理**：完成Phase 8规划阶段,技术文档已更新,等待用户确认开始执行M-8.1试点

**结论**：Phase 8方案分析+技术文档v2.0: 4个并行分析任务(Partial/Feature/外部引用), 文档新增Phase 8/9/10规划, 确定Feature→Component统一为下一阶段 — ✅

---

## [2026-04-08 15:55:29] Phase 8 方案分析与技术文档更新

**背景**：4个并行分析任务完成: 客户端18个Partial分析(7个YES候选)、服务端35个Partial分析(20个YES候选)、Feature系统分析(29个Feature,与Component高度重叠)、外部引用分析(Top1 roleLogicClient.RoleClient 1369次)

**推理**：Feature与Component生命周期高度重叠但Feature能力弱(无事件无内置Update);已有先例BattleRoleLogicStaminaServer从Feature迁移为Component;Feature统一优先级最高(消除架构冗余),Server Partial组件化当前不紧迫(Phase7已将主文件从5131降到329行)

**结论**：确定路线图: Phase8=Feature统一(~29个,中等难度), Phase9=外部引用简化(低难度QoL), Phase10=Server Partial组件化(高难度可选). 技术文档已更新至v2.0

---

## [2026-04-08 15:54:59] 文档: RoleLogic子系统打散方案.md

**背景**：文档状态变更

**推理**：Phase 7标记完成,新增Phase 8 Feature统一方案+Phase 9-10远期规划,更新架构图含RoleLogicServerComponent

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` — ✅ v2.0更新

---

## [2026-04-08 15:29:05] 文档: IRoleLogicServer.cs

**背景**：文档状态变更

**推理**：从RoleLogicServer主文件提取的独立接口(仅RoleCheat使用)

**结论**：`Assets/Script/GamePlay/Server/Modules/Role/IRoleLogicServer.cs` — ✅

---

## [2026-04-08 15:29:04] 文档: RoleBulletInfo.cs

**背景**：文档状态变更

**推理**：从RoleLogicServer主文件提取的独立类

**结论**：`Assets/Script/GamePlay/Server/Modules/Role/RoleBulletInfo.cs` — ✅

---

## [2026-04-08 15:28:56] 进度: RoleLogicServer主文件瘦身: 437→329行, 对齐Client格式

**背景**：[DL] 执行任务

**推理**：提取AddComponents方法, 移走RoleBulletInfo/IRoleLogicServer到独立文件, 5个辅助方法迁入partial(_Misc/_Network/_Statistics/_CheatCheck), mStructFlySpeedLine迁入_Fields

**结论**：RoleLogicServer主文件瘦身: 437→329行, 对齐Client格式 — ✅

---

## [2026-04-08 14:54:46] 进度: RoleKillInfo(627行)→RoleLogicServerComponent转换完成, 编译0错误

**背景**：[DL] 执行任务

**推理**：原评估为中高复杂度,实际分析LOW. 627行但模式重复, 99处外部引用无需修改(MyRoleKillInfo字段类型不变). 服务端组件总数10/11.

**结论**：RoleKillInfo(627行)→RoleLogicServerComponent转换完成, 编译0错误 — ✅

---

## [2026-04-08 14:37:24] 文档: RoleLogicServerComponent.cs

**背景**：文档状态变更

**推理**：服务端组件基类,提供serverLogic/roleLogic/gameWorld/startGame访问

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicServerComponent.cs` — ✅

---

## [2026-04-08 14:37:17] 进度: RoleLogicServer→BattleLogicSystemBase迁移完成

**背景**：[DL] 执行任务

**推理**：9组件→RoleLogicServerComponent, DriveComponents/ClearAllComponents对接, RegisterComponent移除, 编译0错误

**结论**：RoleLogicServer→BattleLogicSystemBase迁移完成 — ✅

---

## [2026-04-08 14:37:04] ADR#17: RoleLogicServer继承BattleLogicSystemBase

**背景**：RoleLogicServer继承BattleLogicSystemBase

**推理**：用户要求对齐Client/Server架构. BattleLogicSystemBase提供AddComponent/DriveComponents/ClearAllComponents能力,无需RegisterComponent代理. 9个组件从BattleRoleLogicComponent改为RoleLogicServerComponent,宿主变为RoleLogicServer.

**结论**：RoleLogicServer改为继承BattleLogicSystemBase,与RoleLogicClient对称. 新增RoleLogicServerComponent基类, 9个服务端组件改为继承此类. 组件由RoleLogicServer自管理.

---

## [2026-04-08 14:32:16] ADR#16: 服务端Component注册位置

**背景**：服务端Component注册位置

**推理**：AddComponent是protected,外部类无法直接调用. 添加public RegisterComponent<T>()代理,保持基类封装性同时允许子系统自管理组件.

**结论**：从BattleRoleLogic.AddComponents()迁移到RoleLogicServer.AwakeInit(), 通过公开的RegisterComponent<T>()代理方法注册. 服务端关注点内聚在RoleLogicServer中.

---

## [2026-04-08 14:27:22] 阶段更新

**背景**：Phase 7 Server 打散全部完成 (M-7.1~M-7.4, 9/11 子循环组件化)

**推理**：所有里程碑完成并通过编译验证

**结论**：阶段推进至 Phase 7 Server 打散全部完成 (M-7.1~M-7.4, 9/11 子循环组件化)

---

## [2026-04-08 14:27:22] M-7.1 Server 子循环组件化最终结果

**背景**：11个IRoleLogicServer实现类中,已成功转换9个为BattleRoleLogicComponent

**推理**：三批转换: Batch1(3个皮肤类), Batch2(4个数据/逻辑类), Batch3(2个中复杂度候选WarFlagData+RoleSkillServer实际评估为低复杂度). 保留RoleCheat(2007行,#if SERVER_LOGIC)和RoleKillInfo(581行,50+调用点)不转换. 所有9个组件文件统一存放在BattleRoleLogic/目录.

**结论**：Phase 7全部完成: M-7.1(9/11组件化) + M-7.2(字段提取) + M-7.3(16个partial) + M-7.4(代码整理). RoleLogicServer主文件5131→432行(-91.6%),编译0错误.

---

## [2026-04-08 14:27:21] 文档: RoleSkillServer.cs

**背景**：文档状态变更

**推理**：从UI/War/Role/RoleSkill/迁入BattleRoleLogic/统一目录

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleSkillServer.cs` — ✅

---

## [2026-04-08 14:27:21] 文档: WarFlagData.cs

**背景**：文档状态变更

**推理**：从Data/迁入BattleRoleLogic/统一目录

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/WarFlagData.cs` — ✅

---

## [2026-04-08 14:27:21] 进度: Batch 3 完成: WarFlagData + RoleSkillServer → BattleRoleLogicComponent, 文件移至BattleRoleLogic/目录. IRoleLogicServer 9/11 已转换, 仅剩 RoleCheat(❌) + RoleKillInfo(待定)

**背景**：[DL] 执行任务

**推理**：WarFlagData纯数据统计,RoleSkillServer仅2处roleLogicServer访问,均为低复杂度转换

**结论**：Batch 3 完成: WarFlagData + RoleSkillServer → BattleRoleLogicComponent, 文件移至BattleRoleLogic/目录. IRoleLogicServer 9/11 已转换, 仅剩 RoleCheat(❌) + RoleKillInfo(待定) — ✅

---

## [2026-04-08 14:01:39] M-7.1 Server 子循环组件化完成

**背景**：11个IRoleLogicServer实现经评估: 7个✅低复杂度, 3个⚠️中复杂度, 1个❌高复杂度(RoleCheat 2007行)

**推理**：按照已建立的转换模式(继承→BattleRoleLogicComponent, Init→OnAwake, Clear→OnClear, OnUpdate→AddUpdate), 分两批完成7个转换。Batch2中RoleLogicCarShift和BattleRoleLogicStaminaServer有OnUpdate逻辑,使用AddUpdate(OnTick)模式。BattleRoleLogicStaminaServer保留条件注册(IsOpenPowerBar)。所有7个文件统一移到BattleRoleLogic/目录。

**结论**：Phase 7 M-7.1~M-7.4全部完成。RoleLogicServer从5131行减至432行(主文件), 37个partial文件+7个Component。编译0错误。

---

## [2026-04-08 14:01:39] 文档: 7个Server Component文件

**背景**：文档状态变更

**推理**：从Data/和Server/移入BattleRoleLogic/统一目录

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/` — ✅

---

## [2026-04-08 14:01:38] 进度: M-7.1 Server 子循环→Component 转换完成: 7/7 ✅ 候选已全部转为 BattleRoleLogicComponent (Batch1: RoleCarSkin/RoleDinoSkin/RoleSkinChangeSkin, Batch2: AutoTestRoleData/RoleLogicCarShift/BattleRoleLogicStaminaServer/RoleLogicLimitedRedPackets), 剩余4个子循环(RoleSkillServer⚠️/RoleCheat❌/RoleKillInfo⚠️/WarFlagData⚠️)不转换

**背景**：[DL] 执行任务

**推理**：7个低复杂度候选全部完成，编译0错误。3个中复杂度候选和1个高复杂度候选按评估结果暂不转换。

**结论**：M-7.1 Server 子循环→Component 转换完成: 7/7 ✅ 候选已全部转为 BattleRoleLogicComponent (Batch1: RoleCarSkin/RoleDinoSkin/RoleSkinChangeSkin, Batch2: AutoTestRoleData/RoleLogicCarShift/BattleRoleLogicStaminaServer/RoleLogicLimitedRedPackets), 剩余4个子循环(RoleSkillServer⚠️/RoleCheat❌/RoleKillInfo⚠️/WarFlagData⚠️)不转换 — ✅

---

## [2026-04-08 13:27:21] 进度: M-7.4 代码整理完成: XML doc目录头(37文件) + Init/OnUpdate来源注释, 主文件432行

**背景**：[DL] 执行任务

**推理**：对标Client成功模式, 加入partial文件清单和方法来源标注, 提升代码可维护性

**结论**：M-7.4 代码整理完成: XML doc目录头(37文件) + Init/OnUpdate来源注释, 主文件432行 — ✅

---

## [2026-04-08 13:07:10] 进度: M-7.3 Server方法群组提取完成: 12个新partial, 主文件5131→369行

**背景**：[DL] 执行任务

**推理**：批量提取Statistics/Fly/RecoverHp/BornPoint/Misc/Damage/LockCamera/Network/HideSeek/CheatCheck/UltraFight/HeroCard, 编译0错误

**结论**：M-7.3 Server方法群组提取完成: 12个新partial, 主文件5131→369行 — ✅

---

## [2026-04-08 11:55:45] 进度: M-7.2 Server字段提取完成

**背景**：[DL] 执行任务

**推理**：604行字段提取到_Fields.cs,编译0错误

**结论**：M-7.2 Server字段提取完成 — ✅

---

## [2026-04-08 11:55:38] 文档: RoleLogicServer_Fields.cs

**背景**：文档状态变更

**推理**：Server字段提取partial,678行

**结论**：`Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Fields.cs` — ✅

---

## [2026-04-08 11:19:56] 进度: M-6.3 评估完成: Push已通过RoleLogicPhysicsComponent事件化(无需再组件化), Football纯生命周期辅助(不适合). Phase 6 Client侧工作完成

**背景**：[DL] 执行任务

**推理**：Push/Football均不满足组件化标准,保留partial是正确选择

**结论**：M-6.3 评估完成: Push已通过RoleLogicPhysicsComponent事件化(无需再组件化), Football纯生命周期辅助(不适合). Phase 6 Client侧工作完成 — ✅

---

## [2026-04-08 11:10:24] 阶段更新

**背景**：M-6.2 完成

**推理**：主文件从863行降至338行,提取5个新partial,编译通过

**结论**：阶段推进至 M-6.2 完成

---

## [2026-04-08 11:10:17] 进度: M-6.2 完成: 主文件863→338行, 新建5个partial(ModeCheck/RoleDisplay/NetCheck/Skill/Misc), 编译0错误

**背景**：[DL] 执行任务

**推理**：Client主文件瘦身完成,超预期从863降到338行

**结论**：M-6.2 完成: 主文件863→338行, 新建5个partial(ModeCheck/RoleDisplay/NetCheck/Skill/Misc), 编译0错误 — ✅

---

## [2026-04-08 11:10:09] 文档: "RoleLogicClient_Misc.cs"

**背景**：文档状态变更

**推理**："M-6.2

**结论**：`"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Misc.cs"` — "✅

---

## [2026-04-08 11:10:08] 文档: "RoleLogicClient_Skill.cs"

**背景**：文档状态变更

**推理**："M-6.2

**结论**：`"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Skill.cs"` — "✅

---

## [2026-04-08 11:10:08] 文档: "RoleLogicClient_NetCheck.cs"

**背景**：文档状态变更

**推理**："M-6.2

**结论**：`"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_NetCheck.cs"` — "✅

---

## [2026-04-08 11:10:07] 文档: "RoleLogicClient_RoleDisplay.cs"

**背景**：文档状态变更

**推理**："M-6.2

**结论**：`"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_RoleDisplay.cs"` — "✅

---

## [2026-04-08 11:10:07] 文档: "RoleLogicClient_ModeCheck.cs"

**背景**：文档状态变更

**推理**："M-6.2

**结论**：`"Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_ModeCheck.cs"` — "✅

---

## [2026-04-08 10:56:22] 进度: 更新打散方案文档 v1.1：修正行数(864→739)、标记字段迁移废弃、明确决策15后计划

**背景**：[DL] 执行任务

**推理**：技术文档需与实际进度和决策保持一致

**结论**：更新打散方案文档 v1.1：修正行数(864→739)、标记字段迁移废弃、明确决策15后计划 — ✅

---

## [2026-04-08 10:56:11] 文档: RoleLogic子系统打散方案.md

**背景**：文档状态变更

**推理**：更新以准确反映决策15后的现状

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` — ✅ 已更新(v1.1 修正行数+废弃字段迁移+明确后续计划)

---

## [2026-04-08 10:49:58] 文档: RoleLogic_ClientFields.cs

**背景**：文档状态变更

**推理**：决策15确认不删除RoleLogicClient，字段迁移不再需要

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` — ❌ 已回滚删除

---

## [2026-04-08 10:48:04] 进度: 回滚误操作的 Phase 6-1 字段迁移：删除 RoleLogic_ClientFields.cs，恢复 RoleLogicClient.cs 原始字段声明，编译通过 0 错误。策略确认：保留 RoleLogicClient/Server，按决策15继续 Partial→Component 抽取

**背景**：[DL] 执行任务

**推理**：上下文恢复后误重做了字段迁移，与决策15冲突。用户确认不删除 RoleLogicClient

**结论**：回滚误操作的 Phase 6-1 字段迁移：删除 RoleLogic_ClientFields.cs，恢复 RoleLogicClient.cs 原始字段声明，编译通过 0 错误。策略确认：保留 RoleLogicClient/Server，按决策15继续 Partial→Component 抽取 — ✅

---

## [2026-04-08 10:31:40] 阶段更新

**背景**：M-6.1 Client字段迁移完成（编译通过）

**推理**：Phase 6-1 全部完成，可进入 6-2

**结论**：阶段推进至 M-6.1 Client字段迁移完成（编译通过）

---

## [2026-04-08 10:31:30] 进度: Phase 6-1 Client 字段迁移完成：35个字段/属性从 RoleLogicClient 迁移到 BattleRoleLogic partial (RoleLogic_ClientFields.cs)，RoleLogicClient 保留转发属性，MSBuild 编译通过 0 错误 0 外部改动

**背景**：[DL] 执行任务

**推理**：M-6.1 里程碑达成

**结论**：Phase 6-1 Client 字段迁移完成：35个字段/属性从 RoleLogicClient 迁移到 BattleRoleLogic partial (RoleLogic_ClientFields.cs)，RoleLogicClient 保留转发属性，MSBuild 编译通过 0 错误 0 外部改动 — ✅

---

## [2026-04-08 10:31:21] 文档: RoleLogic_ClientFields.cs

**背景**：文档状态变更

**推理**：Phase 6-1 创建：客户端字段迁移完成，BattleRoleLogic partial 承载所有从 RoleLogicClient 迁出的字段

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` — ✅

---

## [2026-04-08 10:15:19] 文档: RoleLogic子系统打散方案.md

**背景**：文档状态变更

**推理**：记录 Feature 与 Component 双系统并行现状及打散策略

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` — ✅ 已更新(新增§2.4 Feature系统分析)

---

## [2026-04-08 10:12:43] Feature vs Component 双系统统一评估

**背景**：当前存在 AbsRoleLogicFeature(35+) 和 BattleRoleLogicComponent(24) 两套并行系统，Feature 已挂在 BattleRoleLogic 上

**推理**：Feature 与打散解耦，先完成打散再考虑统一

**结论**：当前 scope 不扩大，Feature 保持不变。后续可评估统一为 Component（消除双系统、统一事件/Update 接口）

---

## [2026-04-08 10:05:36] 文档: 重构进度计划.md

**背景**：文档状态变更

**推理**：进度信息已合并入重构方案v3.0的§1.3阶段完成记录和§6组件完成状态

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` — ❌ 已删除(合并入方案v3.0)

---

## [2026-04-08 09:59:23] 文档: RoleLogic子系统打散方案.md

**背景**：文档状态变更

**推理**：从BattleRoleLogic重构方案中分离Client/Server打散计划为独立文档

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/RoleLogic子系统打散方案.md` — ✅ 新建

---

## [2026-04-08 09:51:52] 文档: 重构进度计划.md

**背景**：文档状态变更

**推理**：进度已合并入重构方案v3.0，单独计划文件冗余

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` — ❌ 已删除(合并入方案)

---

## [2026-04-08 09:51:44] 文档: BattleRoleLogic重构方案.md

**背景**：文档状态变更

**推理**：合并重构方案+进度计划为统一文档，更新架构图和进度到最新状态

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/BattleRoleLogic重构方案.md` — ✅ 已更新(v3.0合并)

---

## [2026-04-08 09:40:35] 进度: BattleLogicSystemBase架构 + BladeBall迁移到RoleLogicClient

**背景**：[DL] 执行任务

**推理**：架构改造完成

**结论**：BattleLogicSystemBase架构 + BladeBall迁移到RoleLogicClient — ✅

---

## [2026-04-08 09:40:34] 文档: RoleLogicClientComponent.cs

**背景**：文档状态变更

**推理**：客户端组件基类

**结论**：`Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClientComponent.cs` — ✅

---

## [2026-04-08 09:40:25] 文档: BattleLogicSystemBase.cs

**背景**：文档状态变更

**推理**：纯C#版IBattleSystem基类

**结论**：`Assets/Script/GamePlay/Host/Modules/BattleLogicSystemBase.cs` — ✅

---

## [2026-04-08 09:21:56] 文档: RoleLogicClient_IdCardSkin.cs

**背景**：文档状态变更

**推理**：拆出身份卡换皮229行

**结论**：`RoleLogicClient/` — ✅

---

## [2026-04-08 09:21:56] 文档: RoleLogicClient_Push.cs

**背景**：文档状态变更

**推理**：拆出推人系统205行

**结论**：`RoleLogicClient/` — ✅

---

## [2026-04-08 09:21:55] 文档: RoleLogicClient_MoveSpeed.cs

**背景**：文档状态变更

**推理**：拆出移动速度逻辑409行

**结论**：`RoleLogicClient/` — ✅

---

## [2026-04-08 09:21:47] 进度: RoleLogicClient 目录化整理完成: 主文件1992→864行, 12个文件

**背景**：[DL] 执行任务

**推理**：拆分为12个partial文件移入子目录并合并3个极小partial

**结论**：RoleLogicClient 目录化整理完成: 主文件1992→864行, 12个文件 — ✅

---

## [2026-04-08 00:30:23] 文档: RoleLogicClientBladeBallComponent.cs

**背景**：文档状态变更

**推理**：C-1 BladeBall 组件新建

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/` — ✅

---

## [2026-04-08 00:30:17] 进度: C-1 BladeBall Component 完成：276行→组件(260行)+门面(30行)，编译通过

**背景**：[DL] 执行任务

**推理**：RoleLogicClient_BladeBallMode.cs 全部逻辑迁入 RoleLogicClientBladeBallComponent，门面仅保留4个API转发

**结论**：C-1 BladeBall Component 完成：276行→组件(260行)+门面(30行)，编译通过 — ✅

---

## [2026-04-08 00:17:58] 文档: 重构进度计划.md v4.0

**背景**：文档状态变更

**推理**：Phase 6/7 策略变更为 Partial→Component 化，更新文档至 v4.0

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` — ✅

---

## [2026-04-08 00:17:52] 文档: RoleLogic_ClientFields.cs

**背景**：文档状态变更

**推理**：Phase 6 策略变更，字段留在 RoleLogicClient 上不迁移

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` — ❌ 已回滚

---

## [2026-04-08 00:17:28] Phase 6/7 策略从打散改为组件化

**背景**：v3.0方案为完全删除RoleLogicClient/Server，需替换881个外部引用文件

**推理**：记录重大架构决策变更

**结论**：Phase 6/7改为Partial→Component化，保留Client/Server为薄壳，0外部改动。Phase 6-1字段迁移已回滚。

---

## [2026-04-07 23:59:45] 进度: Phase 6 策略变更：回滚 6-1 字段迁移，改为 Partial→Component 抽取方案（保留 RoleLogicClient/Server 类）

**背景**：[DL] 执行任务

**推理**：用户确认不删除中间层，改为组件化抽取

**结论**：Phase 6 策略变更：回滚 6-1 字段迁移，改为 Partial→Component 抽取方案（保留 RoleLogicClient/Server 类） — ✅

---

## [2026-04-07 23:59:38] ADR#15: Phase 6 策略变更：保留 RoleLogicClient/Server

**背景**：Phase 6 策略变更：保留 RoleLogicClient/Server

**推理**：881个外部引用替换风险过高，保留中间层可避免大规模批量替换

**结论**：不删除 RoleLogicClient 和 RoleLogicServer，保留为生命周期壳 + 字段容器。Partial 逻辑抽取为 BattleRoleLogicComponent 子类，通过 AddComponent 注册。Phase 6-1 字段迁移已回滚。

---

## [2026-04-07 23:37:11] 文档: RoleLogic_ClientFields.cs

**背景**：文档状态变更

**推理**：新建 BattleRoleLogic partial 文件，包含原 RoleLogicClient 40 个字段

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_ClientFields.cs` — ✅

---

## [2026-04-07 23:37:03] 进度: Phase 6-1: Client 字段迁移完成 — 40 个公开字段/属性迁移到 RoleLogic_ClientFields.cs，RoleLogicClient 改为转发属性，编译通过

**背景**：[DL] 执行任务

**推理**：Client 字段成功迁移到 BattleRoleLogic partial，0 外部文件改动

**结论**：Phase 6-1: Client 字段迁移完成 — 40 个公开字段/属性迁移到 RoleLogic_ClientFields.cs，RoleLogicClient 改为转发属性，编译通过 — ✅

---

## [2026-04-07 23:08:59] 门控: p5 Phase 5 完成门控

**背景**：p5 Phase 5 完成门控 门控检查

**推理**：Phase 1-5全部完成：主文件3503→122行(-96.5%), 23个BattleRoleLogicComponent, 枚举提取, 目录重组; Phase 6/7计划已制定(重构进度计划.md v3.0), ADR#14已确认方案A

**结论**：✅ 通过

---

## [2026-04-07 22:26:55] 文档: 重构进度计划.md v3.0

**背景**：文档状态变更

**推理**：追加Phase6(Client打散)和Phase7(Server打散)详细计划，更新Phase1-5状态为已完成

**结论**：`aigc/docs/GamePlay_Dev/架构迁移/BattleRoleLogic重构/重构进度计划.md` — ✅

---

## [2026-04-07 22:26:47] Server/Client 打散规模分析

**背景**：RoleLogicServer 22 partials ~10,720行, 11个IRoleLogicServer子循环, 449外部引用文件; RoleLogicClient 7 partials ~2,553行, 432外部引用文件; 总计~13,273行, 881外部文件

**推理**：Client无子循环(仅AddFeature)，打散较简单，适合作PoC; Server有11个子循环(IRoleLogicServer)，可自然映射为BattleRoleLogicComponent(已有Init/OnUpdate/Clear生命周期); 外部引用主要是字段访问(roleLogicServer.Property)，可通过脚本化find-replace处理; 代理过渡策略(转发属性)可实现0外部改动的中间态

**结论**：制定Phase6(Client打散)+Phase7(Server打散)两阶段计划，先Client后Server; 更新重构进度计划.md v3.0

---

## [2026-04-07 22:26:33] ADR#14: Server/Client 打散方案选择

**背景**：Server/Client 打散方案选择

**推理**：虽然外部引用达881文件，但方案A可消除Server/Client中间层实现统一组件模型。通过代理过渡（转发属性）降低中间态编译风险，脚本化批量替换控制变更质量

**结论**：方案A：全面打散 RoleLogicServer(~10,720行) 和 RoleLogicClient(~2,553行) 融入 BattleRoleLogic，消除中间层。先Client后Server，代理过渡+批量替换

---

## [2026-04-07 19:08:56] 进度: 补移RoleLogic_MOOD.cs到BattleRoleLogic/目录

**背景**：[DL] 执行任务

**推理**：遗漏的partial文件，必须与主文件同目录

**结论**：补移RoleLogic_MOOD.cs到BattleRoleLogic/目录 — ✅

---

## [2026-04-07 19:03:16] Bug#15 修复

**背景**：CS2001 BattleRoleComponent.cs not found

**推理**：Role目录孤立meta文件

**结论**：删除orphan meta

---

## [2026-04-07 19:03:06] 进度: 目录重组：BattleRoleLogic文件迁移到BattleRoleLogic/子目录，编译通过

**背景**：[DL] 执行任务

**推理**：参照BattleRole目录结构统一组织

**结论**：目录重组：BattleRoleLogic文件迁移到BattleRoleLogic/子目录，编译通过 — ✅

---

## [2026-04-07 18:53:44] 文档: RoleLogicEnums.cs

**背景**：文档状态变更

**推理**：Phase5枚举文件创建

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/` — ✅

---

## [2026-04-07 18:53:36] 进度: Phase 5 完成：LocalRoleSyncState→RoleLogicEnums.cs, checkUserWeaponTime死代码清理

**背景**：[DL] 执行任务

**推理**：枚举提取+死代码清理，编译通过

**结论**：Phase 5 完成：LocalRoleSyncState→RoleLogicEnums.cs, checkUserWeaponTime死代码清理 — ✅

---

## [2026-04-07 18:36:29] 进度: 4D-13 Ground 确认已完成（之前批次已迁移），4D 补充迁移全部完成

**背景**：[项目负责人] 执行任务

**推理**：Ground已是Facade+Component，4D-10~13全部完成

**结论**：4D-13 Ground 确认已完成（之前批次已迁移），4D 补充迁移全部完成 — ✅

---

## [2026-04-07 18:36:22] 文档: RoleLogicUprearComponent.cs

**背景**：文档状态变更

**推理**：Uprear组件文件已创建

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/` — ✅

---

## [2026-04-07 18:36:12] 进度: 4D-12 Uprear 组件完成（RoleLogicUprearComponent 2 handlers, 93→12行）

**背景**：[DL] 执行任务

**推理**：Uprear迁移完成，编译通过

**结论**：4D-12 Uprear 组件完成（RoleLogicUprearComponent 2 handlers, 93→12行） — ✅

---

## [2026-04-07 18:32:13] 进度: 4D-11 Weapon 组件补充完成（+4 handlers, +shootTime字段, 145→108行）

**背景**：[DL] 执行任务

**推理**：Weapon追加迁移完成，编译通过

**结论**：4D-11 Weapon 组件补充完成（+4 handlers, +shootTime字段, 145→108行） — ✅

---

## [2026-04-07 18:23:59] 文档: RoleLogicMoveComponent.cs

**背景**：文档状态变更

**推理**：Move组件文件已创建

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/` — ✅

---

## [2026-04-07 18:23:50] 进度: 4D-10 Move 组件完成（RoleLogicMoveComponent 4 handlers，169→~80行）

**背景**：[DL] 执行任务

**推理**：Move迁移完成，编译通过

**结论**：4D-10 Move 组件完成（RoleLogicMoveComponent 4 handlers，169→~80行） — ✅

---

## [2026-04-07 13:51:41] 文档: RoleLogicWuLinComponent.cs

**背景**：文档状态变更

**推理**：4D-9a 武林客栈区域检测组件

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicWuLinComponent.cs` — ✅

---

## [2026-04-07 13:51:32] 进度: 4D-9a WuLin Component 迁移完成（1事件+Facade+Component+注册，3字段迁移）

**背景**：[DL] 执行任务

**推理**：CheckRoleInWuLinArea自包含，3私有字段全部迁入组件

**结论**：4D-9a WuLin Component 迁移完成（1事件+Facade+Component+注册，3字段迁移） — ✅

---

## [2026-04-07 12:33:05] 规范沉淀#8

**背景**：规范沉淀新增

**推理**：连续2个新组件均犯此错误，需沉淀为规范

**结论**：BattleRoleLogicComponent 的 OnAwake/OnClear 继承自 BattleComponent，访问修饰符为 protected，新组件必须用 protected override 而非 public override

---

## [2026-04-07 12:32:57] Bug#14 修复

**背景**：CS0507: cannot change access modifiers when overriding protected inherited member

**推理**：OnAwake/OnClear基类为protected，新组件误用public override

**结论**：改为protected override

---

## [2026-04-07 12:28:40] ADR#10: 4D-8 Jump组件职责拆分

**背景**：4D-8 Jump组件职责拆分

**推理**：用户要求职责分离，足球区域检测与跳跃参数是独立关注点

**结论**：拆分为 JumpComponent（跳跃配置+特殊移动）+ FootballAreaComponent（足球区域检测），职责更纯粹

---

## [2026-04-07 12:28:29] 文档: RoleLogicFootballAreaComponent.cs

**背景**：文档状态变更

**推理**：4D-8b 足球区域拆分

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicFootballAreaComponent.cs` — ✅

---

## [2026-04-07 12:19:45] 文档: RoleLogicJumpComponent.cs

**背景**：文档状态变更

**推理**：4D-8 Jump组件

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicJumpComponent.cs` — ✅

---

## [2026-04-07 12:19:36] 进度: 4D-8 Jump Component 迁移完成（5事件+Facade+Component+注册）

**背景**：[DL] 执行任务

**推理**：纯计算方法无状态迁移，WarData静态访问无需桥接

**结论**：4D-8 Jump Component 迁移完成（5事件+Facade+Component+注册） — ✅

---

## [2026-04-07 11:38:01] 文档: RoleLogicPhysicsComponent.cs

**背景**：文档状态变更

**推理**：4D-7 三步迁移产出：物理/推人/速度组件

**结论**：`Assets/Script/GamePlay/Host/Modules/Role/Component/RoleLogicPhysicsComponent.cs` — ✅

---

## [2026-04-07 11:37:46] 进度: 4D-7 Physics 组件迁移完成（Events+Facade+Component）

**背景**：[DL] 执行任务

**推理**：176行 → Facade 57行 + Component 158行。6个事件（Query/Cmd各3个），4个私有字段迁入Component。简单字段(IsPushRoleDir/RollSpeed/RollDir)和IsPushRole属性保留在Facade

**结论**：4D-7 Physics 组件迁移完成（Events+Facade+Component） — ✅

---

## [2026-04-07 11:30:29] 进度: active.md 重组（添加 session-sync.sh 7 个锚点节）

**背景**：[项目负责人] 执行任务

**推理**：active.md 手动创建时缺少锚点节，progress/doc/bug 命令无法执行

**结论**：active.md 重组（添加 session-sync.sh 7 个锚点节） — ✅

---

## [2026-04-07 11:30:07] active.md 重组兼容 session-sync.sh

**背景**：active.md 手动创建时缺少 session-sync.sh 要求的锚点节（主进度/文档产出清单/关键决策/Bug记录/规范沉淀/遗留待确认/门控记录），导致 progress/doc/bug 等命令报错未找到锚点

**推理**：对照 _template_dev() 模板和各 cmd_* 函数的 insert_before_section 调用，确认需要 7 个锚点节及其先后顺序。保留原有领域内容（当前进度/迁移定义/行数记录/文件快照）在上半部分不动，下半部分替换为 session-sync 兼容的节结构，迁移关键技术决策和规则沉淀内容到新格式中

**结论**：active.md 下半部分（L122-191）重写为 session-sync 兼容格式。7 个锚点全部就位，progress/doc/bug 命令 dry-run 验证通过。原有门控记录/回滚参考/Background Agent 记录保留在末尾

---

## [2026-04-07] 4D-6 AI：组件内部方法调用不走 Dispatcher

**背景**：`aiEvent()` 内部调用 `CheckAIUseWeapon()`，`GetAILockTargetRole()` 内部调用 `setAILockRole()`。如果两者都是 Facade，Component handler 中如何调用？  
**推理**：同一 Component 内的两个 handler 完全可以共享私有方法，无需再走 Dispatcher 绕一圈。`SetAILockRoleInternal`、`CheckAIUseWeaponInternal`、`GetAIUserWeaponIdInternal` 作为私有方法被多个 handler 复用。  
**结论**：同一 Component 内部的逻辑复用使用 `xxxInternal()` 私有方法，不走 Dispatcher。只有跨 Component 的通信才需要事件派发。

---

## [2026-04-07] 4D-5 Reconnect：跨模块私有方法内联策略

**背景**：`OnRoleReconnect` 调用 `OnRoleReconnectResetState()`，该方法为 `RoleLogic_States.cs` 中的 private 方法（仅含两行 `SetState` 调用）。  
**推理**：该方法为 private，Component 无法访问。选项：① 改为 public → 暴露不必要接口；② 创建新事件 → 过度设计；③ 内联两行 SetState 调用 → 最简洁。  
**结论**：将 `OnRoleReconnectResetState()` 的两行 `SetState` 调用直接内联到 Component 中，不修改 States 文件的访问权限。跨模块 private 方法若足够简单（≤3行），优先内联。

---

## [2026-04-07] 4D-4 HP：属性 setter 拦截器的 CallBack 模式

**背景**：`OnSetHp`/`OnSetMaxHp` 被 `RoleLogic_Fields.cs` 中的属性 setter 调用（`set => hp = OnSetHp(hp, value)`），需要返回值。  
**推理**：Dispatcher 是 void 返回，但因为是同步执行，可以用 `Action<float> CallBack` 模式在事件 handler 中回写结果。setter 调用 Dispatcher 后，callback 已经执行完毕，返回值已通过闭包捕获。  
**结论**：ProcessSetHp/ProcessSetMaxHp 事件新增 `oldValue`、`newValue`、`CallBack` 三个字段。Component handler 计算结果后调用 `CallBack(result)`，Facade 中 `float r = newValue; Dispatcher(new ... { CallBack = v => r = v }); return r;` 模式捕获返回值。

---

## [2026-04-06] KnockoutItem 原子读写字段不宜事件化

**背景**：`isKnockoutDisconnect` 在 StartGame.cs 中是先读后写（`if (!role.isKnockoutDisconnect) { role.isKnockoutDisconnect = true; }`）。  
**推理**：这是原子性的"检查并设置"模式，如果拆成 Query + Cmd 两个事件，中间有重入风险。保留为 public field 比迁入 Component 更安全，且该字段无复杂副作用。  
**结论**：KnockoutItem 和 isKnockoutDisconnect 保留在 RoleLogic_Knockout.cs 为 public 字段；只有 SetRank() 因为会操作 roleLogicServer 而迁成 CmdSetRank 事件。

---

## [2026-04-06] 主文件禁止直接访问 Component 私有字段

**背景**：`BattleRoleLogic.cs:330` 直接写 `teammateBulletNum = UserWeapon.IPickItemClient.GetMaxBulletNum()`，但 `teammateBulletNum` 是 `RoleLogicTeammateWeaponComponent` 的 private 字段。  
**推理**：主文件和 Component 是不同类，主文件无法直接访问 Component 的 private 字段。应通过 `Dispatcher(SetTeammateBulletNum)` 走事件通道写入。  
**结论**：改为 `Dispatcher(new BattleRoleLogicEvents.SetTeammateBulletNum { value = … })`。凡主文件需要写入 Component 持有的状态，一律走 Set 事件，不跨类访问私有字段。

---

## [2026-04-06] Facade 文件事件调用缺 BattleRoleLogicEvents 前缀

**背景**：`RoleLogic_TeammateBehavior.cs`（Facade）全文件事件调用均写成 `new CmdTeammateMove {…}`，编译器找不到类型（CS0246），因为所有事件定义在 `public static class BattleRoleLogicEvents` 内。  
**推理**：事件类型作为 `BattleRoleLogicEvents` 的嵌套类型，在外部访问必须加限定前缀。前次写入时遗漏。  
**结论**：全文件所有 `new Cmd*/Query*/Set*` 调用一律补全 `BattleRoleLogicEvents.` 前缀。后续写 Facade 文件时，默认加前缀，避免重复踩坑。

---

## [2026-04-06] 4B-1 TeammateBehavior — ActionComponent AI 幻觉修复

**背景**：4B-1 ActionComponent 中 Car/Cannon/StandBy 三个 handler 由 AI 生成，大量 API 均不存在（`CarManager.GetCar`、`RoleLocalState.IsUseCar`、`Proto_RoleTeammate.CmdUseCar/LeaveCar/LeaveCannon/CmdStandBy`、`RemoveUser` 等）。  
**推理**：服务端载具/大炮操作走的是 `carNetServer.SetCarServer/removeCarServer` + `gameWorld.ServerBuffControl` 直调模式，不走 Proto 消息；大炮走 `myPlayBoxControlLogic.setPlayBoxLine`；站姿走 `ClientRpc(RpcStandByState)`。这些在原始备份（`Back/RoleLogic_TeammateBehavior.cs` 1087-1196行）有完整实现。  
**结论**：对照备份原始实现重写三个 handler；增加 `List<int> mysteryCheck` 字段；新增辅助方法 `ResetShipPos`。

---

## [2026-04-05] 4A-7 Mode — GoGoParty struct 字段不能迁入 Component

**背景**：BattleRoleLogic_GoGoParty.cs 有 4 个 public struct 字段（goGoPartyModeScoreData 等），外部代码直接做子字段赋值（`role.goGoPartyModeScoreData.clockWorkCoin = 5`）。  
**推理**：C# 中对 struct 的子字段赋值要求父字段是 field（不能是 property），否则操作的是临时副本，不会写回。如果通过 Query 事件返回 struct 再赋值，修改会被丢弃。  
**结论**：GoGoParty 的 struct 定义和 public 字段留在 BattleRoleLogic_GoGoParty.cs 不动，不迁入 Component，不创建事件。BladeBall/FightClose 为纯计算属性同理保持原样。

---

## [2026-04-04] 4A-5 Weapon 迁移：roleLogicClient 的公开性决定 Component 可行性

**背景**：GetGunBayonetRangeEnemy() 内部大量调用 `roleLogicClient.RoleClient.MyRoleControl`，Component 要迁入此方法，必须能访问 `roleLogicClient`。  
**推理**：在执行前确认 RoleLogic_Fields.cs:554 `public RoleLogicClient roleLogicClient`，为 public 字段，Component 可通过 `roleLogic.roleLogicClient` 访问，无需暴露额外接口。  
**结论**：GetGunBayonetRangeEnemy 可以全量迁入 RoleLogicWeaponComponent，无阻塞点。私有辅助方法 CanBeLockedTarget / AddLockEnemyList 一同迁入为 Component 私有方法。

---

## [2026-04-03] 4D-3 Instruction：TeamAiCreateItemTime 字段的最小暴露原则

**背景**：TeamAiCreateItemTime 是 public float 字段，ServerRoleAILogic.cs 只做写入（`roleNet.MyRole.TeamAiCreateItemTime = TimeData.time;`），不做读取。但 IsTeamAiCreateItemIntervalTime 属性内部计算依赖它。  
**推理**：IsTeamAiCreateItemIntervalTime 的计算（TimeData.time - TeamAiCreateItemTime < interval）完全可以在 Component 内完成，外部只需拿到 bool 结果；TeamAiCreateItemTime.get 外部无读需求，返回 0f 即可。  
**结论**：TeamAiCreateItemTime.get 简化为返回 0f，不增加 QueryTeamAiCreateItemTime 事件；IsTeamAiCreateItemIntervalTime.get 走 QueryIsTeamAiCreateItemIntervalTime 事件；Component 内部自主维护 _teamAiCreateItemTime 状态，减少无效事件数量。

---

## [2026-04-03] 4D-2 Ground：public 字段改 property 与 Dispatcher 的兼容性

**背景**：groundPoint 原为 public Vector3 字段，NetworkClient_StartGame.cs 直接做 `roleLogic.groundPoint = data.groundPoint;` 赋值。Component 化后状态移入 Component，需要外部仍能写入。  
**推理**：C# 属性（property）完全兼容字段赋值语法，外部调用方无需修改；get 外部无读取只需返回 Vector3.zero 即可；写 set 触发 Dispatcher → Component 更新 _groundPoint。  
**结论**：将 `public Vector3 groundPoint` 字段改为属性，get 返回 Vector3.zero，set 派发 SetGroundPoint 事件。外部赋值语法不变，零改动。

---

## [2026-04-03] 4D 阶段：AddComponents() 应加注释

**背景**：BattleRoleLogic.cs 的 AddComponents() 列表原本无任何注释，仅有 12 行 AddComponent<>，不看 Component 文件无法知道每个组件的职责。  
**推理**：随着 4D 阶段持续新增 Component，列表会越来越长，无注释会导致后续维护者难以快速定位职责归属。用户明确提出"后面需要加上组件说明注释"。  
**结论**：每次注册新 Component 时，同步补充行尾注释，格式：`// 一句话说明（核心状态 / 方法）`；补全现有 12 行存量注释。

---

## [2026-04-03] 新会话恢复：框架更新核对

**背景**：用户更新了 AIGC 框架，调整了 agent 内容，需要核对新框架与 BattleRoleLogic重构 现状的差异。  
**推理**：对比新旧 AGENTS.md 发现 4 处变化：① [SESSION_DELTA] 新增 `需更新 session-log.md` 字段；② Pre-Flight Protocol（§五）为新增门控；③ active-guide.md 要求补建 session-log.md；④ active.md 格式建议改为体验节点结构。  
**结论**：优先补建 session-log.md（本文件）；active.md 格式问题待用户决策；Pre-Flight Protocol 从下一次代码操作起执行；[SESSION_DELTA] 格式从本次起更新。

---

## [2026-04-02] 字段重复声明问题

**背景**：`birthIslandSetting`/`bornData` 在 Init 文件顶部声明区 + `OnApplicationForce` 前各写了一次，引发 CS0102 重复成员错误。  
**推理**：重构时从原文件复制代码块，容易把字段声明带入已有声明区域。  
**结论**：重构时每次迁移前，检查目标文件是否已有同名字段声明，避免同一 partial class 内二次声明。

---

## [2026-04-02] Component 访问 BattleRoleLogic 字段需用公开属性

**背景**：4A-4 Skill 迁移时，`OnGandaFlyExit` 使用了 `roleLogic.isLocalRole`（private 字段），引发 CS0122。  
**推理**：Component 是独立类，对 BattleRoleLogic 的 private 字段不可见。必须通过公开属性访问。  
**结论**：Component 内访问 BattleRoleLogic 字段时，必须使用公开属性（`IsLocalRole` 而非 `isLocalRole`）。若公开属性不存在，需先在 BattleRoleLogic 中补充。

---

## [2026-04-02] Component 内访问基类属性的规范

**背景**：`RoleLogicLobbyComponent` 中写 `MyStartGame.ServerTime`，引发 CS0103 编译错误。  
**推理**：`MyStartGame` 是 BattleRoleLogic 的自定义属性名，Component 继承的是 `BattleRoleLogicComponent`，基类提供的是 `startGame`（小写）访问器。  
**结论**：Component 内访问 StartGame 用 `startGame`（小写基类属性），不是 `MyStartGame`。规则沉淀入 active.md。

---

## [2026-04-02] 主文件（目录文件）模式对齐 BattleRole.cs

**背景**：`BattleRoleLogic.cs` 原本无目录结构，`Awake`/`init`/`AddComponents` 都扎堆在 Init partial，主文件无法起到目录导航作用。  
**推理**：参考同项目 `BattleRole.cs` 的模式，主文件应该是生命周期骨架 + AddComponents 的索引入口，细节由各 InitXxx 辅助方法分离到 Init partial。  
**结论**：将 Awake/init骨架/AddComponents/Loop 迁入主文件，init 细节拆成 `InitRoleData / InitLoops / InitClient / InitServer` 辅助方法留在 Init partial，主文件 init() 只做调用链。顶部追加索引注释块。

---

## [2026-04-02] 枚举处理策略

**背景**：迁移 4A-1 `RoleLogicLocalStates` 时，`LocalRoleSyncState` 枚举被误删，引发全项目 CS0246 编译错误。  
**推理**：枚举是顶层类型，其他 Partial 或外部文件可能引用。若跟着 Partial 一起迁走，Facade 文件就变成空壳，断掉引用。  
**结论**：迁移前必须 `grep "^public enum|^public struct|^public class"` 检查 Partial 顶层类型；有输出则保留在 Facade 文件顶部。阶段 5 统一迁到 `RoleLogicEnums.cs`，届时类型名不变、零外部改动。

---

## [2026-04-02] 迁移"完成"的三步定义

**背景**：阶段 3A/3B 建了 7 个空壳 Component，但只有结构没有实现，导致进度无法衡量。  
**推理**：空壳不能算完成，否则会导致"文件已建但逻辑未迁"的假完成状态。需要明确定义什么才算一个 Component 的迁移完成。  
**结论**：三步缺一不可：① 事件定义（在 Events.cs 定义 struct）→ ② Facade 替换（Partial 改为单行 Dispatcher）→ ③ Component 实现（OnAwake 注册 + OnClear 反注册）。阶段 3A/3B 产出标记为废弃，不计进度。

---

## [2026-04-01] 继承链与组件基类的选型

**背景**：BattleRoleLogic 原为一个超 3500 行的巨型类，需要拆分为组件化结构。需要决定继承链和组件基类。  
**推理**：BattleRoleLogic 本身已经继承了游戏核心基类，需要对齐项目已有的 BattleSystemBase 继承模式。组件基类需要和 BattleComponent 对齐，才能和整体框架一致。  
**结论**：`BattleRoleLogic` 继承 `BattleSystemBase`；`BattleRoleLogicComponent` 继承 `BattleComponent`。

## [2026-04-08 17:04:06] 进度: M-8.2 done: 3 external-ref Features converted (PowerSkill/Adsorb/HandInHand), 28 GetFeature refs replaced, build pass 0 errors

**背景**：[DL] 执行任务

**推理**：Mechanical pattern + batch replace + compile verify

**结论**：M-8.2 done: 3 external-ref Features converted (PowerSkill/Adsorb/HandInHand), 28 GetFeature refs replaced, build pass 0 errors — ✅

---

