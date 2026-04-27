---
name: mode-rookiecamp
display_name: 新手训练营（RookieCamp）
category: mode/rookiecamp
version: 1.0.0
dependencies:
- mode-base
---

# 新手训练营（RookieCamp）

新手引导模式：为新玩家提供基础操作教程和训练关卡，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/ClientRookieCampData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/ClientRookieCampMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampCreateCarInfo.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampLevelConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampLevelData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampLevelStepConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampSceneItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepAIBornConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepAiUseItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepCarMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepCarPivot.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepGameEnd.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepGrowthTip.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepJumpFly.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepMoveTarget.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepPickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepShootGame.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepSpeedGame.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Config/SORookieCampStepUprear.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Logic/ClientRookieCampAILogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Logic/ClientRookieCampLevelLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Logic/ClientRookieCampTaskLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/IRookieCampTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampAIBornData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampCarTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampCondition.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampDefine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampEndTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampEnemyFactory.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampEventTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampMoveCheckPoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampMoveTargetPath.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampOperateManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampPreload.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Other/RookieCampStartTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Stage/ClientRookieCampInitStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Stage/ClientRookieCampOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Stage/ClientRookieCampPlayStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepCarMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepFactory.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepFlyJump.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepGameEnd.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepGrowthTip.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepIDCard.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepLook.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepMoveTarget.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepPickItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepShootGame.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepSpeedGame.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepUprear.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Step/RookieCampStepUseMedicine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Task/RookieCampMainTask.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Task/RookieCampSubTask.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampAIBornConfigMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampAIBornDataConfigMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampCarData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampCarPivotData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampLevelDataMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampSceneItemMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/RookieCamp/Tool/RookieCampSceneItemPointMono.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/ServerRookieCampData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/ServerRookieCampMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/Stage/ServerRookieCampInitStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/Stage/ServerRookieCampOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/RookieCamp/Stage/ServerRookieCampPlayStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/RookieCamp/ [86 files, 新手营关卡/步骤/AI 配置]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/RookieCamp/ [19 files, 新手营特效]` |

## 备注

共 68 文件. 三端分布: C=63/S=5/H=0. key_classes: ClientRookieCampData, SORookieCampLevelData, ClientRookieCampAILogic, ClientRookieCampLevelLogic, ClientRookieCampTaskLogic, RookieCampAIBornData, RookieCampEnemyFactory, RookieCampOperateManager, ClientRookieCampInitStage, ClientRookieCampOverStage. 子目录: Client: Config(18), Logic(3), Other(13), Stage(3), Step(15), Task(2), Tool(7); Server: Stage(3). GameMode 枚举 RookieCamp。，以客户端引导逻辑为主

依赖：[[mode-base]]
