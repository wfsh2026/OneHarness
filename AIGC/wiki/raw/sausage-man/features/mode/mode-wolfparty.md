---
name: mode-wolfparty
display_name: 狼人派对模式（WolfParty）
category: mode/wolfparty
version: 1.0.0
dependencies:
  - mode-base
  - buff-framework
---

# 狼人派对模式（WolfParty）

狼人派对：非对称对抗模式，玩家分为村民和狼人两阵营。狼人可变身、嚎叫、使用技能；村民需生存/投票/淘汰狼人。支持多个地图变体（月亮勘测点/赛博屋顶/动物园）和 Malou 派对子模式。GameMode 枚举：LimitedtimeWolfparty=17/XdWolfparty=31/LimitedtimeWolfparty01=41/LimitedtimeWolfparty02=67。C/S/H 三端共 111 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/AutoWar/AutoWarData/WolfPartyRoleChangeAutoWar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_WolfParty.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/BSWolfTransformClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyDataLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyMain.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyMain_Malou.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyMain_Middle.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyShoppingLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfpartyHurtNumLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/Data/ClientWolfPartyData.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/ClientMaloPartyBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/ClientMaloPartyEvolutionLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/ClientMaloPartyMusicLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/ClientMaloPartySpeedAreaLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/MaloPartyMovePlatform.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/MaloPartyMovePlatformManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/MaloFeature/MaloPartySpeedArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyBattleState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyBornState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyMoonState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyOverState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyReadyState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyStateMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/State/ClientWolfPartyWinWaitState.cs` |
| `Assets/Script/GamePlay/Client/Modules/WolfParty/WolfBox.cs` |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_WolfParty_Base.cs` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_WolfParty.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleWolfPartyComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_WolfParty.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Data/WolfPartyDataStruct.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Logic/AbsWolfPartyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Logic/IWolfPartyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/MaloFeature/AbsMaloPartyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/MaloFeature/MaloPartyInstructures.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/MaloFeature/MaloPartyStatic.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/MaloFeature/MaloPartyUtils.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Mgr/AbsWolfPartyMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Mgr/AbsWolfPartyState.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Mgr/IWolfPartyState.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/Mgr/WolfPartyLogicMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/WolfParty/WolfPartyUtil.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_WolfParty.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyHurtNumData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyReLoginData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyReLoginRoleData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyResultData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyRoundSyncData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_WolfPartyWeaponAttackData.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/BSWolfTransformServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Data/WolfPartyServerData.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Data/WolfPartyServerData_Methods.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyEvolutionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyMapLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyStatisticsData.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/Logic/ServerWolfPartyWeaponLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyBoxLogger.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyDefaultFashionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyMovePlatformLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyRoleLogic_Evolution.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartyRulerLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/MaloFeature/ServerMaloPartySpeedAreaLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/ServerWolfPartyMain.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/ServerWolfPartyMain_MaloFeature.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/ServerWolfPartyMain_Middle.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyBattleState.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyBornState.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyMoonState.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyOverState.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyReadyState.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyStateMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/WolfParty/State/ServerWolfPartyWinWaitState.cs` |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_WolfParty_Base.cs` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_WolfParty.cs` |
| `Assets/Script/Config/WolfPartyWeaponConfig.cs` |
| `Assets/Script/Config/WolfPartyWeaponStoreConfig.cs` |
| `Assets/Script/Controller/WolfPartyController.cs` |
| `Assets/Script/Controller/WolfPartySelectController.cs` |
| `Assets/Script/Controller/WolfPartyWeaponStoreController.cs` |
| `Assets/Script/UI/SausageClub/WolfPartyAllHurtPrefab.cs` |
| `Assets/Script/UI/SausageClub/WolfPartyNumberPrefab.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOGamePointPos.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartyBox.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartyConfig.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartyMapSet.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartyRoleData.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartyScore.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartySoundAndParticleData.cs` |
| `Assets/Script/UI/War/SO/WolfParty/SOWolfPartySpeedAreaData.cs` |
| `Assets/Script/UI/War/StartGameWolfPartyMode.cs` |
| `Assets/Script/UI/WolfPartySelect/WolfPartySelectItem.cs` |
| `Assets/Script/UI/WolfPartySelect/WolfPartySelectWin.cs` |
| `Assets/Script/UI/WolfPartyUI/StarGroup.cs` |
| `Assets/Script/UI/WolfPartyUI/StarItem.cs` |
| `Assets/Script/UI/WolfPartyUI/WolfPartyEffect.cs` |
| `Assets/Script/UI/WolfPartyUI/WolfPartyStarEffect.cs` |
| `Assets/Script/UI/WolfPartyUI/WolfPartyWin.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/FittingCell.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/StoreItemCell.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/SubTabCell.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfFittingInfo.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfPartyEquipInfo.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfPartyStoreItemGroup.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfPartyWeaponItem.cs` |
| `Assets/Script/UI/WolfPartyWeaponStore/WolfPartyWeaponStoreWin.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/AI/WolfPartyMode_WolfParty_Level1.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/WolfParty_01_MoonLab.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/WolfParty_02_CyberRoof.asset` |
| `Assets/ToBundle/ScriptableObject/Fog/WolfParty_03_Zoo.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/WolfParty/SOGamePoint_MalouPartyBoxPoint01.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/WolfParty/SOGamePoint_WolfPartyBoxPoint01.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/WolfParty/SOGamePoint_WolfPartyBoxPoint02.asset` |
| `Assets/ToBundle/ScriptableObject/LevelData/WolfParty/SOGamePoint_WolfPartyBoxPoint03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/WolfParty_01_MoonLab.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/WolfParty_02_CyberRoof.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ArtSetting/WolfParty_03_Zoo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/WolfPartyMode_SOWolfParty01.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/WolfPartyMode_SOWolfParty02.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/GameSetting/WolfPartyMode_SOWolfParty03.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/ModeSetting/SOCSModeSetting_WolfParty.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOHypoxia/SOHypoxia_WolfParty.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyBox.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyBox_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyConfig.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyConfig_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyMapSet1.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyMapSet2.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyMapSet_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyScore.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyScore_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartySoundAndParticle.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartySoundAndParticle_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartySpeedArea_Malo.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyWolfRoleData.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyWolfRoleData_Activity.asset` |
| `Assets/ToBundle/ScriptableObject/Screen/SOWolfParty/SOWolfPartyWolfRoleData_Malo.asset` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Born_WolfMode_SOWolfParty_01_MoonLab.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Born_WolfMode_SOWolfParty_01_Storage.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Born_WolfMode_SOWolfParty_02_CyberRoof.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Born_WolfMode_SOWolfParty_02_Garage.txt` |
| `Assets/ToBundle/Config/Txt/HostNet/Bin/Born_WolfMode_SOWolfParty_03_Zoo.txt` |
| `Assets/ToBundle/Config/Txt/WolfPartyWeapon.txt` |
| `Assets/ToBundle/Config/Txt/WolfPartyWeaponStore.txt` |
| `Assets/ToBundle/Config/Txt/WolfPartyWeaponStore_Malou.txt` |
| `Assets/ToBundle/Config/Txt/WolfPartyWeapon_Malou.txt` |

## 备注

三端架构：Client (WolfPartyMain+State) / Host (AbsWolfPartyMgr+LogicMgr) / Server (State+Logic)。含 Malou 派对子模式（MaloFeature 子目录）。

依赖：[[mode-base]]、[[buff-framework]]
