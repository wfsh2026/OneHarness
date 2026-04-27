# 1 代架构爆破模式（DefusalMode）制作规范

> **适用范围**：DefusalMode 爆破/拆弹模式 — 新增阶段 / 扩展炸弹机制 / 新增购买商品 / 新增地图
> **不适用**：通用阶段流转框架 → 归 [[模式制作]]；经典 BR → 归 [[mode-classic]]
> **参考实现**：mode-defusal（26 文件，★ 简单，典型回合制对抗模式）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage 基类 / 工厂注册）

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientDefusalModeMgr (Client 端爆破模式主管理器)
  │  路径: Assets/Script/GamePlay/Client/Modules/Mode/DefusalMode/ClientDefusalModeMgr.cs
  │  继承: ClientModeManager
  │  职责: 爆破模式客户端主入口，Stage 管理，数据初始化
  │
  ├── ClientDefusalModeBombLogic
  │     路径: Client/Modules/Mode/DefusalMode/Logic/
  │     职责: C4 炸弹客户端表现（安装进度/拆弹进度/爆炸特效）
  │
  ├── ClientDefusalModeMapLogic
  │     职责: 地图逻辑，炸弹安装点标记，小地图显示
  │
  └── ClientDefusalModeRoleLogic
        职责: 角色阵营显示（攻方/守方），装备 HUD

ServerDefusalModeMgr (Server 端爆破模式主管理器)
  │  路径: Assets/Script/GamePlay/Server/Modules/Mode/DefusalMode/ServerDefusalModeMgr.cs
  │  继承: ServerModeManager
  │  职责: 爆破模式服务端主入口，回合判定，胜负判定
  │
  ├── ServerDefusalModeBombLogic
  │     职责: C4 炸弹服务端判定（安装完成/拆弹完成/爆炸判定/伤害范围）
  │
  ├── ServerDefusalModeMapLogic
  │     职责: 地图安装点管理，出生点分配
  │
  ├── ServerDefusalModeRoleLogic
  │     职责: 角色阵营分配，死亡判定，重生控制
  │
  ├── ServerDefusalModeAwardLogic
  │     职责: 回合奖励/经济系统（击杀奖金/回合胜利奖金）
  │
  ├── ServerDefusalModeMvpLogic
  │     职责: MVP 计算（击杀/拆弹/安装贡献）
  │
  ├── ServerDefusalModeStatisticsLogic
  │     职责: 统计数据（K/D/A/炸弹安装拆除次数）
  │
  └── ServerDefusalModeNsqDataLogic
        职责: NSQ 数据上报

ClientDefusalModeData / ServerDefusalModeData (数据层)
  │  职责: 模式运行时数据存储
  │
  └── DefusalModeDataStruct
        职责: 爆破模式专用数据结构定义

SOData 配置 (ScriptableObject)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/DefusalMode/
  │  3 个配置文件

Proto_DefusalMode (网络协议，继承自 Common)
```

### 1.2 Stage 阶段流转

```
6 阶段制（含独有 ShopStage）：

Born (出生阶段)
  │  攻守双方在各自出生点生成
  ↓
Ready (准备阶段)
  │  倒计时准备，显示阵营信息
  ↓
Shop (商店阶段) ← ★ DefusalMode 独有
  │  玩家使用回合奖金购买武器/装备
  │  继承自 CommonMode 的 BuyWeaponControl
  ↓
Battle (战斗阶段)
  │  攻方目标：安装 C4 并保护至爆炸
  │  守方目标：消灭攻方 或 拆除 C4
  │  判定条件：
  │    ├── 炸弹爆炸 → 攻方胜 (DefusalModeOverType.Bomb)
  │    ├── 炸弹被拆 → 守方胜 (DefusalModeOverType.Defusal)
  │    ├── 时间耗尽 → 守方胜 (DefusalModeOverType.Time)
  │    └── 一方全灭 → 对方胜
  ↓
WinWait (胜利等待)
  │  显示回合结果，等待下一回合
  ↓
Over (游戏结束)
    汇总全局数据，显示 MVP
```

### 1.3 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/DefusalMode/*.asset` | Resources/AB 加载 | Mgr.Init() |
| **商店 UI** | `Assets/ToBundle/UGUI/Windows/War/DefusalShop.prefab` | UIManager.Open() | ShopStage.OnEnter() |
| **炸弹预制体** | `Assets/ToBundle/Items/C4Bomb.prefab` | ItemPool | Battle 阶段 |
| **安装点标记** | 场景内 BombSite 组件 | 场景加载 | 战场初始化 |
| **回合结算 UI** | `Assets/ToBundle/UGUI/Windows/War/DefusalResult.prefab` | UIManager.Open() | WinWait.OnEnter() |

