---
name: buff-dungeon-game-box
display_name: BSDungeonGameBox - DungeonGameBox
category: buff/dungeon
version: 1.0.0
dependencies:
- buff-framework
---

# BSDungeonGameBox - DungeonGameBox

BSDungeonGameBox Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODungeonGameBox.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDungeonGameBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDungeonGameBoxClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDungeonGameBoxServer.cs` |

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
