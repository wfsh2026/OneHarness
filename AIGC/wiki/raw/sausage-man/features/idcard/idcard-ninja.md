---
name: idcard-ninja
display_name: Ninja身份卡 - 忍者
category: idcard/ninja
version: 1.0.0
dependencies:
- idcard-framework
---

# Ninja身份卡 - 忍者

忍者身份卡，提供2个技能：忍者抓钩（NinjaHookFly）发射钩索飞向目标点，影分身（NinjaShadowCopy）在原地留下分身吸引敌人注意。影分身有专属BS客户端和服务端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNinjaShadowCopyClient.cs [影分身客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNinjaShadowCopyServer.cs [影分身服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSNinjaShadowCopy.cs [影分身SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Ninja.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/NinjaHookFly.prefab [钩索预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/NinjaShadowCopy.asset [影分身BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Ninja/ [忍者技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Ninja_1/ [忍者技能特效目录(皮肤1)]` |

## 备注

SkillCardType=7. 技能1: NinjaHookFly(忍者抓钩, CD 15s, 钩索位移). 技能2: NinjaShadowCopy(影分身, CD 45s, 分身诱饵). routing: Server+Client(影分身). 抓钩CD仅15秒。有皮肤变体(NinjaHookFly_Skin1)。

依赖：[[idcard-framework]]
