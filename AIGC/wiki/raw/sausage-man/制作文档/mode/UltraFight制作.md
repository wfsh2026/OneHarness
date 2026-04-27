# 1 代架构极限战斗/奥特派对（UltraFight）制作规范

> **适用范围**：UltraFight 奥特派对模式 — 扩展武器箱 / 道具箱 / 时装变化机制 / 命中部位系统
> **不适用**：通用模式框架 → 归 [[模式制作]]；通用武器系统 → 归 [[武器战斗制作]]
> **参考实现**：mode-ultrafight（25 文件，☆ 极简但独立目录结构）
> **公共框架依赖**：[[模式制作]]（ClientModeManager / ServerModeManager / Stage / 工厂注册）
> **架构特殊性**：不在 Mode/ 目录，而在独立的 Modules/UltraFight/ 目录

---

## 一、架构概述

### 1.1 核心类依赖

```
ClientUltraFightMain (Client 端奥特派对主入口)
  │  路径: Assets/Script/GamePlay/Client/Modules/UltraFight/ClientUltraFightMain.cs
  │  继承: ClientModeManager
  │  ⚠️ 目录: Modules/UltraFight/（非标准 Mode/ 目录）
  │  职责: 客户端入口，道具箱管理，时装变化表现
  │
  ├── ClientUltraFightBoxLogic
  │     职责: 道具箱/武器箱客户端拾取表现
  │
  ├── ClientUltraFightRoleLogic
  │     职责: 角色状态变化（时装丢失/恢复）
  │
  ├── Stage 层（5 阶段）
  │     BornStage → ReadyStage → BattleStage → WinWaitStage → OverStage
  │
  └── ClientUltraFightData
        职责: 客户端运行时数据

ServerUltraFightMain (Server 端奥特派对主入口)
  │  路径: Assets/Script/GamePlay/Server/Modules/UltraFight/ServerUltraFightMain.cs
  │  继承: ServerModeManager
  │  ⚠️ 目录: Modules/UltraFight/
  │
  ├── ServerUltraFightBoxLogic
  │     职责: 道具箱生成/拾取判定
  │
  ├── ServerUltraFightRoleLogic
  │     职责: 角色管理，新角色加入处理
  │
  ├── ServerUltraFightWeaponLogic
  │     职责: 武器系统，武器箱内容分配
  │
  ├── ServerUltraFightAwardLogic
  │     职责: 奖励结算
  │
  ├── ServerUltraFightStatisticsLogic
  │     职责: 战绩统计
  │
  └── ServerUltraFightNsqDataLogic
        职责: NSQ 数据上报

UltraFightSceneMgr (场景专用管理器)
  │  路径: Host 层或独立目录
  │  职责: 奥特派对专属场景管理

数据层（分离式设计 ★）
  │  ServerUltraFightData (基础数据)
  │  ServerUltraFightData_Method (方法扩展 - partial class)
  │  UltraFightDataStruct (Host 层数据结构定义)
  │  ClientUltraFightData (客户端数据)

SOUltraFightConfig (ScriptableObject 配置)
  │  路径: Assets/ToBundle/ScriptableObject/Mode/UltraFight/
  │  关键字段: monsterHitPartNormal / monsterHitPartAttack
```

### 1.2 Stage 阶段流转

```
5 阶段制（标准扩展）：

Born (出生阶段)
  │  玩家在场景出生点生成
  │  NewRoleAdd 消息处理
  ↓
Ready (准备阶段)
  │  等待所有玩家就绪
  │  初始化武器箱/道具箱位置
  ↓
Battle (战斗阶段)
  │  核心玩法：
  │    ├── 击败对手 → 获得对手的时装部件
  │    ├── 拾取武器箱 → 获得新武器
  │    ├── 拾取道具箱 → 获得增益效果
  │    └── 被击败 → 丢失时装部件（roleLostFashionDatas）
  │  判定：
  │    ├── 时间到 → WinWait
  │    └── 某条件满足 → WinWait
  ↓
WinWait (胜利等待)
  │  显示获胜者/结算预览
  ↓
Over (游戏结束)
    最终结算，返回大厅
```

### 1.3 目录结构特殊性

