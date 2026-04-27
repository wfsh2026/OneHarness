---
name: weapon-base
display_name: 武器核心框架
category: weapon/base
version: 1.0.0
dependencies:
- role-base
---

# 武器核心框架

武器系统三端核心框架：Host 层 BattleRoleWeaponComponent/RoleLogicWeaponComponent/WeaponConfig 定义武器状态机和配置加载，Proto_RoleWeapon/Proto_ArcadeWeapon 定义网络同步协议（CmdStartFire/StopFire/ChangeWeapon），Client/Server 层实现表现与校验

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleWeaponComponent.cs [武器状态机核心]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicWeaponComponent.cs [武器逻辑层]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleTeammateWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/Component/RoleLogicTeammateWeaponComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_Weapon.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleLogic_Weapon.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/WeaponConfig.cs [武器配置加载]` |
| `Assets/Script/GamePlay/Host/Modules/Item/ItemConfig/WeaponEquipConfig.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_RoleWeapon.cs [网络协议定义]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Proto_ArcadeWeapon.cs [街机模式武器协议]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientWeaponCheckerFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/WeaponSkillClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/WeaponSkillServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerArcadeWeaponFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerArcadeWeaponRecord.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerWeaponCheckerFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/RoleLogicWeaponHitRatioFeatureManager.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/WeaponType.txt [武器类型定义]` |
| `Assets/ToBundle/Config/Txt/WeaponStore.txt [武器商店/池]` |
| `Assets/ToBundle/Config/Txt/WeaponPosition.txt [武器持握位置]` |
| `Assets/ToBundle/Config/Txt/WeaponSubPath.txt [武器资产路径映射]` |
| `Assets/ToBundle/Config/Txt/WeaponControlAsset.txt [武器控制方案]` |
| `Assets/ToBundle/Config/Txt/WeaponAreaRelation.txt [伤害区域关系]` |
| `Assets/ToBundle/Config/Txt/BattleUiWeaponOptions.txt [战斗UI武器选项]` |
| `Assets/ToBundle/Config/Txt/BigWeaponAsset.txt [大型武器资产]` |
| `Assets/ToBundle/Config/Txt/SOAGWeaponSlot.txt [武器槽位SO]` |
| `Assets/ToBundle/ScriptableObject/Items/Weapons/ [238 files, 98种武器SO定义 — AK12/AKM/AWM/M416/Kar98/RPG/Pan 等全量武器]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/WeaponEff/ [3,305 files, 武器主特效 — 枪口闪光/弹道/命中/后坐力/换弹等]` |
| `Assets/ToBundle/Effect/WeaponCommon/ [3 files, 通用武器特效]` |
| `Assets/ToBundle/Items/War/ [23 files, 战场武器模型]` |

## 备注

武器系统是项目最核心的战斗子系统之一。98种武器通过238个ScriptableObject定义（AK12/AKM/AWM/M416/Kar98/RPG/Pan/信号枪等），921个WeaponEff子目录提供每种武器×每个皮肤的独立特效。WeaponType.txt 定义11个武器大类，WeaponStore.txt 定义53个标准武器池条目。Proto_RoleWeapon 定义了开火/停火/换武器等网络命令。模式专属武器商店配置(14个txt: PkWeapon/ArcadeWeaponStore/DefusalWeaponStore 等)归属各模式 feature。AI武器配置(AIWeaponConfig/AIWeaponSkin)归属 ai-base

依赖：[[role-base]]
