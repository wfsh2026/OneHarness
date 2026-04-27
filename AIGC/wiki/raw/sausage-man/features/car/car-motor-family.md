---
name: car-motor-family
display_name: Motor 控制器载具家族
category: car/motor
version: 1.0.0
dependencies:
- car-base
---

# Motor 控制器载具家族

基于 MotorCarController 物理驱动的载具家族：HoverBoard(悬浮滑板)、PonyVehicle(小马载具)、Machine(机甲车)、NeptuneShark(海王鲨鱼)。共享 MotorCarSetting.cs 配置基类

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/MotorCarSetting.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/PonyVehicleAnim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/UFOSpeedLineAnimationRotationController.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Vehicle/HoverBoard_MotorCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/PonyVehicle_MotorCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/Machine_MotorCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/NeptuneShark_MotorCarSetting.asset` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/HoverBoard/` |
| `Assets/ToBundle/Effect/Carrier/PonyVehicle/` |
| `Assets/ToBundle/Effect/Carrier/UFO/` |
| `Assets/ToBundle/Effect/Carrier/Shark/` |

## 备注

MotorCarController 使用 Rigidbody 直接驱动，不依赖 WheelCollider。Machine_Carrier 可变形为 Machine_Robot（见 car-robot feature）。UFO 目录对应 HoverBoard 的特效

依赖：[[car-base]]
