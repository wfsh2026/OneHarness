---
name: ui-tips
display_name: 提示信息系统
category: ui
version: 1.0.0
dependencies:
  - ui-framework
---

# 提示信息系统

游戏内提示/通知系统。Tips(46文件)管理通用提示弹窗，TipsWar(15文件)管理战场内信息面板(击杀/伤害/拾取)，WarModeTips(28文件)管理模式特定提示，覆盖打金/足球/狼人等模式。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/BuiltinTips/BuiltinTips.cs` |
| `Assets/Script/UI/GameTaskTip/BattleRandomItem.cs` |
| `Assets/Script/UI/GameTaskTip/GameTaskTipWin.cs` |
| `Assets/Script/UI/GameTaskTip/GlobalRandomGameplayWin.cs` |
| `Assets/Script/UI/GolddashEventTips/GolddashEventTipsWin.cs` |
| `Assets/Script/UI/GoldItemPickTips/GoldItemChallengeController.cs` |
| `Assets/Script/UI/GoldItemPickTips/GoldItemChallengeWin.cs` |
| `Assets/Script/UI/GoldItemPickTips/GoldItemOneLeftTip.cs` |
| `Assets/Script/UI/GoldItemPickTips/GoldItemPickTipsController.cs` |
| `Assets/Script/UI/GoldItemPickTips/GoldItemPickTipsWin.cs` |
| `Assets/Script/UI/ModeGuideTips/ModeGuideTipsWin.cs` |
| `Assets/Script/UI/Tips/AddSocreAnimItem.cs` |
| `Assets/Script/UI/Tips/BasePopUpBox.cs` |
| `Assets/Script/UI/Tips/CostConfirm.cs` |
| `Assets/Script/UI/Tips/GoldDashBossTip.cs` |
| `Assets/Script/UI/Tips/GoldDashInGameEventTips.cs` |
| `Assets/Script/UI/Tips/GoldDashLabelItem.cs` |
| `Assets/Script/UI/Tips/GoldDashLootItem.cs` |
| `Assets/Script/UI/Tips/GoldDashMermaidGainTips.cs` |
| `Assets/Script/UI/Tips/GoldDashScoreItem.cs` |
| `Assets/Script/UI/Tips/GoldDashTutorialTipItem.cs` |
| `Assets/Script/UI/Tips/KillInfoItem.cs` |
| `Assets/Script/UI/Tips/NetTips.cs` |
| `Assets/Script/UI/Tips/NoviceGuideWin.cs` |
| `Assets/Script/UI/Tips/ObbLaunchChecker.cs` |
| `Assets/Script/UI/Tips/ObbLaunchTips.cs` |
| `Assets/Script/UI/Tips/OPSMesage.cs` |
| `Assets/Script/UI/Tips/RefuseTips.cs` |
| `Assets/Script/UI/Tips/ShowStateTip.cs` |
| `Assets/Script/UI/Tips/ShutTips.cs` |
| `Assets/Script/UI/Tips/TipBlackBGPanel.cs` |
| `Assets/Script/UI/Tips/TipDeadInfo.cs` |
| `Assets/Script/UI/Tips/TipDeadInfoPartyMode.cs` |
| `Assets/Script/UI/Tips/TipError.cs` |
| `Assets/Script/UI/Tips/TipGoldDash.cs` |
| `Assets/Script/UI/Tips/TipGoldDashAddScoreAnim.cs` |
| `Assets/Script/UI/Tips/TipKillDistance.cs` |
| `Assets/Script/UI/Tips/TipKillInfo.cs` |
| `Assets/Script/UI/Tips/TipKillItemBase.cs` |
| `Assets/Script/UI/Tips/TipPanel.cs` |
| `Assets/Script/UI/Tips/TipPanelWar.cs` |
| `Assets/Script/UI/Tips/TipRoleKillInfo.cs` |
| `Assets/Script/UI/Tips/TipsAntiAddiction.cs` |
| `Assets/Script/UI/Tips/TipsConfirm.cs` |
| `Assets/Script/UI/Tips/TipScoreInfo.cs` |
| `Assets/Script/UI/Tips/TipsDownClient.cs` |
| `Assets/Script/UI/Tips/TipSecondaryAtk.cs` |
| `Assets/Script/UI/Tips/TipServerMsg.cs` |
| `Assets/Script/UI/Tips/TipsGiantBattle.cs` |
| `Assets/Script/UI/Tips/TipsHandler.cs` |
| `Assets/Script/UI/Tips/TipsKillTeam.cs` |
| `Assets/Script/UI/Tips/TipsReLogin.cs` |
| `Assets/Script/UI/Tips/TipsSureCancel.cs` |
| `Assets/Script/UI/Tips/TipsTeam.cs` |
| `Assets/Script/UI/Tips/TipsUtility.cs` |
| `Assets/Script/UI/Tips/TipsWin.cs` |
| `Assets/Script/UI/Tips/TipWeakInfo.cs` |
| `Assets/Script/UI/TipsTeam/DropdownToggle.cs` |
| `Assets/Script/UI/TipsWar/GameQuanCountDownWin.cs` |
| `Assets/Script/UI/TipsWar/RandomGameTip.cs` |
| `Assets/Script/UI/TipsWar/ResurrectionMechanismTip.cs` |
| `Assets/Script/UI/TipsWar/TeamStateChangeTip.cs` |
| `Assets/Script/UI/TipsWar/TipCountDown.cs` |
| `Assets/Script/UI/TipsWar/TipDeliveryCannon.cs` |
| `Assets/Script/UI/TipsWar/TipDownTime.cs` |
| `Assets/Script/UI/TipsWar/TipHolySword.cs` |
| `Assets/Script/UI/TipsWar/TipsFootballMode.cs` |
| `Assets/Script/UI/TipsWar/TipSignalInfo.cs` |
| `Assets/Script/UI/TipsWar/TipSkillCD.cs` |
| `Assets/Script/UI/TipsWar/TipSpecAirThrow.cs` |
| `Assets/Script/UI/TipsWar/TipsWarWin.cs` |
| `Assets/Script/UI/TipsWar/WeaponEquip.cs` |
| `Assets/Script/UI/TipsWar/WeaponEquipItem.cs` |
| `Assets/Script/UI/WarModeTips/CountdownTipsWidget.cs` |
| `Assets/Script/UI/WarModeTips/DangerTipWidget.cs` |
| `Assets/Script/UI/WarModeTips/DeathMatchTips.cs` |
| `Assets/Script/UI/WarModeTips/DefusalModeTips.cs` |
| `Assets/Script/UI/WarModeTips/EnterBroadcastTips.cs` |
| `Assets/Script/UI/WarModeTips/GameResultWidget.cs` |
| `Assets/Script/UI/WarModeTips/GoldDashTaskTips.cs` |
| `Assets/Script/UI/WarModeTips/GoldDashTaskTipsItem.cs` |
| `Assets/Script/UI/WarModeTips/GoldDashTaskTipsResult.cs` |
| `Assets/Script/UI/WarModeTips/GoldDashTimeTips.cs` |
| `Assets/Script/UI/WarModeTips/GoldDashTimeTipsAnim.cs` |
| `Assets/Script/UI/WarModeTips/GunFightTips.cs` |
| `Assets/Script/UI/WarModeTips/HideAndSeekTips.cs` |
| `Assets/Script/UI/WarModeTips/HotPhaseTipWidget.cs` |
| `Assets/Script/UI/WarModeTips/KillPlayerEffectWidget.cs` |
| `Assets/Script/UI/WarModeTips/KnockoutKingTips.cs` |
| `Assets/Script/UI/WarModeTips/LastKillWidget.cs` |
| `Assets/Script/UI/WarModeTips/LobbyPKModeTips.cs` |
| `Assets/Script/UI/WarModeTips/ModeGuideTipsPage.cs` |
| `Assets/Script/UI/WarModeTips/PVEModeTips.cs` |
| `Assets/Script/UI/WarModeTips/SportPartyTips.cs` |
| `Assets/Script/UI/WarModeTips/WarCommonTipsWidget.cs` |
| `Assets/Script/UI/WarModeTips/WarModeShowItemWidget.cs` |
| `Assets/Script/UI/WarModeTips/WarModeTipsWin.cs` |
| `Assets/Script/UI/WarModeTips/WarMultipleTextWidget.cs` |
| `Assets/Script/UI/WarModeTips/WarObjTipsWidget.cs` |
| `Assets/Script/UI/WarModeTips/WarTextTipsWidget.cs` |
| `Assets/Script/UI/WarModeTips/WinnerBadgeWidget.cs` |
