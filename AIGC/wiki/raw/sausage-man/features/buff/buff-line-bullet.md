---
name: buff-line-bullet
display_name: BSLineBullet - 直线连线伤害
category: buff/combat
version: 1.0.0
dependencies:
- buff-framework
---

# BSLineBullet - 直线连线伤害

1代 Buff 系统 直线连线伤害。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOLineBullet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSLineBullet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSLineBulletServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSLineBulletClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/LineBullet/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

key_fields: damage[], radius, checkMaxNum.

依赖：[[buff-framework]]
