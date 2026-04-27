---
name: buff-pve-monster
display_name: BSPveMonster - PveMonster
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveMonster - PveMonster

BSPveMonster Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveMonster.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveMonster.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveMonsterClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveMonsterServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveMonster/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
