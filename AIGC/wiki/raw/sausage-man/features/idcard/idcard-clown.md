---
name: idcard-clown
display_name: Clown身份卡 - 小丑
category: idcard/clown
version: 1.0.0
dependencies:
- idcard-framework
---

# Clown身份卡 - 小丑

小丑身份卡，提供2个技能：小丑炸弹（ClownGrenade）投掷爆炸炸弹，小丑领域（Clownskill2）创建一个持续影响区域。是BS代码文件最多的身份卡之一，含5个子功能完整C/S/H三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2Client.cs [小丑领域客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2Server.cs [小丑领域服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2.cs [小丑领域Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2FallBallClient.cs [落球客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2FallBallServer.cs [落球服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2FallBall.cs [落球Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2AreaEffectClient.cs [区域特效客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2AreaEffectServer.cs [区域特效服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2AreaEffect.cs [区域特效Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2AreaSpeedUpClient.cs [区域加速客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2AreaSpeedUpServer.cs [区域加速服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2AreaSpeedUp.cs [区域加速Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownPlatformClient.cs [平台客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownPlatformServer.cs [平台服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownPlatform.cs [平台Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Clown.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/ClownGrenade.prefab [小丑炸弹预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/Clownskill2.prefab [领域预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/ClownGrenade.asset [炸弹BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Clownskill2AreaEffect.asset [区域特效BSO]` |
| `Assets/ToBundle/Items/Stunt/Bomb/AssaultClownGrenade.prefab [Assault小丑炸弹]` |
| `Assets/ToBundle/Items/Stunt/Bomb/ClownGrenade_BeastCamp.prefab [野兽阵营小丑炸弹]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Clown/ [小丑技能特效目录]` |

## 备注

SkillCardType=23. 技能1: ClownGrenade(小丑炸弹, CD 20s, 短CD投掷爆炸). 技能2: Clownskill2(小丑领域, CD 100s, 持续区域效果). routing: Server+Client+Host(完整三端). 含5个子功能(Skill2/FallBall/AreaEffect/AreaSpeedUp/Platform)共15个BS代码文件，是代码量最大的身份卡。有Assault/BeastCamp/ClassicMode多种模式变体。

依赖：[[idcard-framework]]

## 关联 Buff


### 角色技能 Buff（4）

| feature | 说明 |
|---------|------|
| [[buff-clownskill2]] | BSClownskill2 - Clownskill2 |
| [[buff-clownskill2-area-effect]] | BSClownskill2AreaEffect - Clownskill2AreaEffect |
| [[buff-clownskill2-area-speed-up]] | BSClownskill2AreaSpeedUp - Clownskill2AreaSpeedUp |
| [[buff-clownskill2-fall-ball]] | BSClownskill2FallBall - Clownskill2FallBall |
