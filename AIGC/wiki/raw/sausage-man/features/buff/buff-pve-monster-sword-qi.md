---
name: buff-pve-monster-sword-qi
display_name: BSPveMonsterSwordQi - PveMonsterSwordQi
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveMonsterSwordQi - PveMonsterSwordQi

BSPveMonsterSwordQi Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveMonsterSwordQi.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveMonsterSwordQi.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveMonsterSwordQiClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveMonsterSwordQiServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveMonsterSwordQi/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
