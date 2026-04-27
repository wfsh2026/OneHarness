---
name: role-uprear
display_name: 角色扶人救援系统
category: role/uprear
version: 1.0.0
dependencies:
- role-base
- role-death
---

# 角色扶人救援系统

扶起/救援逻辑（扶起状态管理、救援 CD、队友互救）

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicUprearComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Uprear.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_UprearRole.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleUprearRoleComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_Uprear.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/RoleUprearEffect.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Rescue/ [16 files, 扶人救援特效 — Besties/Bromance/CP/Partner 四种亲密度等级各含 Low/Mid/Option 三档画质]` |

## 备注

扶人系统与虚弱（Weak）状态紧密配合。当角色进入虚弱倒地状态后，队友可通过扶人机制救援。RoleLogicUprearComponent 管理扶起逻辑状态和 CD，BattleRoleUprearRoleComponent 管理 BattleRole 层扶人表现，RoleLogicServer_Uprear 处理服务端权威扶人判定

依赖：[[role-base]] · [[role-death]]
