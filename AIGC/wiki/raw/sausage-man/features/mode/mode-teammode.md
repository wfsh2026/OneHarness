---
name: mode-teammode
display_name: 团队模式（TeamMode）
category: mode/teammode
version: 1.0.0
dependencies:
- mode-base
---

# 团队模式（TeamMode）

团队对战模式：多人分队对抗，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/ClientTeamModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/ClientTeamModeMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/ClientTeamModeUtil.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Logic/ClientTeamModeRuleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Logic/ClientTeamModeSceneLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeReadyStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeRoundOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeRunningStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/TeamMode/Stage/ClientTeamModeStageBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/ServerTeamModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/ServerTeamModeMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeJoinLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeRebornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeRevengeLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeRuleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeTestLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeTransformLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/ServerTeamModeWeaponLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/TeamModeUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Logic/TimerLogic/ModeTimerLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/SOData/SOTeamModeConfigData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeReadyStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeRoundOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeRunningStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/TeamMode/Stage/ServerTeamModeStageBase.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/FreeforallMode/ [3 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/TimeMode/` |

## 备注

共 32 文件. 三端分布: C=11/S=21/H=0. key_classes: ClientTeamModeData, ClientTeamModeRuleLogic, ClientTeamModeSceneLogic, ClientTeamModeBornStage, ClientTeamModeOverStage, ClientTeamModeReadyStage, ClientTeamModeRoundOverStage, ClientTeamModeRunningStage, ClientTeamModeStageBase, ServerTeamModeData. 子目录: Client: Logic(2), Stage(6); Server: Logic(12), SOData(1), Stage(6). GameMode 枚举 TeamMode

依赖：[[mode-base]]
