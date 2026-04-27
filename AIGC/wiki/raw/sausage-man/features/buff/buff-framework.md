---
name: buff-framework
display_name: Buff 框架层
category: buff
version: 1.0.0
dependencies: []
---

# Buff 框架层

1代 Buff 系统核心框架，包含 BuffSystemBase（逻辑路由）、BuffBox（运行时实例）、BuffSOBase（SO 配置）、BuffControl（全局管理）等基类和接口。所有具体 Buff 均继承自此框架。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/BuffControl/BuffSystemBase.cs` |
| `Assets/Script/UI/War/BuffControl/BuffBox.cs` |
| `Assets/Script/UI/War/BuffControl/BuffSOBase.cs` |
| `Assets/Script/UI/War/BuffControl/BuffControl.cs` |
| `Assets/Script/UI/War/BuffControl/HpBuffSystemBase.cs` |
| `Assets/Script/UI/War/BuffControl/HpBuffSOBase.cs` |
| `Assets/Script/UI/War/BuffControl/IAddExtraHp.cs` |
| `Assets/Script/UI/War/BuffControl/IBuffHp.cs` |
| `Assets/Script/UI/War/BuffControl/BuffSpeedSOBase.cs` |
| `Assets/Script/UI/War/BuffControl/BuffSpeedSO.cs` |
| `Assets/Script/UI/War/BuffControl/SceneBuff.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/BuffAsset.txt` |
| `Assets/ToBundle/Config/Txt/AddEffectBuffSkinData.txt` |
| `Assets/ToBundle/Config/Txt/SeasonScoreBuff.txt` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffBoxClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/AbsBSFallDownBuffClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/AbsBSOnTriggerEnterBuffClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddBirthSyncMusicClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddWeekendPeakRankingStageClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAidMeiStageClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCarrierClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDemonMacheteClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSExpressionClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGiantBattleClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoodsBoxClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGuanyuSpinClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGuanyuSprintClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSHolographicImageClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSHotBombFlyClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSKillballonClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSLightningBombClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMonsterCashCarClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMonsterClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMotionPlatformClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSNinjaShadowCopyClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSOBossSceneAirWallClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuFlyAirOneStageClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuFlyAirSecondStageClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPaoKuRollClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPropertyAdditionClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveMonsterSkillClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRainbowBridgeClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRoleHypoxiaClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRoleStateChangeClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSceneDeadItemBoxClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSendPointClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSendPointYClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSShadowCopyRoleClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSlimeClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSlimeDinoBabyClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSlimeNianClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSnowGirlBallClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSSnowGirlSnowManClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaBombCastPointClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaBombClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTaigaShieldClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTigaHopeClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTigaZepellionRayClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTransferClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTreasureStoneClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSUnderWaterClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSWuLinHotelClient.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystemClientBase.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/ClientBuffFeatureManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGiantBattle.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSOnTriggerEnterBuff.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSSlimePickItem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/AceSdk/AceSdkManagerServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffBoxServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/AbsBSFallDownBuffServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddBirthSyncMusicServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddWeekendPeakRankingStageServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAidMeiStageServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBuffTrapServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCarrierServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDemonMacheteServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSExpressionServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGiantBattleServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoodsBoxServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGuanyuSpinServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGuanyuSprintServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSHolographicImageServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSHotBombFlyServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSKillballonServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSLightningBombServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMonsterCashCarServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMonsterItemServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMonsterServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMotionPlatformServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSNinjaShadowCopyServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuFlyAirOneStageServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuFlyAirSecondStageServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPaoKuRollServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPropertyAdditionServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveAttrConsumeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveMonsterSkillServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRainbowBridgeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRoleHypoxiaServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRoleStateChangeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSendPointServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSendPointYServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSShadowCopyRoleServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSlimeDinoBabyServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSlimeNianServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSlimePickItemServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSlimeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSnowGirlBallServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSSnowGirlSnowManServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaBombCastPointServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaBombServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTaigaShieldServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTigaHopeServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTigaZepellionRayServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTransferServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTreasureStoneServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSUnderWaterServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSWuLinHotelServer.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/PveTotemBuffSystemServerBase.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/ServerBSDownHpObjLink.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystemServerBase.cs` |

## 备注

