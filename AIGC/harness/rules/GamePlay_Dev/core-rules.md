# 核心开发规则（Core Rules）

> **适用范围**：DL/ GPO 工程师 / Ability 工程师（涉及 C# 编码的所有 Agent）
> **场景建设工程师不需要读本文件**，只需读 `technical-doc-format.md` + `scene-code.md`
> **优先级**：仅次于 `safety-rules.md`，不可被任何 feature 需求覆盖
>
> ⚠️ **Shader + 美术占位规范**见独立文件 `GamePlay_Dev/shader-code.md`（场景建设 Agent 也需读，故不合并入本文件）

## 📌 场景导航（按任务类型快速定位）

| 场景 | 必读章节 |
|------|---------|
| **任何编码任务** | 第一章 + 第二章 Part1/Part5 + 第五章 |
| GPO → Mode 跨系统事件通信 | 额外读 第二章 Part2 |
| 实现伤害 / 飘血 | 额外读 第二章 Part3 |
| 程序化构建 Entity（new GameObject） | 额外读 第二章 Part4 |
| 涉及网络 RPC / 玩家中途加入 | 额外读 第四章 |
| Gameplay 碰撞 / 区域 / GC 优化 | 额外读 第三章 |

---

# 第一章：开发前必问清单（避坑协议）

凡触发以下任一场景，必须先向用户提问，等待确认后再动手。

## 1.1 关于对象的"系统归属"问题

**触发条件**：需求中出现「武器、飞行物、悬浮体、跟随体、附着体、召唤物」等对象时。

**必须询问**：
> "这个对象是：
> A. **独立的 AI(GPO) 单元**（有自己的血量/AI行为/可被攻击）
> B. **是否手持武器**（手持武器才走枪械系统，否则走 GPO 系统）
> 请确认后我再决定走 GPO 系统还是枪械/其他系统。"

## 1.2 关于"现有组件复用"前置检查

**触发条件**：开始实现任何新功能前，先查下表确认应走哪条系统链路。

检索顺序：① system-map.md 系统地图 → ② 范例文档 → ③ 再动手

| 需求 | 说明 | 核心系统 |
|------|------|---------|
| AI + GPO | 所有可交互玩法内容，含部分迷你规则 | `ServerAIWorld` + `ClientAIWorld` |
| 武器（Weapon） | 角色手持武器；手持以外的可交互物体走 GPO | `ServerWeaponManager` + `ClientWeaponManager` |
| 模式（Mode） | 核心循环规则，控制战斗节奏与玩家体验 | `ServerModeSystem` + `ClientModeSystem` |
| 玩家（Character） | 参与游戏的角色实体 | `ServerCharacterSystem` `CharacterLocalSystem` `CharacterOtherSystem` |
| 刷怪 / 波次 | 刷新敌人、定时或触发式生成单位 | `ServerAIGPOSpawnerSystem` + `AIGpoSpawnerConfig` |
> 详细系统地图见 [[knowledge/system-map]] §二 游戏系统地图

## 1.3 关于美术资源的占位方案

执行计划中涉及新视觉对象时，必须明确：
- **形状**（Cube / Sphere / Cylinder / Line）
- **颜色**（_BaseColor 的 RGBA 值）
- **尺寸**（宽 × 高 × 深，单位：m）
- **挂点/偏移位置**描述

**禁止**只写"白色Cube占位"而不提供具体尺寸和挂点位置。

> 💡 **Skill 提取**：§1.4-1.6 的核心循环验证方法论已提取为独立认知框架，详见 [[核心循环完整性检查框架]]

## 1.4 关于"核心循环"的完整性定义

核心循环必须包含（缺一不可）：

```
① 触发条件（什么时候进入这个循环？）
② 玩家输入/交互（玩家做什么操作？）
③ 客户端 UI 反馈（界面上显示了什么？）
④ CMD 数据上传（玩家操作如何通知服务端？）
⑤ 服务端逻辑处理（服务端如何响应？）
⑥ RPC 数据下发（服务端如何通知客户端结果？）
⑦ 客户端表现（最终玩家看到什么反馈？）
⑧ 循环出口（这个循环什么时候结束/转移到下一状态？）
```

