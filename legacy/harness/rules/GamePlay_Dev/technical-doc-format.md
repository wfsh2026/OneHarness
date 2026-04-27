# 技术文档格式规范 (technical-doc-format.md)

> **适用场景**：GPO 工程师、Ability 工程师、GP、场景建设工程师编写任何技术执行文档时，**必须绝对遵守本规范**。
> **[项目负责人]强制核查**：[项目负责人]在 Round 2（阶段4文档审核）和 Round 3（阶段6模块完成审核）中，必须逐项核对本清单，所有项通过才能放行。

---

## 零、[项目负责人]优先检查（S-01~S-09 布局概览）
| 编号       | 要素          | 说明                                             |
|----------|-------------|------------------------------------------------|
| **S-01** | 作者签署        | 一句话表明，谁做的？                                     |
| **S-02** | 参考文档        | 一句话：做这个之前参考了什么，看了什么规范，                         |
| **S-03** | 功能需求        | 一句话：玩家拿到这个单模块会有怎样的体验？                          |
| **S-04** | 功能定位        | 一句话：这份文档解决什么问题，职责边界在哪                          |
| **S-05** | 文件清单        | **目录树格式**：映射真实项目结构，每条目含操作标签（新建 / 修改 / 已有·调用）；新文件目录须与同类现有文件对应；System 文件名以 System 结尾 |
| **S-06** | ASCII 交互链路图 | 核心流程时序图；涉及玩家操作时必须覆盖 `输入→CMD→服务端→RPC→客户端表现` 全链路 |
| **S-07** | 灰盒资源占位    | 用什么样的临时表现来补充用户体验（**必须包含生成方式**）                 |

> 💡 **Skill 提取**：交互链路思维模型详见 [[系统交互链路思维模型]]
| **S-08** | 边界条件        | 依赖的外部接口 + 禁止做的事 + 边界定义文档引用                     |
| **S-09** | 验收标准        | ≥3 条可测试行为描述                                    |


**每份技术子文档的元信息 `>` 区块必须包含 `**Agent 定位**` 字段**，声明该 Agent 已读取自己的角色定义文件：

### 零.2 Agent 定位字段格式

```markdown
> **文档版本**：v1.0
> **创建时间**：2026-XX-XX
> **负责 Agent**：GPO 工程师
> **Agent 定位**：[[GPO_Programmer]]（已熟读）
> **父文档**：`xxx.md`
> **状态**：⬜ 待开发
```

**各 Agent 对应的定位文件：**

| Agent 角色 | 必须填写的定位文件路径 |
|-----------|---------------------|
| 开发负责人 (DL) | [[Dev_Lead]] |
| GPO 工程师 | [[GPO_Programmer]] |
| Ability 工程师 | [[Ability_Programmer]] |
| 场景建设工程师 | [[Scene_Builder]] |
| Gameplay Designer (GD) | [[GamePlay_Designer]] |
| [项目负责人] | [[quality-gate]] |
| 项目负责人 | [[Project_Lead]] |

> **[项目负责人]规则**：发现文档元信息中**缺少 `**Agent 定位**（已熟读）` 字段**，立即打回，无需继续审核其他项目。

---

## 一、文档九大要素（S-01 ~ S-09，缺一不可）

| 编号 | 要素 | 格式要求 | 详细规范 |
|------|------|---------|---------|
| **S-01** | **作者签署** | 元信息 `>` 区块：`**负责 Agent**：XXX` + `**Agent 定位**：\`...\`（已熟读）` | §零 |
| **S-02** | **参考文档** | 表格：三类条目（开发范例 / 边界定义 / 规则文件），缺类不可通过 | §三 |
| **S-03** | **功能需求** | 一句话描述：玩家拿到这个单模块会有怎样的体验？ | — |
| **S-04** | **功能定位** | 一句话描述：这份文档解决什么问题，职责边界在哪 | — |
| **S-04.5** | **架构预分析** | 写 S-05 之前必须完成的思考输出，见 §一.1 | §一.1 |
| **S-04.7** | **Codegen 工具预读清单** | 涉及 codegen 文件时，列出所有待用工具及其参数/OUTPUT FILES 读取状态 | §一.2 |
| **S-05** | **文件清单** | **目录树格式**：以项目真实目录结构呈现，每个文件条目标注 `【新建】`/`【修改】`/`【已有·调用】`；目录树之后必须紧跟「组件依赖明细」表格（涉及 System 时）；新文件目录须与同类现有文件一致；System 文件名以 `System` 结尾 | §二 |
| **S-06** | **ASCII 交互链路图** | 核心流程时序图；涉及玩家操作时覆盖 `输入→CMD→服务端→RPC→客户端表现` 完整链路 | — |
| **S-07** | **灰盒资源占位** | 每个新视觉对象：**生成方式**/形状/颜色（`_BaseColor RGBA`）/尺寸/挂点偏移，五项缺一退回（参考 `shader-code.md §六`） | §五、§六 |
| **S-08** | **边界条件** | 依赖的外部接口 + 禁止做的事 + 边界定义文档引用 | — |
| **S-09** | **验收标准** | `- [ ]` 清单，覆盖编译/运行时/功能三层，每条必须是可执行行为描述 | §四 |

