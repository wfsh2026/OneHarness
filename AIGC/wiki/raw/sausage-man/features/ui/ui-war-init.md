---
name: ui-war-init
display_name: 战场初始化
category: ui
version: 1.0.0
dependencies:
  - ui-framework
---

# 战场初始化

战场游戏启动与初始化。StartGame系列(11种模式变体)管理网络/镜头/角色初始化，SafeAreaManager管理毒圈收缩，ButtleMap/ButtleLayer管理场景层级，弹幕系统(BarrageCell)处理聊天消息。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/AnimatorCollection.cs` |
| `Assets/Script/UI/War/AsyncPlayParticleEffect.cs` |
| `Assets/Script/UI/War/AsyncPlayScenePart.cs` |
| `Assets/Script/UI/War/BakeMeshRendererDatas.cs` |
| `Assets/Script/UI/War/BakeSceneMgr.cs` |
| `Assets/Script/UI/War/BarrageCell.cs` |
| `Assets/Script/UI/War/BirthIslandManager.cs` |
| `Assets/Script/UI/War/BSMagicLevelStarMono.cs` |
| `Assets/Script/UI/War/ButtleLayer.cs` |
| `Assets/Script/UI/War/ButtleMap.cs` |
| `Assets/Script/UI/War/CalcRoundCreateWeapon.cs` |
| `Assets/Script/UI/War/CameraHit.cs` |
| `Assets/Script/UI/War/CannonColliderCheck.cs` |
| `Assets/Script/UI/War/ChangeMaterialTiling.cs` |
| `Assets/Script/UI/War/ChestMonster.cs` |
| `Assets/Script/UI/War/Clownskill2AreaComponent.cs` |
| `Assets/Script/UI/War/DeC4.cs` |
| `Assets/Script/UI/War/EffectLevelComponent.cs` |
| `Assets/Script/UI/War/EffectLevelManager.cs` |
| `Assets/Script/UI/War/ExpressCannon.cs` |
| `Assets/Script/UI/War/FlyLine.cs` |
| `Assets/Script/UI/War/FlyLineControl.cs` |
| `Assets/Script/UI/War/FlyPlaneNet.cs` |
| `Assets/Script/UI/War/FlyPlaneNetMirror.cs` |
| `Assets/Script/UI/War/GameQuan.cs` |
| `Assets/Script/UI/War/GameQuanMirror.cs` |
| `Assets/Script/UI/War/GoldDashCGMask.cs` |
| `Assets/Script/UI/War/GoldDashCGMaskController.cs` |
| `Assets/Script/UI/War/GoodsBox.cs` |
| `Assets/Script/UI/War/GunBayonetControl.cs` |
| `Assets/Script/UI/War/ItemSpawnPoint.cs` |
| `Assets/Script/UI/War/JumpPropsHpState.cs` |
| `Assets/Script/UI/War/KMeans.cs` |
| `Assets/Script/UI/War/LayerComponent.cs` |
| `Assets/Script/UI/War/MagicTreasure.cs` |
| `Assets/Script/UI/War/NoobFishBoothMono.cs` |
| `Assets/Script/UI/War/PveSubSceneMgr.cs` |
| `Assets/Script/UI/War/QuanBox.cs` |
| `Assets/Script/UI/War/RecvCastleCollider.cs` |
| `Assets/Script/UI/War/RoundCreateAlienWarshipCreateCircle.cs` |
| `Assets/Script/UI/War/RoundCreateAlienWarshipLandingPoint.cs` |
| `Assets/Script/UI/War/RoundCreateCar.cs` |
| `Assets/Script/UI/War/RoundCreateDragon.cs` |
| `Assets/Script/UI/War/RoundCreateRobot.cs` |
| `Assets/Script/UI/War/RoundCreateShip.cs` |
| `Assets/Script/UI/War/RoundCreateUFO.cs` |
| `Assets/Script/UI/War/RoundCreateVehicle.cs` |
| `Assets/Script/UI/War/SafeAreaManager.cs` |
| `Assets/Script/UI/War/ScenceRenderFeatureMgr.cs` |
| `Assets/Script/UI/War/SceneShadowMgr.cs` |
| `Assets/Script/UI/War/SendBarrageWidget.cs` |
| `Assets/Script/UI/War/ShipCreateWeapon.cs` |
| `Assets/Script/UI/War/SOCameraUserData.cs` |
| `Assets/Script/UI/War/SOGoldDashUIHitFeedback.cs` |
| `Assets/Script/UI/War/Startgame_Buff.cs` |
| `Assets/Script/UI/War/StartGame_Lobby.cs` |
| `Assets/Script/UI/War/Startgame_Scene.cs` |
| `Assets/Script/UI/War/StartGame.cs` |
| `Assets/Script/UI/War/StartGameBulletControl.cs` |
| `Assets/Script/UI/War/StartGameBulletTrailControl.cs` |
| `Assets/Script/UI/War/StartGameDefusalMode.cs` |
| `Assets/Script/UI/War/StartGameEnergyBattle.cs` |
| `Assets/Script/UI/War/StartGameGunFightMode.cs` |
| `Assets/Script/UI/War/StartGameHideSeek.cs` |
| `Assets/Script/UI/War/StartGameNet.cs` |
| `Assets/Script/UI/War/StartGameNetMirror.cs` |
| `Assets/Script/UI/War/StartGamePartyMode.cs` |
| `Assets/Script/UI/War/StartGameScuffleMode.cs` |
| `Assets/Script/UI/War/StartGameSimulatorCheck.cs` |
| `Assets/Script/UI/War/StartGameTeam.cs` |
| `Assets/Script/UI/War/StartGameWolfPartyMode.cs` |
| `Assets/Script/UI/War/StartMap.cs` |
| `Assets/Script/UI/War/SyncFlyJumpEff.cs` |
| `Assets/Script/UI/War/TerrainModeInit.cs` |
| `Assets/Script/UI/War/TreasureStone.cs` |
| `Assets/Script/UI/War/UltramanBirthIslandManager.cs` |
| `Assets/Script/UI/War/VATInstanceManager.cs` |
| `Assets/Script/UI/War/WarAnimControl.cs` |
| `Assets/Script/UI/War/WarBarrageChatWidget.cs` |
| `Assets/Script/UI/War/WarBarrageLikeTip.cs` |
| `Assets/Script/UI/War/WarBarrageLikeTips.cs` |
| `Assets/Script/UI/War/WarBarrageOperateWidget.cs` |
| `Assets/Script/UI/War/WaterFoamControl.cs` |
| `Assets/Script/UI/War/WuLinHotelControl.cs` |
| `Assets/Script/UI/War/Data/Knockout/PlayingData.cs` |
| `Assets/Script/UI/War/Data/LoginResultData.cs` |
| `Assets/Script/UI/War/Data/LoginWarData.cs` |
| `Assets/Script/UI/War/Data/RoleDefaultData.cs` |
| `Assets/Script/UI/War/Data/SendLookRoleData.cs` |
| `Assets/Script/UI/War/Data/SendRoleData.cs` |
| `Assets/Script/UI/War/Data/WarBaseData.cs` |
| `Assets/Script/UI/War/Other/GoodTastePlatform.cs` |
| `Assets/Script/UI/War/Other/HideGameObject.cs` |
| `Assets/Script/UI/War/Other/HolySwordPlatform.cs` |
| `Assets/Script/UI/War/Other/KillInfoConfig.cs` |
| `Assets/Script/UI/War/Other/WeekendPeakRankingStage.cs` |
| `Assets/Script/UI/War/Utils/ParseUtils.cs` |
| `Assets/Script/UI/War/Utils/PortUtils.cs` |
| `Assets/Script/UI/War/Utils/WarUtils.cs` |
