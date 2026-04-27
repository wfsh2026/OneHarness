---
name: buff-gold-dash-a-i-fight-status-effect
display_name: BSGoldDashAIFightStatusEffect - GoldDashAIFightStatusEffect
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashAIFightStatusEffect - GoldDashAIFightStatusEffect

BSGoldDashAIFightStatusEffect Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashAIFightStatusEffect.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashAIFightStatusEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashAIFightStatusEffectClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashAIFightStatusEffectServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDashFightStatusEffect/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
