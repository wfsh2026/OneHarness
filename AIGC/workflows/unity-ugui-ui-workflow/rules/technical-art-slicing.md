---
id: workflow-unity-ugui-ui-technical-art-slicing
title: Unity UGUI UI 技术美术切图规则
workflow: unity-ugui-ui-workflow
phase: technical-art
read_when: 需要拆分 UI 素材、运行切图工具、审核 preview 或输出拼接还原文档。
updated: 2026-05-08
---

# Unity UGUI UI 技术美术切图规则

技术美术负责把 UI 策划交接内容翻译成 Unity 可施工资源规范，并按当前界面需要拆分素材。

## 角色声明

- 技术美术开始输出时，必须先显示 `角色：技术美术`。
- 技术美术只能处理素材、切图、命名、导入建议、拼接还原和施工输入，不进入 Unity C#、Prefab 生成器或业务按钮接线。
- 技术美术完成后只通知 UI 策划，并交付可审核产物；不能直接把未审核资源交给 Unity 施工员。

## 切图工具

内置工具位于：

```text
AIGC/workflows/unity-ugui-ui-workflow/scripts/
  unity_ui_auto_slicer.py
  Run_Slicer_PowerShell.ps1
  Run_Slicer.cmd
  requirements.txt
  README_CN.md
```

工具输出：

```text
sliced_output/图片名_时间/
  slice_001_x_y_wxh.png
  manifest.json
  preview_boxes.png
```

## 使用前判断

只有以下条件同时满足时才执行切图：

1. 用户提供了原始 UI 图片或素材合集。
2. UI 策划已经明确哪些元素需要成为独立资源。
3. 技术美术能判断切片是否可直接用于 Unity。

不要切与当前界面无关的素材。明确作为整图背景使用的图片不拆。只有最终效果图时，自动切片默认只能作为候选切片；如果用户确认切片就是正式资源，技术美术必须把正式施工资源清理到可直接使用状态，再交给程序。

## 正式资源门控

当用户要求切图作为正式资源、或 Unity 施工员需要直接使用切图时，技术美术必须输出两个清晰集合：

| 集合 | 要求 | 是否交给 Unity 施工 |
| --- | --- | --- |
| `Final` | 语义命名、无文字污染、无 UI 残留、可直接挂到 UGUI Image 或 Button 使用，`canUseDirectly=true` | 是 |
| `ReferenceOnly` | 含标题、按钮文字、背景污染、只能用于构图参考或重绘依据，`canUseDirectly=false` | 否 |

- `Final` 中不得保留 `canUseDirectly=false` 的资源。
- 带文字按钮底板不得作为正式按钮图；按钮文字必须由 TMP 或独立文本节点生成，除非用户明确要求静态贴图文字。
- 自动切片含污染时，技术美术必须清理、重绘、程序化生成替代 PNG，或移入 `ReferenceOnly`。

## 正式资源清理规则

自动切片不能直接等同于正式资源。技术美术必须按以下步骤处理：

1. 审核切片是否完整。
2. 判断是否存在背景污染、文字污染、边缘裁切、透明通道错误。
3. 将可直接使用资源放入 `Final`。
4. 将只能参考的资源放入 `ReferenceOnly`。
5. 对需要人工补切或重绘的资源写入 `ManualFixList`。
6. UI 策划审核通过前，不得交给 Unity 施工员。

`ManualFixList` 至少包含：

| 资源 | 问题 | 处理方式 | 是否阻塞施工 |
| --- | --- | --- | --- |
| Button_Start | 带文字 | 需要无字按钮底板 | 是 |
| Icon_Wood | 边缘裁切 | 增加 padding 后重切 | 是 |

## 审核规则

技术美术必须审核 `preview_boxes.png`，并结合 `manifest.json` 输出结论：

| 结果 | 处理 |
| --- | --- |
| 切框正确 | 进入命名映射和拼接文档 |
| 漏切小元素 | 降低 `min_area` 后重切 |
| 一个资源被拆碎 | 增大 `group_gap` 后重切 |
| 边缘阴影被裁掉 | 增大 `padding` 后重切 |
| 背景残留明显 | 调整背景阈值或标记手工清理 |
| 误切大量无效块 | 标记不可用，不交给 Unity 施工 |

不允许只看 `manifest.json` 就交付。UI 策划审核前，技术美术必须明确 `Final` 数量、`ReferenceOnly` 数量、`Final` 中不可直接使用资源数量。

## 自动切图失败处理

