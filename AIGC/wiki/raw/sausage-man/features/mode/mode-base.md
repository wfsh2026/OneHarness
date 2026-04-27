---
name: mode-base
display_name: 模式系统框架基类
category: mode
version: 1.1.0
dependencies: []
---

# 模式系统框架基类

模式系统四层架构基类（Manager/Stage/Logic/Data 接口+抽象类）、C/S 两端 Factory 模式创建工厂。所有具体模式均继承此框架。不包含任何具体模式逻辑。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/ClientModeData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/ClientModeDefine.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/ClientModeLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/ClientModeManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/ClientModeStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/Base/Logic/ClientModeInvincibleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/ClientModeFactory.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/ServerModeData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/ServerModeDefine.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/ServerModeManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Logic/ServerModeAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Logic/ServerModeLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Logic/ServerModeNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Logic/ServerModeRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Logic/ServerModeStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Stage/ServerModeBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Stage/ServerModeOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/Base/Stage/ServerModeStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/ServerModeFactory.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/AbsModeData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/AbsModeLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/AbsModeManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/AbsModeMonoLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/AbsModeStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/IModeData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/IModeLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/IModeManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/IModeStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/ModeDataCollection.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/ModeLogicCollection.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/ModeStageCollection.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/Base/SortedQueue.cs` |
| `Assets/Script/GamePlay/Host/Modules/ModeManager/RoundModeBase.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/ [各模式SO配置总目录]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt [模式枚举配置]` |
| `Assets/ToBundle/Config/Txt/GameModeRule.txt [模式规则]` |
| `Assets/ToBundle/Config/Txt/GameModeTab.txt [模式页签]` |
| `Assets/ToBundle/Config/Txt/MatchMode.txt [匹配模式配置 — 每条记录定义一个可匹配的模式实例(含地图变体)，字段: id/sign/game_mode/map_mode/show_mode/icon/enable_match 等]` |
| `Assets/ToBundle/Config/Txt/MatchType.txt [匹配类型]` |
| `Assets/ToBundle/Config/Txt/GameMap.txt [地图配置]` |
| `Assets/ToBundle/Config/Txt/ShowMode.txt [展示模式 — 定义 UI 入口分类，字段: id/sign/desc；被 MatchMode.show_mode 引用]` |
| `Assets/ToBundle/Config/Txt/EntryMode.txt [入口模式]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/AutoGen/ [自动生成动画控制器]` |

## 备注

纯框架层，共 32 文件。三端分布: C=7/S=12/H=13。AbsModeManager 是所有模式的核心基类，管理 Stage/Logic/Data 三个 Collection。ClientModeFactory/ServerModeFactory 通过 switch(WarData.Game_Mode) 创建具体模式实例。新增模式流程见 [[模式制作]]。枚举定义: Assets/Script/Data/Base/GameMode.cs + Assets/Script/Data/WarData.cs
