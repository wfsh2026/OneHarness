---
name: weapon-attachment
display_name: 武器配件系统 — 瞄准镜/弹匣/枪口/枪托/握把/芯片
category: weapon/attachment
version: 1.1.0
dependencies:
- weapon-base
- item-base
---

# 武器配件系统 — 瞄准镜/弹匣/枪口/枪托/握把/芯片

武器配件挂载、属性加成、装配UI与网络同步。支持6个配件槽位(UpperRail瞄准镜/Magazine弹匣/Muzzle枪口/Stock枪托/LowerRail握把/Chip芯片)和弹药类型。包含普通模式SOWepEquipData基础配置和GoldDash模式多等级配件升级体系(GunPartsMap/Level/DefaultParts)。WeaponAssembly提供大厅装配界面，WeaponEquip提供战场内装备管理

## 代码文件

| 路径 |
|------|
| `Assets/Script/Config/SOWepEquipDataConfig.cs [配件基础数据配置SO — 各类配件属性定义(6.6KB)]` |
| `Assets/Script/Config/Partial/SoWepEquipDataConfig.cs [配件数据配置分部类]` |
| `Assets/Script/Config/GunSightSkinConfig.cs [瞄准镜皮肤配置 — 倍率/外观映射(6KB)]` |
| `Assets/Script/Config/Partial/PartialGunSightSkinConfig.cs [瞄准镜皮肤配置分部类]` |
| `Assets/Script/Config/WeaponAssemblyConfig.cs [武器装配配置 — 模式→装配方案映射(3.5KB)]` |
| `Assets/Script/Config/GoldDashGunPartsMapConfig.cs [打金配件映射 — 枪等级→配件类型→物品ID(5.9KB)]` |
| `Assets/Script/Config/GoldDashGunPartsMapConfig_Part.cs [打金配件映射分部类]` |
| `Assets/Script/Config/GoldDashGunPartsLevelConfig.cs [打金配件等级 — 属性加成reload/recoil/range等(10.3KB)]` |
| `Assets/Script/Config/GoldDashGunPartsLevelConfig_Part.cs [打金配件等级分部类]` |
| `Assets/Script/Config/GoldDashGunDefaultPartsConfig.cs [打金默认配件 — 枪支预装配件(6KB)]` |
| `Assets/Script/Config/GoldDashGunDefaultPartsConfig_Part.cs [打金默认配件分部类]` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/WeaponEquipConfig.cs [配件属性计算 — 整合基础+打金配置最终加成(5.7KB)]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_UpperRail.cs [瞄准镜网络同步 — WeaponSign/MaxRatio/SettingRatio]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_ServerItemFeatureManager_WeaponEquipInfo.cs [武器装备信息同步 — weaponId/equipIds[]]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_RoleAIWeaponEquipInfo.cs [AI武器装备信息同步]` |
| `Assets/Script/UI/War/Weapon/WepEquip.cs [战场配件显示 — 挂载点+模型加载(4.7KB)]` |
| `Assets/Script/UI/War/Weapon/WepEquipSkin.cs [战场配件皮肤切换(1.2KB)]` |
| `Assets/Script/UI/War/Weapon/LaserSight.cs [激光瞄准器 — 射线+碰撞指示效果(4.1KB)]` |
| `Assets/Script/UI/War/Weapon/WeaponSightSeal.cs [瞄准镜封蜡 — 开镜视觉效果]` |
| `Assets/Script/UI/War/Weapon/WeaponEquipControl.cs [战场配件控制 — 装备交互逻辑(21.5KB)]` |
| `Assets/Script/UI/War/Weapon/WeaponEquip/WeaponEquipManager.cs [配件管理器 — 槽位/装卸管理(10.7KB)]` |
| `Assets/Script/UI/War/Weapon/WeaponEquip/WeaponChargeChipEffect.cs [充能芯片特效(1.1KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyWin.cs [武器装配窗口 — 主界面入口(19KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyEquipItem.cs [装配界面配件槽 — 6个槽位显示(5.1KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyEquipInfo.cs [装配界面装备信息详情(13.6KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyFittingInfo.cs [装配界面配件详细信息(5.5KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyFittingCell.cs [装配界面配件格子(2.2KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyItemGroup.cs [装配界面物品分组(4.6KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyItemCell.cs [装配界面物品格子(6.6KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyItemInfo.cs [装配界面物品信息(3.1KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyPreset.cs [装配预设方案(3.6KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyPackCapacity.cs [装配背包容量]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyPackItemSplit.cs [装配背包物品拆分]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyPackTipData.cs [装配背包提示数据]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblySubTabCell.cs [装配子标签格子(1.9KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyUIPackItemSplit.cs [装配UI背包物品拆分(3.7KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyUIPackTip.cs [装配UI背包提示(5.6KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyUIPackTipEquip.cs [装配UI背包装备提示(4KB)]` |
| `Assets/Script/UI/WeaponAssembly/WeaponSubTabCell.cs [武器子标签格子(1.7KB)]` |
| `Assets/Script/UI/WeaponAssembly/EquipWidget.cs [配件装备组件(2.7KB)]` |
| `Assets/Script/Controller/WeaponAssemblyController.cs [武器装配控制器 — 装配/拆卸/预设逻辑(30.5KB)]` |
| `Assets/Script/Controller/WeaponAssemblyController_Data.cs [武器装配控制器数据层(15.8KB)]` |
| `Assets/Script/UI/Pack/UIPackWeaponEquip.cs [背包界面武器装备显示(12.1KB)]` |
| `Assets/Script/UI/Pack/UIPackTipWeaponEquip.cs [背包界面武器装备提示(7.2KB)]` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/SOWepEquipData.txt [配件基础数据配置表 — 各类配件属性值(15.7KB)]` |
| `Assets/ToBundle/Config/Txt/GunSightSkin.txt [瞄准镜皮肤配置(1.9KB)]` |
| `Assets/ToBundle/Config/Txt/WeaponAssembly.txt [武器装配方案配置]` |
| `Assets/ToBundle/Config/Txt/GoldDashGunPartsMap.txt [打金配件映射表 — 枪等级→配件(412KB)]` |
| `Assets/ToBundle/Config/Txt/GoldDashGunPartsLevel.txt [打金配件等级属性表(25KB)]` |
| `Assets/ToBundle/Config/Txt/GoldDashGunDefaultParts.txt [打金默认配件表(19.4KB)]` |
| `Assets/ToBundle/Config/Txt/GoldDashAttachmentGridContent.txt [打金配件网格内容]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Attachments/ [101 prefabs — 瞄准镜10/弹匣23/枪口18/枪托6/握把7/芯片37]` |
| `Assets/ToBundle/Items/Ammunition/ [20 prefabs — 弹药类型模型]` |
| `Assets/ToBundle/Skin/Items/Attachments/ [154 files — 配件皮肤资源]` |
| `Assets/ToBundle/Skin/ItemsH/ Attachments/ [4 files — 配件高清皮肤]` |
| `Assets/ToBundle/Skin/PickItems/Attachments/ [69 files — 拾取态配件皮肤]` |
| `Assets/ToBundle/UGUI/Widgets/Common/GoldDashAttachmentGridWidget.prefab [打金配件网格UI]` |
| `Assets/ToBundle/UGUI/Widgets/Common/GoldDashAttachmentPreviewWidget.prefab [打金配件预览UI]` |

## 备注

配件ItemType: UpperRail=81(瞄准镜)/Magazine=82(弹匣)/Stock=83(枪托)/Muzzle=84(枪口)/LowerRail=85(握把)/Chip=805306369(芯片)/Ammunition=26(弹药)。配件属性加成两层: SOWepEquipDataConfig(基础)→GoldDashGunPartsLevelConfig(打金等级覆盖，含reload_ratio/recoil_ratio/shoot_range_ratio等7项)，最终在WeaponEquipConfig整合。6个槽位由WeaponAssemblyEquipItem定义(upperRailBox/muzzleBox/lowerRailBox/magazineBox/stockBox/chipBox)。网络同步: 瞄准镜有独立ProtoStruct_UpperRail(含倍率信息)，通用装备走ProtoStruct_WeaponEquipInfo(weaponId+equipIds[])。WeaponAssemblyController(30KB)是装配核心控制器。角色装备(Equipment/护甲/头盔/背包)不在此feature，归属B12角色装备

依赖：[[weapon-base]] · [[item-base]]
