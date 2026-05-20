# Tharness

Tharness 是一套低 token、目标驱动的通用 AIGC 工作流框架。

当前有效框架入口只在 `AIGC/` 下。默认从 `AIGC/INDEX.md` 开始读取，再按 `read_when` 命中最小文件集合。

## 默认读取

1. `AIGC/INDEX.md`
2. `AIGC/workflows/INDEX.md`
3. 命中工作流的 `WORKFLOW.md`
4. 命中工作流的 `rules/INDEX.md`
5. `AIGC/wiki/INDEX.md`
6. 需要目标项目事实时，读取 `AIGC/projects/INDEX.md`，再通过 `AIGC/_local/registry.yaml` 读取项目胶囊和项目 wiki 入口

禁止为了保险读取全部 wiki、全部历史资料或全部运行记录。

## 主要入口

| 路径 | 用途 |
| --- | --- |
| `AIGC/INDEX.md` | 通用框架入口。 |
| `AIGC/workflows/INDEX.md` | 工作流选择入口。 |
| `AIGC/wiki/INDEX.md` | 通用架构 wiki 入口。 |
| `AIGC/projects/INDEX.md` | 本机项目索引、项目胶囊和项目 wiki 规则入口。 |
| `AIGC/capabilities/INDEX.md` | 当前能力索引。 |

## 可执行自检

当前仓库提供最小自检工具，用于把部分规则从“依赖 Agent 自觉”推进到“项目自己发现问题”。

```powershell
python tools/tharness.py doctor
python tools/tharness.py index --check
python tools/tharness.py index --write
python tools/tharness.py self-check --path AIGC/wiki/architecture/entry-map.md --delivery
python tools/tharness.py gate
```

配置入口是 `AIGC/tharness.yaml`。动态检查范围、必需入口、元数据字段和门控扫描规则都从该配置读取。

AI 修改 Tharness 自身时，按 `AIGC/workflows/development/rules/self-check.md` 的触发矩阵自动选择自检命令；也可以用 `self-check --path ... --delivery` 让工具输出本轮应运行的命令。交付前必须运行 `python tools\tharness.py gate`。

## 边界

- 可提交的通用 AIGC 只保存通用工作流、通用规则、通用 wiki、项目接入机制和模板。
- 具体项目事实、项目 wiki、项目决策和运行记录必须写入被 Git 忽略的 `AIGC/_local/` 项目胶囊。
- 历史项目资料不得保留在主分支；需要追溯时从 Git 历史或独立归档仓库读取。
