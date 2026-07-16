# poe 小助手工具契约
遵守 `../../common/tool-contract.md`。
## tool: poe-evidence-inspection
- tool_id: `poe-evidence-inspection`
- purpose: 检查 POE 补丁、内容包、接口或本地实验所需证据。
- phase: 风险分析与方案形成前。
- preconditions: 游戏版本、来源、读取范围与风险目标明确。
- inputs: 文件、补丁说明、接口资料或用户提供证据。
- outputs: 已确认事实、风险、可逆实验建议。
- side_effects: 默认无；任何游戏包或账号写入须另行明确授权。
- errors: 版本不明、证据不足、加密/格式不支持或外部接口失败。
- retry_stop: 新证据出现后可重试；涉及账号、付费或不可逆写入时停止并询问。
- evidence: 来源、版本、校验结果和风险边界。
