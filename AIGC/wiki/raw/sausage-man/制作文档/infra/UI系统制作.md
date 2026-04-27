# UI 系统制作

> **适用范围**：1 代架构 `Assets/Script/UI/` + `Assets/Script/Manager/` 中窗口管理框架
> **核心路径**：`Assets/Script/Manager/Window.cs`（598 行）· `WindowManager.cs` · `Controller.cs` · `ControllerManager.cs`
> **相关文档**：[[模式制作]] · [[角色制作]] · [[武器战斗制作]] · [[镜头系统制作]]

---

## §1 架构概述

### §1.1 系统定位与职责边界

UI 系统是游戏客户端中所有 2D 界面元素的统一管理框架，位于渲染管线最上层，直接面向玩家交互。在整个游戏架构中的位置：

```
┌──────────────────────────────────────────────────────────────────┐
│                        游戏架构全局视图                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐    │
│  │  网络层      │  │   战斗逻辑层  │  │   UI 系统（本文档）   │    │
│  │  Mirror      │  │   War/       │  │   Manager/           │    │
│  │  NetworkMsg  │←→│   Mode/      │←→│   Window + Controller│    │
│  │              │  │   Ability/   │  │   HUD + Tips + Map   │    │
│  └─────────────┘  └──────┬───────┘  └──────────┬───────────┘    │
│                          │                      │                │
│                   ┌──────┴───────┐       ┌──────┴───────┐       │
│                   │   角色/载具   │       │   资源加载    │       │
│                   │   Role/Car   │       │   AssetLoad  │       │
│                   └──────────────┘       │   UIPool     │       │
│                                          └──────────────┘       │
└──────────────────────────────────────────────────────────────────┘
```

**职责边界**：

| 职责 | UI 系统负责 | UI 系统不负责 |
|------|-----------|-------------|
| 窗口管理 | 打开/关闭/排序/缓存/遮罩 | 窗口内具体业务逻辑 |
| 输入控制 | HUD 按钮/摇杆输入采集与分发 | 角色移动/技能释放的物理计算 |
| 地图系统 | 小地图/大地图渲染、标记管理 | 毒圈伤害计算（归 SafeAreaManager） |
| 提示系统 | 弹窗/面板/浮动提示的展示 | 提示内容的业务判断逻辑 |
| 屏幕适配 | 刘海屏/异形屏/iPad 适配 | 分辨率与画质设置（归 UserSettings） |

**与其他系统的数据流向**：

```
Mirror 网络消息 ──→ Controller.Open() ──→ Window.BeforeOpen() ──→ UI 展示
     ↑                                                              │
     │                   InputControlManager                        │
     │                          │                                   │
     └── 角色操作指令 ←── ButtonControl.OnUpdate() ←── 玩家触摸输入 ←─┘
```

### §1.2 目录结构

```
Assets/Script/
├── Manager/                          ← UI 核心框架
│   ├── Window.cs                     ← 窗口基类（598 行）
│   ├── WindowManager.cs              ← 窗口管理器 Singleton
│   ├── Controller.cs                 ← 窗口数据控制器基类
│   └── ControllerManager.cs          ← 控制器管理器 Singleton
│
├── Config/
│   └── WindowsConfig.cs              ← 窗口配置数据库
│
├── Asset/GameObjectPools/
│   └── UIPool.cs                     ← 窗口预制体缓存池
│
└── UI/
    ├── PlayerControl/                ← HUD 操作面板（182 文件）
    │   ├── PlayerOperateWin.cs       ← 主 HUD 窗口
    │   ├── InputControlManager.cs    ← 输入管理器 Singleton
    │   ├── ButtonControl/            ← 34 种按钮控制实现
    │   └── Movement/                 ← 5 种移动控制实现
    │
    ├── MapInfo/                      ← 地图系统（89 文件）
    │   ├── MapInfoWin.cs             ← 主地图窗口
    │   ├── MapPlayer.cs              ← 玩家标记
    │   ├── MapRoleAI.cs              ← AI 标记
    │   ├── MapItemPoint.cs           ← 物品标记
    │   ├── PoisonGraphic.cs          ← 毒圈可视化
    │   └── UIMapSpotMgr.cs           ← 兴趣点管理
    │
    ├── Elements/                     ← 增强 UGUI 组件
    │   ├── ButtonEx.cs               ← 增强按钮
    │   ├── TextEx.cs                 ← 增强文本
    │   ├── ImageEx.cs                ← 增强图片
    │   ├── RawImageEx.cs             ← 增强原始图片
    │   └── SliderEx.cs               ← 增强滑块
    │
    ├── Component/
    │   └── UIBaseBehaviour.cs        ← UI 通用生命周期基类
    │
    ├── UGUIAdapter/
    │   └── UIAdapter.cs              ← 屏幕适配（9 种定位模式）
    │
    ├── War/                          ← 战场初始化（72 文件）→ [[ui-war-init]]
    │   ├── StartGame.cs              ← 主初始化控制器
    │   ├── StartGame[ModeName].cs    ← 11 种模式变体
    │   ├── SafeAreaManager.cs        ← 毒圈管理
    │   ├── ButtleMap.cs              ← 场景主体
    │   ├── ButtleLayer.cs            ← 场景层级
    │   └── BarrageCell.cs            ← 弹幕聊天
    │
    ├── Tips/                         ← 通用提示（46 文件）
    ├── TipsWar/                      ← 战场提示（15 文件）
    ├── WarModeTips/                  ← 模式提示（28 文件）
    │
    ├── Widgets/                      ← 可复用控件（41 文件）
    │   ├── PlayerAvatar.cs           ← 玩家头像
    │   ├── ItemQuality.cs            ← 物品品质
    │   ├── Redpoint.cs               ← 红点提示
    │   └── Scroller.cs               ← 虚拟滚动列表
    │
    ├── UserSettings/                 ← 设置系统（旧）
    ├── NewUserSetting/               ← 设置系统（新，共 64 文件）
    │
    ├── OBTools/                      ← OB 观战工具（20 文件）
    ├── DevTool/                      ← 开发工具
    ├── TestTool/                     ← 测试工具
    └── AutomationTool/               ← 自动化工具（共 121 文件）
```

### §1.3 窗口管理框架

窗口管理是 UI 系统的核心，采用 **Controller → Window** 双层分离架构：Controller 持有数据和业务逻辑，Window 负责视图展示和生命周期管理。

