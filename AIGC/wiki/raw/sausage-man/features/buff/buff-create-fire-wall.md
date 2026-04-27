---
name: buff-create-fire-wall
display_name: BSCreateFireWall - 创建火墙
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSCreateFireWall - 创建火墙

1代 Buff 系统 创建火墙。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOCreateFireWall.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCreateFireWall.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCreateFireWallServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCreateFireWallClient.cs` |

## 备注

key_fields: lifeTime, fireWallPrefabName, fireWallHeight, fireWallWidth, createTime, clearTime, damageCheck等.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
