---
name: mode-pverogue
display_name: PVE 肉鸽（PveRogue）
category: mode/pverogue
version: 1.0.0
dependencies:
- mode-base
---

# PVE 肉鸽（PveRogue）

PVE Roguelike 模式：随机地牢/关卡生成，支持肉鸽玩法，C/S/H 三端均有实现

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/ClientPveRogueData.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/ClientPveRogueMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/IClientMonsterExcute.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Logic/ClientPveRogueLootLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Logic/ClientPveRogueMonsterLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Logic/ClientPveRogueRoleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Logic/ClientPveRogueTerrainLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Logic/ClientPveRogueTimelineLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonDownHpEffectMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonster.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonsterDragon.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonster_Display.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonster_DownHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Monster/ClientPveMonster_Move.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Other/ClientPveDropItem.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Other/ClientPveDropItemMgr.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Other/ClientRoleLogicPveBattleInfo.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Other/ClientRoleLogicPveDataManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Stage/ClientPveRogueBattleStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Stage/ClientPveRogueBornStage.cs` |
| `Assets/Script/GamePlay/Client/Modules/Mode/PveRogue/Stage/ClientPveRogueOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/ServerPveRogueData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/ServerPveRogueMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueAwardLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueGameplayLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueLootLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueMonsterLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueNsqDataLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueRoleLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueShoppingLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueStatisticsLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueTerrainLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueTestLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Logic/ServerPveRogueTimelineLogic.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/IServerPveMonsterMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/ServerPveMonster.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/ServerPveMonster_AIBehavior.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/ServerPveMonster_Move.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/ServerPveMonster_Skill.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Monster/ServerPveMonster_Target.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/ServerPveRogueBornData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/ServerPveRoguePointData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/ServerPveRoleItemData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/ServerPveRoleItemData_Data.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/ServerRoleLogicPveDataManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/DropItem/ServerPveDropItemData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/DropItem/ServerPveDropItemMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Other/DropItem/ServerPveDropItemPickMgr.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Stage/ServerPveRogueBattleStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Stage/ServerPveRogueBornStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Stage/ServerPveRogueOverStage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Mode/PveRogue/Totem/RoleTotemServer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveDebugHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveMonsterHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveRogueDefine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveTotemConditionDispatcher.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveTotemConditionRegister.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveTotemEffect.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/PveTotemHelper.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/RoleLogicPveDataMgr.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/CustomTotemCheck/CustomTotemCheck.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/CustomTotemCheck/CustomTotemCheckRoleSpecHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/CustomTotemTrigger/CustomTotemTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/CustomTotemTrigger/TotemTriggerMonsterBeKilledBySpecDis.cs` |
| `Assets/Script/GamePlay/Host/Modules/Mode/PveRogue/Monster/PveMonsterBase.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Mode/PveRogue/ [96 files]` |
| `Assets/ToBundle/Config/Txt/GameMode.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Role/Controllers/War/PveMode/` |

## 备注

GameMode 枚举 Pvemode=23. 共 65 文件. 三端分布: C=21/S=31/H=13. key_classes: ClientPveRogueData, ClientPveRogueLootLogic, ClientPveRogueMonsterLogic, ClientPveRogueRoleLogic, ClientPveRogueTerrainLogic, ClientPveRogueTimelineLogic, ClientRoleLogicPveBattleInfo, ClientRoleLogicPveDataManager, ClientPveRogueBattleStage, ClientPveRogueBornStage. 子目录: Client: Logic(5), Monster(6), Other(4), Stage(3); Server: Logic(11), Monster(6), Other(8), Stage(3), Totem(1); Host: CustomTotemCheck(2), CustomTotemTrigger(2), Monster(1). 含独立 Loader: PveModeLoader.cs

依赖：[[mode-base]]

## 关联 Buff


### PVE Buff（42）

| feature | 说明 |
|---------|------|
| [[buff-pve-add-ability-duration]] | BSPveAddAbilityDuration - PveAddAbilityDuration |
| [[buff-pve-add-attr-consume]] | BSPveAddAttrConsume - PveAddAttrConsume |
| [[buff-pve-add-attr-in-duration]] | BSPveAddAttrInDuration - PveAddAttrInDuration |
| [[buff-pve-add-hp]] | BSPveAddHp - PveAddHp |
| [[buff-pve-add-next-bullet-damage]] | BSPveAddNextBulletDamage - PveAddNextBulletDamage |
| [[buff-pve-add-shield-value]] | BSPveAddShieldValue - PveAddShieldValue |
| [[buff-pve-auto-recover-hp]] | BSPveAutoRecoverHp - PveAutoRecoverHp |
| [[buff-pve-buff-add-bullet]] | BSPveBuffAddBullet - PveBuffAddBullet |
| [[buff-pve-buff-reload-bullet]] | BSPveBuffReloadBullet - PveBuffReloadBullet |
| [[buff-pve-bullet-go-through-ability]] | BSPveBulletGoThroughAbility - PveBulletGoThroughAbility |
| [[buff-pve-custom-totem-trigger]] | BSPveCustomTotemTrigger - PveCustomTotemTrigger |
| [[buff-pve-custom-trigger-health]] | BSPveCustomTriggerHealth - PveCustomTriggerHealth |
| [[buff-pve-dash]] | BSPveDash - PveDash |
| [[buff-pve-monster]] | BSPveMonster - PveMonster |
| [[buff-pve-monster-bomb]] | BSPveMonsterBomb - PveMonsterBomb |
| [[buff-pve-monster-bomb-move]] | BSPveMonsterBombMove - PveMonsterBombMove |
| [[buff-pve-monster-bomb-reload]] | BSPveMonsterBombReload - PveMonsterBombReload |
| [[buff-pve-monster-bubbles-bullet]] | BSPveMonsterBubblesBullet - PveMonsterBubblesBullet |
| [[buff-pve-monster-dragon-armor]] | BSPveMonsterDragonArmor - PveMonsterDragonArmor |
| [[buff-pve-monster-dragon-fire]] | BSPveMonsterDragonFire - PveMonsterDragonFire |
| [[buff-pve-monster-dragon-rush]] | BSPveMonsterDragonRush - PveMonsterDragonRush |
| [[buff-pve-monster-exploder]] | BSPveMonsterExploder - PveMonsterExploder |
| [[buff-pve-monster-fire-ball]] | BSPveMonsterFireBall - PveMonsterFireBall |
| [[buff-pve-monster-hail-bullet]] | BSPveMonsterHailBullet - PveMonsterHailBullet |
| [[buff-pve-monster-ice-crystal]] | BSPveMonsterIceCrystal - PveMonsterIceCrystal |
| [[buff-pve-monster-melee]] | BSPveMonsterMelee - PveMonsterMelee |
| [[buff-pve-monster-multi-throw]] | BSPveMonsterMultiThrow - PveMonsterMultiThrow |
| [[buff-pve-monster-rush]] | BSPveMonsterRush - PveMonsterRush |
| [[buff-pve-monster-shake-ground]] | BSPveMonsterShakeGround - PveMonsterShakeGround |
| [[buff-pve-monster-shoot]] | BSPveMonsterShoot - PveMonsterShoot |
| [[buff-pve-monster-spin]] | BSPveMonsterSpin - PveMonsterSpin |
| [[buff-pve-monster-sword-qi]] | BSPveMonsterSwordQi - PveMonsterSwordQi |
| [[buff-pve-monster-throw]] | BSPveMonsterThrow - PveMonsterThrow |
| [[buff-pve-monster-track-bullet]] | BSPveMonsterTrackBullet - PveMonsterTrackBullet |
| [[buff-pve-reset-dash-cool-time]] | BSPveResetDashCoolTime - PveResetDashCoolTime |
| [[buff-pve-reset-skill-c-d]] | BSPveResetSkillCD - PveResetSkillCD |
| [[buff-pve-restore-shield-immediately]] | BSPveRestoreShieldImmediately - PveRestoreShieldImmediately |
| [[buff-pve-shield]] | BSPveShield - PveShield |
| [[buff-pve-totem-add-dmg-no-team-around]] | BSPveTotemAddDmgNoTeamAround - PveTotemAddDmgNoTeamAround |
| [[buff-pve-totem-consume]] | BSPveTotemConsume - PveTotemConsume |
| [[buff-pve-totem-custom-checker]] | BSPveTotemCustomChecker - PveTotemCustomChecker |
| [[buff-pve-totem-time-check-condition]] | BSPveTotemTimeCheckCondition - PveTotemTimeCheckCondition |

### 图腾 Buff（23）

| feature | 说明 |
|---------|------|
| [[buff-totem-add-attr]] | BSTotemAddAttr - TotemAddAttr |
| [[buff-totem-add-come-on]] | BSTotemAddComeOn - TotemAddComeOn |
| [[buff-totem-add-grieved-potion]] | BSTotemAddGrievedPotion - TotemAddGrievedPotion |
| [[buff-totem-add-hot-muzzle]] | BSTotemAddHotMuzzle - TotemAddHotMuzzle |
| [[buff-totem-add-iron-egg]] | BSTotemAddIronEgg - TotemAddIronEgg |
| [[buff-totem-add-nirvana-jewel]] | BSTotemAddNirvanaJewel - TotemAddNirvanaJewel |
| [[buff-totem-add-persimmo]] | BSTotemAddPersimmo - TotemAddPersimmo |
| [[buff-totem-add-rest-station]] | BSTotemAddRestStation - TotemAddRestStation |
| [[buff-totem-add-senior-hunter]] | BSTotemAddSeniorHunter - TotemAddSeniorHunter |
| [[buff-totem-add-stove]] | BSTotemAddStove - TotemAddStove |
| [[buff-totem-add-thistles-shield]] | BSTotemAddThistlesShield - TotemAddThistlesShield |
| [[buff-totem-attack-dis-add-wpn-dmg]] | BSTotemAttackDisAddWpnDmg - TotemAttackDisAddWpnDmg |
| [[buff-totem-charge-add-next-wpn-dmg]] | BSTotemChargeAddNextWpnDmg - TotemChargeAddNextWpnDmg |
| [[buff-totem-combination]] | BSTotemCombination - TotemCombination |
| [[buff-totem-event-cost]] | BSTotemEventCost - TotemEventCost |
| [[buff-totem-event-explosive-bullet]] | BSTotemEventExplosiveBullet - TotemEventExplosiveBullet |
| [[buff-totem-event-ship-arrow]] | BSTotemEventShipArrow - TotemEventShipArrow |
| [[buff-totem-hit-monster-buff]] | BSTotemHitMonsterBuff - TotemHitMonsterBuff |
| [[buff-totem-more-shopping]] | BSTotemMoreShopping - TotemMoreShopping |
| [[buff-totem-teammate-strength]] | BSTotemTeammateStrength - TotemTeammateStrength |
| [[buff-totem-time-add-attr]] | BSTotemTimeAddAttr - TotemTimeAddAttr |
| [[buff-totem-trigger-event]] | BSTotemTriggerEvent - TotemTriggerEvent |
| [[buff-totem-when-attr-then-attr]] | BSTotemWhenAttrThenAttr - TotemWhenAttrThenAttr |

### 地牢 Buff（8）

| feature | 说明 |
|---------|------|
| [[buff-dragon-palace]] | BSDragonPalace - DragonPalace |
| [[buff-dragon-palace-obj]] | BSDragonPalaceObj - DragonPalaceObj |
| [[buff-dungeon-game-ball]] | BSDungeonGameBall - DungeonGameBall |
| [[buff-dungeon-game-box]] | BSDungeonGameBox - DungeonGameBox |
| [[buff-dungeon-game-launcher]] | BSDungeonGameLauncher - DungeonGameLauncher |
| [[buff-dungeon-game-star]] | BSDungeonGameStar - DungeonGameStar |
| [[buff-dungeon-game-switch-door]] | BSDungeonGameSwitchDoor - DungeonGameSwitchDoor |
| [[buff-dungeon-game-target]] | BSDungeonGameTarget - DungeonGameTarget |
