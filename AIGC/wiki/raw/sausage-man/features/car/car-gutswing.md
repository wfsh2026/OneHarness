---
name: car-gutswing
display_name: 胜利飞燕号载具
category: car/gutswing
version: 1.0.0
dependencies:
- fly-vehicle
---

# 胜利飞燕号载具

飞燕号(GutsWing)继承 FlyVehicle 基类的飞行载具，拥有蓄力弹和炸弹攻击能力

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/GutsWing.cs` | 飞燕号控制器（继承 FlyVehicle） |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Vehicle/GutsWing.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/GutsWingShoot.asset` |

## 备注

GutsWing 继承 FlyVehicle，拥有独立的射击配置(GutsWingShoot.asset)，支持蓄力弹和炸弹两种攻击方式

依赖：[[fly-vehicle]]
