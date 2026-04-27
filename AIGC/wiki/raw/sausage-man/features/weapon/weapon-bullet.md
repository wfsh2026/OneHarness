---
name: weapon-bullet
display_name: 弹药与投射物系统
category: weapon/bullet
version: 1.0.0
dependencies:
- weapon-base
---

# 弹药与投射物系统

子弹/投射物全链路：子弹发射数据同步(ProtoStruct_BulletFireData)、弹壳抛射(BulletCaseSpawner)、手雷投掷(ThrowGrenadeState)、炸弹接口(BombDataInterface)、子弹声音(ClientBulletSoundFeatureManager)、特殊子弹Buff(追踪弹/冰雹弹/气泡弹/线弹等)

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Bomb/BombDataInterface.cs [炸弹/手雷接口]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_BulletControl_BulletFireData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_BulletManager_BulletFireData.cs` |
| `Assets/Script/GamePlay/Client/Motion/BulletCaseSpawner.cs [弹壳抛射]` |
| `Assets/Script/GamePlay/Client/Motion/ThrowGrenadeState.cs [手雷投掷动画状态]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientBulletSoundFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientGunSoundModify.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatBullet.cs [子弹反作弊校验]` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleBulletInfo.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/BulletWhistle.txt [子弹呼啸声配置]` |
| `Assets/ToBundle/Config/Txt/SkinBulletAsset.txt [子弹皮肤资产映射]` |
| `Assets/ToBundle/Config/Txt/SOBulletDecal.txt [子弹弹痕贴花]` |
| `Assets/ToBundle/Config/Txt/SOBulletImpact.txt [子弹命中效果]` |
| `Assets/ToBundle/Config/Txt/SOInsertBulletDecal.txt [插入式弹痕贴花]` |
| `Assets/ToBundle/Config/Txt/HiddenWeaponDecal.txt [隐藏武器弹痕]` |
| `Assets/ToBundle/Config/Txt/GunShootEffect.txt [枪械射击特效]` |
| `Assets/ToBundle/Config/Txt/SOWeaponFireEffect.txt [武器开火特效 SO]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Bullet/ [133 files, 子弹投射物特效 — 弹道/尾迹/弹痕/命中火花]` |
| `Assets/ToBundle/Effect/WeaponFlame/ [289 files, 武器火焰特效 — 喷火器/燃烧弹]` |
| `Assets/ToBundle/Effect/WeaponHTK/ [150 files, 击杀/爆头特效]` |
| `Assets/ToBundle/Effect/WeaponShellCase/ [16 files, 弹壳抛射特效]` |
| `Assets/ToBundle/Items/Ammunition/ [20 files, 弹药模型]` |

## 备注

弹药系统覆盖从发射到命中的完整链路。特殊子弹类型（追踪弹BSPveMonsterTrackBullet/冰雹弹BSPveMonsterHailBullet/气泡弹BSPveMonsterBubblesBullet/线弹BSLineBullet）通过 Buff 系统实现（归属 buff-* 特性）。GoldDash 模式有独立弹药升级体系（GoldDashBulletLevel.txt 归属 mode-golddash）

依赖：[[weapon-base]]
