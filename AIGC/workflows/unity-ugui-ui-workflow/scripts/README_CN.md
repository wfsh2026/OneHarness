# Unity UI Auto Slicer v2

这是 Unity UGUI UI 工作流内置的通用自动切图工具。

## 解决的问题

- 不依赖 OpenCV。
- 使用 Pillow 处理图片。
- 支持透明 PNG。
- 支持背景已经烘进图片里的素材图。
- 输出切片 PNG、`manifest.json` 和 `preview_boxes.png`。

## 使用方式

进入本目录后运行：

```powershell
.\Run_Slicer_PowerShell.ps1
```

或使用脚本默认参数处理一张图片：

```powershell
.\.venv\Scripts\python.exe .\unity_ui_auto_slicer.py "<source-image-path>"
```

如果虚拟环境不存在，先运行启动脚本，或手动创建环境并安装依赖：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 输出内容

```text
sliced_output/图片名_时间/
  slice_001_x_y_wxh.png
  manifest.json
  preview_boxes.png
```

`preview_boxes.png` 用来检查切图框是否正确。技术美术必须审核它，不能只看 `manifest.json`。

## Unity 导入建议

```text
Texture Type: Sprite (2D and UI)
Sprite Mode: Single
Mesh Type: Full Rect
Compression: None
Filter Mode: Bilinear
```

## 参数建议

- `group_gap`：一个按钮被切成多个小图时调大。
- `min_area`：小图标漏切时调小。
- `bg_threshold`：棋盘格或背景残留时略微调大。
- `padding`：发光、阴影或边缘装饰被切掉时调大。
