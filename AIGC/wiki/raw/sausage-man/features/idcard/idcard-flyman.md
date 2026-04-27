---
name: idcard-flyman
display_name: Flyman身份卡 - 飞行侠
category: idcard/flyman
version: 1.0.0
dependencies:
- idcard-framework
---

# Flyman身份卡 - 飞行侠

飞行侠身份卡，提供2个技能：烟雾装置（Flyman_Smoke）在脚下释放烟雾弹遮蔽视线，风之翼（Flyman_Fly）展开翅膀飞行一段距离。两技能均通过BSO配置使用通用BS类。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSFlymanFlyServer.cs [风之翼服务端逻辑]` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSFlymanSmokeServer.cs [烟雾装置服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSFlymanFly.cs [风之翼Host端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSFlymanSmoke.cs [烟雾装置Host端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Flyman.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Flyman_Smoke.asset [烟雾装置BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Flyman_Fly.asset [风之翼BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_Flyman_Fly.asset [BladeBall飞行BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/FlyMan/ [飞行侠技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Flyman_1/ [飞行侠技能特效目录(皮肤1)]` |

## 备注

SkillCardType=10. 技能1: Flyman_Smoke(烟雾装置, CD 60s, 视野遮蔽). 技能2: Flyman_Fly(风之翼, CD 60s, 飞行位移). routing: 纯BSO配置. 无专属BS代码文件。Server端有BSFlymanFlyServer.cs和BSFlymanSmokeServer.cs在RoleSkill模块。有Expand扩展版(FlymanFly_Expand)和BladeBall变体。

依赖：[[idcard-framework]]
