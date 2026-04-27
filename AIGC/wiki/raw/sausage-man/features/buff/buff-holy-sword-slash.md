---
name: buff-holy-sword-slash
display_name: BSHolySwordSlash - HolySwordSlash
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSHolySwordSlash - HolySwordSlash

BSHolySwordSlash Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOHolySwordSlash.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSHolySwordSlash.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSHolySwordSlashClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSHolySwordSlashServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/AddEffect_HolySwordSlash.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/HolySword/HolySwordSlash.asset` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
