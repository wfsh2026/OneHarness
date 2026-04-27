---
name: buff-role-swap
display_name: BSRoleSwap - 角色位置互换
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSRoleSwap - 角色位置互换

1代 Buff 系统 角色位置互换。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORoleSwap.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRoleSwap.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRoleSwapServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRoleSwapClient.cs` |

## 备注

key_fields: SpellTime, FxRoleStartAttacker, FxRoleOverAttacker, FxRoleLineAttacker, FxRoleStartTarget, FxRoleOverTarget, FxRoleLineTarget, LineHeight, LoopAudio, ChargeAudio, SucceedAudio.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
