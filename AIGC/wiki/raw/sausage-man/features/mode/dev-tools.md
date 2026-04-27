---
name: dev-tools
display_name: 开发工具/测试（DevTools）
category: system/devtools
version: 1.0.0
dependencies:
  []
---

# 开发工具/测试（DevTools）

开发调试工具：自动化测试框架（AutomationTools）、单元测试（UnitTest）、通用工具函数（Utils）。共 74 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/ATEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/ATSystemEvent.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/AutomationToolData.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/AutomationToolEnum.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/AutomationToolManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/AutomationToolSystem.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/AutomationToolSystem_Event.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATFrame.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATInput.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATLoadPipelineData.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoDocRegister.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoRegister.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoRegister_Rule.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoReplay.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoReplay_Static.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Components/ATProtoSave.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Net/AutoWarCaseNetProgram.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/ATEventProto.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/ATEventProto_Static.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Base.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Camera.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Car.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Compression.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Input.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Item.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Role.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_RoleAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_RoleMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Skill.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_TestTool.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Weapon.cs` |
| `Assets/Script/GamePlay/Client/Modules/AutomationTools/Proto/Doc/ATEventProtoDoc_Win.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/RangeCube.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_AiControl.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_AiRoot.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_Target.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_TargetMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_TargetRoot.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_TargetScore.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_TargetTrigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_Teleporter.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_TeleporterDragonPalace.cs` |
| `Assets/Script/GamePlay/Client/Modules/UnitTest/WN_Trigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/GUIManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/GizmosManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Action/AbsMonsterAIAction.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Action/MonCastSkill.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Action/MonFollow.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Action/MonIdle.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Action/MonRandMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/AbsMonsterAIConditional.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckBattleTimeCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckBlock.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckIsCasting.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckMonsterType.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckOwnBuffID.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckSkillCool.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckSkillHpCheck.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonCheckSkillRange.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonFindLockRole.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/Conditional/MonRayBlock.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/PveAIBehaviorHelper.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/PveAIBehaviorMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/MonsterAI/SharedPveMonster.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/SportPartyBornPointEditor.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/StartExternalProcess.cs` |
| `Assets/Script/GamePlay/Client/Modules/Utils/TimelineManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Utils/ObjManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Utils/RaycastManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Utils/DebugOpenUtils.cs` |
| `Assets/Script/GamePlay/Server/Modules/Utils/RoleInformation.cs` |
| `Assets/Script/GamePlay/Server/Modules/Utils/ServerHelper.cs` |
| `Assets/Script/GamePlay/Server/Modules/Utils/SportPartyGameScoreFormulaUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Utils/WarEventUtils.cs` |

## 备注

依赖：无
