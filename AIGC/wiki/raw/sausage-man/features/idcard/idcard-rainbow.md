---
name: idcard-rainbow
display_name: Rainbow身份卡 - 彩虹
category: idcard/rainbow
version: 1.0.0
dependencies:
- idcard-framework
---

# Rainbow身份卡 - 彩虹

彩虹身份卡，提供2个技能：云朵啵啵（RainbowCloud）投掷云朵炸弹造成范围伤害，彩虹桥（RainbowBridge）在两点之间架设可通行的彩虹桥。彩虹桥有专属BS客户端和服务端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRainbowBridgeClient.cs [彩虹桥客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRainbowBridgeServer.cs [彩虹桥服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSRainbowBridge.cs [彩虹桥SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Rainbow.prefab [身份卡预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/RainbowBridge.prefab [彩虹桥预制体]` |
| `Assets/ToBundle/Items/Stunt/Bomb/RainbowCloud.prefab [云朵预制体]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Rainbow/ [彩虹技能特效目录]` |

## 备注

SkillCardType=15. 技能1: RainbowCloud(云朵啵啵, CD 60s, 范围攻击). 技能2: RainbowBridge(彩虹桥, CD 60s, 架桥通行). routing: Server+Client(彩虹桥). 注意SkillCardType从10跳到15(11-14未使用)。

依赖：[[idcard-framework]]
