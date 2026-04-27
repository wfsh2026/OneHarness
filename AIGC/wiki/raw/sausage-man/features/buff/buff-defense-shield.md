---
name: buff-defense-shield
display_name: BSDefenseShield - 防御护盾含跟随/载具偏移
category: buff/defense
version: 1.0.0
dependencies:
- buff-framework
---

# BSDefenseShield - 防御护盾含跟随/载具偏移

1代 Buff 系统 防御护盾含跟随/载具偏移。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODefenseShield.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDefenseShield.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDefenseShieldServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDefenseShieldClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/DefenseShield/` |

## 备注

key_fields: lifeTime, isFollowTarget, followOffset, carOffsets[].

依赖：[[buff-framework]]
