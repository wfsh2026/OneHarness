---
name: buff-bomb-area
display_name: BSBombArea - 范围爆炸含间隔
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSBombArea - 范围爆炸含间隔

1代 Buff 系统 范围爆炸含间隔。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBombArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBombArea.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBombAreaServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBombAreaClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/BombArea/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: BombDuration, BombInterval, BombArea, EndBuff.

依赖：[[buff-framework]]
