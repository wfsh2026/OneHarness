---
name: buff-client-bomb
display_name: BSClientBomb - 爆炸伤害+击飞+视觉
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSClientBomb - 爆炸伤害+击飞+视觉

1代 Buff 系统 爆炸伤害+击飞+视觉。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClientBomb.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClientBomb.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClientBombServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClientBombClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/ClientBomb/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: BombRange, BombHurt, TeamBuffEffect[], EnemyBuffEffect[], IsStrikeFly.

依赖：[[buff-framework]]
