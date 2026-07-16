# 实习功能案设计者工具契约
遵守 `../../common/tool-contract.md`。
## tool: feature-evidence-search
- tool_id: `feature-evidence-search`
- purpose: 检索功能案所需的项目事实与依赖证据。
- phase: 功能拆分前。
- preconditions: 已授权项目资料入口。
- inputs: 功能目标、路径和检索模式。
- outputs: 已确认事实、推断与待确认项。
- side_effects: 无。
- errors: 入口缺失、无匹配或证据冲突。
- retry_stop: 仅在调整检索条件后重试；无新证据时停止。
- evidence: 实际读取路径与引用位置。
