---
name: buff-gd-entry-group-double-edged-sword
display_name: BSGdEntryGroupDoubleEdgedSword - GdEntryGroupDoubleEdgedSword
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGdEntryGroupDoubleEdgedSword - GdEntryGroupDoubleEdgedSword

BSGdEntryGroupDoubleEdgedSword Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGdEntryGroupDoubleEdgedSword.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGdEntryGroupDoubleEdgedSword.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGdEntryGroupDoubleEdgedSwordClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGdEntryGroupDoubleEdgedSwordServer.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
