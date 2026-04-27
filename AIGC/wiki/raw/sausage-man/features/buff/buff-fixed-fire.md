---
name: buff-fixed-fire
display_name: BSFixedFire - 固定位置轰炸
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSFixedFire - 固定位置轰炸

1代 Buff 系统 固定位置轰炸。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOFixedFire.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSFixedFire.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSFixedFireServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSFixedFireClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/FixedFire/` |

## 备注

routing: GameLoop. key_fields: bulletSign, hitBuffSign, duration, interval, bulletSpeed, spread.

依赖：[[buff-framework]]
