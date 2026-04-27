# UGC 开发规范（ugc-code.md）

> **适用范围**：所有参与 UGC 功能开发的 Agent（DL / GPO 工程师 / Ability 工程师）
> **前置必读**：`core-rules.md`（ECS 规范 / namespace / asmdef 规则全部以该文件为准，本文不重复）、`gpo-code.md`（GPOM 格式规范以该文件为准）

---

## 零、🚨 最高优先级强制规则：UGC 禁止修改 PGC

> **所有 UGC 开发内容必须且只能位于 `Assets/Scripts/UGC/` 目录内。**
> **严禁新建或修改 `Assets/Scripts/UGC/` 之外的任何文件。**

**[Dev_Leader] 强制审查规则**：
- 每次 UGC 开发轮次结束，`[Dev_Leader]`（即 `[项目负责人]`）必须检查本轮所有 `文件变更` 记录
- 如发现任何非 `Assets/Scripts/UGC/` 路径的 `.cs` 文件被新建或修改，**必须立即纠正**：
  - 将该代码移入 UGC 目录下对应位置
  - 或改用 PGC 已有钩子 API（见 §一 PGC 钩子表）
  - 并在 `active.md` Bug 记录中登记该越界行为

> 例外：`aigc/harness/` 目录下的文档文件（`.md`）不受此限制。

---

## 一、UGC 边界规则

PGC 侧已预埋以下钩子，UGC 直接调用即可：

| PGC 钩子文件 | 暴露的注册 API |
|------------|--------------|
| `ServerAIWorld_UGC.cs` | `ServerAIWorld.RegisterGPOSystem()` |
| `ClientAIWorld_UGC.cs` | `ClientAIWorld.RegisterGPOSystem()` |
| `GpoSet_UGC.cs` | `GpoSet.RegisterUGCGPOM()` / `GpoSet.RegisterUGCGpoRow()` |
| `ServerAbilityManager_UGC.cs` | `ServerAbilityManager.RegisterAB()` / `.RegisterAE()` |
| `ClientAbilityManager_UGC.cs` | `ClientAbilityManager.RegisterAB()` / `.RegisterAE()` |
| `ServerModeSystem_UGC.cs` | `ServerModeSystem.RegisterServerModeComponent()` |
| `ClientModeSystem_UGC.cs` | `ClientModeSystem.RegisterClientModeComponent()` |
| `ServerWeaponManager_UGC.cs` | `ServerWeaponManager.RegisterWeapon()` |
| `ClientWeaponManager_UGC.cs` | `ClientWeaponManager.RegisterWeapon()` |
| `ModeData.cs`（内置钩子） | `ModeData.RegisterUGCScene(Data)` — 覆盖 PGC 预埋的 UGC 模式配置（AddTestMode 已预埋空白占坑 `{Id=20001, Mode=ModeUGCTest}`） |
| `SceneData.cs`（内置钩子） | `SceneData.RegisterUGCScene(Data)` — 注入 UGC 场景数据 |

> **PGC 直管坑位（勿在 UGC 重复注入）**：
> - `ModeData.Id_UGCTestMode`（`= 20001`）：Mode ID 由 PGC 定义，UGC 直接引用此常量，无需镜像。
> - `ModeData.GetAllGameMatches()` 中直接包含 UGC 模式的 `ModeMatch` 入口，**UGC 不另注入**。
> - `SceneData.SceneId_UGCTest`（`= 99998`）：Scene ID 由 PGC 定义，`UGCServerGameWorld` 引用此常量。

所有注册调用集中在 `CoreGameWorld_UGC` / `ServerGameWorld_UGC` / `ClientGameWorld_UGC` 的 `OnInit()` 中完成，禁止在 System / Component 内部调用。

---

## 二、程序集与 Namespace

UGC 程序集：`Sofunny.BiuBiuBiu2.UGC`（`Assets/Scripts/UGC/`）。禁止将 UGC 代码放入其他程序集。

