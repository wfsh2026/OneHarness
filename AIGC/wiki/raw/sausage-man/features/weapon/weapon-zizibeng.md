---
name: weapon-zizibeng
display_name: 射线武器（滋滋棒）
category: weapon/zizibeng
version: 1.0.0
dependencies:
- weapon-base
---

# 射线武器（滋滋棒）

滋滋棒(ZiZiBeng)射线武器子系统：两阶段射击（蓄力→持续射线），使用 Physics.RaycastNonAlloc 最多命中 10 个目标，独立的碎片(chipBullet)系统和冷却时间

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/UI/War/Weapon/ZiZiBengControl.cs` | 滋滋棒射线控制器 — 两阶段射击/RaycastNonAlloc(10)/chipBullet碎片系统/coolDownTime |
| `Assets/Script/UI/War/Weapon/ZiZiBengWeapon.cs` | 滋滋棒VFX — Shader _ChargingTime/射线特效 |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/ZiZiBeng.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FocusGun.asset` |

## 备注

射线武器共 2 个实例（滋滋棒/聚焦枪），使用持续射线而非弹道。通过 RaycastNonAlloc 实现多目标命中

依赖：[[weapon-base]]
