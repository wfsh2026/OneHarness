---
name: throwable-bomb
display_name: 投掷物系统
category: throwable
version: 1.0.0
dependencies:
- weapon-base
- weapon-bullet
---

# 投掷物系统

手雷/烟雾弹/治疗弹/爆破炸弹(C4)等投掷物：RoleSkillBomb 技能投掷基类、BombLineRender 抛物线弧线渲染与碰撞预判、BSClientBomb/BSOClientBomb 爆炸伤害(BombRange/BombHurt/StrikeFly击飞)、RoleBombMove 击飞物理(弹簧模型)、BSBlastBomb 可拆除C4炸弹(60s倒计时)、ThrowGrenadeState 投掷动画状态机

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillBomb.cs [投掷技能基类 — OnDownSkill拉弧线/OnUpSkill释放投掷/CmdUseSkill网络同步]` |
| `Assets/Script/UI/War/Weapon/BombLineRender.cs [抛物线渲染 — 768行, LineRenderer弧线+碰撞预判+可投掷判定]` |
| `Assets/Script/UI/War/Weapon/BombLinePreview.cs [落点预览 — EndPointBox/SandCastleCollider碰撞检测]` |
| `Assets/Script/UI/War/Weapon/BoomObjTime.cs [炸弹倒计时对象 — 场景内时间显示]` |
| `Assets/Script/UI/War/Weapon/BombCutTime.cs [手雷使用倒计时UI — fillAmount进度条+Weapon_图标]` |
| `Assets/Script/UI/PlayerControl/UIBomb.cs [投掷物HUD — 手雷图标/数量/切换列表/选中高亮]` |
| `Assets/Script/UI/PlayerControl/GrenadesItem.cs [手雷列表项 — Item_图标+数量+点击选择]` |
| `Assets/Script/GamePlay/Client/Motion/ThrowGrenadeState.cs [投掷动画状态 — StateMachineBehaviour, Animator事件]` |
| `Assets/Script/GamePlay/Host/Modules/Role/RoleBombMove.cs [击飞物理系统 — 179行, BombMoveData/BombMoveConfig弹簧模型]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClientBomb.cs [爆炸Buff核心 — GetBombRange(PVE加成)/InitServer/InitClient]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBlastBomb.cs [爆破炸弹Buff — C4类型, 可拆除]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSC4Bomb.cs [C4炸弹Buff — bombTime倒计时/defuseBombDistance]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBombArea.cs [轰炸区域Buff — 毒圈缩圈机制]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClientBomb.cs [爆炸SO — BombRange/BombHurt/DelayBombTime/IsStrikeFly/StrikeFlyTarget枚举]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBlastBomb.cs [爆破SO — bombTime/refreshTime/removeRange/BlastBombEffect]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOC4Bomb.cs [C4 SO — bombTime/defuseBombDistance/C4SetAudioSign]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBombArea.cs [轰炸区SO — BombDuration/BombInterval/BombArea/BombDelay]` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBombMove.cs [击飞配置SO — StartBombSpeed/UpRatio/DownRatio/GroundDragRatio/AirDragRatio/StopSpeed]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClientBombServer.cs [爆炸Server — 151行, SetFireRoleBombHurt/AddBuffEffectCheck/AddBombMove]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBlastBombServer.cs [爆破Server — Init/OnUpdate倒计时/Clear]` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSC4BombServer.cs [C4 Server端]` |
| `Assets/Script/GamePlay/Server/Modules/Features/GameWorld/Base/ServerBombAreaManager.cs [轰炸区管理 — 393行, BombAreaState状态机(None/BombDeploy/BombTime/BombOver)]` |
| `Assets/Script/GamePlay/Client/Modules/Features/GameWorld/ClientBombAreaManager.cs [轰炸区客户端 — 320行, PlayBombWarningEffect/ShowBombEffect]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBlastBombClient.cs [爆破Client — UI倒计时/F键拆除提示]` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClientBombClient.cs [爆炸Client端]` |
| `Assets/Script/GamePlay/Client/Modules/Mode/CommonMode/Mono/BlastBombAreaMono.cs [爆破区域Mono — 场景视觉表现]` |
| `Assets/Script/GamePlay/Host/Modules/Bomb/BombDataInterface.cs [轰炸数据接口 — GetBombData/GetYuanPoint圆内随机点]` |
| `Assets/Script/UI/War/HitType/BombArea.cs [爆炸区域标记 — MonoBehaviour场景组件]` |
| `Assets/Script/UI/War/SO/SOBombAreaEffect.cs [轰炸特效配置 — MonoBehaviour]` |
| `Assets/Script/Data/PlayableAnimData/TimelineEventDefine.cs [ThrowGrenade Timeline事件参数]` |

