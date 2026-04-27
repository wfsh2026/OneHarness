# UI 系统内容边界定义

> **版本**：v1.0  
> **适用对象**：AI 会话（UGC/PGC UI 开发、界面调整）、开发者参考  
> **定位**：本文档定义通过 AI 聊天创建/修改 UI 界面、HUD、弹窗、加载页与全局 UI Feature 时，AI 可操作的内容范围、配置边界与合法性验证规则。  
> **使用对象**：负责处理 UI/界面/弹窗/HUD/红点/公告相关请求的 AI Agent。玩家不直接阅读本文档。  
> **数据库**：`G:\BiuBiuBiu2-MiniGame\Assets\Scripts`  
> **命名空间**：`Sofunny.BiuBiuBiu2.View` / `Sofunny.BiuBiuBiu2.UI` / `Sofunny.BiuBiuBiu2.ClientMessage` / `Sofunny.BiuBiuBiu2.UIMessage`

---

## 目录

1. [总则](#1-总则)
2. [UI 能力模板库](#2-ui-能力模板库)
3. [参数与配置规范](#3-参数与配置规范)
4. [UI 预设包](#4-ui-预设包)
5. [AI 意图识别增强规则](#5-ai-意图识别增强规则)
6. [意图理解规范](#6-意图理解规范)
7. [AI 处理流程](#7-ai-处理流程)
8. [代码模板](#8-代码模板)
9. [通用组件 vs 定制组件](#9-通用组件-vs-定制组件)
10. [开发规范](#10-开发规范)
11. [已决策项归档](#11-已决策项归档)
12. [待确认项](#12-待确认项)

---

## 1. 总则

### 1.1 AI 可以做什么

| 操作类型 | 说明 | 示例 | 需修改的文件 |
|---------|------|------|------------|
| **新建 UIView** | 基于现有 `UIViewBase` 体系创建新界面 | “加一个大厅活动页” | `UI\UIView\Feature\XxxView.cs` + `UIViewManager_Layer.cs` + `UIViewManager_LifeCycle.cs` |
| **配置层级/生命周期** | 把已有 UI 接入正确层级与阶段 | “把奖励弹窗提到二级提示层，并只在结算时显示” | `UIViewManager_Layer.cs` / `UIViewManager_LifeCycle.cs` |
| **新建 RegisterFeature** | 创建全局持续监听模块，处理红点、公告、重连、弹窗转发等 | “游戏启动后持续监听一个活动入口” | `UI\UIView\RegisterFeature\XxxRegisterView.cs` + `UIViewManager_RegisterFeature.cs` |
| **接入消息驱动 UI** | 通过 `CM_UI` / `UIM_UI` 或业务消息打开/关闭/刷新界面 | “收到奖励消息时弹出展示页” | View/Feature 文件中的消息注册与派发逻辑 |
| **微调已有 UI 行为** | 调整全屏、返回逻辑、打开关闭时机、同层展示顺序 | “设置页打开时隐藏下层大厅界面” | 优先改具体 View 或配置；必要时改层级/生命周期映射 |
| **灰盒 UI 搭建** | 在缺少正式美术资源时，用 UGUI 默认组件先把结构和交互跑通 | “先用占位图搭一个活动页，资源后补” | UGUI 预制结构 + `Image` / `UISprite` 占位 + 对应 View/Control 代码 |

**唯一限制**：不修改 UI 框架底层与启动主流程，除非用户明确要求且已有充分上下文。默认禁止直接改动：

- `Assets\Scripts\UI\UIView\UIViewManager.cs`
- `Assets\Scripts\UI\UIView\UIViewManager_Static.cs`
- `Assets\Scripts\UI\UIView\UIViewManager_LoginGame.cs`
- `Assets\Scripts\UI\UIView\UIViewBase.cs`
- `Assets\Scripts\UI\UIView\UIRoot.cs`

**工程上已支持的通用能力（可直接复用）**：

| 能力 | 工程机制 | 关键类/消息 |
|------|---------|-----------|
| UI 打开/关闭 | 静态入口 + 异步资源加载 | `UIViewManager.OpenUI<T>()` / `CloseUI<T>()` |
| 全屏遮挡处理 | 打开全屏 UI 时自动隐藏下层 | `UIViewBase.FullScreenUI()` + `UIViewManager.HideOtherUI()` |
| 层级排序 | 层级基准值 + 同层按打开顺序递增 | `UIViewManager_Layer.cs` |
| 生命周期切换 | Room / Battle / WarEnd / Login 自动关闭不匹配 UI | `UIViewManager.SetCurrentLifeCycle()` |
| 全局常驻监听 | Feature 在 Init 时注册，在 Clear 时清理 | `InitRegisterFeature` + `UIViewManager_RegisterFeature.cs` |
| UI 打开/关闭埋点 | 派发 UI 世界消息 | `UIM_UI.OpenUIView` / `UIM_UI.CloseUIView` |
| 通用提示 | 对话框 / Toast / 公告 | `CM_UI.ShowDialog` / `CM_UI.ShowToast` |
| 无资源灰盒 UI | 通用 UGUI 结构 + 默认占位图 | `Image` / 通用 `UISprite` / 纯色背景 / 文本占位 |

### 1.2 UI 系统职责

UI 系统是**纯客户端系统**，负责：

- 大厅、战斗、结算、登录、加载等界面的组织与切换
- UI 层级（Scene / Control / UI / UITip1 / UITip2 / Loading / SystemTip）管理
- 生命周期（All / Room / Battle / WarEnd / Login）管理
- 弹窗、提示、奖励展示、公告、重连、红点等全局 UI Feature

它与以下系统协作：

- **模式系统**：决定房间、战斗、结算阶段的 UI 生命周期切换
- **3C / 镜头系统**：战斗控制 HUD、准星、操作布局等界面依赖角色与视角状态
- **消息系统**：绝大多数 UI 打开/关闭/刷新通过 `MsgRegister` 驱动
- **资源系统**：UI 预制体由 `AssetManager.LoadUI()` / `LoadUIRoot()` 异步加载

### 1.3 UI 结构分层

```
UI 系统
├── UI/UIView/UIViewManager*.cs        ← UI 管理器（层级、生命周期、Feature 注册、登录流）
├── UI/UIView/UIViewBase.cs            ← UIView 基类
├── UI/UIView/UIRoot.cs                ← UI 根节点层级容器
├── UI/UIView/Feature/                 ← 具体界面 View
├── UI/UIView/RegisterFeature/         ← 全局常驻监听 Feature
├── UI/UIControl/                      ← 具体控件与页面实现
├── Message/GamePlay/Client/World/CM_UI.cs
└── Message/UI/World/UIM_UI.cs
```

> ⚠️ 重点：当前 UI 体系以 `UIViewManager` 为统一入口。AI 不得自行引入新的 UI 管理器、生命周期管理器或并列的根节点架构。
>  
> 当正式美术资源缺失时，AI 应优先交付**可运行的灰盒 UI**，而不是停止在“等待资源”阶段。

### 1.4 关键代码目录

| 层级 | 路径 |
|------|------|
| UI 管理入口 | `Assets\Scripts\UI\UIView\UIViewManager.cs` |
| 静态接口 | `Assets\Scripts\UI\UIView\UIViewManager_Static.cs` |
| 层级配置 | `Assets\Scripts\UI\UIView\UIViewManager_Layer.cs` |
| 生命周期配置 | `Assets\Scripts\UI\UIView\UIViewManager_LifeCycle.cs` |
| Feature 注册配置 | `Assets\Scripts\UI\UIView\UIViewManager_RegisterFeature.cs` |
| 登录 UI 流程 | `Assets\Scripts\UI\UIView\UIViewManager_LoginGame.cs` |
| View 基类 | `Assets\Scripts\UI\UIView\UIViewBase.cs` |
| UI 根节点 | `Assets\Scripts\UI\UIView\UIRoot.cs` |
| 具体界面 | `Assets\Scripts\UI\UIView\Feature\` |
| 全局监听 Feature | `Assets\Scripts\UI\UIView\RegisterFeature\` |
| 具体控件实现 | `Assets\Scripts\UI\UIControl\` |
| Client UI 世界消息 | `Assets\Scripts\Message\GamePlay\Client\World\CM_UI.cs` |
| UI 世界消息 | `Assets\Scripts\Message\UI\World\UIM_UI.cs` |

---

## 2. UI 能力模板库

### 2.1 模板分类体系

#### 🔵 A 类：通用接入（无需改底层框架）

| 模板 | 能力 | 典型场景 | 必改文件 |
|------|------|---------|---------|
| U01 | 新建大厅页 | 大厅入口页、背包页、活动页、排行榜页 | `Feature\XxxView.cs` + Layer/LifeCycle 配置 |
| U02 | 新建战斗 HUD | 战斗提示、模式进度、准星附属界面 | `Feature\XxxView.cs` + Battle 生命周期配置 |
| U03 | 新建一层弹窗 | 详情页、二次确认页、装备/奖励预览 | `Feature\XxxView.cs` + `UITip1` |
| U04 | 新建二层提示 | 奖励展示、升级解锁、功能解锁 | `Feature\XxxView.cs` + `UITip2` |
| U05 | 新建系统提示 | Toast、公告、小浮层提示 | `Feature\XxxView.cs` + `SystemTip` |

#### 🟡 B 类：Feature 组合（无需新架构）

| 模板 | 组合方式 | 场景 |
|------|---------|------|
| U06 | `InitRegisterFeature` + 业务消息监听 | 红点、公告、活动入口、重连提示 |
| U07 | `CM_UI.ShowDialog` / `ShowToast` | 通用确认框、文本提示 |
| U08 | `UIM_UI.OpenUIView` / `CloseUIView` | 统计、埋点、弹窗队列联动 |
| U09 | 生命周期切换 + Mode UI | 房间 → 战斗 → 结算整套界面联动 |

#### 🔴 C 类：特化开发（默认需先确认）

| 需求 | 原因 |
|------|------|
| 新增 `UIRootLayer` 枚举层级 | 会影响所有 UI 排序与根节点映射 |
| 新增 `UILifeCycle` 枚举阶段 | 会影响全局切换逻辑与大量已有 UI 配置 |
| 改写 `UIViewManager` 打开/关闭机制 | 属于框架层，风险高 |
| 改写登录 UI 主流程 | 与平台、网络、场景切换强耦合 |

---

## 3. 参数与配置规范

### 3.1 层级规范（`UIViewManager.UIRootLayer`）

| 层级 | 枚举值 | 基础 SortOrder | 用途 | 说明 |
|------|-------|---------------|------|------|
| `Scene` | 0 | 100 | 场景表现、战斗场景叠层 | 如血迹、模式 HUD 背景 |
| `Control` | 1 | 300 | 操作层 | 摇杆、按钮、玩家控制 |
| `UI` | 2 | 600 | 主界面层 | 大厅、背包、商店等 |
| `UITip1` | 3 | 800 | 第一层弹窗 | 详情、选择、确认 |
| `UITip2` | 4 | 1000 | 第二层提示 | 奖励、升级、解锁 |
| `Loading` | 5 | 1200 | 加载层 | 过场、切场景 |
| `SystemTip` | 6 | 1500 | 系统提示层 | 公告、Toast、系统提示 |

补充规则：

- `UI` / `UITip1` / `UITip2` 都挂到 `UIRoot.UILayer`，通过 `SortOrder` 区分上下层。
- 同一层内后打开的 UI 默认排在更上方。
- 不允许为了“临时压住别的 UI”随意上提到 `SystemTip`；优先使用正确的层级和打开顺序。

### 3.2 生命周期规范（`UIViewManager.UILifeCycle`）

| 生命周期 | 枚举值 | 适用场景 | 说明 |
|---------|-------|---------|------|
| `All` | 0 | 全阶段常驻 | 不会因阶段切换自动关闭 |
| `Room` | 1 | 大厅 / 房间 | 大部分功能页和入口页 |
| `Battle` | 2 | 战斗中 | HUD、模式 UI、控制 UI |
| `WarEnd` | 3 | 结算 | 奖励、排行、结算展示 |
| `Login` | 4 | 登录 | 登录、合规、启动账号流程 |

补充规则：

- 一个 UI 可以配置到多个生命周期。
- 生命周期切换时，系统会关闭不属于新阶段的 UI。
- 需要常驻显示时才放到 `All`，不要滥用。

### 3.3 `UIViewBase` 关键行为边界

| 能力 | 默认值/现状 | 可操作边界 | 说明 |
|------|------------|-----------|------|
| `ViewType` | `None / Room / Battle / Login` | 只能复用现有枚举 | 影响按类型关闭等逻辑 |
| `isFullScreenUI` | 默认 `false` | 可在构造时调用 `FullScreenUI()` 开启 | 全屏 UI 会隐藏下层非 Battle 界面 |
| `OnInit()` | 仅一次 | 可注册消息、初始化状态 | 不建议放重型异步 |
| `OnLoadUICompleted(UIBase ui)` | 资源加载完成后 | 可做 UI 初始化后的首帧处理 | 适合拿到具体 `UIBase` 后绑定逻辑 |
| `OnClose()` | 每次关闭 | 必须做反注册和释放引用 | 避免内存泄漏 |

### 3.4 消息接入边界

| 消息 | 类型 | 用途 | 备注 |
|------|------|------|------|
| `CM_UI.ShowDialog` | Client World Event | 通用确认弹窗 | 面向业务侧调用 |
| `CM_UI.ShowToast` | Client World Event | 文本提示 | 轻提示 |
| `CM_UI.PlayHudVFX` | Client World Event | HUD 特效 | 战斗提示特效 |
| `UIM_UI.OpenUIView` | UI World Event | UI 打开广播 | 常用于埋点/统计/队列 |
| `UIM_UI.CloseUIView` | UI World Event | UI 关闭广播 | 常用于弹窗队列清理 |
| `UIM_UI.IsFullScreenUI` | UI World Event | 全屏状态广播 | Feature 可监听 |

规则：

- 优先复用现有 `CM_UI` / `UIM_UI`，不要为普通 UI 开关滥造新消息类型。
- 若是某个业务系统专属 UI 刷新，优先监听该业务已有消息，而不是把所有逻辑塞进 `CM_UI`。

### 3.5 灰盒资源与默认图片规范

当用户没有提供正式美术资源时，AI 默认采用以下策略：

| 主题 | 默认策略 | 说明 |
|------|---------|------|
| 图片组件 | 优先通用 `UISprite`，否则使用 UGUI `Image` | 以工程现有通用控件优先 |
| 背景 | 纯色底图 / 半透明遮罩 / 简单九宫格 | 保证层次和可点击区域清晰 |
| 图标 | 默认 Sprite / 占位框 / 文本标签 | 先表达信息结构，不追求最终视觉 |
| 按钮 | 标准 `Button + Image + Text` 组合 | 保证交互可跑通 |
| 列表项 | 重复结构 + 占位图标 + 文本 | 优先验证信息密度和布局节奏 |

灰盒 UI 的交付要求：

1. **结构先行**：先保证层级、布局、点击区域、显示/关闭流程正确。
2. **交互可验收**：按钮、返回、弹窗遮罩、列表滚动等关键行为必须可用。
3. **视觉可替换**：占位图和底图应易于后续替换正式资源，不写死复杂临时逻辑。
4. **不要把缺少资源当成阻塞**：除非用户明确要求“必须等正式资源后再做”。

### 3.6 灰盒 UI 的合法行为边界

- 可以：创建临时 `Image`、纯色背景、文字占位、默认图标占位、基础九宫格底板。
- 可以：按页面信息结构组织节点层级，类似场景系统中的灰盒搭建。
- 不可以：为了“看起来更像成品”而引入新的底层 UI 框架或私造通用资源体系。
- 不可以：把占位资源和正式资源强耦合到复杂脚本中，导致后续替换困难。

---

## 4. UI 预设包

### 4.1 预设包一览

| 预设码 | 名称 | 核心机制 | 适用场景 |
|--------|------|---------|---------|
| **UI01** | 大厅主页面 | `UI` 层 + `Room` 生命周期 | 大厅、商店、背包、排行榜 |
| **UI02** | 战斗 HUD | `Scene/Control` 层 + `Battle` 生命周期 | 血条、准星、技能提示、模式进度 |
| **UI03** | 一层弹窗 | `UITip1` + 可选全屏 | 详情、确认、选择 |
| **UI04** | 二层奖励展示 | `UITip2` + 全屏/半屏 | 升级、解锁、奖励展示 |
| **UI05** | 系统提示 | `SystemTip` + `All/Room/Battle` | Toast、公告、连接提示 |
| **UI06** | 全局入口 Feature | `RegisterFeature` + 业务消息 | 红点、活动入口、重连 |
| **UI07** | 灰盒页面 | 通用 `Image` / `UISprite` + 文本占位 + 基础按钮 | 缺少正式资源时快速搭界面 |

### 4.2 互斥与组合规则

| 组合 | 关系 | 说明 |
|------|------|------|
| UI01 + UI03 | ✅ 可组合 | 页面上叠一层详情/确认弹窗 |
| UI03 + UI04 | ✅ 可组合 | 二级提示压在一层弹窗上方 |
| UI02 + 全屏 UI01 | ⚠️ 谨慎 | 战斗中打开大厅型全屏页通常不合理 |
| UI05 + 任意预设 | ✅ 可组合 | 系统提示通常可叠加 |
| UI07 + UI01/UI03/UI04 | ✅ 可组合 | 先以灰盒形式验证页面结构，再替换正式资源 |
| 多个全屏 UI | ⚠️ 谨慎 | 依赖现有全屏遮挡逻辑，需确认返回栈体验 |

---

## 5. AI 意图识别增强规则

### 5.1 关键词到能力映射

| 用户关键词 | 识别为 | 说明 |
|-----------|-------|------|
| UI、界面、页面、面板、按钮、布局 | 新建/修改 UIView | 优先判断是页面还是控件 |
| 占位图、默认图、先搭结构、没美术、灰盒 UI | 灰盒 UI 搭建 | 默认允许 AI 用 UGUI 占位资源先交付 |
| 弹窗、提示框、确认框、奖励展示、解锁提示 | 弹窗 UI | 优先落到 `UITip1/UITip2` |
| HUD、准星、战斗提示、操作按钮、摇杆 | 战斗 UI | 通常是 `Scene/Control/Battle` |
| 红点、公告、重连、活动入口、常驻监听 | RegisterFeature | 倾向全局 Feature |
| Toast、公告提示、系统提示 | SystemTip/通用消息 | 优先复用 `CM_UI.ShowToast` / `ShowDialog` |
| 登录页、加载页、结算页 | 生命周期 UI | 需同时判断 `Login/Loading/WarEnd` |

### 5.2 识别补充规则

1. **先区分 View / Feature / UIControl**：  
   - 有界面载体 = `UIView`  
   - 持续监听、可能不开界面 = `RegisterFeature`  
   - 单个组件细节 = `UIControl`
2. **带“战斗操作 / 视角 / HUD”字样时**，通常同时涉及 UI + 3C/镜头。
3. **带“结算 / 奖励 / 模式结果”字样时**，通常同时涉及 UI + 模式系统。

---

## 6. 意图理解规范

处理 UI 请求时，AI 必须先判断用户真正要改的是哪一层：

| 层级 | 问题类型 | 典型请求 |
|------|---------|---------|
| `UIView` | 需要一个新界面或页面容器 | “加一个活动中心页面” |
| `RegisterFeature` | 需要常驻监听业务消息 | “登录后一直监听活动入口状态” |
| `UIControl` | 只改某个页面里的控件实现 | “改设置页里的按钮布局” |
| 层级/生命周期配置 | 现有 UI 显示时机不对 | “结算页不要在大厅出现” |

如果一个请求同时涉及多个系统，采用以下拆解思路：

- 先由玩法系统提供数据/状态
- 再由 UI 系统消费该状态，决定打开什么界面、挂在哪个生命周期

---

## 7. AI 处理流程

```
1. 读取 system-map + 本文档
2. 判断请求属于 UIView / Feature / UIControl / 生命周期配置 哪一类
3. 查找对应现有 View、Feature、消息与生命周期配置
4. 优先复用现有层级、生命周期、消息机制
5. 如需要新增界面：
   - 新建 XxxView
   - 配置 Layer
   - 配置 LifeCycle
   - 必要时接入 RegisterFeature 或业务消息
   - 若无正式资源，先按灰盒 UGUI 方案搭预制结构与占位图
6. 仅在明确必要时修改核心管理配置文件
7. 汇报新建/修改了哪些文件，并说明 UI 在哪个层、哪个生命周期生效
```

---

## 8. 代码模板

### 8.1 新建 UIView 模板

```csharp
using Sofunny.BiuBiuBiu2.View;

public class MyShopView : UIViewBase {
    public MyShopView() {
        FullScreenUI();
        SetViewType(ViewType.Room);
    }

    protected override void OnInit() {
        // 注册消息
    }

    protected override void OnLoadUICompleted(UIBase ui) {
        // 资源加载完成后做界面初始化
    }

    protected override void OnClose() {
        // 反注册消息，释放引用
    }
}
```

### 8.2 新建 RegisterFeature 模板

```csharp
using Sofunny.BiuBiuBiu2.View;

public class MyActivityRegisterView : InitRegisterFeature {
    public void Init() {
        // 注册消息监听
    }

    public void Clear() {
        // 注销消息监听
    }
}
```

### 8.3 配置映射模板

```csharp
// UIViewManager_Layer.cs
{
    UIRootLayer.UI, new List<Type> {
        typeof(MyShopView),
    }
}

// UIViewManager_LifeCycle.cs
{
    UILifeCycle.Room, new List<Type> {
        typeof(MyShopView),
    }
}
```

---

## 9. 通用组件 vs 定制组件

| 场景 | 优先方案 | 不建议方案 |
|------|---------|-----------|
| 普通页面/弹窗 | 新建 `UIView` + 配置 Layer/LifeCycle | 改 `UIViewManager` 底层逻辑 |
| 常驻监听能力 | 新建 `RegisterFeature` | 把监听逻辑塞进随机 View |
| 页面内控件交互 | 修改对应 `UIControl` | 新建一套并列 UI 框架 |
| 通用提示 | 复用 `CM_UI.ShowDialog/ShowToast` | 为单个提示另起一套通用系统 |
| 缺少正式资源的 UI | 先做灰盒预制与占位图 | 因无图而停工或跳过结构验证 |

---

## 10. 开发规范

1. **先查已有 View/Feature 再新增**，避免重复页面与重复监听。
2. **新增 UI 必须同步配置 Layer 与 LifeCycle**，否则很容易出现“能打开但看不见”。
3. **默认不要修改核心文件**，尤其是 `UIViewManager.cs`、`UIViewManager_Static.cs`、`UIViewManager_LoginGame.cs`。
4. **消息注册与反注册必须成对出现**，避免内存泄漏和重复响应。
5. **Battle UI 和 Room UI 不要混生命周期**，除非有明确设计需求。
6. **不要滥用 `FullScreenUI()`**，只有确实需要遮挡下层时才开启。
7. **没有美术资源时默认允许灰盒交付**，优先用通用 `UISprite` 或 UGUI `Image` 搭结构。
8. **灰盒 UI 也必须遵守最终接入规则**：Layer、LifeCycle、返回逻辑、消息解绑都不能省略。

---

## 11. 已决策项归档

1. UI 系统当前以 `UIViewManager` 为唯一管理入口。
2. UI 系统是纯客户端体系，无独立 Proto 网络层。
3. `UI` / `UITip1` / `UITip2` 共用 `UIRoot.UILayer`，主要靠 `SortOrder` 区分层级。
4. `RegisterFeature` 是全局持续监听机制，适合红点、公告、重连、社交入口等常驻逻辑。
5. 生命周期当前固定为 `All / Room / Battle / WarEnd / Login`。
6. 缺少正式美术资源时，AI 可以按灰盒方式组织 UGUI 预制，用默认图和占位图先完成 UI 结构与交互。

---

## 12. 待确认项

遇到以下情况，AI 必须先向用户确认：

- 需要新增 `UIRootLayer` 或 `UILifeCycle`
- 需要修改 `UIViewManager` 底层打开/关闭逻辑
- 需要调整登录主流程或启动链路
- 一个 UI 是否应该为全屏、应该归属哪个生命周期存在歧义
- 一个需求同时涉及玩法状态、网络协议和 UI 表现，但用户没有说明以谁为准
- 用户明确要求“不要用灰盒占位，必须等待正式美术资源”
