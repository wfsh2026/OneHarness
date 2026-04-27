---
name: buff-c4bomb
display_name: BSC4Bomb - C4定时炸弹
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSC4Bomb - C4定时炸弹

1代 Buff 系统 C4定时炸弹。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOC4Bomb.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSC4Bomb.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSC4BombServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSC4BombClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/C4Bomb/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: bombTime, defuseBombDistance.

依赖：[[buff-framework]]
