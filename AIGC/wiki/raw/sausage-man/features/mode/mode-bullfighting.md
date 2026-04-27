---
name: mode-bullfighting
display_name: 枪王之王（BullFightingMode）
category: mode/bullfighting
version: 1.0.0
dependencies:
- mode-base
---

# 枪王之王（BullFightingMode）

枪王竞技模式：强调个人枪法的竞技对战，仅 Client/Server 两端

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/BullFightingModeStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/ClientBullFightingModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/ClientBullFightingModeMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Logic/ClientBullFightingModeMapLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeInfoStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeOverStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeRoundEndStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeRoundStartStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/BullFightingMode/Stage/ClientBullFightingModeShopStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/ServerBullFightingModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/ServerBullFightingModeMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Logic/ServerBullFightingModeAILogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Logic/ServerBullFightingModeAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Logic/ServerBullFightingModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Logic/ServerBullFightingModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Logic/ServerBullFightingModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeInfoStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeRoundEndStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeRoundStartStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/BullFighting/Stage/ServerBullFightingModeShopStage.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/BullFightingMode/ [2 files]` |
| `Assets/ToBundle/ScriptableObject/Screen/SOGunfightRoundData/ [54 files, 回合制对战数据]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 备注

GameMode 枚举 Bullfighting=43. 共 23 文件. 三端分布: C=10/S=13/H=0. key_classes: BullFightingModeStage, ClientBullFightingModeData, ClientBullFightingModeMapLogic, ClientBullFightingModeBornStage, ClientBullFightingModeInfoStage, ClientBullFightingModeOverStage, ClientBullFightingModeRoundEndStage, ClientBullFightingModeRoundStartStage, ClientBullFightingModeShopStage, ServerBullFightingModeData. 子目录: Client: Logic(1), Stage(6); Server: Logic(5), Stage(6). 注意 Server 端目录名为 BullFighting（无 Mode 后缀）

依赖：[[mode-base]]

## 关联 Buff


### 拳击 Buff（2）

| feature | 说明 |
|---------|------|
| [[buff-boxing-fly]] | BSBoxingFly - BoxingFly |
| [[buff-boxing-trampoline]] | BSBoxingTrampoline - BoxingTrampoline |
