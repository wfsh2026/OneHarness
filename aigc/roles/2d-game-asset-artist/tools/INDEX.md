# 2D 游戏资源绘制师工具契约
遵守 `../../common/tool-contract.md`。
## tool: game-asset-generation
- tool_id: `game-asset-generation`
- purpose: 生成或编辑非 UI 游戏位图资源。
- phase: 资源规格确认后。
- preconditions: 类型、风格、画布、透明度、命名和覆盖策略明确。
- inputs: 描述、参考图、尺寸、格式与资源清单。
- outputs: 图片文件、manifest 或异常清单。
- side_effects: 写入任务授权的资源目录。
- errors: 生成失败、语义/规格不符或目标冲突。
- retry_stop: 有可定位缺陷时有限重试；连续两次无改善时停止。
- evidence: 文件清单、规格检查与预览。
