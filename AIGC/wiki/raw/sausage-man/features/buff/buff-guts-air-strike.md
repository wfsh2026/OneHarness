---
name: buff-guts-air-strike
display_name: BSGutsAirStrike - GutsAirStrike
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSGutsAirStrike - GutsAirStrike

BSGutsAirStrike Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGutsAirStrike.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGutsAirStrike.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGutsAirStrikeClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGutsAirStrikeServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GutsAirStrike/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
