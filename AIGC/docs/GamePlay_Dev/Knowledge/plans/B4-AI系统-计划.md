# B4 AI 系统 Knowledge 构建计划

> 批次：B4 | 系统：AI 系统 (RoleAI)
> 依赖文档：[[Gen1-knowledge构建技术方案]]
> 状态：🔄 补建中（feature.json 已完成，制作文档待产出）

---

## 一、目标

从 1 代代码中梳理 AI 系统的完整知识，产出 AI 行为树/状态机结构化数据 + 制作文档。

---

## 二、输入

| 输入 | 路径 | 说明 |
|------|------|------|
| Client 端代码 | `Assets/Script/GamePlay/Client/Modules/RoleAI/` | ~214 文件 |
| Server 端代码 | `Assets/Script/GamePlay/Server/Modules/RoleAI/` | ~108 文件 |
| Host 端代码 | `Assets/Script/GamePlay/Host/Modules/RoleAI/` | ~53 文件 |
| AutoWar 代码 | `Assets/Script/GamePlay/AutoWar/` | ~35 文件（自动战斗/回放） |
| resource-map §五 | [[resource-map]] | AI 资源索引 |

> ⚠️ **ADR#2 约束**：无 2 代 AI 文档可参考。1 代架构目录下无 AI 文档，本批次完全基于代码分析。

---

## 三、产出物

### 产出 1：system-map.md AI 系统条目（补完）

- 当前已有基础条目，需补充意图识别关键词指向 1 代制作文档

### 产出 2：AI 系统 feature.json（✅ 已完成）

已在 `aigc/wiki/raw/sausage-man/features/ai/` 创建 6 个功能包：
- `ai-base.json` — AI 基础框架
- `ai-behavior.json` — AI 行为树
- `ai-buff.json` — AI Buff 处理
- `ai-spawner.json` — AI 生成器
- `ai-teammate.json` — AI 队友
- `ai-navigation.json` — AI 导航

### 产出 3：1 代架构制作文档（❌ 待创建）

产出 [[AI制作]]，内容覆盖：

- 行为树节点如何编写（Action/Conditional 继承规则）
- 行为树 SO 配置如何关联 AI 角色
- AI 投放/生成策略（Spawner 机制）
- AI 参数调整入口
- AI 武器/时装配置

> 格式遵循 `aigc/docs/GamePlay_Dev/sausage-framework/README.md` 规范

### 产出 4：意图识别关键词（补充）

在 system-map.md §三 中补充 AI 系统关键词，指向 1 代制作文档。

---

## 四、执行步骤

| 步骤 | 内容 | 状态 |
|------|------|------|
| 1 | 扫描 C/S/H 三端 RoleAI/ 目录结构 | ✅ 已完成（feature.json 创建时） |
| 2 | 识别关键类型（行为树节点、AI Manager、Spawner） | ✅ 已完成 |
| 3 | 创建 feature.json | ✅ 6 个已创建 |
| 4 | 深入分析行为树创建流程 | 📋 待执行 |
| 5 | 分析 AI 投放/生成策略 | 📋 待执行 |
| 6 | 编写 AI制作.md | 📋 待执行 |
| 7 | 更新 system-map 意图识别 | 📋 待执行 |
| 8 | 用户审核 | 📋 待执行 |

---

*状态：🔄 补建中*
