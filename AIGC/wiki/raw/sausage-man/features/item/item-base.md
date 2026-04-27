---
name: item-base
display_name: 道具核心框架
category: item/base
version: 1.0.0
dependencies:
- role-base
---

# 道具核心框架

道具系统三端核心框架：Host 层 ItemManager/PickItemNet 管理地面道具生成与网络同步，BattleRole*ItemComponent 处理角色拾取/消耗/检测；Client 层 PickItem/ClientItemFeatureManager 处理表现与UI；Server 层 ServerItemFeatureManager/ServerGoodsBox 处理业务逻辑与宝箱。含 SeasonItem 赛季道具和 ShieldTheme 主题道具子系统

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Item/ItemManager.cs [道具生成/销毁管理器]` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNet.cs [网络道具同步]` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNetBase.cs [抽象拾取基类]` |
| `Assets/Script/GamePlay/Host/Modules/Item/AbsPickItemNet.cs [抽象网络拾取]` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNet_Mode.cs [模式专属网络]` |
| `Assets/Script/GamePlay/Host/Modules/Item/BattleRoyaleItemManager.cs [吃鸡道具管理]` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldItem.cs [金币道具]` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldItemServerManager.cs [金币生成管理]` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/ItemConfigManager.cs [道具配置管理]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRolePickItemComponent.cs [角色拾取组件]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleConsumeItemComponent.cs [角色消耗组件]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCheckSceneItemComponent.cs [道具检测组件]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Item.cs [角色道具扩展]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_Item.cs [道具网络协议]` |
| `Assets/Script/GamePlay/Client/Modules/Item/PickItem.cs [客户端拾取道具]` |
| `Assets/Script/GamePlay/Client/Modules/Item/PickItemNetClient.cs [客户端网络]` |
| `Assets/Script/GamePlay/Client/Modules/Item/ClientItemFeatureManager.cs [客户端道具管理]` |
| `Assets/Script/GamePlay/Client/Modules/Item/IClientItemManager.cs [客户端道具接口]` |
| `Assets/Script/GamePlay/Client/Modules/Item/SceneDeadItemBox.cs [尸体掉落箱]` |
| `Assets/Script/GamePlay/Client/Modules/Item/ShieldThemeItemManager.cs [护盾主题道具]` |
| `Assets/Script/GamePlay/Client/Modules/Item/ShieldThemeSceneItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/ShieldThemeSignManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/PropsBox/PropsBoxParent.cs [宝箱基类]` |
| `Assets/Script/GamePlay/Client/Modules/PropsBox/RefreshSkillProp.cs [技能道具刷新]` |
| `Assets/Script/GamePlay/Server/Modules/Item/PickItemNetServer.cs [服务端网络]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerItemFeatureManager.cs [服务端道具管理]` |
| `Assets/Script/GamePlay/Server/Modules/Item/IServerItemManager.cs [服务端道具接口]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerGoodsBoxFeatureManager.cs [宝箱管理器]` |
| `Assets/Script/GamePlay/Host/Modules/SeasonItem/SeasonItemBase.cs [赛季道具-Host]` |
| `Assets/Script/GamePlay/Client/Modules/SeasonItem/SeasonItemClient.cs [赛季道具-Client]` |
| `Assets/Script/GamePlay/Server/Modules/SeasonItem/SeasonItemServer.cs [赛季道具-Server]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientSeasonItemFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerSeasonItemFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Item.cs` |
| `Assets/Script/GamePlay/Client/Modules/BeginnerTutorial/TutorialPickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/BeginnerTutorial/TutorialUseItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/ClientItemFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/ClientSplitItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/ClientSplitItem_PickItemData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/IClientItemManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/PickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/PickItemNetClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/SceneDeadItemBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/ShieldThemeItemManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/SeasonItem/SeasonItemClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/AbsPickItemNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/BattleRoyaleItemManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldItemServerManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/ItemConfigManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/WeaponConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNetBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/PickItemNet_Mode.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/SORandomEventMoreCreateItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/SORandomEventMoreSeasonItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/SeasonItem/SeasonItemBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatGoldItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatUseItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/IServerItemManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/PickItemNetServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerGoodsBoxFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerItemFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_AirThrow.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_ItemData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_PickItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_PirateShip.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_RoleData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_SceneDeadItemBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItem_GridData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportPlayerItemLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportDecItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportGetItemFromBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportOverCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportTotalCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUseItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/SeasonItem/SeasonItemServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/PropsBox/PropsBoxParent.cs` |
| `Assets/Script/GamePlay/Client/Modules/PropsBox/RefreshSkillProp.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/ItemQuality.txt [道具品质等级]` |
| `Assets/ToBundle/Config/Txt/ItemSize.txt [道具尺寸]` |
| `Assets/ToBundle/Config/Txt/ItemTabBase.txt [道具UI分类标签]` |
| `Assets/ToBundle/Config/Txt/ItemTableBase.txt [道具主表]` |
| `Assets/ToBundle/Config/Txt/ItemAsset.txt [道具视觉资产映射]` |
| `Assets/ToBundle/Config/Txt/ItemRoulette.txt [道具随机/轮盘]` |
| `Assets/ToBundle/Config/Txt/PickItemData.txt [拾取道具定义]` |
| `Assets/ToBundle/Config/Txt/PickItemAsset.txt [拾取道具视觉]` |
| `Assets/ToBundle/Config/Txt/PickUpItemType.txt [拾取类别]` |
| `Assets/ToBundle/Config/Txt/OneClickItemType.txt [一键拾取类型]` |
| `Assets/ToBundle/Config/Txt/OneClientItemTypeSetContent.txt [一键拾取集合]` |
| `Assets/ToBundle/Config/Txt/BattleUiArmorOptions.txt [战斗UI护甲选项]` |
| `Assets/ToBundle/Config/Txt/ShieldThemeItem.txt [护盾主题道具]` |
| `Assets/ToBundle/Config/Txt/TaskItemData.txt [任务道具数据]` |
| `Assets/ToBundle/Config/Txt/SORoleAIItem.txt [AI道具行为]` |
| `Assets/ToBundle/ScriptableObject/Items/ [1 file (Stunt SO), 道具主定义SO — 注：Weapons/(238)归属weapon-base]` |
| `Assets/ToBundle/ScriptableObject/Bag/ [225 files, 背包/容器SO配置]` |
| `Assets/ToBundle/ScriptableObject/Equipments/ [1 file, 装备SO]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/BirthIsland/ [16 files, 出生岛道具模型]` |
| `Assets/ToBundle/Items/Stunt/ [82 files, 特技道具模型]` |
| `Assets/ToBundle/Items/ItemLod/ [27 files, 道具LOD变体]` |
| `Assets/ToBundle/Items/PrankItem/ [31 files, 恶作剧道具模型]` |

## 备注

道具系统是战斗循环的基础设施之一。所有可拾取物继承自 PickItemNet 基类。Proto_Item.cs 外还有 17 个 ProtoStruct 定义各类道具同步数据结构(WarDropItem/GoldItem/KnockoutItem/WolfBoxItem 等)。武器配置(WeaponConfig/WeaponEquipConfig)在 Item/ItemConfig/ 目录下但逻辑归属 weapon-base。模式专属道具模型(MouseHoleMode/GoGoPartyMode/PveItem/UGCMode 等)归属各模式 feature

依赖：[[role-base]]
