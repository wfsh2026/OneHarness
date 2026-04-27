# UI 系统开发 AI 技术范例文档

> **适用对象**：AI Agent、程序、技术策划  
> **适用场景**：新建/修改大厅 UI、战斗 HUD、弹窗、加载页、结算页、全局 UI Feature  
> **核心目标**：让 AI 在阅读一份文档后，就能理解 `UIViewManager` 体系、知道该改哪些文件、哪些不能改，以及在**缺少正式美术资源**时如何用灰盒 UGUI 方式先交付可运行界面。  
> **代码根目录**：`G:\BiuBiuBiu2-MiniGame\Assets\Scripts`

---

## 1. 文档定位

本文件整合了原 `UI系统开发` 目录下的：

- `UI 开发文档中心.txt`
- `UIViewManager 快速上手指南.txt`
- `UIViewManager 技术文档.txt`
- `UIViewManager 架构图与流程图.txt`

并按 **“给 AI 使用”** 的方式重新整理，目标不是培训新手，而是让 AI 能快速判断：

1. 这是 `UIView`、`RegisterFeature`、`UIControl` 还是层级/生命周期配置问题。
2. 需要改哪些文件，按什么顺序改。
3. 没有美术资源时，如何用灰盒 UGUI 快速搭一个可运行版本。
4. 哪些参考内容只是旧习惯，哪些是当前工程中的真实实现。

---

## 2. 系统总览

### 2.1 UI 系统的核心角色

当前项目的 UI 系统以 `UIViewManager` 为唯一管理入口，负责：

- UI 打开/关闭
- UI 层级排序
- 生命周期切换
- 全屏 UI 遮挡处理
- 全局 RegisterFeature 初始化与清理
- 登录链路中的部分 UI 流程

### 2.2 真实代码结构

```text
Assets\Scripts\UI\UIView\
├── UIViewManager.cs                  核心逻辑
├── UIViewManager_Static.cs           静态接口
├── UIViewManager_Layer.cs            层级配置
├── UIViewManager_LifeCycle.cs        生命周期配置
├── UIViewManager_LoginGame.cs        登录流程
├── UIViewManager_RegisterFeature.cs  Feature 注册配置
├── UIViewBase.cs                     View 基类
├── UIRoot.cs                         UI Root 层级容器
├── Feature\                          具体界面
└── RegisterFeature\                  全局常驻监听模块

Assets\Scripts\UI\UIControl\          具体控件与页面逻辑
Assets\Scripts\Message\GamePlay\Client\World\CM_UI.cs
Assets\Scripts\Message\UI\World\UIM_UI.cs
```

### 2.3 架构关系

```text
UIViewManager
├── Layer Manager        层级：Scene / Control / UI / UITip1 / UITip2 / Loading / SystemTip
├── LifeCycle Manager    生命周期：All / Room / Battle / WarEnd / Login
├── RegisterFeature      全局常驻消息监听
└── UIViewBase           具体页面实例
```

---

## 3. AI 应先做的判断

收到 UI 需求后，先判断它属于哪类：

| 类型 | 典型需求 | 主要落点 |
|------|---------|---------|
| `UIView` | “加一个活动页”“做一个结算弹窗” | `UI\UIView\Feature\XxxView.cs` |
| `RegisterFeature` | “登录后一直监听一个活动入口” | `UI\UIView\RegisterFeature\XxxRegisterView.cs` |
| `UIControl` | “改设置页里的按钮布局/列表项表现” | `UI\UIControl\...` |
| Layer/LifeCycle 配置 | “只在战斗里显示”“改成提示层” | `UIViewManager_Layer.cs` / `UIViewManager_LifeCycle.cs` |

**结论规则：**

- 有界面容器 = 优先判断为 `UIView`
- 不一定开界面，但要持续监听 = 优先判断为 `RegisterFeature`
- 只改某个页面内部控件表现 = 优先判断为 `UIControl`
- 现有页面“能开但时机/层级不对” = 优先判断为配置问题

