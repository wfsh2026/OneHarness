# 游戏模式开发规范

> 参考范例：[[模式参考范例]]
> 参考文档：[[模式系统内容边界定义]]

---

## ⚠️ 强制工具规则

> **新建模式时，AI 必须调用以下工具：**
> 1. `aigc/harness/tools/codegen/mode-gen.sh` — 生成 ModeData 注册 + Server/Client Mode 文件 + System switch 注册
> 2. `aigc/harness/tools/codegen/component-gen.sh` — 生成模式专属 Component 模板（`--type mode`）
>
> 禁止手动创建 Mode 文件或手动修改 ModeData.cs / ServerModeSystem.cs / ClientModeSystem.cs 注册。
> 仅在修改已有 Mode 的业务逻辑时可直接编辑。
> 详见 [[codegen/README]]。

---

## 一、新建模式必须创建/修改的文件清单

> 每新增一个游戏模式，必须完成以下所有步骤，缺少任一会导致运行时错误。

### 📋 数据配置层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/Data/ModeData.cs` | **修改**：ModeEnum 新增枚举值 | 如 `ModeTankBattle = 17` |
| `Assets/Scripts/Data/ModeData.cs` | **修改**：`Init()` switch 新增 case | 配置 RoundWinState、ScoreChannelDatas 等 |
| `Assets/Scripts/Template/data/Mode.cs` | **修改**：ModeSet 新增 Id 常量 + data 数组新增行 | `Id_ModeTankBattle` 常量 + 数据行 |
| `Assets/Scripts/Template/data/AiLevel.cs` | **修改**：新增对应 gameMode 的数据行 | 测试 ID 使用 10001-19999 区间，避免与生产 ID 冲突 |

> **⚠️ 注意**：`ModeEnum.ModeTankBattle = 17`（枚举整数）与 `ModeSet.Id_ModeTankBattle`（数据行 ID）是**两个不同的值**，不可混淆。测试 ID 必须用高位（10001+），避免与生产 ModeSet ID 冲突（参见 core-rules.md §3.7）。

---

### 🔌 路由注册层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Server/Mode/ServerModeSystem.cs` | **修改**：`InitModeComponent()` switch 新增 case | 注册模式专属 Server 组件 |
| `Assets/Scripts/GamePlay/Client/Mode/ClientModeSystem.cs` | **修改**：`InitModeComponent()` switch 新增 case | 注册模式专属 Client 组件 |

---

### 🖥️ 服务端模式组件层（必须）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Server/Mode/Components/ServerXXXMode.cs` | **新建** | 继承 `ComponentBase`，实现模式专属逻辑（计分/AI生成/胜负判定等） |

---

### 💻 客户端模式组件层（按需）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/GamePlay/Client/Mode/Components/ClientXXXMode.cs` | **新建**（若有客户端专属表现） | 接收服务端 Rpc，驱动 UI 和本地状态机 |

---

### 🗺️ 场景层（按需）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scenes/Runtime/XXX.unity` | **新建** | 客户端场景（含 Renderer/光照） |
| `Assets/Scenes/Runtime/ServerXXX.unity` | **新建**（Editor 脚本生成） | 服务端场景（无 Renderer，仅碰撞体） |
| `Assets/Bundle/Configs/Scene/MapXXX_01.asset` | **新建** | 场景配置 SO（Mode ID / 出生点 / AI 刷新点）|

> 场景建设完整规范见 `scene-code.md`。

---

### 📡 网络协议层（按需）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Assets/Scripts/Message/GamePlay/Server/World/SM_XXXMode.cs` | **新建**（若有模式专属世界消息） | 如 `SM_TankBattle.SpawnTank` 等 |

---

## 二、ServerModeSystem 默认已注册的通用组件

继承 `ServerModeSystem` 时，`AddComponents()` 已默认注册：

| 组件 | 职责 |
|------|------|
| `ServerModeMainLoop` | 回合状态机（必须，所有模式均需要） |
| `ServerModeHero` | 英雄模式扩展（**无英雄概念的模式可去掉**） |
| `ServerModeCharacter` | GPO 与 PlayerId 映射 |
| `ServerModeScore` | 积分管理 |
| `ServerModeTimer` | 回合计时 |
| `ServerModeClockSync` | 服务器时间同步 |
| `ServerModeCreateAI` | 模式内 AI 生成管理 |
| `ServerModeDropItem` | 击杀掉落物品 |

模式专属组件只需关注**差异化逻辑**，通用组件不需要在模式 Component 中重复注册。

---

## 三、常见运行时 Bug 与陷阱

> 来源：坦克大乱斗 Phase 1 复盘（2026-03-26）

### 3.1 ModeData 配置陷阱

