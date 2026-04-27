---
name: role-motion
display_name: 角色动画状态机与 Motion 系统
category: role/motion
version: 1.0.0
dependencies:
- role-base
- role-animation
- role-animator
---

# 角色动画状态机与 Motion 系统

动画状态机全部 State 实现（移动/跳跃/坠落/射击/换弹/投掷/近战/游泳/飞行/载具等），武器动画片段管理，皮肤骨骼合并，布娃娃控制，角色材质切换，Anim-Opt 优化工具

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Motion/MoveState.cs` |
| `Assets/Script/GamePlay/Client/Motion/FallState.cs` |
| `Assets/Script/GamePlay/Client/Motion/FallLandState.cs` |
| `Assets/Script/GamePlay/Client/Motion/FallIntoSwimState.cs` |
| `Assets/Script/GamePlay/Client/Motion/JumpInAirState.cs` |
| `Assets/Script/GamePlay/Client/Motion/JumpLandState.cs` |
| `Assets/Script/GamePlay/Client/Motion/FlyJumpState.cs` |
| `Assets/Script/GamePlay/Client/Motion/ShootingState.cs` |
| `Assets/Script/GamePlay/Client/Motion/ReloadState.cs` |
| `Assets/Script/GamePlay/Client/Motion/ReloadAutoState.cs` |
| `Assets/Script/GamePlay/Client/Motion/OpenState.cs` |
| `Assets/Script/GamePlay/Client/Motion/CloseState.cs` |
| `Assets/Script/GamePlay/Client/Motion/EjectState.cs` |
| `Assets/Script/GamePlay/Client/Motion/AimingState.cs` |
| `Assets/Script/GamePlay/Client/Motion/NoAimingState.cs` |
| `Assets/Script/GamePlay/Client/Motion/AimSwing.cs` |
| `Assets/Script/GamePlay/Client/Motion/ChangeWeaponState.cs` |
| `Assets/Script/GamePlay/Client/Motion/PullWeaponState.cs` |
| `Assets/Script/GamePlay/Client/Motion/PutbackWeaponState.cs` |
| `Assets/Script/GamePlay/Client/Motion/EmptyHandState.cs` |
| `Assets/Script/GamePlay/Client/Motion/ThrowGrenadeState.cs` |
| `Assets/Script/GamePlay/Client/Motion/MeleeAttackState.cs` |
| `Assets/Script/GamePlay/Client/Motion/MeleeFinishedState.cs` |
| `Assets/Script/GamePlay/Client/Motion/HoldMeleeState.cs` |
| `Assets/Script/GamePlay/Client/Motion/HoldDemonMacheteState.cs` |
| `Assets/Script/GamePlay/Client/Motion/ToggleStanceState.cs` |
| `Assets/Script/GamePlay/Client/Motion/PickUpState.cs` |
| `Assets/Script/GamePlay/Client/Motion/OpenParachuteState.cs` |
| `Assets/Script/GamePlay/Client/Motion/SwimTramsState.cs` |
| `Assets/Script/GamePlay/Client/Motion/SneakSandState.cs` |
| `Assets/Script/GamePlay/Client/Motion/PaokuRollState.cs` |
| `Assets/Script/GamePlay/Client/Motion/CheckRandomIdleState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponAnimationClips.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponAnimationClipsEditor.cs` |
| `Assets/Script/GamePlay/Client/Motion/DefaultWeaponAnimClips.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponSelfAimationClisp.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponShootState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponReloadState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponReloadAutoState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponOpenState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponCloseState.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeaponEjectState.cs` |
| `Assets/Script/GamePlay/Client/Motion/FollowWeaponController.cs` |
| `Assets/Script/GamePlay/Client/Motion/SkinManager.cs` |
| `Assets/Script/GamePlay/Client/Motion/SkinManagerXCC.cs` |
| `Assets/Script/GamePlay/Client/Motion/SkinBoneManager.cs` |
| `Assets/Script/GamePlay/Client/Motion/SkinnedMeshCombiner.cs` |
| `Assets/Script/GamePlay/Client/Motion/FashionPartHide.cs` |
| `Assets/Script/GamePlay/Client/Motion/FashionEffectCondition.cs` |
| `Assets/Script/GamePlay/Client/Motion/SlideEffectSkin.cs` |
| `Assets/Script/GamePlay/Client/Motion/CharacterAnimOverride.cs` |
| `Assets/Script/GamePlay/Client/Motion/RagdollControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/RoleMatChangeMgr.cs` |
| `Assets/Script/GamePlay/Client/Motion/CameraFollow.cs` |
| `Assets/Script/GamePlay/Client/Motion/MarkComponent.cs` |
| `Assets/Script/GamePlay/Client/Motion/SausageController.cs` |
| `Assets/Script/GamePlay/Client/Motion/BulletCaseSpawner.cs` |
| `Assets/Script/GamePlay/Client/Motion/CarStateEffect.cs` |
| `Assets/Script/GamePlay/Client/Motion/WeakAnimIK.cs` |
| `Assets/Script/GamePlay/Client/Motion/CustomRoleModel.cs` |
| `Assets/Script/GamePlay/Client/Motion/DinosaurAnimationEffect.cs` |
| `Assets/Script/GamePlay/Client/Motion/DinosaurSkin.cs` |
| `Assets/Script/GamePlay/Client/Motion/CircusBallSkin.cs` |
| `Assets/Script/GamePlay/Client/Motion/CircusBallStateAnim.cs` |
| `Assets/Script/GamePlay/Client/Motion/GandaFlyAnimEvent.cs` |
| `Assets/Script/GamePlay/Client/Motion/GandaFlyAnimState.cs` |
| `Assets/Script/GamePlay/Client/Motion/GandaFlyAnimStatePrep.cs` |
| `Assets/Script/GamePlay/Client/Motion/GandaFlyAnimStateTumble01.cs` |
| `Assets/Script/GamePlay/Client/Motion/GuanyuSpinState.cs` |
| `Assets/Script/GamePlay/Client/Motion/SlimeNianEvent.cs` |
| `Assets/Script/GamePlay/Client/Motion/SnowGirlSnowManState.cs` |
| `Assets/Script/GamePlay/Client/Motion/XiaoChangChangAnim.cs` |
| `Assets/Script/GamePlay/Client/Motion/XiaoChangChangAnimEvent.cs` |
| `Assets/Script/GamePlay/Client/Motion/AIXiaoChangChangAnim.cs` |
| `Assets/Script/GamePlay/Client/Motion/BeRatRoleModelAnimCtrl.cs` |
| `Assets/Script/GamePlay/Client/Motion/RoleAIAuxiliaryAimingMono.cs` |
| `Assets/Script/GamePlay/Client/Motion/RoleAuxiliaryAimingMono.cs` |
| `Assets/Script/GamePlay/Client/Motion/FollowCarWheelLR.cs` |
| `Assets/Script/GamePlay/Client/Motion/Recorder.cs` |
| `Assets/Script/GamePlay/Client/Motion/AnimTestControl.cs` |
| `Assets/Script/GamePlay/Client/Motion/AutomaticWeaponTester.cs` |
| `Assets/Script/GamePlay/Client/Motion/FashionTester.cs` |
| `Assets/Script/GamePlay/Client/Motion/RifleTest.cs` |
| `Assets/Script/GamePlay/Client/Motion/CharAnimTestController.cs` |
| `Assets/Script/GamePlay/Client/Motion/Anim-Opt/AnimatorControllerAnalyzer.cs` |
| `Assets/Script/GamePlay/Client/Motion/Anim-Opt/AnimatorControllerUpdater.cs` |
| `Assets/Script/GamePlay/Client/Motion/Anim-Opt/WeaponEnum.cs` |
| `Assets/Script/GamePlay/Client/Motion/Anim-Opt/Editor/AnimatorControllerGenerateDataSO.cs` |
| `Assets/Script/GamePlay/Client/Motion/Anim-Opt/Editor/AnimtorControllerGenerators.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/RoleSitType.txt` |
| `Assets/ToBundle/Config/Txt/RoleCheckOperate.txt` |

## 备注

Motion 模块是角色 3C 动画表现层的核心：(1) *State.cs 定义动画状态机各状态的进入/更新/退出逻辑；(2) WeaponAnimationClips 管理武器动画片段映射；(3) SkinManager/SkinBoneManager 处理皮肤骨骼合并和换装表现；(4) RagdollControl 管理布娃娃物理；(5) 含多个特殊角色动画（关羽旋转、奥特飞行、马戏团球等）；(6) Anim-Opt 包含 AnimatorController 分析和优化工具

依赖：[[role-base]] · [[role-animation]] · [[role-animator]]
