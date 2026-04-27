---
name: weapon-melee-framework
display_name: 近战格斗框架（FightClose）
category: weapon/melee-framework
version: 1.0.0
dependencies:
- weapon-base
---

# 近战格斗框架（FightClose）

FightClose 通用近战框架：C/S 镜像架构，含 Data/Logic/Stage 三层，提供近战状态机和伤害判定。具体近战武器实现见 [[weapon-melee]]

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/GamePlay/Client/Modules/FightClose/ClientFightCloseMainLogic.cs` | 客户端近战主逻辑 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Data/ClientFightCloseData.cs` | 客户端近战数据 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Data/ClientFightCloseData_Method.cs` | 客户端近战数据方法 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Logic/ClientFightCloseMusicLogic.cs` | 客户端近战音效 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Logic/ClientFightCloseRoleLogic.cs` | 客户端近战角色逻辑 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Stage/ClientFightCloseBattleStage.cs` | 客户端战斗阶段 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Stage/ClientFightCloseOverStage.cs` | 客户端结束阶段 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Stage/ClientFightCloseReadyStage.cs` | 客户端准备阶段 |
| `Assets/Script/GamePlay/Client/Modules/FightClose/Stage/ClientFightCloseStageMgr.cs` | 客户端阶段管理器 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Data/ServerFightCloseData.cs` | 服务端近战数据 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Data/ServerFightCloseData_Method.cs` | 服务端近战数据方法 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Data/ServerFightCloseData_Net.cs` | 服务端近战网络 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Logic/ServerFightCloseCrazyMomentLogic.cs` | 服务端疯狂时刻 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Logic/ServerFightCloseRebirthLogic.cs` | 服务端复活逻辑 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Logic/ServerFightCloseRoleLogic.cs` | 服务端角色逻辑 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/ServerFightCloseMainLogic.cs` | 服务端近战主逻辑 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Stage/ServerFightCloseBattleStage.cs` | 服务端战斗阶段 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Stage/ServerFightCloseOverStage.cs` | 服务端结束阶段 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Stage/ServerFightCloseReadyStage.cs` | 服务端准备阶段 |
| `Assets/Script/GamePlay/Server/Modules/FightClose/Stage/ServerFightCloseStageMgr.cs` | 服务端阶段管理器 |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleMeleeAttackEffect.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Misc/SOMeleeAttackData.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOMeleeAttackData_GoldDash.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOMeleeEffectData.asset` |
| `Assets/ToBundle/ScriptableObject/Misc/SOMeleeEffectData_GoldDash.asset` |
| `Assets/ToBundle/Config/Txt/SOAGMeleeSlot.txt` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/AbsFightCloseLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/AbsFightCloseMainLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/AbsFightCloseStage.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/AbsFightCloseStageMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/FightCloseData.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/FightCloseDataCompare.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/FightCloseLogicMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/IFightCloseLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/FightClose/IFightCloseStage.cs` |

## 备注

FightClose 是 C/S 镜像架构的通用近战框架，Data 层定义近战数据，Logic 层处理战斗逻辑，Stage 层管理近战阶段状态机（Ready→Battle→Over）

依赖：[[weapon-base]]
