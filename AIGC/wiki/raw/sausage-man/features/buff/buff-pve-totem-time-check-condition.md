---
name: buff-pve-totem-time-check-condition
display_name: BSPveTotemTimeCheckCondition - PveTotemTimeCheckCondition
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveTotemTimeCheckCondition - PveTotemTimeCheckCondition

BSPveTotemTimeCheckCondition Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveTotemTimeCheckCondition.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveTotemTimeCheckCondition.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveTotemTimeCheckConditionClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveTotemTimeCheckConditionServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TotemTimeCheckCondition/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
