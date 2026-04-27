---
name: buff-trigger-trap
display_name: BSTriggerTrap - 主动触发机关
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSTriggerTrap - 主动触发机关

1代 Buff 系统 主动触发机关。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTriggerTrap.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTriggerTrap.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTriggerTrapClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TriggerTrap/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: triggerBuff:BuffSOBase, MyCdType:CdType, triggerCd, maxUseDistance, lifeTime, uiImageSign, cdTipsSign.

依赖：[[buff-framework]]