> ⚠️ **两大高频漏项（Agent 必须在输出文档前逐项确认）**：
>
> **S-02 参考文档**（§三格式）：三类条目（开发范例 / 边界定义 / 规则文件）缺一退回，不接受含糊声明。
>
> **S-05 文件清单**（§二目录树格式）：必须用目录树呈现，每条目标注操作标签；只写路径不写标签直接退回。

---

## 一.1　S-04.5「架构预分析」格式规范

### 触发条件

凡文档涉及**新建 System 或 Component** 的，S-04.5 **必填**。  
纯配置类文档（仅追加 IdSet 常量 / ModeData 枚举 / CSV 行）可填 `N/A（无新建 System/Component）`。

### 格式要求

S-04.5 必须回答以下四个问题，**按顺序输出，不可跳过**：

```markdown
## S-04.5：架构预分析

### 需要哪些 System？

| System | 端 | 继承 | 核心职责（一句话） |
|--------|----|------|-----------------|
| XxxSystem_UGC | Server | S_AI_Base | 挂载行为组件，不含业务逻辑 |
| ... | | | |

### 每个 System 挂哪些 Component？

**XxxSystem_UGC**
- `XxxComponent_UGC`（新建）— 核心行为，做什么
- `ServerAIHurt`（PGC 默认，base.AddComponents 自动挂载）— 受伤扣血
- ...

### 每个 Component 的核心职责

| Component | 新建/复用 | 核心做什么 | 关键字段/依赖 |
|-----------|---------|-----------|-------------|
| `XxxComponent_UGC` | 新建 | 每帧做 X | InitData.Offset，_masterGPO |
| `ServerAIHurt` | 复用 PGC | 响应 Event_GPOHurt 扣血 | — |

### 依赖关系

- `XxxSystem_UGC` → 挂载 → `XxxComponent_UGC`（通过 InitData 传入偏移）
- `XxxComponent_UGC` → 监听 → `SE_AI.Event_GetMasterGPO`（获取主人 GPO）
- `XxxComponent_UGC` → 依赖 → `iGPO.SetPoint()`（框架接口）
```

### 门控规则

- **S-04.5 未填写 → S-05 不得开始输出**
- **S-04.7 Codegen 工具预读清单未填写 → S-05 不得开始输出**（涉及 codegen 生成文件时）
- [项目负责人] Round 审核时，S-04.5 与 S-05 文件清单必须互相对应：S-04.5 中列出的 System/Component 必须在 S-05 目录树中出现，不得有遗漏或多余

---

## 一.2　S-04.7「Codegen 工具预读清单」格式规范

### 触发条件

当技术文档涉及**任何需要 codegen 工具生成的文件**时（GPO/Component/Ability/Mode/Scene），必须在 S-05 之前输出 S-04.7。

### 格式要求

```markdown
## S-04.7：Codegen 工具预读清单

| # | 工具 | 用途 | 参数已读 | OUTPUT FILES 已读 |
|---|------|------|:--------:|:-----------------:|
| 1 | gpom-gen.sh | 生成 XXX GPOM 数据 | ✅ | ✅ |
| 2 | gpo-gen.sh | 注册 XXX GPO 类型（含 Graybox 参数） | ✅ | ✅ |
| 3 | component-gen.sh | 生成 XXX AI 组件（含 --template 模板参数） | ✅ | ✅ |
| 4 | mode-gen.sh | 生成 XXX 模式 | ✅ | ✅ |

> 工具路径：`aigc/harness/tools/codegen/{工具名}.sh`
> OUTPUT FILES 块位于各工具头部注释中
```

