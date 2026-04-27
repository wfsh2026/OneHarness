---
name: buff-magic-treasure-down-hp
display_name: BSMagicTreasureDownHp - MagicTreasureDownHp
category: buff/magic
version: 1.0.0
dependencies:
- buff-framework
---

# BSMagicTreasureDownHp - MagicTreasureDownHp

BSMagicTreasureDownHp Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOMagicTreasureDownHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSMagicTreasureDownHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMagicTreasureDownHpClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMagicTreasureDownHpServer.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