---

## 4. 当前工程中的真实机制

### 4.1 打开 UI 的真实流程

```text
UIViewManager.OpenUI<T>()
→ OnOpenUI<T>()
→ 若不存在则 new T()
→ 根据类型查 Layer / LifeCycle
→ UIViewBase.Init(...)
→ AssetManager.LoadUI(...)
→ 加载完成后生成 UIBase
→ 设置父节点与 SortOrder
→ 回调 openEndCallBack
```

### 4.2 关闭 UI 的真实流程

```text
UIViewManager.CloseUI<T>()
→ OnCloseUI<T>()
→ 调用 view.Close()
→ UIViewBase.OnClose()
→ ui.Clear()
→ Destroy(ui.gameObject)
→ 从 views 列表移除
→ 若是全屏 UI，恢复被遮挡的界面
```

### 4.3 生命周期切换

```text
UIViewManager.SetCurrentLifeCycle(newCycle)
→ 遍历当前打开的 views
→ 不属于新生命周期的 UI 自动关闭
→ All 生命周期 UI 保留
```

### 4.4 Feature 初始化

```text
UIViewManager.Init()
→ InitRegisterFeature()
→ ConfigureRegisterFeatures()
→ AddRegisterFeature<T>()
→ feature.Init()
```

---

## 5. 重要：参考文档与真实代码的口径差异

为了避免 AI 被旧文档带偏，这里明确几条**以代码为准**的事实：

1. `UIViewBase` **没有**通用 `OnOpen()` 钩子。  
   若需要在 UI 加载完成后拿到 `UIBase` 做初始化，应使用：
   - `protected override void OnLoadUICompleted(UIBase ui)`
   - 或 `UIViewManager.OpenUI<T>(ui => { ... })` 的打开回调

2. `UI`、`UITip1`、`UITip2` 虽然是不同层级概念，但都挂在 `UIRoot.UILayer` 上，主要靠 `SortOrder` 区分。

3. 不要假设可以随意扩展新的 UI 管理器；当前唯一入口就是 `UIViewManager`。

4. 登录链路相关逻辑在 `UIViewManager.cs` / `UIViewManager_LoginGame.cs` 中，默认不应被普通 UI 需求修改。

---

## 6. Layer 与 LifeCycle 速查

### 6.1 Layer 速查

| 层级 | 枚举 | 基础值 | 适合放什么 |
|------|------|-------|-----------|
| Scene | `UIRootLayer.Scene` | 100 | 场景 UI、模式 HUD 背景、战斗叠层表现 |
| Control | `UIRootLayer.Control` | 300 | 摇杆、按钮、玩家控制 |
| UI | `UIRootLayer.UI` | 600 | 大厅、背包、商店、排行榜 |
| UITip1 | `UIRootLayer.UITip1` | 800 | 详情弹窗、确认弹窗、选择页 |
| UITip2 | `UIRootLayer.UITip2` | 1000 | 奖励展示、升级提示、功能解锁 |
| Loading | `UIRootLayer.Loading` | 1200 | 加载页 |
| SystemTip | `UIRootLayer.SystemTip` | 1500 | 公告、Toast、系统提示 |

### 6.2 LifeCycle 速查

| 生命周期 | 枚举 | 适合放什么 |
|---------|------|-----------|
| All | `UILifeCycle.All` | 全阶段常驻 UI |
| Room | `UILifeCycle.Room` | 大厅、房间、功能入口页 |
| Battle | `UILifeCycle.Battle` | 战斗 HUD、控制界面、战斗提示 |
| WarEnd | `UILifeCycle.WarEnd` | 结算页、奖励页、排行页 |
| Login | `UILifeCycle.Login` | 登录页、合规页、账号流程 |

---

## 7. AI 新建 UIView 的标准步骤

### 7.1 第一步：建 View