当自动切图无法得到可用资源时，不得反复盲目重切。必须选择以下处理方式之一：

| 情况 | 处理方式 |
| --- | --- |
| 合集图背景复杂 | 标记为 ReferenceOnly，要求人工切图 |
| 按钮带文字 | 要求提供无字版本，或标记为静态贴图按钮 |
| 图标边缘发光被裁 | 提高 padding 后重切 |
| 多个小装饰被合并 | 降低 group_gap 后重切 |
| 一个完整按钮被拆碎 | 增大 group_gap 后重切 |

## 命名规则

- 自动切片名只能作为临时名。
- 最终资源名使用语义化英文。
- 按功能命名，不按切片序号命名。
- 按钮背景不要带文字，除非用户明确要求静态贴图文字。
- 状态图必须带状态后缀，例如 `_Normal`、`_Hover`、`_Pressed`、`_Disabled`。

## 背景资源规则

- 禁止把最终效果图、Unity 截图或带完整 UI 的合成图作为唯一背景。
- 如果用户提供的是纯背景图，例如不包含按钮、Logo、交互文字和动态 UI 的 `BG_MainMenu.png`，允许作为全屏背景层整图使用。
- 如果背景图需要视差、遮挡、动效、雾层或前景压暗，则技术美术再拆成远景、地面、前景、雾层、暗角等分层资源。
- 背景是否整图使用，必须在技术美术拼接还原文档里标注：`isPureBackground=true/false`。

## 拼接还原文档

最低字段：

| 字段 | 说明 |
| --- | --- |
| 自动切片文件 | 工具输出的原始文件名 |
| 最终资源名 | 给 Unity 使用的语义资源名 |
| 来源 bbox | x、y、width、height |
| 原图尺寸 | image_width、image_height |
| Unity 节点 | 对应 UGUI 节点名 |
| 父层级 | BackgroundLayer / DecorationLayer / InteractionLayer 等 |
| 建议尺寸 | 由 bbox 转换 |
| 建议位置 | 由 bbox 转换 |
| 用途 | 背景、按钮、图标、装饰、特效等 |
| 使用方式 | Simple / Sliced / 三段式 / 整图 |
| 是否可直接使用 | 是 / 否 |
| 备注 | 是否需要手工清理、九宫格、校准 |

## 坐标转换

- 原图坐标系左上角为 `0,0`，x 向右，y 向下。UGUI 默认施工坐标系以 Canvas 中心为 `0,0`，x 向右，y 向上。
- 锚点优先由视觉归属决定，而不是统一 Center。

若 Reference Resolution 等于原图尺寸：

```text
anchoredPosition.x = x + width / 2 - imageWidth / 2
anchoredPosition.y = imageHeight / 2 - (y + height / 2)
sizeDelta = width, height
```

若 Reference Resolution 不等于原图尺寸：

```text
scaleX = referenceWidth / imageWidth
scaleY = referenceHeight / imageHeight
anchoredPosition.x = (x + width / 2) * scaleX - referenceWidth / 2
anchoredPosition.y = referenceHeight / 2 - (y + height / 2) * scaleY
sizeDelta = width * scaleX, height * scaleY
```

以上坐标是第一版施工值，必须经过 Unity 截图校准,同时在像素级偏差表中记录偏差。

## 像素级偏差表

| 节点 | 目标中心 | 当前中心 | 中心偏差 | 目标尺寸 | 当前尺寸 | 尺寸偏差 | 建议修正 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logo | 836,210 | 836,232 | y +22 | 850x212 | 820x204 | -30,-8 | Y -22，W +30，H +8 |
| StartButton | 836,515 | 836,528 | y +13 | 560x90 | 530x82 | -30,-8 | Y -13，W +30，H +8 |

## 校准优先级

1. 先校准背景与主构图层。
2. 再校准 Logo。
3. 再校准主按钮组。
4. 再校准装饰图标。
5. 最后校准字体、阴影、透明度和动效。

## 交付给 Unity 施工员

技术美术交付包至少包含：

1. 切片 PNG 文件夹。
2. `manifest.json`。
3. `preview_boxes.png` 审核结论。
4. 切片命名映射表。
5. 素材拼接还原文档。
6. Unity 导入设置。
7. 不可用切片与手工补切清单。

Unity 施工员只能使用 UI 策划审核通过、且技术美术标记为“可直接使用”的切片。`ReferenceOnly`、污染裁剪、候选切片和待清理资源不得进入 Unity 施工依赖表。
