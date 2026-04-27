---
name: buff-shield-soldier
display_name: BSShieldSoldier - 士兵护盾含反弹
category: buff/defense
version: 1.0.0
dependencies:
- buff-framework
---

# BSShieldSoldier - 士兵护盾含反弹

1代 Buff 系统 士兵护盾含反弹。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOShieldSoldier.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSShieldSoldier.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSShieldSoldierServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSShieldSoldierClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: LastTime, HitCount, StartBuff[].

依赖：[[buff-framework]]
