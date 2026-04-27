---
name: buff-circle-trigger-damage
display_name: BSCircleTriggerDamage - 圆形触发伤害区域
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSCircleTriggerDamage - 圆形触发伤害区域

1代 Buff 系统 圆形触发伤害区域。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCircleTriggerDamage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCircleTriggerDamageServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCircleTriggerDamageClient.cs` |

## 备注

key_fields: TriggerInterval, BuffSign.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
