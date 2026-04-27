---
name: buff-totem-when-attr-then-attr
display_name: BSTotemWhenAttrThenAttr - TotemWhenAttrThenAttr
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemWhenAttrThenAttr - TotemWhenAttrThenAttr

BSTotemWhenAttrThenAttr Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemWhenAttrThenAttr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemWhenAttrThenAttr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTotemWhenAttrThenAttrClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemWhenAttrThenAttrServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemWhenAttrThenAttr/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
