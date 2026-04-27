---
name: role-teammate
display_name: 角色队友代管系统
category: role/teammate
version: 1.0.0
dependencies:
- role-base
- role-movement
---

# 角色队友代管系统

队友行为代管总线（掉线/AI 接管时的移动/武器/开火/行动代管）

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateBehaviorComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateMoveComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateFireComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateActionComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_TeammateBehavior.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_TeammateBehavior.cs` |

## 备注

5 个 Teammate Component 构成代管总线：BehaviorComponent 是帧驱动入口，Move/Weapon/Fire/Action 分别代管移动同步、武器换弹切换、开火弹药、道具使用和救援 CD。RoleLogic_TeammateBehavior 是 Host 层 partial，RoleLogicServer_TeammateBehavior 是服务端处理

依赖：[[role-base]] · [[role-movement]]
