---
name: role-equipment
display_name: 角色装备系统 - 防弹衣/头盔/背包/吉利服/狗牌
category: item/equipment
version: 1.0.0
dependencies:
- item-base
- item-loot
- weapon-base
- buff-repair-equip
---

# 角色装备系统 - 防弹衣/头盔/背包/吉利服/狗牌

1代角色防具装备系统，管理防弹衣(ArmoredVests=66)、头盔(Headgear=71)、背包(Back=61)、功能性服装/吉利服(FunctionalGarment=72)、小背心(SmallVest=95)、狗牌(DogTag)的配置加载、穿戴显示、防御计算和网络同步。SOEquipPartConfig提供通用配置（EquipHp/ProtectRatio/AddPackValue），BattleRoleEquipComponent在Host端管理装备状态事件驱动显示，EquipPart通过MeshRenderer控制防弹衣/头盔/背包/吉利服的模型渲染。GoldDash模式下有独立的防装等级和背包容量配置体系。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Config/SOEquipPartConfig.cs [通用装备配置：EquipHp/ProtectRatio/Level/AddPackValue/SOBuffList]` |
| `Assets/Script/Config/GoldDashVestBaseValueConfig.cs [GoldDash防弹衣基础值：df_ratio防御比/depreciation贬值等级]` |
| `Assets/Script/Config/GoldDashHelmetBaseValueConfig.cs [GoldDash头盔基础值配置]` |
| `Assets/Script/Config/GoldDashArmorLevelConfig.cs [GoldDash防装等级配置：全套属性表]` |
| `Assets/Script/Config/GoldDashArmorLevelConfig_Part.cs [GoldDash防装等级配置部分类]` |
| `Assets/Script/Config/GoldDashBackpackLevelConfig.cs [GoldDash背包等级配置：容量/重量]` |
| `Assets/Script/Config/GoldDashBackpackLevelConfig_Part.cs [GoldDash背包等级配置部分类]` |
| `Assets/Script/Config/GoldDashBackpackBaseValueConfig.cs [GoldDash背包基础值配置]` |
| `Assets/Script/Config/GoldDashModelEquipConfig.cs [GoldDash模型装备配置：装备外观映射]` |
| `Assets/Script/Config/BattleUiArmorOptionsConfig.cs [战斗UI防装选项配置]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleEquipComponent.cs [★核心：角色装备显示组件，事件驱动头盔/防弹衣/背包/功能性道具显示隐藏]` |
| `Assets/Script/UI/War/Weapon/EquipPart.cs [★核心：装备部件MeshRenderer渲染管理，VestsRenderers/HeadRenderers/BackRenderers/GhillieShrubsRenderers]` |
| `Assets/Script/UI/War/Weapon/BagControl.cs [背包控制：动画/挂点/特效管理]` |
| `Assets/Script/UI/PlayerControl/UIEquipHpValue.cs [装备血量显示UI：实时显示防弹衣耐久度]` |
| `Assets/Script/UI/WeaponAssembly/EquipWidget.cs [装备Widget UI组件]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyEquipInfo.cs [武器组装界面装备信息]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyEquipItem.cs [武器组装界面装备项]` |
| `Assets/Script/UI/WeaponAssembly/WeaponAssemblyUIPackTipEquip.cs [武器组装背包提示装备]` |
| `Assets/Script/UI/WeaponStore/EquipmentInfo.cs [武器商店装备详情：头盔/防弹衣/武器图标展示]` |
| `Assets/Script/UI/BullFightingWeaponStore/BullFightingEquipInfo.cs [斗牛模式装备信息]` |
| `Assets/Script/UI/ArcadeWeaponStore/ArcadeEquipInfo.cs [街机模式装备信息]` |
| `Assets/Script/UI/ArcadeWeaponStore/NormalArcadeEquipInfo.cs [普通街机装备信息]` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfPartyEquipInfo.cs [狼人派对装备信息]` |
| `Assets/Script/UI/GunFight/GunFightEquipInfoWin.cs [枪战模式装备信息窗口]` |
| `Assets/Script/UI/GunFight/GunFightEquipInfoView.cs [枪战模式装备信息视图]` |
| `Assets/Script/UI/Pack/UIPackEquit.cs [背包界面装备项]` |
| `Assets/Script/UI/Pack/UIPackEquits.cs [背包界面装备列表]` |
| `Assets/Script/UI/Pack/UIPackTipEquip.cs [背包装备提示面板]` |
| `Assets/Script/UI/Pack/UIPackTipEquipBtn.cs [背包装备提示按钮]` |
| `Assets/Script/UI/Pack/UIPackHitPart.cs [背包击中部位显示]` |
| `Assets/Script/UI/GoldDash/UIGoldDashBreakEquipEffect.cs [GoldDash装备破损特效]` |
| `Assets/Script/UI/GoldDash/UIGoldDashEscapePointConditionBtnNoEquip.cs [GoldDash逃脱点无装备条件按钮]` |
| `Assets/Script/UI/PlayerControl/Control/UIGoldDashEquip.cs [GoldDash装备HUD控制]` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/ClientGoldDashBackpack.cs [★GoldDash客户端背包逻辑：容量/等级/装备管理]` |
| `Assets/Script/UI/War/SO/Mode/GoldDash/SOGoldDashBackpackFullRatio.cs [GoldDash背包满载比例配置]` |
| `Assets/Script/UI/War/SO/Mode/GoldDash/SOGoldDashEquipDefaultSkin.cs [GoldDash装备默认皮肤配置]` |
| `Assets/Script/UI/War/Role/Dogtag/Role_DogTag.cs [狗牌显示管理]` |
| `Assets/Script/UI/War/Role/Dogtag/DogTagHpPanel.cs [狗牌血量面板UI]` |
| `Assets/Script/UI/War/Role/Dogtag/DogTagHpItem.cs [狗牌血量项UI]` |
| `Assets/Script/Data/SOEquipment.cs [ScriptableObject装备数据]` |
| `Assets/Script/Data/Base/GoldDashEquipPost.cs [GoldDash装备位置枚举]` |
| `Assets/Script/Data/Base/UnetPlayerWarEquip.cs [网络同步装备数据结构]` |
| `Assets/Script/Data/UserSettingData/Basics/EquipStateData.cs [装备状态用户设置数据]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAutoFireDogTag.cs [狗牌自动开火Buff(Host)]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAutoFireDogTag.cs [狗牌自动开火BSO配置]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAutoFireDogTagClient.cs [狗牌自动开火Buff(Client)]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAutoFireDogTagServer.cs [狗牌自动开火Buff(Server)]` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIArmor.cs [AI防装管理：Helmet=1/Armor=2枚举]` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAILogic/RoleAIExtendArmor.cs [AI扩展防装数据结构]` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/SOEquipPart.txt [装备部件通用配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashVestBaseValue.txt [GoldDash防弹衣基础值配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashHelmetBaseValue.txt [GoldDash头盔基础值配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashArmorLevel.txt [GoldDash防装等级配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashBackpackLevel.txt [GoldDash背包等级配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashBackpackBaseValue.txt [GoldDash背包基础值配置表]` |
| `Assets/ToBundle/Config/Txt/GoldDashModelEquip.txt [GoldDash模型装备映射表]` |
| `Assets/ToBundle/Config/Txt/BattleUiArmorOptions.txt [战斗UI防装选项配置表]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/Back/ [背包预制体 21个]` |
| `Assets/ToBundle/Items/Equipment/DogTag/ [狗牌预制体 5个]` |
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/ [功能性服装预制体 32个]` |
| `Assets/ToBundle/Items/Equipment/Headgear/ [头盔预制体 31个]` |
| `Assets/ToBundle/Skin/Items/Equipment/Back/ [背包皮肤 234个]` |
| `Assets/ToBundle/Skin/Items/Equipment/BagAnimator/ [背包动画 2个]` |
| `Assets/ToBundle/Skin/PickItems/Equipment/ [装备拾取皮肤 302个]` |

## 备注

B12批次。装备系统与B11武器配件系统共享UI/War/Weapon/目录但功能完全不同：B11管理武器上的瞄准镜/弹匣/枪口等，B12管理穿在角色上的防具。SOEquipPartConfig的ProtectRatio控制降伤百分比，AddPackValue控制背包增容，EquipHp控制防弹衣耐久度。GoldDash模式有独立的防装等级体系（Vest/Helmet/Backpack各有BaseValue+Level配置）。狗牌(DogTag)是特殊高级头盔装饰物(ItemID=1805890064002060288)，带BSAutoFireDogTag自动开火Buff。装备资源总计约627个文件（89预制体+236背包皮肤+302拾取皮肤）。

依赖：[[item-base]] · [[item-loot]] · [[weapon-base]] · [[buff-repair-equip]]