```
┌─────────────────────────────────────────────────────────────────┐
│                    窗口管理框架核心架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────┐              │
│  │ ControllerManager│        │  WindowManager    │              │
│  │    (Singleton)   │        │   (Singleton)     │              │
│  │                  │        │                   │              │
│  │  Open<T>()  ─────┼───→    │  Open(controller) │              │
│  │  Close<T>() ─────┼───→    │  Close(name)      │              │
│  │  Get<T>()        │        │  Show/Hide        │              │
│  │                  │        │  PreLoad          │              │
│  └────────┬─────────┘        └────────┬──────────┘              │
│           │ 管理                       │ 管理                    │
│    ┌──────┴──────┐             ┌───────┴───────┐               │
│    │  Controller  │ ──关联──→  │    Window      │               │
│    │  (数据+逻辑) │             │  (视图+生命期) │               │
│    │              │             │               │               │
│    │ FunctionName │             │ WindowType    │               │
│    │ IsOpen       │             │ SortOrder     │               │
│    │ Window ref   │             │ IsShow/IsOpen │               │
│    │ PreLoad()    │             │ Canvas        │               │
│    │ Open()       │             │               │               │
│    │ Close()      │             │               │               │
│    └──────────────┘             └───────────────┘               │
│                                        │                        │
│                                 ┌──────┴──────┐                │
│                                 │ WindowsConfig│                │
│                                 │ (配置数据库)  │                │
│                                 └──────┬──────┘                │
│                                        │                        │
│                                 ┌──────┴──────┐                │
│                                 │   UIPool     │                │
│                                 │ (预制体缓存) │                │
│                                 └─────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

**核心类职责**：

| 类名 | 路径 | 职责 |
|------|------|------|
| `Window` | `Assets/Script/Manager/Window.cs`（598 行） | 所有 UI 窗口的基类，管理 Canvas、排序层级、生命周期回调 |
| `WindowManager` | `Assets/Script/Manager/WindowManager.cs` | Singleton，负责窗口的打开/关闭/显示/隐藏/预加载，管理摄像机模式和高斯模糊遮罩 |
| `Controller` | `Assets/Script/Manager/Controller.cs` | 窗口数据控制器基类，持有业务数据，驱动 Window 的打开/关闭 |
| `ControllerManager` | `Assets/Script/Manager/ControllerManager.cs` | Singleton，通过泛型 API 管理所有 Controller 实例 |
| `WindowsConfig` | `Assets/Script/Config/WindowsConfig.cs` | 窗口配置数据库，定义窗口名称→预制体路径→WindowType 的映射 |
| `UIPool` | `Assets/Script/Asset/GameObjectPools/UIPool.cs` | 窗口预制体对象池，缓存已加载的 UI 预制体，避免重复实例化 |

**两套 API 入口**：

```csharp
// 泛型方式（推荐，编译期类型安全）
ControllerManager.Instance.Open<LobbyController>();
ControllerManager.Instance.Close<LobbyController>();
var ctrl = ControllerManager.Instance.Get<LobbyController>();

// 字符串方式（动态场景，如配置驱动）
ControllerManager.Instance.Open("LobbyController");
ControllerManager.Instance.Close("LobbyController");
```

### §1.4 窗口类型与排序层级

Window 定义了 7 种 `WindowType`，通过 `sortOrder` 控制 Canvas 的渲染层级，确保弹窗、提示、系统弹框等按正确顺序叠加。

```
渲染层级（从底到顶）：

sortOrder
  │
  │  13000+  ┌─────────────────────┐
  │          │     OverLay          │  ← 最顶层覆盖（Loading/转场）
  │  11000+  ├─────────────────────┤
  │          │     MaxMap           │  ← 全屏地图
  │  9000+   ├─────────────────────┤
  │          │     System           │  ← 系统弹窗（断线/维护）
  │  7000+   ├─────────────────────┤
  │          │     Tip              │  ← 提示层（Toast/飘字）
  │  5000+   ├─────────────────────┤
  │          │     Modal            │  ← 模态弹窗（确认框/奖励）
  │  3000+   ├─────────────────────┤
  │          │     Normal           │  ← 普通窗口（功能面板）
  │  1000    ├─────────────────────┤
  │          │     Base             │  ← 基础层（大厅主界面）
  │    0     └─────────────────────┘
  ▼
