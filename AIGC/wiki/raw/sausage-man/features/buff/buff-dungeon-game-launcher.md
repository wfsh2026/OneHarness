---
name: buff-dungeon-game-launcher
display_name: BSDungeonGameLauncher - DungeonGameLauncher
category: buff/dungeon
version: 1.0.0
dependencies:
- buff-framework
---

# BSDungeonGameLauncher - DungeonGameLauncher

BSDungeonGameLauncher Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODungeonGameLauncher.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDungeonGameLauncher.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDungeonGameLauncherClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDungeonGameLauncherServer.cs` |

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
