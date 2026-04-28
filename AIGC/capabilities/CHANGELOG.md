# AIGC 变更记录

## 0.6.2

- 将 `tools/oneharness.py` 拆分为配置、Markdown、索引、检查和自检规划模块，降低单个 CLI 文件职责。
- 新增 `python tools\oneharness.py index --write`，按扫描结果写回 `AIGC/wiki/index.yaml` 的页面清单。
- 新增 `python tools\oneharness.py self-check --path ... --delivery`，按变更路径输出应运行的自检命令。
- 扩展 `AIGC/oneharness.yaml`，将自检路径规则和交付前命令移入配置。
- 将 wiki 元数据检查补齐到 `type` 和 `status` 字段，与 `AIGC/wiki/SCHEMA.md` 保持一致。

## 0.6.1

- 新增 `workflows/development/rules/self-check.md`，定义 OneHarness 自身改动的自检触发矩阵。
- 将 `self-check.md` 接入开发执行规则索引和最小门控配置。
- 更新开发执行工作流、质量门控规则和交付规则，要求交付前运行 `python tools\oneharness.py gate`。
- 更新开发交付模板，新增自检结果记录区域。

## 0.6.0

- 新增 `tools/oneharness.py` 最小自检 CLI，支持 `doctor`、`index --check` 和 `gate`。
- 新增 `AIGC/oneharness.yaml`，集中配置入口文件、wiki 索引、规则元数据和质量门控检查范围。
- 为 `workflows/**/rules/*.md` 补充最小 YAML 元数据，使工作流规则可被机器检查。
- 扩展 `AIGC/wiki/index.yaml`，加入显式页面清单，支持索引一致性校验。
- 新增 `tools/test_oneharness.py`，覆盖未知命令、缺失配置和当前仓库健康检查。

## 0.5.0

- 从历史资料中提炼通用质量门控能力，新增 `quality-gate` 规则。
- 从历史资料中提炼问题沉淀路由能力，新增 `issue-routing` 规则。
- 从历史资料中提炼低 token 知识分层能力，新增 `knowledge-layering` 架构页。
- 删除主分支历史隔离目录，避免全仓检索继续读取项目资料。

## 0.4.0

- 新增 `project-wiki-maintenance` 工作流，用于统一项目 wiki 搭建、检索、更新和健康检查入口。
- 修正根 README 的旧 wiki 路径，默认入口改为新版 `AIGC/INDEX.md`。
- 补充有效 AGENTS 规则，避免 `AIGC/AGENTS.md` 指向不存在的根文件。
- 明确一次性运行事实写入目标项目运行记录，不写入项目 wiki。

## 0.3.0

- 新增 `project-wiki-bootstrap` 能力，用于检索已有工程并主动搭建目标项目 wiki。
- 新增 `project-wiki-update` 能力，用于开发后更新目标项目 wiki。
- 补充项目 wiki 检索、健康检查、创建结构和页面模板规则。
- 明确通用 wiki 与项目 wiki 的调用边界：通用架构知识读 `AIGC/wiki`，项目事实读目标项目适配层 wiki。

## 0.2.0

- 废弃旧 wiki 搭建方式，不再保留 `raw/knowledge/log/html/common` 混合项目 wiki 结构。
- 新增通用架构 wiki，只保存跨项目可复用的项目架构搭建知识。
- 参考外部 harness 的 YAML 头、自描述索引和关联检索思路，但不迁入其项目内容。
- 移除已不存在的策划能力库候选入口。

## 0.1.1

- 整理当前 AIGC 系统版本说明。
- 在 `VERSION.md` 中补充当前版本功能清单、版本边界和验证结果。
- 在 `INDEX.md` 中补充当前系统版本和能力状态说明。
- 本次为 patch 级文档整理，不改变工作流行为。

## 0.1.0

- 新增 AIGC 能力索引。
- 新增 AIGC 能力版本记录。
- 新增 AIGC 能力演化工作流。
- 将外部 harness 分析、能力提取、能力索引更新和版本记录纳入同一条工作流。
- 在能力演化判断标准中加入：是否能拓展或补充现有能力、是否能用更少 token 完成功能开发、是否支持一次只做一件事。
