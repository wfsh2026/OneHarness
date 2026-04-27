---
name: idcard-snowgirl
display_name: SnowGirl身份卡 - 雪妹
category: idcard/snowgirl
version: 1.0.0
dependencies:
- idcard-framework
---

# SnowGirl身份卡 - 雪妹

雪妹身份卡，提供2个技能：雪球（SnowGirlBall）投掷滚动增大的雪球击退敌人，雪人（SnowGirlSnowMan）在指定位置堆建雪人作为掩体。两技能均有专属BS客户端和服务端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSnowGirlBallClient.cs [雪球客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSnowGirlBallServer.cs [雪球服务端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSnowGirlSnowManClient.cs [雪人客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSnowGirlSnowManServer.cs [雪人服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSSnowGirlBall.cs [雪球SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSSnowGirlSnowMan.cs [雪人SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_SnowGirl.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/SnowGirlBall.prefab [雪球预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/SnowGirlSnowMan.asset [雪人BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_SnowGirlBall.asset [客户端雪球BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_Client_SnowGirlBall.asset [BladeBall雪球BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/SnowGirl/ [雪妹技能特效目录]` |

## 备注

SkillCardType=16. 技能1: SnowGirlBall(雪球, CD 60s, 滚动增大+击退). 技能2: SnowGirlSnowMan(雪人, CD 120s, 掩体). routing: Server+Client. 有Expand扩展版(SnowGirlSnowMan_Expand)和BladeBall变体。雪球有墨渍遮挡效果(SnowGirlInkOcclusion)。

依赖：[[idcard-framework]]
