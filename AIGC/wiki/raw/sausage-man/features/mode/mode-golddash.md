---
name: mode-golddash
display_name: 撤离模式（GoldDash）
category: mode/golddash
version: 1.0.0
dependencies:
- mode-base
---

# 撤离模式（GoldDash）

撤离模式：玩家在限时内收集金币并撤离，支持 PvPvE 玩法，包含撤离点、金库、AI 敌人等子系统。最大模式模块，C/S/H 三端共计约 264 文件

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/ClientGoldDashData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/ClientGoldDashEventId.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/ClientGoldDashMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashAirdropLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashAltarLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashBackpack.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashBlackMarketLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashBornLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashBossRushLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashDeadModelLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashEscapePointLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashGameOverMsgLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashItemOutLineLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashKeyRoomLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashMapInfoLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashMapLevelLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashMonsterLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashRookieGuideLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashSausage2Logic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashSceneLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientMatchModeExtConfOverrideGuideLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/ClientGoldDashBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/ClientGoldDashRoleBoxItemMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/ClientGoldDashRoleBoxOpenMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/Data/ClientGoldDashBoxData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/Data/ClientGoldDashBoxItemData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/GoldDashBox/Data/ClientGoldDashBoxProtectData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientGoldDashInGameEventMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientGoldDashInGameEventMgr_Constructor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientGoldDashInGameTaskMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientGoldDashMermaidTaskTipsLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameEventMoreRewards.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameEventSearchClue.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameEventSearchClueFind.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameEventSearchClueTime.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameMonsterSquad.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/ClientInGameTask.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/InGameEvent/InGameTaskTouchMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Interactable/ClientGoldDashInteractItemTriggerMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Interactable/ClientGoldDashInteractLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Interactable/ClientGoldDashInteractStateRunTime.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Interactable/ClientGoldDashInteractable.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideBullet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideEliteEnemy.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideEscape.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideEscaping.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideFirstKill.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideGameStart.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideMonsterFind.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideSafeBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideSeniorEnemy.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideTreausryBoxFind.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideUseMed.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashHardSteps.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashSoftSteps.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialAIBattle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialEscape.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialMap.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialMoveToTarget.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/ClientGoldDashTutorialSearchQte.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/GoldDashTutorialMask.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/GoldDashTutorialMaskWin.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/GoldDashTutorialMaskWinController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/Tutorial/GoldDashTutorialRectWidget.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/AbsGoldDashColliderMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BlindingShieldBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BlindingShieldView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/ClientGoldDashDeadModelData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/ClientGoldDashUtils.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/ColliderMoveToTopIfPlayerInside.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/ColliderMoveToTopIfPlayerInside4Sides.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashAirDropBoxView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashAirPlane.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashAltarBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashAltarEmpty.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashAltarView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashBoxRandomData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashDeadModelMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashEscapePointMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashInteractableMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashInteractableMonoStateEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashKeyRoomView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashMapArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashMiniMapDebugger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashRewardMissionPosTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashRookieCampClickHide.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashShowItemPoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashTreasureChestView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/GoldDashWarBoxData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/RoleGoldDash.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/SOGoldDashRookieCampTutorial.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BlackMarket/ClientGoldDashBlackMarket.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BlackMarket/ClientGoldDashBlackMarketItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BlackMarket/RandomBlackMarketAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/BoxOutLineComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoAirThrow.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoBoss.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoCommon.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoDeadBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoDrone.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoEmpty.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxMonoJrone.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/GoldDashBoxQTEChest.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/ItemOutLineComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/AbsGoldDashBoxMonoComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoBelongHeader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoBoxEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoBoxEffectBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoBoxSound.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoColliderMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoDefaultEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoItemEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoOutLine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoProtectBelongHeader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoSceneMark.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoTutorialCommonBoxEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Other/BoxMono/MonoComponent/GoldDashBoxMonoTutorialDeadBoxEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Stage/ClientGoldDashBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Stage/ClientGoldDashOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Stage/ClientGoldDashRunningStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/ServerGoldDashData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/ServerGoldDashEventId.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/ServerGoldDashMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/GoldDashRoleLogicPuzzlePieces.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerAIFightSessionComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashAICreateLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashActionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashAirdropLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashAltarLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBackpackFullLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBlackMarketLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBossAirWallLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBossAllocateLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBossJokerLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBossOctopusLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBossRushLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBoxCreateLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashDeadLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashEscapePointCreateLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashEscapePointLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashGameOverLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashInteractTreasuryHouseLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashItemCreateLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashItemEntryLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashKeyRoomLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashLoginErrorLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashLookLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashMapIconLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashMapMonsterLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashMermaidLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashModeAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashPickAuthoringLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashPortablePointLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashRandomBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashRankScoreLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashRewardTaskLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashRoleInitLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashSImulateOpenBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashSausage2Logic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashSceneLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/ServerGoldDashStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/GoldDashInteractFactory.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/GoldDashInteractManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/GoldDashInteractStateRunTimeBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/GoldDashInteractStateTransition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/GoldDashParamParser.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/ServerGoldDashInteractStateRunTime.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/ServerGoldDashInteractable.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/ServerGoldDashInteractableLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/CountdownTimeTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/GameTimeTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/HaveItemTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/IFunctionTriggerCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/MissionStatusTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/PrefabStatusTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/SubmitItemTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/TargetEquipmentTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/TargetWeightBelowTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/IFunctionTriggerCondition/UseItemTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateChangeCondition/AfterFunctionCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateChangeCondition/AfterUseCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateChangeCondition/IStateChangeCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateChangeCondition/KillGPOMonsterCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateChangeCondition/PrefabStatusCondition.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/ConditionEscapePointCreateFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/EscapePointCreateFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/EscapeSuccessNowFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/EscapeTimePointCreateFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/IInteractFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Interactable/StateFunciton/TreasuryHouseFunction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Settlement/ServerGoldDashRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Settlement/SettlementDropLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Settlement/SettlementItemLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Settlement/SettlementRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Settlement/SettlementTestLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Logic/Tutorial/ServerGoldDashTutorialLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/EscapePointNumLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashDataUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashDeadModelData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashItemData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/POIAreaChecker.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/RoleLogicGoldDashServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ServerGoldDashBlackMarket.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ServerGoldDashDeadModelData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/AbsGoldDashStateBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/ServerGoldDashStateBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/AbsGoldDashBoxCompoent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/GoldDashBoxItemComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/GoldDashBoxOpenComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/GoldDashExplodeItemComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/GoldDashProtectComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/GoldDashBox/Component/SOExplodeItemSetting.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashInGameEventMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashInGameEventMgr_AutoSync.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashInGameEventMgr_Constructor.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashInGameTaskInfo.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashMermaidTaskDriver.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerGoldDashTimeTaskDriver.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEvent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventAirDrop.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventCallEventDirector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventCatchCrab.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventConditionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventKillTarget.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventMonsterSquad.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventMoreRewards.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventSearchChest.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventSearchClue.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventSearchClueFind.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventSearchClueTime.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventStealth.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameEventWealthGod.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/ServerInGameTask.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/Checker/ServerInGameEventCheckHasEnoughChest.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/InGameEvent/Checker/ServerInGameEventCheckHasEnoughMonster.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ItemCreator/GoldDashBag.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ItemCreator/GoldDashBagContainer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ItemCreator/GoldDashItemContainer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ItemCreator/GoldDashItemGroup.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Other/ItemCreator/GoldDashItemGroupContainer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Stage/ServerGoldDashBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Stage/ServerGoldDashOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoldDash/Stage/ServerGoldDashRunningStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/GoldDashBlackMarketProtectTimeData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/GoldDashConditionQuery.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/GoldDashInGameEventUtils.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/GoldDashInteractableStateBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/IGoldDashInteractReadAble.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/InGameEventConstructorData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEvent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventCatchCrab.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventKillMonster.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventMonsterSquad.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventMoreRewards.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventSearchChest.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/GoldDash/InGameEvent/SOGoldDashInGameEventSearchClue.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/AbsRoleTalent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashAltarSyncState.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashDynamicEntryEffectDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashInGameEventDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashInGameEventLevelDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashInGameTaskDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashRoleLogicBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashSuitEntries.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashTalentHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/GoldDash/GoldDashTutorial.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashPassiveSkill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleLogicLimitedRedPackets.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleLogicRandomItemServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleStatistics.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleTaskServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashStatisticsData.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/GoldDash/ [89 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientGoldDashActionFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientGoldDashSceneRenderFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientGoldDashSausage2Manager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerGoldDashActionFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerGoldDashSausage2Manager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/GoldDashRedItemPity.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDash/RedTempZone/ClientRedTempZoneEntityStateController.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDash/RedTempZone/ClientRedTempZoneEntityStateManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDash/RedTempZone/ClientRedTempZonePlayerStateController.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDash/RedTempZone/ClientRedTempZonePresenter.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDashDrag/GoldDashItemData.cs` |
| `Assets/Script/GamePlay/Client/Modules/GoldDashDrag/ItemDragManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/GoldDash/HostNoCollisionToLocalRole.cs` |
| `Assets/Script/GamePlay/Host/Modules/SOConfig/GoldDashEntryBuffConfig/SOGoldDashEntryBerserkerData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SOConfig/GoldDashEntryBuffConfig/SOGoldDashEntryCriticalBonusData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SOConfig/GoldDashEntryBuffConfig/SOGoldDashEntryDoubleEdgedSwordData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SOConfig/GoldDashEntryBuffConfig/SOGoldDashEntryFlauntData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SOConfig/GoldDashEntryBuffConfig/SOGoldDashEntryPorterData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/FastGoldDashCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/FastGoldDashCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatLogData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashRoleCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatGoldDashAI.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/IRedTempZoneTarget.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZoneAIAdpater.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZoneHpProcesser.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZoneJudger.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZoneJudgerManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZoneNumericService.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/RedTempZonePlayerAdapter.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/SORedTempZoneLevelData.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/ServerRedTempZoneAIStateController.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/ServerRedTempZoneEntityStateController.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/ServerRedTempZoneEntityStateManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/GoldDash/RedTempZone/ServerRedTempZonePlayerStateController.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Mode/` |
| `Assets/ToBundle/Role/Controllers/War/GoldDash/` |
| `Assets/ToBundle/Effect/Mode/GoldDash/` |

## 备注

GameMode 枚举 GoldDash=28. 共 264 文件. 三端分布: C=125/S=126/H=13. key_classes: ClientGoldDashData, ClientGoldDashAirdropLogic, ClientGoldDashAltarLogic, ClientGoldDashBlackMarketLogic, ClientGoldDashBornLogic, ClientGoldDashBossRushLogic, ClientGoldDashDeadModelLogic, ClientGoldDashEscapePointLogic, ClientGoldDashGameOverMsgLogic, ClientGoldDashItemOutLineLogic. 子目录: Client: Logic(65), Other(54), Stage(3); Server: Logic(76), Other(44), Stage(3); Host: InGameEvent(8). 含独立的撤离点、金库、AI 系统等复杂子模块

依赖：[[mode-base]]

## 关联 Buff


### 撤离模式 Buff（25）

| feature | 说明 |
|---------|------|
| [[buff-gd-entry-group-berserker]] | BSGdEntryGroupBerserker - GdEntryGroupBerserker |
| [[buff-gd-entry-group-critical-bonus]] | BSGdEntryGroupCriticalBonus - GdEntryGroupCriticalBonus |
| [[buff-gd-entry-group-double-edged-sword]] | BSGdEntryGroupDoubleEdgedSword - GdEntryGroupDoubleEdgedSword |
| [[buff-gd-entry-group-flaunt]] | BSGdEntryGroupFlaunt - GdEntryGroupFlaunt |
| [[buff-gd-entry-group-porter]] | BSGdEntryGroupPorter - GdEntryGroupPorter |
| [[buff-gold-dash-a-i-fight-status-effect]] | BSGoldDashAIFightStatusEffect - GoldDashAIFightStatusEffect |
| [[buff-gold-dash-air-drop-box]] | BSGoldDashAirDropBox - GoldDashAirDropBox |
| [[buff-gold-dash-altar]] | BSGoldDashAltar - GoldDashAltar |
| [[buff-gold-dash-back-pack-ratio]] | BSGoldDashBackPackRatio - GoldDashBackPackRatio |
| [[buff-gold-dash-boss-rush-fight-state]] | BSGoldDashBossRushFightState - GoldDashBossRushFightState |
| [[buff-gold-dash-box]] | BSGoldDashBox - GoldDashBox |
| [[buff-gold-dash-dead-model]] | BSGoldDashDeadModel - GoldDashDeadModel |
| [[buff-gold-dash-dragon-suit-entries]] | BSGoldDashDragonSuitEntries - GoldDashDragonSuitEntries |
| [[buff-gold-dash-evolution-station]] | BSGoldDashEvolutionStation - GoldDashEvolutionStation |
| [[buff-gold-dash-get-site]] | BSGoldDashGetSite - GoldDashGetSite |
| [[buff-gold-dash-interact-action]] | BSGoldDashInteractAction - GoldDashInteractAction |
| [[buff-gold-dash-interact-item]] | BSGoldDashInteractItem - GoldDashInteractItem |
| [[buff-gold-dash-joker-suit]] | BSGoldDashJokerSuit - GoldDashJokerSuit |
| [[buff-gold-dash-key-room]] | BSGoldDashKeyRoom - GoldDashKeyRoom |
| [[buff-gold-dash-load-scene]] | BSGoldDashLoadScene - GoldDashLoadScene |
| [[buff-gold-dash-passive-skill]] | BSGoldDashPassiveSkill - GoldDashPassiveSkill |
| [[buff-gold-dash-reward-mission]] | BSGoldDashRewardMission - GoldDashRewardMission |
| [[buff-gold-dash-scene-transfer]] | BSGoldDashSceneTransfer - GoldDashSceneTransfer |
| [[buff-gold-dash-transfer]] | BSGoldDashTransfer - GoldDashTransfer |
| [[buff-gold-dash-treasure]] | BSGoldDashTreasure - GoldDashTreasure |
