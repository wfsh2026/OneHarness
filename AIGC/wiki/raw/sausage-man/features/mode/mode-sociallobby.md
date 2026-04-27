---
name: mode-sociallobby
display_name: 互动大厅（SocialLobby）
category: mode/sociallobby
version: 1.0.0
dependencies:
- mode-base
---

# 互动大厅（SocialLobby）

社交互动模式：提供玩家社交空间，支持互动活动，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/ClientSocialLobbyData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/ClientSocialLobbyMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Logic/ClientSocialLobbyGroupLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Logic/ClientSocialLobbyInitItemLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/LobbyChangeSceneCmpt.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/LobbyEventNpc.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/PlayerSceneAvatar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/MiniGameTeam/ClientMiniGameTeamData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/RedPacketRain/RedPacketRainNpcHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/RedPacketRain/RedPacketRainNpcModel.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/RedPacketRain/RedPacketRainPoint.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/RedPacketRain/WealthGodNpcHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/ILobbyShootGameMonoObj.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameCheckPointMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameDeadArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameEndArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameItemGroupMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameMonoTool.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameRankArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameRebornArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameScorePointMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameStartArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameTargetMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Other/ShootGame/SocialLobbyShootGameTriggerArea.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Stage/ClientSocialLobbyInitStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Stage/ClientSocialLobbyOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/SocialLobby/Stage/ClientSocialLobbyRunningStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/ServerSocialLobbyData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/ServerSocialLobbyMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Logic/ServerSocialLobbyEventLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Logic/ServerSocialLobbyGroupLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Logic/ServerSocialLobbyInitItemLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Logic/ServerSocialLobbyRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ServerLobbyEventData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/CircleGame/ServerSocialLobbyCircleGameManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/MiniGameTeam/IMiniGameMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/MiniGameTeam/ServerMiniGameTeamData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/IServerLobbyShootGameFeature.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCheckPoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCopy.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCopy_Log.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCopy_Rank.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCopy_Role.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameCopy_State.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGamePlayerData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameRankData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameRebornPoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameScorePoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Other/ShootGame/ServerLobbyShootGameTargetPoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Stage/ServerSocialLobbyInitStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Stage/ServerSocialLobbyOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/SocialLobby/Stage/ServerSocialLobbyRunningStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/SocialLobby/LobbyMiniGameHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/SocialLobby/MiniGameTeamPlayerData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/SocialLobby/SocialLobbyDefine.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/SocialLobby/ [1 file]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientLobbyPKFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientSocialLobbyMiniGameTeamManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientSocialLobbyShootGameManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerLobbyPKFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerSocialLobbyCircleGameRankManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerSocialLobbyMiniGameTeamManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerSocialLobbyShootGameManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/LobbyMiniGame/BoxingTrampoline/BoxingTrampolineMono.cs` |

## 备注

GameMode 枚举 InteractionSpace=25. 共 56 文件. 三端分布: C=28/S=25/H=3. key_classes: ClientSocialLobbyData, ClientSocialLobbyGroupLogic, ClientSocialLobbyInitItemLogic, ClientMiniGameTeamData, ClientSocialLobbyInitStage, ClientSocialLobbyOverStage, ClientSocialLobbyRunningStage, ServerSocialLobbyData, ServerSocialLobbyEventLogic, ServerSocialLobbyGroupLogic. 子目录: Client: Logic(2), Other(21), Stage(3); Server: Logic(4), Other(16), Stage(3)

依赖：[[mode-base]]
