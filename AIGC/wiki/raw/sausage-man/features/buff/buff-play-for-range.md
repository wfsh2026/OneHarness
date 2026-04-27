---
name: buff-play-for-range
display_name: BSPlayForRange - 范围触发器（支持凸多边形区域）
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSPlayForRange - 范围触发器（支持凸多边形区域）

1代 Buff 系统 范围触发器（支持凸多边形区域）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPlayForRange.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPlayForRange.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPlayForRangeServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPlayForRangeClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PlayForRange/` |

## 备注

routing: GameLoop. key_fields: Range, TeamBuffEffect[], EnemyBuffEffect[], vertexArray, vertexHeightRange, myCheckType.

依赖：[[buff-framework]]
