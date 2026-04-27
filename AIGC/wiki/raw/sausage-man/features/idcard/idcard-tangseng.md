---
name: idcard-tangseng
display_name: TangSeng身份卡 - 唐僧
category: idcard/tangseng
version: 1.0.0
dependencies:
- idcard-framework
---

# TangSeng身份卡 - 唐僧

唐僧身份卡，提供2个技能：紧箍咒（TangSengSpell）对范围内敌人施加减速控制，道法自然（TangSengGunFire）发射法术弹幕攻击。两技能均有完整C/S/H三端BS代码，含SpellRange范围检测子功能。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTangSengSpellClient.cs [紧箍咒客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTangSengSpellServer.cs [紧箍咒服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTangSengSpell.cs [紧箍咒Host端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTangSengSpellRangeClient.cs [范围检测客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTangSengSpellRangeServer.cs [范围检测服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTangSengSpellRange.cs [范围检测Host端]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTangSengGunFireClient.cs [法术弹幕客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTangSengGunFireServer.cs [法术弹幕服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTangSengGunFire.cs [法术弹幕Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_TangSeng.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/TangSengSpell.asset [紧箍咒BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/TangSengGunFire.asset [法术弹幕BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/TangSeng/ [唐僧技能特效目录]` |

## 备注

SkillCardType=24. 技能1: TangSengSpell(紧箍咒, CD 60s, 范围减速控制). 技能2: TangSengGunFire(道法自然, CD 120s, 法术弹幕). routing: Server+Client+Host(完整三端). 含3个子功能(Spell/SpellRange/GunFire)共9个BS代码文件。有伤害物体变体(DownHpObj_TangSengSpell)。

依赖：[[idcard-framework]]

## 关联 Buff


### 唐僧 Buff（3）

| feature | 说明 |
|---------|------|
| [[buff-tang-seng-gun-fire]] | BSTangSengGunFire - TangSengGunFire |
| [[buff-tang-seng-spell]] | BSTangSengSpell - TangSengSpell |
| [[buff-tang-seng-spell-range]] | BSTangSengSpellRange - TangSengSpellRange |
