---
name: car-buggy-family
display_name: Buggy 控制器载具家族
category: car/buggy
version: 1.0.0
dependencies:
- car-base
---

# Buggy 控制器载具家族

基于 BuggyCarController 物理驱动的地面载具家族：Jeep(吉普)、Buggy(沙滩车)、ArmoredBus(装甲巴士)、JetCar(喷气车)、Kayak(皮划艇)。共享 BuggyCarSetting.cs 配置基类

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/BuggyCarSetting.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/JetCarJump.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Vehicle/Jeep_BuggyCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/Buggy_BuggyCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/ArmoredBus_BuggyCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/JetCar_BuggyCarSetting.asset` |
| `Assets/ToBundle/ScriptableObject/Vehicle/Kayak_BuggyCarSetting.asset` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/Jeep/` |
| `Assets/ToBundle/Effect/Carrier/Buggy/` |
| `Assets/ToBundle/Effect/Carrier/ArmoredBus/` |
| `Assets/ToBundle/Effect/Carrier/JetCar/` |

## 备注

BuggyCarController 使用 WheelCollider 驱动，适合轮式地面载具。Kayak 虽然是水上载具但也用 BuggyCarSetting

依赖：[[car-base]]
