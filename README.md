# OneHarness

OneHarness 是一套低 token、目标驱动的通用 AIGC 工作流框架。

当前有效框架入口只在 `AIGC/` 下。默认从 `AIGC/INDEX.md` 开始读取，再按 `read_when` 命中最小文件集合。

## 默认读取

1. `AIGC/INDEX.md`
2. `AIGC/workflows/INDEX.md`
3. 命中工作流的 `WORKFLOW.md`
4. 命中工作流的 `rules/INDEX.md`
5. `AIGC/wiki/INDEX.md`
6. 需要目标项目事实时，读取 `AIGC/projects/INDEX.md` 和目标项目 wiki 入口

禁止为了保险读取全部 wiki、全部历史资料或全部运行记录。

## 主要入口

| 路径 | 用途 |
| --- | --- |
| `AIGC/INDEX.md` | 通用框架入口。 |
| `AIGC/workflows/INDEX.md` | 工作流选择入口。 |
| `AIGC/wiki/INDEX.md` | 通用架构 wiki 入口。 |
| `AIGC/projects/INDEX.md` | 目标项目适配和项目 wiki 规则入口。 |
| `AIGC/capabilities/INDEX.md` | 当前能力索引。 |

## 边界

- 通用 AIGC 只保存通用工作流、通用规则、通用 wiki 和项目适配模板。
- 具体项目事实、项目 wiki、项目决策和运行记录必须写入目标项目自己的适配层。
- 历史项目资料不得保留在主分支；需要追溯时从 Git 历史或独立归档仓库读取。