## 1.5 关于技术设计文档的"关键交互链路"要求

**触发条件**：功能涉及玩家输入（点击按钮、选择词条、确认操作等）时。

**执行计划必须包含**：

```
[玩家输入]
  → [客户端 UI 组件 OnGUI/Button 响应]
  → [CMD 消息发送（CharacterLocalSystem权限）]
  → [服务端 System/Component 接收]
  → [服务端逻辑处理 + 状态更新]
  → [RPC/TargetRpc 广播结果]
  → [客户端接收 RPC + 表现层]
```

若技术设计文档中缺少此链路图，**禁止进入开发阶段**。

## 1.6 核心循环完整性 Checklist（执行计划阶段必做）

在确定「最小核心循环 / 阶段1」之前，逐项核对以下问题：

| # | 检查项 | 内容 | 是否已定义 |
|---|--------|------|----------|
| ① | 触发条件 | 什么时候进入这个循环？ | ☐ |
| ② | 玩家输入 | 玩家需要做什么操作？有无点击/选择/确认行为？ | ☐ |
| ③ | 客户端 UI | 是否有界面需要弹出/更新？缺 UI 是否会导致玩家无法操作？ | ☐ |
| ④ | CMD 链路 | 玩家操作如何通知服务端？是否定义了对应 CMD 消息？ | ☐ |
| ⑤ | 服务端处理 | 服务端如何响应，结果如何存储？ | ☐ |
| ⑥ | RPC 下发 | 服务端如何广播结果给各客户端？ | ☐ |
| ⑦ | 客户端表现 | 玩家最终看到什么反馈（UI关闭/动画/特效）？ | ☐ |
| ⑧ | 循环出口 | 这个循环何时结束或跳转下一状态？ | ☐ |

**若②③任意一项为"有，但未定义"**，则该功能**不得归入后续阶段**，必须纳入核心循环阶段一并实现。

---

# 第二章：ECS 代码规范（全局强制）

## 第一部分：ECS 架构规则（System / Component）

### Rule 1：System 只做组装，不含业务逻辑

System 仅允许做两件事：1. **组装 Component**（`AddComponent<T>()`、`BuildAndSetEntity()`）；2. **暂代资源引用**（声明 Transform/GameObject 供同 System Component 访问）。

**System 中一律禁止**：`AddUpdate(...)` 帧更新、状态机、条件判断、伤害计算等业务逻辑。

```csharp
// ✅ 正确
public class ServerAIBIU26EnemyChargeSystem : S_AI_Base {
    protected override void OnAwake() {
        AddComponent<ServerAIBIU26EnemyChargeMainComponent>();
        AddComponent<ServerAIBIU26EnemyMoveComponent>();
    }
}

// ❌ 错误：System 含帧更新
protected override void OnAwake() {
    AddUpdate(OnUpdate);          // ❌ 禁止
}
```

### Rule 1.1：Component 禁止调用 AddComponent
`AddComponent<T>()` 只能在 **System 的 `OnAwake()`** 中调用，Component 内部**禁止**反向调用。
```csharp
// ❌ Component 内反向调用 System 组装
protected override void OnAwake() {
    mySystem.AddComponent<SomeOtherComponent>(); // 禁止
}

// ✅ 所有组装统一在 System.OnAwake() 中声明
```
> 原因：Component 是逻辑单元，不负责自身或他者的组装。

### Rule 2：Component 所有成员一律 private

Component 内的**字段、属性、方法**全部声明为 `private`。唯一例外：继承自基类的**生命周期函数**保留 `protected override`（`OnAwake`、`OnDestroy`、`OnSetNetwork`）。

```csharp
// ✅                                          // ❌
private float _chargeSpeed = 8f;              public float ChargeSpeed = 8f;     // ❌
private void OnUpdate() { ... }               public void StartCharge() { ... }  // ❌
protected override void OnAwake() { ... }     // ✅ 生命周期例外
```

