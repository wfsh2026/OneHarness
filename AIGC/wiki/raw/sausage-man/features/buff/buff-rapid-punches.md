---
name: buff-rapid-punches
display_name: BSRapidPunches - 连续拳击多阶段
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSRapidPunches - 连续拳击多阶段

1代 Buff 系统 连续拳击多阶段。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORapidPunches.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRapidPunches.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRapidPunchesServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRapidPunchesClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RapidPunches/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: startTime, loopOnceTime, endTime, attackNum.

依赖：[[buff-framework]]
