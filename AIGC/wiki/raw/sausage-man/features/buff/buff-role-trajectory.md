---
name: buff-role-trajectory
display_name: BSRoleTrajectory - 角色轨迹追踪
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSRoleTrajectory - 角色轨迹追踪

1代 Buff 系统 角色轨迹追踪。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORoleTrajectory.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRoleTrajectory.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRoleTrajectoryServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRoleTrajectoryClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: CheckTime, CheckRatio, CheckHp, CheckRoleDistance, IsCheckTeam, prefabName, ClientUdpateRatio, showLineRenderOffset等. 继承自 BSRoleStateChange.

依赖：[[buff-framework]]