```

**详细层级规则**：

| WindowType | 基础 sortOrder | 动态计算规则 | 典型用途 |
|-----------|---------------|-------------|---------|
| `Base` | 1000 | 固定值 | 大厅主界面、战场 HUD 底板 |
| `Normal` | 3000 + N×100 | N = 当前 Normal 窗口栈深度 | 商城/背包/好友列表等功能面板 |
| `Modal` | 5000 + N×100 | N = 当前 Modal 窗口栈深度 | 确认弹窗/二次确认/奖励展示 |
| `Tip` | 7000 + N×100 | N = 当前 Tip 窗口栈深度 | Toast 提示/飘字/临时信息 |
| `System` | 9000 | 固定值 | 网络断线/服务器维护/强制更新 |
| `MaxMap` | 11000 | 固定值 | 全屏大地图覆盖层 |
| `OverLay` | 13000 | 固定值 | Loading 界面/场景转场遮罩 |

> **动态层级说明**：Normal/Modal/Tip 类型的窗口通过栈深度 N 自动递增 sortOrder（每层 +100），确保后打开的窗口始终在先打开的窗口之上。关闭窗口时自动回收层级编号。

### §1.5 窗口生命周期

Window 提供完整的生命周期回调链，开发者可在每个节点插入自定义逻辑：

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Window 完整生命周期                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Controller.PreLoad()                                                │
│       │                                                              │
│       ▼                                                              │
│  ╔═══════════════╗    WindowManager 从 UIPool 获取预制体              │
│  ║  Instantiate   ║    实例化 → 获取 Window 组件 → 设置 Canvas        │
│  ╚═══════╤═══════╝                                                   │
│          │                                                           │
│          ▼                                                           │
│  ┌───────────────┐    → OnCreateWindowEvent 触发                     │
│  │  BeforeOpen    │    UI 初始化：绑定数据、设置初始状态               │
│  └───────┬───────┘                                                   │
│          │                                                           │
│          ▼                                                           │
│  ┌───────────────┐    → OnBeforeOpenEvent 触发                       │
│  │    Active      │    Canvas.enabled = true，开始接收输入            │
│  └───────┬───────┘    → OnActivatedEvent 触发                        │
│          │                                                           │
│          ▼                                                           │
│  ┌───────────────┐    → OnAfterOpenEvent 触发                        │
│  │   AfterOpen    │    开场动画播放、引导触发                         │
│  └───────┬───────┘                                                   │
│          │                                                           │
│          ▼                                                           │
│  ╔═══════════════╗    IsShow=true, IsOpen=true, IsOpened=true        │
│  ║  Open (运行中) ║    正常交互，接收 OnUpdate 帧更新                  │
│  ╚═══════╤═══════╝                                                   │
│          │                                                           │
│          ▼  （调用 Close）                                            │
│  ┌───────────────┐    → OnBeforeCloseEvent 触发                      │
│  │  BeforeClose   │    保存数据、停止动画                              │
│  └───────┬───────┘                                                   │
│          │                                                           │
│          ▼                                                           │
│  ┌───────────────┐    → OnAfterCloseEvent 触发                       │
│  │  AfterClose    │    Canvas.enabled = false，回收到 UIPool          │
│  └───────┬───────┘                                                   │
│          │                                                           │
│          ▼                                                           │
│  ┌───────────────┐    GameObject.Destroy() 或 回池缓存               │
│  │   Destroy      │    释放引用，清理事件监听                          │
│  └───────────────┘                                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**关键状态属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `IsShow` | bool | 窗口是否可见（Canvas.enabled） |
| `IsOpen` | bool | 窗口是否处于打开流程中（BeforeOpen → AfterClose 之间） |
| `IsOpened` | bool | 窗口是否已完成打开（AfterOpen 之后） |
| `IsBattleUI` | bool | 是否为战场 UI（战场结束时统一关闭） |
| `IsKeepOnlyMove` | bool | 打开时是否只保留移动输入（禁止射击等） |
| `IsForceHide` | bool | 是否被强制隐藏（截图/录屏时） |

**WindowManager 事件总线**：

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `OnCreateWindowEvent` | Window 实例化完成 | 统计/日志 |
| `OnBeforeOpenEvent` | BeforeOpen 回调前 | 预处理、高斯模糊遮罩开启 |
| `OnActivatedEvent` | Active 回调后 | 焦点管理、输入路由切换 |
| `OnAfterOpenEvent` | AfterOpen 回调后 | 引导系统检查 |
| `OnBeforeCloseEvent` | BeforeClose 回调前 | 数据保存 |
| `OnAfterCloseEvent` | AfterClose 回调后 | 高斯模糊遮罩关闭、焦点恢复 |

**摄像机模式**（WindowManager 管理）：

| 模式 | 说明 |
|------|------|
| `Lobby` | 大厅主界面，3D 背景 + 2D UI 叠加 |
| `War` | 战场内，UI 覆盖在战场摄像机之上 |
| `Timeline` | 过场动画模式，UI 最小化或隐藏 |
| `Lobby3DRoom` | 大厅 3D 展厅，角色展示 + UI 面板 |

### §1.6 HUD 操作面板架构

HUD 操作面板是战场内最核心的 UI 模块（`Assets/Script/UI/PlayerControl/`，182 文件），负责玩家在战场中的所有操作输入，包括移动、射击、换弹、技能、物品使用等。

```
┌────────────────────────────────────────────────────────────────┐
│                    HUD 操作面板架构                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────┐                              │
│  │    PlayerOperateWin          │  ← 主 HUD 窗口（Window 子类） │
│  │    (WindowType.Base)         │                              │
│  └──────────────┬───────────────┘                              │
│                 │ 持有                                          │
│  ┌──────────────┴───────────────┐                              │
│  │   InputControlManager        │  ← 输入管理器 Singleton       │
│  │                              │                              │
│  │   OnUpdate()                 │  ← 每帧调用                   │
│  │     ├── UpdateControlStyle() │  ← 根据状态选择 ButtonControl │
│  │     ├── UpdateControlState() │  ← 更新按钮可见性/可用性      │
│  │     └── control.OnUpdate()   │  ← 委托给具体控制器处理       │
│  └──────────────┬───────────────┘                              │
│                 │ 持有当前活跃的                                 │
│  ┌──────────────┴───────────────┐                              │
│  │  IButtonControl（34 种实现）  │                              │
│  │  + IMove（5 种实现）          │                              │
│  └──────────────────────────────┘                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**输入处理主循环**：

```
每帧 InputControlManager.OnUpdate()
  │
  ├─ 1. UpdateControlStyle()
  │     └─ 根据当前角色状态（步行/载具/观战/OB/编辑器）
  │        选择对应的 IButtonControl 实现
  │
  ├─ 2. UpdateControlState()
  │     └─ 根据游戏状态更新各按钮的：
  │        · 可见性（是否显示）
  │        · 可用性（是否可交互）
  │        · 图标/文本（如换弹进度、技能 CD）
  │
  └─ 3. currentControl.OnUpdate()
        └─ 具体控制器处理输入事件：
           · 摇杆移动 → IMove.OnMove()
           · 按钮点击 → 对应操作回调
           · 长按/双击 → 特殊操作
```

### §1.7 输入控制继承体系

#### 按钮控制继承树

```
IButtonControl（接口）
  │
  └── AbsButtonControl（抽象基类）
        │
        ├── CommonButtonControl          ← 通用默认控制
        ├── StateButtonControl           ← 状态切换控制
        ├── MoveButtonControl            ← 纯移动控制
        │
        ├── RoleMoveButtonControl        ← 角色移动专用
        ├── RoleStateButtonControl       ← 角色状态专用
        ├── BattleStateButtonControl     ← 战斗状态专用
        │
        ├── VehicleMoveButtonControl     ← 载具移动（通用）
        ├── AircraftMoveButtonControl    ← 飞行载具移动
        │
        ├── ObserveButtonControl         ← 观战模式
        ├── OBButtonControl              ← OB 控制台
        ├── EditorButtonControl          ← 编辑器模式
        ├── PackButtonControl            ← 背包操作
        │
        └── ... 其余 22 种专用控制器
```

#### 移动控制继承树

```
IMove（接口）
  │
  └── AbsMovement（抽象基类）
        │
        ├── CommonMovement              ← 标准摇杆移动
        ├── OBMovement                  ← OB 自由移动
        ├── RollMovement                ← 翻滚闪避移动
        ├── SneakSandMovement           ← 潜行/沙地移动
        └── （其他模式特定移动）
```

**控制器切换规则**：

| 游戏状态 | ButtonControl | Move |
|---------|--------------|------|
| 步行战斗 | `BattleStateButtonControl` | `CommonMovement` |
| 载具驾驶 | `VehicleMoveButtonControl` | `CommonMovement` |
| 飞行载具 | `AircraftMoveButtonControl` | `CommonMovement` |
| 观战 | `ObserveButtonControl` | `OBMovement` |
| OB 控制 | `OBButtonControl` | `OBMovement` |
| 编辑器 | `EditorButtonControl` | `CommonMovement` |
| 背包界面 | `PackButtonControl` | 无移动 |
| 翻滚状态 | 当前控制器不变 | `RollMovement`（临时切换） |

### §1.8 地图系统

地图系统（`Assets/Script/UI/MapInfo/`，89 文件）提供小地图和大地图两种显示模式，管理地图上的所有动态标记。

