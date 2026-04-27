---
name: buff-red-packet-rain-point
display_name: BSRedPacketRainPoint - 红包雨掉落点
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSRedPacketRainPoint - 红包雨掉落点

1代 Buff 系统 红包雨掉落点。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORedPacketRainPoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRedPacketRainPoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRedPacketRainPointServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRedPacketRainPointClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RedPacketRain/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: ItemSign, DiffusionValue, FlyEffectName, DropInterval, ItemLifeTime, PickLimitNum等.

依赖：[[buff-framework]]
