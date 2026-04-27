---
name: buff-summon-shen-long
display_name: BSSummonShenLong - 召唤神龙多阶段
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSSummonShenLong - 召唤神龙多阶段

1代 Buff 系统 召唤神龙多阶段。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOSummonShenLong.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSummonShenLong.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSummonShenLongServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSummonShenLongClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/SummonShenLong/` |

## 备注

key_fields: LifeTime, DelayRoleShield, DelayShowShenLong, ShenLongHeight, ShenLongShieldBuff, ShenLongCloudEffect等.

依赖：[[buff-framework]]