```csharp
using Sofunny.BiuBiuBiu2.UI;
using Sofunny.BiuBiuBiu2.View;

public class MyActivityView : UIViewBase {
    public MyActivityView() {
        FullScreenUI();
        SetViewType(ViewType.Room);
    }

    protected override void OnInit() {
        // 注册消息、初始化轻量状态
    }

    protected override void OnLoadUICompleted(UIBase ui) {
        // 拿到 UIBase 后做初始化
    }

    protected override void OnClose() {
        // 反注册消息、释放引用
    }
}
```

### 7.2 第二步：配 Layer

在 `UIViewManager_Layer.cs` 的 `layerToTypes` 中加入你的类型。

### 7.3 第三步：配 LifeCycle

在 `UIViewManager_LifeCycle.cs` 的 `lifeCycleToUI` 中加入你的类型。

### 7.4 第四步：必要时接消息或 Feature

如果页面不是用户主动打开，而是消息触发打开：

- 在业务消息里 `UIViewManager.OpenUI<MyActivityView>()`
- 或由 `RegisterFeature` 监听后打开

---

## 8. AI 新建 RegisterFeature 的标准步骤

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

然后在 `UIViewManager_RegisterFeature.cs` 中注册：

```csharp
AddRegisterFeature<MyActivityRegisterView>();
```

### 8.1 RegisterFeature 适合做什么

- 红点
- 公告
- 活动入口
- 重连提示
- 登录后持续监听的业务 UI 分发

### 8.2 不适合做什么

- 页面内部的一次性逻辑
- 必须依附某个具体页面生命周期的逻辑
- 与具体 View 强耦合的大段界面操作

---

## 9. 没有美术资源时，AI 应怎么做

这是给 AI 的**强约束**：

### 9.1 默认进入灰盒 UI 模式

如果用户没有给正式美术资源，AI **不应**因为缺图而停工。  
应先交付一个可运行的灰盒版本，目标类似场景系统里的灰盒生成：

- 验证信息结构
- 验证布局关系
- 验证层级遮挡
- 验证交互流程
- 验证返回与关闭逻辑

### 9.2 默认占位策略

| 元素 | 默认做法 |
|------|---------|
| 背景 | 半透明纯色底图 / 简单色块 |
| 面板底板 | 通用九宫格底图 / 默认 Sprite / 纯色 `Image` |
| 图标 | 占位框 + 文本标签 / 默认 Sprite |
| 按钮 | `Button + Image + Text` 组合 |
| 列表项 | 重复结构 + 占位图 + 文本 |
| 弹窗遮罩 | 半透明黑色 `Image` |

### 9.3 组件优先级

1. 优先复用项目内现成通用 `UISprite`
2. 若没有合适封装，使用常规 UGUI `Image`
3. 使用纯色底图、默认 Sprite、文本占位表达结构

### 9.4 灰盒 UI 交付标准

灰盒版本至少要满足：

- 可打开
- 可关闭
- 层级正确
- 生命周期正确
- 交互按钮可点
- 列表/弹窗/遮罩/返回链路可验证

### 9.5 灰盒 UI 不是“偷懒版”

灰盒只是视觉占位，不代表可以省略：

- `Layer` 配置
- `LifeCycle` 配置
- `OnClose()` 清理
- 消息注册/反注册
- Feature 接入
- 返回逻辑与遮挡逻辑

---

## 10. 常用消息与静态接口

### 10.1 常用静态接口

```csharp
UIViewManager.OpenUI<T>(callback);
UIViewManager.CloseUI<T>();
UIViewManager.IsOpen<T>();
UIViewManager.GetUI<T>();
UIViewManager.SetCurrentLifeCycle(UIViewManager.UILifeCycle.Battle);
UIViewManager.BackToLobby();
UIViewManager.CloseUIByType(UIViewBase.ViewType.Room);
```

### 10.2 常见消息

