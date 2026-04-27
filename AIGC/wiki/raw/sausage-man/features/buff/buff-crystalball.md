---
name: buff-crystalball
display_name: BSCrystalball - 水晶球减速
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSCrystalball - 水晶球减速

1代 Buff 系统 水晶球减速。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOCrystalball.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCrystalball.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCrystalballServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCrystalballClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Crystalball/` |

## 备注

key_fields: buffTime, stateSkillNum, reduceMoveSpeed, buffEffect. 继承自 BuffSpeedSOBase.

依赖：[[buff-framework]]
