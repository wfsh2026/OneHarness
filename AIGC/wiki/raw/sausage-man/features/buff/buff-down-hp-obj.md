---
name: buff-down-hp-obj
display_name: BSDownHpObj - 可破坏物体
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSDownHpObj - 可破坏物体

1代 Buff 系统 可破坏物体。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODownHpObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDownHpObj.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDownHpObjServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDownHpObjClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/DownHpObj/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: MaxHp, ReLifeTime, HPOverBuff[], weaponHitRatio. 继承自 IBuffDownHp.

依赖：[[buff-framework]]
