---
name: buff-pve-totem-add-dmg-no-team-around
display_name: BSPveTotemAddDmgNoTeamAround - PveTotemAddDmgNoTeamAround
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveTotemAddDmgNoTeamAround - PveTotemAddDmgNoTeamAround

BSPveTotemAddDmgNoTeamAround Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveTotemAddDmgNoTeamAround.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveTotemAddDmgNoTeamAround.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveTotemAddDmgNoTeamAroundClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveTotemAddDmgNoTeamAroundServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。
[纯代码Buff] Totem机制实现层，SO配置由对应的BSOTotem*类管理，本Buff仅提供运行时逻辑。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
