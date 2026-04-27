---
name: role-state
display_name: 角色状态机系统
category: role/state
version: 1.0.0
dependencies:
- role-base
---

# 角色状态机系统

核心状态机（站/蹲/趴/游泳/飞行/载具）、状态转换表、LocalStates 本地状态

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_States.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_LocalStates.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_StateSync.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicLocalStatesComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleStateComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleStateSyncComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_State.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleStateTypes.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_ModeCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleStateCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleStateForbidFuncManager.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/RoleState.txt` |
| `Assets/ToBundle/Config/Txt/RoleStateForbidFunc.txt` |

## 备注

RoleLogic_States 是大型 partial 文件，定义所有状态转换逻辑。LocalStatesComponent 管理本地状态（站蹲趴等），BattleRoleStateComponent 管理同步状态。状态变更通过 AT Event 通知各系统。RoleStateCheck/RoleStateForbidFuncManager 提供客户端状态检查和禁用功能管理

依赖：[[role-base]]
