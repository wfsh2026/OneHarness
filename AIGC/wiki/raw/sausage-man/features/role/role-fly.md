---
name: role-fly
display_name: 角色飞行/跳伞系统
category: role/fly
version: 1.0.0
dependencies:
- role-base
- role-state
---

# 角色飞行/跳伞系统

飞行状态、跳伞控制、BoxingFly（拳击飞行）、飞行物理

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleFlyComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSqParachuteComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_SqParachute.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_BoxingFly.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/FlymanControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Fly.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/HqParachute/` |

## 备注

飞行包含跳伞（BR 模式开局，由 SqParachute 管理）和特殊飞行（BoxingFly 拳击飞行是特定模式功能）。BattleRoleFlyComponent 管理飞行状态和物理，FlymanControl 处理客户端飞行控制表现

依赖：[[role-base]] · [[role-state]]
