---
name: buff-totem-add-attr
display_name: BSTotemAddAttr - TotemAddAttr
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemAddAttr - TotemAddAttr

BSTotemAddAttr Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemAddAttr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemAddAttr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTotemAddAttrClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemAddAttrServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemAddAttr/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
