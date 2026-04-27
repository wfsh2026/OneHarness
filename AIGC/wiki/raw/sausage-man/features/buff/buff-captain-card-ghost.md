---
name: buff-captain-card-ghost
display_name: BSCaptainCardGhost - 队长卡灵体
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSCaptainCardGhost - 队长卡灵体

1代 Buff 系统 队长卡灵体。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOCaptainCardGhost.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCaptainCardGhost.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCaptainCardGhostServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCaptainCardGhostClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/CaptainCardGhost/` |

## 备注

key_fields: ruler, JudgeHp, FinalHp, AddMoveSpeed, HeighDropSpeed, endEffect, lineRenderOffset, lineRenderEffect. 继承自 BSRoleStateChange.

依赖：[[buff-framework]]