三层架构: BuffSOBase(配置层SO) → BuffSystemBase(逻辑层,路由InitServer/InitClient) → BuffBox(运行时容器)。BuffControl : AbsBaseGameWorldFeature 为 BattleWorld 单例管理器。框架位于 UI/War/BuffControl/(11文件) 而非 GamePlay/。

设计模式: Factory Method(BuffSOBase.init()→BuffSystemBase), Template Method(Init→InitServer/InitClient), Strategy(RequestServer<T>/RequestClient<T>), Observer(OnChangePointCallBack), Repository(BuffControl 18+查询方法), Decorator(AddHpBuffSystemBase护盾)。

核心类: BuffSystemBase(所有Buff逻辑基类, key_methods: Init/InitServer/InitClient/RequestServer<T>/RequestClient<T>/OnUpdate/Clear), BuffBox(运行时容器, key_methods: AddBuff/SetBuffData/BuffEnd, SyncState枚举8种: Range/RangeXZ/TeamAndRange/Team/OnlyServer/OnlySelf/World/Custom), BuffSOBase(SO配置基类, key_methods: init→BuffSystemBase/checkCanUser), BuffControl(全局管理器, key_methods: PlayBuff/RemoveBuff/GetBuff/GetBuffsBySign/GetBuffByType<T>, base: AbsBaseGameWorldFeature), HpBuffSystemBase(可破坏Buff, key_methods: ServerDownHp/ServerSetHp/ClientDownHp, key_fields: Hp/HPOverBuff[]/weaponHitRatio[]), AddHpBuffSystemBase:IAddExtraHp(护盾吸收, key_methods: SetDownHp/InitHpValue), BuffSpeedSOBase(速度Buff, AddSpeedRatio接口), SceneBuff(场景Buff触发器MonoBehaviour)。

接口: IBuffSystemBase(Init/Clear/OnUpdate/GetCustomSyncList), IBuffBox(Init/Clear/OnUpdate/BuffEnd), IBuffDownHpServer(ServerDownHp), IBuffDownHpClient(GetBuffHits/ClientDownHp), IAddExtraHp(IsOpenAddHp/AddHpValue/SetDownHp), BuffSpeedSO(AddSpeedRatio)。

集成点: gameWorld.BuffControl(全局入口), ServerBuffControl/ClientBuffControl(端侧管理), role.MyRoleBuffControl.addBuffEffect()(角色Buff效果), BattleWorld.ServerBuffControl.SyncDownHpObj()(HP同步)。

资源加载链: BuffControl.PlayBuff(sign) → AssetsLoad.GetSOBuffData(sign) → BuffAssetConfig.Get(sign) → AssetManager.LoadAsset<BuffSOBase>("Assets/ToBundle/ScriptableObject/Buff/{path}/{id}.asset") → buffBox.AddBuff(buffSO) → buff.init(this) → BuffSystemBase.Init → InitServer/InitClient。

## 关联 Buff


### 战斗 Buff（15）

| feature | 说明 |
|---------|------|
| [[buff-add-hp-for-time]] | BSAddHPForTime - 持续回血/掉血DoT/HoT |
| [[buff-attack-effect]] | BSAttackEffect - 攻击特效 |
| [[buff-beat-back]] | BSBeatBack - 击退 |
| [[buff-blast-bomb]] | BSBlastBomb - 爆炸触发 |
| [[buff-bomb-area]] | BSBombArea - 范围爆炸含间隔 |
| [[buff-c4bomb]] | BSC4Bomb - C4定时炸弹 |
| [[buff-circle-trigger-damage]] | BSCircleTriggerDamage - 圆形触发伤害区域 |
| [[buff-client-bomb]] | BSClientBomb - 爆炸伤害+击飞+视觉 |
| [[buff-down-hp-box]] | BSDownHpBox - 陷阱箱伤害 |
| [[buff-down-hp-obj]] | BSDownHpObj - 可破坏物体 |
| [[buff-gun-bayonet]] | BSGunBayonet - 枪刺近战 |
| [[buff-infinite-pack-bullet]] | BSInfinitePackBullet - 无限弹匣 |
| [[buff-line-bullet]] | BSLineBullet - 直线连线伤害 |
| [[buff-range-down-hp]] | BSRangeDownHp - 范围持续伤害 |
| [[buff-rapid-punches]] | BSRapidPunches - 连续拳击多阶段 |

### 移动 Buff（7）

