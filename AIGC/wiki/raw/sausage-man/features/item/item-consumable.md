---
name: item-consumable
display_name: 消耗品/药品系统
category: item/consumable
version: 1.0.0
dependencies:
- buff-framework
- role-base
- item-base
- network-framework
- mode-common
---

# 消耗品/药品系统

管理 ItemType.Consumables(46) 的完整生命周期：BattleRoleConsumeItemComponent 核心使用验证(CanUseItem/DownTimeUseItem)、MedicineInfo 数据结构驱动 Buff 触发、BSOAddHPForLimit(即时回血20个SO)/BSOAddHPForTime(持续回血3个SO)/BSORoleSize(变身型4个SO) 三种效果模式、Server 端 RoleLogicServer_Item 验证链路、UIMedicine 药品面板 UI

## 代码文件

| 路径 |
|------|
| `Assets/Script/Data/ItemData.cs [物品类型常量 — Consumables=46, Med系列常量(Bandage/FirstAidKit/MedKit/Painkiller/EnergyDrink), IsMedicine(), SortConsumablesLevel1()]` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleLogic/MedicineInfo.cs [消耗品运行时数据结构 — AutoId, ItemId, ItemSign, NowValue, BuffSign[], UserTime]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleConsumeItemComponent.cs [消耗品使用核心组件 — UserItemCheckTime/CanUseItem/DownTimeUseItem/CheckBiggerUse/CancelUserItem]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Item.cs [物品使用转发层(Stub) — 维护 useItemSigns[] 映射表(索引+1=useItemState)，转发到 ConsumeItemComponent]` |
| `Assets/Script/Utils/SORoleUserMedicine.cs [药品显示配置SO — MedicineDetail(itemSign, isShow, isLeftHand, locPosition/Euler/Scale)]` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Item.cs [Server端物品使用验证 — CmdUserItem→ServerCheckCanUseItem→DownUseItem]` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUseItem.cs [物品使用统计上报]` |
| `Assets/Script/UI/PlayerControl/UIMedicine.cs [药品面板UI — Init/ChangeQMList/UseQuickMedicineDown·Up, 监听 SetCurItem/UpdateItemList]` |
| `Assets/Script/UI/PlayerControl/MedicineItem.cs [单个药品UI组件 — SetItemData/OnItemClick, 显示图标与数量]` |
| `Assets/Script/UI/PlayerControl/Control/ItemStateButtonControl.cs [消耗品快捷键绑定 — MedKit/FirstAidKit/Bandage/Painkiller/EnergyDrink→FuncCode映射]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForLimit.cs [即时回血SO — AddHp/AddMood(Basic/Percent), MinUseHp国内/海外双轨, 弱化状态判定]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddHPForTime.cs [持续回血BS — 定时触发回血效果]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForTime.cs [持续回血SO — AddHp/LifeTime/DeployTime/IsAddHpByRatio/EffectSign]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAddHp.cs [PVE模式专用回血BS]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAddHp.cs [PVE回血配置SO]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAutoRecoverHp.cs [PVE自动恢复血量BS]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAutoRecoverHp.cs [PVE自动回血配置SO]` |
| `Assets/Script/UI/War/BuffControl/HpBuffSOBase.cs [HP Buff基类 — Hp数值/HPOverBuff(损毁触发)/weaponHitRatio(武器伤害系数)]` |
| `Assets/Script/UI/War/BuffControl/IAddExtraHp.cs [额外血量接口 — IsOpenAddHp/AddHpValue/MaxAddHpValue/IsOpenTimeDown/SetDownHp()]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSRoleSize.cs [变大药剂BS — addHp额外血量/buffTime持续时间]` |
| `Assets/Script/UI/War/BuffControl/Buff/SO/BSORoleSize.cs [变大药剂SO — RoleSize/BuffTime/AddHp/AddMoveSpeedRatio/AddJumpPower/CameraRatio/ChangeRoleSizeSpeed]` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAILogic/ServerFeature/ServerRoleAIUseItem.cs [Server AI使用物品 — UseItem(RoleAIItemType), HP/Mood/Power属性恢复]` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/AIBehavior/Action/RoleAIUseItem.cs [Client AI使用物品 — BehaviorDesigner Task]` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/TeammateBehavior/Action/TeammateUseItem.cs [队友使用物品 — 构建MedicineInfo并调用TeammateUserItemCheckTime]` |
| `Assets/Script/Config/Partial/SORoleAIItemConfig.cs [AI物品使用配置SO]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_Role.cs [消耗品网络协议 — CmdUserItemState/RpcUserItemState]` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepUseMedicine.cs [新手营使用药品教程步骤]` |
| `Assets/Script/GamePlay/Client/Modules/BeginnerTutorial/TutorialUseItem.cs [初学者教程物品使用]` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoldDashMode/Logic/RookieGuide/GoldDashRookieGuideUseMed.cs [GoldDash教程使用药品]` |

## 配置文件

| 路径 |
|------|
| `Assets/Script/Utils/SORoleUserMedicine.cs [药品显示配置SO — itemSign/isShow/isLeftHand/locPosition/locEuler/locScale/useShowItemSign]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForLimit.cs [即时回血SO — addHpValueType(Basic/Percent)/AddHp/MinUseHp/GlobalMinUseHp/isMinSausage/AttackType, 共20个.asset]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddHPForTime.cs [持续回血SO — IsAddHpByRatio/AddHp/AddHpRatio/LifeTime/DeployTime, 共3个.asset]` |
| `Assets/Script/UI/War/BuffControl/Buff/SO/BSORoleSize.cs [变大药剂SO — RoleSize/BuffTime/AddHp/AddMoveSpeedRatio/AddJumpPower/CameraRatio, 共4个.asset]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/GamePlayItem/PickItems/Bandage.prefab [绷带预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/FirstAidKit.prefab [急救包预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/MedKit.prefab [医疗箱预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/MedKit_1.prefab [医疗箱变体预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/Painkiller.prefab [止痛药预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/EnergyDrink.prefab [能量饮料预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/Bigger.prefab [变大药剂预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/PanBigger.prefab [平底锅变大预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/PizzaPackage.prefab [披萨包(团队医疗箱)预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/AddHPForLimit/ [20个, 限制条件回血SO资产]` |
| `Assets/ToBundle/ScriptableObject/Buff/AddHPForTime/ [3个, 持续回血SO资产]` |
| `Assets/ToBundle/ScriptableObject/Buff/PveAddHp/ [7个, PVE回血SO资产]` |
| `Assets/ToBundle/ScriptableObject/Buff/RoleSize/ [4个, 变大药剂SO资产]` |

## 备注

消耗品使用走 MedicineInfo 结构体而非直接操作 PickItemNet。useItemSigns[] 索引+1=useItemState值，只能末尾追加不能中间插入。BSOAddHPForLimit 支持国内(MinUseHp)/海外(GlobalMinUseHp)双轨配置，通过 GlobalDefine.isGlobal 切换。绷带(Bandage)有 IsReUseItem=true 连续使用机制。变大药剂(Bigger) CapsuleCast 检查头顶空间，室内天花板阻挡。弱化状态(IsWeak)下恢复弱化值而非血量。汽油(Oilbucket)和传送胶囊(TransportItem)不属于本模块，归 B14 战场道具

依赖：[[item-base]]

依赖：[[buff-framework]] · [[role-base]] · [[item-base]] · [[network-framework]] · [[mode-common]]
