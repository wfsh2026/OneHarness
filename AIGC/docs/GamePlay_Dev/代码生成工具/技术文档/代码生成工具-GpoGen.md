# 代码生成工具 — GpoGen 技术文档

> **文档版本**：v1.0
> **创建时间**：2026-04-04
> **负责 Agent**：GPO 工程师
> **Agent 定位**：[[GPO_Programmer]]（已熟读）
> **父文档**：`代码生成工具开发计划.md`
> **状态**：⬜ 待开发

---

## S-01 作者签署

GPO 工程师，负责 gpo-gen.sh 的模板规格定义。

## S-02 参考文档

| 类型 | 文档 | 用途 |
|------|------|------|
| **开发范例** | `Assets/Scripts/Template/gpo/GPOM_Helicopter.cs` | 完整 GPOM 范例（战斗型） |
| **开发范例** | `Assets/Scripts/Template/gpo/GPOM_GoldenEgg.cs` | 简单 GPOM 范例 |
| **开发范例** | `Assets/Scripts/GamePlay/Server/AI/ServerAIHelicopterSystem.cs` | Server AI System 范例 |
| **开发范例** | `Assets/Scripts/GamePlay/Client/AI/ClientAIHelicopterSystem.cs` | Client AI System 范例 |
| **边界定义** | `Assets/Scripts/Template/data/GpoType.cs` | GpoType 注册格式 |
| **边界定义** | `Assets/Scripts/Template/data/Gpo.cs` | Gpo 数据注册格式 |
| **边界定义** | `Assets/Scripts/Template/gpo/IGPOM.cs` | GPOM 路由注册格式 |
| **边界定义** | `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs` | Server AI 路由格式 |
| **边界定义** | `Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs` | Client AI 路由格式 |
| **规则文件** | [[gpo-code]] | GPO 开发规则 |

## S-03 功能需求

AI Agent 调用一条命令，即可获得新 GPO 类型的全部骨架代码（GPOM + Server/Client System）+ 所有注册，无遗漏。

## S-04 功能定位

定义 gpo-gen.sh 的完整输入参数、输出文件、模板结构和注册逻辑。本文档是编写脚本的唯一技术依据。

## S-04.5 架构预分析

GPO 系统的代码结构分三层：
1. **数据层**：GPOM_{Name}.cs（模板数据）+ GpoType.cs + Gpo.cs（类型/实例注册）
2. **服务端**：ServerAI{Name}System.cs（AI 行为 + 战斗逻辑）
3. **客户端**：ClientAI{Name}System.cs（表现 + 网络同步）

注册关系：GpoType → Gpo → IGPOM 路由 → ServerAIWorld_Switch → ClientAIWorld_Switch

---

## S-05 文件清单

### 5.1 脚本创建的文件（3类）

```
Assets/Scripts/Template/gpo/
└── GPOM_{Name}.cs                         【新建】GPOM 模板数据（struct + Set 类）

Assets/Scripts/GamePlay/Server/AI/
└── ServerAI{Name}System.cs                【新建】服务端 AI System

Assets/Scripts/GamePlay/Client/AI/
└── ClientAI{Name}System.cs                【新建】客户端 AI System
```

### 5.2 脚本修改的文件（5类）

```
Assets/Scripts/Template/data/
├── GpoType.cs                             【修改】添加 GpoType 常量 + Data 数组条目
└── Gpo.cs                                 【修改】添加 Gpo 常量 + Data 数组条目

Assets/Scripts/Template/gpo/
└── IGPOM.cs                               【修改】GetGPOMData switch 添加 case

Assets/Scripts/GamePlay/Server/AI/Components/
└── ServerAIWorld_Switch.cs                【修改】switch 添加 case（before default:）

Assets/Scripts/GamePlay/Client/AI/Component/
└── ClientAIWorld_Switch.cs                【修改】switch 添加 case（before default:）
```

---

## S-06 脚本执行流程

```
gpo-gen.sh 接收命令行参数
    │
    ▼
[验证阶段] 检查参数完整性 + 目标路径可写 + 文件不重复
    │ 失败 → 报错退出
    ▼
[GPOM 创建] heredoc 生成 GPOM_{Name}.cs
    │ struct: 12 base fields + custom fields
    │ Set class: Data array (空) + GetGPOMByIdAndMatchMode 方法
    ▼
[System 创建] heredoc 生成 Server/Client AI System
    │ 基于 template 参数选择模板（simple/combat/vehicle）
    ▼
[注册阶段] sed 修改 5 个现有文件
    │ GpoType.cs: const + Data 条目
    │ Gpo.cs: const + Data 条目
    │ IGPOM.cs: switch case
    │ ServerAIWorld_Switch.cs: switch case
    │ ClientAIWorld_Switch.cs: switch case
    ▼
[输出摘要] exit 0
```

## S-07 灰盒资源占位

N/A — 本工具为代码生成脚本，不涉及视觉对象。

## S-08 边界条件

### 依赖外部接口
- Mac BSD `sed -i ''`
- GpoType ID 和 Gpo ID 由用户指定（非自动递增，因为存在跳跃间隔）

### 禁止做的事
- 禁止自动分配 GpoType ID（ID 不连续，必须由用户指定）
- 禁止生成不含 12 个 IGPOM 基础字段的 GPOM 文件

### 模板类型差异

| 模板 | 特点 | Server System 额外组件 |
|------|------|----------------------|
| simple | 无攻击、无移动 | 基础生命周期 |
| combat | 有攻击 | ServerAIFindTarget, ServerAIFire 等 |
| vehicle | 有移动和状态机 | ServerNavMeshMove, ServerAIBehavior 等 |

---

## S-09 验收标准

- [ ] **编译层**：gpo-gen.sh 生成的所有 .cs 文件可被 Unity 编译通过
- [ ] **注册层**：GpoType/Gpo/IGPOM/ServerAIWorld_Switch/ClientAIWorld_Switch 5 个文件全部正确注册
- [ ] **结构层**：GPOM_{Name}.cs 包含完整的 12 个 IGPOM 基础字段 + 自定义字段
- [ ] **幂等层**：重复运行提示已存在并跳过
- [ ] **模板层**：simple/combat/vehicle 三种模板均能正确生成

---

## 附录：命令行参数规格

```bash
gpo-gen.sh \
  --name <GpoTypeName>           # 必填，如 LandMine
  --cn-name <中文名>              # 必填，如 "地雷"
  --gpo-type-id <int>            # 必填，GpoType ID（如 30）
  --gpo-id <int>                 # 必填，Gpo 数据 ID（如 3001）
  --template <simple|combat|vehicle> # 必填，System 模板类型
  --custom-fields <field_list>   # 可选，GPOM 自定义字段，如 "Atk:int,ExplosionRadius:float"
  --project-root <path>          # 可选，项目根路径
```
