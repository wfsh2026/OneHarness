---
name: idcard-geed
display_name: Geed身份卡 - 捷德奥特曼
category: idcard/geed
version: 1.0.0
dependencies:
- idcard-framework
---

# Geed身份卡 - 捷德奥特曼

捷德奥特曼联动身份卡，提供跳跃技能（GeedJump）。仅有客户端RoleSkill模块代码，服务端和Host端无专属实现。BSO配置含Jump和Shot两个技能。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSGeedJumpClient.cs [捷德跳跃客户端表现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSGeedJump.cs [捷德跳跃SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Geed.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Geed_Jump.asset [跳跃BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Geed_Shot.asset [射击BSO配置]` |

## 备注

无SkillCardType(联动卡). 奥特曼系列联动. 技能: GeedJump(跳跃). routing: Client only(RoleSkill). 仅客户端有专属代码(BSGeedJumpClient)，服务端/Host端缺失。BSO含Geed_Jump和Geed_Shot两个配置。

依赖：[[idcard-framework]]
