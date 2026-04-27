---
name: buff-lobby-shoot-game
display_name: BSLobbyShootGame - 大厅射击小游戏★完整系统
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSLobbyShootGame - 大厅射击小游戏★完整系统

1代 Buff 系统 大厅射击小游戏★完整系统。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOLobbyShootGame.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSLobbyShootGame.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSLobbyShootGameServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSLobbyShootGameClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/LobbyShootGame/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: GameSign, MaxRoleCnt, GameType, GameEndCond, StartWaitTime, MatchTime, EndTime, WeaponSign, StuntItems[], BornList[], TargetList[], CheckPointList[], ScorePointList[], DeadAreaConfig等~27字段.

依赖：[[buff-framework]]
