---
name: buff-add-h-p-for-limit
display_name: BSAddHPForLimit - AddHPForLimit
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddHPForLimit - AddHPForLimit

BSAddHPForLimit Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForLimit.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddHPForLimit/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 1 个文件。

依赖：[[buff-framework]]
