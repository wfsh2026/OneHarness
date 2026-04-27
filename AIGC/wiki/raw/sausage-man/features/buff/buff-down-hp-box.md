---
name: buff-down-hp-box
display_name: BSDownHpBox - 陷阱箱伤害
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSDownHpBox - 陷阱箱伤害

1代 Buff 系统 陷阱箱伤害。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODownHpBox.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDownHpBox.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDownHpBoxServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDownHpBoxClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/AddEffect_BeastDownHpBox.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/CreateBuff/CreateBuff_BeastDownHpBox.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/DownHpObj/DownHpObj_BeastDownHpBox.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/OnlyUp/BSODownHpBox.asset` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: lockingRange, TrapEffectData[].

依赖：[[buff-framework]]