### Rule 3：外部访问 Component 只能通过事件

- Component 之间只能用 SE_ 事件互相访问，禁止直接字段引用（含 `static`）或直接调用方法
- 不可将 `SystemBase` / `ComponentBase` 作为参数传给其他代码

```csharp
// ✅ 派发事件
mySystem.Dispatcher(new SE_BIU26Enemy.Event_StartCharge { TargetGpoId = targetId });
// ✅ 在 OnAwake 中监听
Register<SE_BIU26Enemy.Event_StartCharge>(OnStartCharge);

// ❌ 直接调用 Component 方法
GetComponent<ServerAIBIU26EnemyChargeMainComponent>().StartCharge();
```

### Rule 4：事件注册时机规则

- **事件的注册需要写在 Component 的 `OnAwake()` 里**
- **事件的派发不能写在 Component 的 `OnAwake()` 里**
- **`AddUpdate(OnUpdate)` 不能写在 Component 的 `OnAwake()` 里**（帧更新注册需在初始化完成后）
- **`AddProtoCallBack` 需要写在 `protected override void OnSetNetwork()` 里**

### Rule 5：CMD 权限约束

**CMD 的使用只有 `CharacterLocalSystem` 下 `ClientCharacterComponent` 才有权限**

---

## 第二部分：跨系统事件通信

### Rule 6：GPO → Mode 跨系统事件通知

> 来源：坦克大乱斗 Phase 3 SuperBuff 联调复盘

**核心原则**

`SE_XXX.EventYYY` 走 **GPO 本地系统总线**，不走全局 MsgRegister。因此 GPO 内派发的 SE_ 事件，Mode 中 `Register<T>` 永远收不到（两个不同 System）。

**正确做法：通过 SM_AI.Event_AddAI 回调拿到 GPO System**

```csharp
// ❌ 错误：在 Mode 自身 System 上注册
// Register<SE_TankBattle.Event_BuffPickedUp>(OnBuffPickedUp);  // 永远收不到！

// ✅ 正确：监听 AddAI 事件 → 拿到 GPO system → 在它上面注册
protected override void OnAwake()
{
    MsgRegister.Register(new SM_AI.Event_AddAI { AISign = GPOM_SuperBuffSet.Sign_SuperBuff },
        (evt) =>
        {
            evt.system.Register<SE_TankBattle.Event_BuffPickedUp>(OnBuffPickedUp);
        });
}
```

**GPO 侧：必须用 `mySystem.Dispatcher`（不能用 `MsgRegister.Dispatcher`）**

```csharp
// ✅ 正确
mySystem.Dispatcher(new SE_TankBattle.Event_BuffPickedUp { pickerGpoId = enterGpoId });

// ❌ 错误：SE_ 事件用 MsgRegister.Dispatcher → 无法与 System 本地监听对接
// MsgRegister.Dispatcher(new SE_TankBattle.Event_BuffPickedUp { ... });
```

| 派发方式 | 注册方式 | 是否配对 |
|---------|---------|---------|
| `mySystem.Dispatcher(SE_evt)` | `Register<T>` 在**同一** System | ✅ |
| `mySystem.Dispatcher(SE_evt)` | `Register<T>` 在**不同** System | ❌ |
| `mySystem.Dispatcher(SE_evt)` | via `SM_AI.Event_AddAI → evt.system.Register<T>` | ✅ |
| `MsgRegister.Dispatcher(SM_msg)` | `MsgRegister.Register(SM_msg, callback)` | ✅（全局） |

### Rule 7：自定义 GPO 的移除方式

`SE_AI.Event_OnRemoveAI` 仅对含 `ServerAIDead` 的标准 AI 有效。自定义 GPO 使用全局事件：

```csharp
// ✅ 正确
MsgRegister.Dispatcher(new SM_AI.Event_RemoveAI { GpoId = iGPO.GetGpoID() });
```

