---
name: role-movement
display_name: 角色移动系统
category: role/movement
version: 1.0.0
dependencies:
- role-base
- role-state
---

# 角色移动系统

客户端移动控制、MoveSpeed 计算（热路径）、方向处理、移动同步

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Movement.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_MoveSpeed.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_Push.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Move.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Move.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/Adsorb/AdsorbBoneNode.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/Adsorb/AdsorbBoneParent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/Adsorb/AdsorbDynamicBone.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleBridgeMoveEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleControlOld.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleSlidingMoveEffect.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/DoubleRoleControllerPosition.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientAdsorbFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientGourdAdsorbFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientRoleLogicAdsorbFeature.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerAdsorbFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/ServerGourdAdsorbFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/ServerRoleLogicAdsorbFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/AddMove/AddMoveComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/AddMove/AddMoveManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/AddMove/LRRoleAddMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/AddMove/ORRoleAddMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/WarAdsorb/WarAdsorbManager.cs` |

## 备注

MoveSpeed 是性能热路径（每帧计算），包含 Buff/载具/游泳/飞行等多种速度修正。Movement 处理方向输入和移动同步。Push 处理推人物理。Role_Move 是 BattleRole 层的移动 partial

依赖：[[role-base]] · [[role-state]]
