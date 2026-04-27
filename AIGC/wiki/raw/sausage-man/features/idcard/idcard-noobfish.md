---
name: idcard-noobfish
display_name: NoobFish身份卡 - 咸鱼
category: idcard/noobfish
version: 1.0.0
dependencies:
- idcard-framework
---

# NoobFish身份卡 - 咸鱼

咸鱼身份卡，提供2个技能：摸鱼（NoobFishTouch）变身咸鱼隐蔽在地上，咸鱼摊（NoobFishBooth）放置一个咸鱼摊位回复生命值。是代码量最大的身份卡之一，两技能均有完整C/S/H三端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNoobFishTouchClient.cs [摸鱼客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNoobFishTouchServer.cs [摸鱼服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSNoobFishTouch.cs [摸鱼Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNoobFishRecoveryClient.cs [恢复客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNoobFishRecoveryServer.cs [恢复服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSNoobFishRecovery.cs [恢复Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNoobFishBoothClient.cs [咸鱼摊客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNoobFishBoothServer.cs [咸鱼摊服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSNoobFishBooth.cs [咸鱼摊Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNoobFishBoothCreateClient.cs [摊位创建客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNoobFishBoothCreateServer.cs [摊位创建服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSNoobFishBoothCreate.cs [摊位创建Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_NoobFish.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishTouch.asset [摸鱼BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishBooth.asset [咸鱼摊BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishBoothCreate.asset [摊位创建BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishRecovery.asset [恢复BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishSpeed.asset [速度BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/NoobFish/BSONoobFishTouchForward.asset [摸鱼前摇BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/NoobFish/ [咸鱼技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/NoobFish_1/ [咸鱼技能特效目录(皮肤1)]` |

## 备注

SkillCardType=18. 技能1: NoobFishTouch(摸鱼, CD 60s, 变身隐蔽). 技能2: NoobFishBooth(咸鱼摊, CD 60s, 放置回血摊位). routing: Server+Client+Host(完整三端). 是BS代码文件最多的身份卡(12个.cs)，含4个子功能: Touch/Recovery/Booth/BoothCreate。有专属BSO子目录(Buff/NoobFish/)。

依赖：[[idcard-framework]]

## 关联 Buff


### 诺比鱼 Buff（4）

| feature | 说明 |
|---------|------|
| [[buff-noob-fish-booth]] | BSNoobFishBooth - NoobFishBooth |
| [[buff-noob-fish-booth-create]] | BSNoobFishBoothCreate - NoobFishBoothCreate |
| [[buff-noob-fish-recovery]] | BSNoobFishRecovery - NoobFishRecovery |
| [[buff-noob-fish-touch]] | BSNoobFishTouch - NoobFishTouch |
