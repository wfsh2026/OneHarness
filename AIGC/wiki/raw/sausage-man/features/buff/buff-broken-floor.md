---
name: buff-broken-floor
display_name: BSBrokenFloor - 地板破碎
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSBrokenFloor - 地板破碎

1代 Buff 系统 地板破碎。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBrokenFloor.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBrokenFloor.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBrokenFloorServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBrokenFloorClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/OnlyUp/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: BrokenDelayTime, ReviveTime, TriggerEffectSign.

依赖：[[buff-framework]]