```
┌──────────────────────────────────────────────────────────┐
│                    地图系统架构                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐                                        │
│  │  MapInfoWin   │  ← 主地图窗口                         │
│  │  小地图 ←→ 大地图 切换                                 │
│  └──────┬───────┘                                        │
│         │ 管理                                            │
│  ┌──────┴───────────────────────────────┐                │
│  │           标记管理层                   │                │
│  │                                       │                │
│  │  ┌────────────┐  ┌────────────┐      │                │
│  │  │ MapPlayer   │  │ MapRoleAI  │      │  ← 动态标记    │
│  │  │ (玩家位置)  │  │ (AI 位置)  │      │                │
│  │  └────────────┘  └────────────┘      │                │
│  │                                       │                │
│  │  ┌──────────────┐  ┌──────────────┐  │                │
│  │  │ MapItemPoint  │  │ UIMapSpotMgr │  │  ← 静态/POI   │
│  │  │ (物品标记)    │  │ (兴趣点管理) │  │                │
│  │  └──────────────┘  └──────────────┘  │                │
│  └──────────────────────────────────────┘                │
│         │                                                │
│  ┌──────┴───────┐                                        │
│  │ PoisonGraphic │  ← 毒圈可视化                         │
│  │ (圆环渲染)    │     与 SafeAreaManager 数据联动        │
│  └──────────────┘                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**地图标记类型**：

| 标记类 | 用途 | 数据来源 |
|-------|------|---------|
| `MapPlayer` | 显示队友/敌人位置 | Role 网络同步位置 |
| `MapRoleAI` | 显示 AI 单位位置 | AI System 网络同步 |
| `MapItemPoint` | 显示地面物品/空投 | Item 网络同步 |
| `UIMapSpotMgr` | 管理兴趣点标记 | 场景静态数据 + 动态事件 |
| `PoisonGraphic` | 毒圈边界可视化 | SafeAreaManager 半径/圆心 |

### §1.9 基础组件层

#### 增强 UGUI 组件（Elements/）

项目对 Unity 原生 UGUI 组件进行了统一增强封装：

| 组件 | 路径 | 增强特性 |
|------|------|---------|
| `ButtonEx` | `Assets/Script/UI/Elements/ButtonEx.cs` | 按压缩放动画（0.95x）、双击支持、音效反馈、防连点 |
| `TextEx` | `Assets/Script/UI/Elements/TextEx.cs` | 多语言 Key 绑定、富文本扩展、字体降级 |
| `ImageEx` | `Assets/Script/UI/Elements/ImageEx.cs` | 异步加载、灰度化、点击穿透控制 |
| `RawImageEx` | `Assets/Script/UI/Elements/RawImageEx.cs` | 异步纹理加载、内存管理 |
| `SliderEx` | `Assets/Script/UI/Elements/SliderEx.cs` | 缓动动画、分段显示 |

> **强制规范**：新建 UI 预制体中，禁止使用原生 `Button`/`Text`/`Image`，必须使用 `ButtonEx`/`TextEx`/`ImageEx` 等增强版本。

#### UIBaseBehaviour 生命周期

`UIBaseBehaviour` 是所有 UI 子组件的通用基类，提供标准化生命周期：

```csharp
public class UIBaseBehaviour : MonoBehaviour
{
    public virtual void Initialize() { }   // 初始化（替代 Awake/Start）
    public virtual void OnUpdate() { }     // 帧更新（由宿主 Window 驱动，非 Unity Update）
    public virtual void Clear() { }        // 清理（释放引用、取消事件监听）
}
```

> **注意**：`OnUpdate()` 不是 Unity 原生的 `Update()`，而是由宿主 `Window` 在其 `OnUpdate` 中手动调用，避免每个子组件独立注册 MonoBehaviour.Update 带来的性能开销。

#### UIAdapter 屏幕适配

`UIAdapter.cs` 支持 9+1 种屏幕适配定位模式，通过 `AdapterType` 枚举配置：

| AdapterType | 锚点位置 | 典型用途 |
|------------|---------|---------|
| `Left` | 左侧居中 | 侧边栏 |
| `Right` | 右侧居中 | 侧边栏 |
| `TopLeft` | 左上角 | 玩家信息/小地图 |
| `TopCenter` | 顶部居中 | 系统通知栏 |
| `TopRight` | 右上角 | 设置按钮/时间 |
| `Center` | 屏幕中心 | 瞄准准心/模态弹窗 |
| `BottomLeft` | 左下角 | 移动摇杆 |
| `BottomCenter` | 底部居中 | 技能栏/物品栏 |
| `BottomRight` | 右下角 | 射击/技能按钮 |
| `FullScreen` | 全屏拉伸 | Loading/转场 |

**异形屏适配要点**：
- 自动检测刘海屏/挖孔屏，在刘海侧追加安全边距
- iPad 设备使用自定义边距（横屏两侧留更多空间）
- `Screen.safeArea` 作为适配基准，`UIAdapter` 在此基础上叠加 `AdapterType` 偏移

### §1.10 提示系统

提示系统分三层，覆盖从通用弹窗到模式特定提示的全部场景：

```
┌────────────────────────────────────────────────────────────┐
│                     提示系统三层架构                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────┐            │
│  │  Tips/（46 文件）— 通用提示层               │            │
│  │                                            │            │
│  │  · 确认弹窗 / 二次确认                      │            │
│  │  · Toast 飘字提示                           │            │
│  │  · 物品获取提示                              │            │
│  │  · 系统错误/网络异常提示                     │            │
│  │  · 引导/教学弹窗                            │            │
│  └────────────────────────────────────────────┘            │
│                                                            │
│  ┌────────────────────────────────────────────┐            │
│  │  TipsWar/（15 文件）— 战场信息层            │            │
│  │                                            │            │
│  │  · 击杀信息面板（Kill Feed）                 │            │
│  │  · 伤害数字飘字                              │            │
│  │  · 拾取物品提示                              │            │
│  │  · 队友倒地/淘汰通知                         │            │
│  │  · 安全区收缩警告                            │            │
│  └────────────────────────────────────────────┘            │
│                                                            │
│  ┌────────────────────────────────────────────┐            │
│  │  WarModeTips/（28 文件）— 模式特定提示层     │            │
│  │                                            │            │
│  │  · 模式专属任务提示                          │            │
│  │  · 模式特殊状态变更通知                      │            │
│  │  · 模式积分/排名变化提示                     │            │
│  │  · 模式特殊事件弹窗                          │            │
│  └────────────────────────────────────────────┘            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**提示优先级规则**：Tips 中的窗口使用 `WindowType.Tip`（sortOrder 7000+），确保始终显示在 Normal/Modal 窗口之上。战场提示（TipsWar）通常不使用独立 Window，而是挂载在 HUD 层作为子组件，由 `PlayerOperateWin` 统一管理生命周期。

