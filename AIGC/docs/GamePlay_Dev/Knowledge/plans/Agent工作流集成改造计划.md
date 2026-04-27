# 制作文档 → Agent 工作流集成改造计划

## 问题陈述

当前 AIGC 框架的 Agent 工作流（DL/GPO/Ability/Scene）是为 **2 代 ECS 架构**设计的，GPO/Ability/Scene Agent 均只处理 `Biubiubiu2/` 代码。但香肠派对项目 **83% 的代码（10,856 文件）是 1 代 C/S/H Modules 架构**，这些代码的开发缺少对应的编码规范和工作流路由。

**目标**：让 DL 通过 system-map 正确路由到 1 代制作文档 + feature JSON，使 Agent 开发 1 代功能时有规范可依。

## 设计约束（用户已确认）

- GPO/Ability/Scene Agent = 2 代专属，**不修改**
- AIGC 框架多项目共享，**不修改共享文件**（rules/core-rules.md, workflow-dev.md 等）
- 新文件放在项目专属路径（`sausage-framework/`, `knowledge/`）
- DL 读 system-map → 一站式路由到制作文档 + feature JSON
- 意图识别合入 system-map，不再作为独立 skill

---

## 改造文件清单（3 个文件）

### T1：[[knowledge/system-map]]（✏️ 修改）

修复错误 + 新增代际路由节。

| 改动 | 位置 | 内容 |
|------|------|------|
| 修复 BombArea 描述 | §二 第42行 | 删除投掷物系统描述中的「轰炸区缩圈机制」 |
| 修复 BombArea 路由 | §三 第160行 | 轰炸区/BombArea 从投掷物系统移到模式系统 |
| 新增代际路由节 | §三ʼ 新增 | 「代际判断规则」— DL 判断 1代/2代 的决策逻辑 |
| 整合意图识别 | §三ʼ | 将 skill 决策树合入为标准检索流程 |
| 补充 1代规范加载 | §五 | 「涉及 1代 开发 → 额外加载 1代架构/core-rules.md」 |

### T2：[[sausage-core-rules]]（🆕 新建）

1 代 C/S/H Modules 编码规范（对标共享 core-rules.md 的 2 代 ECS 版本）。

```
§一 架构总览：C/S/H 三端 Modules 模式
§二 命名规范：Module/Buff/Proto/Stage/Partial 命名约定
§三 核心架构模式：四层架构/Factory/Component/Buff三端
§四 配置与资源：SO + Txt + Loaders 体系
§五 网络约定：Mirror/Proto/三端同步
§六 开发前必读：system-map + 制作文档 + feature JSON
```

### T3：`aigc/harness/rules/Workflow/workflow-dev-sausage.md`（🆕 新建）

香肠派对工作流扩展（基于共享 workflow-dev.md 增加 1 代路由步骤）。

```
§一 Phase 2 增补：代际判断
§二 Phase 4 增补：1代文档化（不走 codegen）
§三 Phase 6 增补：1代编码（DL 直接编码）
§四 制作文档 × feature JSON 索引
```

## 执行顺序

```
T1 system-map.md 修改（基础）→ T2 core-rules.md 新建 → T3 workflow-dev-project.md 新建
```

## 关键设计

- core-rules.md 的内容从 15 个制作文档提取共性，不发明新规则
- workflow-dev-project.md 是扩展不是替换
- 意图识别 skill 文件不删除（其他项目可能用）
- DL.md 是共享文件，通过 system-map 路由而非修改 DL 定义

## 已确认决策

- ✅ core-rules.md = 完整版（200+ 行含代码示例）
- ✅ DL.md 不修改（通过 system-map 路由）
- ✅ workflow-dev-sausage.md（非 project）
