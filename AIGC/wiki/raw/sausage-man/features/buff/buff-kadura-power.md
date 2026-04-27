---
name: buff-kadura-power
display_name: BSKaduraPower - KaduraPower
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSKaduraPower - KaduraPower

BSKaduraPower Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOKaduraPower.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSKaduraPower.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKaduraPowerClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKaduraPowerServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/KaduraPower/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
