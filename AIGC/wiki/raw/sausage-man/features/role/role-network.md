---
name: role-network
display_name: 角色网络同步系统
category: role/network
version: 1.0.0
dependencies:
- role-base
---

# 角色网络同步系统

RoleNet 三端网络框架、Mirror 同步、重连处理、状态同步

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNetData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNetMirror.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNetSyncMirror.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_States.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_UNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_BladeBallMode.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_GoldDash.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleNet_Knockout.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Network.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_DownHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_AI.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_GetPower.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_ReLogin.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleNetServer_Knockout.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleNetClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleNetClient_ATEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_NetCheck.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Reconnect.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicReconnectComponent.cs` |

## 备注

RoleNet 是 Host 层网络框架（Mirror 同步），RoleNetServer 处理服务端 Cmd 校验，RoleLogicClient_NetCheck 处理客户端网络状态检查。两种消息机制：Proto（protobuf）+ RPC（Mirror），重连由 ReconnectComponent 管理。RoleNet 有多个模式扩展 partial（BladeBall/GoldDash/Knockout）

依赖：[[role-base]]
