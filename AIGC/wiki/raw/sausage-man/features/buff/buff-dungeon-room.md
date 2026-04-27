---
name: buff-dungeon-room
display_name: BSDungeonRoom - DungeonRoom
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSDungeonRoom - DungeonRoom

BSDungeonRoom Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODungeonRoom.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDungeonRoom.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDungeonRoomClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDungeonRoomServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Dungeon/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
