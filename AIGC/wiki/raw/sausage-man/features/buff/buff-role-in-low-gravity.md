---
name: buff-role-in-low-gravity
display_name: BSRoleInLowGravity - RoleInLowGravity
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSRoleInLowGravity - RoleInLowGravity

BSRoleInLowGravity Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORoleInLowGravity.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 1 个文件。
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