### 1.4 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **CommonMode 的 BuyWeaponControl** — 仅通过配置调整商品，不改购买框架
- **GameMode.cs 已有枚举值** `Defusalmode=34` — 不可修改

---

## 二、新建/扩展 Checklist

### Phase 1：模式注册（已完成，扩展时跳过）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Host/Mode/GameMode.cs` | 已有 | `Defusalmode = 34` |
| 2 | `ClientModeFactory.cs` | 已有 | `AddFeature<ClientDefusalModeMgr>()` |
| 3 | `ServerModeFactory.cs` | 已有 | `AddFeature<ServerDefusalModeMgr>()` |

### Phase 2：新增 Logic 模块

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | `Client/Modules/Mode/DefusalMode/Logic/Client{LogicName}Logic.cs` | 新建 | 继承模式 Logic 基类，在 Mgr.Init() 中注册 |
| 5 | `Server/Modules/Mode/DefusalMode/Logic/Server{LogicName}Logic.cs` | 新建 | 在 ServerDefusalModeMgr.Init() 中注册 |
| 6 | `ClientDefusalModeMgr.cs` | 修改 | Init() 中 `AddLogic(new Client{LogicName}Logic())` |
| 7 | `ServerDefusalModeMgr.cs` | 修改 | Init() 中 `AddLogic(new Server{LogicName}Logic())` |

### Phase 3：新增 Stage 阶段

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `Client/Modules/Mode/DefusalMode/Stage/ClientDefusalMode{StageName}Stage.cs` | 新建 | 继承 Stage 基类 |
| 9 | `Server/Modules/Mode/DefusalMode/Stage/ServerDefusalMode{StageName}Stage.cs` | 新建 | 继承 Stage 基类 |
| 10 | `DefusalModeDataStruct.cs` | 修改 | 新增 Stage 枚举值 |
| 11 | Mgr.cs 双端 | 修改 | 注册新 Stage |

### Phase 4：扩展炸弹机制

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 12 | `ServerDefusalModeBombLogic.cs` | 修改 | 新增炸弹行为（如多点安装、远程引爆） |
| 13 | `ClientDefusalModeBombLogic.cs` | 修改 | 对应客户端表现 |
| 14 | SO 配置 | 修改 | 新增炸弹参数字段 |

### Phase 5：新增地图

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 15 | 场景文件 `.unity` | 新建 | 放置 BombSite 组件标记安装点 |
| 16 | `ServerDefusalModeMapLogic.cs` | 修改 | 注册新地图出生点配置 |
| 17 | SO 配置 | 修改 | 新增地图条目 |

---

## 三、配置文件详解

### 3.1 GameMode 枚举

**路径**：`Assets/Script/GamePlay/Host/Mode/GameMode.cs`

```csharp
public enum GameMode {
    // ...
    Defusalmode = 34,  // 爆破模式
    // ...
}
```

### 3.2 DefusalModeDataStruct

**路径**：`Host/Modules/Mode/DefusalMode/DefusalModeDataStruct.cs`

```csharp
// 回合结束类型
public enum DefusalModeOverType {
    Bomb,       // 炸弹爆炸 → 攻方胜
    Defusal,    // 炸弹被拆 → 守方胜
    Time,       // 时间耗尽 → 守方胜
    AllDead,    // 全灭
}

// 炸弹数据接口
public interface BombDataInterface {
    bool IsSetBomb { get; }          // 是否已安装炸弹
    float BombSetProgress { get; }   // 安装进度 (0-1)
    float BombDefuseProgress { get; } // 拆弹进度 (0-1)
    Vector3 BombPosition { get; }    // 炸弹位置
}
```

### 3.3 ScriptableObject 配置

**路径**：`Assets/ToBundle/ScriptableObject/Mode/DefusalMode/`

```
DefusalMode/
├── SODefusalModeConfig.asset      ← 主配置
│   ├── roundCount: int            // 总回合数（默认 13）
│   ├── roundTime: float           // 单回合时间（秒）
│   ├── bombSetTime: float         // 安装炸弹耗时
│   ├── bombDefuseTime: float      // 拆弹耗时
│   ├── bombExplodeTime: float     // 安装后爆炸倒计时
│   ├── bombExplodeRadius: float   // 爆炸伤害半径
│   ├── startMoney: int            // 初始金钱
│   └── roundWinMoney: int         // 回合胜利奖金
│
├── SODefusalModeMapConfig.asset   ← 地图配置
│   ├── bombSiteCount: int         // 安装点数量（通常 2）
│   ├── attackSpawnPoints: List    // 攻方出生点
│   └── defenseSpawnPoints: List   // 守方出生点
│
└── SODefusalModeWeaponConfig.asset ← 武器商店配置
    ├── weaponList: List           // 可购买武器列表
    ├── equipmentList: List        // 可购买装备列表
    └── priceTable: Dictionary     // 价格表
```

