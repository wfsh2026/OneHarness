---
name: buff-beast-game-box-down-hp
display_name: BSBeastGameBoxDownHp - BeastGameBoxDownHp
category: buff/beatbeast
version: 1.0.0
dependencies:
- buff-framework
---

# BSBeastGameBoxDownHp - BeastGameBoxDownHp

BSBeastGameBoxDownHp Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBeastGameBoxDownHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBeastGameBoxDownHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBeastGameBoxDownHpClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBeastGameBoxDownHpServer.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/BeastCamp/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