### 填写规则

1. **参数已读**：Agent 必须在写 S-04.7 前打开工具脚本头部，读取参数列表（必填/可选参数及默认值）
2. **OUTPUT FILES 已读**：Agent 必须读取 `# OUTPUT FILES` 注释块，确认该工具会创建/修改哪些文件
3. 两列全部 ✅ 后，S-05 中该工具相关的 CREATE/MODIFY 文件必须与 OUTPUT FILES 声明严格一致
4. 不涉及 codegen 的纯手写文件不需要在此表中列出

### 门控规则

- **涉及 codegen 文件但未填写 S-04.7 → S-05 不得开始输出**
- [项目负责人] Round 审核时，S-04.7 清单与 S-05 文件清单必须互相对应：S-04.7 中列出的工具 OUTPUT FILES 必须在 S-05 目录树中找到对应条目

---

## 二、S-05「文件清单」格式规范

### 2.1 呈现方式：项目目录树（强制）

**S-05 文件清单必须以「项目目录树」形式呈现**，直接映射项目真实目录结构，不得用纯表格列举替代。

目录树中每个文件条目必须在行尾标注操作类型标签，以及一句话说明其职责：

| 操作标签 | 含义 |
|---------|------|
| `【新建】` | 全新创建，项目中不存在的文件 |
| `【修改】` + 说明 | 已有文件，本次追加或变更，必须说明改了什么 |
| `【已有·调用】` | 已有文件，本次不改动，仅说明会调用它的哪个接口 |

### 2.2 目录树标准格式

目录树以项目根路径 `Assets/` 为起点，完整展示所有涉及文件的层级。**不涉及的兄弟目录用 `...` 省略**，涉及的目录必须完整展开到文件名。

```
Assets/
├── Scripts/
│   ├── Template/
│   │   └── gpo/
│   │       ├── IGPOM.cs                        【修改】switch 末尾追加 default 分支
│   │       └── GPOM_BIU26Set.cs                【新建】承载全部 5 个 BIU26 GPO struct
│   └── GamePlay/
│       └── Server/
│           └── AI/
│               ├── Systems/
│               │   └── ServerAIBIU26SpawnerSystem.cs   【新建】刷怪器服务端 GPO System
│               └── Components/
│                   └── ServerAIBIU26SpawnerAttack.cs   【新建】刷怪器攻击行为组件
└── Bundle/
    └── Configs/
        └── Gpo/
            └── Gpo.csv                         【修改】追加刷怪器数据行（csv-gen）
```

### 2.3 System 文件命名规则（强制）

凡 System 类文件（GPO System / Ability System），**文件名必须以 `System` 结尾**，与项目现有命名保持一致：

| 文件类型 | 已有范例 | 新文件正确写法 | 错误写法 |
|---------|---------|-------------|---------|
| GPO Server System | `ServerAIMachineGunSystem.cs` | `ServerAIBIU26SpawnerSystem.cs` | ❌ `ServerAIBIU26Spawner.cs` |
| GPO Client System | `ClientAIMachineGunSystem.cs` | `ClientAIBIU26SpawnerSystem.cs` | ❌ `ClientAIBIU26Spawner.cs` |
| SAB System | `SAB_BulletSystem.cs` | `SAB_BIU26LightningSystem.cs` | ❌ `SAB_BIU26Lightning.cs` |
| CAB System | `CAB_GrenadeSystem.cs` | `CAB_BIU26LightningSystem.cs` | ❌ `CAB_BIU26Lightning.cs` |
| Mode 组件 | `ServerModeMainLoop.cs` | `ServerBIU26MainLoop.cs` | — |

> 注：Mode 组件（`ComponentBase` 子类）不是 System，不加 System 后缀，直接描述功能命名。
> GPO 行为组件（`Components/` 目录下的逻辑组件）同理，无需 System 后缀。

### 2.4 新文件的目录必须与项目既有结构对应

新文件放置的目录层级，**必须与项目中同类型的现有文件所在目录保持一致**，不得新造目录层级或放错层。

检查方法：写文件路径前，先找一个同类型的现有文件，确认其所在目录，新文件放同一层：

