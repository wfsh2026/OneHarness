---
name: ai-behavior
display_name: AI 行为树引擎
category: ai/behavior
version: 1.0.0
dependencies:
- ai-base
---

# AI 行为树引擎

基于 Action/Conditional 模式的行为树决策系统：客户端 96 个 Action（射击/移动/拾取/跳跃/使用道具等）+ 92 个 Conditional（状态检查/距离判断/物品检测/安全区判定等），服务端 27 Action + 25 Conditional + 32 Feature 模式扩展

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/CheckSharedFloatAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RecordTimeAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIBaseFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIBlindageFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIBlindageLigalCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIBlocking.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIBornMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAICalBlindageFirePos.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIChangeIdleState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAICheckTargetHasPath.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIChoseBlindagePos.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIClearCommand.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAICreateAndDropItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIDashFireByTargetHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIDirectionMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIEscape.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIFar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIFindBlindage.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIFollow.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIForbidTrans.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIGlide.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIGuanyuSprint.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIJump.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAILookAt.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMark.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMarkItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMarkSafeZonePoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMeleeChargeAttack.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMoveTarget.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMoveToPickCoin.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMoveToQuanCenter.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIMoveToResurrect.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAINextWeapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIPickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIRangeFollow.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIReload.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIRookiePickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIRookieTargetPosMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAISearchSafeZonePoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAISendCommand.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIStopAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAITargetPosMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIUnEquipWeapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIUprearRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIUseItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIUseResurrectionMachine.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/DelayRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/IntervalRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RandomDelayRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICanMark.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckBullet.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckCommand.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckDistance.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckGroundHeight.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckIsDead.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckIsEquipWeapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckMarkItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckQuanCenterDistance.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckRandom.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckResurrectionMachineRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckRookieAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckRookieData.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAICheckTeamUprear.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindAttackRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindAttackRoleCanFailure.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindCoinTeammatePosition.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindLockRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindNearRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindSeeRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIFindSeeRoleCanFailure.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasEquipChange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasItemRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasJumpState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasMedical.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasMedicalNearby.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasMoveState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasObstacle.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasTeammatesWaitingBeResurrected.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasUseItemState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasWeaponChange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHasWeaponEquipNearby.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIHealthIsNotEnough.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIInBlindageCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIIsBirthIsland.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIIsInSafeZone.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIIsNotEnoughBullet.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIIsPosInSafeZone.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIIsWeaponNull.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIPartyModeFindLockRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Conditional/RoleAIStateCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/BehaviorBase/BehaviorBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/GoldDash/ServerRoleAIBack.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIAction.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIBlocking.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIClassicFire.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIDirectionMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIFar.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIFire.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIFollow.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIMoveAndStop.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIMoveToBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIMoveToPos.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIStopAction.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Action/ServerRoleAIStopAndStance.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Composite/WeightSelector.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashAreaAICheckNoMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashAreaAIFindLockRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashAreaAIFindSeeTargetByBeAttack.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashAreaAIUpdateRandomPos.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashAreaAIUpdateState.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/GoldDash/ServerGoldDashRoleAIStateCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerDelayRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerIntervalRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAICheckDistance.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIConditional.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIFindBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIFindFireRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIFindLockRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIFindSeeRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIHasObstacle.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIOpenBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIPMFindLockRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/AIBehavior/Conditional/ServerRoleAIStateCheck.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/AIBehavior/ [19 files: Mode/(1) + Other/(3) + Pve/(9) 行为树 SO 配置]` |
| `Assets/ToBundle/Config/Txt/AIBehaviorMap.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/RoleAI/AIBehavior/ [23 files, 行为树资产: EnemyAIBehavior_1~8(难度递增) + Blindage/GroupBattery/InPosition/NoJump/Run(战术变体) + RookieAI/TeamAI/Teammate/TurnBased 等]` |

## 备注

行为树采用 Action+Conditional 组合模式（非传统 BT 节点树）。客户端驱动主要行为决策，服务端做权威校验。关键 Action 包括：RoleAIFire（开火）、RoleAITargetPosMove（移动到目标）、RoleAIPickItem（拾取物品）、RoleAIFindAttackRole（寻找攻击目标）。难度通过不同 AIBehavior SO 资产控制（EnemyAIBehavior_1 最简单到 _8 最难）

依赖：[[ai-base]]
