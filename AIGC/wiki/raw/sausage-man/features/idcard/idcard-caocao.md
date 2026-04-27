---
name: idcard-caocao
display_name: CaoCao身份卡 - 曹操
category: idcard/caocao
version: 1.0.0
dependencies:
- idcard-framework
---

# CaoCao身份卡 - 曹操

曹操身份卡，提供2个技能：枭雄降临（CaoCaoArrival）传送到指定位置并产生冲击波，投掷盾兵（CaoCaoShieldPawn）投掷盾兵到前方阻挡敌人。两技能均通过BSO配置使用通用BS类。

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_CaoCao.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/CaoCaoShieldPawn.prefab [盾兵预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CaoCaoArrival.asset [枭雄降临BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/CaoCaoTransfer.asset [传送BSO配置]` |

## 备注

SkillCardType=6. 技能1: CaoCaoArrival(枭雄降临, CD 60s, 传送+冲击波). 技能2: CaoCaoShieldPawn(投掷盾兵, CD 60s, 投掷阻挡物). routing: 纯BSO配置. 无专属BS代码文件。传送机制通过CaoCaoTransfer BSO实现。

依赖：[[idcard-framework]]