| 新文件类型 | 找已有同类文件位置 | 新文件就放同一目录 |
|---------|---------------|---------------|
| Server GPO System | `GamePlay/Server/AI/Systems/ServerAIMachineGunSystem.cs` | → `GamePlay/Server/AI/Systems/` |
| Server GPO 行为组件 | `GamePlay/Server/AI/Components/Attack/ServerAIMachineGunAttack.cs` | → `GamePlay/Server/AI/Components/` 或对应子目录 |
| SAB System | `GamePlay/Server/Ability/System/SAB/SAB_BulletSystem.cs` | → `GamePlay/Server/Ability/System/SAB/` |
| CAB System | `GamePlay/Client/Ability/System/CAB/CAB_GrenadeSystem.cs` | → `GamePlay/Client/Ability/System/CAB/` |
| Mode 组件 | `GamePlay/Server/Mode/Components/MainLoop/ServerModeMainLoop.cs` | → `GamePlay/Server/Mode/Components/` 或对应子目录 |

> **特殊情况——跨目录模块**（如本项目有独立的 `UGC/` 目录）：新目录下的子层级结构必须完整映射主代码目录的层级，不得简化或跳层。
> 例：主代码 `GamePlay/Server/Ability/System/SAB/` → 对应目录下也必须是 `GamePlay/Server/Ability/System/SAB/`，不能写成 `GamePlay/Server/Ability/SAB/`。

### 2.5 禁止写法

- ❌ 只用表格列举文件路径，不展示目录层级关系
- ❌ 文件条目缺少操作标签（`【新建】` / `【修改】` / `【已有·调用】`）
- ❌ `【修改】` 后不写具体改了什么
- ❌ 新文件放入与项目现有同类文件不对应的目录（如 System 文件放进 `Components/`，SAB 文件缺少 `System/` 中间层）
- ❌ System 文件名不以 `System` 结尾
- ❌ 多个文件挤在同一行，不分行列出

---

### 2.6 组件依赖明细（强制子节，紧跟目录树之后）

**凡文档涉及 System 的，目录树之后必须紧接「组件依赖明细」表格**，每张表对应一个 System，列出该 System 挂载的所有组件。

**四列缺一退回：**

| 列 | 说明 |
|----|------|
| **对应组件** | 组件类名，精确到 `XxxComponent` |
| **来源** | `UGC 新建` / `PGC 默认（base.AddComponents 自动挂载）` / `PGC 复用（显式 AddComponent）` |
| **挂载方式** | `base.AddComponents()` / `AddComponent<X>()` / `AddComponent<X>(new X.InitData{...})` |
| **作用** | 一句话，说清楚这个组件在运行时做什么 |

**格式示例：**

```markdown
#### ServerAIFollowDroneSystem_UGC 组件依赖明细

| 对应组件 | 来源 | 挂载方式 | 作用 |
|---------|------|---------|------|
| `ServerAIAttribute` | PGC 复用 | `AddComponent<>(new InitData{ ATK=..., MaxHp=... })` | 初始化 GPO 属性数据（攻击力/血量/速度） |
| `ServerUAVMove` | PGC 复用 | `AddComponent<ServerUAVMove>()` | 每帧跟随主人玩家飞行 |
| `ServerAIDroneFollow_UGC` | UGC 新建 | `AddComponent<>(new InitData{ Offset=... })` | 控制跟随偏移位置，平滑插值到主人背后 |
| `ServerAIHurt` | PGC 默认 | `base.AddComponents()` 自动挂载 | 响应 Event_GPOHurt，执行扣血逻辑 |
```

> ⚠️ 父节点（System）必须单独一张表；若有多个 System，每个 System 各一张表，不得合并。

## 三、S-02「参考文档」格式规范

### 3.1 位置要求

必须放在文档顶部元信息 `>` 区块之后，**第一个 `---` 之后**，第一个正文章节之前。

### 3.2 格式要求

声明表必须包含**三类**条目（每类若无对应文档则写「暂无」）：开发范例、边界定义、规则文件。

