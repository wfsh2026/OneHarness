---
name: weapon-fireball-launcher
display_name: 榴弹发射器
category: weapon/fireball-launcher
version: 1.0.0
dependencies:
- weapon-base
---

# 榴弹发射器

榴弹发射器(FireBallLauncher)子系统：单发弹药、5 秒攻击 CD、弹体爆炸 AOE 伤害

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/UI/War/Weapon/FireBallLauncherControl.cs` | 榴弹发射器控制器 — AttackCD(5s)/单发弹药/弹体爆炸AOE |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FireBallLauncher.asset` |

## 备注

榴弹发射器是最简单的特殊武器，单发 5 秒 CD，弹体爆炸 AOE。目前仅 1 个实例

依赖：[[weapon-base]]
