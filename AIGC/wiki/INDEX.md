# 通用 Wiki 入口

本 wiki 只服务通用工作流检索，不保存具体项目事实。

## 默认读取

| 文件 | read_when |
| --- | --- |
| `retrieval.md` | 需要降低 token 消耗或判断读取顺序。 |
| `reliability.md` | 需要判断知识是否可靠、能否升级为 accepted。 |
| `wiki-creation.md` | 需要创建或更新通用 AIGC wiki 知识卡片。 |
| `session-extraction.md` | 需要从会话、开发交付物或运行记录提取稳定知识。 |
| `wiki-health.md` | 需要检查 wiki 是否断链、孤岛、缺元数据或内容过时。 |
| `workflow-evolution.md` | 需要修改或演进通用工作流。 |
| `common/INDEX.md` | 需要查看通用知识分区。 |
| `common/candidates/INDEX.md` | 需要查看候选通用知识。 |
| `common/accepted/INDEX.md` | 需要查看已确认通用知识。 |
| `templates/INDEX.md` | 需要创建 wiki 页面、知识碎片或健康检查报告。 |

## 状态

- `candidate`：候选知识，不能直接当强规则。
- `accepted`：已确认知识，可作为通用规则。
- `deprecated`：废弃知识，仅保留追溯。
