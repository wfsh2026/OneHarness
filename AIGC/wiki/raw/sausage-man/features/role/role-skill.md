---
name: role-skill
display_name: 角色技能系统（RoleSkill）
category: role/skill
version: 1.0.0
dependencies:
  - role-base
  - buff-framework
---

# 角色技能系统（RoleSkill）

角色主动技能系统：各身份卡技能 BS 实现、技能冷却管理、技能 UI 控制。与 Buff 系统深度耦合。共 163 个 .cs 文件。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Config/GoldDashGameRoleSkillConfig.cs` |
| `Assets/Script/Config/GoldDashGameRoleSkillTimeConfig.cs` |
| `Assets/Script/Config/Partial/SORoleSkillConfig.cs` |
| `Assets/Script/Config/SORoleSkillConfig.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSBeRatClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSBeRatForwardClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSFlymanFlyClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSGeedJumpClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSSlideTackleBallClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSWolfHowlClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSWolfManPowerClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSZeroEmeriumClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleSkill/BSZetaBlinkClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSFlymanFly.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSFlymanSmoke.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleSkill/BSZetaBlink.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSBeRatForwardServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSBeRatServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSFlymanFlyServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSFlymanSmokeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSSlideTackleBallServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSWolfHowlServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSWolfManPowerServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSZeroEmeriumServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleSkill/BSZetaBlinkServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Skill/RoleSkillQueue.cs` |
| `Assets/Script/GamePlay/Server/Modules/Skill/RoleSkillUpdater.cs` |
| `Assets/Script/GamePlay/Server/Modules/Skill/ServerSkillTimeState.cs` |
| `Assets/Script/UI/PlayerControl/Skill/Base/IUIRoleSkill.cs` |
| `Assets/Script/UI/PlayerControl/Skill/Base/UIRoleSkillBase.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillBase_ATEvent.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillExpandUI.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillInstant.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillMgr.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillState.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillStateForever.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillThrow.cs` |
| `Assets/Script/UI/PlayerControl/Skill/UISkillStateInfo.cs` |
| `Assets/Script/UI/PlayerControl/UIRoleSkillSpecial.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/ClientSkillTimeState.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkill.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillBase.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillBomb.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillEffect.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillExpandUIBase.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Adsorb.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/AidMeiHealingBot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/AidMeiStage.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ArrowTower.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/AssaultClownGrenade.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/AssaultKittyJump.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/AssaultSungodBurn.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BeRat.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallAbsorb.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallAirCut.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallFrozen.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallInversion.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallMindControl.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallShieldSoldier.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallSnowBall.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/BladeBallSwap.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/CaoCaoArrival.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/CaoCaoSelectRole.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/CaoCaoShieldPawn.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/CaptainCardGhost.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/CaptainCardHot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ClownGrenade.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ClownGrenadeBeastCamp.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ClownPlatform.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Clownskill2.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/DefenseShieldHpState.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Doctorwhoskill1.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Doctorwhoskill2.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/EightDirDash.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/FlyManFootControl.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/FlymanFly.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/FlymanSmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/FlymanWingControl.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GandaBurn.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GandaFly.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GandaFlyControl.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GaunletDash.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Geed_Jump.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/Geed_Shot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GoldDashDoctorwhoskill2.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GoldDashNinjaShadowCopy.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GoldDashNoobFishTouch.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GoldDashSmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GoldDashSpySmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GuanyuSpin.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GuanyuSprint.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/GutsAirStrike.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/HadesFireBall.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/HadesFireWall.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/HadesHiding.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/InvicableStar.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/KaduraPower.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/KaduraShield.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/KittyJump.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/KittyRadar.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/LightningBomb.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/LightningTransfer.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/MonsterShot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NeptuneShark.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NeptuneShield.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NinjaHookFly.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NinjaShadowCopy.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NoobFishAnimSound.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NoobFishBooth.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/NoobFishTouch.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/PaoKuFlyAir.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/PaoKuRoll.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/PlaySound.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/PveDash.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/RainbowBridge.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/RainbowCloud.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ReconArrowTowers.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ReconBaGuaZhen.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ReconKittyRadar.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ReplaceWeapon.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/RigibodyIgnore.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/RigibodyIgnoreRole.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SandGrenade.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SandPlatform.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ShadowCopyRole.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SkillBlindingShieldSummon.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SkillRoleItem.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SkirmisherGuanyuSprint.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SkirmisherHadesHiding.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SkirmisherSmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SnowGirlBall.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SnowGirlSnowMan.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SungodBurn.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SungodFly.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SupperAidMeiHealingBot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SupperNeptuneShield.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/SupperSmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TaigaBomb.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TaigaShield.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TaigaShieldHpStateEffect.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TangSengGunFire.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TangSengSpell.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TigaHope.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/TigaZepellionRay.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/UltraFightGutsAirStrike.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/UltramanShot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfHide.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfHowl.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfKillerAutoAim.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfManJump.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfManPower.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/WolfSmoke.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZeroEmerium.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZeroWideshot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZetaBlink.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZetaShot.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZhuGeLiangArrowTowers.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillImpl/ZhuGeLiangBaGuaZhen.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillPart.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillState.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/SkillEventManager.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/SkillTimeData.cs` |
| `Assets/Script/UI/War/Role/RoleSkill/SkillTimeUpdate.cs` |

## 备注

依赖：[[role-base]]、[[buff-framework]]
