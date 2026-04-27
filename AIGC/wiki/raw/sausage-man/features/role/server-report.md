---
name: server-report
display_name: 服务端数据上报（Report）
category: server/report
version: 1.0.0
dependencies:
  - mode-base
---

# 服务端数据上报（Report）

服务端数据上报与日志系统：战斗日志、NSQ 数据上报、各模式统计数据上报。纯 Server 端 + 部分客户端举报 UI。共 70 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Biubiubiu2/Data/WarReportData.cs` |
| `Assets/Script/Biubiubiu2/UI/UIControl/WarReport/UIWarReport.cs` |
| `Assets/Script/Biubiubiu2/UI/UIView/Feature/WarReportView.cs` |
| `Assets/Script/Config/FootballReportConfig.cs` |
| `Assets/Script/Config/FootballReportConfig_Part.cs` |
| `Assets/Script/Data/SOWarReportSet.cs` |
| `Assets/Script/Editor/BundleBuild/Editor/Scripts/BundleBuildTimeReport.cs` |
| `Assets/Script/Editor/ReportAirDropDateEditor.cs` |
| `Assets/Script/FunnyTools/ReportAirDropDate.cs` |
| `Assets/Script/GamePlay/AutoWar/WarReportPlayTool.cs` |
| `Assets/Script/GamePlay/Base/Report/ReportLogRegister.cs` |
| `Assets/Script/GamePlay/Base/Report/ReportNsqRegister.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballReportLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/Features/ClientRoleAIReportMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballReportEventId.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_SportsPartyGameOverData_ReportData.cs` |
| `Assets/Script/GamePlay/Server/Constants/ServerLogReportConstants.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatLogDataReport.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatLogReportConstants.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutReportLogLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutReportNsqLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallRoleReportLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballReportLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportBatteryTurretLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportPlayerCheatLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportPlayerFps40Log.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportPlayerItemLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportReviveLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportRoundEndDataLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportTeamLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportTreasureCrateLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportUnetError.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReporMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportAddHP.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportAppointObjectHert.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportConsumeBullet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportDead.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportDecItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportDestroyCarrier.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportDriveKill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportGetItemFromBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportHurt.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportKill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportKillAppointObject.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportKillStreak.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportOverCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportPartsKill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportPartyHeroProficiency.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportRevive.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportSpecial.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportTeamKill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportTotalCollectItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUnetReport.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUpdateClientType.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUseAction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportUseItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportWarPlayerStatusDetails.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Nsq/ReportWeedOut.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/ILogClear.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/ServerLogDataReport.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/ServerNsqDataReport.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/ServerNsqDataReport_Knockout.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIManager/Features/ServerRoleAIReportMgr.cs` |
| `Assets/Script/Manager/WarReportSetting.cs` |
| `Assets/Script/QualityTool/Script/AssetCheckTool/Database/Report.cs` |
| `Assets/Script/QualityTool/Script/AssetCheckTool/Window/ReportWindow.cs` |
| `Assets/Script/UI/OnlyUpPlayersInfo/OnlyUpPlayerInfoReportWidget.cs` |
| `Assets/Script/Utils/FunnyTool/ExceptionReportController.cs` |

## 备注

依赖：[[mode-base]]
