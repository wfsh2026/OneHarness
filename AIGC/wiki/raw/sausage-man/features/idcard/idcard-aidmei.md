---
name: idcard-aidmei
display_name: AidMei身份卡 - 医疗兵
category: idcard/aidmei
version: 1.0.0
dependencies:
- idcard-framework
---

# AidMei身份卡 - 医疗兵

医疗兵身份卡，提供2个技能：治疗机器人（AidMeiHealingBot）投掷治疗机器人持续回血，复活队友（AidMei_Stage）对倒地队友进行快速复活。Stage技能有专属BS客户端和服务端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAidMeiStageClient.cs [复活队友客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAidMeiStageServer.cs [复活队友服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSAidMeiHealingBot.cs [治疗机器人SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSAidMeiStage.cs [复活队友SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSAidMeiSecondStage.cs [复活二阶段SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_AidMei.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/AidMeiHealingBot.prefab [治疗机器人预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/SupperAidMeiHealingBot.prefab [强化治疗机器人]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_AidMeiHealingBot.asset [客户端治疗机器人BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_AidMeiSecondState.asset [客户端二阶段BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_AidMeiStage.asset [客户端复活BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_GoldDashAidMeiHealingBot.asset [GoldDash治疗BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/AidMei/ [医疗兵技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/AidMei_1/ [医疗兵技能特效目录(皮肤1)]` |

## 备注

SkillCardType=8. 技能1: AidMeiHealingBot(治疗机器人, CD 60s, 投掷回血). 技能2: AidMei_Stage(复活队友, CD 120s, 快速复活). routing: Server+Client(Stage). 治疗机器人有强化版(Supper)和GoldDash变体。有皮肤变体(AidMeiHealingBot_Skin1)。HealingBot有Expand扩展版本。

依赖：[[idcard-framework]]
