---
name: idcard-kitty
display_name: Kitty身份卡 - 猫猫
category: idcard/kitty
version: 1.0.0
dependencies:
- idcard-framework
---

# Kitty身份卡 - 猫猫

猫猫身份卡，提供2个技能：猫猫跳（KittyJump）高跳起后落地冲击，猫猫看（KittyRadar）扫描并标记周围敌人位置。两技能均有完整C/S/H三端BS代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKittyJumpClient.cs [猫跳客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKittyJumpServer.cs [猫跳服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSKittyJump.cs [猫跳Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKittyRadarClient.cs [雷达客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKittyRadarServer.cs [雷达服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSKittyRadar.cs [雷达Host端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Kitty.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/KittyJump.asset [猫跳BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/KittyRadar.asset [雷达BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/AssaultKittyJump.asset [Assault猫跳BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_KittyJump.asset [BladeBall猫跳BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/ReconKittyRadar.asset [Recon雷达BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Kitty/ [猫猫技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/KittyOption/ [猫猫可选特效目录]` |

## 备注

SkillCardType=19. 技能1: KittyJump(猫猫跳, CD 10s, 超短CD高跳+落地冲击). 技能2: KittyRadar(猫猫看, CD 120s, 敌人侦测标记). routing: Server+Client+Host(完整三端). 猫跳CD仅10秒，是全部身份卡中最短CD。有Assault/BladeBall/Recon多种模式变体。

依赖：[[idcard-framework]]

## 关联 Buff


### Kitty Buff（2）

| feature | 说明 |
|---------|------|
| [[buff-kitty-jump]] | BSKittyJump - KittyJump |
| [[buff-kitty-radar]] | BSKittyRadar - KittyRadar |
