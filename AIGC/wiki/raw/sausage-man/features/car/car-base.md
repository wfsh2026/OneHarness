---
name: car-base
display_name: 载具系统基础框架
category: car
version: 1.1.0
dependencies: []
---

# 载具系统基础框架

1代载具系统公共组件：物理驱动(MotorCarController/BuggyCarController)、主控(Car.cs)、网络同步(CarNet)、上下车交互(CarShift)、Component组件架构、操作UI、碰撞管理

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Car/Car.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarNetClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShift.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShiftLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarPlace.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarGetOffPos.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarDiverBox.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarOcclusion.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarSpolied.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarCheckHit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CollisionObjectManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/SwipControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarSystemBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/ICarSystem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/ICarComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarComponentBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarMovementComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarAudioComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarEffectComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarPassengerComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarSkillComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarTransformComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/Components/CarEvents.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarPointSpeedAnim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarRotaSpeedAnim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarSpeedAnim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarShowHideSpeedAnim.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarOperateWin.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/CarOperateWin_ATEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/UICarButtonCD.cs` |
| `Assets/Script/GamePlay/Client/Modules/Car/UICarDownCD.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/CarNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/CarNetMirror.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/CarNetSyncMirror.cs` |
| `Assets/Script/GamePlay/Host/Modules/Car/SoCarPlaceData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Car/CarNetServer.cs` |
| `Assets/Script/3rd/RCC/MotorCarController.cs` |
| `Assets/Script/3rd/RCC/BuggyCarController.cs` |
| `Assets/Script/3rd/RCC/Plugin/ICarController.cs` |
| `Assets/Script/3rd/RCC/Plugin/RCCCarController.cs` |
| `Assets/Script/UI/PlayerControl/Control/VehicleStateButtonControl.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/SOCreateObjData/` |
| `Assets/ToBundle/ScriptableObject/Vehicle/` |
| `Assets/Script/Config/SOCarDataConfig.cs` |
| `Assets/Script/Config/SOCarDataConfig_Wrap.cs` |
| `Assets/Script/Config/SOCarSkinDataConfig.cs` |
| `Assets/Script/Config/SOCarSkillConfig.cs` |
| `Assets/Script/Config/CarItemAssetConfig.cs` |
| `Assets/Script/Config/CarSkinHConfig.cs` |
| `Assets/ToBundle/Config/Txt/SOCarData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SOCarSkill.txt` |
| `Assets/ToBundle/Config/Txt/CarItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/CarSkinH.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientCarFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientCarOwnerFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientCarSpoiledFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerCarOwnerFeatureManager.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Carrier/Common/` |

## 备注

MotorCarController.cs 和 BuggyCarController.cs 是物理核心，禁止修改。CarShift.cs 仅通过配置调参。CarNet.cs 是网络基类，影响所有载具。新增载具流程见 [[载具制作]]