```markdown
## 参考文档

| Agent 角色 | 类别 | 已读文件 | 路径 |
|-----------|------|---------|------|
| GPO 工程师 | 开发范例 | GPO 参考范例.md | [[GPO 参考范例]] |
| GPO 工程师 | 边界定义 | UGC GPO 内容边界定义.md | [[UGC GPO 内容边界定义]] |
| GPO 工程师 | 规则 | system-map.md | [[knowledge/system-map]] |
| GPO 工程师 | 规则 | safety-rules.md | [[safety-rules]] |
| GPO 工程师 | 规则 | core-rules.md | [[core-rules]] |
| GPO 工程师 | 规则 | shader-code.md | [[shader-code]] |
| GPO 工程师 | 规则 | technical-doc-format.md | [[technical-doc-format]] |
| GPO 工程师 | 规则 | gpo-code.md | [[gpo-code]] |
```

> **"暂无"写法**（该系统无开发范例或无边界定义时）：
> `| XXX 工程师 | 开发范例 | 暂无 | — |`

> **[项目负责人] S-02 核查重点**：检查声明表是否包含三类条目（开发范例行 / 边界定义行 / 规则行），且文件列表与 `technical-doc-format.md §3.3` 映射表完全对应。

### 3.3 各 Agent 必须声明的文件

| Agent | 文档类型 | 开发范例（声明表中必须有） | 边界定义（声明表中必须有） | 规则文件（声明表中必须有） |
|-------|---------|--------------------------|--------------------------|--------------------------|
| GPO 工程师 | 所有 GPO 技术文档 | **GPO 参考范例.md** | **UGC GPO 内容边界定义.md** | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **gpo-code.md** |
| GPO 工程师 | **UGC GPO 技术文档** | **GPO 参考范例.md** | **UGC GPO 内容边界定义.md** | 上述规则 + **ugc-code.md** |
| DL| **Mode 系统文档** | **模式参考范例.md** | **模式系统内容边界定义.md** | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **plan-doc.md** + **mode-code.md** |
| DL| **武器/枪械文档** | **枪械系统开发范例文档.md** | **枪械系统内容边界定义.md** | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **plan-doc.md** + **weapon-code.md** |
| DL| **3C/镜头文档** | 镜头系统开发范例文档.md（若有）或"暂无" | 3C/镜头系统内容边界定义.md | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **plan-doc.md** |
| DL| **Ability 相关文档** | **Ability 系统开发范例文档.md** | **Ability 系统内容边界定义.md** | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **plan-doc.md** + **ability-code.md** |
| DL| **UGC 相关文档** | 对应系统范例 | 对应系统边界定义 | 上述基础规则 + **ugc-code.md** |
| DL| 其他技术文档 | 对应系统范例（无则"暂无"） | 对应系统边界定义（无则"暂无"） | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **plan-doc.md** + 涉及领域规则 |
| Ability 工程师 | 所有 Ability 技术文档 | **Ability 系统开发范例文档.md** | **Ability 系统内容边界定义.md** | system-map.md + safety-rules + **core-rules.md** + **shader-code.md** + **technical-doc-format.md** + **ability-code.md** |
| Ability 工程师 | **UGC Ability 技术文档** | **Ability 系统开发范例文档.md** | **Ability 系统内容边界定义.md** | 上述规则 + **ugc-code.md** |
| 场景建设工程师 | 所有场景建设文档 | **场景建设-TankBattle.md** | 暂无 | system-map.md + safety-rules + **shader-code.md** + **technical-doc-format.md** + **scene-code.md** |

> **⚠️ [项目负责人]注意**：声明表缺少对应系统的开发范例或边界定义条目（包括"暂无"行）→ **立即退回**。若声明"暂无"但实际存在对应文件（见 [[quality-gate]]「当前可用资源清单」）→ 同样退回。

---

## 四、S-09「验收标准」格式规范

### 4.1 必须覆盖三个层面

```markdown
## N、验收标准

### N.1 编译验收
- [ ] 所有新建文件编译通过，无报错

### N.2 功能验收（运行时）
- [ ] 核心功能正常运行（具体描述预期行为）

### N.3 集成验收（与其他模块联动）
- [ ] 跨模块事件/消息正确传递
```

### 4.2 验收项必须是可执行的检查条目

- ✅ `- [ ] 击杀第8只小怪时，触发保底掉落（SpawnWeaponDrop 被调用，可通过日志确认）`
- ❌ `- [ ] 功能正常` （过于模糊，质检不通过）

---

## 五、场景建设文档额外要求（S-06 / S-07 扩展）

场景建设文档除上述规范外，**必须额外包含**：

### 5.1 场景层级结构 ASCII 树

