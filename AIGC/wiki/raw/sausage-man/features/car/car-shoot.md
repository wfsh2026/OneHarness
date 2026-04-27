---
name: car-shoot
display_name: 载具射击系统
category: car/shoot
version: 1.1.0
dependencies:
- car-base
---

# 载具射击系统

载具射击功能：车载武器组件(CarShootComponent)、自动射击(CarAutoShootComponent)、驻车射击(CarStayShootComponent)、客户端射击管理、服务端校验(CarShootServerCheck)

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Car/CarShoot/CarShootComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShoot/CarShootClientMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShoot/CarAutoShootComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShoot/CarStayShootComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShoot/SOCarShootConfig.cs` |
| `Assets/Script/GamePlay/Server/Modules/Car/CarShootServerCheck.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/AbsCarShootBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/AbsCarShootClientMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/SORobotShoot.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Misc/SORobotShoot.asset [机甲车射击 SO 配置]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/UGUI/Sprite/War/CarShootImg.png [车载武器 UI 图标]` |
| `Assets/ToBundle/UGUI/Sprite/Weapon/CarShoot.png [车载射击准星图标]` |

## 备注

载具射击是部分载具（如机甲车 CyberTitan、GutsWing）的扩展功能。不是所有载具都有射击能力

依赖：[[car-base]]