| 发送方式 | 作用域 | 适用场景 |
|---------|--------|---------|
| `Dispatcher(evt)` | 当前 GPO 本地系统 | Component 之间通信（同一 GPO 内） |
| `MsgRegister.Dispatcher(evt)` | 全局世界，跨 GPO/System | 移除 GPO、物品掉落、SM_ 消息广播 |

### Rule 8：MasterGPO 继承链规范

```csharp
// ✅ 正确：召唤物的主人应为顶层玩家，而非中间召唤者
MasterGPO = aiSystem.MasterGPO ?? iGPO,
```

---

## 第三部分：伤害事件规范

### Rule 9：使用 Event_GPOHurt 而非 Event_DownHP

```csharp
hitGPO.Dispatcher(new SE_GPO.Event_GPOHurt {
    Hurt = atk,
    AttackGPO = iGPO,
    DamageType = DamageType.Normal,
});
```

### Rule 10：飘血动画需要显式调用 PlayBloodSplatter AB

飘血动画**不会自动触发**，需要显式调用：

```csharp
MsgRegister.Dispatcher(new SM_Ability.PlayAbility {
    FireGPO = iGPO,
    MData = AbilityM_PlayBloodSplatter.CreateForID(AbilityM_PlayBloodSplatter.ID_BloodSplatter),
    InData = new AbilityIn_PlayBloodSplatter {
        In_HitGpoId = hitGPO.GetGpoID(),
        In_HitPoint = hitGPO.GetBodyTran(GPOData.PartEnum.Body)?.position ?? hitGPO.GetPoint(),
        In_BloodValue = atk,
        In_HitItemId = 0,
    }
});
```

---

## 第四部分：程序化 Entity 构建规范

### Rule 11：SetGameObjectEntity 的使用

| 方法 | 适用场景 |
|------|---------|
| `SetEntity(go, layer)` | 内部方法，Prefab 加载路径自动调用，无需手动调用 |
| `SetGameObjectEntity(go, layer)` | **所有程序化 `new GameObject()` 的 Entity** |

程序化构建的实体**必须用** `SetGameObjectEntity`，否则 Clear 时 GameObject 不会被销毁，产生内存泄漏。

| 实体类型 | 前置要求 |
|---------|---------|
| GPO 类（AI 单位、可受击场景物体） | HitType + AIEntity（顺序见 gpo-code.md）→ `SetGameObjectEntity` |
| 武器实体（WeaponEntity / GunEntity） | 直接 `SetGameObjectEntity`，不需要 HitType / AIEntity |
| 特效 / 场景装饰 Entity | 直接 `SetGameObjectEntity`，不需要 HitType / AIEntity |

### Rule 12：HitType 规则

- 每个 GameObject **只能有一个** `HitType` 组件
- 根节点（root）**必须是** `PartEnum.RootBody`
- `Layer`：`World` = 可受击，`Ignore` = 不参与检测

```csharp
rootHit.Part = GPOData.PartEnum.RootBody;
rootHit.Layer = GPOData.LayerEnum.World;
bodyHit.Part = GPOData.PartEnum.Body;
bodyHit.Layer = GPOData.LayerEnum.World;
```

### Rule 13：OnSetEntityObj 时机

`OnStart()` 在 `SetGameObjectEntity()` **之前**触发，依赖 Transform/Entity 的逻辑必须写在 `OnSetEntityObj` 里。

```csharp
// ❌ OnStart 中访问 Body：空引用
// ✅ 正确时机：
protected override void OnSetEntityObj(IEntity iEntity) {
    base.OnSetEntityObj(iEntity);
    selfTransform = iGPO.GetBodyTran(GPOData.PartEnum.RootBody);
}
```

### Rule 14：子节点 Transform 获取方式

子节点 Transform 通过 `HitType` + `GetBodyTran` 获取（禁止通过自定义事件直接传递 Transform）：

