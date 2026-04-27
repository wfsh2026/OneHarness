---
name: buff-wolf-killer-auto-aim
display_name: BSWolfKillerAutoAim - WolfKillerAutoAim
category: buff/wolfparty
version: 1.0.0
dependencies:
- buff-framework
---

# BSWolfKillerAutoAim - WolfKillerAutoAim

BSWolfKillerAutoAim Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOWolfKillerAutoAim.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSWolfKillerAutoAim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSWolfKillerAutoAimClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSWolfKillerAutoAimServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/WolfKillerAutoAim/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
