# harness/rules/ 规则目录总索引

> 按功能分类管理所有规则文件。
> **各 Agent 必读文件清单见 `QualityGate/quality-gate.md`**，本文件只做文件导航。

---

## 全局强制规则（所有 Agent 每次必读）

| 文件 | 内容 |
|------|------|
| `safety-rules.md` | AI 禁止行为黑名单 + 架构级设计约束（最高优先级） |
| `system-map.md` | 系统地图 + 意图识别 + 检索指导（DL/GPO/Ability 每次启动必读） |
| `background-agent.md` | Background Agent 启动/记录/Prompt 模板规范（派发前必读） |
| `GamePlay_Dev/shader-code.md` | Shader 规范 + 美术占位规则（涉及视觉对象时必读） |
| `GamePlay_Dev/technical-doc-format.md` | 技术文档格式强制规范（编写技术文档时必读） |

---

## 流程与质量管控

| 文件 | 内容 |
|------|------|
| `QualityGate/quality-gate.md` | 文档门控参考手册：各 Agent 必读文件清单 + Round 0/1/2/3 触发条件 |
| `QualityGate/quality-gate-checklists.md` | 门控审核清单详细规则：R1/R2/R3 逐条规则 + 多文档审核规范 |
| `lessons-learned.md` | 开发复盘记录：历史坑点 + 问题路由表 |
| `session-guide.md` | session-state 记录规范：active.md + session-log.md 编写规则 + 时间戳格式 |

---

## Workflow/ 工作流文件

> 项目负责人根据用户意图选择对应工作流，详见 [[Project_Lead]] §五。

| 文件 | 适用场景 |
|------|---------|
| `Workflow/workflow-dev.md` | 游戏功能开发：需求分析 → 文档生成 → 代码开发 |
| `Workflow/workflow-project-ops.md` | 项目运维：切换分支、拉取代码（游戏项目仓库内触发）|
| `Workflow/workflow-framework.md` | Framework 管理：同步/迁移/版本发布（仅 aigc-framework 仓库）|
| `Workflow/workflow-env-setup.md` | 项目绑定：首次使用或路径变更时初始化 local-env.json（仅 aigc-framework 仓库）|
| `Workflow/workflow-discussion.md` | 轻量讨论：技术核对、方案讨论、规范确认等非开发类对话 |

---

## GamePlay_Dev/ 专项规则（按需加载）

> 详细场景索引见 `GamePlay_Dev/README.md`。

| 文件 | 适用场景 |
|------|---------|
| `GamePlay_Dev/core-rules.md` | 编码 Agent 核心规则（DL/GPO/Ability 每次必读）：开发前必问清单 + ECS规范 + Gameplay逻辑 + 网络RPC |
| `GamePlay_Dev/gpo-code.md` | 涉及新 GPO / SceneGPO 开发 |
| `GamePlay_Dev/gpo-code-scenegpo.md` | 涉及 SceneGPO（基地/可破坏掩体/触发区域/Buff刷新点）时补充读取 |
| `GamePlay_Dev/ugc-code.md` | **涉及 UGC 功能开发时必读**：边界规则 + 命名规范 + 目录映射 + ID 范围 + GPOM 格式（所有项目同步，仅 UGC 项目适用）|
| `GamePlay_Dev/ability-code.md` | 涉及 Ability / AE 开发 |
| `GamePlay_Dev/mode-code.md` | 涉及游戏模式开发（DL 按需） |
| `GamePlay_Dev/scene-code.md` | 涉及场景建设 |
| `GamePlay_Dev/camera-code.md` | 涉及镜头/辅助瞄准（DL 按需） |
| `GamePlay_Dev/weapon-code.md` | 涉及枪械开发（DL 按需） |
| `GamePlay_Dev/plan-doc.md` | 大型功能开发计划模式（DL 按需） |

---

## Gameplay_Designer/ 规则（扩展预留）

> 暂时为空，策划规则目前在 [[设计文档完整性思维框架]]。

---

## Skills 认知框架索引（harness/skills/）

> Skills 是 AI 的**思维方法论**，与 Rules（约束）互补。Rules 告诉 AI「什么能做什么不能做」，Skills 教 AI「怎么思考问题」。

### GamePlay_Dev/

| 目录 | Skill 文件 | 用途 | 来源 |
|------|-----------|------|------|
| `system_thinking/` | `核心循环完整性检查框架.md` | 验证功能的核心循环是否完整（8 要素 checklist） | core-rules.md §1.4-1.6 |
| `system_thinking/` | `系统交互链路思维模型.md` | Input→CMD→Server→RPC→Client 链路思维检查 | technical-doc-format.md §S-06 |
| `intent_recognition/` | `意图识别与系统归属思维框架.md` | 识别用户需求涉及哪个系统 + 加载对应文档 | system-map.md §三 |
| `problem_patterns/` | `开发问题模式识别框架.md` | 5 种常见问题模式分类 + 路由到正确规范 | lessons-learned.md |
| `code_review/` | `code_review.md` | 资深代码审查认知框架 | 原始 |

### Gameplay_Designer/

| Skill 文件 | 用途 |
|-----------|------|
| `主策划设计哲学-核心认知框架.md` | 设计决策的底层认知（好玩 vs 成立） |
| `主策划竞品分析能力-设计进化判断框架.md` | 竞品分析三轴定位（机制/价值/市场） |
| `游戏设计艺术-主策划核心技能.md` | 体验驱动设计（Schell 透镜方法论） |
| `设计文档完整性思维框架.md` | 策划案写作维度完整性检查 |
