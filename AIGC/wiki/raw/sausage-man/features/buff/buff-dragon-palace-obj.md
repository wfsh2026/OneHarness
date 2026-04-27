---
name: buff-dragon-palace-obj
display_name: BSDragonPalaceObj - DragonPalaceObj
category: buff/dungeon
version: 1.0.0
dependencies:
- buff-framework
---

# BSDragonPalaceObj - DragonPalaceObj

BSDragonPalaceObj Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODragonPalaceObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDragonPalaceObj.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDragonPalaceObjClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDragonPalaceObjServer.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Dungeon/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