| 字段 | 陷阱 | 正确做法 |
|------|------|---------|
| `StartModeDownTime` | **设为 0 或过小**会导致 `ServerModeCreateAI.waitAddAITime = 0`，`UpdateAddAI()` 直接 return，**AI 永远不会生成** | 新模式至少设为 `10f` |
| `RoundTime` | **设为 -1** 会导致 `UpdateRoundTime()` 第一帧立即触发 `RoundEnd`（框架内部用 `-1` 作为"已触发"哨兵值，与 "无限回合" 语义冲突）；`RoundTime` 是 `int` 类型，不可使用 float 字面量（如 `36000f`）| 无限回合改用大整数如 `36000`（10小时） |
| `MaxRoleNum` / `MaxRoleNumPerTeam` | 默认值可能是旧数据，导致目标人数达不到 | 开发时明确配置目标人数 |
| `StartRoundDownTime` | **设为 > 0** 会在 `WaitStartDownTime` 倒计时结束后**再多一段 WaitRoundStart 等待**（即双段倒计时），体验上像"卡顿"。若不需要开局 3-2-1 倒计时，直接设为 `0f` | 坦克大乱斗设为 `0f`（10s 等待结束后直接开战） |

### 3.1.1 ModeData 两段倒计时说明（2026-03-27 新增）

框架在进入对局时会经历**最多两段**倒计时，分别由不同字段控制：

```
Wait（等待玩家）
  ↓ 达到 MinStartModeTeamNum
WaitStartDownTime（StartModeDownTime 秒）← 第一段：等待足够玩家时的倒计时
  ↓
WaitRoundStart（StartRoundDownTime 秒） ← 第二段：3-2-1 开战准备（可选）
  ↓
RoundStart（正式开战）
```

**客户端接入开局倒计时的正确方式**：
- 服务端自动广播 `Proto_Mode.Rpc_GameDownTime`（两段倒计时均用此消息）
- `ClientModeMainLoop` 收到后发 `CM_Mode.SetDownTime { DownTime }` 全局消息
- 客户端自定义 Mode 组件订阅 `CM_Mode.SetDownTime` + `CM_Mode.SetGameState` 即可获取倒计时秒数和当前状态
- 通过 `gameState == RoundStart` 判断是否在对局内，决定显示"开局前倒计时"还是"回合内剩余时间"

```csharp
// 客户端订阅示例（ClientXXXMode.cs）
protected override void OnAwake() {
    MsgRegister.Register<CM_Mode.SetDownTime>(OnSetDownTime);   // 开局倒计时
    MsgRegister.Register<CM_Mode.SetGameState>(OnSetGameState); // 状态变化
}
private void OnSetDownTime(CM_Mode.SetDownTime msg) {
    hud.PreRoundSeconds = Mathf.RoundToInt(msg.DownTime);
}
private void OnSetGameState(CM_Mode.SetGameState msg) {
    hud.IsPreRound = msg.GameState != ModeData.GameStateEnum.RoundStart;
}
```

### 3.2 角色出生坐标为 (0,0,0)

**根因**：在 `OnAddCharacterFinish` 中立即 spawn 时，角色出生点坐标仍为 `Vector3.zero`。

**正确 Hook 点**：注册 `SM_Mode.GetStartPoint`，在 `OnGetStartPointCallBack` 里用回调给出的真实 `point` 坐标再 spawn：

```csharp
// ❌ 错误：OnAddCharacterFinish 时坐标还是 zero
protected override void OnAddCharacterFinish(IGPO gpo) {
    SpawnTankForCharacter(gpo);  // gpo.GetPoint() 此时是 Vector3.zero！
}

// ✅ 正确：在出生点确认回调后 spawn
// 注册：AddComponentCallBack<SM_Mode.GetStartPoint>(OnGetStartPointCallBack);
private void OnGetStartPointCallBack(SM_Mode.GetStartPoint ent) {
    ent.CallBack?.Invoke(point);       // 先告诉框架出生点
    SpawnTankForCharacter(gpo, point); // 再用真实坐标 spawn
}
```

### 3.3 服务端 Prefab 命中检测失效（Layer 双重配置问题）

服务端 Prefab 必须**同时**满足：
- `HitType.Layer = LayerEnum.World`（框架内部受击）
- Unity `gameObject.layer = "ServerLayer"`（物理射线层）

两者缺一：
- 只设 `HitType.Layer = World` 但 `gameObject.layer` 是 Default → 炮弹打不中
- Prefab 新建时 Unity 默认 Layer 是 Default，**必须手动改为 ServerLayer**

### 3.4 OnRoundStart 重复 Spawn 导致双实体

如果在 `OnRoundStart` 中清空了字典再重新 spawn，旧实体仍存活，新旧叠加 → 双坦克/双角色。

**Phase 1 单回合模式不需要在 RoundStart 重新 spawn，移除即可。**

### 3.5 坦克死亡后角色不死

坦克 `SetIsDead` 回调中必须**主动通知宿主角色死亡**：

```csharp
characterGpo.Dispatcher(new SE_GPO.Event_SetIsDead { IsDead = true });
```

---

### 3.6 回合开始时实体（坦克/载具）位置重置

**场景**：多单位模式（坦克大乱斗等），回合开始需要把所有实体归位到出生点。

**禁止做法**：通过 `Event_SetIsDead` 杀死实体再重新 Spawn。这会触发死亡回调，导致复活队列误入队、死亡特效/音效误播放。

