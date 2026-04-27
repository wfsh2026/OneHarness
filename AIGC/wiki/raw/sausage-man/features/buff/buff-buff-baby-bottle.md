---
name: buff-buff-baby-bottle
display_name: BSBuffBabyBottle - 婴儿奶瓶
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSBuffBabyBottle - 婴儿奶瓶

1代 Buff 系统 婴儿奶瓶。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBuffBabyBottle.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBuffBabyBottle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBuffBabyBottleServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBuffBabyBottleClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/BabyBottle/` |

## 备注

key_fields: LifeTime, MoveSpeedAddRate, AddHpValue, FontEffect, LineEffect, LineEffectOffset, AnimSpeed, SoundLoopSign, SoundOnceSign. 继承自 BuffSpeedSOBase.

依赖：[[buff-framework]]
