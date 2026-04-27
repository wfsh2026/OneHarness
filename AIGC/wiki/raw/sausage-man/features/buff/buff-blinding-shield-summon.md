---
name: buff-blinding-shield-summon
display_name: BSBlindingShieldSummon - BlindingShieldSummon
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSBlindingShieldSummon - BlindingShieldSummon

BSBlindingShieldSummon Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBlindingShieldSummon.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBlindingShieldSummon.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBlindingShieldSummonClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBlindingShieldSummonServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/BlindingShieldSummon/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
