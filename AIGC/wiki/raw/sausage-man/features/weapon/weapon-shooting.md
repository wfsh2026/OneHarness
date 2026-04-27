---
name: weapon-shooting
display_name: 射击武器系统
category: weapon/shooting
version: 1.0.0
dependencies:
- weapon-base
- weapon-bullet
---

# 射击武器系统

射击武器表现层实现：WeaponControl 射击状态机(开火/装弹/换弹/切枪)、SOWeaponControl 175+字段配置、WeaponControlMulti 双持武器、WeaponEquipControl 装弹动画与后坐力类型、GunController/GunControllerRotate 弹簧物理后坐力模拟、BulletManager 弹道管理与伤害计算链路

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/Weapon/WeaponControl.cs [射击武器核心控制器 — 开火/装弹/切枪状态机]` |
| `Assets/Script/UI/War/Weapon/SOWeaponControl.cs [武器SO配置 — FireType(Auto/Single/Dartle), GunType(Normal/Ray/Multi), 175+字段]` |
| `Assets/Script/UI/War/Weapon/WeaponControlMulti.cs [双持武器控制器 — left/rightSlots 双侧射击]` |
| `Assets/Script/UI/War/Weapon/WeaponControlSkin.cs [武器皮肤管理 — 配件挂点/开火特效/模型显隐]` |
| `Assets/Script/UI/War/Weapon/WeaponEquipControl.cs [武器装备表现 — WeaponRecoilType/ShootAction/ReloadAction 动画驱动]` |
| `Assets/Script/UI/War/Weapon/WeaponEquip/WeaponEquipManager.cs [配件管理器 — 配件属性加成计算]` |
| `Assets/Script/UI/War/Weapon/WeaponEquip/WeaponChargeChipEffect.cs [蓄力芯片特效]` |
| `Assets/Script/UI/War/Weapon/WeaponEffectControl.cs [武器开火/待机特效管理]` |
| `Assets/Script/UI/War/Weapon/WeaponDecorationManager.cs [武器装饰品特效 — Shoot/Run/Idle权重选择]` |
| `Assets/Script/UI/War/Weapon/CtrlWeaponEffect.cs [设备分级特效控制 — LOW/MIDDLE/HIGH/Ultra]` |
| `Assets/Script/UI/War/Weapon/WeaponSpring/GunController.cs [弹簧后坐力 — 弹簧模拟(stiffness:100, damping:25)]` |
| `Assets/Script/UI/War/Weapon/WeaponSpring/GunControllerRotate.cs [后坐力旋转 — 垂直抖动/水平偏移/旋转摇晃]` |
| `Assets/Script/UI/War/Weapon/WeaponBarrelRotationControl.cs [加特林炮管旋转 — Minigun/MiniGunFirework]` |
| `Assets/Script/UI/War/Weapon/RobotWeaponBarrelControl.cs [机甲炮管旋转 — 载具武器变体]` |
| `Assets/Script/UI/War/Weapon/LaserSight.cs [激光瞄准线 — LineRenderer可配最大长度]` |
| `Assets/Script/UI/War/Weapon/BulletManager.cs [弹道管理核心 — 弹速/重力/距离衰减/网络同步]` |
| `Assets/Script/UI/War/Weapon/BulletControl.cs [弹体行为控制 — 碰撞检测/穿透/弹道物理]` |
| `Assets/Script/UI/War/Weapon/BulletTuoWei.cs [弹道拖尾特效渲染]` |
| `Assets/Script/UI/War/Weapon/BulletSkin.cs [弹体皮肤定制]` |
| `Assets/Script/UI/War/Weapon/WeaponPveDataManager.cs [PvE武器数据 — Rogue升级/武器Buff/自动射击]` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/FrontSight.txt [准星配置 — 各武器准星样式/扩散参数]` |
| `Assets/ToBundle/Config/Txt/SOWepEquipData.txt [武器配件数据 — RecoilRatio/ShootRangeRatio修正倍率]` |
| `Assets/ToBundle/Config/Txt/PickItemData.txt [物品拾取数据 — ItemSign/ItemType映射(共用，射击武器核心入口)]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Items/Weapons/*.asset [47个射击武器SO — AK12/M416/AWM/S686/Minigun等]` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/SpecialA/ [射击武器A变体]` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/SpecialB/ [射击武器B变体]` |

## 备注

射击武器是项目最核心的战斗子系统。47个射击武器SO通过SOWeaponControl定义175+字段（基础/射击/后坐力/配件/声音/附着/特殊模式等7组）。弹簧物理后坐力通过GunController实现（stiffness:100, damping:25, fireInterval:0.2s）。WeaponEquipControl定义4种装弹动画类型(Auto/OpenClose/OpenCloseMag/OpenCloseEmptyToFull)和2种后坐力类型(Light/Heavy)。双持武器通过WeaponControlMulti扩展，需同时配置left/rightSlots。BulletManager管理弹道全链路：发射→距离衰减(DistancePower)→爆头加成(HeadDiffRatio)→护甲减伤(ArmoredVestsHurtDiffRatio)

依赖：[[weapon-base]] · [[weapon-bullet]]
