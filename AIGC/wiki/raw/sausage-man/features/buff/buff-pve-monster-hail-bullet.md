---
name: buff-pve-monster-hail-bullet
display_name: BSPveMonsterHailBullet - PveMonsterHailBullet
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveMonsterHailBullet - PveMonsterHailBullet

BSPveMonsterHailBullet Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveMonsterHailBullet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveMonsterHailBullet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveMonsterHailBulletClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveMonsterHailBulletServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveMonsterMelee/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
