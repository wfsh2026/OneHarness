---
name: buff-dungeon-game-star
display_name: BSDungeonGameStar - DungeonGameStar
category: buff/dungeon
version: 1.0.0
dependencies:
- buff-framework
---

# BSDungeonGameStar - DungeonGameStar

BSDungeonGameStar Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODungeonGameStar.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDungeonGameStar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDungeonGameStarClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDungeonGameStarServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Dungeon/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Dungeon/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