**正确做法**：直接使用 `SE_Entity.SyncPointAndRota` 传送到目标点（参考 `ServerVSReLifeMode.ResetCharacterState`）：

```csharp
// ✅ 正确：直接传送，不经过死亡回调
tank.Dispatcher(new SE_Entity.SyncPointAndRota {
    Point     = spawnPoint,
    Rota      = Quaternion.identity,
    OR_IsSync = true
});
tank.Dispatcher(new SE_GPO.Event_ReLife { UpHp = 9999999 });

// ❌ 错误：杀死再重生，会触发 SetIsDead 回调并误入复活队列
tank.Dispatcher(new SE_GPO.Event_SetIsDead { IsDead = true });
SpawnTankForCharacter(gpo, point); // 也不对
```



## 四、游戏状态机（模式生命周期）

```
None
 └─► Wait（等待玩家加入）
       └─► WaitStartDownTime（达到最小人数，开始倒计时）
             └─► WaitRoundStart（等待回合开始）
                   └─► RoundStart（回合进行中）
                         └─► RoundEnd（回合结束）
                               ├─► WaitNextRound（多回合）→ WaitRoundStart
                               └─► WaitModeOver → ModeOver → SaveReport → QuitApp
```

> 注意：`ServerModeMainLoop.OnUpdate()` 中，`ModeOver` 调用 `OnWaitSaveReport()`，`SaveReport` 调用 `OnWaitQuitAPP()`——函数名与状态名存在**一级偏移**，阅读代码时注意对照。

---

## 五、新模式测试入口接入规范（DL 负责）

> 来源：BIU26 Phase 1 复盘（2026-03-29）  
> 每新增模式，DL 必须完成以下三步，否则测试工具面板不会显示该模式入口。

### 5.1 三步必改清单

| 步骤 | 文件 | 说明 |
|------|------|------|
| ① | `Assets/Scripts/Data/ModeData.cs` → `AddTestMode()` | 追加新模式的 Data 条目，否则 `GetModeDataForModeEnum()` 返回 null → 运行时 NullReferenceException |
| ② | `Assets/Scripts/Data/SceneData.cs` | 添加 `public const int {ModeName}_Dev = {ID}` 常量 + `datas` 条目 |
| ③ | `Assets/Scripts/Data/ModeData.cs` → `GetAllGameMatches()` | 追加 `ModeMatch` 条目，使模式出现在 `UIModeTool` 测试面板 |

> **职责说明**：步骤①③由 DL 负责；步骤②（SceneData）由场景建设工程师负责。两者必须在同一轮次完成，否则会出现编译通过但运行时找不到场景数据的 Bug。

---

### 5.2 代码示例

#### ① ModeData.AddTestMode() 追加条目
```csharp
// ModeData.cs → AddTestMode()
datas.Add(new Data {
    Id              = Id_BIU26,          // 测试 ID 区间 10001-19999
    ModeEnum        = ModeEnum.ModeBIU26,
    MaxRoleNum      = 4,
    MaxRoleNumPerTeam = 4,
    RoundTime       = -1f,               // -1 = 无限时
    StartModeDownTime = 10f,             // ⚠️ 不能为 0，否则 AI 永远不会生成
});
```

#### ② SceneData.cs 追加常量和数据
```csharp
public const int BIU26_Dev = 20000;  // 测试场景 ID（20000+ 区间）

// 在 datas 列表追加：
new Data() { ID = BIU26_Dev, StageSign = "BIU26_Dev", ElementConfig = "MapBIU26_Dev_01" },
// StageSign = 客户端场景名（不含路径和扩展名）
// ElementConfig = SceneConfig SO 文件名（不含扩展名）
```

#### ③ ModeData.GetAllGameMatches() 追加入口
```csharp
// ModeMatch 构造函数签名：
// ModeMatch(int id, int modeId, int mapId, string sign, string desc, string showName, sbyte openType, int clientSort, int entranceSize, string enterSign, string modeSwitchSign)
list.Insert(list.Count, new ModeMatch(
    Id_BIU26, Id_BIU26, SceneData.BIU26_Dev,
    "MapBIU26_Dev_01", "BIU26 割草发育", "BIU26 割草发育",
    0, 0, 0, "", ""));
```

---

### 5.3 SceneConfig SO 的 TargetScenePath 规则

> ⚠️ **高频错误**：TargetScenePath 应填**客户端场景路径**，不是服务端场景路径！

| 字段 | 正确值 | 错误值 |
|------|-------|-------|
| `TargetScenePath` | `Assets/Scenes/Runtime/BIU26_Dev.unity` | `Assets/Scenes/Runtime/ServerBIU26_Dev.unity` |

**原因**：`StageData.GetServerStage(clientName)` = `"Server" + clientName`，服务端场景路径由框架自动推导，无需手填。

---

### 5.4 测试验证流程

```
Enter Play Mode
→ UIModeTool 面板 → 选择新模式（BIU26 割草发育）
→ 进入战斗 → 验证 GPO 刷出 → 击杀 → 掉落拾取
→ 若无法显示：检查步骤①②③是否全部完成
```
