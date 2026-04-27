---
name: weapon-hidden
display_name: 暗器武器系统
category: weapon/hidden
version: 1.0.0
dependencies:
- weapon-base
---

# 暗器武器系统

暗器(HiddenWeapon)子系统：支持蓄力射击(ChargeShoot)和直射(DirectShoot)两种模式，伤害走 Buff 系统(IsUseBulletHitBuff=true, BulletPower=0)。葫芦(Gourd)变体有独立的吸附攻击逻辑

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/UI/War/Weapon/HiddenWeaponControl.cs` | 暗器控制器(24.7KB) — hw*字段/ChargeShoot蓄力/DirectShoot直射/Gourd吸附 |
| `Assets/Script/UI/War/Weapon/HiddenWeaponDecalConfig.cs` | 暗器弹痕贴花配置 |
| `Assets/Script/GamePlay/Client/Modules/Features/Gourd/ClientGourdAdsorbFeatureManager.cs` | 葫芦吸附管理 — 目标列表/Clear()防泄漏 |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/HiddenWeaponDecal.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FlyKnife.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Gourd.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Crystalball.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Thundetalisman.asset` |

## 备注

暗器共 4 个实例（飞刀/葫芦/水晶球/雷符），通过 hw* 前缀字段扩展 SOWeaponControl。伤害走 Buff 系统而非弹道伤害。葫芦有独立的吸附逻辑(ClientGourdAdsorbFeatureManager)

依赖：[[weapon-base]]
