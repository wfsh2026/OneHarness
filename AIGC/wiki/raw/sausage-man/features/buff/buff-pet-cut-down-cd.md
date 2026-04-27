---
name: buff-pet-cut-down-cd
display_name: BSPetCutDownCd - 宠物冷却缩减Client
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSPetCutDownCd - 宠物冷却缩减Client

1代 Buff 系统 宠物冷却缩减Client。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPetCutDownCd.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPetCutDownCd.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPetCutDownCdClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/` |

## 备注

key_fields: EffectName, HumanEffectName, EffectDurationTime, bodyPartData, HumanEffectOffset.

依赖：[[buff-framework]]
