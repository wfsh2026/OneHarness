---
name: idcard-zeta
display_name: Zeta身份卡 - 泽塔奥特曼
category: idcard/zeta
version: 1.0.0
dependencies:
- idcard-framework
---

# Zeta身份卡 - 泽塔奥特曼

泽塔奥特曼联动身份卡，提供1-2个技能：泽塔闪烁（ZetaBlink）瞬间位移闪现到目标位置。Blink有完整C/S/H三端RoleSkill代码。BSO配置含Shot附加技能。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSZetaBlinkClient.cs [闪烁客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSZetaBlinkServer.cs [闪烁服务端逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSZetaBlink.cs [闪烁Host端逻辑]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Zeta.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Zeta_Blink.asset [闪烁BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Zeta_Shot.asset [射击BSO配置]` |
| `Assets/ToBundle/Items/Stunt/Bomb/Zeta_Blink.prefab [闪烁投掷物预制体]` |

## 备注

无SkillCardType(联动卡). 奥特曼系列联动. 技能: ZetaBlink(泽塔闪烁, 瞬移). routing: Server+Client+Host(完整三端, RoleSkill模块). BSO含Zeta_Blink和Zeta_Shot两个配置。是奥特曼联动卡中唯一有完整三端代码的。

依赖：[[idcard-framework]]
