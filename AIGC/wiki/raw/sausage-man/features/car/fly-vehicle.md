---
name: fly-vehicle
display_name: 飞行载具框架
category: car/fly
version: 2.0.0
dependencies:
- car-base
---

# 飞行载具框架

飞行载具基类(FlyVehicle)提供统一的飞行物理、操控和配置管理。具体飞行载具（翼龙/飞燕号/神龙/飞行扫帚/飞龙）各自拥有独立 feature

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/FlyVehicle.cs` | 飞行载具基类 |
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/FlyVehicleConfig.cs` | 飞行配置 |
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/FlyVehicleHash.cs` | 动画哈希 |
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/SORobotAttackConfig.cs` |

## 备注

FlyVehicle 基类定义飞行载具的通用物理和操控逻辑。具体实现在各独立 feature 中：car-dragon、car-peterosaur、car-gutswing、car-shenlong、car-flyingbroom

依赖：[[car-base]]
