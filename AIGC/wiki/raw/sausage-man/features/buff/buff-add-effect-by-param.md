---
name: buff-add-effect-by-param
display_name: BSAddEffectByParam - 参数化特效加载（从 buffSyncInfo JSON 反序列化 EffectSign）
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddEffectByParam - 参数化特效加载（从 buffSyncInfo JSON 反序列化 EffectSign）

1代 Buff 系统 参数化特效加载（从 buffSyncInfo JSON 反序列化 EffectSign）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddEffectByParam.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddEffectByParam.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddEffectByParamClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/` |

## 备注

routing: Client only. key_fields: EffectSign (from JSON).

依赖：[[buff-framework]]
