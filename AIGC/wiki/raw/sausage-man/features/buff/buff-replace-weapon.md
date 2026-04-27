---
name: buff-replace-weapon
display_name: BSReplaceWeapon - 武器替换站
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSReplaceWeapon - 武器替换站

1代 Buff 系统 武器替换站。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOReplaceWeapon.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSReplaceWeapon.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSReplaceWeaponServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSReplaceWeaponClient.cs` |

## 备注

key_fields: itemSign, itemType:ItemType, lifeTime.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
