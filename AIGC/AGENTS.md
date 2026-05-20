本目录继承仓库根目录 `AGENTS.md`。

补充规则：

- 可提交的 `AIGC/` 只保存通用工作流、规则、wiki、项目接入机制和模板。
- 具体项目事实、项目 wiki、项目决策和运行记录只能写入本机忽略目录 `AIGC/_local/` 下的项目胶囊。
- 需要目标项目事实时，先读取 `AIGC/projects/INDEX.md`，再读取 `AIGC/_local/registry.yaml` 指向的项目胶囊。
