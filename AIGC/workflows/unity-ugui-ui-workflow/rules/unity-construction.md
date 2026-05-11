---
id: workflow-unity-ugui-ui-construction
title: Unity UGUI UI 施工规则
workflow: unity-ugui-ui-workflow
phase: construction
read_when: 需要由 UI 开发者生成 Unity UGUI Prefab 施工方案、Editor 创建脚本、Controller 或绑定表。
updated: 2026-05-11
---

# Unity UGUI UI 施工规则

UI 开发者负责把 UI 规划和资源核查产物落地为 Unity 工程内容。

## 角色声明

- 施工阶段开始输出时，必须先显示 `角色：UI 开发者`。
- UI 开发者只能使用已审核的资源核查交接包；不能直接使用未审核元素资源。
- 如果资源核查交接包返工，已经生成的施工内容降级为草稿，必须基于新交接包重新修订。
- 需要生成 `.cs` 和 Prefab 时，按 `context-isolation.md` 写入脚本文件和施工报告，不在主会话展开完整代码。

## 生成前条件

生成 Unity 代码前必须已经有：

- UI 规划输出。
- 资源验收与拼装结论。
- 正式资源包或明确的占位资源策略。
- UI 开发者对资源包的审核结论。
- UGUI 层级。
- RectTransform 布局表。
- 资源路径依赖表。
- 文本表。
- 按钮事件表。

缺失时先输出待确认项，不直接生成完整代码。

## 占位资源策略

如果 L2 或 L3 输入中存在缺失资源，但用户允许先施工，UI 开发者可以使用占位资源策略：

| 缺失类型 | 占位策略 |
| --- | --- |
| 缺少 Sprite | 创建 Image 节点但不绑定 Sprite，并输出缺失日志 |
| 缺少字体 | 使用项目默认 Font，并写入待替换项 |
| 缺少 Hover 状态图 | 使用 Normal 图代替，并写入待替换项 |
| 缺少动态数据来源 | 只暴露 Bind 字段，不写死测试值 |

使用占位策略时，产物必须标记为草稿，不得标记为最终交付。

## 必须输出

- UGUI Prefab 层级。
- `UILayoutSpec` 或等价集中配置。
- `CreateXXXPrefab.cs`。
- `XXXPanelController.cs`。
- 按钮事件接口。
- Prefab 绑定字段表。
- 资源路径依赖表。
- 运行检查清单。
- 截图校准反馈表。

## `UILayoutSpec` 最低字段

UI 开发者输出的 `UILayoutSpec` 或等价集中配置，至少包含：

| 字段 | 说明 |
| --- | --- |
| nodeName | 节点名 |
| nodeType | Image / Button / Text / CanvasGroup / Empty |
| parentPath | 父节点路径 |
| anchorPreset | 锚点预设 |
| pivot | Pivot |
| anchoredPosition | 位置 |
| sizeDelta | 尺寸 |
| localScale | 缩放 |
| siblingIndex | 层级顺序 |
| spritePath | 图片资源路径，可为空 |
| textContent | 固定文本，可为空 |
| textStyle | 文本样式，可为空 |
| buttonEvent | 按钮事件名，可为空 |
| raycastTarget | 是否参与点击 |
| activeDefault | 默认显示状态 |

布局、资源、按钮配置必须来自 `UILayoutSpec` 或集中表，不得散落在 Controller 业务代码中。

## 文件职责

### `CreateXXXPrefab.cs`

职责：

- 创建 Canvas、SafeArea 和 UI Layer。
- 创建 Image、Button、Text 等节点。
- 设置 RectTransform。
- 按资源路径加载 Sprite。
- 绑定 Button、Image、Text。
- 添加 `XXXPanelController`。
- 保存 Prefab。
- 输出缺失资源日志。

限制：

- 必须放在 `Editor` 目录。
- 必须使用 `UnityEditor` API。
- 必须提供菜单入口。
- 不写运行时业务逻辑。
- 布局值来自配置或集中表，不散落在方法体中。

### `XXXPanelController.cs`

职责：

- 持有 `[SerializeField]` 字段。
- 初始化按钮事件。
- 提供 `Show`、`Hide`、`Bind`、`Refresh`。
- 播放轻量 UI 反馈。
- 对外抛出按钮事件。

限制：

- 不创建完整节点树。
- 不加载硬编码资源。
- 不写复杂游戏业务。
- 不直接跳转具体界面，除非用户明确要求。
- 不把临时测试数据写死。

## 每文件单类规则

每个 `.cs` 文件只定义一个类。抽象类或接口除外。需要配置结构时，优先使用单独文件、集中 JSON 配置或 Unity 可序列化配置。

## UGUI 规则

- 所有 UGUI 文本显示必须使用旧版 `UnityEngine.UI.Text` 组件，不使用 `TextMeshProUGUI`、`TMP_Text` 或其他 TextMeshPro 组件。
- 所有可交互元素必须独立节点化。
- 按钮文字与按钮背景分离，除非用户明确要求静态贴图按钮。
- 资源路径、布局参数、按钮配置集中管理；不能把可调参数散落在 Controller 业务代码中。
- 只能加载 UI 资源整理员 `Final` 或等价正式资源集合，不能加载 `ReferenceOnly`、污染元素、未切素材合集或未审核候选资源。
- 不允许把整张效果图或任一全屏截图作为唯一背景；背景必须按资源核查交接包组合分层资源。
- Controller 只负责 UI 行为和事件转发，不写复杂业务逻辑。
- 未确认 Tween 库时，不强行引入第三方依赖。

## 推荐目录结构

```text
Assets/
  Game/
    UI/
      Common/
      PanelName/
        Prefabs/
        Sprites/
        Scripts/
        Editor/
        Configs/
```

项目内具体路径必须来自目标项目 wiki、项目适配层或用户确认，不能写入通用 AIGC。

## 验证清单

1. Unity 编译通过。
2. Editor 菜单能创建 Prefab。
3. Prefab 能生成到目标路径。
4. Prefab 无缺失 Sprite / Text / Button 引用。
5. Inspector 字段绑定完整。
6. Button 点击能触发 Controller 事件。
7. Controller 只暴露事件或接口，不包含业务跳转硬编码。
8. 关闭和销毁时没有残留 Tween。
9. 资源依赖表只包含 UI 开发者审核通过的正式资源集合。
10. 施工代码没有引用参考图、完整展示图、`ReferenceOnly`、未切素材合集或未审核元素资源。