```csharp
// 构建时加 HitType
headGo.AddComponent<HitType>().Part = GPOData.PartEnum.Head;

// OnSetEntityObj 中获取
headTransform = iEntity.GetBodyTran(GPOData.PartEnum.Head);
```

### Rule 15：服务端程序化 Entity 不得保留 Renderer

```csharp
// ✅ 推荐：空 GameObject
var headGo = new GameObject("Head");
headGo.AddComponent<HitType>().Part = GPOData.PartEnum.Head;

// ✅ 备选：CreatePrimitive 后立即销毁 Renderer + MeshFilter
```

### Rule 16：AI 实体 Scale 设置规范

**❌ 无效方式**：修改 Prefab 根节点 `m_LocalScale`。加载时会被 `EntityData`（默认 `Vector3.one`）覆盖。

**✅ 正确方式**：在客户端 AI System 的 `OnStart()` 中，**`CreateEntity()` 调用前**设置：

```csharp
protected override void OnStart() {
    base.OnStart();
    // iEntity 此时是 EntityData，设置后 IsScaleChange = true
    // SetIEntity() 挂载真实 entity 时自动应用
    iEntity.SetLocalScale(Vector3.one * 2f);
    CreateEntity(MData.GetAssetSign());
}
```

**机制**：`SystemBase.SetIEntity()` 检查 `entityData.IsScaleChange`，若为 true 则将预设 scale 写入真实 entity。

### Rule 17：AI Prefab 加载路径（C_AI_Base）

| 方法 | 最终 Prefab 路径 |
|------|---------------|
| `CreateEntity(sign)` | `Assets/Bundle/GamePlay/AI/Client/{sign}.prefab` |
| `CreateSharedEntity(sign)` | `Assets/Bundle/GamePlay/AI/Shared/{sign}.prefab` |
| `CreateEntityToPool(sign)` | `Assets/Bundle/GamePlay/AI/Client/{sign}.prefab`（池化） |

新建 AI Prefab 必须放在对应目录，否则运行时 `[Error]加载失败: ...`。

### Rule 18：YAML 手动添加组件必须同时修改两处

```yaml
# 1. 根 GameObject m_Component 列表追加引用
m_Component:
- component: {fileID: 原有fileID}
- component: {fileID: 新组件fileID}   # ← 必加

# 2. 文件末尾追加 MonoBehaviour 数据块
--- !u!114 &新组件fileID
MonoBehaviour:
  m_GameObject: {fileID: 根GOfileID}
  m_Script: {fileID: 11500000, guid: 脚本GUID, type: 3}
  # 字段...
```

缺少任意一处，Unity 导入时无法识别该组件。

### Rule 19：assetSign vs sign（GPOM 双标识）

| 字段 | 方法 | 用途 |
|------|------|------|
| `AssetSign` | `GetAssetSign()` | 视觉 Prefab 文件名 → 传给 `CreateEntity()` |
| `Sign` | `GetSign()` | AI 类型唯一标识符 → 传给 `Event_AddAI.AISign` |

客户端 `OnStart()` 加载 Prefab 用 `GetAssetSign()`，不要用 `GetSign()`。

---

## 第五部分：全局 C# 强制规范

### Rule 16：所有 C# 文件必须声明 namespace

```csharp
// ✅ namespace Sofunny.BiuBiuBiu2.ServerGamePlay { public class MySystem : S_AI_Base { ... } }
// ❌ public class MySystem : S_AI_Base { ... }  // 无 namespace
```

### Rule 17：禁止创建或修改程序集（.asmdef）

不允许：新建 `.asmdef` / 修改已有 `.asmdef` / 将类迁移至新建程序集。所有代码必须放入**现有程序集**（主体为 `Assembly-CSharp`）。

### Rule 18：using 声明必须位于 namespace 之前（外部）

```csharp
// ✅ 正确
using System;
using Sofunny.BiuBiuBiu2.ServerMessage;

namespace Sofunny.BiuBiuBiu2.ServerGamePlay
{
    public class MySystem : S_AI_Base { ... }
}

// ❌ 错误：using 在 namespace 内部
namespace Sofunny.BiuBiuBiu2.ServerGamePlay
{
    using System;  // ❌ 禁止
}
```

