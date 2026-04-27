---
name: role-death
display_name: 角色死亡/复活系统
category: role/death
version: 1.0.0
dependencies:
- role-base
- role-damage
---

# 角色死亡/复活系统

死亡处理、复活逻辑、虚弱状态、出生点管理

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Dead.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Resurrection.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Weak.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_BornPoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_States.cs` |

## 备注

死亡/复活由服务端权威控制。Dead 处理击杀统计和淘汰，Resurrection 管理复活点和复活倒计时，Weak 处理虚弱状态（倒地求救），BornPoint 管理出生点选择

依赖：[[role-base]] · [[role-damage]]
