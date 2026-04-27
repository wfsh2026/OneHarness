---
name: mode-customroomcamp
display_name: 自定义房间阵营对抗（CustomRoomCamp）
category: mode/customroomcamp
version: 1.0.0
dependencies:
- mode-base
---

# 自定义房间阵营对抗（CustomRoomCamp）

自定义房间阵营模式：支持玩家自建房间进行阵营对抗，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/ClientCustomRoomCampMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/Data/ClientCustomRoomCampData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/Stage/ClientCustomRoomCampBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/Stage/ClientCustomRoomCampBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/CustomRoomCamp/Stage/ClientCustomRoomCampOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/ServerCustomRoomCampMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Data/ServerCustomRoomCampData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Logic/ServerCustomRoomCampAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Logic/ServerCustomRoomCampNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Logic/ServerCustomRoomCampRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Stage/ServerCustomRoomCampBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Stage/ServerCustomRoomCampBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/CustomRoomCamp/Stage/ServerCustomRoomCampOverStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/CustomRoomCamp/ [2 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |
| `Assets/ToBundle/Config/Txt/CustomRoom.txt` |

## 备注

GameMode 枚举 CampCustomized=42. 共 13 文件. 三端分布: C=5/S=8/H=0. key_classes: ClientCustomRoomCampData, ClientCustomRoomCampBattleStage, ClientCustomRoomCampBornStage, ClientCustomRoomCampOverStage, ServerCustomRoomCampData, ServerCustomRoomCampAwardLogic, ServerCustomRoomCampNsqDataLogic, ServerCustomRoomCampRoleLogic, ServerCustomRoomCampBattleStage, ServerCustomRoomCampBornStage. 子目录: Client: Data(1), Stage(3); Server: Data(1), Logic(3), Stage(3). 依赖 CustomRoom.txt 配置

依赖：[[mode-base]]
