---
name: role-animator
display_name: 角色 AnimatorControl 框架
category: role/animator
version: 1.0.0
dependencies:
- role-base
- role-animation
---

# 角色 AnimatorControl 框架

AnimatorControl 核心控制器、Decorator 模式扩展、BaseCheck/AimCheck/RunAddCheck 检测链、CommonAnimatorControl 通用控制、NPC 动画控制、动画枚举定义

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Motion/AnimatorControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimatorControlDecorator.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimatorControlBaseCheck.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimatorControlAimCheck.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimatorControlRunAddCheck.cs` |
| `Assets/Script/GamePlay/Client/Motion/CommonAnimatorControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/NpcAnimatorControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimatorEnum.cs` |
| `Assets/Script/GamePlay/Client/Motion/IRoleLogicAuxiliaryAiming.cs` |
| `Assets/Script/GamePlay/Client/Motion/IRoleLogicClientAuxiliaryAiming.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/RoleControllerAsset.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/` |

## 备注

AnimatorControl 是角色动画状态机的核心驱动（Decorator 模式包装 Animator），通过 BaseCheck/AimCheck/RunAddCheck 链式判定当前动画状态。CommonAnimatorControl 供非战斗角色使用，NpcAnimatorControl 供 NPC 使用。辅助瞄准接口 IRoleLogicAuxiliaryAiming 提供瞄准偏移计算

依赖：[[role-base]] · [[role-animation]]
