---
name: car-robot
display_name: 机甲载具系统（CyberTitan / Robot）
category: car/robot
version: 1.1.0
dependencies:
- car-base
- car-shoot
- car-motor-family
---

# 机甲载具系统（CyberTitan / Robot）

机甲车(Machine_Carrier)及其变形形态(Machine_Robot)：包含机器人武器控制、变形动画控制器、独立网络同步(RobotNet)、机甲专属射击逻辑

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Car/RobotWeaponControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/RobotTransformAnimatorController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarRobotPressWeapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarRobotStopDash.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarTransform.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/RobotNet.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Vehicle/SORobotAttackConfig_CyberTitan.asset` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/Robot/` |
| `Assets/ToBundle/Effect/Carrier/CyberTitan/` |

## 备注

Machine_Carrier 可变形为 Machine_Robot。MoveType 中分别有 Carrier_Robot_Role(104) 和 Carrier_Robot_Car(105)。CyberTitan 是新一代机甲载具

依赖：[[car-base]] · [[car-shoot]] · [[car-motor-family]]
