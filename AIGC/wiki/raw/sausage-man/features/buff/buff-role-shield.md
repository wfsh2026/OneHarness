---
name: buff-role-shield
display_name: BSRoleShield - 角色护盾
category: buff/defense
version: 1.0.0
dependencies:
- buff-framework
---

# BSRoleShield - 角色护盾

1代 Buff 系统 角色护盾。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORoleShield.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRoleShield.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRoleShieldServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRoleShieldClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RoleShield/` |

## 备注

key_fields: ShieldValue, LifeTime, EndBuff[].

依赖：[[buff-framework]]
