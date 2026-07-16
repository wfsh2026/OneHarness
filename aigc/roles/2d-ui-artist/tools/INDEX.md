# 2D UI 绘图师工具契约
遵守 `../../common/tool-contract.md`。
## tool: ui-image-generation
- tool_id: `ui-image-generation`
- purpose: 生成或编辑 UI 位图资源。
- phase: 视觉方案确认后。
- preconditions: 规格、风格参考、输出目录和覆盖策略明确。
- inputs: 描述、参考图、尺寸、格式、透明度要求。
- outputs: 图片文件与异常清单。
- side_effects: 写入任务授权的图片目录。
- errors: 生成失败、规格不符或目标冲突。
- retry_stop: 有明确缺陷时有限重试；连续两次无改善或需扩范围时停止。
- evidence: 文件清单、尺寸/透明度检查和预览。
