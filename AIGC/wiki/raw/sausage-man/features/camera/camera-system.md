---
name: camera-system
display_name: 镜头系统
category: camera
version: 1.0.0
dependencies:
  - role-base
  - network-framework
---

# 镜头系统

战场镜头控制全链路：CameraController 主控器(视距/旋转/锁定/陀螺仪/折叠屏/自由视角)、BattleRoleCameraComponent 角色镜头状态同步(Alpha透明/锁定目标/视角切换)、SOCameraUserData 配置(站立/射击/飞行/载具/技能多套镜头参数)、Proto_Camera 网络协议(CmdCameraMoveData/CmdSetLockCameraRole/CmdFreeLook)、PlayCameraEffect 镜头特效池、CameraHit 碰撞检测、CameraUtility 后处理(高斯模糊/截图)、CameraFovSettingData FOV 持久化设置

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/Camera/CameraController.cs` | 主镜头控制器 — 视距/旋转/锁定/陀螺仪/折叠屏/自由视角/武器镜头 |
| `Assets/Script/GamePlay/Client/Modules/Camera/CameraEffectControl.cs` | 动画驱动镜头效果 — Animator 状态控制/循环时间/清除 |
| `Assets/Script/GamePlay/Client/Modules/Camera/CameraMove_ATEvent.cs` | 自动化工具事件绑定 — ATEvent 镜头旋转回调 |
| `Assets/Script/GamePlay/Client/Modules/Camera/PlayCameraEffect.cs` | 镜头特效池 — 特效生命周期/自动清除/角色绑定/BladeBall 逻辑 |
| `Assets/Script/GamePlay/Client/Motion/CameraFollow.cs` | 简单跟随镜头 — target+offset 跟随(Legacy) |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleCameraComponent.cs` | 角色镜头状态组件 — Alpha 透明计算/锁定目标更新/视角切换 |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Camera.cs` | 角色镜头门面层 — CmdSetLockCameraRole/CameraState/死亡镜头 |
| `Assets/Script/UI/War/CameraHit.cs` | 镜头碰撞检测 — Rigidbody 驱动/OnTriggerStay/HitType.CanCamera |
| `Assets/Script/Utils/Camera/CameraUtility.cs` | 后处理工具 — 高斯模糊/Bloom/截图/RenderTexture 池 |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_Camera.cs` | 镜头网络协议 — CmdCameraMoveData/CmdLookCameraMoveData/CmdSetLockCameraRole/CmdFreeLook |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_CameraMoveData.cs` | 镜头移动数据结构 |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_Camera.cs` | Server 端镜头网络处理 |
| `Assets/Script/GamePlay/Server/Network/Base/Feature/NetworkServer_Camera_Base.cs` | Server 端镜头网络基类 |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_Camera.cs` | Client 端镜头网络处理 |
| `Assets/Script/GamePlay/Client/Network/Base/Feature/NetworkClient_Camera_Base.cs` | Client 端镜头网络基类 |
| `Assets/Script/GamePlay/Server/Modules/Role/RoleLogicServer_LockCamera.cs` | Server 端锁定镜头逻辑 |
| `Assets/Script/Config/CameraAlphaConfig.cs` | 墙壁透明配置 — wallRatio 配置加载 |
| `Assets/Script/Data/UserSettingData/Graphics/CameraFovSettingData.cs` | FOV 持久化设置 — 默认60/LocalSave 存取 |
| `Assets/Script/Controller/BirthIslandCameraMoveController.cs` | 出生岛镜头移动控制 |
| `Assets/Script/UI/War/BirthIsland/BirthIslandCameraMove.cs` | 出生岛镜头移动 UI |
| `Assets/Script/GamePlay/AutoWar/AutoWarData/CameraMoveAutoWar.cs` | 自动战斗镜头数据 |
| `Assets/Script/Utils/ComponentExtension/CameraExtension.cs` | Camera 扩展方法 |
| `Assets/Script/Utils/AlwaysLookAtCamera.cs` | 始终面向镜头组件 |
| `Assets/Script/Utils/SameCamera.cs` | 同步镜头工具 |

## 配置文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/UI/War/SOCameraUserData.cs` | 镜头参数 SO — 站立/射击/飞行/载具/技能多套参数(NoMoPoint/ShootPoint/UFO/Robot/Zeus/Hades 等) |
| `Assets/Script/Config/CameraAlphaConfig.cs` | 墙壁透明配置 — id→wallRatio 映射 |
| `Assets/Script/UI/War/SO/Mode/PveRogue/SOPveCameraTween.cs` | PVE 镜头 Tween 配置 |

## 备注

CameraController 是最大单文件之一(246KB)。镜头系统通过 SOCameraUserData 管理所有场景的镜头参数，包括站立持枪(NoMoPoint/ShootPoint)、载具(Robot/UFO/BUS)、技能(Zeus/Hades/Guanyu/Tiga 等身份卡专属镜头)。网络同步通过 Proto_Camera(API_ID=12) 实现旋转和锁定目标的同步。BattleRoleCameraComponent 通过 wallCameraAlpha 计算墙壁透明度实现穿墙可见。CameraFovSettingData 持久化 FOV 设置(默认60)

依赖：[[role-base]] · [[network-framework]]
