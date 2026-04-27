---
name: idcard-zhugeliang
display_name: ZhuGeLiang身份卡 - 诸葛亮
category: idcard/zhugeliang
version: 1.0.0
dependencies:
- idcard-framework
---

# ZhuGeLiang身份卡 - 诸葛亮

诸葛亮身份卡，提供2个技能：箭塔（ZhuGeLiangArrowTowers）在指定位置放置自动攻击的箭塔，八卦阵（ZhuGeLiangBaGuaZhen）创建一个减速/困敌的阵法区域。两技能均通过BSO配置使用通用BS类。

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_ZhuGeLiang.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/ZhuGeLiangArrowTowers.prefab [箭塔预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/ZhuGeLiangArrowTowers.asset [箭塔BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/ZhuGeLiangBaGuaZhen.asset [八卦阵BSO配置]` |

## 备注

SkillCardType=4. 技能1: ZhuGeLiangArrowTowers(箭塔, CD 60s, 放置自动攻击箭塔). 技能2: ZhuGeLiangBaGuaZhen(八卦阵, CD 120s, 区域控制). routing: 纯BSO配置. 无专属BS代码文件。有GoldDash变体(AddEffect_GoldDashZhuGeLiangBaGuaStart)。

依赖：[[idcard-framework]]
