---
name: buff-blast-bomb
display_name: BSBlastBomb - 爆炸触发
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSBlastBomb - 爆炸触发

1代 Buff 系统 爆炸触发。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBlastBomb.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBlastBomb.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBlastBombServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBlastBombClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/BlastBomb/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: BlastBombEffect, bombTime, refreshTime.

依赖：[[buff-framework]]
