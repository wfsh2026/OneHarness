---
name: mode-sportsparty
display_name: 运动派对模式（SportsParty）
category: mode/sportsparty
version: 1.0.0
dependencies:
  - mode-base
  - buff-framework
---

# 运动派对模式（SportsParty）

运动派对：多回合竞技模式，支持商店购买系统和金币经济。采用 ExtendGameWorldFeature 架构。包含多地图（彩虹岛/超新星/战斗岛）、专属 Buff（SportsPartyChest/SportsPartyCoin）。C/S/H 三端 + UI 共 68 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Controller/SportsPartyController.cs` |
| `Assets/Script/Funny/AdvancedLevelDesign/SportsPartyBornAreaEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSportsPartyChestClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSportsPartyCoinClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyLodMapLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyMainLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyRoundLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartyShoppingLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/SportsParty/ClientSportsPartySyncLogic.cs` |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_SportsParty_Base.cs` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_SportsParty.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/AbsSportsPartyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/AbsSportsPartyMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/ISportsPartyData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/ISportsPartyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/ISportsPartyMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsParty.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyBornArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyCoinData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyDataMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyFightData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyGameOverData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyLogicMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyMainData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyMessageData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyRoleData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyRoundData.cs` |
| `Assets/Script/GamePlay/Host/Modules/SportsParty/SportsPartyStatisticsData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_SportsParty.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyBuyStruct.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyCoinMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyCoinSyncMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyGameOverData_ReportData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyGameOverData_RoundData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyGameOverSyncMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyLookLoginMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyReLoginMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyRoundSyncMessageData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyRoundSyncMessageData_TeamWinPoint.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartySellStruct.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSportsPartyChestServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSportsPartyCoinServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyCheckCheatLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyCoinLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyFightLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyGameOverLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyMainLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyMapLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyNet.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyReLoginLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyRoundLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyShoppingLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyTimeLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyWaitLogic.cs` |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_SportsParty_Base.cs` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_SportsParty.cs` |
| `Assets/Script/UI/MapInfo/SportsPartyMapInfo.cs` |
| `Assets/Script/UI/SportsParty/SportsPartyCoinTips.cs` |
| `Assets/Script/UI/SportsParty/SportsPartyWin.cs` |
| `Assets/Script/UI/War/BuffControl/Buff/SO/BSOSportsPartyChest.cs` |
| `Assets/Script/UI/War/BuffControl/Buff/SO/BSOSportsPartyCoin.cs` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSSportsPartyChest.cs` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSSportsPartyCoin.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/AI/SportsPartyMode_CombatIsland_Level1.asset` |
| `Assets/ToBundle/ScriptableObject/AI/SportsPartyMode_RainbowIsland_Level1.asset` |
| `Assets/ToBundle/ScriptableObject/AI/SportsPartyMode_SupernovaStar_Level1.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/CreateBuff/CreateBuff_SportsPartyChest.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/CreateBuff/CreateBuff_SportsPartyCoin.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/GoodsBox/BSOGoodsBox_SportsParty.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/SportsParty/PB_SportsPartyChest.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/SportsParty/PB_SportsPartyCoin.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/CatIsland/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/CombatIsland/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/CombatRetro/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/RainbowIsland/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/StarfishIsland/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/PlayBoxBuffGroup/SupernovaStar/SportsPartyMode/PlayBoxBuffGroup.asset` |
| `Assets/ToBundle/ScriptableObject/Mode/SportsParty/ServerSportsPartyConfig.asset` |
| `Assets/ToBundle/ScriptableObject/SOCreateObjData/RainbowIsland_SportsPartyCreateData.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/DropItem/SOMonsterItem_SportsParty.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/BaseGameCreateItem.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_1_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_1_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_1_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_1_4.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_2_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_2_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_3_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_3_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_3_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_4_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_4_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_4_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_5_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_5_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SOCombatIsland/SportsPartyMode_SOCombatIsland_5_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/BaseGameCreateItem.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_1_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_1_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_1_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_1_4.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_2_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_2_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_3_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_3_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_3_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_4_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_4_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_4_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_5_1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_5_2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameCreateItem/SportsPartyMode_SORainbowIsland/SportsPartyMode_SORainbowIsland_5_3.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/Custom_SportsPartyMode_SOCombatIsland.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/Custom_SportsPartyMode_SORainbowIsland.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/Custom_SportsPartyMode_SOSupernovaStar.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/SportsPartyMode_SOCombatIsland.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/SportsPartyMode_SORainbowIsland.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/SportsPartyMode_SOSupernovaStar.asset` |
| `Assets/ToBundle/Effect/Buff/Common/SportsPartyChest.prefab` |
| `Assets/ToBundle/Effect/Buff/Common/SportsPartyCoin.prefab` |
| `Assets/ToBundle/Effect/UI/War/SportsParty/UISportsPartyChestBox.prefab` |
| `Assets/ToBundle/Effect/UI/War/SportsParty/UISportsPartyCoinBox.prefab` |
| `Assets/ToBundle/UGUI/Windows/SportsParty.prefab` |

## 备注

三端架构：Client (SportsPartyMgr+Logic) / Host (AbsSportsPartyMgr+DataMgr+LogicMgr, ExtendGameWorldFeature) / Server (SportsPartyMgr+Logic)。含专属 Buff：BSSportsPartyChest、BSSportsPartyCoin。

依赖：[[mode-base]]、[[buff-framework]]
