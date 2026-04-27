---
name: idcard-guanyu
display_name: GuanYu身份卡 - 关羽
category: idcard/guanyu
version: 1.0.0
dependencies:
- idcard-framework
---

# GuanYu身份卡 - 关羽

关羽身份卡，提供2个技能：无畏冲锋（GuanyuSprint）向前方冲刺并击退敌人，十方无敌（GuanyuSpin）原地旋转大刀攻击周围敌人。两个技能均有完整C/S/H三端BS代码实现。Host端代码位于SOSystem目录（非常规路径）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSGuanyuSprint.cs [冲锋Host端逻辑(SOSystem非常规路径)]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGuanyuSprintClient.cs [冲锋客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGuanyuSprintServer.cs [冲锋服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSGuanyuSpin.cs [旋转斩Host端逻辑(SOSystem非常规路径)]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGuanyuSpinClient.cs [旋转斩客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGuanyuSpinServer.cs [旋转斩服务端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_GuanYu.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/GuanyuSprint.asset [冲锋BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/GuanyuSpin.asset [旋转斩BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/GuanyuSprint_JumpMode.asset [冲锋JumpMode变体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/SkirmisherGuanyuSprint.asset [冲锋Skirmisher变体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_GuanyuSpin.asset [旋转斩BladeBall变体]` |
| `Assets/ToBundle/Effect/AbilitiesCards/GuanYu/ [默认皮肤技能特效(30+prefab: Skill1冲锋3阶段+Skill2旋转4阶段+HeadBuff)]` |
| `Assets/ToBundle/Effect/AbilitiesCards/GuanYu_1/ [皮肤1特效变体]` |
| `Assets/ToBundle/Effect/AbilitiesCards/GuanYu_2/ [皮肤2特效变体]` |
| `Assets/ToBundle/Effect/AbilitiesCards/PickupProp/Sfx_Item_IDCard_Guanyu.prefab [拾取特效]` |

## 备注

SkillCardType=5. 技能1: GuanyuSprint(无畏冲锋, CD 15s, 短CD位移+击退). 技能2: GuanyuSpin(十方无敌, CD 60s, 范围旋转攻击). routing: 完整C/S/H三端. ⚠️Host端BS代码在SOSystem非常规路径(UI/War/BuffControl/Buff/SOSystem/). 冲锋有JumpMode和Skirmisher变体, 旋转有BladeBall变体. 3套皮肤特效(默认+Skin1+Skin2).

依赖：[[idcard-framework]]
