---
name: buff-shield-pawn
display_name: BSShieldPawn - 盾兵护盾
category: buff/defense
version: 1.0.0
dependencies:
- buff-framework
---

# BSShieldPawn - 盾兵护盾

1代 Buff 系统 盾兵护盾。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOShieldPawn.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSShieldPawn.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSShieldPawnServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSShieldPawnClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/DownHpObj/DownHpObj_ShieldPawn.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/LineMove/LineMove_ShieldPawn.asset` |

## 备注

key_fields: FollowBuffData[], serverColliderUrl. 继承自 BSDownHpObj.

依赖：[[buff-framework]]