| 消息 | 用途 |
|------|------|
| `CM_UI.ShowDialog` | 通用确认弹窗 |
| `CM_UI.ShowToast` | 文本提示 |
| `CM_UI.PlayHudVFX` | HUD 特效 |
| `UIM_UI.OpenUIView` | UI 打开事件 |
| `UIM_UI.CloseUIView` | UI 关闭事件 |
| `UIM_UI.IsFullScreenUI` | 全屏状态事件 |

---

## 11. AI 修改 UI 时的优先级建议

### 11.1 优先改的文件

| 目标 | 优先落点 |
|------|---------|
| 加页面 | `Feature\XxxView.cs` |
| 加常驻监听 | `RegisterFeature\XxxRegisterView.cs` |
| 改层级 | `UIViewManager_Layer.cs` |
| 改生命周期 | `UIViewManager_LifeCycle.cs` |
| 改某个页面内部控件 | `UIControl\...` |

### 11.2 默认不要改的文件

- `UIViewManager.cs`
- `UIViewManager_Static.cs`
- `UIViewManager_LoginGame.cs`
- `UIViewBase.cs`
- `UIRoot.cs`

除非用户明确要求，且需求本身就是框架层改动。

---

## 12. 常见坑

### 12.1 UI 能打开但看不见

先检查：

1. 是否配置了 `UIViewManager_Layer.cs`
2. 是否配置了 `UIViewManager_LifeCycle.cs`
3. 当前 `LifeCycle` 是否匹配
4. 是否被全屏 UI 隐藏
5. `SortOrder` 是否被其他 UI 压住

### 12.2 生命周期切换时 UI 被自动关掉

通常是因为它不属于新的生命周期。  
优先修 `lifeCycleToUI`，不要误以为是打开逻辑坏了。

### 12.3 页面逻辑写进 Feature

Feature 适合“常驻监听 + 分发”，不适合变成“另一个页面控制器”。

### 12.4 误用不存在的 `OnOpen()`

当前工程中没有通用 `OnOpen()` 钩子。  
应使用：

- `OnLoadUICompleted(UIBase ui)`
- `UIViewManager.OpenUI<T>(ui => { ... })`

### 12.5 没图就停工

这是 AI 在 UI 任务里最常见的错误之一。  
正确做法是：**先交付灰盒 UGUI**，再让用户或美术替换资源。

---

## 13. 推荐的 AI 输出格式

当 AI 完成一个 UI 需求后，建议按以下方式汇报：

```text
【UI 需求拆解】
- 类型：UIView / RegisterFeature / UIControl / 配置修改
- 生效阶段：Room / Battle / WarEnd / Login / All
- 所在层级：UI / UITip1 / UITip2 / SystemTip ...

【本次修改文件】
- XxxView.cs
- UIViewManager_Layer.cs
- UIViewManager_LifeCycle.cs

【实现说明】
- 页面如何打开
- 由什么消息驱动
- 是否为全屏
- 是否使用灰盒占位资源

【待确认项】
- 正式美术资源是否后续替换
- 文案/图片/布局优先级是否需要调整
```

---

## 14. AI 最终检查清单

提交前至少确认：

- 已判断正确需求类型（View / Feature / UIControl / 配置）
- 新 UI 已配置 Layer
- 新 UI 已配置 LifeCycle
- `OnClose()` 做了必要清理
- 没有误改 `UIViewManager` 核心逻辑
- 若无美术资源，已采用灰盒 UGUI 方案
- 使用的文档口径与真实代码一致

---

## 15. 结论

对于 AI 来说，当前 UI 系统最重要的三条规则是：

1. **一切都围绕 `UIViewManager` 工作**，不要私造第二套 UI 框架。
2. **先判断是 View、Feature、UIControl 还是配置问题**，再动手。
3. **没有美术资源也要先交付灰盒 UGUI**，用默认 `UISprite` / `Image` 把结构和交互跑通。