| 文件类型 | Namespace |
|---------|-----------|
| UGC 服务端 System / Component | `Sofunny.BiuBiuBiu2.ServerGamePlay.UGC` |
| UGC 客户端 System / Component | `Sofunny.BiuBiuBiu2.ClientGamePlay.UGC` |
| UGC 注册入口（GameWorld） | `Sofunny.BiuBiuBiu2.GamePlay.UGC` |
| UGC 模板数据（GPOM / IdSet） | `Sofunny.BiuBiuBiu2.Template.UGC` |
| UGC GpoTypeSet 扩展（partial） | `Sofunny.BiuBiuBiu2.Template`（必须与 PGC 一致） |
| UGC 网络协议（proto） | `Sofunny.BiuBiuBiu2.NetworkMessage.UGC` |
| UGC 数据配置（AbilityM / Config） | `Sofunny.BiuBiuBiu2.Data` |

---

## 三、命名规范

**所有 UGC 文件名以 `_UGC` 后缀结尾**（`SAB_` / `CAB_` / `GPOM_` 框架前缀保留在最前面，UGC 标识统一放末尾）。

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| PGC 钩子扩展文件 | `PGC类名_UGC.cs` | `ServerAIWorld_UGC.cs` / `GpoSet_UGC.cs` |
| 服务端 GPO System | `ServerAIXxxSystem_UGC.cs` | `ServerAIFollowDroneSystem_UGC.cs` |
| 客户端 GPO System | `ClientAIXxxSystem_UGC.cs` | `ClientAIFollowDroneSystem_UGC.cs` |
| GPO 行为组件 | `ServerAIXxxBehavior_UGC.cs` | `ServerAIDroneFollow_UGC.cs` |
| Mode 组件 | `ServerXxxMode_UGC.cs` | `ServerTestMode_UGC.cs` |
| SAB System | `SAB_XxxSystem_UGC.cs` | `SAB_DroneShotSystem_UGC.cs` |
| SAB Component | `SABXxxXxx_UGC.cs` | `SABDroneShotFlyHit_UGC.cs` |
| CAB System | `CAB_XxxSystem_UGC.cs` | `CAB_DroneShotSystem_UGC.cs` |
| GPOM 数据文件 | `GPOM_XxxSet_UGC.cs` | `GPOM_FollowDroneSet_UGC.cs` |
| UGC 常量/ID 集 | `GpoTypeSet_UGC.cs`（partial class 追加） | `GpoTypeSet_UGC.cs` |

> **规则**：`_UGC` 是层级标识后缀，不是前缀。框架类型前缀（`SAB_` / `CAB_` / `GPOM_`）最优先，`_UGC` 紧跟 System/Set 等语义词之后置于末尾。

**System 类文件（GPO System / SAB / CAB）文件名必须以 `System_UGC` 结尾**。Mode 组件、Weapon、GPO 行为组件不加 `System` 中缀。

---

## 四、目录结构规范

`Assets/Scripts/UGC/` 是 UGC 所有代码的根目录。当前实际目录结构（以第一个 UGC 项目为基准）：

