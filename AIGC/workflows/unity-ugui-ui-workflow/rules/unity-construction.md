---
id: workflow-unity-ugui-ui-construction
title: Unity UGUI UI 施工规则
workflow: unity-ugui-ui-workflow
phase: construction
read_when: 需要生成 Unity UGUI Prefab 施工方案、Editor 创建脚本、Controller 或绑定表。
updated: 2026-05-08
---

# Unity UGUI UI 施工规则

Unity 施工员负责把 UI 策划和技术美术产物落地为 Unity 工程内容。

## 生成前条件

生成 Unity 代码前必须已经有：

- UI 策划输出。
- 技术美术拆解。
- UGUI 层级。
- RectTransform 布局表。
- 资源路径依赖表。
- 文本表。
- 按钮事件表。

缺失时先输出待确认项，不直接生成完整代码。

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

## 文件职责

### `CreateXXXPrefab.cs`

职责：

- 创建 Canvas、SafeArea 和 UI Layer。
- 创建 Image、Button、TMP_Text 等节点。
- 设置 RectTransform。
- 按资源路径加载 Sprite。
- 绑定 Button、Image、TMP_Text。
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

- 正式文本默认使用 `TextMeshProUGUI`，不使用 Unity 默认 `Text`。
- 所有可交互元素必须独立节点化。
- 按钮文字与按钮背景分离，除非用户明确要求静态贴图按钮。
- 资源路径、布局参数、按钮配置集中管理。
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
4. Prefab 无缺失 Sprite / TMP / Button 引用。
5. Inspector 字段绑定完整。
6. Button 点击能触发 Controller 事件。
7. Controller 只暴露事件或接口，不包含业务跳转硬编码。
8. 关闭和销毁时没有残留 Tween。