### §1.11 战场初始化流程（→ [[ui-war-init]]）

战场初始化通过 `StartGame.cs` 及其模式变体驱动整个战场 UI 和逻辑的搭建：

```
场景加载完成
    │
    ▼
StartGame.cs 主初始化控制器
    │
    ├─ 1. 网络初始化
    │     └─ GameWorldNetworkManager 连接/同步
    │
    ├─ 2. 场景层级搭建（ButtleMap + ButtleLayer）
    │     ├─ Role 层    ← 角色实体
    │     ├─ Net 层     ← 网络实体
    │     ├─ Item 层    ← 场景物品
    │     ├─ Tree 层    ← 植被/可破坏物
    │     ├─ UI 层      ← UI Canvas 根节点
    │     ├─ Effect 层  ← 特效根节点
    │     ├─ Car 层     ← 载具根节点
    │     └─ Level 层   ← 关卡逻辑
    │
    ├─ 3. 镜头初始化
    │     └─ 战场摄像机设置
    │
    ├─ 4. 角色创建
    │     └─ 本地玩家角色实例化
    │
    ├─ 5. HUD 初始化
    │     └─ PlayerOperateWin.Open()
    │         └─ InputControlManager.Init()
    │
    └─ 6. 模式特定初始化
          └─ StartGame[ModeName].cs（11 种变体）
              ├─ StartGameClassic        ← 经典吃鸡
              ├─ StartGameTeamDeath      ← 团队死斗
              ├─ StartGameInfection      ← 感染模式
              └─ ... 等 8 种
```

**ButtleLayer 场景层级**：

| 层级名称 | 功能 | 与 UI 的关系 |
|---------|------|-------------|
| `Role` | 角色实体容器 | 血条/名牌等世界空间 UI 跟随 |
| `Net` | 网络同步实体 | 网络状态指示器 |
| `Item` | 场景物品 | 拾取提示 UI |
| `Tree` | 植被/可破坏物 | 无直接 UI 关联 |
| `UI` | UI Canvas 根节点 | 所有 Screen Space UI 的父节点 |
| `Effect` | 特效根节点 | 特效 UI（伤害数字等） |
| `Car` | 载具根节点 | 载具 HUD（油量/血量） |
| `Level` | 关卡逻辑 | 关卡事件触发 UI |

**弹幕聊天系统**（`BarrageCell.cs`）：
- 战场内实时聊天以弹幕形式展示
- 挂载在 HUD 层，随 PlayerOperateWin 生命周期管理
- 支持文本消息、快捷语音、表情

---

## §2 新增窗口 Checklist

### 步骤总览

```
① 创建 Controller 子类
     │
     ▼
② 在 WindowsConfig 中注册窗口配置
     │
     ▼
③ 创建 UI 预制体（Prefab）
     │
     ▼
④ 创建 Window 子类并挂载到预制体
     │
     ▼
⑤ 在 Controller 中实现业务逻辑
     │
     ▼
⑥ 配置屏幕适配（UIAdapter）
     │
     ▼
⑦ 功能测试与验收
```

### 步骤详解

#### ① 创建 Controller 子类

```csharp
// Assets/Script/UI/[YourModule]/[YourModule]Controller.cs
public class YourModuleController : Controller
{
    // FunctionName 必须与 WindowsConfig 中的 key 一致
    public override string FunctionName => "YourModuleWin";

    // 传入数据（可选）
    public YourDataModel Data { get; private set; }

    public override void PreLoad()
    {
        base.PreLoad();
        // 预加载资源（如有需要）
    }

    public override void Open()
    {
        base.Open();
        // 初始化数据
    }

    public override void Close()
    {
        // 清理数据
        base.Close();
    }

    // 业务方法
    public void SetData(YourDataModel data)
    {
        Data = data;
        if (Window != null && Window.IsOpened)
        {
            (Window as YourModuleWin)?.RefreshUI();
        }
    }
}
```

#### ② 在 WindowsConfig 中注册

在 `Assets/Script/Config/WindowsConfig.cs` 的配置数据库中添加新窗口条目：

| 配置字段 | 说明 | 示例值 |
|---------|------|--------|
| `FunctionName` | 窗口唯一标识（与 Controller.FunctionName 一致） | `"YourModuleWin"` |
| `PrefabPath` | 预制体路径 | `"Assets/ToBundle/UI/YourModule/YourModuleWin.prefab"` |
| `WindowType` | 窗口类型（决定层级） | `WindowType.Normal` |
| `ShowBlur` | 是否显示高斯模糊遮罩 | `true` / `false` |

#### ③ 创建 UI 预制体

预制体创建规范：
- 路径：`Assets/ToBundle/UI/[YourModule]/YourModuleWin.prefab`
- 根节点必须挂载 `Window` 子类脚本
- 所有文本使用 `TextEx`，所有按钮使用 `ButtonEx`，所有图片使用 `ImageEx`
- 根据需要挂载 `UIAdapter` 组件设置适配模式
- Canvas Scaler 设置：Reference Resolution = 1920×1080，Match = 0.5

#### ④ 创建 Window 子类

```csharp
// Assets/Script/UI/[YourModule]/YourModuleWin.cs
public class YourModuleWin : Window
{
    [SerializeField] private TextEx titleText;
    [SerializeField] private ButtonEx closeBtn;
    [SerializeField] private ButtonEx confirmBtn;

    protected override void BeforeOpen()
    {
        base.BeforeOpen();
        // 绑定事件
        closeBtn.onClick.AddListener(OnCloseClick);
        confirmBtn.onClick.AddListener(OnConfirmClick);
    }

    protected override void AfterOpen()
    {
        base.AfterOpen();
        RefreshUI();
    }

    protected override void BeforeClose()
    {
        // 解绑事件
        closeBtn.onClick.RemoveListener(OnCloseClick);
        confirmBtn.onClick.RemoveListener(OnConfirmClick);
        base.BeforeClose();
    }

    public void RefreshUI()
    {
        var ctrl = ControllerManager.Instance.Get<YourModuleController>();
        if (ctrl?.Data != null)
        {
            titleText.text = ctrl.Data.Title;
        }
    }

    private void OnCloseClick()
    {
        ControllerManager.Instance.Close<YourModuleController>();
    }

    private void OnConfirmClick()
    {
        // 确认逻辑
    }
}
```

#### ⑤ 实现业务逻辑

在 Controller 中实现数据获取/处理，在 Window 中实现 UI 刷新。保持 Controller 持有数据、Window 只负责展示的分层原则。

#### ⑥ 配置屏幕适配

