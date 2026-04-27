---
name: idcard-kadura
display_name: Kadura身份卡 - 卡杜拉
category: idcard/kadura
version: 1.0.0
dependencies:
- idcard-framework
---

# Kadura身份卡 - 卡杜拉

卡杜拉身份卡，提供1个技能：卡杜拉之力（KaduraPower）进入强化状态提升战斗能力。有完整C/S/H三端BS代码实现。BSO配置在独立子目录(KaduraPower/)下。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKaduraPowerClient.cs [卡杜拉之力客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKaduraPowerServer.cs [卡杜拉之力服务端]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSKaduraPower.cs [卡杜拉之力Host端]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Kadura.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/KaduraPower/BSOKaduraPower.asset [卡杜拉之力BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Kadura/ [卡杜拉技能特效目录]` |

## 备注

无SkillCardType(未绑定标准映射). 技能: KaduraPower(卡杜拉之力, 强化状态). routing: Server+Client+Host(完整三端). 仅1个技能(非标准的2技能配置)。BSO在独立子目录Buff/KaduraPower/下而非Skills/。

依赖：[[idcard-framework]]
