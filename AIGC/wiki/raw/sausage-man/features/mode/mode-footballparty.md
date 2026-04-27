---
name: mode-footballparty
display_name: 足球派对（FootballParty）
category: mode/footballparty
version: 1.0.0
dependencies:
- mode-base
---

# 足球派对（FootballParty）

足球竞技模式：多人足球对战，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/ClientFootballData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/ClientFootballDefine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/ClientFootballMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballBallLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballBallLogic_Other.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballCheatCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballDataLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballReportLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballTerrainLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Mono/ClientFootballController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Mono/ClientFootballDataDisplay.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Mono/ClientScreenDisplay.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Mono/FootBallAwake.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Mono/FootBallRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/ClientFootballAnimatorEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/FootballBallEffectMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/FootballGameEffectMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/FootballRoleCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/RoleFootBall.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Other/WallTouchBallEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballCameraStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballCloseupStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballReadyStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Stage/ClientFootballShowStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/ServerFootballData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/ServerFootballDefine.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/ServerFootballMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootbalNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballBallLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballBuffAreaLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballCheatCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballEventLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballReportLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballTerrainLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Mono/ServerFootballController.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Mono/ServerFootballGoal.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Mono/ServerFootballOutside.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Mono/ServerFootballWoodwork.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballCameraStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballCloseupStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballReadyStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Stage/ServerFootballShowStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/AbsFootballController.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/BeizerPathManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootBallNetwork.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootBallNetworkMirror.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballMonoManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballReportEventId.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FootballParty/FootballWall.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/FootballParty/ [2 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/Football/` |
| `Assets/ToBundle/Effect/Mode/Fifa/` |

## 备注

GameMode 枚举 LimitedtimeFifamode=19. 共 61 文件. 三端分布: C=28/S=24/H=9. key_classes: ClientFootballData, ClientFootballBallLogic, ClientFootballBallLogic_Other, ClientFootballDataLogic, ClientFootballReportLogic, ClientFootballRoleLogic, ClientFootballTerrainLogic, ClientFootballController, ClientFootballDataDisplay, ClientFootballBattleStage. 子目录: Client: Logic(7), Mono(5), Other(6), Stage(7); Server: Logic(10), Mono(4), Stage(7)

依赖：[[mode-base]]
