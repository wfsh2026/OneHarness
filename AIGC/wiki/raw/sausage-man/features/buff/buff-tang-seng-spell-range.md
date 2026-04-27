---
name: buff-tang-seng-spell-range
display_name: BSTangSengSpellRange - TangSengSpellRange
category: buff/tangseng
version: 1.0.0
dependencies:
- buff-framework
---

# BSTangSengSpellRange - TangSengSpellRange

BSTangSengSpellRange Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTangSengSpellRange.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTangSengSpellRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTangSengSpellRangeClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTangSengSpellRangeServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TangSengGunFire/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
