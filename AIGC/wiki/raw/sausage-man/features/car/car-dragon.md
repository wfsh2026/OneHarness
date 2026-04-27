---
name: car-dragon
display_name: 飞龙载具
category: car/dragon
version: 1.0.0
dependencies:
- car-base
---

# 飞龙载具

飞龙(Dragon)使用独立的 DragonControl.cs 控制器（不继承 FlyVehicle 基类），拥有独立的网络同步(DragonNet.cs)和火焰攻击能力

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/Car/DragonControl.cs` | 飞龙客户端控制器 |
| `Assets/Script/GamePlay/Host/Modules/Car/DragonNet.cs` | 飞龙网络同步 |

## 备注

Dragon 不继承 FlyVehicle 基类，使用完全独立的控制器。依赖 car-base 而非 fly-vehicle

依赖：[[car-base]]
