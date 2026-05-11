# AIGC 变更记录

## 2.2.0

- 将 `unity-ugui-ui-workflow` 从默认三角色流水线瘦身为 `ui-programmer` 快速路径、`ui-asset-curator` 可选资源核查路径和独立施工路径。
- 新增 `context-isolation.md`，定义复杂 UI 的上下文隔离触发条件：大量已切元素、图片数量过多、长 manifest、`.cs` + Prefab 施工、多轮截图校准、长报告和长资源清单。
- 更新 UGUI 规则索引、UI 规划、资源整理、Unity 施工、截图校准和交付模板的角色命名，移除旧的 UI 策划 / 技术美术 / Unity 施工员默认三角色表述。
- 删除未被索引引用且已禁用的 `technical-art-slicing.md`，避免 OneHarness 自检失败。
- 版本级别为 minor，因为本次新增上下文隔离规则并调整 UGUI 工作流内部默认执行路径，不改变通用 AIGC 的项目事实写入边界。

## 2.1.0

- 新增 `unity-ugui-ui-workflow` 通用工作流，用于把 UI 截图、效果图或素材图转成 Unity UGUI 策划、技术美术拆解、Prefab 施工和截图校准交付物。
- 新增输入完整度、UI 策划、技术美术资源验收与拼装、Unity 施工和截图校准五个阶段规则，保留“信息不足只输出估算和待确认项”的边界。
- 将 Unity UI Auto Slicer v2 保留为历史归档并停用，当前工作流只接收用户提供的已切元素图片。
- 新增 UI 图转 UGUI 交付报告模板，覆盖三角色交接表、拼接还原文档、绑定字段表和截图校准反馈表。
- 更新工作流索引、能力索引和版本记录，使新能力可从 AIGC 入口检索。
- 版本级别为 minor，因为本次新增了通用工作流、规则、模板和工具目录，不改变现有默认写入边界。

## 2.0.0

- 将策划到开发的交接方式升级为项目 wiki 驱动：策划工作流输出目标项目 wiki 的 `design/` 页面，开发工作流只接收项目 wiki 策划页面或开发任务页入口。
- 将主程评审、开发任务拆解、子任务分配和接口契约写入目标项目 wiki 的 `development/` 分区，避免复制整份策划案或整份 wiki。
- 更新项目 wiki 结构、创建、检索和更新规则，新增 `design/` 与 `development/` 分区的路由。
- 新增通用架构 wiki 页面 `architecture-wiki-mediated-workflow-handoff`，沉淀项目 wiki 驱动的跨工作流交接模式。
- 更新开发执行工作流、主程规则、角色读取规则、质量门控和交付模板，使开发成员只读取项目 wiki 子任务页允许的入口。
- 明确运行过程、失败尝试、命令输出和候选知识审核过程写入运行记录或交付物，不写入项目 wiki 正文。
- 版本级别为 major，因为本次改变了通用工作流的写入边界和默认读取入口。

## 1.0.0

- 将开发执行工作流升级为主程调度制：主程负责用户沟通、任务拆解、模块分配、接口契约、集成验收和知识候选审核。
- 新增游戏开发角色路由规则，固定 UI、3C、场景、战斗、AI、玩法系统、工具、技术美术和 QA 验证角色。
- 要求每个开发子任务通过项目任务文档入口交给全新 SubAgent 或全新会话执行，降低上下文污染和无关读取。
- 新增子任务分配模板和 Wiki 候选审核模板，明确总策划案章节引用、允许读取入口、写入范围、接口契约和验证要求。
- 调整 Wiki 沉淀边界：开发者只提交候选知识点，主程审核后再调用通用 wiki 或项目 wiki 规则，并记录写入或不写入理由。
- 更新开发执行相关规则、Agent 定义和交付模板，使任务包、角色分配、验证、质量门控、问题路由和交付记录保持一致。

## 0.7.0

- 新增游戏策划方法卡体系，按来源、阶段和触发词组织策划提问、体验转译、系统机制、战斗手感、用户理解和原型验证。
- 新增 `game-design-methodology.md`，将游戏策划讨论固定为“问清楚 -> 拆体验 -> 建机制 -> 做反馈 -> 降低理解成本 -> 验证真实需求”。
- 新增游戏策划方案模板，要求输出玩家幻想、核心体验、玩法机制、反馈表现、理解成本和最小验证原型。
- 将书籍来源卡标记为 `pending-source`，等待合法来源材料校准，不保存书籍原文。
- 新增方法卡设计原理与维护规则，明确来源层、方法卡层、工作流层和项目层的更新边界。

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
