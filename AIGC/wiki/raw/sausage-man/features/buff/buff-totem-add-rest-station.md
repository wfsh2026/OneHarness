---
name: buff-totem-add-rest-station
display_name: BSTotemAddRestStation - TotemAddRestStation
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemAddRestStation - TotemAddRestStation

BSTotemAddRestStation Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemAddRestStation.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemAddRestStation.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemAddRestStationServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemSpecial/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。

依赖：[[buff-framework]]
