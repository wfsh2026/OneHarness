---
name: buff-gold-dash-passive-skill
display_name: BSGoldDashPassiveSkill - GoldDashPassiveSkill
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashPassiveSkill - GoldDashPassiveSkill

BSGoldDashPassiveSkill Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashPassiveSkill.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashPassiveSkill.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashPassiveSkillClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashPassiveSkillServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDashPassiveSkill/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
