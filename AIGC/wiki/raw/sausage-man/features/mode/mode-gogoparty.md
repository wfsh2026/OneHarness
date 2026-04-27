---
name: mode-gogoparty
display_name: 闯关吧！肠肠！（GoGoPartyMode）
category: mode/gogoparty
version: 1.0.0
dependencies:
- mode-base
---

# 闯关吧！肠肠！（GoGoPartyMode）

多人闯关模式：玩家通过各种障碍关卡竞速，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/ClientGoGoPartyModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/ClientGoGoPartyModeEventId.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/ClientGoGoPartyModeMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Logic/ClientGoGoPartyModeActionLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Logic/ClientGoGoPartyModeAwardBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Logic/ClientGoGoPartyModeBornLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Logic/ClientGoGoPartyModeEffectLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Logic/ClientGoGoPartyModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/AwardBoxTriggerMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/AwardDanmuUI.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/GoGoPartyPrizeWall.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/GoGoPartyPrizetem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/OpenAwardBoxFailUI.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Mono/OpenAwardBoxUI.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Stage/ClientGoGoPartyModeBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Stage/ClientGoGoPartyModeGameStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/GoGoPartyMode/Stage/ClientGoGoPartyModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/ServerGoGoPartyModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/ServerGoGoPartyModeEventId.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/ServerGoGoPartyModeMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServeGoGoPartyModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeAFKLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeActionLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeAwardBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeMiniGameLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyModeTeamLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Logic/ServerGoGoPartyReplayLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/SOData/SOGoGoPartyModeAwardBoxConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/SOData/SOGoGoPartyModeConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/SOData/SOGoGoPartyModeEffectConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Stage/ServerGoGoPartyModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Stage/ServerGoGoPartyModeGameStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/GoGoPartyMode/Stage/ServerGoGoPartyModeOverStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/GoGoPartyMode/ [4 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/GoGoParty/` |

## 备注

GameMode 枚举 GogoParty=47. 共 36 文件. 三端分布: C=17/S=19/H=0. key_classes: ClientGoGoPartyModeData, ClientGoGoPartyModeActionLogic, ClientGoGoPartyModeAwardBoxLogic, ClientGoGoPartyModeBornLogic, ClientGoGoPartyModeEffectLogic, ClientGoGoPartyModeRoleLogic, ClientGoGoPartyModeBornStage, ClientGoGoPartyModeGameStage, ClientGoGoPartyModeOverStage, ServerGoGoPartyModeData. 子目录: Client: Logic(5), Mono(6), Stage(3); Server: Logic(10), SOData(3), Stage(3)

依赖：[[mode-base]]
