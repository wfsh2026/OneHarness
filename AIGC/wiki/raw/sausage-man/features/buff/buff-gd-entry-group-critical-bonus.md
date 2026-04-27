---
name: buff-gd-entry-group-critical-bonus
display_name: BSGdEntryGroupCriticalBonus - GdEntryGroupCriticalBonus
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGdEntryGroupCriticalBonus - GdEntryGroupCriticalBonus

BSGdEntryGroupCriticalBonus Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGdEntryGroupCriticalBonus.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGdEntryGroupCriticalBonus.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGdEntryGroupCriticalBonusClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGdEntryGroupCriticalBonusServer.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