### Rule 19：C# 命名规范

| 修饰符 | 命名格式 | 示例 |
|--------|---------|------|
| `private` 字段 | camelCase（无下划线前缀） | `private float checkDistance;` |
| `public` 字段/属性 | PascalCase | `public float CheckDistance;` |
| `const` | SCREAMING_SNAKE_CASE | `const float CHECK_DISTANCE = 10f;` |
| 局部变量 | camelCase | `var bestTarget = null;` |
| 方法名 | PascalCase | `private void FindNearestEnemy()` |
| 参数 | camelCase | `void OnUpdate(float delta)` |

```csharp
// ✅ 正确
private float checkDistance;
private IGPO currentTarget;
public float CheckDistance;
const int MAX_RETRY_COUNT = 3;

// ❌ 错误
private float _checkDistance;   // 禁止下划线前缀
private float check_distance;  // 禁止蛇形命名
```

### Rule 20：服务端 Transform 变化必须通过 iEntity 同步

直接修改 `rootTran.position` / `rootTran.rotation` / `rootTran.localScale` **仅改变服务端本地 Transform**，不会同步到客户端。如需客户端同步，必须调用对应的 `iEntity` 方法：

| 变化 | 同步方法 |
|------|---------|
| 位置 | `iEntity.SetPoint(newPosition)` |
| 旋转 | `iEntity.SetRota(newRotation)` |
| 缩放 | `iEntity.SetLocalScale(newScale)` |

```csharp
// ✅ 正确：先修改 Transform 再同步
rootTran.position += rootTran.forward * speed * delta;
iEntity.SetPoint(rootTran.position);

var newRot = Quaternion.Slerp(rootTran.rotation, targetRot, speed * delta);
rootTran.rotation = newRot;
iEntity.SetRota(newRot);

// ❌ 错误：仅修改 Transform，客户端看不到变化
rootTran.position += rootTran.forward * speed * delta;  // 缺少 iEntity.SetPoint
rootTran.rotation = targetRot;                           // 缺少 iEntity.SetRota
```

### Rule 21：AI Component 开发必须优先使用模板

新建 Server AI Component 时，**必须先检查是否有匹配的预置模板**，有则用 `--template`，无则手动编写。

| 模板 | 适用场景 | 命令示例 |
|------|---------|---------|
| `findtarget` | 周期扫描索敌 | `--template findtarget` |
| `lifetime` | 倒计时自毁 | `--template lifetime` |
| `move` | 方向移动 + SetPoint | `--template move` |
| `rotate` | A→B 旋转插值 + SetRota | `--template rotate` |
| `scale` | A→B 缩放插值 + SetLocalScale | `--template scale` |

**开发流程**：
1. `gpo-gen.sh` → 生成 System + 注册
2. `gpom-gen.sh` → 生成 GPOM 模板数据
3. `component-gen.sh --template xxx` → 按需生成各 Component
4. 在 `System.AddComponents()` 中组装

**Graybox 模式**：`gpo-gen.sh` 默认生成 Graybox 占位体（Box 碰撞 + 红色 Cube），用 `--shape`/`--size`/`--color` 定制，或 `--model` 指定模型路径关闭 Graybox。

---

