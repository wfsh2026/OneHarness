# wiki 管理员工具契约
遵守 `../../common/tool-contract.md`。
## tool: wiki-index
- tool_id: `wiki-index`
- purpose: 校验或更新通用 wiki 索引。
- phase: wiki 页面新增、移动或交付前。
- preconditions: 候选内容已通过通用性与边界判断。
- inputs: wiki 页面与 `AIGC/wiki/index.yaml`。
- outputs: 索引差异、扫描数量与错误列表。
- side_effects: check 无；write 仅修改 wiki 索引。
- errors: 元数据缺失、重复 id、页面缺失或边界违规。
- retry_stop: 修复确定性错误后重试；项目专属事实不得通过重试写入通用层。
- evidence: 命令、退出码、页面数和差异。
