---
name: buff-gaunlet-recover-hit
display_name: BSGaunletRecoverHit - 拳套打击恢复护盾
category: buff/movement
version: 1.0.0
dependencies:
- buff-framework
---

# BSGaunletRecoverHit - 拳套打击恢复护盾

1代 Buff 系统 拳套打击恢复护盾。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGaunletRecoverHit.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGaunletRecoverHit.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGaunletRecoverHitServer.cs` |

## 备注

key_fields: aoeRecoverShieldMax, hitRecoverShield.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
