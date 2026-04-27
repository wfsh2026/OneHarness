---
name: mode-golddash-fast
display_name: 快速撤离（FastGoldDash）
category: mode/golddash-fast
version: 1.0.0
dependencies:
- mode-base
- mode-golddash
---

# 快速撤离（FastGoldDash）

撤离模式的快速版：简化流程、缩短时长的撤离玩法，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/ClientFastGoldDashData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/ClientFastGoldDashEventId.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/ClientFastGoldDashMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/FastGoldDashModeStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Logic/ClientFastGoldDashAirWallLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Logic/ClientFastGoldDashMarkLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Logic/ClientFastGoldDashPanelLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Logic/ClientFastGoldDashShopLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Stage/ClientFastGoldDashBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Stage/ClientFastGoldDashOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Stage/ClientFastGoldDashRoundEndStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Stage/ClientFastGoldDashRoundStartStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FastGoldDash/Stage/ClientFastGoldDashShopStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/ServerFastGoldDashData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/ServerFastGoldDashEventId.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/ServerFastGoldDashMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashAirWallLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashBornLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashLookLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashShopLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashSkillLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Logic/ServerFastGoldDashStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Stage/ServerFastGoldDashBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Stage/ServerFastGoldDashOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Stage/ServerFastGoldDashRoundEndStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Stage/ServerFastGoldDashRoundStartStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FastGoldDash/Stage/ServerFastGoldDashShopStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FastGoldDash/HostFastGoldDashClass.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FastGoldDash/HostFastGoldDashRoleShopInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FastGoldDash/HostFastGoldDashRoleSkillsInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/FastGoldDash/HostFastGoldDashShopSuitInfo.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/FastGoldDash/ [7 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/GoldDash/` |
| `Assets/ToBundle/Effect/Mode/GoldDash/` |

## 备注

共 34 文件. 三端分布: C=13/S=17/H=4. key_classes: ClientFastGoldDashData, FastGoldDashModeStage, ClientFastGoldDashAirWallLogic, ClientFastGoldDashMarkLogic, ClientFastGoldDashPanelLogic, ClientFastGoldDashShopLogic, ClientFastGoldDashBornStage, ClientFastGoldDashOverStage, ClientFastGoldDashRoundEndStage, ClientFastGoldDashRoundStartStage. 子目录: Client: Logic(4), Stage(5); Server: Logic(9), Stage(5). GameMode 枚举 FastGoldDashMode。。基于 GoldDash 简化，依赖 mode-golddash

依赖：[[mode-base]] · [[mode-golddash]]
