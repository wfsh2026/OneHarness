---
name: idcard-taiga
display_name: Taiga身份卡 - 泰迦奥特曼
category: idcard/taiga
version: 1.0.0
dependencies:
- idcard-framework
---

# Taiga身份卡 - 泰迦奥特曼

泰迦奥特曼联动身份卡，提供3个技能：泰迦护盾（TaigaShield）释放防护护盾，泰迦炸弹（TaigaBomb）投掷炸弹攻击，炸弹施法点（TaigaBombCastPoint）标记投弹位置。三技能均有C/S两端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaShieldClient.cs [护盾客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaShieldServer.cs [护盾服务端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaBombClient.cs [炸弹客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaBombServer.cs [炸弹服务端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaBombCastPointClient.cs [施法点客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaBombCastPointServer.cs [施法点服务端]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSTaigaShield.cs [护盾SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSTaigaBomb.cs [炸弹SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSTaigaBombCastPoint.cs [施法点SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Taiga.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/TaigaShield.asset [护盾BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/TaigaBomb.asset [炸弹BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/TaigaBombCastPoint.asset [施法点BSO配置]` |

## 备注

无SkillCardType(联动卡). 奥特曼系列联动. 3个技能: TaigaShield(护盾)/TaigaBomb(炸弹)/TaigaBombCastPoint(施法点). routing: Server+Client(无Host端). 含3个子功能共6个BS代码文件。

依赖：[[idcard-framework]]
