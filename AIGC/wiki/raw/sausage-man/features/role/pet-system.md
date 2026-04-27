---
name: pet-system
display_name: 宠物系统（Pet）
category: system/pet
version: 1.0.0
dependencies:
  - role-base
---

# 宠物系统（Pet）

战场宠物系统：宠物 SO 配置、宠物表现、跟随逻辑。含 SausagePet 子系统。共 63 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Config/GoldDashPetPassiveConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkillConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkillLvConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkillLvUnetConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkillMapConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkillTypeConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkinConfig.cs` |
| `Assets/Script/Config/GoldDashPetSkinTimeConfig.cs` |
| `Assets/Script/Config/Partial/GoldDashPetSkinTimeConfig.cs` |
| `Assets/Script/Config/SOPetPriorityConfig.cs` |
| `Assets/Script/Data/Base/ExtraPet.cs` |
| `Assets/Script/Data/Base/GoldDashPetPersonalType.cs` |
| `Assets/Script/Data/Base/GoldDashPetSkillType.cs` |
| `Assets/Script/Data/Base/UnetPlayerGoldDashPet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPetCutDownCdClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPetSkillBubbleClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientPetManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/SausageClientPetManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/ClientRolePet.cs` |
| `Assets/Script/GamePlay/Client/Modules/Features/RoleLogic/SausageClientRolePet.cs` |
| `Assets/Script/GamePlay/Client/Modules/FlyVehicle/Peterosaur.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ClientPetMovement.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ClientPetPassiveAbilities.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ClientPetView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/PetSkinHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/SausagePetView.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ScriptableObject/SOPetSkinColor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ScriptableObject/SOPetSkinPattern.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ViewBinder/PetAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ViewBinder/PetAuthoring.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ViewBinder/PetColorChange.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ViewBinder/PetColorChange_ShaderProperty.cs` |
| `Assets/Script/GamePlay/Client/Modules/Pet/ViewLogic/PetAnimLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/SausagePet/ClientPetPassiveAbilities.cs` |
| `Assets/Script/GamePlay/Client/Modules/SausagePet/SausageClientPetMovement.cs` |
| `Assets/Script/GamePlay/Client/Modules/SausagePet/SausageClientPetView.cs` |
| `Assets/Script/GamePlay/Client/Modules/SausagePet/SausagePetSkinHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/SausagePet/ViewLogic/SausagePetAnimLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPetCutDownCd.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPetSkillBubble.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPetCutDownCd.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPetSkillBubble.cs` |
| `Assets/Script/GamePlay/Host/Modules/Pet/PetInstructure.cs` |
| `Assets/Script/GamePlay/Host/Modules/Pet/PetPassiveAbilityShare.cs` |
| `Assets/Script/GamePlay/Host/Modules/Pet/SOPet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Pet/SOPetView.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_PetPassiveData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_PetSkinData.cs` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_PetSyncData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPetSkillBubbleServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/SausageServerPetManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerPetManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/SausageServerRolePet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Features/RoleLogic/ServerRolePet.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/AbsPetPassiveAbility.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/PetLotteryComponent.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/PetSkillCDCutdownAbility.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/PetSkillFreeUseAbility.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/ServerPetMovement.cs` |
| `Assets/Script/GamePlay/Server/Modules/Pet/ServerPetPassiveAbilities.cs` |
| `Assets/Script/GamePlay/Server/Modules/SausagePet/SausageServerPetMovement.cs` |
| `Assets/Script/Lua/XLua/Gen/PetActionWrap.cs` |
| `Assets/Script/Lua/XLua/Gen/PetColorChangeWrap.cs` |

## 备注

依赖：[[role-base]]
