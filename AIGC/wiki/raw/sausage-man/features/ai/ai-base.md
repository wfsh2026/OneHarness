---
name: ai-base
display_name: AI 核心框架
category: ai/base
version: 1.0.0
dependencies:
- role-base
---

# AI 核心框架

RoleAI 三端核心框架：Host 层接口定义(IRoleAILogic/IRoleAIManager)、数据结构(RoleAIData/RoleAIInfo/RoleAIState)、Manager 生命周期管理、Logic 角色状态/武器/装备/特性管理、ServerFeature 服务端校验套件

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/IRoleAIFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/IRoleAILogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIArmor.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIData.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIDefenseTactics.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIExtendArmor.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIFeatureList.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIItemData.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIItemSlot.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIKnapsack.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAILogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIMedical.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIMLAgent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIRookieData.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIState.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIWeapon.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIWeaponEquip.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/Features/RoleAIBuffMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/Features/RoleAIFashionRandom.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/Features/RoleAILoadMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/IRoleAIManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/IRoleAIMgrFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/RoleAIItemMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/RoleAIManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/RoleAIMgrFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIManager/RoleAIMgrFeatureList.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/AIFindTargetPointAround.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIAnimator.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIAutoAiming.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIBallistic.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIBattleTime.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIBehavior.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIBuffState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAICaptainFly.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAICollisionEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIController.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIFashionShop.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIFeature.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIFly.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIGlide.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIHash.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIHitCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIHitRate.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIHypoxia.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIIdentity.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAILogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIMatMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIMoveBallistic.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIObserver.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIPathFinder.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIRayBallistic.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIResurrection.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAISkin.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAISocialFeature.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAISync.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIUprear.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIWeapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIWeaponController.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIWeaponData.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIWeaponSkin.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIXCCFeature.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ForbidNavMeshCollider.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/NavMeshLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/RoleAICheckMoveStuck.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/RoleAIEquip.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/RoleAIParachute.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/RoleAISkinManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/RoleAIXccModel.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/ClientRoleAIManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIBehaviorMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIBornMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIFlyMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIHealthMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAILoadMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIMgrFeature.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAINavMeshMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIOBCameraMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIOBMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIPickItemMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIReportMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAISyncMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIUIMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIArea.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIBehavior.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAICaptainFly.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIController.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIDataRequest.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIFly.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIHealth.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIHitCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIKillInfo.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIOnline.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIPathFinder.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIRecord.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIResurrection.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIState.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAISync.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIUprearAndHold.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIUseItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIWeapon.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerMirrorAIBridge.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerRoleAIFeature.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerRoleAILogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerRoleAISkin.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIAreaMoveMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIAwardMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIBehaviorMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIBornMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAICreateMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIFashionShopMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIHealthMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAILoadMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIMarkMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAINsqMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIOBMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIPickItemMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIProximityMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIReportMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAISyncMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIUprearMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/ServerRoleAIManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/ServerRoleAIMgrFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/ScriptableObject/RoleAIConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/ScriptableObject/RoleAIMgrConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/ScriptableObject/RoleAIWeaponConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/ClientRoleAIEffectManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/RoleAIAlien.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/RoleAIAr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/RoleAIBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/RoleAINormal.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAI/RoleAITraining.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/AIBehaviorHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/AIBehaviorManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/AITacticsNodeMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/AbsRoleAIAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Aim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Blocking.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Buff.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Crouch.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/DirectionMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Fall.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Far.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Fire.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Follow.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Glide.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Idle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Jump.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Move.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/OpenDoor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/PathMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/PlayTacticesAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Prone.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/RandomDir.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Reload.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Run.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Stand.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Action/Walk.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/AbsDelayConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/AbsRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/AttackTimeCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/CheckNextPoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/CheckPatrolState.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/FindAttackRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/FindLockRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/FindSeeRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/FindTacticesNode.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/HasForwardObstacle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/HasMoveDistance.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/HasState.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/HasTacticesNode.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/HasTargetObstacle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/IsEnoughBullet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/IsInAttackRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/IsInRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/IsTargetSwim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/Conditional/IsWeaponType.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/RoleAIBehavior.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/RoleAIBehavior_Net.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/RoleAIBlindageFightDate.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/RoleAIController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/RoleAILocalData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/SharedRoleAIBlindageFightDate.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/SharedRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAIBehavior/SharedTacticesNode.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAICheckMoveHit.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleAIControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleAIControl_AddAI.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/AI/ [109 files, 按模式/地图/难度的 AI 关卡配置]` |
| `Assets/ToBundle/ScriptableObject/RoleAI/ [51 files: Role/(9) 角色装备配置 + Weapon/(42) 武器配置]` |
| `Assets/ToBundle/Config/Txt/AiParamLocator.txt` |
| `Assets/ToBundle/Config/Txt/AIWeaponConfig.txt` |
| `Assets/ToBundle/Config/Txt/AIWeaponSkin.txt` |
| `Assets/ToBundle/Config/Txt/AiDropMap.txt` |
| `Assets/ToBundle/Config/Txt/RobotGun.txt` |
| `Assets/ToBundle/Config/Txt/SORoleAIItem.txt` |
| `Assets/ToBundle/Config/Txt/SORoleAIFashion.txt` |
| `Assets/ToBundle/Config/Txt/SORoleAIFashionShop.txt` |
| `Assets/ToBundle/Config/Txt/RookieCampAI.txt` |
| `Assets/ToBundle/Config/Txt/SOAnimatorAim.txt` |
| `Assets/ToBundle/Config/Txt/SOAnimatorAimPriority.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientAIFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerPerformAIManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/AnimaFootCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/AnimalController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/IAnimalCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/ICarSkill.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/Raptors.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/SwordTiger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/Trexking.cs` |
| `Assets/Script/GamePlay/Client/Modules/Animal/Triceratops.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/ClientRoleAIUtils.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIBlackArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIObjectPool.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIUtils.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/ServerRoleAIUtils.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/RoleAI/Prefabs/ [43 files: Role/(25) 角色预制体 + Ballistic/(5) 弹道 + RoleAIEquip/(12) 装备 + Weapon/(1)]` |
| `Assets/ToBundle/RoleAI/Animator/ [39 files: Role/(2) 角色动画控制器 + Weapon/(37) 武器动画控制器]` |

## 备注

AI 核心框架采用 C/S/H 三端架构，共 131 文件。三端分布: H=32/C=59/S=40。Host 层定义接口和数据结构，Client 层实现表现逻辑（动画/皮肤/特效/导航），Server 层实现校验逻辑（ServerFeature 套件含 18 个子文件覆盖状态/血量/武器/击杀/复活/同步等）。ServerMirrorAIBridge 负责与 2 代 AI 系统的桥接通信

依赖：[[role-base]]
