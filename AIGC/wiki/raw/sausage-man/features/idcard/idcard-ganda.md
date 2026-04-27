---
name: idcard-ganda
display_name: Ganda身份卡 - 甘达
category: idcard/ganda
version: 1.0.0
dependencies:
- idcard-framework
---

# Ganda身份卡 - 甘达

甘达身份卡，提供3个技能：甘达灼烧（GandaBurn）对敌人施加灼烧伤害，甘达飞行（GandaFly）飞行位移，甘达飞行冲刺（GandaFlyRun）飞行中的冲刺加速。三技能均有完整C/S/H三端BS代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGandaBurnClient.cs [灼烧客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGandaBurnServer.cs [灼烧服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGandaBurn.cs [灼烧Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGandaFlyClient.cs [飞行客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGandaFlyServer.cs [飞行服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGandaFly.cs [飞行Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGandaFlyRunClient.cs [飞行冲刺客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGandaFlyRunServer.cs [飞行冲刺服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGandaFlyRun.cs [飞行冲刺Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Ganda.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOGandaFly.asset [飞行BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOGandaBurn.asset [灼烧BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOGandaFlyRun.asset [飞行冲刺BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Ganda/ [甘达技能特效目录]` |

## 备注

无SkillCardType(未绑定标准映射). 3个技能: GandaBurn(灼烧)/GandaFly(飞行)/GandaFlyRun(飞行冲刺). routing: Server+Client+Host(完整三端). 含3个子功能共9个BS代码文件。注意: 有3个技能而非标准的2个。

依赖：[[idcard-framework]]

## 关联 Buff


### 盖亚 Buff（3）

| feature | 说明 |
|---------|------|
| [[buff-ganda-burn]] | BSGandaBurn - GandaBurn |
| [[buff-ganda-fly]] | BSGandaFly - GandaFly |
| [[buff-ganda-fly-run]] | BSGandaFlyRun - GandaFlyRun |