| feature | 说明 |
|---------|------|
| [[buff-eight-dir-dash]] | BSEightDirDash - 八方向冲刺+拖尾 |
| [[buff-gaunlet-dash]] | BSGaunletDash - 拳套冲刺含伤害 |
| [[buff-gaunlet-recover-hit]] | BSGaunletRecoverHit - 拳套打击恢复护盾 |
| [[buff-glide-move-py]] | BSGlideMovePY - 滑翔/模拟风移动 |
| [[buff-line-move]] | BSLineMove - 直线移动投射物 |
| [[buff-manual-add-speed]] | BSManualAddSpeed - 手动增加速度 |
| [[buff-move-speed-ratio]] | BSMoveSpeedRatio - 速度倍率 |

### 视觉 Buff（9）

| feature | 说明 |
|---------|------|
| [[buff-add-effect-by-param]] | BSAddEffectByParam - 参数化特效加载（从 buffSyncInfo JSON 反序列化 EffectSign） |
| [[buff-add-effect-obj]] | BSAddEffectObj - 加载特效物体（最常用的特效 Buff 基类） |
| [[buff-add-game-obj]] | BSAddGameObj - 加载游戏物体（直接引用 GameObject） |
| [[buff-add-server-scene-obj]] | BSAddServerSceneObj - 服务器场景物体生成 |
| [[buff-art-range]] | BSArtRange - 美术范围指示器显示 |
| [[buff-fire-obj]] | BSFireObj - 火枪/塔防炮台（继承 BSDownHpObj，可被摧毁） |
| [[buff-fixed-fire]] | BSFixedFire - 固定位置轰炸 |
| [[buff-play-for-range]] | BSPlayForRange - 范围触发器（支持凸多边形区域） |
| [[buff-show-hp]] | BSShowHP - 显示血条/Debuff UI |

### 通用 Buff（50）

| feature | 说明 |
|---------|------|
| [[buff-add-h-p-for-limit]] | BSAddHPForLimit - AddHPForLimit |
| [[buff-add-power]] | BSAddPower - AddPower |
| [[buff-adsorb-target]] | BSAdsorbTarget - 吸附锁定目标⚠️Bug |
| [[buff-attracted-blade-ball]] | BSAttractedBladeBall - AttractedBladeBall |
| [[buff-auto-fire-dog-tag]] | BSAutoFireDogTag - 自动开火 |
| [[buff-beat-beast-camp-lock-item]] | BSBeatBeastCampLockItem - 打野营地锁定 |
| [[buff-beat-beast-transport-point]] | BSBeatBeastTransportPoint - 打野传送点 |
| [[buff-blinding-shield]] | BSBlindingShield - BlindingShield |
| [[buff-blinding-shield-summon]] | BSBlindingShieldSummon - BlindingShieldSummon |
| [[buff-bomb-move]] | BSBombMove - BombMove |
| [[buff-boss-scene-air-wall]] | BSBossSceneAirWall - BossSceneAirWall |
| [[buff-buff-baby-bottle]] | BSBuffBabyBottle - 婴儿奶瓶 |
| [[buff-buff-create-car]] | BSBuffCreateCar - Buff触发生成载具 |
| [[buff-captain-card-ghost]] | BSCaptainCardGhost - 队长卡灵体 |
| [[buff-captain-card-hot]] | BSCaptainCardHot - 队长卡热卡前摇 |
| [[buff-captain-card-recovery]] | BSCaptainCardRecovery - 队长卡恢复 |
| [[buff-circle-trigger-damage-buff]] | BSCircleTriggerDamageBuff - CircleTriggerDamageBuff |
| [[buff-clown-platform]] | BSClownPlatform - 小丑平台同BSSandPlatform结构 |
| [[buff-create-battery-turret]] | BSCreateBatteryTurret - 部署炮台无特殊字段 |
| [[buff-create-buff]] | BSCreateBuff - CreateBuff |
| [[buff-create-fire-wall]] | BSCreateFireWall - 创建火墙 |
| [[buff-create-item]] | BSCreateItem - CreateItem |
| [[buff-crystalball]] | BSCrystalball - 水晶球减速 |
| [[buff-delivery-cannon]] | BSDeliveryCannon - 传送炮台 |
| [[buff-drop-level]] | BSDropLevel - 等级下降 |
| [[buff-dungeon-room]] | BSDungeonRoom - DungeonRoom |
| [[buff-fairy-stick]] | BSFairyStick - 仙女棒 |
| [[buff-feeding-bottle-revive]] | BSFeedingBottleRevive - 奶瓶复活自救 |
| [[buff-frozen-blade-ball]] | BSFrozenBladeBall - FrozenBladeBall |
| [[buff-guts-air-strike]] | BSGutsAirStrike - GutsAirStrike |
| [[buff-hades-fire-wall]] | BSHadesFireWall - 冥界火墙地形检测 |
| [[buff-holy-sword-slash]] | BSHolySwordSlash - HolySwordSlash |
| [[buff-is-in-water]] | BSIsInWater - 水中标记无字段 |
| [[buff-kadura-power]] | BSKaduraPower - KaduraPower |
| [[buff-mind-control]] | BSMindControl - 精神控制三阶段 |
| [[buff-out-control]] | BSOutControl - OutControl |
| [[buff-pet-cut-down-cd]] | BSPetCutDownCd - 宠物冷却缩减Client |
| [[buff-radar]] | BSRadar - 雷达扫描 |
| [[buff-recon-passive-skill]] | BSReconPassiveSkill - 侦察被动 |
| [[buff-restrict-role-move]] | BSRestrictRoleMove - RestrictRoleMove |
| [[buff-role-in-low-gravity]] | BSRoleInLowGravity - RoleInLowGravity |
| [[buff-role-swap]] | BSRoleSwap - 角色位置互换 |
| [[buff-role-trajectory]] | BSRoleTrajectory - 角色轨迹追踪 |
| [[buff-sand-platform]] | BSSandPlatform - 沙地平台升降 |
| [[buff-sg-fast]] | BSSGFast - 快速射击被动 |
| [[buff-skill-forward-time]] | BSSkillForwardTime - 技能前置时间 |
| [[buff-sneak-sand]] | BSSneakSand - 潜沙★34字段: rotateSpeed/powerRecoveryTime/powerCostTime/wallWaitTime/animationCurve/inSandEffect/endSandEffect等 |
| [[buff-summon-shen-long]] | BSSummonShenLong - 召唤神龙多阶段 |
| [[buff-support-passive-skill]] | BSSupportPassiveSkill - 辅助被动加速回血 |
| [[buff-thundetalisman]] | BSThundetalisman - 雷符眩晕 |

