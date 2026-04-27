---
name: buff-totem-combination
display_name: BSTotemCombination - TotemCombination
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemCombination - TotemCombination

BSTotemCombination Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemCombination.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemCombination.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTotemCombinationClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemCombinationServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemCombination/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
