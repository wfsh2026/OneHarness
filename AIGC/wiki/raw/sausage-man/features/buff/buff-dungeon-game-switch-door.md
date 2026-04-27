---
name: buff-dungeon-game-switch-door
display_name: BSDungeonGameSwitchDoor - DungeonGameSwitchDoor
category: buff/dungeon
version: 1.0.0
dependencies:
- buff-framework
---

# BSDungeonGameSwitchDoor - DungeonGameSwitchDoor

BSDungeonGameSwitchDoor Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODungeonGameSwitchDoor.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDungeonGameSwitchDoor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDungeonGameSwitchDoorClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDungeonGameSwitchDoorServer.cs` |

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