```
Assets/Scripts/UGC/
│
├── Sofunny.BiuBiuBiu2.UGC.asmdef          ← UGC 程序集定义（勿移动）
│
├── Message/
│   └── Network/
│       └── 100_Proto_UGC.cs               ← UGC 网络协议（ModID=100）ns: NetworkMessage.UGC
│
├── Template/                              ← UGC 静态数据定义（ns: Template.UGC）
│   └── gpo/
│       ├── GpoTypeSet_UGC.cs               ← GPO 类型 ID（partial class，ns: Template，与 PGC 对齐）
│       ├── GPOM_FollowDroneSet_UGC.cs     ← 无人机 GPOM 模板数据
│       └── GPOM_TargetDummySet_UGC.cs     ← 靶子 GPOM 模板数据
│
├── Data/                                  ← UGC 运行时数据配置（ns: Data，与 PGC 配置层一致）
│   └── Configs/
│       └── Ability/
│           ├── AbilityConfig_UGC.cs        ← UGC AbilityConfig 工厂（ns: Template.UGC）
│           └── AB/
│               └── TemplateM/
│                   ├── AbilityM_UGCDroneShot.cs          ← 无人机子弹 AB 模板数据（ns: Data）
│                   └── Select/
│                       └── AbilityM_UGCDroneShot_Select.cs
│
└── GamePlay/                              ← UGC 游戏逻辑（按 Server/Client/Core 分层）
    ├── GameWorld_UGC.cs                   ← 注册入口（反射自动发现，ns: GamePlay.UGC）
    ├── Core/
    │   └── CoreGameWorld_UGC.cs           ← 公共注册：GPO行/GPOM/Scene/Mode/Proto（ns: ClientGamePlay.UGC）
    ├── Server/                            ← 服务端逻辑（ns: ServerGamePlay.UGC）
    │   ├── ServerGameWorld_UGC.cs         ← 服务端注册：GPO System/Mode/AB 工厂
    │   ├── Mode/
    │   │   └── ServerTestMode_UGC.cs      ← UGC 测试 Mode 服务端组件
    │   ├── AI/
    │   │   ├── Systems/                   ← GPO System（继承 S_AI_Base）
    │   │   │   ├── ServerAIFollowDroneSystem_UGC.cs
    │   │   │   └── ServerAITargetDummySystem_UGC.cs
    │   │   └── Components/                ← GPO Component（继承 ComponentBase）
    │   │       ├── ServerAIDroneFollow_UGC.cs
    │   │       └── ServerAIDroneFire_UGC.cs
    │   └── Ability/
    │       └── System/
    │           └── SAB/                   ← 服务端 Ability System + Component
    │               ├── SAB_DroneShotSystem_UGC.cs
    │               └── SABDroneShotFlyHit_UGC.cs
    └── Client/                            ← 客户端逻辑（ns: ClientGamePlay.UGC）
        ├── ClientGameWorld_UGC.cs         ← 客户端注册：GPO System/Mode/CAB 工厂
        ├── Mode/
        │   └── ClientTestMode_UGC.cs      ← UGC 测试 Mode 客户端组件
        ├── AI/
        │   └── Systems/                   ← 客户端 GPO System（继承 C_AI_Base）
        │       ├── ClientAIFollowDroneSystem_UGC.cs
        │       └── ClientAITargetDummySystem_UGC.cs
        └── Ability/
            └── System/
                └── CAB/                   ← 客户端 Ability System
                    └── CAB_DroneShotSystem_UGC.cs
```

**目录对应规则**：`UGC/GamePlay/` 子目录层级必须与 `Scripts/GamePlay/` 完全对应，禁止跳层。

**高频错误：**
- SAB / CAB 漏写中间层 `System/`：应为 `Ability/System/SAB/`，不是 `Ability/SAB/`
- Server GPO System 放进 `Components/`：应在 `Systems/`
- Mode 组件放 `Mode/` 根目录：应在 `Mode/` 下（当前 UGC 测试 Mode 即放此处）

---

## 五、Component 编码规范（GPO Component 专属）

> GPO Component 编码规范（private 成员、InitData 注入、AddUpdate 时机）已统一收录至 **`gpo-code.md §六`**，UGC Component 完全适用，无额外差异，请直接参阅该章节。

---

## 六、ID 范围

所有 ID 必须在对应 IdSet 常量中定义，禁止 hardcode。

| 系统 | 值 | 定义位置 |
|------|---|---------|
| GPO 类型 ID | `10000 ~ 19999` | `GpoTypeSet_UGC.cs` |
| Mode 数据 Id | `ModeData.Id_UGCTestMode`（由 PGC 定义，当前值 `20001`） | **PGC** `Data/ModeData.cs` |
| Mode 枚举坑位 | `ModeData.ModeEnum.ModeUGCTest = 100`（固定，PGC 已预留） | PGC `Data/ModeData.cs` |
| Scene 数据 Id | `SceneData.SceneId_UGCTest`（由 PGC 定义，当前值 `99998`） | **PGC** `Data/SceneData.cs` |
| AB / AE TypeID | 字符串，前缀 `"UGC_AB_"` / `"UGC_AE_"` | `AbilityConfig_UGC.cs`（`AB_UGCDroneShot` 等） |
| Weapon itemId | `50000 ~ 59999` | `UGCItemIdSet.cs` |

