# Tharness 能力维护员工具契约
遵守 `../../common/tool-contract.md`。
## tool: tharness-check
- tool_id: `tharness-check`
- purpose: 执行结构、注册表、规则和边界自检。
- phase: Tharness 修改后与交付前。
- preconditions: 从仓库根目录使用可用 Python。
- inputs: `doctor`、`index --check`、`registry` 或 `check`。
- outputs: PASS/FAIL、错误、警告与统计。
- side_effects: 无（`index --write` 除外）。
- errors: 配置错误=2、自检失败=1、成功=0。
- retry_stop: 修复确定性错误后重试；环境缺失时停止并记录替代检查。
- evidence: 准确命令、退出码和错误/统计摘要。
## tool: tharness-eval
- tool_id: `tharness-eval`
- purpose: 运行与模型波动分离的确定性行为策略 Eval。
- phase: 自治、委派、输出、任务包、工具契约或路由修改后。
- preconditions: registry 与核心策略文件存在。
- inputs: `python tools/tharness.py eval`。
- outputs: 用例数量、PASS/FAIL 与失败说明。
- side_effects: 无。
- errors: 策略缺失或契约不一致时返回 1。
- retry_stop: 修复规则或注册信息后重试；不得通过放宽安全断言伪造通过。
- evidence: 命令、用例数量、退出码和失败项。
