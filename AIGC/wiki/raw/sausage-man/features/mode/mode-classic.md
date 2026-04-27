---
name: mode-classic
display_name: 经典模式（吃鸡/BR）
category: mode
version: 1.0.0
dependencies:
- mode-base
- mode-common
---

# 经典模式（吃鸡/BR）

Classic 经典模式（GameMode.Classic=1），即吃鸡/大逃杀。复合型模式，基于 CommonMode 阶段流，叠加毒圈(GameQuan)、跳伞(SqParachute)、航线(FlyLine)、轰炸区(BombArea)、安全区(SaveArea)、随机事件(RandomEvent) 等 BR 专属机制。目标：最终存活获胜。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/GameQuan/GameQuanCollider.cs [毒圈碰撞体]` |
| `Assets/Script/GamePlay/Host/Modules/GameQuan/GameQuanColliderManager.cs [毒圈碰撞管理]` |
| `Assets/Script/UI/War/GameQuan.cs [毒圈UI主类]` |
| `Assets/Script/UI/War/GameQuanMirror.cs [毒圈镜像UI]` |
| `Assets/Script/Controller/GameQuanCountDownController.cs [毒圈倒计时控制器]` |
| `Assets/Script/UI/TipsWar/GameQuanCountDownWin.cs [毒圈倒计时UI]` |
| `Assets/Script/UI/War/FlyLine.cs [航线UI]` |
| `Assets/Script/UI/War/FlyLineControl.cs [航线控制]` |
| `Assets/Script/UI/MapInfo/MapFlyLine.cs [地图航线显示]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Role_SqParachute.cs [跳伞角色逻辑]` |
| `Assets/Script/GamePlay/Host/Modules/Role/BattleRole/Component/BattleRoleSqParachuteComponent.cs [跳伞组件]` |
| `Assets/Script/GamePlay/Client/Motion/OpenParachuteState.cs [开伞动作状态]` |
| `Assets/Script/UI/War/SqParachute/SqParachuteOperateManager.cs [跳伞操作管理]` |
| `Assets/Script/UI/War/SqParachute/SqParachuteSelectRole.cs [跳伞角色选择]` |
| `Assets/Script/UI/War/SqParachute/SqParachuteUIItem.cs [跳伞UI元素]` |
| `Assets/Script/UI/War/Role/RoleParachute.cs [角色降落伞]` |
| `Assets/Script/UI/War/Role/RoleParachuteFly.cs [角色飞行中降落伞]` |
| `Assets/Script/UI/War/Role/RoleParachuteFollowing.cs [跟随降落伞]` |
| `Assets/Script/UI/War/Role/SORoleHqParachute.cs [高品质降落伞配置]` |
| `Assets/Script/Config/ParachuteColorConfig.cs [降落伞颜色配置]` |
| `Assets/Script/Config/Partial/PartialParachuteColorConfig.cs [降落伞颜色配置扩展]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/Extend/ClientSaveAreaFeatureManager.cs [安全区客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/Extend/ServerSaveAreaFeatureManager.cs [安全区服务端]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientBombAreaManager.cs [轰炸区客户端管理]` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerBombAreaManager.cs [轰炸区服务端管理]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBombArea.cs [轰炸区BSO]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBombArea.cs [轰炸区Buff逻辑]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBombAreaClient.cs [轰炸区Buff客户端]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBombAreaServer.cs [轰炸区Buff服务端]` |
| `Assets/Script/UI/War/HitType/BombArea.cs [轰炸区伤害UI]` |
| `Assets/Script/UI/War/SO/SOBombAreaEffect.cs [轰炸区特效配置]` |
| `Assets/Script/GamePlay/Client/Network/Feature/NetworkClient_BombArea.cs [轰炸区网络客户端]` |
| `Assets/Script/GamePlay/Server/Network/Feature/NetworkServer_BombArea.cs [轰炸区网络服务端]` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventBigBomb.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventBigger.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventBigSandStorm.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventJumpHigher.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventMoreHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventRoleSkillCoolDown.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventSuperEnergy.cs` |
| `Assets/Script/GamePlay/Client/Modules/RandomEvent/ClientRandomEventUtil.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventAutoRecover.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventBigBomb.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventBigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventBigSandStorm.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventDeadResurrect.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventDuelingBlades.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventJumpHigher.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventMoreCreateItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventMoreHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventMoreSeasonItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventRoleBigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventRoleSkillCoolDown.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventSuperEnergy.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventSuperHalo.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventUnknownEvent.cs` |
| `Assets/Script/GamePlay/Server/Modules/RandomEvent/ServerRandomEventUtil.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventAutoRecover.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventBigBomb.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventBigSandStorm.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventBigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventDeadResurrect.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventDuelingBlades.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventJumpHigher.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventMoreCreateItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventMoreHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventMoreSeasonItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventRoleBigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventRoleSkillCoolDown.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventSuperEnergy.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventSuperHalo.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventUnknownEvent.cs` |
| `Assets/Script/GamePlay/Host/Modules/RandomEvent/HostRandomEventUtil.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/RandomEvent/ [19个随机事件SO配置]` |
| `Assets/ToBundle/Config/Txt/ParachuteColor.txt [降落伞颜色]` |

## 备注

复合型模式，共 72 文件。核心子系统: 毒圈(GameQuan, 6文件) + 跳伞(SqParachute, 15文件) + 航线(FlyLine, 3文件) + 轰炸区(BombArea, 11文件) + 安全区(SaveArea, 2文件) + 随机事件(RandomEvent, C8/S16/H16=40文件 但部分也被其他模式使用)。⚠️ 毒圈=GameQuan 不是 BombArea！WarData.AttackType: DuQuan=8(毒圈), AirBomb=7(轰炸区)。GameMode.Classic=1 对应此模式。此 JSON 不含 CommonMode 代码(已拆至 mode-common.json)。

依赖：[[mode-base]] · [[mode-common]]
