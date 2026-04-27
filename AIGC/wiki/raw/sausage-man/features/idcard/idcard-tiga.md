---
name: idcard-tiga
display_name: Tiga身份卡 - 迪迦奥特曼
category: idcard/tiga
version: 1.0.0
dependencies:
- idcard-framework
---

# Tiga身份卡 - 迪迦奥特曼

迪迦奥特曼联动身份卡，提供2个技能：哉佩利敖光线（TigaZepellionRay）发射标志性光线攻击，迪迦之希望（TigaHope）进入强化状态。两技能均有C/S两端代码。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTigaZepellionRayClient.cs [光线客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTigaZepellionRayServer.cs [光线服务端逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTigaHopeClient.cs [希望客户端表现]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTigaHopeServer.cs [希望服务端逻辑]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSTigaZepellionRay.cs [光线SOSystem Host实现]` |
| `Assets/Script/UI/War/BuffControl/Buff/SOSystem/BSTigaHope.cs [希望SOSystem Host实现]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/IDCard_Tiga.prefab [身份卡预制体]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Tiga_ZepellionRay.asset [光线BSO配置]` |
| `Assets/ToBundle/ScriptableObject/Buff/Skills/Tiga_Hope.asset [希望BSO配置]` |

## 备注

无SkillCardType(联动卡). 奥特曼系列联动. 技能1: TigaZepellionRay(哉佩利敖光线). 技能2: TigaHope(迪迦之希望). routing: Server+Client(无Host端). 光线名来自迪迦奥特曼经典技能 Zepellion Ray。

依赖：[[idcard-framework]]
