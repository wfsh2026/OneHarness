---
name: role-base
display_name: 角色系统核心基础
category: role
version: 1.0.0
dependencies: []
---

# 角色系统核心基础

BattleRole + BattleRoleLogic 核心生命周期管理，双层 Component 注册机制，IRoleLogic 接口，Fields 数据存储，角色创建/销毁流程

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/BattleRole.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/BattleRoleComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Init.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Clear.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_TimeEvent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Fields.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleATEventComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleAnimationComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleBladeBallComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleBuffComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCameraComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCarSyncComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCheckSceneItemComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleColliderComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCombatComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleConsumeItemComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleDanceComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleDefusalModeComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleDragonComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleEnergyBattleComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleEngageComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleEquipComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleFireComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleFlyComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleHideSeekComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleHitPartComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleHurtComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleJumpComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleMarkComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleMovePlatformComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleNetworkComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleOnlyUpComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRolePickItemComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRolePositionComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleReloadComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleRobotComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleShowComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSideAimComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSitComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSkinComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSlidingComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSneakSandComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSoundComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSqParachuteComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleStateComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleStateSyncComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleUprearRoleComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleWolfPartyComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/BattleRoleLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/BattleRoleLogicComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Fields.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Init.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Clear.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_TimeEvent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicAIComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicClientBladeBallComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicDataInfoComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicDungeonComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicFootballAreaComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicGroundComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicHPComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicInstructionComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicJumpComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicLobbyComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicLocalStatesComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicModeComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicPhysicsComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicReconnectComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicSkillComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicSwimComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateActionComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateBehaviorComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateFireComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicUprearComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicWuLinComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/IRoleLogicServer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleStateTypes.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/ClientRolePowerSkillManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/ClientRoleTalent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/GoldDashRoleLogicClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/HandInHandClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/HandInHandConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAutoOpenDoor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAutoOpenDoorHitBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAutoPickUp.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAutoRemind.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleCheckKaZhu.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClientComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_BladeBallMode.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_DuoJin.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Fields.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Football.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Item.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Misc.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Skill.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Vehicle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RolePressWeapon.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/BattleRoleEvents.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Camera.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_CheckSceneItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Fire.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_HideSeek.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_HitPart.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Item.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Mark.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Sound.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/AutoTestRoleData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/BattleRoleLogicEvents.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/BattleRoleLogicStaminaServer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/BattleRoleLogic_GoGoParty.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleCarSkin.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleDinoSkin.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleKillInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicCarShift.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicEnums.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicLimitedRedPackets.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicPathFinder.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogicServerComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_AI.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_BladeBallMode.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_DataInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_DungeonGame.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_FightClose.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Ground.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Instruction.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Inventory.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Jump.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Lobby.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_MOOD.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Mode.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_New.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Skill.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleSkillServer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/WarFlagData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleBombMove.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleBuffControl.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleFriendBubble.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/BattleRoleLogicStaminaClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/BattleRoyaleRoleLogicClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/Clownskill2AreaRoleLogicClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/GunBayonetRoleLogicClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/IItemRolelogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/MedicineInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/RoleLogicPassiveSkill.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleTriggerChecker.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GamePlayCheckConfigUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleLogicServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/GoldDashRoleLogicServerComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/HandInHandServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/IGoldDashRoleLogicServerComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer/RoleLogicServer_MOOD.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_AIEvent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_BadExpression.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_BladeBallMode.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_DataInfo.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_DefusalMode.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_DuoJin.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Fields.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_FightClose.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_HeroCard.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_HideSeek.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Item.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_ItemSkin.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Lobby.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_LockCamera.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_LookRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Manager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Misc.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Network.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Property.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Pve.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Skill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Statistics.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_TeamMode.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_UltraFight.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/ServerRolePowerSkillManager.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Misc/SORoleBaseData.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SoRoleBasePcData.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SORoleSpecialBaseData.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SORoleSandConfig.asset` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientRoleLogicAFKFeature.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientRoleLogicRoleNetCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientRoleLogicStateSyncFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicBeAttackedFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicDisconnectManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicPingManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicPowerFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicResurrectionServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicStatisticsDataManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicTrajectoryFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicUprearFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicWeakFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/ServerRoleLogicAFKFeature.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/ServerRoleLogicStateSyncFeatureManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/BattleComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/BattleLogicSystemBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/BattleMonoSystemBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/IBattleSystem.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Prefabs/` |

## 备注

BattleRole 是角色实体（MonoBehaviour），管理 44 个 BattleRoleComponent；BattleRoleLogic 是逻辑层，管理 25 个 BattleRoleLogicComponent + 2 个 IRoleLogic（Server/Client）。生命周期：CreateRole → BattleRoleLogic.init() → BattleRole.Init() → TimeEvent 驱动。注意：BattleRole 的 partial 文件使用 Role_ 前缀（如 Role_Init.cs），BattleRoleLogic 使用 RoleLogic_ 前缀
