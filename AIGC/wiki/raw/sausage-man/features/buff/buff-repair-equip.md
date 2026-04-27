---
name: buff-repair-equip
display_name: BSRepairEquip - 修复装备
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSRepairEquip - 修复装备

1代 Buff 系统 修复装备。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORepairEquip.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRepairEquip.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRepairEquipServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRepairEquipClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: EquipTypeList:List<GoldDashEquipType>, RepairValue, EffectDuration, BodyPartData, Offset, AIOffset.

依赖：[[buff-framework]]
