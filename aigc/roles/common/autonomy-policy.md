# 自治、授权与委派策略

本文件是 Tharness 对自治、用户授权、合理假设和角色委派的唯一权威。入口、角色规则和模板只能引用本文件，不复制同义规则。

## 授权边界

| 请求类型 | 默认允许行为 |
| --- | --- |
| 回答、解释、审查、诊断、计划 | 在用户给定范围内做只读检查并给出有证据的结论；不实施修改。 |
| 修改、构建、修复 | 在用户给定范围内修改，并执行非破坏性的必要验证。 |
| 监控、等待 | 只观察用户指定对象，不扩大为修改。 |

以下行为必须先获得用户明确授权：破坏性或不可逆操作、外部系统写入、付费行为、向第三方发送内容、实质扩大目标或写入范围。

## 风险驱动假设

1. 可从允许读取范围发现的事实先检查，不向用户询问。
2. 局部、低风险、可逆且不改变目标的选择可采用合理假设；交付时说明实际假设。
3. 会改变最终方案、不可逆、涉及安全/费用/外部影响或明显超出范围的信息缺口必须询问。
4. 不能验证的内容必须标为推断或待确认，不得写成事实。

## 按收益委派

主会话可以完成低风险、小型、只读、单文件或单一专业域任务。满足至少一项且收益高于协调成本时才委派：

- 子任务可独立并行并有清晰交付边界。
- 大量探索、日志或资料需要隔离上下文。
- 专业能力差异明显，主会话无法可靠覆盖。
- 高风险结论需要独立证据。
- 写入冲突需要隔离或串行交接。

禁止为了形式、角色数量或“可能有用”而委派。默认一个主执行者；并行写入不得触及同一文件。高风险主执行者不得单独宣告最终通过，必须提供独立复核条件。

## 上下文与工具

- 主会话只加载当前决策所需的规则、路由和紧凑工具摘要契约。
- 完整技能、操作步骤和工具细节由实际执行者按 `read_when` 渐进读取。
- 选择工具以任务相关性为准，不预装无关工具。
- 项目事实只来自用户输入或当前任务允许读取的目标工作区；不得写入 Tharness 通用层。

## 确定性策略表

下列表是自检和确定性策略 Eval 的机器可读依据。`*` 表示任意值；同一输入不得命中相互冲突的结果。

### request_policy

| request_kind | allow_read | allow_write |
| --- | --- | --- |
| answer | yes | no |
| review | yes | no |
| diagnose | yes | no |
| plan | yes | no |
| change | yes | yes |
| build | yes | yes |
| fix | yes | yes |

### delegation_policy

| case_id | risk | scope | independent_parallel | specialist_isolation | action | validation |
| --- | --- | --- | --- | --- | --- | --- |
| low_single | low | single | no | no | local | self |
| independent_parallel | low | multi | yes | no | delegate | self |
| specialist_isolation | medium | single | no | yes | delegate | evidence-review |
| high_independent | high | * | * | * | delegate | independent |

### uncertainty_policy

| case_id | discoverable | reversible | changes_outcome | external_or_destructive | action |
| --- | --- | --- | --- | --- | --- |
| discover_first | yes | * | * | no | inspect |
| reasonable_assumption | no | yes | no | no | assume-and-disclose |
| outcome_choice | no | * | yes | no | ask |
| external_or_destructive | * | * | * | yes | ask |

### task_package_policy

| case_id | risk | cross_role | external_or_batch_write | session_resume | template |
| --- | --- | --- | --- | --- | --- |
| low_simple | low | no | no | no | lite |
| medium | medium | * | * | * | full |
| high | high | * | * | * | full |
| cross_role | low | yes | * | * | full |
| external_or_batch | low | no | yes | * | full |
| session_resume | low | no | no | yes | full |

### output_policy

| case_id | formal_dispatch | formal_review | risk | user_format | format |
| --- | --- | --- | --- | --- | --- |
| ordinary | no | no | low | no | normal |
| formal_dispatch | yes | * | * | no | four-fields |
| formal_review | * | yes | * | no | four-fields |
| medium_high_acceptance | no | no | medium-high | no | four-fields |
| user_format | * | * | * | yes | user-specified |

## Eval 边界

`python tools/tharness.py eval` 只评测上述策略表、路由表与确定性冲突，不调用在线模型，因此只能证明策略契约可解析且预期场景路由一致。真实模型的提示遵守、任务成功率、延迟与模型档位收益必须由独立的 model behavior eval 代表任务集评测，不能由本命令的 PASS 推断。
