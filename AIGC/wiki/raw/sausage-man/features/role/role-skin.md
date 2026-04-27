---
name: role-skin
display_name: 角色皮肤换装系统
category: role/skin
version: 1.0.0
dependencies:
- role-base
- role-render
---

# 角色皮肤换装系统

皮肤管理、换装数据、FashionData、DuoBaoSuit 夺宝换装

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Role/RoleSkinManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleSkinManager_MalouParty.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/DuoBaoSuit/DuoBaoSuitData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/DuoBaoSuit/DuoBaoSuitLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/DuoBaoSuit/DuoBaoSuitManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/DuoBaoSuit/DuoBaoSuitMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/SkinHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_RoleDisplay.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_DuoBaoSuit.cs` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_IdCardSkin.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSkinComponent.cs` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRoleLogic/RoleSkinChangeSkin.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Misc/SkinHAniConfig.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOSkinLodConfig.asset` |
| `Assets/ToBundle/Config/Txt/SkinItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/SkinItemHAsset.txt` |
| `Assets/ToBundle/Config/Txt/SkinPickItemAsset.txt` |
| `Assets/ToBundle/Config/Txt/IdCardSkin.txt` |
| `Assets/ToBundle/Config/Txt/IdCardSkinFashion.txt` |
| `Assets/ToBundle/Config/Txt/FashionAsset.txt` |
| `Assets/ToBundle/Config/Txt/FashionInfo.txt` |
| `Assets/ToBundle/Config/Txt/FashionEffect.txt` |
| `Assets/ToBundle/Config/Txt/FashionSet.txt` |
| `Assets/ToBundle/Config/Txt/FashionPartDefault.txt` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientChangeSkinFeatureManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerChangeSkinFeatureManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinChangeDefine.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinChanger.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinContainer.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinEffectContainer.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinFashionContainer.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinFashionPart.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinSlot.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinSlot_Effect.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Core/SkinSlot_Fashion.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/Other/SkinChangeUtil.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/PeformanceOpitimize/DissolvePosDispatcher.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/PeformanceOpitimize/DissolvePosReceiver.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/PeformanceOpitimize/KeywordOptimizer.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeAnimation.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeAnimator.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeGameObjectActive.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeMark.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeNormalAnimator.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinChangeSimpleAnimation.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinComponent.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinEffectLoader.cs` |
| `Assets/Script/GamePlay/Client/Modules/SkinChange/Runtime/SkinComponents/SkinFashionLoader.cs` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Fashion/` |
| `Assets/ToBundle/Skin/Items/` |
| `Assets/ToBundle/Skin/ItemsH/` |
| `Assets/ToBundle/Skin/PickItems/` |

## 备注

RoleSkinManager 管理皮肤加载和切换。DuoBaoSuit/ 目录包含 DuoBaoSuitData/Loader/Manager/Mgr 四个文件，处理夺宝换装特殊逻辑。RoleLogicClient_RoleDisplay 驱动模型加载，SkinHelper 提供皮肤工具方法

依赖：[[role-base]] · [[role-render]]
