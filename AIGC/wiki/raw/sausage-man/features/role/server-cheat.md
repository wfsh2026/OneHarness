---
name: server-cheat
display_name: 服务端反作弊系统（Cheat）
category: server/cheat
version: 1.0.0
dependencies:
  - mode-base
---

# 服务端反作弊系统（Cheat）

服务端反作弊检测系统：移动校验、伤害校验、速度检测、各模式专属反作弊逻辑。纯 Server 端实现。共 101 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/AutoWar/AutoWarData/BulletCheatAutoWar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Cheat/CheatColliderComponet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientCheatColliderManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientGameCheatFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/FootballParty/Logic/ClientFootballCheatCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/OnlyUp/Logic/ClientOnlyUpCheatLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleBodyPartCheat.cs` |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_GameCheat_Base.cs` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_GameCheat.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Data/CheatAreaData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/CheatArea.cs` |
| `Assets/Script/GamePlay/Host/Modules/Knockout/Node/CheatNodeParent.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_GameCheat.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_BulletControl_BulletCheatData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_BulletManager_BulletCheatData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_OnlyUpCheatData.cs` |
| `Assets/Script/GamePlay/Server/Constants/ServerConstans_Cheat.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleAimDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleCheatContext.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleDamageDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleKillAnalyzerData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleKillDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleKillMeleeAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleKillSpeedAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleKillSuspicionAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleShootDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/BattleWallHackDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/IBattleCheatDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BattleDetector/IBattleKillAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/BeastCampCheatModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatAreaUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatConfigManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatLogDataReport.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatLogReportConstants.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/CheatUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/FastGoldDashCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/FastGoldDashCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoGoPartyCheatModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatLogData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/GoldDashRoleCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/JumpDetector/IJumpCheatDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/JumpDetector/JumpCheatContext.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/JumpDetector/JumpFlyDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/JumpDetector/JumpPointDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/JumpDetector/JumpSpeedDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/CheatMoveSpeedConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/IMoveCheatDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/IMoveSpeedAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/InstantSpeedAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/LongTermSpeedAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/MoveCheatContext.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/MoveDistanceDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/MoveNetStateDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/MoveSpeedAnalyzerData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/MoveSpeedDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/NoClipMoveDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/ResetTimeSpeedAnalyzer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/MoveDetector/TeleportDetector.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/PartyModeCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/PartyModeCheatJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/PartyModeCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatBuff.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatBulletCheckData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatBulletFireData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatCollider.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatGoldDashAI.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatGoldItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatHighPing.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatHolySword.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatKill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatMeleeAttackData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatPoint.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatSausageAI.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatUseItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/RoleCheatWave.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/SausageRoleCheatBattle.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/SausageRoleCheatJump.cs` |
| `Assets/Script/GamePlay/Server/Modules/Cheat/SausageRoleCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerCheatFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Knockout/ServerKnockoutCheatCheckLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/FootballParty/Logic/ServerFootballCheatCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/OnlyUp/Logic/ServerOnlyUpCheatLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Report/Data/Log/ReportPlayerCheatLog.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheat.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatAction.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatBullet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatCar.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatMTP.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleCheatWeapon.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_CheatCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/SportsParty/ServerSportsPartyCheckCheatLogic.cs` |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_GameCheat_Base.cs` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_GameCheat.cs` |
| `Assets/Script/UI/DevTool/DevToolHelp/DevToolAntiCheat.cs` |
| `Assets/Script/UI/War/Role/SOCheatCollider.cs` |
| `Assets/Script/UI/War/Role/SOCheatZiZiBeng.cs` |
| `Assets/Script/GamePlay/Client/Modules/AceSdk/AceSdkManagerClient.cs` |

## 备注

依赖：[[mode-base]]