### 3.4 阶段数据同步

```csharp
// 客户端数据
public class ClientDefusalModeData {
    public SODefusalModeConfig Config;
    public int CurrentRound;           // 当前回合
    public int AttackScore;            // 攻方得分
    public int DefenseScore;           // 守方得分
    public bool IsAttacker;            // 本地玩家是否攻方
    public bool IsSetBomb;             // 炸弹是否已安装
}

// 服务端数据
public class ServerDefusalModeData {
    public int CurrentRound;
    public int AttackScore;
    public int DefenseScore;
    public Dictionary<int, int> PlayerMoney;  // 玩家金钱
    public DefusalModeOverType LastOverType;   // 上回合结束类型
}
```

---

## 四、关键代码修改点

### 4.1 Mgr 初始化与 Logic 注册

**文件**：`ClientDefusalModeMgr.cs`

```csharp
public class ClientDefusalModeMgr : ClientModeManager {
    
    private ClientDefusalModeBombLogic bombLogic;
    private ClientDefusalModeMapLogic mapLogic;
    private ClientDefusalModeRoleLogic roleLogic;
    
    public override void Init() {
        base.Init();
        // 加载配置
        data = new ClientDefusalModeData();
        data.Config = LoadSOConfig<SODefusalModeConfig>();
        
        // 注册 Logic
        bombLogic = new ClientDefusalModeBombLogic();
        mapLogic = new ClientDefusalModeMapLogic();
        roleLogic = new ClientDefusalModeRoleLogic();
        
        AddLogic(bombLogic);
        AddLogic(mapLogic);
        AddLogic(roleLogic);
    }
    
    // 注册 Stage
    protected override void InitStage() {
        AddStage(new ClientDefusalModeBornStage());
        AddStage(new ClientDefusalModeReadyStage());
        AddStage(new ClientDefusalModeShopStage());    // ★ 独有
        AddStage(new ClientDefusalModeBattleStage());
        AddStage(new ClientDefusalModeWinWaitStage());
        AddStage(new ClientDefusalModeOverStage());
    }
}
```

### 4.2 炸弹安装/拆弹核心逻辑（Server）

**文件**：`ServerDefusalModeBombLogic.cs`

```csharp
public class ServerDefusalModeBombLogic : ServerLogicBase {
    
    // 玩家开始安装炸弹
    public void OnStartSetBomb(BattleRoleLogic role, int siteIndex) {
        if (!CanSetBomb(role, siteIndex)) return;
        
        // 开始安装进度
        bombSetProgress = 0f;
        isSettingBomb = true;
        settingRole = role;
        
        // 广播给所有客户端
        SendEvent(ServerDefusalModeEventId.OnBombSetStart, siteIndex);
    }
    
    // 每帧更新安装进度
    public override void OnUpdate(float deltaTime) {
        if (isSettingBomb) {
            bombSetProgress += deltaTime / config.bombSetTime;
            if (bombSetProgress >= 1f) {
                OnBombSetComplete();
            }
        }
        
        if (isDefusing) {
            defuseProgress += deltaTime / config.bombDefuseTime;
            if (defuseProgress >= 1f) {
                OnBombDefuseComplete();
            }
        }
        
        if (isBombSet && !isDefused) {
            bombTimer -= deltaTime;
            if (bombTimer <= 0f) {
                OnBombExplode();
            }
        }
    }
    
    // 炸弹爆炸
    private void OnBombExplode() {
        // 范围伤害
        var roles = GetRolesInRadius(bombPosition, config.bombExplodeRadius);
        foreach (var role in roles) {
            role.TakeDamage(/* 爆炸伤害 */);
        }
        // 攻方胜利
        mgr.EndRound(DefusalModeOverType.Bomb);
    }
}
```

### 4.3 商店阶段（ShopStage）

**文件**：`ClientDefusalModeShopStage.cs`

```csharp
public class ClientDefusalModeShopStage : StageBase {
    
    public override void OnEnter() {
        base.OnEnter();
        // 打开购买 UI
        UIManager.Open<DefusalShopPanel>();
        
        // 显示当前金钱
        var money = mgr.Data.PlayerMoney[GameData.LocalRoleId];
        EventDispatcher.Send(DefusalEventId.OnMoneyUpdate, money);
    }
    
    public override void OnExit() {
        UIManager.Close<DefusalShopPanel>();
        base.OnExit();
    }
}
```

### 4.4 回合结算与经济系统

**文件**：`ServerDefusalModeAwardLogic.cs`

