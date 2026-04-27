---
name: buff-adsorb-target
display_name: BSAdsorbTarget - 吸附锁定目标⚠️Bug
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSAdsorbTarget - 吸附锁定目标⚠️Bug

1代 Buff 系统 吸附锁定目标⚠️Bug。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAdsorbTarget.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAdsorbTarget.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAdsorbTargetServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAdsorbTargetClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: checkNotMoveTime, moveSpeed, effectOffset, moveMinTime, moveMaxTime, stopDistance, moveEffect, overEffect, quitEffect等.

依赖：[[buff-framework]]
