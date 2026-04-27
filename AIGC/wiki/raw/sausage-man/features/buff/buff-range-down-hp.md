---
name: buff-range-down-hp
display_name: BSRangeDownHp - 范围持续伤害
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSRangeDownHp - 范围持续伤害

1代 Buff 系统 范围持续伤害。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORangeDownHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRangeDownHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRangeDownHpServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GomoraItem/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: AttackValue, RangeXZ, RangeY.

依赖：[[buff-framework]]
