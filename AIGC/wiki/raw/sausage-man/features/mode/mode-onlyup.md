---
name: mode-onlyup
display_name: 暴跳西游路（OnlyUp）
category: mode/onlyup
version: 1.0.0
dependencies:
- mode-base
---

# 暴跳西游路（OnlyUp）

暴跳西游路（OnlyUp竞速攀登模式）：玩家向上攀爬竞速，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/ClientOnlyUpDefine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/ClientOnlyUpMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/OnlyUpModeStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Data/ClientOnlyUpData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpAdsorbLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpArtSettingLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpBornLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpCheatLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpChestLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpEffectLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpLevelConfigLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpLevelLayerLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpTimeRecordLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpTimerLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/AbsClientOnlyUpLevelLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelCantPassLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelDeadAreaLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelLoaderMgrLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelMapLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelMustPassLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelNameCardLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelLoader/ClientOnlyUpLevelTimerLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelObjCreater/ClientOnlyUpLevelObj.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelObjCreater/ClientOnlyUpLevelObjPool.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/LevelObjCreater/OnlyUpLevelObjPool.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Other/OnlyUpLevelNameCard.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Other/OnlyUpLevelObj.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Other/ParentLevelLayer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Other/SubLevelLayer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/SOData/SOOnlyUpArtSettings.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/SOData/SOOnlyUpEffectData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Stage/ClientOnlyUpBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Stage/ClientOnlyUpGameStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Stage/ClientOnlyUpOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/ServerOnlyUpEventId.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/ServerOnlyUpMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Data/ServerOnlyUpData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpAFKLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpAdsorbLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpCheatLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpChestLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpLevelConfigLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpLevelRefreshLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpMaorioLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpSaveLevelLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpTimeRecordLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpTimerLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpTrapLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/SOData/SOOnlyUpLevelData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/SOData/SOOnlyUpModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/SOData/SOOnlyUpTrapData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Stage/ServerOnlyUpBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Stage/ServerOnlyUpGameStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Stage/ServerOnlyUpOverStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/OnlyUpMode/AbsOnlyUpLevelConfigLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/OnlyUpMode/AbsOnlyUpModeData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/OnlyUpMode/AbsOnlyUpRoleTimeRecordLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/OnlyUpMode/OnlyUpRoleLevelTime.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/OnlyUpMode/OnlyUpSubLevelTime.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/OnlyUp/ [16 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/OnlyUp/` |

## 备注

GameMode 枚举 OnlyUp=40. 共 65 文件. 三端分布: C=35/S=25/H=5. key_classes: OnlyUpModeStage, ClientOnlyUpData, ClientOnlyUpAdsorbLogic, ClientOnlyUpArtSettingLogic, ClientOnlyUpBornLogic, ClientOnlyUpCheatLogic, ClientOnlyUpChestLogic, ClientOnlyUpEffectLogic, ClientOnlyUpLevelConfigLogic, ClientOnlyUpLevelLayerLogic. 子目录: Client: Data(1), Logic(22), Other(4), SOData(2), Stage(3); Server: Data(1), Logic(16), SOData(3), Stage(3). 注意 Host 端目录名为 OnlyUpMode

依赖：[[mode-base]]