### 道具 Buff（23）

| feature | 说明 |
|---------|------|
| [[buff-action-trigger]] | BSActionTrigger - 动作触发器 |
| [[buff-broken-floor]] | BSBrokenFloor - 地板破碎 |
| [[buff-circle-game]] | BSCircleGame - 圆形节奏小游戏Client |
| [[buff-escape-point]] | BSEscapePoint - 逃脱点 |
| [[buff-firework-chest]] | BSFireworkChest - 烟花宝箱 |
| [[buff-gold-chest]] | BSGoldChest - 黄金宝箱 |
| [[buff-joker-statue]] | BSJokerStatue - 丑角雕像交互 |
| [[buff-lobby-shoot-game]] | BSLobbyShootGame - 大厅射击小游戏★完整系统 |
| [[buff-on-trigger-enter-buff]] | BSOnTriggerEnterBuff - 碰撞体进入触发 |
| [[buff-play-box-line]] | BSPlayBoxLine - 箱子连线解谜 |
| [[buff-play-dance]] | BSPlayDance - 跳舞 |
| [[buff-props-trigger]] | BSPropsTrigger - 道具特效触发 |
| [[buff-red-packet-rain-npc]] | BSRedPacketRainNpc - 红包雨NPC |
| [[buff-red-packet-rain-player]] | BSRedPacketRainPlayer - 红包雨玩家 |
| [[buff-red-packet-rain-point]] | BSRedPacketRainPoint - 红包雨掉落点 |
| [[buff-red-temp-zone-level]] | BSRedTempZoneLevel - 红色临时区域等级 |
| [[buff-repair-equip]] | BSRepairEquip - 修复装备 |
| [[buff-repair-item]] | BSRepairItem - 修复机器人 |
| [[buff-replace-weapon]] | BSReplaceWeapon - 武器替换站 |
| [[buff-seat-area]] | BSSeatArea - 座位区域 |
| [[buff-trigger-trap]] | BSTriggerTrap - 主动触发机关 |
| [[buff-wander-nova-ship]] | BSWanderNovaShip - 流浪超新星飞船 |
| [[buff-wealth-god]] | BSWealthGod - 财神NPC |

### 防御 Buff（5）

| feature | 说明 |
|---------|------|
| [[buff-defense-shield]] | BSDefenseShield - 防御护盾含跟随/载具偏移 |
| [[buff-pet-skill-bubble]] | BSPetSkillBubble - 宠物技能气泡 |
| [[buff-role-shield]] | BSRoleShield - 角色护盾 |
| [[buff-shield-pawn]] | BSShieldPawn - 盾兵护盾 |
| [[buff-shield-soldier]] | BSShieldSoldier - 士兵护盾含反弹 |