```
标准模式目录结构：
  Assets/Script/GamePlay/Client/Modules/Mode/{ModeName}/
  Assets/Script/GamePlay/Server/Modules/Mode/{ModeName}/

UltraFight 独立目录：
  Assets/Script/GamePlay/Client/Modules/UltraFight/    ← ⚠️ 不在 Mode/ 下
  Assets/Script/GamePlay/Server/Modules/UltraFight/    ← ⚠️ 不在 Mode/ 下
  
原因：UltraFight 早期开发时使用独立目录，后续未迁移
影响：新增文件应放在 Modules/UltraFight/ 目录，不要放到 Mode/ 下
```

### 1.4 预制体与资源加载（★）

| 资源 | 路径 | 加载方式 | 时机 |
|------|------|---------|------|
| **模式配置** | `Assets/ToBundle/ScriptableObject/Mode/UltraFight/SOUltraFightConfig.asset` | Resources/AB | Main.Init() |
| **武器箱** | 场景内预置 / 动态生成 | ItemPool | Battle 阶段 |
| **道具箱** | 场景内预置 / 动态生成 | ItemPool | Battle 阶段 |
| **时装资源** | `Assets/ToBundle/Role/Fashion/` | FashionManager | 击败对手时 |
| **命中部位配置** | SOUltraFightConfig 内嵌 | 配置加载 | Init() |

### 1.5 禁止修改的文件

- **ClientModeManager.cs / ServerModeManager.cs** — 模式基类
- **GameMode.cs** 已有枚举值 `Ultrafight=20`
- **FashionManager** 核心逻辑 — UltraFight 通过接口调用，不直接修改

---

## 二、新建/扩展 Checklist

### Phase 1：模式注册（已完成）

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 1 | `Host/Mode/GameMode.cs` | 已有 | `Ultrafight = 20` |
| 2 | `ClientModeFactory.cs` | 已有 | `AddFeature<ClientUltraFightMain>()` |
| 3 | `ServerModeFactory.cs` | 已有 | `AddFeature<ServerUltraFightMain>()` |

### Phase 2：新增 Logic

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 4 | `Client/Modules/UltraFight/Client{LogicName}Logic.cs` | 新建 | ⚠️ 注意目录是 UltraFight/ 不是 Mode/ |
| 5 | `Server/Modules/UltraFight/Server{LogicName}Logic.cs` | 新建 | 同上 |
| 6 | `ClientUltraFightMain.cs` | 修改 | Init() 中 AddLogic() |
| 7 | `ServerUltraFightMain.cs` | 修改 | Init() 中 AddLogic() |

### Phase 3：扩展武器箱/道具箱

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 8 | `ServerUltraFightWeaponLogic.cs` | 修改 | 新增武器类型 |
| 9 | `ServerUltraFightBoxLogic.cs` | 修改 | 新增道具箱内容 |
| 10 | `ClientUltraFightBoxLogic.cs` | 修改 | 对应客户端表现 |

### Phase 4：扩展时装变化系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 11 | `ClientUltraFightRoleLogic.cs` | 修改 | 新增时装变化表现 |
| 12 | `ServerUltraFightRoleLogic.cs` | 修改 | 新增时装丢失/获取规则 |
| 13 | `UltraFightDataStruct.cs` | 修改 | 新增数据结构字段 |

### Phase 5：调整命中部位系统

| # | 文件 | 操作 | 说明 |
|---|------|------|------|
| 14 | `SOUltraFightConfig.asset` | 修改 | 调整 monsterHitPartNormal/Attack |
| 15 | `RoleUltraFightHitPart` 相关代码 | 修改 | 新增命中部位类型 |

---

## 三、配置文件详解

### 3.1 SOUltraFightConfig

**路径**：`Assets/ToBundle/ScriptableObject/Mode/UltraFight/SOUltraFightConfig.asset`

| 字段 | 类型 | 说明 |
|------|------|------|
| `monsterHitPartNormal` | HitPartConfig[] | 普通状态的命中部位配置 |
| `monsterHitPartAttack` | HitPartConfig[] | 攻击状态的命中部位配置 |
| `battleTime` | float | 战斗时长（秒） |
| `boxSpawnInterval` | float | 道具箱刷新间隔 |
| `weaponBoxSpawnInterval` | float | 武器箱刷新间隔 |
| `maxBoxCount` | int | 场景内最大箱子数量 |
| `fashionLostOnDeath` | bool | 死亡是否丢失时装 |

### 3.2 数据层分离设计

