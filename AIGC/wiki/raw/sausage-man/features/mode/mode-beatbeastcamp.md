---
name: mode-beatbeastcamp
display_name: 暴打猛兽营（BeatBeastCamp）
category: mode/beatbeastcamp
version: 1.0.0
dependencies:
- mode-base
---

# 暴打猛兽营（BeatBeastCamp）

PvE 合作模式：玩家组队挑战猛兽 Boss，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/ClientBeatBeastCampData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/ClientBeatBeastCampEventId.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/ClientBeatBeastCampMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateAwardRunner.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateGoldRunnerClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateMonsterRunnerClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateTargetRunnerClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientBeastCampLevelLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientBeastGameTriggerMgrLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientBeatBeastCampBornLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientBeatBeastCampMapLoadLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientBeatBeastCampRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Logic/ClientSceneMonoUpdateManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/BeastCampChangeSceneComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/BeastCampLevelDesignAIConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/BeastCampLevelDesignMenu.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/BeastCampLevelDesignSkillConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/BeastCampLockItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/AINodeDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/AirWallAreaDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/BeastCampLevelDesignDataType.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/BornPointDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/ChestDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/DeadAreaDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/GoldDataMaker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/LevelAreaDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/LevelDesignDataManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/LevelDesignDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/LockBuffDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/MonsterCoinDataMaker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/ParentLevelDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/PointDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/SkillConfigDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/StarDataMaker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/SubLevelDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/TransportPointDataMarker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Mono/LevelDesignDataMarker/TriggerDataMaker.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Stage/ClientBeatBeastCampBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Stage/ClientBeatBeastCampGameStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BeatBeastCamp/Stage/ClientBeatBeastCampOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/ServerBeatBeastCampEventId.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/ServerBeatBeastCampMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/SeverBeatBeastCampData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateGoldRunnerServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateMonsterRunnerServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerCreateTargetRunnerServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServeBeastCampStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeastCampMonsterDropLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeastGameTriggerMgrLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeatBeastCampBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeatBeastCampLevelLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeatBeastCampMonsterLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeatBeastCampNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Logic/ServerBeatBeastCampRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/SOData/SOBeatBeastCampConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/SOData/SOBeatBeastCampLevelConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Stage/ServerBeatBeastCampBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Stage/ServerBeatBeastCampGameStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BeatBeastCamp/Stage/ServerBeatBeastCampOverStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/BeastCampMonsterDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/HostBeastCampLevelLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastCodeBlockMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastCodeBlockTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastGameMoveRotate.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastGameTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastGameTriggerManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastGoldTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastStarTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/BeastTriggerLightOnBlock.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastCollectionSpawn.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerCreateAward.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerCreateGold.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerCreateMonster.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerCreateTarget.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerMove.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/BeatBeastCamp/GameTriggerRunner/SOBeastTrigger/SOBeastTriggerRotation.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/BeatBeastCamp/ [63 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/TimeModeBeastCamp/` |
| `Assets/ToBundle/Effect/Mode/BeatBeastCamp/` |

## 备注

GameMode 枚举 BeatCamp=45. 共 78 文件. 三端分布: C=40/S=19/H=19. key_classes: ClientBeatBeastCampData, ClientBeastCampLevelLogic, ClientBeastGameTriggerMgrLogic, ClientBeatBeastCampBornLogic, ClientBeatBeastCampMapLoadLogic, ClientBeatBeastCampRoleLogic, ClientSceneMonoUpdateManager, AINodeDataMarker, AirWallAreaDataMarker, BeastCampLevelDesignDataType. 子目录: Client: GameTriggerRunner(4), Logic(6), Mono(24), Stage(3); Server: GameTriggerRunner(3), Logic(8), SOData(2), Stage(3); Host: GameTriggerRunner(17). PvE Boss 挑战类模式

依赖：[[mode-base]]

## 关联 Buff


### 猛兽营 Buff（3）

| feature | 说明 |
|---------|------|
| [[buff-beast-camp-gold]] | BSBeastCampGold - BeastCampGold |
| [[buff-beast-game-box-down-hp]] | BSBeastGameBoxDownHp - BeastGameBoxDownHp |
| [[buff-beast-trigger-collected-award]] | BSBeastTriggerCollectedAward - BeastTriggerCollectedAward |
