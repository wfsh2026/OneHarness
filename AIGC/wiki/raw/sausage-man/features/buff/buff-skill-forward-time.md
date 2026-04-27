---
name: buff-skill-forward-time
display_name: BSSkillForwardTime - 技能前置时间
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSSkillForwardTime - 技能前置时间

1代 Buff 系统 技能前置时间。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOSkillForwardTime.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSkillForwardTime.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSkillForwardTimeServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSkillForwardTimeClient.cs` |

## 备注

key_fields: skillSign, roleAnimatorNum, isWolfManPower, isNoobFishTouch. 继承自 BSRoleStateChange.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
