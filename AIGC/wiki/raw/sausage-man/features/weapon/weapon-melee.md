---
name: weapon-melee
display_name: 近战武器实例
category: weapon/melee
version: 2.0.0
dependencies:
- weapon-melee-framework
---

# 近战武器实例

具体近战武器实现：晾衣杆(ClothesPole)、火矛(FlameSpear)、圣剑(HolySword)、长枪(Longspear)。每种武器有独立 SO 配置和专属皮肤，基于 FightClose 框架([[weapon-melee-framework]])运行

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/MeleeWeaponClothesPole.cs` | 晾衣杆 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/MeleeWeaponFlameSpear.cs` | 火矛 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/HolySword.cs` | 圣剑 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/Longspear.cs` | 长枪 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/MeleeAttackSlot.cs` | 近战攻击槽位 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/MyMeleeAttackDamageCheck.cs` | 近战伤害判定 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/ClothesPoleSkin.cs` | 晾衣杆皮肤 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/FlameSpearScript.cs` | 火矛脚本 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/SOClothesPole.cs` | 晾衣杆SO配置 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/SOFlameSpear.cs` | 火矛SO配置 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/SOHolySword.cs` | 圣剑SO配置 |
| `Assets/Script/GamePlay/Client/Modules/MeleeWeapon/SOLongspear.cs` | 长枪SO配置 |
| `Assets/Script/GamePlay/Client/Motion/MeleeAttackState.cs` | 近战攻击动画状态 |
| `Assets/Script/GamePlay/Client/Motion/MeleeFinishedState.cs` | 近战完成状态 |
| `Assets/Script/GamePlay/Client/Motion/HoldMeleeState.cs` | 持握近战状态 |
| `Assets/Script/GamePlay/Client/Motion/HoldDemonMacheteState.cs` | 恶魔砍刀持握 |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Misc/SOClothesPole.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOClothesPole_Malou.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOFlameSpear.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOHolySword.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOLongspear.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FlameSpearGold.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FlameSpearPurple.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/FlameSpearRed.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/HolySword.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/HolySwordFire.asset` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/Longspear.asset` |
| `Assets/ToBundle/Config/Txt/MeleeSkinEffect.txt` |
| `Assets/ToBundle/Config/Txt/MeleeSkinWaveEffect.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/GamePlayItem/WeaponControls/FlameSpearGold.prefab` |
| `Assets/ToBundle/GamePlayItem/WeaponControls/FlameSpearPurple.prefab` |
| `Assets/ToBundle/GamePlayItem/WeaponControls/FlameSpearRed.prefab` |
| `Assets/ToBundle/GamePlayItem/WeaponControls/HolySword.prefab` |
| `Assets/ToBundle/GamePlayItem/WeaponControls/HolySwordFire.prefab` |
| `Assets/ToBundle/GamePlayItem/WeaponControls/Longspear.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/FlameSpearRed.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/HolySword.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/HolySwordFire.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/Longspear.prefab` |
| `Assets/ToBundle/Skin/Items/Weapons/Melee/` |
| `Assets/ToBundle/Skin/Items/Weapons/Origin/` |

## 备注

4 种近战武器各有独立 SO 和专属皮肤。近战动画状态(MeleeAttackState 等)在 Motion 目录中，属于 role-motion 的扩展但逻辑上归属近战系统。框架代码(FightClose)已分离到 [[weapon-melee-framework]]
