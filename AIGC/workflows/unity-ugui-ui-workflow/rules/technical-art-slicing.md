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

不要切与当前界面无关的素材。明确作为整图背景使用的图片不拆。只有最终效果图时，自动切片只能作为候选切片，不能默认交给程序使用。

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

不允许只看 `manifest.json` 就交付。

## 命名规则

- 自动切片名只能作为临时名。
- 最终资源名使用语义化英文。
- 按功能命名，不按切片序号命名。
- 按钮背景不要带文字，除非用户明确要求静态贴图文字。
- 状态图必须带状态后缀，例如 `_Normal`、`_Hover`、`_Pressed`、`_Disabled`。

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
| 是否估算 | 是 / 否 |
| 备注 | 是否需要手工清理、九宫格、校准 |

## 坐标转换

原图坐标系左上角为 `0,0`，x 向右，y 向下。UGUI 默认施工坐标系以 Canvas 中心为 `0,0`，x 向右，y 向上。

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

以上坐标是第一版施工值，必须经过 Unity 截图校准。

## 交付给 Unity 施工员

技术美术交付包至少包含：

1. 切片 PNG 文件夹。
2. `manifest.json`。
3. `preview_boxes.png` 审核结论。
4. 切片命名映射表。
5. 素材拼接还原文档。
6. Unity 导入设置。
7. 不可用切片与手工补切清单。

Unity 施工员只能使用技术美术标记为“可直接使用”的切片。
