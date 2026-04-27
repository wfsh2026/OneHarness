---
name: buff-sg-fast
display_name: BSSGFast - 快速射击被动
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSSGFast - 快速射击被动

1代 Buff 系统 快速射击被动。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOSGFast.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSGFast.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSGFastServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSGFastClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/HelmetLevel3SGFast/` |

## 备注

key_fields: ShootFrequency, FireNumBetweenDelay, SingleFireDeploy, ReloadTime, AnimSpeed.

依赖：[[buff-framework]]
