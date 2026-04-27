---
name: ui-map
display_name: 地图系统
category: ui
version: 1.0.0
dependencies:
  - ui-framework
---

# 地图系统

小地图+大地图+战略标记系统。MapInfoWin为主窗口，MapPlayer/MapRoleAI/MapItemPoint等标记类型，PoisonGraphic毒圈可视化，UIMapSpotMgr管理兴趣点，支持PC/移动端双模式。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/MapInfo/AnchorTool.cs` |
| `Assets/Script/UI/MapInfo/AnchorToolBox.cs` |
| `Assets/Script/UI/MapInfo/EscWindow.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Base/UIGoldDashInteractSpotItem.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Base/UIGoldDashInteractSpotLogicBase.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Base/UIGoldDashInteractSpotLogicFactory.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Base/UIGoldDashInteractSpotLogicPollingBase.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Base/UIGoldDashInteractSpotStateConfig.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicConditionEscape.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicDefault.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicDragonGate.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicPrePos.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicSwitchPull.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Data/UIGoldDashInteractSpotLogicSwitchPullEscape.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Other/UIGoldDashInteractGameTimeTxt.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/Interact/Other/UIGoldDashInteractMapLine.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/MapAreaFollowMapScale.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/MapTips/UIGoldDashInteractMapTips.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/MapTips/UIGoldDashInteractMapTipsSwitchPull.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/MapTips/UIGoldDashInteractMapTipsSwitchPullEscapePoint.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/SOGoldDashLayerItemData.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashInteractSpotItemBase.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashInteractSpotMgr.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapBox.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapLayer.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapLayerConfig.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapLayerData.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapLayerMgr.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapLayerSlot.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapMermaidTaskSpot.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapSpecialSpot.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashMapSpotMonster.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashRedTempZoneSpot.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIGoldDashRedTempZoneSpotMgr.cs` |
| `Assets/Script/UI/MapInfo/GoldDash/UIMapTimeEscape.cs` |
| `Assets/Script/UI/MapInfo/GoldDashMapIconFilterDropdown.cs` |
| `Assets/Script/UI/MapInfo/GoldDashMapIconFilterOption.cs` |
| `Assets/Script/UI/MapInfo/GoldDashMapInfoWin.cs` |
| `Assets/Script/UI/MapInfo/GoldDashMapTips.cs` |
| `Assets/Script/UI/MapInfo/MapAutoTool.cs` |
| `Assets/Script/UI/MapInfo/MapBeastCampInfo.cs` |
| `Assets/Script/UI/MapInfo/MapCannonSpot.cs` |
| `Assets/Script/UI/MapInfo/MapCarPoint.cs` |
| `Assets/Script/UI/MapInfo/MapEnemyPoint.cs` |
| `Assets/Script/UI/MapInfo/MapFlyLine.cs` |
| `Assets/Script/UI/MapInfo/MapInfoAreaMapGraphic.cs` |
| `Assets/Script/UI/MapInfo/MapInfoBeastCampMode.cs` |
| `Assets/Script/UI/MapInfo/MapInfoGraphic.cs` |
| `Assets/Script/UI/MapInfo/MapInfoLine.cs` |
| `Assets/Script/UI/MapInfo/MapInfoMic.cs` |
| `Assets/Script/UI/MapInfo/MapInfoSpeaker.cs` |
| `Assets/Script/UI/MapInfo/MapInfoWin_OB.cs` |
| `Assets/Script/UI/MapInfo/MapInfoWin_Other.cs` |
| `Assets/Script/UI/MapInfo/MapInfoWin_PC.cs` |
| `Assets/Script/UI/MapInfo/MapInfoWin.cs` |
| `Assets/Script/UI/MapInfo/MapItemMark.cs` |
| `Assets/Script/UI/MapInfo/MapItemPoint.cs` |
| `Assets/Script/UI/MapInfo/MapLandMark.cs` |
| `Assets/Script/UI/MapInfo/MapLogoExplain.cs` |
| `Assets/Script/UI/MapInfo/MapLogoExplainMgr.cs` |
| `Assets/Script/UI/MapInfo/MapMarkName.cs` |
| `Assets/Script/UI/MapInfo/MapPirateShip.cs` |
| `Assets/Script/UI/MapInfo/MapPirateShipMarkTrigger.cs` |
| `Assets/Script/UI/MapInfo/MapPlayer.cs` |
| `Assets/Script/UI/MapInfo/MapPoint.cs` |
| `Assets/Script/UI/MapInfo/MapRoleAI.cs` |
| `Assets/Script/UI/MapInfo/MapRouteSpotPoint.cs` |
| `Assets/Script/UI/MapInfo/MapSpotPoint.cs` |
| `Assets/Script/UI/MapInfo/MapSpotStreamer.cs` |
| `Assets/Script/UI/MapInfo/MapSweepInfo.cs` |
| `Assets/Script/UI/MapInfo/MapSweepInfoControl.cs` |
| `Assets/Script/UI/MapInfo/MapTeamItem.cs` |
| `Assets/Script/UI/MapInfo/MapTerrainPoint.cs` |
| `Assets/Script/UI/MapInfo/MapTestToolBox.cs` |
| `Assets/Script/UI/MapInfo/MapTransPortPoint.cs` |
| `Assets/Script/UI/MapInfo/PcMapBox.cs` |
| `Assets/Script/UI/MapInfo/PoisonGraphic.cs` |
| `Assets/Script/UI/MapInfo/PositionShiftByScreenSpace.cs` |
| `Assets/Script/UI/MapInfo/RoleSpeakerBehaviour.cs` |
| `Assets/Script/UI/MapInfo/SOUIGoldDashMapLayer.cs` |
| `Assets/Script/UI/MapInfo/SportsPartyMapInfo.cs` |
| `Assets/Script/UI/MapInfo/SweepInfoItem.cs` |
| `Assets/Script/UI/MapInfo/UIMapSpotItem.cs` |
| `Assets/Script/UI/MapInfo/UIMapSpotMgr.cs` |
| `Assets/Script/UI/MapInfo/UIMapTaskSpot.cs` |
| `Assets/Script/UI/MapInfo/UIMapTimeBoss.cs` |
| `Assets/Script/UI/MapInfo/UIPlayerFocus.cs` |
| `Assets/Script/UI/MapInfo/Widgets/LobbyMapInfoIconItem.cs` |
| `Assets/Script/UI/MapInfo/Widgets/MapInfoIconItem.cs` |
