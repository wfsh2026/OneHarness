---
name: buff-captain-card-recovery
display_name: BSCaptainCardRecovery - 队长卡恢复
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSCaptainCardRecovery - 队长卡恢复

1代 Buff 系统 队长卡恢复。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOCaptainCardRecovery.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCaptainCardRecovery.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCaptainCardRecoveryServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCaptainCardRecoveryClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/CaptainCardRecovery/` |

## 备注

key_fields: LifeTime, JudgeTime, RecoveryHp, HpEffectSign, SoundSign.

依赖：[[buff-framework]]
