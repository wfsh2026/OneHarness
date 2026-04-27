---
name: buff-add-power
display_name: BSAddPower - AddPower
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddPower - AddPower

BSAddPower Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddPower.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddPower/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 1 个文件。

依赖：[[buff-framework]]
