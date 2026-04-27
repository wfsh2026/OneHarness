---
name: mode-defusal
display_name: 爆破模式（DefusalMode）
category: mode/defusal
version: 1.0.0
dependencies:
- mode-base
---

# 爆破模式（DefusalMode）

经典爆破模式：攻防双方围绕炸弹进行对抗，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/ClientDefusalModeMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Data/ClientDefusalModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Logic/ClientDefusalModeBombLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Logic/ClientDefusalModeMapLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Logic/ClientDefusalModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeReadyStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeShopStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/Stage/ClientDefusalModeWinWaitStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/ServerDefusalModeMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Data/ServerDefusalModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeBombLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeMapLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeMvpLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Logic/ServerDefusalModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeReadyStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeShopStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/Stage/ServerDefusalModeWinWaitStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/DefusalMode/ [3 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/DeMode/` |

## 备注

GameMode 枚举 Defusalmode=34. 共 26 文件. 三端分布: C=11/S=15/H=0. key_classes: ClientDefusalModeData, ClientDefusalModeBombLogic, ClientDefusalModeMapLogic, ClientDefusalModeRoleLogic, ClientDefusalModeBattleStage, ClientDefusalModeBornStage, ClientDefusalModeOverStage, ClientDefusalModeReadyStage, ClientDefusalModeShopStage, ClientDefusalModeWinWaitStage. 子目录: Client: Data(1), Logic(3), Stage(6); Server: Data(1), Logic(7), Stage(6)

依赖：[[mode-base]]
