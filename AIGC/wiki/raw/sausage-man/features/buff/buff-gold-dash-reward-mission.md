---
name: buff-gold-dash-reward-mission
display_name: BSGoldDashRewardMission - GoldDashRewardMission
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashRewardMission - GoldDashRewardMission

BSGoldDashRewardMission Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashRewardMission.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashRewardMission.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashRewardMissionClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashRewardMissionServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
