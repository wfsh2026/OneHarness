---
name: buff-clownskill2-area-effect
display_name: BSClownskill2AreaEffect - Clownskill2AreaEffect
category: buff/role-skill
version: 1.0.0
dependencies:
- buff-framework
---

# BSClownskill2AreaEffect - Clownskill2AreaEffect

BSClownskill2AreaEffect Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClownskill2AreaEffect.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2AreaEffect.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2AreaEffectClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2AreaEffectServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Clownskill2/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