```csharp
// 基础数据（字段定义）
public class ServerUltraFightData {
    public SOUltraFightConfig Config;
    public float BattleTimer;
    public List<int> ActiveBoxIds;
    public Dictionary<int, List<int>> RoleFashionMap;  // 角色 → 时装部件列表
}

// 方法扩展（partial class）
public partial class ServerUltraFightData {
    public void AddFashion(int roleId, int fashionId) {
        if (!RoleFashionMap.ContainsKey(roleId))
            RoleFashionMap[roleId] = new List<int>();
        RoleFashionMap[roleId].Add(fashionId);
    }
    
    public void RemoveFashion(int roleId, int fashionId) {
        RoleFashionMap[roleId]?.Remove(fashionId);
    }
}

// Host 层数据结构定义
public class UltraFightDataStruct {
    // 命中部位
    public struct HitPartConfig {
        public string partName;
        public float damageMultiplier;
        public int fashionSlot;     // 对应时装槽位
    }
}

// 客户端数据
public class ClientUltraFightData {
    public SOUltraFightConfig Config;
    public List<int> MyFashions;           // 我的时装部件
    public List<int> roleLostFashionDatas; // 缓存丢失的时装数据
}
```

---

## 四、关键代码修改点

### 4.1 Main 初始化（独立目录）

**文件**：`ClientUltraFightMain.cs`

```csharp
public class ClientUltraFightMain : ClientModeManager {
    
    public override void Init() {
        base.Init();
        data = new ClientUltraFightData();
        data.Config = LoadSOConfig<SOUltraFightConfig>();
        
        // 注册 Logic
        AddLogic(new ClientUltraFightBoxLogic());
        AddLogic(new ClientUltraFightRoleLogic());
    }
    
    protected override void InitStage() {
        AddStage(new ClientUltraFightBornStage());
        AddStage(new ClientUltraFightReadyStage());
        AddStage(new ClientUltraFightBattleStage());
        AddStage(new ClientUltraFightWinWaitStage());
        AddStage(new ClientUltraFightOverStage());
    }
}
```

### 4.2 时装变化系统

**文件**：`ServerUltraFightRoleLogic.cs`

```csharp
public class ServerUltraFightRoleLogic : ServerLogicBase {
    
    // 角色被击败 → 丢失时装
    public void OnRoleDead(BattleRoleLogic victim, BattleRoleLogic killer) {
        // 获取受害者的时装列表
        var fashions = data.RoleFashionMap[victim.RoleId];
        
        if (fashions.Count > 0) {
            // 随机选择一件时装转移给击杀者
            int index = Random.Range(0, fashions.Count);
            int fashionId = fashions[index];
            
            data.RemoveFashion(victim.RoleId, fashionId);
            data.AddFashion(killer.RoleId, fashionId);
            
            // 通知客户端状态变化
            SendRpc(new OnUltraFightChangeState {
                victimId = victim.RoleId,
                killerId = killer.RoleId,
                fashionId = fashionId
            });
        }
    }
    
    // 新角色加入
    public void NewRoleAdd(BattleRoleLogic role) {
        // 初始化时装数据
        data.RoleFashionMap[role.RoleId] = GetInitialFashions(role);
        
        // 缓存时装数据（用于补人时装概率处理）
        CacheRoleFashionData(role);
    }
    
    // 角色状态变化 → 服装变化
    public void RoleStateChange(int roleId) {
        var fashions = data.RoleFashionMap[roleId];
        // 根据当前持有的时装更新角色外观
        UpdateRoleAppearance(roleId, fashions);
    }
}
```

### 4.3 道具箱系统

**文件**：`ServerUltraFightBoxLogic.cs`

```csharp
public class ServerUltraFightBoxLogic : ServerLogicBase {
    
    public override void OnUpdate(float deltaTime) {
        // 定时刷新道具箱
        boxSpawnTimer -= deltaTime;
        if (boxSpawnTimer <= 0 && data.ActiveBoxIds.Count < data.Config.maxBoxCount) {
            SpawnRandomBox();
            boxSpawnTimer = data.Config.boxSpawnInterval;
        }
    }
    
    private void SpawnRandomBox() {
        var spawnPoint = GetRandomSpawnPoint();
        var boxType = Random.value > 0.5f ? BoxType.Weapon : BoxType.Item;
        
        // 生成箱子
        var boxId = CreateBox(boxType, spawnPoint);
        data.ActiveBoxIds.Add(boxId);
        
        // 通知客户端
        SendRpc(new RpcBoxSpawn { boxId = boxId, type = boxType, position = spawnPoint });
    }
    
    // 玩家拾取箱子
    public void OnBoxPickup(int roleId, int boxId) {
        var boxType = GetBoxType(boxId);
        
        if (boxType == BoxType.Weapon) {
            // 武器箱 → 通过 WeaponLogic 分配
            mgr.GetLogic<ServerUltraFightWeaponLogic>().GiveRandomWeapon(roleId);
        } else {
            // 道具箱 → 直接给效果
            ApplyItemEffect(roleId);
        }
        
        data.ActiveBoxIds.Remove(boxId);
    }
}
```