```markdown
## N、场景层级结构

### 客户端场景结构（BIU26.unity）

BIU26 (Scene Root)
├── Environment/
│   ├── Terrain
│   ├── Props/
│   │   └── ...
├── Gameplay/
│   ├── SpawnPoints/
│   │   ├── SpawnPoint_01 (Position: 10, 0, 10)
│   │   └── ...
└── Lighting/
```

### 5.2 关键坐标表

对于出生点、边界围墙、区域中心等关键位置，必须列出具体世界坐标。

---

## 六、[项目负责人]专用检查清单（Round 2 / Round 3 必用）

[项目负责人]在执行 Round 2（阶段4文档审核）和 Round 3（阶段6模块审核）时，**必须逐项运行以下检查**：

```
【技术文档格式合规检查】
文档名：_______________
Agent：_______________

布局要素（对照 §一 S-01~S-09）：
S-01 作者签署（负责 Agent 字段 + Agent 定位字段）：✅ / ❌
S-02 参考文档（表格，含三类：开发范例 / 边界定义 / 规则文件）：✅ / ❌
S-03 功能需求（玩家体验一句话描述）：✅ / ❌
S-04 功能定位（职责边界一句话描述）：✅ / ❌
S-05 文件清单（目录树格式 + 每条目含操作标签）：✅ / ❌
S-06 ASCII 交互链路图（核心时序图，含完整操作链路）：✅ / ❌
S-07 灰盒资源占位（**生成方式**/形状/颜色/尺寸/挂点偏移 五项齐全）：✅ / ❌ / N/A（无新视觉对象）
S-08 边界条件（外部接口 + 禁止事项 + 边界文档引用）：✅ / ❌
S-09 验收标准（编译/运行时/功能三层，每条可执行行为描述）：✅ / ❌

S-05 文件清单专项核查（§二 规则）：
⑤-a 是否以目录树格式呈现（不是纯表格列举）：✅ / ❌
⑤-b 每个文件条目是否标注【新建】/【修改】/【已有·调用】：✅ / ❌
⑤-c 新文件目录是否与项目同类现有文件所在目录对应（§2.4 对应关系）：✅ / ❌
⑤-d System 文件名是否以 System 结尾（§2.3 命名规则）：✅ / ❌ / N/A
⑤-e ⚠️【重点】涉及 System 的文档，目录树之后是否紧跟组件依赖明细表格（§2.6）：✅ / ❌ / N/A
⑤-f ⚠️【重点】组件依赖明细四列（对应组件/来源/挂载方式/作用）是否全部填写，无空列：✅ / ❌
⑤-g ⚠️【重点】每个 System 是否各有独立的组件依赖明细表，父节点关联清晰，未合并：✅ / ❌

S-04.5 架构预分析核查（§一.1 规则）：
④.5-a 涉及新建 System/Component 的文档是否填写了 S-04.5：✅ / ❌ / N/A（纯配置类）
④.5-b S-04.5 中列出的 System/Component 是否全部出现在 S-05 目录树中：✅ / ❌
④.5-c S-04.5 四个问题（System列表/Component挂载/Component职责/依赖关系）是否全部回答：✅ / ❌

S-04.7 Codegen 工具预读清单核查（§一.2 规则）：
④.7-a 涉及 codegen 生成文件的文档是否填写了 S-04.7：✅ / ❌ / N/A（无 codegen 文件）
④.7-b S-04.7 中每个工具的「参数已读」和「OUTPUT FILES 已读」是否全部 ✅：✅ / ❌
④.7-c S-05 中 codegen 相关的 CREATE/MODIFY 文件是否与 S-04.7 工具的 OUTPUT FILES 声明一致：✅ / ❌

内容正确性：
⑩ S-02 参考文档是否与 §3.3「各 Agent 必须声明的文件」完全对应（不可模糊通过）：✅ / ❌
⑪ S-05 文件清单中不含已决策放弃的方案（无淘汰文件）：✅ / ❌
⑫ 无遗留 ⬜ 待确认决策项：✅ / ❌

合规结论：
- ❌ 存在以上任意项未通过 → 退回，要求 Agent 修复后重新提交
- ✅ 全部通过 → Round 通过，文档可呈现给用户
```



> **制定原因**：BIU26 Phase 1 阶段4文档生成过程中，发现 Mode系统.md 等文档存在格式不完整问题（缺签名区/验收标准/旧方案残留），导致需要 Round 2 多轮修复。