在预制体上的需要适配的节点挂载 `UIAdapter` 组件：
- 选择合适的 `AdapterType`（参考 §1.9）
- 测试刘海屏/iPad 等特殊设备的显示效果

#### ⑦ 功能测试

- [ ] 打开/关闭窗口无报错
- [ ] 窗口层级正确（不被其他窗口遮挡）
- [ ] 高斯模糊遮罩正确显示/隐藏
- [ ] 多次快速打开/关闭无异常
- [ ] 内存无泄漏（关闭后引用正确释放）
- [ ] 各分辨率/刘海屏适配正常
- [ ] 战场 UI 在战场结束时正确关闭（IsBattleUI）

---

## §3 配置详解

### §3.1 WindowsConfig 窗口配置

`WindowsConfig.cs`（`Assets/Script/Config/WindowsConfig.cs`）是窗口系统的配置数据库，定义了所有窗口的注册信息。

**配置项说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `FunctionName` | string | ✅ | 窗口唯一标识，Controller.FunctionName 必须与此一致 |
| `PrefabPath` | string | ✅ | 预制体资源路径 |
| `WindowType` | enum | ✅ | 窗口类型（Base/Normal/Modal/Tip/System/MaxMap/OverLay） |
| `ShowBlur` | bool | ❌ | 打开时是否在下层窗口上叠加高斯模糊遮罩（默认 false） |
| `PreLoad` | bool | ❌ | 是否在启动时预加载（默认 false，仅频繁使用的窗口开启） |
| `IsBattleUI` | bool | ❌ | 是否为战场 UI（战场结束时自动关闭） |

**WindowType 选择指南**：

| 场景 | 推荐 WindowType | 原因 |
|------|---------------|------|
| 大厅主界面 | `Base` | 固定底层，不参与层级动态计算 |
| 商城/背包/好友 | `Normal` | 普通功能面板，支持多层叠加 |
| 购买确认/二次确认 | `Modal` | 模态弹窗，阻断下层交互 |
| 获取物品/成就达成 | `Tip` | 短暂提示，不阻断操作 |
| 网络断线 | `System` | 最高优先级系统级弹窗 |
| 全屏大地图 | `MaxMap` | 专用层级，覆盖战场 UI |
| Loading/转场 | `OverLay` | 最顶层覆盖一切 |

**预加载策略**（`PreLoadByFunctionName`）：

```
WindowManager.PreLoadByFunctionName(functionName)
  │
  ├─ 1. 根据 functionName 从 WindowsConfig 获取预制体路径
  ├─ 2. 通过 UIPool 异步加载预制体
  ├─ 3. 实例化但不激活（Canvas.enabled = false）
  └─ 4. 缓存在 UIPool 中，后续 Open 时直接取用
```

> **预加载适用场景**：战场 HUD（`PlayerOperateWin`）、通用 Tips 窗口等高频使用的窗口建议预加载。低频窗口（设置/商城）不建议预加载，避免内存浪费。

### §3.2 UIAdapter 屏幕适配配置

`UIAdapter.cs`（`Assets/Script/UI/UGUIAdapter/UIAdapter.cs`）负责处理不同设备的屏幕适配。

**适配原理**：

```
物理屏幕
┌──────────────────────────────────────────┐
│  ┌──刘海──┐                              │
│  │        │   Screen.safeArea             │
│  │  ┌─────┴──────────────────────────┐   │
│  │  │                                │   │
│  │  │     UIAdapter 适配区域          │   │
│  │  │     (safeArea + AdapterType     │   │
│  │  │      偏移计算)                  │   │
│  │  │                                │   │
│  │  └────────────────────────────────┘   │
│  └────────────────────────────────────────┘
└──────────────────────────────────────────┘
```

**使用方式**：

1. 在需要适配的 UI 节点上挂载 `UIAdapter` 组件
2. 在 Inspector 中设置 `AdapterType`
3. 运行时 UIAdapter 自动根据 `Screen.safeArea` 和设备类型计算偏移

**iPad 特殊处理**：
- iPad 设备横屏时左右两侧留出自定义边距
- 通过设备检测自动生效，无需额外配置

**刘海屏检测**：
- 利用 `Screen.safeArea` 与 `Screen.width/height` 的差值判断
- 刘海侧自动追加安全边距，防止 UI 元素被遮挡

### §3.3 InputControlManager 输入配置

`InputControlManager`（`Assets/Script/UI/PlayerControl/InputControlManager.cs`）是 Singleton 输入管理器，控制战场中玩家的操作输入分发。

**控制风格切换逻辑**：

```
InputControlManager.UpdateControlStyle()
  │
  ├─ 角色状态检查
  │   ├─ 驾驶载具？  → VehicleMoveButtonControl
  │   ├─ 飞行载具？  → AircraftMoveButtonControl
  │   ├─ 观战模式？  → ObserveButtonControl
  │   ├─ OB 模式？   → OBButtonControl
  │   ├─ 编辑器？    → EditorButtonControl
  │   ├─ 背包打开？  → PackButtonControl
  │   └─ 默认步行    → BattleStateButtonControl
  │
  └─ 切换时自动调用：
      ├─ oldControl.OnExit()    ← 旧控制器退出
      └─ newControl.OnEnter()   ← 新控制器进入
```

### §3.4 ButtonControl 按钮映射

每个 `IButtonControl` 实现定义了一组按钮的可见性和行为映射。以 `BattleStateButtonControl` 为例：

| 按钮 | 可见条件 | 点击行为 |
|------|---------|---------|
| 移动摇杆 | 始终可见 | 驱动 IMove.OnMove() |
| 射击按钮 | 持有武器 | 触发射击 |
| 瞄准按钮 | 持有可瞄准武器 | 切换瞄准模式 |
| 换弹按钮 | 弹夹未满 | 触发换弹 |
| 技能按钮 | 技能可用 | 释放技能 |
| 跳跃按钮 | 非载具状态 | 角色跳跃 |
| 趴下按钮 | 非载具状态 | 切换趴下姿态 |
| 背包按钮 | 始终可见 | 打开背包界面 |
| 地图按钮 | 始终可见 | 切换小地图/大地图 |

> **配置要点**：按钮可见性和行为通过各 `ButtonControl` 子类的 `UpdateControlState()` 方法动态控制，不在配置文件中静态定义。

---

## §4 关键代码路径

### §4.1 打开/关闭窗口

**打开窗口完整调用链**：

