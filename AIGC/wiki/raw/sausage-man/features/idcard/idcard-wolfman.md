---
name: idcard-wolfman
display_name: WolfMan身份卡 - 狼王
category: idcard/wolfman
version: 1.0.0
dependencies:
- idcard-framework
---

# WolfMan身份卡 - 狼王

狼王身份卡，提供2个技能：狼王跳跃（WolfManJump）高跳起后落地冲击，狼王力量（WolfManPower）进入强化状态提升近战能力。特殊卡：有RoleSkill模块服务端代码，BladeBall模式有独立三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBladeBallWolfManJumpClient.cs [BladeBall跳跃客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBladeBallWolfManJumpServer.cs [BladeBall跳跃服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBladeBallWolfManJump.cs [BladeBall跳跃Host端]` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSWolfManPowerServer.cs [狼王力量服务端逻辑]` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSWolfHowlServer.cs [狼王嚎叫服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSWolfManPower.cs [狼王力量SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSWolfHowl.cs [狼王嚎叫SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSWolfTransfrom.cs [狼王变身SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_WolfMan.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfManJump.asset [跳跃BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfManPower.asset [力量BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfManPowerForward.asset [力量前摇BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/BladeBall_WolfManJump.asset [BladeBall狼跳BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl.asset [狼王嚎叫BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfManPowerForward_Expand.asset [力量前摇扩展BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl_malou.asset [麻六嚎叫BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl_wukong.asset [悟空嚎叫BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl_wukongS.asset [悟空S嚎叫BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl_yangjian.asset [杨戬嚎叫BSO]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/WolfHowl_yangjianS.asset [杨戬S嚎叫BSO]` |
| `Assets/ToBundle/Effect/AbilitiesCards/WolfMan/ [狼王技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/WolfMan_1/ [狼王技能特效目录(皮肤1)]` |

## 备注

无SkillCardType(特殊卡，未绑定标准映射). 技能1: WolfManJump(狼王跳跃, 高跳+落地冲击). 技能2: WolfManPower(狼王力量, 近战强化). routing: Server(RoleSkill)+BladeBall(三端)+SOSystem(Host). 特殊之处: 跳跃技能仅BladeBall模式有三端BS代码，力量技能Server端在RoleSkill模块、Host端在SOSystem(BSWolfManPower/BSWolfHowl/BSWolfTransfrom)。有Expand扩展版(WolfManPowerForward_Expand)和WolfHowl嚎叫技能(含malou/wukong/wukongS/yangjian/yangjianS皮肤变体)。

依赖：[[idcard-framework]]

## 关联 Buff


### 狼人 Buff（4）

| feature | 说明 |
|---------|------|
| [[buff-wolf-hide]] | BSWolfHide - WolfHide |
| [[buff-wolf-killer-auto-aim]] | BSWolfKillerAutoAim - WolfKillerAutoAim |
| [[buff-wolf-killer-passive]] | BSWolfKillerPassive - WolfKillerPassive |
| [[buff-wolf-smoke]] | BSWolfSmoke - WolfSmoke |
