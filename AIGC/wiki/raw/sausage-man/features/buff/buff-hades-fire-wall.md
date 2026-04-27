---
name: buff-hades-fire-wall
display_name: BSHadesFireWall - 冥界火墙地形检测
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSHadesFireWall - 冥界火墙地形检测

1代 Buff 系统 冥界火墙地形检测。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOHadesFireWall.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSHadesFireWall.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSHadesFireWallServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSHadesFireWallClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: checkNum, checkStartPoints, checkDistance, checkSegment, checkHeight, checkAccuracy等.

依赖：[[buff-framework]]