```
// 外部调用入口
ControllerManager.Instance.Open<LobbyController>();

// 调用链展开
ControllerManager.Open<T>()
  │
  ├─ 1. controller = GetOrCreate<T>()           ← 获取或创建 Controller 实例
  ├─ 2. controller.PreLoad()                     ← 预加载资源
  │
  └─ 3. WindowManager.Instance.Open(controller)
          │
          ├─ 3a. config = WindowsConfig.Get(controller.FunctionName)
          │       └─ 获取预制体路径、WindowType 等配置
          │
          ├─ 3b. windowObj = UIPool.Get(config.PrefabPath)
          │       ├─ 池中有缓存？ → 直接取出
          │       └─ 池中无缓存？ → Instantiate 新实例
          │
          ├─ 3c. window = windowObj.GetComponent<Window>()
          │
          ├─ 3d. window.SetSortOrder(计算层级)
          │       └─ 根据 WindowType + 栈深度计算 sortOrder
          │
          ├─ 3e. OnCreateWindowEvent.Invoke()     ← 创建事件
          │
          ├─ 3f. window.BeforeOpen()               ← 初始化
          │       └─ OnBeforeOpenEvent.Invoke()
          │
          ├─ 3g. window.Active()                   ← Canvas.enabled = true
          │       └─ OnActivatedEvent.Invoke()
          │
          ├─ 3h. window.AfterOpen()                ← 开场动画
          │       └─ OnAfterOpenEvent.Invoke()
          │
          └─ 3i. 高斯模糊遮罩处理
                  └─ config.ShowBlur ? 开启模糊 : 无操作
```

**关闭窗口完整调用链**：

```
// 外部调用入口
ControllerManager.Instance.Close<LobbyController>();

// 调用链展开
ControllerManager.Close<T>()
  │
  ├─ 1. controller = Get<T>()
  │
  └─ 2. WindowManager.Instance.Close(controller.FunctionName)
          │
          ├─ 2a. window = FindWindow(functionName)
          │
          ├─ 2b. OnBeforeCloseEvent.Invoke()
          ├─ 2c. window.BeforeClose()              ← 保存数据
          │
          ├─ 2d. window.AfterClose()               ← Canvas.enabled = false
          │       └─ OnAfterCloseEvent.Invoke()
          │
          ├─ 2e. UIPool.Return(windowObj)           ← 回池缓存
          │       └─ 或 Destroy（不可复用的窗口）
          │
          ├─ 2f. 高斯模糊遮罩关闭
          │
          └─ 2g. controller.Close()                ← Controller 清理
```

**Show/Hide 与 Open/Close 的区别**：

| 操作 | 行为 | 适用场景 |
|------|------|---------|
| `Open/Close` | 完整生命周期，涉及实例化/销毁 | 功能面板的打开/关闭 |
| `Show/Hide` | 仅切换 Canvas.enabled | 临时隐藏（截图/转场时） |

### §4.2 按钮输入处理流程

**从玩家触摸到角色操作的完整链路**：

```
玩家触摸屏幕（或点击按钮）
    │
    ▼
Unity EventSystem → ButtonEx.OnPointerDown/Up/Click
    │
    ▼
InputControlManager.OnUpdate()（每帧）
    │
    ├─ UpdateControlStyle()
    │   └─ 判断当前应使用哪个 ButtonControl
    │
    ├─ UpdateControlState()
    │   └─ 更新所有按钮的可见性和可用性
    │
    └─ currentButtonControl.OnUpdate()
        │
        ├─ 摇杆输入检测
        │   └─ currentMove.OnMove(direction, magnitude)
        │       └─ 发送移动指令到角色控制器
        │
        ├─ 射击按钮检测
        │   └─ 长按 → 持续射击
        │   └─ 松开 → 停止射击
        │
        ├─ 技能按钮检测
        │   └─ SM_Ability.PlayAbility()
        │
        └─ 其他按钮检测
            └─ 对应操作回调
```

### §4.3 物品拾取 UI 流程

```
战场中物品进入玩家拾取范围
    │
    ▼
网络层通知 → Item 触发检测
    │
    ▼
拾取提示 UI 显示（TipsWar 层）
    │
    ├─ 自动拾取：直接执行拾取
    │   └─ 拾取结果通知 → TipsWar 飘字
    │
    └─ 手动拾取：显示拾取按钮
        │
        ▼
    玩家点击拾取按钮
        │
        ▼
    发送拾取请求 → 服务端验证
        │
        ▼
    拾取成功回调
        ├─ 背包 UI 更新
        ├─ 拾取飘字提示
        └─ 场景物品消失
```

### §4.4 模式特定 UI 加载流程

不同游戏模式通过 `StartGame[ModeName].cs` 加载模式特定的 UI 元素：

```
StartGame 基础初始化完成
    │
    ▼
根据当前 ModeName 选择 StartGame 变体
    │
    ├─ StartGameClassic
    │   └─ 加载：安全区倒计时 + 存活人数 + 空投提示
    │
    ├─ StartGameTeamDeath
    │   └─ 加载：双方比分面板 + 复活倒计时
    │
    ├─ StartGameInfection
    │   └─ 加载：感染进度 + 感染者/幸存者计数
    │
    └─ 其他模式变体...
        └─ 各自加载模式特定 UI 元素
            │
            ▼
    WarModeTips/ 中对应的提示组件激活
    TipsWar/ 中的通用战场提示组件激活
```

> **扩展新模式 UI 的要点**：
> 1. 在 `War/` 目录下创建 `StartGame[NewMode].cs`，继承 `StartGame` 基础流程
> 2. 在 `WarModeTips/` 下创建模式特定的提示组件
> 3. 在 StartGame 变体中调用模式特定组件的初始化

---

## §5 踩坑记录

### 坑 1：窗口排序层级冲突

**现象**：两个 Normal 类型窗口同时打开时，后打开的窗口被先打开的窗口遮挡。

**原因**：手动设置了 Canvas.sortingOrder 覆盖了 WindowManager 的自动排序。

**解决**：禁止在 Window 子类中手动设置 `Canvas.sortingOrder`，层级完全由 `WindowManager.SetSortOrder()` 根据 WindowType + 栈深度自动计算。如有特殊需求，通过调整 `WindowType` 或使用 `OverLay` 类型解决。

---

### 坑 2：Window 关闭后事件监听未清理导致内存泄漏

**现象**：频繁打开/关闭某窗口后内存持续增长，Profiler 显示 Window 实例未被 GC 回收。

**原因**：在 `BeforeOpen()` 中注册了全局事件监听（如 `EventManager.AddListener`），但在 `BeforeClose()` 中未对应移除，导致全局事件持有 Window 引用。

**解决**：

```csharp
// ✅ 正确做法：成对注册/注销
protected override void BeforeOpen()
{
    base.BeforeOpen();
    EventManager.AddListener(EventType.OnScoreChanged, OnScoreChanged);
}

protected override void BeforeClose()
{
    EventManager.RemoveListener(EventType.OnScoreChanged, OnScoreChanged);
    base.BeforeClose();
}

// ❌ 错误做法：只注册不注销
protected override void BeforeOpen()
{
    base.BeforeOpen();
    EventManager.AddListener(EventType.OnScoreChanged, OnScoreChanged);
}
// BeforeClose 中漏掉 RemoveListener
```

