---
name: ai-spawner
display_name: AI 生成管理系统
category: ai/spawner
version: 1.0.0
dependencies:
- ai-base
---

# AI 生成管理系统

AI 角色生成/销毁生命周期管理：通用生成器(CommonAISpawner)含 6 种 Query 查询系统(Combat/Item/SpawnPoint/SafeZone/Poi/Vehicle)，模式专属生成器(Normal/GoldDash/PartyMode)，生成规则校验(RuleCheck)，数量/点位/死亡管理

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAISpawner/ClientRoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/AbsServerRoleAiSpawnerManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAICombatQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAIItemQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAIPlayerDeliveryState.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAIPoiQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAISafeZoneQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAISpawnPointQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAISpawnService.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonAISpawner/CommonAIVehicleQuery.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/CommonServerRoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/GoldDash/ServerGoldDashRoleAISpawnerAddMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/GoldDash/ServerGoldDashRoleAISpawnerPointMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/GoldDash/ServerGoldDashTeamModeRoleAISpawner.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/ServerRoleAIPartyModeSpawnerMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/ServerRoleAISpawnerAddMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/ServerRoleAISpawnerDeadMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/ServerRoleAISpawnerNumMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/Features/ServerRoleAISpawnerPointMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/RoleAISpawnerData.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/RoleAISpawnerRuleCheck.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/ServerGoldDashRoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAISpawner/ServerNormalRoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/IRoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/IRoleAISpawnerMgrFeature.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/RoleAIMgrSpawnerFeatureList.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/RoleAISpawnerManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAISpawner/RoleAISpawnerMgrFeature.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/ContainerPos.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/RoleAI/ServerData/GoldDashAIBehavior/ [8 files, GoldDash 模式 AI 行为配置]` |
| `Assets/ToBundle/RoleAI/ServerData/GoldDashTeamAIBeahavior/ [1 file]` |
| `Assets/ToBundle/RoleAI/ServerData/PartyModeRoleAIBehavior/ [1 file]` |
| `Assets/ToBundle/RoleAI/ServerData/Prefabs/ [1 file]` |

## 备注

生成系统以服务端为权威（22 文件），客户端仅 1 个 Manager。核心模式：CommonAISpawner 提供 6 种 Query 对象（战斗/物品/出生点/安全区/POI/载具查询），Features 管理生成数量/点位/死亡处理。GoldDash 和 PartyMode 有独立的生成策略

依赖：[[ai-base]]
