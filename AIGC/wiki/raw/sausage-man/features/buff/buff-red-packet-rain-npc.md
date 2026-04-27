---
name: buff-red-packet-rain-npc
display_name: BSRedPacketRainNpc - 红包雨NPC
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSRedPacketRainNpc - 红包雨NPC

1代 Buff 系统 红包雨NPC。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORedPacketRainNpc.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRedPacketRainNpc.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRedPacketRainNpcServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRedPacketRainNpcClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/RedPacketRain/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: MatchMode, MoveData[], MoveSpeed, CreateItemBuff, OnceDropTime, OnceDropNum, DropItemRound, MapIconSign等.

依赖：[[buff-framework]]
