---
name: role-swim
display_name: 角色游泳系统
category: role/swim
version: 1.0.0
dependencies:
- role-base
- role-state
- role-movement
---

# 角色游泳系统

游泳状态管理、水面检测、游泳移动、浮力计算

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicSwimComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Swim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleSwim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleUnderWater.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleHypoxia.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleHypoxia_Display.cs` |

## 备注

游泳由 Host 层 Component 驱动，包含水面检测和浮力模拟。RoleLogic_Swim 管理游泳逻辑状态，RoleSwim 处理客户端游泳表现。RoleUnderWater 处理水下逻辑，RoleHypoxia/RoleHypoxia_Display 处理缺氧机制及显示

依赖：[[role-base]] · [[role-state]] · [[role-movement]]
