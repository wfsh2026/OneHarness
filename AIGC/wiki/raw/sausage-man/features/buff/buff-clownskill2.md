---
name: buff-clownskill2
display_name: BSClownskill2 - Clownskill2
category: buff/role-skill
version: 1.0.0
dependencies:
- buff-framework
---

# BSClownskill2 - Clownskill2

BSClownskill2 Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClownskill2.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2Client.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2Server.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Clownskill2/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
