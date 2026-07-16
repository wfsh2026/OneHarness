# UI 素材拆分师工具契约
遵守 `../../common/tool-contract.md`。
## tool: ui-asset-slicing
- tool_id: `ui-asset-slicing`
- purpose: 将正式 UI 稿重建拆分为可接入透明素材。
- phase: 已确认源图与拆分清单后。
- preconditions: 网格/九宫格、命名、状态变体和输出目录明确。
- inputs: 源图、区域清单、画布与缩放/偏移规则。
- outputs: 透明 PNG、预览、manifest 与接入说明。
- side_effects: 写入任务授权的素材目录。
- errors: 源图不足、切分污染、对齐失败或覆盖冲突。
- retry_stop: 修正坐标/规则后可重试；源证据不足或连续两次失败时停止。
- evidence: 黑白底预览、尺寸/透明度检查和 manifest。
