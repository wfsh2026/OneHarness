---
name: buff-totem-time-add-attr
display_name: BSTotemTimeAddAttr - TotemTimeAddAttr
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemTimeAddAttr - TotemTimeAddAttr

BSTotemTimeAddAttr Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemTimeAddAttr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemTimeAddAttr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTotemTimeAddAttrClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemTimeAddAttrServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemTimeAddAttr/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
