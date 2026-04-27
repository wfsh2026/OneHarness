---
name: buff-wealth-god
display_name: BSWealthGod - 财神NPC
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSWealthGod - 财神NPC

1代 Buff 系统 财神NPC。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOWealthGod.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSWealthGod.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSWealthGodServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSWealthGodClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RedPacketRain/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: WealthGodConfig:SOWealthGodConfig, MoveSpeed, WaitMoveTime, MoveEndWaitHideTime, OffsetPoint:Vector3, offsetRadius, EffectScale:Vector3.

依赖：[[buff-framework]]
