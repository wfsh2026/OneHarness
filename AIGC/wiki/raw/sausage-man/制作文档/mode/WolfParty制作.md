# 1 代架构狼人派对（WolfParty）制作规范

> **适用范围**：WolfParty 狼人派对 — 新增角色状态 / 扩展 Malou 子模式 / 调整非对称对抗
> **不适用**：通用模式框架 → 归 [[模式制作]]
> **参考实现**：mode-wolfparty（111 文件，★★★ 复杂，ExtendGameWorldFeature + 非对称对抗 + Malou 子模式 + 武器商店）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **架构差异**：⚠️ 使用 `ExtendGameWorldFeature` + `AbsWolfPartyMgr` + StateMgr（非 ModeManager + Stage）
> **GameMode 枚举**：`LimitedtimeWolfparty=17`（变体：31,41,67）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientWolfPartyMain (Client 端狼人派对主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/WolfParty/ClientWolfPartyMain.cs
  │  继承: AbsWolfPartyMgr（非 ClientModeManager）
  │  架构: ExtendGameWorldFeature
  │
  ├── ClientWolfPartyStateMgr（State 管理器 — 替代 Stage 系统）★
  │     ├── ClientWolfPartyBornState     — 出生
  │     ├── ClientWolfPartyReadyState    — 准备
  │     ├── ClientWolfPartyMoonState     — 月亮阶段 ★ 独有
  │     ├── ClientWolfPartyBattleState   — 战斗
  │     ├── ClientWolfPartyWinWaitState  — 胜利等待
  │     └── ClientWolfPartyOverState     — 结束
  │
  ├── Logic 层（6 个 + Malou 4 个）
  │     ClientWolfPartyDataLogic          — 数据同步
  │     ClientWolfPartyRoleLogic          — 角色管理
  │     ClientWolfPartyBoxLogic           — 箱子交互
  │     ClientWolfPartyShoppingLogic      — 商店购买
  │     ClientWolfpartyHurtNumLogic       — 伤害数字
  │     ├── Malou 子模式 Logic
  │     │     ClientMaloPartyBoxLogic         — Malou 箱子
  │     │     ClientMaloPartyEvolutionLogic   — Malou 进化
  │     │     ClientMaloPartyMusicLogic       — Malou 音乐
  │     │     ClientMaloPartySpeedAreaLogic   — Malou 速度区域
  │
  └── ClientWolfPartyData

ServerWolfPartyMain (Server 端狼人派对主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/WolfParty/ServerWolfPartyMain.cs
  │  继承: AbsWolfPartyMgr
  │
  ├── ServerWolfPartyStateMgr（State 管理器）
  │     6 个 Server State（Born/Ready/Moon/Battle/WinWait/Over）
  │
  ├── Logic 层（12 个 + Malou 7 个）★★
  │     ServerWolfPartyDataLogic          — 数据处理
  │     ServerWolfPartyBoxLogic           — 箱子逻辑
  │     ServerWolfPartyEvolutionLogic     — 进化系统 ★
  │     ServerWolfPartyMapLogic           — 地图管理
  │     ServerWolfPartyRoleLogic          — 角色逻辑
  │     ServerWolfPartyWeaponLogic        — 武器系统
  │     ServerWolfPartyStatisticsData     — 统计数据
  │     ├── Malou 子模式 Logic（7 个）
  │     │     ServerMaloPartyBoxLogic
  │     │     ServerMaloPartyEvolutionLogic
  │     │     ServerMaloPartyRoleLogic
  │     │     ServerMaloPartyRoleLogic_Evolution
  │     │     ServerMaloPartyRulerLogic
  │     │     ServerMaloPartySpeedAreaLogic
  │
  └── WolfPartyServerData

Host 层 — AbsWolfPartyMgr
    WolfPartyLogicMgr — 逻辑管理器
    WolfPartyRoleState 枚举:
      Normal(0)      — 普通人类
      WolfKiller(1)  — 猎人
      Wolf(2)        — 狼人
      WolfKing(3)    — 狼王

非对称对抗核心 ★★★
    角色转换 Buff:
      BSWolfTransformClient — 客户端狼人变身
      BSWolfTransformServer — 服务端狼人变身
    进化系统:
      ServerWolfPartyEvolutionLogic — 进化点追踪
    武器系统:
      WolfPartyWeaponConfig (16 参数: 伤害/装配件/子弹数等)
      WolfPartyWeaponStoreConfig — 武器商店

Malou 子模式 ★★
    独立目录: MaloFeature/
    独立配置: SOWolfPartyConfig_Malo / SOWolfPartyBox_Malo
    条件分支: if (IsMaloFeature) { AddMaloLogics(); }
    特有机制: 移动平台 / 速度区域 / 独立进化规则
```

### 1.2 State 阶段流转

```
6 State 制（使用 StateMgr 而非 Stage 系统）：
★ WolfParty 使用 IWolfPartyState 接口 → AbsWolfPartyState → 具体 State

Born (1) — 出生
  │  生成玩家角色
  │  初始化装备
  ↓
Ready (2) — 准备
  │  阵营分配（人类/狼人/猎人）
  │  武器商店开放
  ↓
Moon (3) — 月亮阶段 ← ★ WolfParty 独有
  │  狼人变身动画
  │  月光效果
  │  阵营揭示
  ↓
Battle (4) — 战斗
  │  非对称对抗：
  │    人类 vs 狼人 vs 猎人
  │    狼人击杀人类 → 人类变狼
  │    猎人辨识并击杀狼人
  │    进化系统：击杀获得进化点
  │  判定：某阵营全灭 / 时间到
  ↓
WinWait (5) — 胜利等待
  │  展示获胜阵营
  ↓
Over (6) — 结束
    结算/排名
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **主配置** | `SOWolfPartyConfig.asset` | Resources/AB | Init |
| **Malou 配置** | `SOWolfPartyConfig_Malo.asset` | Resources/AB | Init（Malou） |
| **地图集** | `SOWolfPartyMapSet1/2/Malo.asset` (3 个) | Resources/AB | Born |
| **箱子配置** | `SOWolfPartyBox.asset` / `_Malo.asset` | Resources/AB | Born |
| **武器配置** | `WolfPartyWeaponConfig` Txt | TextAsset | Init |
| **商店配置** | `WolfPartyWeaponStoreConfig` Txt | TextAsset | Init |
| **评分配置** | `SOWolfPartyScore.asset` | Resources/AB | Over |
| **音效** | `SOWolfPartySoundAndParticle.asset` | Resources/AB | 按需 |

---

## 二、新建/扩展 Checklist

### Phase 1：新增角色状态

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `WolfPartyRoleState` | 修改 | 新增枚举值 |
| 2 | 变身 Buff | 新建 | Client + Server 端 |
| 3 | 角色能力 | 新建 | 新状态的技能/属性 |

### Phase 2：扩展 Malou 子模式

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | `MaloFeature/` 新 Logic | 新建 | Client + Server |
| 5 | `SOWolfPartyConfig_Malo` | 修改 | 新配置项 |
| 6 | 条件分支判断 | 修改 | `IsMaloFeature` 路径 |

### Phase 3：调整武器商店

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 7 | `WolfPartyWeaponConfig` | 修改 | 新武器 (16 参数) |
| 8 | `WolfPartyWeaponStoreConfig` | 修改 | 商店商品 |
| 9 | 商店 Logic（Client/Server） | 修改 | 购买流程 |

---

## 三、配置文件详解

### 3.1 武器配置（16 参数）

**配置路径**：`WolfPartyWeaponConfig.txt` / `WolfPartyWeaponConfig_Malou.txt`

```csharp
// WolfPartyWeaponConfig.cs — 16 字段
public class WolfPartyWeaponConfig {
    public readonly string resourcesSign;       // 1. 武器ID
    public readonly string itemName;            // 2. 显示名称
    public readonly float backSpeed;            // 3. 后坐力速度
    public readonly float backDampingSpeed;     // 4. 后坐力阻尼
    public readonly float damageRatio;          // 5. 基础伤害倍率
    public readonly string upperRail;           // 6. 瞄具（上导轨）
    public readonly string muzzle;              // 7. 枪口配件
    public readonly string magazine;            // 8. 弹匣
    public readonly string lowerRail;           // 9. 前握把（下导轨）
    public readonly string stock;               // 10. 枪托
    public readonly string chip;                // 11. 芯片组件
    public readonly int preBullet;              // 12. 标准子弹数
    public readonly float shootDelay;           // 13. 射击间隔（射速）
    public readonly float reloadTime;           // 14. 换弹时间
    public readonly int itemType;               // 15. 物品分类
    public readonly float headDamage;           // 16. 爆头伤害倍率
    public readonly int preBulletMalou;         // Malou专用子弹数
}
```

**商店配置**：`WolfPartyWeaponStoreConfig.txt`

```csharp
// 商店货架 — 每把武器的默认配件组合
public class WolfPartyWeaponStoreConfig {
    public readonly string resourcesSign;       // 武器ID（关联WeaponConfig）
    public readonly string itemName;            // 显示名称
    public readonly string subtabTypeKey;       // 商店分类标签
    public readonly int maxNumber;              // 最大购买数量
    public readonly string upperRail;           // 默认瞄具
    public readonly string muzzle;              // 默认枪口
    public readonly string magazine;            // 默认弹匣
    public readonly string lowerRail;           // 默认前握把
    public readonly string stock;               // 默认枪托
    public readonly string chip;                // 默认芯片
}
```

**购买流程**：
```
CmdWolfPartySendBuyInfo(itemSign, playerId)
  → ServerWolfPartyWeaponLogic.OnBuyEquip()
  → 检查 RunState != Battle（战斗中禁止购买）
  → CreateWeaponByConfig() 创建武器+自动装配全部配件
  → 发送 TargetRpcWolfPartyWeaponAttack 反馈后坐力参数
```

### 3.2 角色状态与能力

```csharp
// AbsWolfPartyMgr.cs 第42-68行
public enum WolfPartyRoleState {
    None = 0,
    Normal,        // 普通人类 — 基础攻击+防御
    WolfKiller,    // 猎人 — 强化攻击+辨识技能
    Wolf,          // 狼人 — 变身攻击+潜伏+感染
    WolfKing,      // 狼王 — 全能力+召唤+统领
}
```

| 状态 | fashionId | 技能来源 | 特殊Buff | 阵营目标 |
|------|-----------|---------|----------|---------|
| Normal | 0 | 无专属技能 | 无 | 存活到最后 |
| WolfKiller | 0~N | `specialRoleSkillConfigList[0]` | `WolfKillerPassive` | 击杀狼人 |
| Wolf | 0~N | `specialRoleSkillConfigList[1]` | `WolfTransform` + `WolfInvicable`（变身短暂无敌） | 感染人类 |
| WolfKing | 0~N | `specialRoleSkillConfigList[2]` | 同 Wolf | 统领狼群 |

**角色转换触发**：
```csharp
// ServerWolfPartyBattleState.cs 第80-107行
// Battle 开始时分配阵营
ChooseWolfKing();  // 按人数规则选狼王（4-6人→1狼王，7-10人→2狼王）
ChooseWolf();      // 剩余狼人名额按随机分配

// 变身时播放 Buff 动画
MyBuffControl.PlayBuff("WolfTransform", roleId);  // 变身动画+僵直
MyBuffControl.PlayBuff("WolfInvicable", roleId);  // 短暂无敌（仅Wolf+WolfKing）
```

### 3.3 SO 配置变体（标准 vs Malou）

| 配置类型 | 标准版 | Malou 版 |
|---------|--------|---------|
| 主配置 | `SOWolfPartyConfig.asset` | `SOWolfPartyConfig_Malo.asset` |
| 箱子配置 | `SOWolfPartyBox.asset` | `SOWolfPartyBox_Malo.asset` |
| 地图集 | `SOWolfPartyMapSet1/2.asset` | `SOWolfPartyMapSet_Malo.asset` |
| 积分配置 | `SOWolfPartyScore.asset` | `SOWolfPartyScore_Malo.asset` |
| 音效/粒子 | `SOWolfPartySoundAndParticle.asset` | `SOWolfPartySoundAndParticle_Malo.asset` |

---

## 四、关键代码修改点

### 4.1 State 阶段与 Moon 相位

**WolfParty 6 阶段流转**：

```csharp
public enum WolfPartyState {
    None, Born, Ready, Moon, Battle, WinWait, Over
}

// Moon 阶段实际作用：纯计时器（无特殊机制）
// ServerWolfPartyMoonState.cs
public class ServerWolfPartyMoonState : AbsWolfPartyState {
    public override void OnStart() {
        nextStateTime = gameWorld.MyStartGame.ServerTime + serverData.GetStateTime();
    }
    public override void OnUpdate(float delta) {
        if (gameWorld.MyStartGame.ServerTime >= nextStateTime) {
            NextState();  // → Battle
        }
    }
}

// ⚠️ 身份分配不在 Moon 而在 Battle.OnStart()
// ServerWolfPartyBattleState.cs 第80-107行
public override void OnStart() {
    ChooseWolfKing();  // 按人数规则选狼王
    ChooseWolf();      // 分配剩余狼人
}
```

**Moon 阶段定位**：
- 客户端播放月亮动画/VFX
- 网络同步缓冲（等待所有客户端就绪）
- 实际身份分配发生在 Battle.OnStart()

### 4.2 非对称对抗 — 角色转换与感染

```csharp
// 角色状态变更（ServerWolfPartyRoleLogic.cs 第150-177行）
if (state >= WolfPartyRoleState.WolfKiller) {
    int index = state - WolfPartyRoleState.WolfKiller;  // 0=猎人, 1=狼人, 2=狼王
    var skillConfig = roleLogic.WolfPartyRoleSOData.specialRoleSkillConfigList[index];
    var config = skillConfig.data[fashionId];
    // 装备专属技能
    gameWorld.ServerSkillManager.SetSkill(
        playerID, config.skillIndex, config.skillConfigName, false, false);
    // 变身 Buff 动画
    MyBuffControl.PlayBuff("WolfTransform", roleId);     // 僵直+变身
    if (state >= WolfPartyRoleState.Wolf)
        MyBuffControl.PlayBuff("WolfInvicable", roleId); // 短暂无敌
}

// 感染追踪（Proto32 ID 32022）
TargetRpcWolfPartyAddWolfInfect { infectCount }  // 累计感染次数
RpcWolfPartyShowWolfInfect { attackRoleId, deadRoleId } // 感染动画全场广播
```

### 4.3 进化系统（100 分进化）

**核心逻辑**：`ServerWolfPartyEvolutionLogic.cs`

```csharp
// 进化点积累
private void MsgAddWolfEvolution(Body bd, WolfPartyAddEvolution info) {
    int resultPoint = role.roleLogicServer.wolfEvolution + info.AddPoint;
    role.roleLogicServer.wolfEvolution = resultPoint;

    // ⭐ 阈值判定：100 分 = 进化
    if (resultPoint >= 100) {
        if (role.GetWolfPartyRoleState == WolfPartyRoleState.Wolf) {
            // Wolf → WolfKing 进化！
            DispatchMessage(OnWolfPartyTargetRoleStateChange,
                role.AutoRoleId, WolfPartyRoleState.WolfKing, fashionId);
        }
    }
    // 同步客户端
    TargetRpc(new TargetRpcWolfPartyWolfEvolution {
        evolutionPoint = resultPoint, roleId = info.RoleId
    }, role.MyRoleNet);
}

// 回合间重置
private void MsgClearWolfEvolution() {
    role.roleLogicServer.wolfEvolution = 0;
}
```

**进化点来源**：击杀人类、感染人类（具体分值由 SO 配置）

### 4.4 Malou 子模式双轨进化

**路径**：`Server/Modules/WolfParty/MaloFeature/`（7 个 Server Logic）

```csharp
// Malou 双轨进化（ServerMaloPartyRoleLogic_Evolution.cs 第60-99行）
// 两条独立进化轨道：
//   MaloEvolution   — 妖王进化（对应 SuperMaloKing）
//   SoldierEvolution — 战士进化（对应 SuperSoldierKing）

public void FixEvolutionPoint(int roleId, WolfPartyRoleState nowState, int fashionId) {
    switch (nowState) {
        case Wolf:
            MaloEvolution = 0; SoldierEvolution = 0;  // 重置双轨
            break;
        case WolfKing:
            var needPoint = MaloPartyUtils.GetNeedPoint(
                fashionId == SuperMaloKing ? MaloLevel.SuperKing : MaloLevel.King,
                globalSetting);
            if (MaloEvolution < needPoint) MaloEvolution = needPoint;
            SoldierEvolution = 0;  // 清除另一轨
            break;
        case WolfKiller:
            // 同理处理 Soldier 轨道
            break;
    }
}
```

**Malou 专属 Logic**：

| Logic 类 | 功能 |
|----------|------|
| `ClientMaloPartyBoxLogic` | 替代标准箱子逻辑 |
| `ClientMaloPartyEvolutionLogic` | 双轨进化 UI 显示 |
| `ClientMaloPartySpeedAreaLogic` | 速度区域效果 |
| `ClientMaloPartyMusicLogic` | 动态背景音乐 |
| `ServerMaloPartyRulerLogic` | 统治者计分逻辑 |
| `ServerMaloPartyPlatformLogic` | 移动平台机制 |

### 4.5 Proto32 网络协议

**API ID = 32**，关键消息（`Proto_WolfParty.cs`）：

| 消息 ID | 类型 | 名称 | 用途 |
|---------|------|------|------|
| 32001 | ClientRpc | `RpcWolfPartySetStage` | 阶段同步 |
| 32002 | ClientRpc | `RpcWolfPartyRoundData` | 回合数据 |
| 32003 | Cmd | `CmdWolfPartySendBuyInfo` | 购买武器 |
| 32007 | Cmd | `CmdWolfPartyChangeSausageKing` | 香肠王变身 |
| 32008 | TargetRpc | `TargetRpcWolfPartyWeaponAttack` | 射击后坐力（dir, backSpeed, backDampingSpeed） |
| 32009 | ClientRpc | `RpcWolfPartyBox` | 箱子分布 |
| 32010 | Cmd/Rpc | `CmdWolfPartyGetBoxItem` | 箱子交互 |
| 32013 | Cmd | `CmdWolfPartySellItem` | 出售武器 |
| **32015** | **ClientRpc** | **`RpcWolfPartyChangeRoleState`** | **身份揭示**（roleId, state, fashionId） |
| 32019 | TargetRpc | `TargetRpcWolfPartyWolfChangeLife` | 狼人生命状态 |
| **32022** | **TargetRpc** | **`TargetRpcWolfPartyAddWolfInfect`** | **感染计数** |
| 32024 | ClientRpc | `RpcWolfPartyShowWolfInfect` | 感染动画全场广播 |
| 32026 | ClientRpc | `RpcWolfPartyPlayerHurt` | 伤害数字 |

---

## 五、常见问题与踩坑记录

### 5.1 狼人变身后碰撞体不一致

**现象**：变身为狼人后角色大小改变但碰撞体未更新

**根因**：`BSWolfTransformClient` 只更新了模型但未更新 Collider

**解决方案**：在变身 Buff 的 OnApply 中同步更新 CharacterController 的 height/radius

### 5.2 Malou 子模式 Logic 与标准 Logic 冲突

**现象**：启用 Malou 后某些标准功能异常

**根因**：`ServerMaloPartyBoxLogic` 与 `ServerWolfPartyBoxLogic` 同时注册，处理同一事件

**解决方案**：Malou 启用时移除标准 BoxLogic，确保互斥注册

### 5.3 Moon 阶段网络延迟导致提前泄露身份

**现象**：Moon 阶段还未结束，部分玩家已看到谁是狼人

**根因**：变身 RPC 发送时间不一致，部分客户端提前收到

**解决方案**：Moon 阶段开始时统一加黑屏遮罩，RPC 全部到达后才揭示

---

## 六、验收标准

- [ ] 6 State 正常流转（Born→Ready→Moon→Battle→WinWait→Over）
- [ ] 4 种角色状态正确分配/转换
- [ ] 非对称对抗机制正确（狼人感染/猎人辨识）
- [ ] 武器商店购买/装备正常
- [ ] 进化系统正确（击杀→进化点→能力提升）
- [ ] Malou 子模式独立运行
- [ ] 3 张地图正常加载
- [ ] Moon 阶段变身同步
- [ ] Proto 32 协议正常（Stage同步/购买/伤害）

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-wolfparty]]
