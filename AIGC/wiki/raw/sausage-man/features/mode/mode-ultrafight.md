---
name: mode-ultrafight
display_name: 奥特派对（UltraFight）
category: mode/ultrafight
version: 1.0.0
dependencies:
- mode-base
---

# 奥特派对（UltraFight）

奥特主题对战模式：回合制团队对抗，含武器箱/道具箱拾取机制，C/S 两端完整实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/UltraFight/ClientUltraFightMain.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/UltraFightSceneMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Data/ClientUltraFightData.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Logic/ClientUltraFightBoxLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Logic/ClientUltraFightRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Stage/ClientUltraFightBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Stage/ClientUltraFightBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Stage/ClientUltraFightOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Stage/ClientUltraFightReadyStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/UltraFight/Stage/ClientUltraFightWinWaitStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/ServerUltraFightMain.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Data/ServerUltraFightData.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Data/ServerUltraFightData_Method.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightBoxLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Logic/ServerUltraFightWeaponLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Stage/ServerUltraFightBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Stage/ServerUltraFightBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Stage/ServerUltraFightOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Stage/ServerUltraFightReadyStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/UltraFight/Stage/ServerUltraFightWinWaitStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/UltraFight/RoleUltraFight.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleUltraFightHitPart.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/UltraFight/ [1 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |
| `Assets/Script/GamePlay/Host/Modules/UltraFight/Data/UltraFightDataStruct.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/Ultrafight/` |

## 备注

GameMode 枚举 Ultrafight=20. 共 25 文件. 三端分布: C=11/S=14/H=0. key_classes: ClientUltraFightData, ClientUltraFightBoxLogic, ClientUltraFightRoleLogic, ClientUltraFightBattleStage, ClientUltraFightBornStage, ClientUltraFightOverStage, ClientUltraFightReadyStage, ClientUltraFightWinWaitStage, ServerUltraFightData, ServerUltraFightData_Method. 子目录: Client: Data(1), Logic(2), Stage(5); Server: Data(2), Logic(6), Stage(5). 代码不在 Mode/ 目录，位于独立的 Modules/UltraFight/。（1 Manager + 1 Data + 2 Logic + 5 Stage）、（1 Manager + 2 Data + 6 Logic + 5 Stage）。Mode/UltraFight/ 仅有辅助类 RoleUltraFight.cs

依赖：[[mode-base]]
