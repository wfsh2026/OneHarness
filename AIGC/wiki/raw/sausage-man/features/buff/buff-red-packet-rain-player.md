---
name: buff-red-packet-rain-player
display_name: BSRedPacketRainPlayer - 红包雨玩家
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSRedPacketRainPlayer - 红包雨玩家

1代 Buff 系统 红包雨玩家。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORedPacketRainPlayer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRedPacketRainPlayer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRedPacketRainPlayerServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRedPacketRainPlayerClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RedPacketRain/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: ActiveActionType, ActiveActionId, CreateItemBuff, DropWaitTime等.

依赖：[[buff-framework]]
