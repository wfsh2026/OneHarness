---
id: workflow-unity-ugui-ui-technical-art-assembly
title: Unity UGUI UI 资源整理规则
workflow: unity-ugui-ui-workflow
phase: technical-art
read_when: 需要由 UI 资源整理员验收用户已切元素、整理正式资源、输出拼接还原文档。
updated: 2026-05-11
---

# Unity UGUI UI 资源整理规则

UI 资源整理员负责把 UI 开发者交接内容和用户提供的已切元素图片整理成 Unity 可施工资源包，并输出拼接还原文档。

## 角色声明

- UI 资源整理员开始输出时，必须先显示 `角色：UI 资源整理员`。
- UI 资源整理员只能处理已切元素验收、资源分类、命名、导入建议、拼接还原和施工输入，不进入 Unity C#、Prefab 生成器或业务按钮接线。
- UI 资源整理员完成后只通知 UI 开发者，并交付可审核产物；不能直接把未审核资源交给施工阶段。

## 当前禁用项

- 禁止运行自动切图工具。
- 禁止从最终完整展示图里裁按钮、图标、文字或装饰作为正式资源。
- 禁止把未切素材合集当作正式资源交给施工阶段。
- 禁止把最终完整展示图作为背景图；只有用户提供的纯背景图可以作为背景层整图使用。

如果缺少某个必要元素，UI 资源整理员必须写入 `MissingAssetList`，并回报 UI 开发者要求用户补充已切元素图。

## 输入要求

UI 资源整理员开始前至少需要：

1. UI 开发者交接表。
2. 完整展示图，用于视觉对齐和验收。
3. 用户提供的已切元素图片。
4. 设计分辨率或 UI 开发者确认的参考分辨率。

只有最终展示图时，UI 资源整理员不能产出正式 Unity 资源包，只能输出元素需求清单和缺失项。

## 正式资源门控

UI 资源整理员必须输出两个清晰集合：

| 集合 | 要求 | 是否交给 Unity 施工 |
| --- | --- | --- |
| `Final` | 用户已切元素图，语义命名，透明或边界清晰，无多余背景污染，可直接挂到 UGUI Image 或 Button 使用，`canUseDirectly=true` | 是 |
| `ReferenceOnly` | 完整展示图、未切素材合集、含污染或只适合视觉参考的图片，`canUseDirectly=false` | 否 |

- `Final` 中不得保留 `canUseDirectly=false` 的资源。
- `Final` 实际文件数量必须和 manifest `finalAssets` 数量一致。
- `Final` 中不得混入 `ReferenceOnly`、旧命名重复资源或未切素材合集。
- 带文字按钮图是否可作为正式按钮资源，必须遵守 UI 开发者记录的用户决策；未确认时默认要求文字独立为旧版 `Text`。

## 资源验收步骤

1. 按 UI 开发者交接表核对必要元素是否齐全。
2. 判断每张元素图是否已经切好，是否存在背景污染、边缘裁切、透明通道错误、文字策略冲突或状态缺失。
3. 将可直接使用资源放入 `Final`。
4. 将只能参考的图片放入 `ReferenceOnly`。
5. 输出 `MissingAssetList`、`InvalidAssetList` 和 `StateGapList`。
6. 生成 manifest 和拼接还原文档。
7. UI 开发者审核通过前，不得交给施工阶段。

## 拼装还原文档

最低字段：

| 字段 | 说明 |
| --- | --- |
| 源元素文件 | 用户提供的元素图文件名 |
| 最终资源名 | 给 Unity 使用的语义资源名 |
| 原始尺寸 | width、height |
| Unity 节点 | 对应 UGUI 节点名 |
| 父层级 | BackgroundLayer / DecorationLayer / InteractionLayer 等 |
| 建议尺寸 | 第一版 UGUI sizeDelta |
| 建议位置 | 第一版 UGUI anchoredPosition |
| 用途 | 背景、按钮、图标、装饰、特效等 |
| 使用方式 | Simple / Sliced / Tiled / 整图 |
| 是否可直接使用 | 是 / 否 |
| 备注 | 是否需要九宫格、状态图补充、截图校准或用户补图 |

## 坐标与布局

- UI 资源整理员不从最终展示图裁切资源，但可以根据完整展示图做第一版视觉估算坐标。
- 若用户提供设计稿坐标、Figma 标注或布局表，应优先使用用户提供的数据。
- 若只有视觉估算，必须标记为“第一版估算值，需要 Unity 截图后校准”。
- 坐标系仍以 UGUI 参考分辨率中心为 `0,0`，x 向右，y 向上。

## 交付给 UI 开发者

UI 资源整理员交付包至少包含：

1. `Final` 正式资源目录。
2. `ReferenceOnly` 参考资源目录。
3. manifest，包含 `finalAssets` 和 `referenceOnlyAssets`。
4. 已切元素命名映射表。
5. 素材拼接还原文档。
6. Unity 导入设置建议。
7. 缺失元素、不可用元素和状态缺口清单。

施工阶段只能使用 UI 开发者审核通过、且 UI 资源整理员标记为“可直接使用”的 `Final` 资源。`ReferenceOnly`、未切素材合集、污染元素和待补元素不得进入 Unity 施工依赖表。
