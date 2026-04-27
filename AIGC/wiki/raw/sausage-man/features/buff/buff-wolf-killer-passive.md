---
name: buff-wolf-killer-passive
display_name: BSWolfKillerPassive - WolfKillerPassive
category: buff/wolfparty
version: 1.0.0
dependencies:
- buff-framework
---

# BSWolfKillerPassive - WolfKillerPassive

BSWolfKillerPassive Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOWolfKillerPassive.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSWolfKillerPassive.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSWolfKillerPassiveClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSWolfKillerPassiveServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/WolfKillerPassive/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
