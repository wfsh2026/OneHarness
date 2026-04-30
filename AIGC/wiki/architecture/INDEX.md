# 通用项目架构索引

默认只读本索引。按架构问题命中具体页面。

| id | read_when | 文件 |
| --- | --- | --- |
| `architecture-entry-map` | 需要为一个项目建立最小架构入口和检索路径。 | `entry-map.md` |
| `architecture-repository-structure` | 需要规划项目目录、文档、源码、配置和运行记录的分层。 | `repository-structure.md` |
| `architecture-module-boundaries` | 需要划分模块职责、所有权和禁止跨层修改范围。 | `module-boundaries.md` |
| `architecture-dependency-direction` | 需要判断模块依赖方向、反向依赖或循环依赖风险。 | `dependency-direction.md` |
| `architecture-configuration-surface` | 需要设计可配置参数、环境入口和禁止硬编码边界。 | `configuration-surface.md` |
| `architecture-workflow-routing` | 需要为任务选择工作流、阶段、规则索引和后续读取路径。 | `workflow-routing.md` |
| `architecture-capability-registry` | 需要设计能力入口、状态、版本和可检索维护规则。 | `capability-registry.md` |
| `architecture-project-adapter-layer` | 需要隔离通用框架与目标项目事实、运行记录和项目 wiki。 | `project-adapter-layer.md` |
| `architecture-knowledge-boundary` | 需要判断一条知识应该写入通用 wiki 还是项目适配层。 | `knowledge-boundary.md` |
| `architecture-wiki-mediated-workflow-handoff` | 需要设计策划、主程拆解、开发执行之间的低 token 交接方式。 | `wiki-mediated-workflow-handoff.md` |
| `architecture-verifiable-work-loop` | 需要把任务压缩成一个可验证的最小闭环。 | `verifiable-work-loop.md` |
| `architecture-knowledge-layering` | 需要拆分过大的规则、知识页、说明文档或能力入口。 | `knowledge-layering.md` |

## 写入规则

新增页面前先读 `../rules/building.md`，页面格式使用 `../templates/architecture-card.md`。
