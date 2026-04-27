---
name: buff-add-effect-obj
display_name: BSAddEffectObj - 加载特效物体（最常用的特效 Buff 基类）
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddEffectObj - 加载特效物体（最常用的特效 Buff 基类）

1代 Buff 系统 加载特效物体（最常用的特效 Buff 基类）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddEffectObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddEffectObj.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddEffectObjServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddEffectObjClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/` |

## 备注

routing: Server + Client. key_fields: EffectSign, ServerEffectSign, SubpackageGroupSign, PartData, LifeTime, IsFollowRole, IsBindRoleSkin, EndBuff.

依赖：[[buff-framework]]
