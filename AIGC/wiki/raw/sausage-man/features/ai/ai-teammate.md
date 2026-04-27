---
name: ai-teammate
display_name: AI 队友行为系统
category: ai/teammate
version: 1.0.0
dependencies:
- ai-behavior
- role-teammate
---

# AI 队友行为系统

玩家离线/挂机时的队友 AI 代管行为：59 个 Conditional（距离/状态/物品/装备检查）+ 30 个 Action（移动/战斗/道具使用）+ PVE 专属队友行为，仅客户端实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateCancelState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateDirectionMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateFollow.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateMarkCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateMoveToCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateMoveToResurrect.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammatePickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateRangeFollow.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateStopAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateUprearRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateUseCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateUseItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateUseResurrectionMachine.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/DelayTeammateConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/IntervalTeammateConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/Pve/TeammateFindAttackMonster.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/Pve/TeammateFindSeeMonster.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/RandomDelayTeammateConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckDistance.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckIsDead.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckResurrectionMachineRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckTeamUprear.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateCheckWeaponUsable.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateFindAttackRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateFindCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateFindCoinPosition.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateFindLockRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateFindSeeRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasEquipChange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasJumpState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasMedical.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasMedicalNearby.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasObstacle.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasUseCar.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasUseItemState.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasWaitingBeResurrected.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasWeaponChange.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHasWeaponEquipNearby.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateHealthIsNotEnough.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateIsInDungeonRoom.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateIsWeaponNull.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Conditional/TeammateStateCheck.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/RoleAI/AIBehavior/TeammateBehavior.asset [队友行为树 SO 配置]` |
| `Assets/ToBundle/RoleAI/AIBehavior/TeammatePveBehavior.asset [PVE 队友行为树 SO 配置]` |

## 备注

队友 AI 与敌人 AI（ai-behavior）共享行为树引擎但有独立的 Action/Conditional 实现。仅客户端实现（无服务端镜像），因为队友行为由客户端本地驱动。依赖 role-teammate 获取代管状态（BehaviorComponent 帧驱动入口）

依赖：[[ai-behavior]] · [[role-teammate]]
