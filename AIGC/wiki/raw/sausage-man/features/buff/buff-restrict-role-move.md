---
name: buff-restrict-role-move
display_name: BSRestrictRoleMove - RestrictRoleMove
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSRestrictRoleMove - RestrictRoleMove

BSRestrictRoleMove Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORestrictRoleMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRestrictRoleMoveClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRestrictRoleMoveServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。

依赖：[[buff-framework]]
