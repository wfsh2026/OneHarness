---
name: buff-add-hp-for-time
display_name: BSAddHPForTime - 持续回血/掉血DoT/HoT
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddHPForTime - 持续回血/掉血DoT/HoT

1代 Buff 系统 持续回血/掉血DoT/HoT。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForTime.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddHPForTime.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddHPForTimeServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddHPForTimeClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddHPForTime/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: AddHp, AddHpRatio, LifeTime, DeployTime.

依赖：[[buff-framework]]
