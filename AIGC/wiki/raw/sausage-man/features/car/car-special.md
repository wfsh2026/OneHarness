---
name: car-special
display_name: 特殊载具标记与标签
category: car/special
version: 1.1.0
dependencies:
- car-base
---

# 特殊载具标记与标签

载具特殊标记组件：AirShipRoomTag(飞船房间标记)、AlienWarshipTag(外星战舰标记)、FlyingCarpet(飞毯)、CircusBall(马戏球)。用于特定玩法或场景的载具标记

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Car/AirShipRoomTag.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/AlienWarshipTag.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/FlyingCarpet.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/AlienWarShip/` |
| `Assets/ToBundle/Effect/Carrier/CircusBall/` |

## 备注

AlienWarship 对应 MoveType.Carrier_AlienWarship(106)。CircusBall(161 prefabs) 是马戏球系列载具特效

依赖：[[car-base]]
