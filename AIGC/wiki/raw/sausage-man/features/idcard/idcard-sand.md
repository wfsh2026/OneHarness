---
name: idcard-sand
display_name: Sand身份卡 - 沙之精灵
category: idcard/sand
version: 1.0.0
dependencies:
- idcard-framework
---

# Sand身份卡 - 沙之精灵

沙之精灵身份卡，提供1个技能：沙之平台（SandPlatform）在空中创建可站立的沙之平台。有完整C/S/H三端BS代码实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSandPlatformClient.cs [沙平台客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSandPlatformServer.cs [沙平台服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSandPlatform.cs [沙平台Host端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSSandCastleLineMove.cs [沙堡移动SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Sand.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/SandPlatform.asset [沙平台BSO配置]` |
| `Assets/ToBundle/Items/Stunt/Bomb/SandCastle.prefab [沙堡投掷物]` |
| `Assets/ToBundle/Items/Stunt/Bomb/SandGrenade.prefab [沙之手雷]` |
| `Assets/ToBundle/Effect/AbilitiesCards/Sand/ [沙之精灵技能特效目录]` |
| `Assets/ToBundle/Effect/AbilitiesCards/SneakSand/ [潜沙技能特效目录]` |

## 备注

无SkillCardType(未绑定标准映射). 技能: SandPlatform(沙之平台, 创建空中平台). routing: Server+Client+Host(完整三端). 仅1个技能。功能类似建筑/掩体系统。

依赖：[[idcard-framework]]
