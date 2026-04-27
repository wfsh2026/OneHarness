---
name: mode-turnbased
display_name: PK之王（TurnBasedMode1V1）
category: mode/turnbased
version: 1.0.0
dependencies:
- mode-base
---

# PK之王（TurnBasedMode1V1）

回合制 1V1 对战模式：玩家轮流操作的 PK 玩法，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/ClientTurnBasedMode1v1Data.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/ClientTurnBasedMode1v1Mgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/TurnBasedMode1v1Stage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Logic/ClientTurnBasedMode1v1MapLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Logic/ClientTurnBasedMode1v1RoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Stage/ClientTurnBasedMode1V1BornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Stage/ClientTurnBasedMode1V1OverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Stage/ClientTurnBasedMode1V1RoundEndStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TurnBasedMode1V1/Stage/ClientTurnBasedMode1V1RoundStartStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/ServerTurnBasedMode1V1Data.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/ServerTurnBasedMode1V1Mgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Logic/ServerTurnBasedMode1V1AwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Logic/ServerTurnBasedMode1V1NsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Logic/ServerTurnBasedMode1V1RoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Logic/ServerTurnBasedMode1v1StatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Logic/ServerTurnBasedModeAILogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Stage/ServerTurnBasedMode1V1BornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Stage/ServerTurnBasedMode1V1OverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Stage/ServerTurnBasedMode1V1RoundEndStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TurnBasedMode1V1/Stage/ServerTurnBasedMode1V1RoundStartStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/TurnBasedMode1V1/ [2 files]` |
| `Assets/ToBundle/ScriptableObject/Screen/SOGunfightRoundData/ [54 files, 回合制对战数据]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 备注

GameMode 枚举 Turnbased=33. 共 20 文件. 三端分布: C=9/S=11/H=0. key_classes: ClientTurnBasedMode1v1Data, TurnBasedMode1v1Stage, ClientTurnBasedMode1v1MapLogic, ClientTurnBasedMode1v1RoleLogic, ClientTurnBasedMode1V1BornStage, ClientTurnBasedMode1V1OverStage, ClientTurnBasedMode1V1RoundEndStage, ClientTurnBasedMode1V1RoundStartStage, ServerTurnBasedMode1V1Data, ServerTurnBasedMode1V1AwardLogic. 子目录: Client: Logic(2), Stage(4); Server: Logic(5), Stage(4)

依赖：[[mode-base]]
