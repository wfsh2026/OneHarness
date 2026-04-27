---
name: autowar-system
display_name: 自动战斗/回放系统（AutoWar）
category: system/autowar
version: 1.0.0
dependencies:
  - mode-base
---

# 自动战斗/回放系统（AutoWar）

自动战斗（AI 托管）和战斗回放系统：各模式 AutoWarData、回放录制/播放。共 160 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/AutoWar/AutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ARAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddCarAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddFlyLineAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddGoldDashBoxStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddGoldDashItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddRoleAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AddRoleStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AlienAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AttackAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AttackWaveAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/AttackWaveEffectAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BlackMarketAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BombHitEffectAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BombOverAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BuffSyncInfoAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BuffValueAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BulletCheatAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BulletDecalAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CameraMoveAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarDashAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarFireAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarHpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarJumpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarJumpStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarMoveAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarPointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarRotaAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarShiftAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CarTransformAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ChangeItemHpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ClientRoleLocalStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ClientStartGameTimeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CreateAbilityGiantDaDaFightRangeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CreateGoldDashPVEAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CreateRoleAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/DanMuAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/DeadGoldDashPVEAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/DownHpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/DownHpDoorAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/EnterBombAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/EnterBombDeployAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/FireAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/FootballPosAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GameBaseAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoGoPartyGameEndAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoGoPartyGameTimeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoGoPartyLoadGameAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoGoPartyRandomSeedAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoGoPartyRulePlayerAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashAddItemForRoleAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashChangeInteractItemStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashDiscardItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashKeyRoomCreateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashKeyRoomUpdateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashMonsterAddEffectEventAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashMoveItemSiteAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashPIItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/GoldDashPickItemNetAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/HiddenWeaponAttackAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/HideSeekAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/HitFeedBackAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/HoldOnBombEffectAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ItemValueChangeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/MeleeHeavyAttackAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/MoveAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/OpenDoorAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/OutLossAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PIItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PickItemNetAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PlayActionAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PlayAnimGoldDashPVEAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PlayBoxMovePointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PlayBoxMoveRotaAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PlayBuffAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PullOutSwordAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveDownHpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveDropItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveModeDataAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveMonsterHitAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveMonsterMoveAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveRoleDataAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveRoundDataAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/PveShopAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/QuanPointSyncAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/QuanSyncAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RandomEventAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RemoveBuffAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RemoveCarAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RemoveItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RemoveRoleAIAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ResurrectionStartRewardAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RobotNetAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleAISyncPointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleAISyncStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleCmdStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleCommandAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleFireStareAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleHandInHandAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleHoldWeakRoleAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleResurrectionAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleRotaAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleSizeAddHpAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RoleSyncStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RollDirAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/RotaV3AutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SeasonItemShowStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SeasonItemTipAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ServerTimeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetCarAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetChangeWeaponPackIndexAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetGoldDashPVEPointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetGoldDashPVERotationAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetJumpFallLand.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetPlayBoxLineAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetReleaseAnim.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetUnWeaponEquipAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetUsePropAnim.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SetWeaponEquipAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/StartAirDropperAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/StartAirThrowAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/StartPointAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/StrikeFlyAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/SyncAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/TrexkingAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/TrexkingTreadAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/TurnBaseModeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UltraFightBoxAddAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UltraFightBoxAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UltraFightRoleStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UprearRoleAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UseItemStateAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UseParentForBuffAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/UseParentForItemAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/WolfPartyRoleChangeAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/WuLinHotelAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ZeusAttackAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/ZiZiBengRayAutoWar.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarHelper.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarProfiler.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWarProgram.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWar_LoadData.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWar_Play.cs` |
| `Assets/Script/GamePlay/AutoWar/AutoWar_SaveData.cs` |
| `Assets/Script/GamePlay/AutoWar/ReadWar.cs` |
| `Assets/Script/GamePlay/AutoWar/ReplayCapture/ReplayCapture.cs` |
| `Assets/Script/GamePlay/AutoWar/ReplayCapture/ReplayHelper.cs` |
| `Assets/Script/GamePlay/AutoWar/ReplayCapture/UnityMainThreadDispatcher.cs` |
| `Assets/Script/GamePlay/AutoWar/ReplayCapture/VideoSliceInfo.cs` |
| `Assets/Script/GamePlay/AutoWar/WarReportPlayTool.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Net/AutoWarCaseNetProgram.cs` |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_AutoWar_Base.cs` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_AutoWar.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_AutoWar.cs` |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_AutoWar_Base.cs` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_AutoWar.cs` |

## 备注

依赖：[[mode-base]]