| 类型 | 命名空间 |
|------|---------|
| Server AI System / Component | `Sofunny.BiuBiuBiu2.ServerGamePlay` |
| Client AI System / Component | `Sofunny.BiuBiuBiu2.ClientGamePlay` |
| GPO 数据结构（`GPOM_XXX` struct） | `Sofunny.BiuBiuBiu2.Template` |
| Mode System / Component | `Sofunny.BiuBiuBiu2.ServerGamePlay` |
| Ability（`SAB_XXX` / `SAE_XXX`） | `Sofunny.BiuBiuBiu2.ServerGamePlay` |
| `DamageType` | `Sofunny.BiuBiuBiu2.Template` |
| `AbilityM_PlayBloodSplatter`, `AbilityIn_PlayBloodSplatter` | `Sofunny.BiuBiuBiu2.Data` |
| `SM_Ability`, `SE_GPO`, `SE_AI` | `Sofunny.BiuBiuBiu2.ServerMessage` |
| `MsgRegister`, `IEntity`, `IGPO` | `Sofunny.BiuBiuBiu2.Message` / `CoreGamePlay` |
| `HitType`, `AIEntity` | `Sofunny.BiuBiuBiu2.Component` |
| `GPOData`, `LayerData`, `StageData` | `Sofunny.BiuBiuBiu2.Data` |

---

## [项目负责人]代码合规检查清单

当技术文档中含有 C# 代码示例时，逐条核查：

```
【代码合规检查 — {文档名}】
R1  System 无业务逻辑（只有 AddComponent）：✅ / ❌（行XX）
R2  Component 所有成员 private（生命周期除外）：✅ / ❌（行XX）
R3  外部访问 Component 通过事件：✅ / ❌（行XX）
R4  事件注册/派发时机正确（注册在OnAwake，派发不在OnAwake）：✅ / ❌（行XX）
R5  GPO→Mode 跨系统通信方式正确：✅ / N/A
R6  自定义 GPO 移除用 SM_AI.Event_RemoveAI：✅ / N/A
R7  伤害用 Event_GPOHurt（非 Event_DownHP）：✅ / N/A
R8  程序化 Entity 使用 SetGameObjectEntity：✅ / N/A
R9  所有类都有 namespace 声明（值与类型对应）：✅ / ❌（行XX）
R10 无新建/修改 .asmdef：✅ / N/A
R11 using 声明在 namespace 外部（上方）：✅ / ❌（行XX）
结论：✅ 代码合规 / ❌ 不合规，违规条目：[列出 Rn]
```

---

# 第三章：Gameplay 玩法逻辑规范

## 3.1 碰撞检测

GPO 角色碰撞体很多时候 `isTrigger = true`，不能无脑跳过：

```csharp
// ✅ 正确：先判断 GPO，GPO 不受 isTrigger 限制
var hitGPO = GetGPOFromCollider(col);
if (hitGPO != null) { /* 处理 GPO */ }
else if (!col.isTrigger) { /* 非 GPO 障碍物 */ }
```

动态 scale 时碰撞半径需同步更新：

```csharp
float currentRadius = baseRadius * iEntity.GetLocalScale().x;
Physics.OverlapSphereNonAlloc(pos, currentRadius, _colliders, layerMask);
```

## 3.2 区域检测

```csharp
// ✅ 正确：Role 和 AI 都纳入检测
var gpoType = gpo.GetGPOType();
if (gpoType != GPOData.GPOType.Role && gpoType != GPOData.GPOType.AI) continue;
// ✅ 排除 GodMode（场景装饰/区域 GPO 自身）
if (mySystem.HasTag("GodMode")) continue;
```

## 3.3 GC 优化

禁止在 Update / 定时轮询中 new 容器：

```csharp
// ✅ 预分配为字段，每次轮询复用
private readonly Dictionary<int, List<IGPO>> teamDict = new();
private void CheckArea() {
    foreach (var list in teamDict.Values) list.Clear();
    teamDict.Clear();
}
// ✅ TryGetValue 代替 ContainsKey + []
if (!teamDict.TryGetValue(teamId, out var list)) { teamDict[teamId] = list = new(); }
list.Add(gpo);
```

## 3.4 道具掉落系统选择

| 系统 | 触发条件 | 使用场景 |
|------|---------|---------|
| `ServerGPODropItem` 组件 | 死亡/HP百分比 | 标准 AI 击杀掉落 |
| `SM_Item.Event_DropItem` | **任意自定义时机** | 关卡完成、争夺胜利等 |

## 3.5 Unity GameObject 销毁

