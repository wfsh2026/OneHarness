---
name: idcard-neptune
display_name: Neptune身份卡 - 海神波塞冬
category: idcard/neptune
version: 1.0.0
dependencies:
- idcard-framework
---

# Neptune身份卡 - 海神波塞冬

海神波塞冬身份卡，提供2个技能：防护罩（NeptuneShield）创建一个可移动的能量护盾，鲨鱼载具（NeptuneShark）召唤鲨鱼载具。两个技能均通过BSO配置使用通用BS类（LineMove/AddEffect），无专属BS代码文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSNeptuneShield.cs [防护罩SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Neptune.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/NeptuneShield.prefab [防护罩预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/NeptuneWaterBall.prefab [水球预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/SupperNeptuneShield.prefab [强化防护罩]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/NeptuneShield.asset [防护罩BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/NeptuneShark.asset [鲨鱼载具BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/GoldDashNeptuneShield.asset [GoldDash防护罩BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Neptune/ [海神技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Neptune_1/ [海神技能特效目录(皮肤1)]` |

## 备注

SkillCardType=2. 技能1: NeptuneShield(防护罩, CD 90s, 可移动能量盾). 技能2: NeptuneShark(鲨鱼载具, CD 60s, 召唤鲨鱼). routing: 纯BSO配置. 无专属BS代码文件，两技能均通过通用LineMove/AddEffect类实现。有GoldDash变体(GoldDashNeptuneShield)和强化版(SupperNeptuneShield)。

依赖：[[idcard-framework]]
