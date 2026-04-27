---
name: idcard-hades
display_name: Hades身份卡 - 冥王哈迪斯
category: idcard/hades
version: 1.0.0
dependencies:
- idcard-framework
---

# Hades身份卡 - 冥王哈迪斯

冥王哈迪斯身份卡，提供2个技能：冥火墙（HadesFireWall）在地面释放一道火墙造成伤害，冥王潜行（HadesHiding）进入隐身状态。火墙技能有专属BS三端代码实现，潜行技能通过BSO配置使用通用BS类。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSHadesFireWallClient.cs [冥火墙客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSHadesFireWallServer.cs [冥火墙服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSHadesFireWall.cs [冥火墙Host端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Hades.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/Hades_Skill1.prefab [技能1投射物]` |
| `Assets/ToBundle/Items/Stunt/Bomb/HadesFireBall.prefab [火球投射物]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/HadesFireWall.asset [冥火墙BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/HadesHiding.asset [冥王潜行BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CreateHadesFireWall.asset [火墙创建BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_HadesHiding.asset [BladeBall潜行BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CreateHadesFireWall_GoldDash.asset [GoldDash火墙BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/GoldDash_HadesFireWall.asset [GoldDash模式火墙BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_HadesFireBall.asset [客户端火球BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/SkirmisherHadesHiding.asset [先锋模式潜行BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Hades/ [冥王技能特效目录]` |

## 备注

SkillCardType=1. 技能1: HadesFireWall(冥火墙, CD 60s, 地面火墙AOE). 技能2: HadesHiding(冥王潜行, CD 60s, 隐身). routing: Server+Client. 火墙有GoldDash变体(CreateHadesFireWall_GoldDash/SkirmisherHadesHiding). HadesHiding无专属BS类，使用通用BladeBall配置。

依赖：[[idcard-framework]]