`visualObj = null` 只是清空引用，不销毁 GameObject。必须先 `Object.Destroy(visualObj)` 再置 null。

MonoBehaviour 必须在 `OnDestroy` 中注销 `MsgRegister` 监听，否则销毁后仍会收到事件导致 NullRef。

## 3.6 载具/坐骑

`Event_DrivingVehicle` 中 `DriveGPO` 必须是真实的载具 GPO 引用（不可为 null）。
载具被摧毁时，必须先派发 `IsDriving=false`，再派发 `Event_OnSetDead`。

## 3.7 游戏模式 ID 管理

测试专用模式必须使用 **10001–19999 区间**，避免与生产 ModeSet ID 冲突。
新测试模式必须同步在 `AiLevel`、`AiBehaviourTreeLevel` 等模板数据中补充对应行。

---

# 第四章：网络与 RPC 规范

## 4.1 Transform 同步规范

Scale 必须由服务端驱动，客户端单独改 scale 只改视觉不改碰撞体。

`S_GPO_Base` 已注册 `ServerNetworkTransform`，`C_GPO_Base` 已注册 `ClientNetworkTransform`，**不需要在子 System 中重复添加。**

## 4.2 客户端 RPC 反序列化注册规范

新增 Proto 模块**必须**在 `ClientNetworkSerialize.UnSerializeBuffer()` 的 switch 中注册，否则 RPC 消息静默失败，日志出现：

```
[Client] RPC 没有注册对应的反序列化: XX
```

```csharp
case Proto_ResourceContest.ModID:
    protoDoc = Proto_ResourceContest.ReadRpcBuffer(funcId);
    break;
```

**新建 GPO 功能模块的完整 Checklist：**
1. 创建 `Proto_XXX.cs`（分配唯一 `ModID`）
2. 在 `UnSerializeBuffer()` 添加 `case Proto_XXX.ModID`
3. 在客户端 Component 的 `OnSetNetwork()` 中 `AddProtoCallBack(Proto_XXX.Func.ID, handler)`

## 4.3 玩家中途加入的状态同步（SyncList）

继承 `ServerNetworkComponentBase` 并覆写 `SyncList()` 以支持登录同步：

```csharp
public class ServerXXX_Progress : ServerNetworkComponentBase {
    protected override List<ITargetRpc> SyncList() {
        if (isCompleted) return null;  // null = 不需要同步
        return new List<ITargetRpc> {
            new Proto_XXX.TargetRpc_Start { ... },
            new Proto_XXX.TargetRpc_Progress { ... },
        };
    }
}
```

`ComponentBase` 子类**没有** `SyncList`，不支持登录同步。

---

# 第五章：架构级约束

> 适用范围：所有编码 Agent（DL/ GPO / Ability）。

## 5.1 不修改 Base 类

以下代码**禁止修改**：

```
SystemBase / ComponentBase / NetworkBase / EventBase / GamePlayBase
```

AI 只能：继承、使用、调用。禁止：修改源码、改变函数行为。

## 5.2 不生成新的父类

**禁止生成**：
- `XXXBase` / `XXXFramework` / `XXXCore`
- `C_GPO_XXXXX`（作为父类）
- `C_Ability_XXXX`（作为父类）
- `S_GPO_XXXXX`（作为父类）
- `S_Ability_XXXXX`（作为父类）

示例：
- ❌ `WeaponSystemBase`、`SkillFramework`、`DamageCore`
- ✅ `WeaponSystem`、`WeaponComponent`、`WeaponEvent`

## 5.3 只能在协议层做功能开发

允许开发的层：`System` / `Component` / `Event` / `Network 协议层`  
禁止：新增新的架构体系 / 新增新的框架层

## 5.4 关键文件地址速查

| 目录 | 路径 |
|------|------|
| 事件系统目录 | `Assets/Scripts/Message/GamePlay` |
| 网络协议目录 | `Assets/Scripts/Message/Network` |
| 模版数据目录 | `Assets/Scripts/Template/` |

