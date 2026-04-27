---
name: buff-kitty-radar
display_name: BSKittyRadar - KittyRadar
category: buff/kitty
version: 1.0.0
dependencies:
- buff-framework
---

# BSKittyRadar - KittyRadar

BSKittyRadar Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOKittyRadar.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSKittyRadar.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKittyRadarClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKittyRadarServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
