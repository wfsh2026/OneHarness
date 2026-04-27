---
name: buff-totem-add-nirvana-jewel
display_name: BSTotemAddNirvanaJewel - TotemAddNirvanaJewel
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemAddNirvanaJewel - TotemAddNirvanaJewel

BSTotemAddNirvanaJewel Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemAddNirvanaJewel.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemAddNirvanaJewel.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemAddNirvanaJewelServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemSpecial/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。

依赖：[[buff-framework]]
