---
name: idcard-doctorwho
display_name: Doctorwho身份卡 - 博士
category: idcard/doctorwho
version: 1.0.0
dependencies:
- idcard-framework
---

# Doctorwho身份卡 - 博士

博士身份卡，提供2个技能：魔法射线（Doctorwhoskill1）发射连续射线攻击敌人，魔法虫洞（Doctorwhoskill2）在目标位置创建虫洞传送装置。两技能主要通过BSO配置实现。

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Doctorwho.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/Doctorwhoskill2.prefab [虫洞预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Doctorwhoskill1.asset [魔法射线BSO配置]` |

## 备注

SkillCardType=21. 技能1: Doctorwhoskill1(魔法射线, CD 120s, 连续射线). 技能2: Doctorwhoskill2(魔法虫洞, CD 60s, 传送装置). routing: 纯BSO配置. 无专属BS代码文件。有护盾相关BSO(DownHpObj_DoctorwhoShield/ShieldHpOverEffect)。虫洞有位移炸弹变体(Doctorwhoskill_ShiftDeviceBomb)。

依赖：[[idcard-framework]]
