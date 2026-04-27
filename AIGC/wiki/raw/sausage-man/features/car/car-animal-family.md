---
name: car-animal-family
display_name: 动物坐骑载具家族
category: car/animal
version: 1.0.0
dependencies:
- car-base
---

# 动物坐骑载具家族

基于 AnimalCarSetting 的动物坐骑家族：Raptors(恐龙)、SwordTiger(剑齿虎)、TRexKing(霸王龙)、Triceratops(三角龙)。独立的动物动画驱动和骑乘逻辑

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/AnimalCarSetting.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/SOTrexking.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Vehicle/Raptors_AnimalCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/SwordTiger_AnimalCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/TRexKing_AnimalCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/Triceratops_AnimalCarSetting.asset` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/SwordTiger/` |
| `Assets/ToBundle/Effect/Carrier/TreasureCar/` |

## 备注

GoldDash 模式也有独立的 AnimalCarSetting 配置（GolddashAnimalCarSetting），但那属于 GoldDash 模式的 feature

依赖：[[car-base]]