> **重要约束**：Mode ID 使用 PGC 定值 `ModeData.Id_UGCTestMode`，UGC 直接引用，禁止在 UGC 代码中硬编码数字。
> Mode 的大厅入口（`ModeMatch`）由 PGC `ModeData.GetAllGameMatches()` 直接管理，UGC 不另行注入。
> Mode 运行时属性通过 `ModeData.RegisterUGCScene(new ModeData.Data {...})` 在 `CoreGameWorld_UGC.OnInit()` 中覆盖（PGC `AddTestMode` 已预埋空白占坑 `{Id=20001, Mode=ModeUGCTest}`）。
> Scene 注册（`SceneData.RegisterUGCScene()`）和 Mode 属性覆盖均在 `CoreGameWorld_UGC.OnInit()` 中执行（非 server/client 分支内），确保双侧均可查到。

---

## 七、GPO 注册三步规则

新增 UGC GPO 时，必须完成以下三步，缺一运行时崩溃：

```csharp
// CoreGameWorld_UGC.OnInit() — 公共区（Server + Client 均需）
// 2. GPOM 数据路由（缺少 → GetGPOMData 返回 null）
GpoSet.RegisterUGCGPOM(
    GpoTypeSet.Id_UGCXxx,
    (id, mode) => GPOM_UGCXxxSet.GetGPOMByIdAndMatchMode(id, mode)
);
// 3. Gpo 行数据（缺少 → GetGpoById 返回 default，流程中断）
GpoSet.RegisterUGCGpoRow(
    new Gpo(GpoTypeSet.Id_UGCXxx, GpoTypeSet.Id_UGCXxx, "UGCXxx", "UGCXxx", "UGCXxx", "")
);

// ServerGameWorld_UGC.OnInit() — 服务端区
// 1. GPO System 工厂
ServerAIWorld.RegisterGPOSystem(
    GpoTypeSet.Id_UGCXxx,
    (mgr, cb) => mgr.AddSystem<UGCServerAIXxxSystem>(cb)
);
```

> GPOM 数据格式（`struct GPOM_UGCXxx : IGPOM` + `static class GPOM_UGCXxxSet`）参照 `gpo-code.md §一`。

---

## 八、AI GPO 血量注意事项

> 此规则适用于所有有 HP 的 AI GPO（PGC + UGC），已统一收录至 **`gpo-code.md §六点五`**，请直接参阅该章节。

---

## 九、[Dev_Leader] UGC 追加检查清单

Round 审核含 UGC 内容的文档时，在 `core-rules.md` 检查清单基础上追加：

```
U0  所有新建/修改文件路径全在 Assets/Scripts/UGC/ 下（最高优先级）：✅ / ❌
U1  PGC 钩子标注【已有·调用】，未误标【新建】/【修改】：✅ / ❌
U2  Namespace 符合 §二 分区规范（ServerGamePlay.UGC / ClientGamePlay.UGC 等）：✅ / ❌
U3  文件名以 _UGC 后缀结尾（SAB_/CAB_/GPOM_ 前缀例外）：✅ / ❌
U4  System 文件名以 System_UGC 结尾：✅ / ❌ / N/A
U5  UGC 目录层级对应 PGC，无跳层：✅ / ❌
U6  ID 通过 IdSet 常量引用，无 hardcode：✅ / ❌
U7  GPO 注册三步完整：✅ / ❌ / N/A
U8  AddComponents() 首行有 base.AddComponents()：✅ / ❌ / N/A
U9  需要 HP 的 AI GPO 已添加 ServerAIAttribute：✅ / ❌ / N/A  （规则详见 gpo-code.md §六点五）
U10 未在 Client 代码中使用 Shader.Find() 创建材质（见 shader-code.md §六）：✅ / ❌
```

> ❌ U0 不通过时，[Dev_Leader] **必须立即纠正**，不得继续下一步。

---

## 十、UGC 模板覆盖规范

### 核心原则

**UGC 用户在现有模板基础上通过注册接口覆盖行为，禁止修改模板文件本身。**

| 操作 | 规则 |
|------|------|
| 覆盖/实现模板接口（注册工厂/System） | ✅ 允许，这是标准做法 |
| 修改 `Template/` 下的模板文件 | ❌ 禁止，模板是公共基础 |
| 在模板 `GPOM_XxxSet_UGC.cs` 里加特定逻辑 | ❌ 禁止，数据与逻辑分离 |
| 拷贝模板文件后另存为新文件 | ✅ 允许（新文件命名遵循 §三 命名规范） |

