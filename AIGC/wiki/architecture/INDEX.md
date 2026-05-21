# Tharness 通用架构索引

默认只读本索引。按架构问题命中具体页面。

| id | read_when | 文件 |
| --- | --- | --- |
| `architecture-role-system` | 需要理解 Tharness 角色体系、角色目录职责、技能工具归属或管理员调度边界。 | `role-system.md` |
| `architecture-role-dispatch-routing` | 需要为任务选择角色、派发方式、规则索引和后续读取路径。 | `role-dispatch-routing.md` |
| `architecture-capability-registry` | 需要设计能力入口、状态、版本和可检索维护规则。 | `capability-registry.md` |
| `architecture-project-adapter-layer` | 需要隔离可提交通用框架与目标项目事实、运行记录和项目知识。 | `project-adapter-layer.md` |
| `architecture-knowledge-boundary` | 需要判断一条知识应该写入通用 wiki 还是本机项目适配包。 | `knowledge-boundary.md` |
| `architecture-project-knowledge-handoff` | 需要设计策划、主程拆解、开发执行之间的低 token 交接方式。 | `project-knowledge-handoff.md` |
| `architecture-verifiable-work-loop` | 需要把任务压缩成一个可验证的最小闭环。 | `verifiable-work-loop.md` |
| `architecture-knowledge-layering` | 需要拆分过大的规则、知识页、说明文档或能力入口。 | `knowledge-layering.md` |

## 写入规则

新增页面前先读 `../rules/building.md`，页面格式使用 `../templates/architecture-card.md`。
