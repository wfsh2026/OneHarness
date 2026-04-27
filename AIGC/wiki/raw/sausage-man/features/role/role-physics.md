---
name: role-physics
display_name: 角色碰撞物理系统
category: role/physics
version: 1.0.0
dependencies:
- role-base
---

# 角色碰撞物理系统

HitBox 碰撞体、CapsuleMove 胶囊体移动、ColliderCheck 碰撞检测、EdgeCheck 边缘检测

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Role/RoleHitBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleHitCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleCapsuleMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleColliderCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleEdgeCheck.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Collider.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleColliderComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleHitPartComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Physics.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicPhysicsComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicGroundComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleBodyPartCheat.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleHitPartMove.cs` |

## 备注

物理系统分 Client 和 Host 两层：Client 负责实际碰撞检测（RoleHitBox/RoleCapsuleMove/RoleColliderCheck），Host 的 Component 负责逻辑判定。RoleLogicGroundComponent 检测地面接触用于跳跃和落地。Role_Collider 是 BattleRole 层碰撞管理 partial

依赖：[[role-base]]
