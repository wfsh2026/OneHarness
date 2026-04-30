---
id: workflow-development-wiki-sync
title: 开发 Wiki 同步规则
workflow: development
phase: wiki-sync
read_when: 需要沉淀开发知识、项目事实或运行记录。
updated: 2026-04-30
---

# 开发 Wiki 同步规则

## 结论

开发执行者只提交候选知识点。主程审核候选知识点后，调用通用 wiki 或项目 wiki 维护规则判断是否沉淀，并记录写入或不写入的具体理由。

## 候选知识点格式

候选知识点必须包含：

- 知识点。
- 类型：通用知识、项目知识、运行记录、临时过程或不确定。
- 来源任务和子任务。
- 证据：代码、验证记录、用户确认或策划案章节。
- 建议写入位置。
- 建议理由。
- 不写入风险。

使用 `../templates/wiki-candidate-review.md` 汇总主程审核结果。

## 写入通用架构 wiki

满足以下全部条件时，按 `../../../wiki/rules/building.md` 写入 `AIGC/wiki/architecture/`：

- 与具体项目无关。
- 可被多个项目复用为架构搭建知识。
- 有明确来源。
- 已在开发或验证中产生稳定结论。
- 低频变化。
- 能通过 `read_when` 精确检索。
- 已由主程说明跨项目复用理由。

## 写入目标项目 wiki

满足以下任一条件时，写入目标项目 wiki：

- 项目架构约束。
- 项目模块边界。
- 项目路径、配置或构建规则。
- 已确认技术决策。
- 后续开发会重复查询的稳定经验。
- 项目内游戏模块职责、接口契约、资源约定或验证流程。

目标项目 wiki 不存在时，先执行 `../../../projects/rules/project-wiki-bootstrap.md`。目标项目 wiki 已存在时，按 `../../../projects/rules/project-wiki-update.md` 更新。

## 写入运行记录

以下内容写入本次工作流运行记录：

- 本轮输入摘要。
- 实施过程摘要。
- 验证命令和结果。
- 临时失败尝试。
- 关键决策。
- 被否决方案。
- 经验教训。
- 未完成事项。

运行记录只能保存过程事实，不能替代项目决策或通用架构结论。

## 知识碎片提取

开发交付物包含以下内容时，优先按知识碎片提取：

| 内容 | 写入位置 |
| --- | --- |
| 可跨项目复用的架构结论 | `AIGC/wiki/architecture/` |
| 通用 wiki 检索、写入、健康检查规则 | `AIGC/wiki/rules/` |
| 目标项目技术决策 | 目标项目 wiki |
| 目标项目踩坑经验 | 目标项目 wiki 或运行记录 |
| 一次性调试过程 | 运行记录 |
| 无法确认稳定性的候选知识 | 不写入 wiki，保留不写入理由 |

通用架构页模板见 `../../../wiki/templates/architecture-card.md`。

## 审核流程

1. 子任务开发者提交候选知识点。
2. 主程检查来源、稳定性、复用范围和写入边界。
3. 通用知识候选按 `../../../wiki/rules/building.md` 判断。
4. 项目知识候选按 `../../../projects/rules/project-wiki-update.md` 判断。
5. 不满足写入条件时，记录“不写入”理由。
6. 写入后运行对应健康检查；无法写入时说明阻塞。

## 禁止

- 不允许把项目事实写入通用 wiki。
- 不允许把一次性调试过程写入 wiki。
- 不允许把未确认内容写成稳定架构结论。
- 不允许子任务开发者绕过主程审核直接写入正式 wiki。
- 不允许只写“建议沉淀”而不说明写入或不写入理由。

通用 wiki 创建规则见 `../../../wiki/rules/building.md`。项目事实边界见 `../../../projects/PROJECT_ADAPTER.md`。项目 wiki 检索规则见 `../../../projects/rules/project-wiki-retrieval.md`。Wiki 健康检查规则见 `../../../wiki/rules/health.md` 和 `../../../projects/rules/project-wiki-health.md`。
