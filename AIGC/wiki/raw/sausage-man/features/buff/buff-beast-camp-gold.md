---
name: buff-beast-camp-gold
display_name: BSBeastCampGold - BeastCampGold
category: buff/beatbeast
version: 1.0.0
dependencies:
- buff-framework
---

# BSBeastCampGold - BeastCampGold

BSBeastCampGold Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBeastCampGold.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBeastCampGold.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBeastCampGoldClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBeastCampGoldServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/BeastCamp/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/BeastCamp/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
