---
name: role-cheat
display_name: 角色反作弊系统
category: role/cheat
version: 1.0.0
dependencies:
- role-base
- role-damage
- role-network
---

# 角色反作弊系统

服务端反作弊检测（伤害校验、速度校验、位置校验、子弹校验、武器校验）

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheat.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatAction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatBullet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatCar.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatMTP.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatWeapon.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_CheatCheck.cs` |

## 备注

RoleCheat 系统包含 8 个文件，全部运行在服务端，对客户端上报的数据进行校验。核心检测：RoleCheatAction（行为合法性）、RoleCheatBullet（子弹合法性）、RoleCheatMove（移动速度/位置瞬移）、RoleCheatWeapon（武器数据）、RoleCheatCar（载具作弊）、RoleCheatMTP（MTP 反作弊集成）、RoleCheatConfig（配置）。RoleLogicServer_CheatCheck 是服务端作弊检查入口

依赖：[[role-base]] · [[role-damage]] · [[role-network]]
