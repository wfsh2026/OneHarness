# 实习版本功能分析员工具契约
遵守 `../../common/tool-contract.md`。
## tool: version-feature-scan
- tool_id: `version-feature-scan`
- purpose: 从 Git 历史和差异提取版本功能候选并生成审核产物。
- phase: 版本功能分析与确认后生成。
- preconditions: 仓库、版本范围、输出目录和确认阶段明确。
- inputs: Git 仓库、起止引用、扫描/生成参数。
- outputs: 审核目录、功能文档、结构化摘要与退出码。
- side_effects: dry-run 无；确认生成时写入授权输出目录。
- errors: 参数错误=2、证据/仓库错误=1，成功=0。
- retry_stop: 修正参数或证据范围后重试；未获确认不得进入生成阶段。
- evidence: 准确命令、版本范围、退出码与产物清单。