---

### 坑 3：UIAdapter 在编辑器中不生效

**现象**：UIAdapter 在编辑器（Game View）中不产生偏移，部署到设备后才生效。

**原因**：编辑器的 `Screen.safeArea` 返回全屏区域，没有刘海/挖孔区域，因此 UIAdapter 计算的偏移为 0。

**解决**：
- 使用 Unity Device Simulator 模拟特定设备的 safeArea
- 或在 UIAdapter 中添加编辑器模拟开关，手动设置 safeArea 进行调试
- 真机测试仍然是最终验证手段

---

### 坑 4：高斯模糊遮罩与多窗口叠加异常

**现象**：连续打开两个 `ShowBlur = true` 的窗口，关闭第二个时高斯模糊消失，但第一个窗口仍然打开。

**原因**：高斯模糊遮罩采用引用计数机制，但关闭第二个窗口时错误地将计数直接清零而非 -1。

**解决**：确保高斯模糊遮罩的引用计数正确匹配：
- 每次 Open 且 `ShowBlur = true` → 计数 +1
- 每次 Close 且 `ShowBlur = true` → 计数 -1
- 计数归零时才关闭模糊遮罩

---

### 坑 5：InputControlManager 控制器切换时按钮状态残留

**现象**：从载具下车后，载具专属按钮（如氮气加速）仍然显示在 HUD 上。

**原因**：`VehicleMoveButtonControl.OnExit()` 中未正确隐藏所有载具专属按钮，部分按钮的可见性状态在切换时被遗漏。

**解决**：在每个 `ButtonControl.OnExit()` 中，必须显式重置所有该控制器管理的按钮状态。推荐在 `AbsButtonControl.OnExit()` 基类中添加统一的按钮状态重置逻辑，子类只需 `base.OnExit()` 即可。

---

### 坑 6：快速连续 Open/Close 导致窗口状态异常

**现象**：极短时间内连续调用 `Open → Close → Open`，窗口处于半开半闭的异常状态。

**原因**：Open 是异步流程（涉及资源加载），Close 在 Open 未完成时被调用，导致生命周期回调顺序混乱。

**解决**：
- `WindowManager.Open()` 内部维护打开队列，同一窗口不允许并发 Open
- 在 `Open` 进行中收到 `Close` 请求时，标记为 "pending close"，等 Open 完成后立即执行 Close
- 使用 `Controller.IsOpen` 和 `Window.IsOpened` 双重状态检查

---

### 坑 7：预制体中使用原生 UGUI 组件导致功能缺失

**现象**：新建的 UI 预制体中按钮没有按压缩放效果和音效反馈。

**原因**：使用了 Unity 原生 `Button` 组件而非项目封装的 `ButtonEx`。

**解决**：严格遵守组件使用规范（见 §1.9），所有 UI 预制体中禁止使用原生 `Button`/`Text`/`Image`，必须使用 `ButtonEx`/`TextEx`/`ImageEx`。在代码审查中将此作为必检项。

---

## §6 验收标准

### 6.1 新增窗口验收清单

| # | 检查项 | 验收标准 | 通过 |
|---|-------|---------|------|
| 1 | Controller 注册 | `FunctionName` 与 `WindowsConfig` 条目一致 | ☐ |
| 2 | WindowType 正确 | 窗口类型选择合理，层级不与现有窗口冲突 | ☐ |
| 3 | 生命周期完整 | `BeforeOpen` 中注册的事件在 `BeforeClose` 中全部注销 | ☐ |
| 4 | 增强组件使用 | 无原生 `Button`/`Text`/`Image`，全部使用 `Ex` 版本 | ☐ |
| 5 | 屏幕适配 | 刘海屏/iPad/不同分辨率下 UI 元素不被遮挡、不溢出 | ☐ |
| 6 | 高斯模糊遮罩 | 需要遮罩的窗口正确配置 `ShowBlur`，多层叠加/关闭行为正确 | ☐ |
| 7 | 内存安全 | 反复打开/关闭 10 次后无内存泄漏（Profiler 验证） | ☐ |
| 8 | 快速操作 | 极速连续打开/关闭不导致异常状态 | ☐ |
| 9 | 战场 UI 标记 | 战场相关窗口正确设置 `IsBattleUI = true` | ☐ |
| 10 | 预加载策略 | 高频窗口配置预加载，低频窗口按需加载 | ☐ |

### 6.2 HUD 按钮控制验收清单

| # | 检查项 | 验收标准 | 通过 |
|---|-------|---------|------|
| 1 | 控制器切换 | 步行/载具/观战/OB 模式切换时按钮状态正确更新 | ☐ |
| 2 | 按钮可见性 | 各状态下按钮的显示/隐藏符合设计（无多余按钮残留） | ☐ |
| 3 | 输入响应 | 摇杆/按钮输入正确传达到角色控制器 | ☐ |
| 4 | 退出清理 | `ButtonControl.OnExit()` 中所有按钮状态正确重置 | ☐ |
| 5 | 移动控制 | 移动摇杆在各 `IMove` 实现中行为一致且流畅 | ☐ |

### 6.3 地图系统验收清单

| # | 检查项 | 验收标准 | 通过 |
|---|-------|---------|------|
| 1 | 小地图/大地图切换 | 切换流畅，标记位置正确同步 | ☐ |
| 2 | 标记更新 | 玩家/AI/物品标记实时跟随目标位置 | ☐ |
| 3 | 毒圈可视化 | `PoisonGraphic` 与 `SafeAreaManager` 数据一致 | ☐ |
| 4 | 兴趣点 | `UIMapSpotMgr` 管理的兴趣点正确显示/隐藏 | ☐ |
| 5 | 性能 | 大量标记（50+）时地图帧率不低于 30fps | ☐ |

### 6.4 提示系统验收清单

| # | 检查项 | 验收标准 | 通过 |
|---|-------|---------|------|
| 1 | 层级正确 | Tips 窗口始终显示在 Normal/Modal 之上 | ☐ |
| 2 | 自动消失 | Toast 类提示在指定时间后自动消失 | ☐ |
| 3 | 队列管理 | 多条提示同时触发时按队列依次显示，不重叠 | ☐ |
| 4 | 战场提示 | TipsWar 提示正确挂载在 HUD 层，随 HUD 生命周期管理 | ☐ |
| 5 | 模式提示 | WarModeTips 在非对应模式下不加载/不显示 | ☐ |
