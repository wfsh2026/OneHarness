---
name: mode-evodeathmatch
display_name: 团队激斗进阶版（EvoDeathMatch）
category: mode/evodeathmatch
version: 1.0.0
dependencies:
- mode-base
---

# 团队激斗进阶版（EvoDeathMatch）

进阶版团队激斗模式：在标准团队模式基础上增加进化/升级机制，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/ClientEvoDeathMatchEventIds.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/ClientEvoDeathMatchMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Data/ClientEvoDeathMatchData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/LevelEdit/EvoDeathBattleAreaEdit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/LevelEdit/EvoDeathBornGroupEdit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/LevelEdit/EvoDeathBornPointEdit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/LevelEdit/EvoDeathMapEdit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Logic/ClientEvoDeathLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Logic/ClientEvoDeathMapLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Logic/ClientEvoDeathScore.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Stage/ClientEvoDeathBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Stage/ClientEvoDeathOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Stage/ClientEvoDeathStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/EvoDeathMatch/Stage/ClientEvoDeathStartStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/ServerEvoDeathEventIds.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/ServerEvoDeathMatchData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/ServerEvoDeathMatchMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathBorn.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathCall.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathDead.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathNsqData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Logic/ServerEvoDeathScore.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Stage/ServerEvoDeathBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Stage/ServerEvoDeathOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Stage/ServerEvoDeathStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/EvoDeathMatch/Stage/ServerEvoDeathStartStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/EvoDeathMatch/EvoDeathMatchDef.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/EvoDeathMatch/SOEvoDeathBattlePoint.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/EvoDeathMatch/SOEvoDeathMatch.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/EvoDeathMatch/ [6 files, 进阶激斗配置]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 备注

共 31 文件. 三端分布: C=14/S=14/H=3. key_classes: ClientEvoDeathMatchData, ClientEvoDeathLogic, ClientEvoDeathMapLogic, ClientEvoDeathBornStage, ClientEvoDeathOverStage, ClientEvoDeathStage, ClientEvoDeathStartStage, ServerEvoDeathMatchData, ServerEvoDeathLogic, ServerEvoDeathNsqData. 子目录: Client: Data(1), LevelEdit(4), Logic(3), Stage(4); Server: Logic(7), Stage(4). GameMode 枚举 PartyMode（通过 IsEvoDeathMatch 标记区分）

依赖：[[mode-base]]