### 4.4 命中部位系统

```csharp
// RoleUltraFightHitPart 定义
public class RoleUltraFightHitPart {
    public HitPartConfig[] normalParts;   // 普通状态部位
    public HitPartConfig[] attackParts;   // 攻击状态部位
    
    public float GetDamageMultiplier(string hitPart, bool isAttacking) {
        var parts = isAttacking ? attackParts : normalParts;
        foreach (var part in parts) {
            if (part.partName == hitPart)
                return part.damageMultiplier;
        }
        return 1f;  // 默认倍率
    }
}
```

---

## 五、常见问题与踩坑记录

### 5.1 新文件放错目录

**现象**：新建的 Logic 文件放在了 `Mode/UltraFight/` 下，编译找不到引用

**根因**：UltraFight 使用独立目录 `Modules/UltraFight/`，不在标准 `Mode/` 下

**解决方案**：
1. Client 端文件放 `Assets/Script/GamePlay/Client/Modules/UltraFight/`
2. Server 端文件放 `Assets/Script/GamePlay/Server/Modules/UltraFight/`
3. 检查 asmdef 引用是否包含 UltraFight 目录

### 5.2 时装丢失后未在客户端同步

**现象**：被击杀后服务端已转移时装，但客户端外观没变化

**根因**：
- `OnUltraFightChangeState` 消息未到达客户端
- 或 ClientUltraFightRoleLogic 的 `roleLostFashionDatas` 缓存未更新

**解决方案**：
1. 确认 NetworkServer/Client 消息通道正确
2. ClientUltraFightRoleLogic 收到消息后调用 `RoleStateChange()` 更新外观
3. 更新 `roleLostFashionDatas` 缓存以支持补人时装概率

### 5.3 道具箱刷新过密或不刷新

**现象**：场景内同时出现大量箱子，或者长时间没有新箱子

**根因**：
- `boxSpawnInterval` 配置过小导致刷新过密
- `maxBoxCount` 达到上限但旧箱子未正确移除导致不刷新

**解决方案**：
1. 检查 SOUltraFightConfig 的 `boxSpawnInterval` 和 `maxBoxCount` 配置
2. 确认 OnBoxPickup 后 `data.ActiveBoxIds.Remove(boxId)` 正确执行
3. 添加超时自动销毁逻辑：箱子存在超过 N 秒自动移除

### 5.4 Data_Method partial class 编译顺序问题

**现象**：`ServerUltraFightData_Method.cs` 中的方法无法访问 `ServerUltraFightData.cs` 的字段

**根因**：两个 partial class 文件不在同一 namespace 或 class 名拼写不一致

**解决方案**：
1. 确认两个文件的 namespace 完全一致
2. 确认类名完全一致：`partial class ServerUltraFightData`
3. 确认两个文件都被同一个 asmdef 包含

---

## 六、验收标准

### 6.1 编译

- [ ] 零 CS error
- [ ] GameMode 枚举值 `Ultrafight=20` 无冲突
- [ ] Factory 双端已注册
- [ ] partial class 编译正常（Data + Data_Method）

### 6.2 配置

- [ ] SOUltraFightConfig 命中部位配置合理
- [ ] 箱子刷新参数（间隔/上限）合理
- [ ] 时装丢失规则配置正确

### 6.3 运行时

- [ ] 5 阶段正常流转（Born→Ready→Battle→WinWait→Over）
- [ ] 武器箱拾取后正确获得武器
- [ ] 道具箱拾取后正确获得效果
- [ ] 击杀对手正确获得对手时装
- [ ] 被击杀正确丢失时装
- [ ] 命中部位伤害倍率正确
- [ ] 箱子定时刷新正常

### 6.4 兼容性

- [ ] 不影响其他模式
- [ ] 不影响 FashionManager 核心逻辑
- [ ] 场景管理器 UltraFightSceneMgr 正常工作

依赖知识：[[模式制作]] · [[mode-base]] · [[mode-ultrafight]] · [[武器战斗制作]]