```csharp
public class ServerDefusalModeAwardLogic : ServerLogicBase {
    
    public void OnRoundEnd(DefusalModeOverType overType) {
        // 胜利方奖金
        int winMoney = config.roundWinMoney;
        int loseMoney = config.roundLoseMoney;
        
        foreach (var role in allRoles) {
            bool isWinner = IsWinTeam(role, overType);
            int award = isWinner ? winMoney : loseMoney;
            
            // 击杀奖金
            award += role.KillCount * config.killMoney;
            
            // 安装/拆弹额外奖金
            if (overType == DefusalModeOverType.Bomb && role == bombSetter)
                award += config.bombSetMoney;
            if (overType == DefusalModeOverType.Defusal && role == defuser)
                award += config.defuseMoney;
            
            data.PlayerMoney[role.RoleId] += award;
        }
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 炸弹安装后客户端不显示倒计时

**现象**：服务端炸弹已安装成功，但客户端没有显示爆炸倒计时 UI

**根因**：
- `ClientDefusalModeBombLogic` 未监听 `OnBombSetComplete` 事件
- 或 Proto 消息未在 NetworkClient_Defusal 中正确派发

**解决方案**：
1. 确认 ServerDefusalModeBombLogic.OnBombSetComplete() 发送了 Rpc 广播
2. 确认 NetworkClient_Defusal 的 OnRpc 方法正确调用 ClientDefusalModeBombLogic
3. 确认 UI 监听了 DefusalEventId.OnBombTimerStart 事件

### 5.2 ShopStage 购买后武器未同步

**现象**：玩家在商店购买了武器，进入 Battle 阶段后手中没有武器

**根因**：
- 购买请求发送到服务端后，服务端 BuyWeaponControl 返回成功
- 但 Battle Stage OnEnter 时角色 Inventory 未刷新

**解决方案**：
1. 确认购买 Cmd 的回调中更新了 ClientDefusalModeData.PlayerWeapons
2. 在 BattleStage.OnEnter() 中调用 role.RefreshInventory()
3. 确认购买扣款与服务端金钱一致（使用 Server 权威，Client 仅显示）

### 5.3 回合切换攻守方时出生点错误

**现象**：半场交换（如第 7 回合）后，攻方出生在守方出生点

**根因**：
- ServerDefusalModeMapLogic 在半场交换时未交换 SpawnPoint 引用
- 或 RoleLogic 的阵营标记未同步更新

**解决方案**：
1. 在回合开始前检查 `currentRound > totalRound / 2` 时交换 SpawnGroup
2. 更新所有 Role 的 TeamId 标记
3. 通知客户端刷新阵营 UI

### 5.4 多回合后内存增长

**现象**：13 回合打完后内存明显高于开局，观战模式更严重

**根因**：
- 每回合的 BombEffect/ExplosionEffect 粒子未回收
- WinWait UI 反复创建未销毁

**解决方案**：
1. BombLogic.OnRoundEnd() 中调用 EffectPool.Release() 回收所有本回合特效
2. UIManager 使用 Open/Close 而非 Create/Destroy
3. StatisticsLogic 的历史回合数据使用固定大小环形缓冲

### 5.5 MVP 计算不准确

**现象**：拆弹成功的玩家没有被评为 MVP

**根因**：MVP 权重公式未包含炸弹操作贡献

**解决方案**：
1. 检查 ServerDefusalModeMvpLogic 的评分公式
2. 确认包含：击杀权重 + 助攻权重 + 安装炸弹权重 + 拆弹权重 + 存活权重
3. 关键操作（成功安装/拆弹）应有较高的额外分值

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `Defusalmode=34` 无冲突
- [ ] ClientModeFactory + ServerModeFactory 已注册
- [ ] 所有 Stage 类编译通过
- [ ] Logic 类在 Mgr.Init() 中全部注册

### 6.2 配置

- [ ] SODefusalModeConfig 配置参数合理（回合数/时间/金钱）
- [ ] 地图配置包含正确的安装点和出生点
- [ ] 武器商店价格表完整
- [ ] Stage 枚举 C/S 一致

### 6.3 运行时

- [ ] 6 个 Stage 阶段正常流转（Born→Ready→Shop→Battle→WinWait→Over）
- [ ] 炸弹安装/拆弹/爆炸全流程正常
- [ ] 三种结束条件均可触发（炸弹爆炸/拆弹成功/时间耗尽）
- [ ] 经济系统正确（击杀奖金/回合奖金/购买扣费）
- [ ] 半场交换攻守方正常
- [ ] MVP 正确计算
- [ ] 多回合后无内存泄漏

### 6.4 兼容性

- [ ] 不影响其他模式（Common/Team/Classic 等）
- [ ] 自定义房间中爆破模式可用
- [ ] 观战模式下 UI 正常显示

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-common]] · [[mode-defusal]] · [[网络消息制作]]
