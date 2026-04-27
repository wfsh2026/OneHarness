---
name: weapon-elastic
display_name: 弹射武器（弓箭）
category: weapon/elastic
version: 1.0.0
dependencies:
- weapon-base
---

# 弹射武器（弓箭）

弹射武器(ElasticWeapon)子系统：按住蓄力→释放发射抛物线弹体。拥有独立 SO 配置(SOElasticWeaponControl)扩展蓄力参数，弹体(ElasticBulletControl)支持穿透和空气阻力

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/UI/War/Weapon/SOElasticWeaponControl.cs` | 弹射武器SO — 蓄力参数: DrawShootDamp/MaxShootRange/MinShootRange/BulletMinSpeed/BulletMaxSpeed |
| `Assets/Script/UI/War/Weapon/ElasticWeapon.cs` | 弹射武器控制器 — 按住蓄力→释放发射抛物线弹体 |
| `Assets/Script/UI/War/Weapon/ElasticWeaponAnim.cs` | 弹射武器动画 — 蓄力拉弓/释放动画 |
| `Assets/Script/UI/War/Weapon/ElasticBulletControl.cs` | 弹射弹体 — 抛物线弹道/PenetrationNum穿透/AirDamp空气阻力 |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Bow.asset` |

## 备注

弹射武器使用独立的 SOElasticWeaponControl（继承 SOWeaponControl），是唯一使用抛物线弹道的武器类型。目前仅弓箭(Bow) 1 个实例

依赖：[[weapon-base]]
