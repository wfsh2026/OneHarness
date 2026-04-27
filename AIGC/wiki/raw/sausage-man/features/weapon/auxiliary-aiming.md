---
name: auxiliary-aiming
display_name: 辅助瞄准系统（AuxiliaryAiming）
category: system/aiming
version: 1.0.0
dependencies:
  - role-base
---

# 辅助瞄准系统（AuxiliaryAiming）

辅助瞄准系统：灵敏度控制、自动追踪、辅助瞄准状态机。纯客户端。共 27 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Asset/Loaders/AuxiliaryAimingLoader.cs` |
| `Assets/Script/Data/SOAuxiliaryAimingData.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Adsorb/AdsorbControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceAppearState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceInAdsorbState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceInBoxState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceOutBoxState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceStateBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AutoTrace/AutoTraceState/AutoTraceStopState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AuxiliaryAimingHit.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/AuxiliaryAimingUtil.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Editor/AdsorbControlEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Editor/AutoTraceControlEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Editor/AuxiliaryAimingEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Editor/SensitivityControlEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Helper/AdsorbHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Helper/AdsorbLookAtHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Lib/IState.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Lib/StateBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Lib/StateMachine.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/RoleAuxiliaryAimingControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Sensitivity/SensitivityControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/IRoleLogicAuxiliaryAiming.cs` |
| `Assets/Script/GamePlay/Client/Motion/IRoleLogicClientAuxiliaryAiming.cs` |
| `Assets/Script/GamePlay/Client/Motion/RoleAIAuxiliaryAimingMono.cs` |
| `Assets/Script/GamePlay/Client/Motion/RoleAuxiliaryAimingMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Resources/CubeBox.prefab` |
| `Assets/Script/GamePlay/Client/Modules/AuxiliaryAiming/Resources/Sphere.prefab` |

## 备注

依赖：[[role-base]]
