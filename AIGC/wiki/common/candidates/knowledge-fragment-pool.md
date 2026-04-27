---
id: candidate-knowledge-fragment-pool
status: candidate
scope: 通用 AIGC wiki 检索和知识沉淀
source: source-legacy-harness-review
last_verified: 2026-04-25
read_when: 需要降低 wiki 检索成本、避免大文档膨胀、设计知识沉淀粒度
confidence: medium
---

# 知识碎片池

## 结论

当 wiki 内容增长后，知识的最小沉淀单位不应只有文件，也可以拆成“知识碎片”。

一条知识碎片只表达一个稳定认知，例如一个决策、一个教训、一个事实、一个被否决方案或一个意外发现。

## 适用范围

- wiki 文件变长，AI 为了找一个结论需要读取整篇文档。
- 开发交付物中经常出现可复用经验，但不适合直接变成完整页面。
- 需要保留“被否决方案”和“踩坑教训”，避免后续重复尝试。

## 建议元数据

- `id`
- `type`: `decision`、`lesson`、`fact`、`context`、`rejected`、`discovery`
- `tags`
- `source`
- `created`
- `last_verified`
- `last_used`
- `use_count`
- `superseded_by`

## 不适用场景

- 当前 wiki 规模很小，文件级卡片已经足够。
- 知识尚未验证，只能留在运行记录或候选区。
- 内容依赖单一项目事实。

## 来源

来自旧项目删除前审查中提取的可复用知识沉淀经验，详见来源索引。该设计中的“认知碎片、类型、来源、使用次数、取代关系”适合抽象为通用候选知识。
