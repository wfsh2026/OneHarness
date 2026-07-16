# 项目开发者工具契约

遵守 `../../common/tool-contract.md`。

## tool: project-inspection
- tool_id: `project-inspection`
- purpose: 定位目标项目结构、引用与约定。
- phase: 方案与实现前。
- preconditions: 任务已授权对应读取范围。
- inputs: 路径、符号或文本模式。
- outputs: 匹配文件、位置和引用证据。
- side_effects: 无。
- errors: 路径不存在、权限拒绝或无匹配。
- retry_stop: 仅在修正路径/模式后重试；连续无新证据时停止。
- evidence: 实际读取路径与关键匹配位置。

## tool: project-edit
- tool_id: `project-edit`
- purpose: 在授权范围内修改代码、配置或测试。
- phase: 实现。
- preconditions: 写入范围、完成条件与回滚方式明确。
- inputs: 目标文件、补丁和预期行为。
- outputs: 可审查差异。
- side_effects: 修改目标工作区文件。
- errors: 冲突、越界、编码或写入失败。
- retry_stop: 修正确定性冲突后可重试；范围不明或需扩权时停止。
- evidence: 文件差异与实际写入清单。

## tool: project-verify
- tool_id: `project-verify`
- purpose: 按风险验证实现。
- phase: 交付前。
- preconditions: 验证命令或检查方法在任务范围内可执行。
- inputs: 测试、静态检查或可复现步骤。
- outputs: 退出码、通过数量或失败证据。
- side_effects: 仅允许测试产生的临时输出。
- errors: 环境缺失、测试失败或结果不确定。
- retry_stop: 只在修复明确失败后重试；环境阻塞时停止并说明替代检查。
- evidence: 准确命令、退出码和结果摘要。

