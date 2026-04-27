---
name: idcard-captaincard
display_name: CaptainCard身份卡 - 船长
category: idcard/captaincard
version: 1.0.0
dependencies:
- idcard-framework
---

# CaptainCard身份卡 - 船长

船长身份卡，提供2个技能：船长回血（CaptainCardHot）使用热力治疗回复自身和队友生命，船长英灵（CaptainCardGhost）召唤英灵协助战斗。两技能均有完整C/S/H三端BS代码，含额外Recovery子功能。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCaptainCardHotClient.cs [回血客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCaptainCardHotServer.cs [回血服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCaptainCardHot.cs [回血Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCaptainCardGhostClient.cs [英灵客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCaptainCardGhostServer.cs [英灵服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCaptainCardGhost.cs [英灵Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCaptainCardRecoveryClient.cs [恢复客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCaptainCardRecoveryServer.cs [恢复服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCaptainCardRecovery.cs [恢复Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_CaptainCard.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CaptainCardHot.asset [回血BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CaptainCardGhost.asset [英灵BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CaptainCardRecovery.asset [恢复BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/CaptainCard/ [船长技能特效目录]` |

## 备注

SkillCardType=22. 技能1: CaptainCardHot(船长回血, CD 60s, 热力治疗). 技能2: CaptainCardGhost(船长英灵, CD 120s, 召唤英灵). routing: Server+Client+Host(完整三端). 含3个子功能(Hot/Ghost/Recovery)共9个BS代码文件。有GoldDash变体(GoldDash_CaptainCardGhost)和失控变体(CaptainCardGhostOutContol)。

依赖：[[idcard-framework]]
