---
name: mode-knockout
display_name: 淘汰赛模式（Knockout）
category: mode/knockout
version: 1.0.0
dependencies:
  - mode-base
---

# 淘汰赛模式（Knockout）

淘汰赛：赛制休闲模式，多轮竞技逐步淘汰。包含关卡编辑器（Node 节点系统：Area/Box/Point/Trap）、多种赛制规则（Speed/Survival/Victory）、道具系统、反作弊检测。GameMode 枚举：LimitedtimeKnockout=14。C/S/H 三端 + UI 共 125 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Asset/Loaders/KnockoutLoader.cs` |
| `Assets/Script/Config/KnockoutRuleTableConfig.cs` |
| `Assets/Script/Config/KnockoutRuleTableConfigOverride.cs` |
| `Assets/Script/Config/KnockoutTableConfig.cs` |
| `Assets/Script/Config/KnockoutTableConfigOverride.cs` |
| `Assets/Script/Config/KnockoutUICloneObjConfig.cs` |
| `Assets/Script/Config/KnockoutUIObjConfig.cs` |
| `Assets/Script/Config/KnockoutUIObjPcConfig.cs` |
| `Assets/Script/Controller/KnockoutController.cs` |
| `Assets/Script/Controller/KnockoutLoadingController.cs` |
| `Assets/Script/Data/Base/PlayerKnockoutModeInfo.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutBornCheckLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutCameraLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutDeadCheckLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutEffectLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutHeartbeatLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutItemLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutMainLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutMusicLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutPlaying.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutSyncTimeLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/ClientKnockoutUILogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Knockout/RandomItem/KnockoutRandomItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Message/KnockoutItemMessage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleNetClient_Knockout.cs` |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_Knockout_Base.cs` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_Knockout.cs` |
| `Assets/Script/GamePlay/GameWorld_Knockout.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/AbsKnockoutLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/AbsKnockoutPlaying.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/AreaData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/BoxData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/CheatAreaData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/GroupData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/IReadWrite.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/ItemGroupData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/KnockoutData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/PointData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/PveGroupData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/PvePointData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/RoleAIPointData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Editor/KnockoutCreateEditor.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Editor/KnockoutReadEditor.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Editor/KnockoutTest.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Editor/KnockoutWriteEditor.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/IKnockoutData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/IKnockoutLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/IKnockoutPlaying.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Knockout.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/KnockoutDataMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/KnockoutLogicMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/Area.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/BirthNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/BoxNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/CheatArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/CheatNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/ChestPoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/DeadNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/Group.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/ItemGroup.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/ItemNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/ItemPoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/NodeObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/Point.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/PveNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/PvePoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/RoleAIPoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/RootNode.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/SaveNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/SubLevelNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/TimerNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/TrapBoxNode.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/TrapNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/WinNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Knockout.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_Knockout.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_Knockout.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_KnockoutExpData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_KnockoutItemData.cs` |
| `Assets/Script/GamePlay/Server/GameWorldServerKnockout.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Data/ServerKnockoutRunData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Data/ServerKnockoutRunData_Method.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Data/ServerKnockoutStatsData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Data/ServerKnockoutStatsData_Method.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Playing/Data/KoutRule.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Playing/ServerKnockoutSpeedLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Playing/ServerKnockoutSpeedVictoryLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Playing/ServerKnockoutSurvivalLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Playing/ServerKnockoutSurvivalVictoryLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutCheatCheckLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutCheckOnlineLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutCompetitionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutHeartbeatLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutItemLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutMainLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutPlaying.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutPropsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutReportLogLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutReportNsqLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutTimeCheckLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutWinCheckLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Utils/ServerKnockoutHelper.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/Utils/ServerKnockoutNet.cs` |
| `Assets/Script/GamePlay/Server/Modules/KnockoutSystem/KnockoutData.cs` |
| `Assets/Script/GamePlay/Server/Modules/KnockoutSystem/KnockoutSystemManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Message/KnockoutExitLookMessage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Message/KnockoutGetItemMessage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/ServerNsqDataReport_Knockout.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Knockout.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetKnockoutLogin.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_Knockout.cs` |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_Knockout_Base.cs` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_Knockout.cs` |
| `Assets/Script/UI/Knockout/KnockoutWin.cs` |
| `Assets/Script/UI/KnockoutLoading/KnockoutLoadingWin.cs` |
| `Assets/Script/UI/War/Data/Knockout/PlayingData.cs` |
| `Assets/Script/UI/War/SO/Knockout/Rule/SOKnockoutSpeedRule.cs` |
| `Assets/Script/UI/War/SO/Knockout/Rule/SOKnockoutSpeedVictoryRule.cs` |
| `Assets/Script/UI/War/SO/Knockout/Rule/SOKnockoutSurvivalRule.cs` |
| `Assets/Script/UI/War/SO/Knockout/Rule/SOKnockoutSurvivalVictoryRule.cs` |
| `Assets/Script/UI/War/SO/Knockout/SOKnockoutConfig.cs` |
| `Assets/Script/UI/War/SO/Knockout/SOKnockoutRule.cs` |
| `Assets/Script/UI/WarModeTips/KnockoutKingTips.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Final_S_01.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_Awards.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_B_01.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_B_01_Art.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_B_02.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_B_03.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_C_01.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_C_02.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Speed_C_03.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/Knockout_Survival_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Final_S_01/Knockout_Final_S_01_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_A_01/Knockout_Speed_A_01_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_B_01/Knockout_Speed_B_01_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_B_02/Knockout_Speed_B_02_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_B_03/Knockout_Speed_B_03_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_B_03/TweenGo.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_C_01/Knockout_Speed_C_01_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_C_02/Knockout_Speed_C_02_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_C_03/Knockout_Speed_C_03_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Speed_C_03/TweenGo.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/Knockout_Survival_A_01/Knockout_Survival_A_01_SceneProps.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Final_S_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_Awards.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_B_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_B_01_Art.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_B_02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_B_03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_C_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_C_02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Speed_C_03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/Knockout_Survival_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Final_S_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_B_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_B_02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_B_03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_C_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_C_02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Speed_C_03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/KnockoutMode_SOKnockout_Survival_A_01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/SpeedVictory_A01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/SpeedVictory_B01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/SpeedVictory_B02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/SpeedVictory_C01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/SpeedVictory_S01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_A01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_B01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_B02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_B03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_C01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_C02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Speed_C03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Config/Survival_A01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Rule/Speed/Speed_Rule_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Rule/SpeedVictory/SpeedVictory_Rule_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Rule/Survival/Survival_Rule_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/Knockout/Rule/SurvivalVictory/SurvivalVictory_Rule_1.asset` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Final_S_01.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_A_01.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_B_01.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_B_02.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_B_03.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_C_01.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_C_02.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Speed_C_03.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Root_Knockout_Survival_A_01.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/LevelData/Knockout_Speed_B_01` |
| `Assets/ToBundle/Config/Txt/HostNet/LevelData/Knockout_Speed_B_01/SOElementConfig.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/LevelData/Knockout_Speed_B_01/SOElementPathConfig.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/LevelData/Knockout_Speed_B_01/SOGroupConfig.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/LevelData/Knockout_Speed_B_01/SOLevelConfig.txt` |
| `Assets/ToBundle/Config/Txt/KnockoutRuleTable.txt` |
| `Assets/ToBundle/Config/Txt/KnockoutUICloneObj.txt` |
| `Assets/ToBundle/Config/Txt/KnockoutUIObj.txt` |
| `Assets/ToBundle/Config/Txt/KnockoutUIObjPc.txt` |

## 备注

三端架构：Client (Playing+Logic) / Host (Knockout 核心 + Node 编辑器系统) / Server (Playing+Logic+KnockoutSystem)。Host 层含完整关卡编辑器（Area/Box/Point/Group/Trap 等节点类型）。

依赖：[[mode-base]]
