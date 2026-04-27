---
name: buff-ganda-burn
display_name: BSGandaBurn - GandaBurn
category: buff/ganda
version: 1.0.0
dependencies:
- buff-framework
---

# BSGandaBurn - GandaBurn

BSGandaBurn Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGandaBurn.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGandaBurn.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGandaBurnClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGandaBurnServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/LineMove/LineMove_GandaBurn.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOGandaBurn.asset` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