### 模板覆盖的标准方式

以无人机 GPO 为例，模板已提供 `GPOM_FollowDroneSet_UGC`，用户**不需要**修改它，只需通过注册接口覆盖：

```csharp
// CoreGameWorld_UGC.OnInit() 中注册自己的数据工厂
GpoSet.RegisterUGCGPOM(
    GpoTypeSet.Id_UGCFollowDrone,
    (id, mode) => MyCustomDroneSet.GetGPOMByIdAndMatchMode(id, mode)
    // ↑ 自定义数据集，不改原模板
);
```

### 模板目录说明

`Assets/Scripts/UGC/Template/` 是 PGC 提供给 UGC 用户的参考模板，包含：

| 文件 | 说明 | 用户操作 |
|------|------|---------|
| `gpo/GpoTypeSet_UGC.cs` | GPO 类型 ID（partial class） | 追加新 ID 常量，不删除已有 |
| `gpo/GPOM_FollowDroneSet_UGC.cs` | 无人机 GPOM 模板数据 | 只读参考，如需自定义拷贝后另存 |
| `gpo/GPOM_TargetDummySet_UGC.cs` | 靶子 GPOM 模板数据 | 只读参考，如需自定义拷贝后另存 |

> **Mode ID 使用**：直接引用 PGC `ModeData.Id_UGCTestMode`，无需单独文件镜像。  
> **AB TypeID 使用**：定义在 `Data/Configs/Ability/AbilityConfig_UGC.cs` 的字符串常量（如 `AbilityConfig_UGC.AB_UGCDroneShot`），无需单独文件。

> **场景制作**的模板使用规范见 `scene-code.md §十`（以 `Map_Template` 为基础场景复制）。

---

## 十一、Codegen 脚本 UGC/PGC 模式判定

### 判定规则

当 Agent 调用 codegen 脚本（`ability-gen.sh`、`gpo-gen.sh`、`gpom-gen.sh`、`mode-gen.sh`、`component-gen.sh`）时，**必须根据当前功能判断是否添加 `--ugc` 标志**：

| 条件 | 模式 | 操作 |
|------|------|------|
| 当前功能属于 UGC 模块（产出文件在 `Assets/Scripts/UGC/` 下） | UGC | 脚本命令追加 `--ugc` |
| 当前功能属于 PGC（产出文件在 `Assets/Scripts/` 非 UGC 目录下） | PGC | 不加 `--ugc`（默认行为） |

### 判断依据优先级

1. **session-state/active.md** 中的活跃功能名包含 "UGC" → UGC 模式
2. **设计文档**明确标注产出目录为 `Assets/Scripts/UGC/` → UGC 模式
3. **用户指令**明确要求 UGC 或 PGC → 按指令执行

### `--ugc` 标志的行为差异

| 操作 | PGC（默认） | UGC（`--ugc`） |
|------|-----------|---------------|
| CREATE 路径 | `Assets/Scripts/...` | `Assets/Scripts/UGC/...` |
| Namespace | 标准（如 `ServerGamePlay`） | 追加 `.UGC`（如 `ServerGamePlay.UGC`） |
| System 类名 | `SAB_XxxSystem` | `SAB_XxxSystem_UGC` |
| MODIFY 目标 | PGC 注册文件（`AbilityConfig_AutoGenerated.cs` 等） | UGC 注册枢纽（`AbilityConfig_UGC.cs`、`CoreGameWorld_UGC.cs` 等） |
| RPC | 独立 Proto 文件 + 独立 ModID | `partial class Proto_UGC` + 共享 ModID=100 |
| ID 范围 | PGC 范围（见 §六） | UGC 范围（ConfigId 60001+、GpoType 10000+） |

### 容错机制

若传了 `--ugc` 但项目未安装 UGC hook 文件（`ugc/` 目录不存在），脚本会输出 `⚠️` 警告并**自动回退到 PGC 流程**，不会崩溃。

> **禁止**：在 UGC 功能开发中遗漏 `--ugc` 标志（会导致文件生成到 PGC 目录，违反 §零 最高优先级规则）。
