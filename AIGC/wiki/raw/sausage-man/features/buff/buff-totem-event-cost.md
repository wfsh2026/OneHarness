---
name: buff-totem-event-cost
display_name: BSTotemEventCost - TotemEventCost
category: buff/totem
version: 1.0.0
dependencies:
- buff-framework
---

# BSTotemEventCost - TotemEventCost

BSTotemEventCost Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTotemEventCost.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTotemEventCost.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTotemEventCostClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTotemEventCostServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。
[纯代码Buff] Totem机制实现层，SO配置由对应的BSOTotem*类管理，本Buff仅提供运行时逻辑。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
