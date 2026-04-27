---
name: idcard-sungod
display_name: Sungod身份卡 - 太阳神
category: idcard/sungod
version: 1.0.0
dependencies:
- idcard-framework
---

# Sungod身份卡 - 太阳神

太阳神身份卡，提供2个技能：天火（SungodBurn）向目标区域投掷火球造成范围灼烧伤害，冲星（SungodFly）化身流星向前冲刺并造成撞击伤害。两技能主要通过BSO配置实现。

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Sungod.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOSungodSkill1.asset [天火BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOSungodSkill2.asset [冲星BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOSungodFlyRun.asset [冲星飞行BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BSOAssaultSungodBurn.asset [Assault天火BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_FireBallSungod.asset [客户端火球BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Client_FireBallGoldDashSungod.asset [GoldDash火球BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/DownHp_SungodSkill1Fire.asset [天火伤害BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/DownHp_GoldDashSungodSkillFire.asset [GoldDash天火伤害BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Sungod/ [太阳神技能特效目录]` |

## 备注

SkillCardType=20. 技能1: SungodBurn(天火, CD 60s, 火球AOE灼烧). 技能2: SungodFly(冲星, CD 120s, 流星冲刺). routing: 纯BSO配置. 无专属BS代码文件。BSO文件名为BSOSungodSkill1/2而非技能名。有Assault变体(BSOAssaultSungodBurn)和GoldDash变体。

依赖：[[idcard-framework]]