## 配置文件

| 路径 |
|------|
| `Assets/Script/Config/BombLineRenderConfig.cs [抛物线配置类 — SkillSign/AddSpeed/AddHeight/Gravity/MaxLength/PointLength/IsCheckCollider/IsHook/Width]` |
| `Assets/ToBundle/Config/Txt/BombLineRender.txt [抛物线配置表 — Tab分隔, 每行一个技能的弧线物理参数]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/GamePlayItem/PickItems/Grenade.prefab [标准手雷预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/GrenadeMax.prefab [超级手雷预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/FireGrenade.prefab [燃烧弹预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/SandGrenade.prefab [沙砂手雷预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/BlastBomb.prefab [爆破炸弹(C4)预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/DiscoBomb.prefab [迪斯科炸弹预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/SlimeBomb.prefab [史莱姆炸弹预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/LightningBombBullet.prefab [闪电弹子弹预制体]` |
| `Assets/ToBundle/GamePlayItem/PickItems/TotemAddDashBomb.prefab [图腾冲刺炸弹]` |
| `Assets/ToBundle/GamePlayItem/PickItems/TotemEventJumpBomb.prefab [图腾跳跃炸弹]` |
| `Assets/ToBundle/GamePlayItem/PickItems/TotemEventMonsterHpDownBomb.prefab [图腾怪物减血炸弹]` |
| `Assets/ToBundle/ScriptableObject/Buff/ClientBomb/ [爆炸Buff SO — 59个asset]` |
| `Assets/ToBundle/ScriptableObject/Buff/BombMove/ [击飞配置SO — 12个asset]` |
| `Assets/ToBundle/ScriptableObject/Buff/BlastBomb/ [爆破SO — 1个asset]` |
| `Assets/ToBundle/ScriptableObject/Buff/C4Bomb/ [C4 SO — 1个asset]` |
| `Assets/ToBundle/ScriptableObject/Buff/BombArea/ [轰炸区SO — 1个asset]` |
| `Assets/ToBundle/ScriptableObject/Buff/LineMove/ [弧线移动SO — 含Grenade/SandGrenade/DiscoBomb等6个]` |
| `Assets/ToBundle/Effect/WarItem/Bomb/ [投掷物战场特效 — 4个]` |
| `Assets/ToBundle/Effect/Tricks/Pve/Bomber/ [PVE炸弹怪特效 — 64个]` |

## 备注

投掷物分3大类：普通手雷(Bomb=31, 10+种×烟雾/治疗/闪电等变体)、爆破炸弹(BlastBomb=97, C4可拆除)、角色手雷技能(RoleSkillBomb子类6种)。投掷弧线由BombLineRender(768行)驱动LineRenderer抛物线+碰撞预判。爆炸伤害走Buff系统(BSClientBomb/BSBlastBomb/BSC4Bomb)，击飞物理由BSOBombMove→RoleBombMove弹簧模型实现。轰炸区缩圈机制(ServerBombAreaManager 393行)由Server独立管理。Proto_BombArea定义RPC 16001-16007网络协议

依赖：[[weapon-base]] · [[weapon-bullet]]
