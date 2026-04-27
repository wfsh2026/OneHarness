---
name: buff-ganda-fly
display_name: BSGandaFly - GandaFly
category: buff/ganda
version: 1.0.0
dependencies:
- buff-framework
---

# BSGandaFly - GandaFly

BSGandaFly Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGandaFly.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGandaFly.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGandaFlyClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGandaFlyServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
