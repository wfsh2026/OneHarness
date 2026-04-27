---
name: idcard-lvbu
display_name: LvBu身份卡 - 吕布
category: idcard/lvbu
version: 1.0.0
dependencies:
- idcard-framework
---

# LvBu身份卡 - 吕布

吕布身份卡，仅有道具资产注册和BSO配置文件，无任何专属BS代码实现。可能为未完成或已下线的身份卡。仅有LvBuBombCastPoint施法点配置。

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_LvBu.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/LvBuBombCastPoint.asset [施法点BSO配置]` |

## 备注

无SkillCardType(无技能映射). ⚠️ STUB/占位卡: 无任何BS代码文件实现，仅有ItemAsset注册和BSO配置(LvBuBombCastPoint)。可能为计划中但未完成的身份卡，或已下线。制作新身份卡时不建议参考此卡。

依赖：[[idcard-framework]]
