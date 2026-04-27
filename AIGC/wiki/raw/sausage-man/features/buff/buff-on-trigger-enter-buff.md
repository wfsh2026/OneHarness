---
name: buff-on-trigger-enter-buff
display_name: BSOnTriggerEnterBuff - 碰撞体进入触发
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSOnTriggerEnterBuff - 碰撞体进入触发

1代 Buff 系统 碰撞体进入触发。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOOnTriggerEnterBuff.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSOnTriggerEnterBuffServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSOnTriggerEnterBuffClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/OnlyUp/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/WarItem/` |

## 备注

key_fields: BuffSign, SoundSign, TriggerInterval, BuffDuration.

依赖：[[buff-framework]]
