---
name: role-animation
display_name: 角色动画系统
category: role/animation
version: 1.0.0
dependencies:
- role-base
---

# 角色动画系统

Playable Animation 驱动、Animator 控制、IK、动画事件触发、骨骼缓存

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Animation.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleAnimationComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleControlBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/IKCtrl.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleAnimatorControlPool.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/RoleAnimation.txt` |
| `Assets/ToBundle/Config/Txt/RoleAnimationEvent.txt` |
| `Assets/ToBundle/Config/Txt/RoleClipAsset.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/AnimGraphData/` |

## 备注

BattleRoleAnimationComponent 管理动画状态机，RoleControl 是客户端 Animator 控制器（IK/骨骼缓存/动画事件）。RoleControlBase 是基类，IKCtrl 处理 IK 控制。RoleAnimatorControlPool 管理 Animator 控制器对象池

依赖：[[role-base]]
