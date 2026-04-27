---
name: ai-navigation
display_name: AI 导航与 ML 系统
category: ai/navigation
version: 1.0.0
dependencies:
- ai-base
---

# AI 导航与 ML 系统

AI 寻路与机器学习导航：NavMesh 加载/管理、NavAgent 配置工厂、射线检测配置、MLAgent 集成(IMLAgent 接口)、小地图导航(TinyMapMLAgent)、客户端 PathFinder 路径规划

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/AreaInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/ClientRoleAIMLAgent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/ClientRoleAITinyMapMLAgent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/DirectResult.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/IMLAgent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/IRoleAIMLAgent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/NavAgentConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/NavAgentConfigFactory.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/RayCastVisualizer.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/RayLayerConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/MLAgent/ServerRoleAITeamMapMLAgent.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ClientRoleAIPathFinder.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/NavMeshLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAILogic/ForbidNavMeshCollider.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIManager/ClientRoleAINavMeshMgr.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/RoleAI/ServerData/MLAgent/ [5 files, ML 模型/配置资产]` |

## 备注

导航系统分两层：(1) 传统 NavMesh 寻路 — NavMeshLoader 加载地图导航网格，ClientRoleAIPathFinder 计算路径；(2) ML-Agent 增强导航 — IMLAgent 接口支持机器学习辅助决策。项目使用 Unity.ML-Agents 包(com.unity.ml-agents)

依赖：[[ai-base]]
