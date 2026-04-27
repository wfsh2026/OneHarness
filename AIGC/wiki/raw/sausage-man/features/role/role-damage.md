---
name: role-damage
display_name: 角色伤害计算系统
category: role/damage
version: 1.0.0
dependencies:
- role-base
- role-network
---

# 角色伤害计算系统

服务端权威伤害计算（DownHp 全链路）、Buff减伤、护甲计算、HP管理、伤害类型判定

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_DownHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_RecoverHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Damage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_HP.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicHPComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_DownHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_GetPower.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleKillSound.cs` |

## 备注

DownHp 是最核心的服务端计算路径（130+ 调用点）。流程：Client CmdDownHp → RoleNetServer 校验（CheckNetState/CheckTeammate等）→ ServerDownHp → GetBuffPower → 计算最终伤害 → 应用。RoleLogicServer_Damage 处理额外伤害逻辑，RoleNetServer_GetPower 处理服务端力量获取

依赖：[[role-base]] · [[role-network]]
