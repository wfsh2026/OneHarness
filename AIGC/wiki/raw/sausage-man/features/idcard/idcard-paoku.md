---
name: idcard-paoku
display_name: PaoKu身份卡 - 跑酷小子
category: idcard/paoku
version: 1.0.0
dependencies:
- idcard-framework
---

# PaoKu身份卡 - 跑酷小子

跑酷小子身份卡，提供2个技能：一飞冲天（PaoKuFlyAir）向上飞冲后滑翔，牛气滚滚（PaoKuRoll）变成球体滚动碾压敌人。两技能均有专属BS客户端和服务端代码，飞冲有两阶段实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuFlyAirOneStageClient.cs [飞冲第一阶段客户端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuFlyAirSecondStageClient.cs [飞冲第二阶段客户端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuRollClient.cs [牛气滚滚客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuFlyAirOneStageServer.cs [飞冲第一阶段服务端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuFlyAirSecondStageServer.cs [飞冲第二阶段服务端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuRollServer.cs [牛气滚滚服务端]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSPaoKuFlyAirOneStage.cs [飞冲一阶段SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSPaoKuFlyAirSecondStage.cs [飞冲二阶段SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSPaoKuRoll.cs [滚动SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_PaoKu.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/PaoKuFlyAir.asset [飞冲BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/PaoKuFlyAirSecondStage.asset [飞冲第二阶段BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/PaoKuRoll.asset [滚动BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/PaoKu/ [跑酷小子技能特效目录]` |

## 备注

SkillCardType=9. 技能1: PaoKuFlyAir(一飞冲天, CD 90s, 两阶段: 上升+滑翔). 技能2: PaoKuRoll(牛气滚滚, CD 60s, 球体滚动). routing: Server+Client. 飞冲技能分OneStage(起飞)和SecondStage(滑翔)两阶段实现。无Host端专属代码。

依赖：[[idcard-framework]]
