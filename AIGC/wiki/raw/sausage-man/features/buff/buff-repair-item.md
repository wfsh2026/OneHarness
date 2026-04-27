---
name: buff-repair-item
display_name: BSRepairItem - 修复机器人
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSRepairItem - 修复机器人

1代 Buff 系统 修复机器人。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORepairItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRepairItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRepairItemServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRepairItemClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: RepairBuff:BuffSOBase, TotalDuration, IntervalTime, Radius, Height, HaloEffectSign, 多段音效.

依赖：[[buff-framework]]
