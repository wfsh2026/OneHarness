---
name: idcard-zeus
display_name: Zeus身份卡 - 众神之王宙斯
category: idcard/zeus
version: 1.0.0
dependencies:
- idcard-framework
---

# Zeus身份卡 - 众神之王宙斯

众神之王宙斯身份卡，提供2个技能：雷电传送（LightningTransfer）瞬移到指定位置，神王降临（LightningBomb）在目标区域降下雷电AOE。LightningBomb有专属BS客户端和服务端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSLightningBombClient.cs [雷电轰炸客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSLightningBombServer.cs [雷电轰炸服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSLightningBomb.cs [雷电轰炸SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Zeus.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/LightningBomb.asset [雷电轰炸BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/LightningTransfer.asset [雷电传送BSO配置]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Zeus/ [宙斯技能特效目录]` |

## 备注

SkillCardType=3. 技能1: LightningTransfer(雷电传送, CD 60s, 瞬移). 技能2: LightningBomb(神王降临, CD 60s, 雷电AOE). routing: Server+Client(LightningBomb). LightningTransfer无专属BS类。无Host端专属代码。

依赖：[[idcard-framework]]
