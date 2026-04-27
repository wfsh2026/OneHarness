---
name: role-render
display_name: 角色渲染显示系统
category: role/render
version: 1.0.0
dependencies:
- role-base
---

# 角色渲染显示系统

模型显示/隐藏控制、材质控制、可见性管理、特效显示

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleShowComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSkinComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_RoleDisplay.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleSkinEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleEffectPart.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/ObjSizeForLocalRole.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Materials/` |
| `Assets/ToBundle/Effect/RoleAnimation/` |

## 备注

BattleRoleShowComponent 控制角色可见性切换，BattleRoleSkinComponent 管理皮肤渲染器列表和材质。RoleLogicClient_RoleDisplay 驱动客户端模型加载。RoleSkinEffect/RoleEffect/RoleEffectPart 管理角色特效显示

依赖：[[role-base]]
