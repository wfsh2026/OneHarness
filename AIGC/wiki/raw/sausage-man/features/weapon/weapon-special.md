---
name: weapon-special
display_name: 特殊武器系统总览
category: weapon/special
version: 2.0.0
dependencies:
- weapon-base
---

# 特殊武器系统总览

4 类特殊武器子系统的总览。各类型已拆分为独立 feature：

- [[weapon-elastic]] — 弹射武器（弓箭），蓄力→抛物线弹体
- [[weapon-hidden]] — 暗器（飞刀/葫芦/水晶球/雷符），蓄力/直射+Buff 伤害
- [[weapon-zizibeng]] — 射线武器（滋滋棒/聚焦枪），两阶段射线+碎片系统
- [[weapon-fireball-launcher]] — 榴弹发射器，单发 5s CD 弹体爆炸 AOE

均复用 SOWeaponControl 但各自扩展独立字段和控制器类

## 资源文件

| 路径 | 说明 |
|------|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Harrywand.asset` | 魔杖 — 魔法武器(BulletPower:0+Buff伤害) |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/RainbowMagicWand.asset` | 彩虹魔杖 |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/TransMagicWand.asset` | 变身魔杖 |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/HandCannon.asset` | 手炮 |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/ParticleCannon.asset` | 粒子炮 |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/RailGun.asset` | 电磁炮 |

## 备注

特殊武器共 27 个 SO(6 分类)。4 个有独立控制器的子类型已拆分为独立 feature。剩余的魔法/传说武器(3 个)和特殊发射类(10 个)使用标准 WeaponControl，仅 SO 差异，保留在本 feature 中

依赖：[[weapon-base]]
