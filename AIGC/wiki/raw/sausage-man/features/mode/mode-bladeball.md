---
name: mode-bladeball
display_name: 痛击飞球（BladeBallMode）
category: mode/bladeball
version: 1.0.0
dependencies:
- mode-base
- mode-common
---

# 痛击飞球（BladeBallMode）

飞球对战模式：玩家躲避并击打飞球，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallModeMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallSkillLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallSkillOperate.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallSkinLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallUILogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/ClientBladeBallUtil.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/BladeBall/ClientBladeBallController.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/BladeBall/ClientBladeBallMono.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/BladeBall/ClientBladeBallRotate.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeReadyStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeRoundOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BladeBallMode/Stage/ClientBladeBallModeWaitStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BattleCommonDynamicData_BladeBallMode.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallAFKLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeObLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallPointLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallRevengeLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallRoleReportLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallRoleTimeLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallRuleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallSkillLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/ServerBladeBallSkinLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/AbsBladeBallController.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/BladeBallC2S.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/BladeBallC2SMirror.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/BladeBallNetwork.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/BladeBallNetworkMirror.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/ServerBladeBallController.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/ServerBladeBallUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/BallSpeed/ServerBladeBallSpeedControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Buff/ServerBladeBallBuffBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Buff/ServerBladeBallBuffControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Buff/ServerBladeBallBuffFrozen.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Buff/ServerBladeBallBuffInvincible.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Buff/ServerBladeBallBuffInvisible.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/Property/ServerBladeBallPropertyControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateAppear.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateBeHit.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateBecauseWeak.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateConfused.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateHitRole.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateNone.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/BladeBall/State/ServerBladeBallStateReadyMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/SOData/SOBladeBallModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/SOData/SOBladeBallModeExtData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/SOData/SOBladeBallModeMeleeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeReadyStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeRoundOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BladeBallMode/Stage/ServerBladeBallModeWaitStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/BladeBallMode/ [5 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/BladeBallMode/` |

## 备注

GameMode 枚举 Bladeballmode=24. 共 65 文件. 三端分布: C=17/S=48/H=0. key_classes: ClientBladeBallLogic, ClientBladeBallModeData, ClientBladeBallSkillLogic, ClientBladeBallSkinLogic, ClientBladeBallUILogic, ClientBladeBallController, ClientBladeBallModeBattleStage, ClientBladeBallModeBornStage, ClientBladeBallModeOverStage, ClientBladeBallModeReadyStage. 子目录: Client: BladeBall(3), Stage(6); Server: BladeBall(24), SOData(3), Stage(6)

依赖：[[mode-base]] · [[mode-common]]

## 关联 Buff


### 飞球 Buff（3）

| feature | 说明 |
|---------|------|
| [[buff-blade-ball-air-cut]] | BSBladeBallAirCut - BladeBallAirCut |
| [[buff-blade-ball-inversion]] | BSBladeBallInversion - BladeBallInversion |
| [[buff-blade-ball-wolf-man-jump]] | BSBladeBallWolfManJump - BladeBallWolfManJump |
