---
name: buff-seat-area
display_name: BSSeatArea - 座位区域
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSSeatArea - 座位区域

1代 Buff 系统 座位区域。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOSeatArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSeatArea.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSeatAreaServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSeatAreaClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/SeatArea/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: seatSize:Vector2, seatDatas:SeatData[], useDir, sitGroup.

依赖：[[buff-framework]]
