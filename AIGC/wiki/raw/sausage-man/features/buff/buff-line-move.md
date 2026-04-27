---
name: buff-line-move
display_name: BSLineMove - 直线移动投射物
category: buff/movement
version: 1.0.0
dependencies:
- buff-framework
---

# BSLineMove - 直线移动投射物

1代 Buff 系统 直线移动投射物。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOLineMove.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSLineMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSLineMoveServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSLineMoveClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/LineMove/` |

## 备注

key_fields: FirstSpeed, DownSpeed, IsHitEnd, EndBuff, BallSize. 继承自 IBuffDownHpServer.

依赖：[[buff-framework]]
