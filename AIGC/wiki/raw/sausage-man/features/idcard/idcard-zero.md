---
name: idcard-zero
display_name: Zero身份卡 - 赛罗奥特曼
category: idcard/zero
version: 1.0.0
dependencies:
- idcard-framework
---

# Zero身份卡 - 赛罗奥特曼

赛罗奥特曼联动身份卡，提供1-2个技能：艾梅利姆光线（ZeroEmerium）发射赛罗标志性光线攻击。Emerium有C/S两端RoleSkill代码。BSO配置含Wideshot附加技能。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSZeroEmeriumClient.cs [光线客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSZeroEmeriumServer.cs [光线服务端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Zero.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Zero_Emerium.asset [光线BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Zero_Wideshot.asset [广域射击BSO配置]` |

## 备注

无SkillCardType(联动卡). 奥特曼系列联动. 技能: ZeroEmerium(艾梅利姆光线). routing: Server+Client(RoleSkill模块, 无Host端). BSO含Zero_Emerium和Zero_Wideshot两个配置。艾梅利姆光线是赛罗奥特曼经典技能 Emerium Slash。

依赖：[[idcard-framework]]
