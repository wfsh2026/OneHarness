---
name: car-golddash
display_name: GoldDash 模式载具配置
category: car/golddash
version: 1.0.0
dependencies:
- car-base
---

# GoldDash 模式载具配置

GoldDash（黄金乱斗）模式的专属载具配置：独立的 AnimalCar/MotorCar/RoleCar 三套 Setting 配置、GolddashCSV2Config 配置转换

## 代码文件

| 路径 |
|------|
| `Assets/Script/Biubiubiu2/Template/client/GolddashAnimalCarSetting.cs` |
| `Assets/Script/Biubiubiu2/Template/client/GolddashMotorCarSetting.cs` |
| `Assets/Script/Biubiubiu2/Template/client/GolddashRoleCarSetting.cs` |
| `Assets/Script/Config/GolddashAnimalCarSettingConfig.cs` |
| `Assets/Script/Config/GolddashMotorCarSettingConfig.cs` |
| `Assets/Script/Config/GolddashRoleCarSettingConfig.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/GolddashCSV2Config.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/GolddashAnimalCarSetting.txt` |
| `Assets/ToBundle/Config/Txt/GolddashMotorCarSetting.txt` |
| `Assets/ToBundle/Config/Txt/GolddashRoleCarSetting.txt` |
| `Assets/ToBundle/Config/Txt/GolddashCarData.txt` |
| `Assets/ToBundle/Config/Txt/GolddashCarType.txt` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |

## 备注

GoldDash 模式有独立于主游戏的载具配置体系。3 种 Setting 分别对应动物坐骑、机动载具、角色变身三种载具类型。[纯配置覆盖] 视觉资产通过 car-base 依赖共享，无独立美术资源

依赖：[[car-base]]
