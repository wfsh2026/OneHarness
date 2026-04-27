# Feature 格式规范

> **版本**: v2.2 | **状态**: 强制执行
>
> 本文件定义 features/ 下所有 feature 文件的统一格式和颗粒度规则。
> **v2.0 起，feature 文件采用 MD 格式（frontmatter + 正文），取代 JSON 格式。**
> 迁移工具：`python3 aigc/harness/tools/wiki/features/migrate-json-to-md.py`

---

## 零、文件格式（v2.0 新增）

### 模板

```markdown
---
name: {kebab-case 唯一标识}
display_name: {人类可读名称}
category: {系统分类}
version: {语义版本号}
dependencies:
  - {依赖的 feature name}
uses:
  - {引用的 feature name}
---

# {display_name}

{功能描述，2-4 句话}

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Scripts/...` | 服务端 System |
| `Assets/Scripts/...` | 客户端 System |

## 配置文件

| 路径 |
|------|
| `Assets/Bundle/...` |

## 资源文件

| 路径 |
|------|
| `Assets/Bundle/...` |
```

### 字段说明

**frontmatter（YAML，工具解析用）：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | kebab-case，全局唯一 |
| `display_name` | string | ✅ | 中文优先 |
| `category` | string | ✅ | 系统分类（gpo/mode/ability/ugc/cross-cut/ui） |
| `version` | string | ✅ | semver 格式 |
| `dependencies` | string[] | ✅ | 空列表 `[]` 表示无依赖 |
| `uses` | string[] | ❌ | 代码引用关系 |

**正文（MD，人类阅读用）：**
- `# 标题` — display_name
- 描述段落 — 功能说明
- `## 代码文件` — 表格列出代码路径（必须精确到 .cs 文件）
- `## 配置文件` — 表格列出 config 路径（可选）
- `## 资源文件` — 表格列出 asset 路径（可选）

### 范例

```markdown
---
name: feiyu
display_name: FeiYu（飞鱼）
category: gpo
version: 1.0.0
dependencies:
  - gpo-base
---

# FeiYu（飞鱼）

飞鱼GPO单位，包含FeiYu/FeiShu/NvWu变体。

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Scripts/GamePlay/Server/AI/Systems/ServerAIFeiYuSystem.cs` | 服务端 System |
| `Assets/Scripts/GamePlay/Client/AI/Systems/ClientAIFeiYuSystem.cs` | 客户端 System |
| `Assets/Scripts/Template/gpo/GPOM_FeiYu.cs` | GPOM 模板数据 |

## 资源文件

| 路径 |
|------|
| `Assets/Bundle/GamePlay/AI/Client/FeiYu.prefab` |
| `Assets/Bundle/GamePlay/AI/Client/FeiShu.prefab` |
| `Assets/Bundle/GamePlay/AI/Client/NvWu.prefab` |
| `Assets/Bundle/GamePlay/AI/Server/FeiYuServer.prefab` |
```
| `dependencies` | string[] | ✅ | 空数组 `[]` 表示无依赖，值为其他 feature 的 `name` |
| `files` | object | ✅ | 必须包含 `code`、`config`、`asset`、`template` 四个子字段 |
| `notes` | string | ✅ | 纯文本，空字符串 `""` 若无补充 |

---

## 二、颗粒度规则（核心）

### 核心原则

> **1 个 feature.json = 1 个可独立识别和描述的功能单元**

### 判断标准（必须同时满足）

1. **有独立代码文件** — 至少有 1 个专属 .cs 文件
2. **有明确名称** — 在代码中有可搜索的类名/模块名
3. **有独立职责** — 能用 1-2 句话描述其功能，不与其他 feature 完全重叠

### files.code 路径精度规则

> **强制要求**：`files.code` 必须列出具体 `.cs` 文件路径，**禁止使用目录路径**。

原因：
- 精确路径使搜索和引用成为可能（AI Agent 可直接定位文件）
- 目录路径隐藏了实际代码组成，不利于依赖分析
- 已验证所有系统均可实现精确路径：Car 73、Mode 1032、Role 301、Buff 362

例外：`files.asset` 和 `files.config` 允许目录路径（资源文件数量可能极大且结构不固定）。

### 聚合 vs 拆分判断规则

> 三条判断标准确定"可以成为独立 feature"，但实际是否拆分还需结合以下规则：

**必须拆分（任一条满足即拆）：**

1. **有独立控制器类** — 实例拥有专属 `.cs` 控制器/System 类（不是仅继承基类无扩展）
2. **有独立技能/攻击逻辑** — 实例有专属的 Buff/Skill/攻击方式实现
3. **system-map §三 实例清单中需要独立条目** — 每个条目必须能精确指向一个 feature

**允许聚合（全部满足才可聚合）：**

1. **共享同一控制器类** — 所有实例共用同一个 `.cs` 控制器，无专属代码
2. **差异仅在数据层** — 区别仅在 SO 参数/配置表数值，无代码分支
3. **共享同一基类/设置类** — 例如同一个 `XXXCarSetting` 驱动多个载具实例

**聚合时的命名规则**：使用 `{系统}-{驱动器名}-family` 格式，如 `car-buggy-family`。

#### 示例

| 场景 | 判断 | 原因 |
|------|------|------|
| Jeep/Buggy/ArmoredBus 共享 BuggyCarController，仅 SO 不同 | ✅ 聚合为 `car-buggy-family` | 无独立代码，差异仅数据 |
| Dragon 有 `DragonControl.cs`，Peterosaur 有 `Peterosaur.cs` | ❌ 必须拆分 | 各自有独立控制器类 |
| 47 个射击武器共享 `WeaponControl.cs`，仅 SO 字段不同 | ✅ 聚合为 `weapon-shooting` | 无独立代码，差异仅配置 |
| ElasticWeapon 有 `ElasticWeapon.cs`，ZiZiBeng 有 `ZiZiBengControl.cs` | ❌ 必须拆分 | 各自有独立控制器类 |
| FightClose 框架 + ClothesPole/FlameSpear 各有独立类 | ❌ 框架与武器分离 | 框架是基础设施，武器是实例 |

### system-map 对齐约束

> **强制规则**：`system-map.md §三` 实例清单中的每个条目的 `feature` 列必须精确指向一个 feature wiki-link。
> - ❌ 禁止多个不同实例条目指向同一个聚合 feature（除非满足上述聚合条件）
> - ❌ 禁止 feature 列使用「同上」或空值
> - ✅ 聚合 feature 在 §三 中只占一行（列出家族名，不逐实例展开）

### 各系统颗粒度定义

| 系统 | 1 file = | 文件命名模式 | 示例 |
|------|----------|-------------|------|
| **Mode** | 1 个游戏模式（变体共享） | `mode-{模式名}.md` | `mode-golddash.md` |
| **Role** | 1 个功能子系统 | `role-{子系统名}.md` | `role-damage.md` |
| **Car** | 1 个控制器驱动家族（共享控制器可聚合）或 1 个有独立控制器的载具 | `car-{类型/家族}.md` | `car-buggy-family.md`（聚合）、`car-dragon.md`（独立） |
| **Buff** | 1 个 Buff 类型（BSO/BS/BSServer/BSClient 四文件） | `buff-{bs名-kebab}.md` | `buff-add-effect-obj.md` |
| **AI** | 1 个 AI 行为/框架 | `ai-{行为名}.md` | `ai-behavior.md` |
| **Weapon** | 1 个武器子系统框架 或 1 个有独立控制器的武器类型 | `weapon-{类型}.md` | `weapon-shooting.md`（聚合）、`weapon-elastic.md`（独立） |
| **IdCard** | 1 张身份卡 | `idcard-{名称}.md` | `idcard-hades.md` |
| **Item** | 1 个道具子系统 | `item-{类型}.md` | `item-consumable.md` |
| **框架** | 1 个系统的核心基础设施代码 | `{系统}-base.md` 或 `{系统}-framework.md` | `car-base.md`、`buff-framework.md` |

### BiuBiuBiu2 项目颗粒度定义

> **核心规则**：system-map §三 实例清单中的每个条目对应一个 feature.json。

| 系统 | 颗粒度 | 命名规则 | 目录 | 示例 |
|------|--------|---------|------|------|
| **GPO** | 每个 GpoTypeSet ID = 1 个 feature | `{gpo名}.json` | `features/gpo/` | `feiyu.json`、`tank.json` |
| **Mode** | 每个 ModeEnum = 1 个 feature（变体共享） | `mode-{模式名}.json` | `features/mode/` | `mode-explore.json`、`mode-vs-relife.json` |
| **AB** | 每个 AbilityM = 1 个 feature | `ab-{名称}.json` | `features/ability/ab/` | `ab-bullet.json`、`ab-bomb.json` |
| **AE** | 每个 AbilityM = 1 个 feature | `ae-{名称}.json` | `features/ability/ae/` | `ae-move-speed-rate.json` |
| **UGC** | 按架构层拆分 | `ugc-{层名}.json` | `features/ugc/` | `ugc-base.json`、`ugc-gpo.json` |
| **基础框架** | 每个系统的核心代码 = 1 个 base feature | `{系统}-base.json` | `features/{分类}/` | `gpo-base.json`、`mode-base.json` |
| **跨切面** | 被多系统共享的基础代码 | `{域名}.json` | `features/cross-cut/` | `network-base.json`、`template-data.json` |

**模式变体规则**：同一模式的变体（如 5V5 复活 / 5V5 无限火力）共享同一个 feature，因为代码相同只有数据配置不同。

### Buff 系统特殊说明

Buff 系统采用 BSO/BS/BSServer/BSClient 四文件架构，每个 Buff 类型由 4 个文件组成：

```
BSOXxx.cs     → Host/Modules/Buff/BuffScriptableObject/
BSXxx.cs      → Host/Modules/Buff/BuffSystem/
BSXxxServer.cs → Server/Modules/Buff/BuffSystem/
BSXxxClient.cs → Client/Modules/Buff/BuffSystem/
```

因此 1 个 Buff feature.json 对应 4 个代码文件，`files.code` 应列出这 4 个具体文件路径。

### 关联实例段落规范（v2.2 新增）

当一个功能 feature（mode/idcard 等）使用了大量 Buff 或其他系统的实例时，必须在该 feature 文件末尾追加「关联 Buff」段落，列出所有使用到的实例 wiki-link。

**格式**：

```markdown
## 关联 Buff

### {分类中文名}（{数量}）

| feature | 说明 |
|---------|------|
| [[buff-xxx]] | 描述 |
| [[buff-yyy]] | 描述 |
```

**规则**：

1. **功能专属 buff 必须挂到消费者 feature** — 如 `buff/golddash` 的 25 个 buff 必须出现在 `mode-golddash.md` 的「关联 Buff」段落
2. **通用 buff 挂到框架 feature** — 如 `buff/combat`、`buff/movement` 等通用分类挂到 `buff-framework.md`
3. **按分类子组组织** — 多个分类的 buff 按子标题分组（如 mode-pverogue 同时有 PVE/图腾/地牢三个分类）
4. **幂等注入** — 已有「关联 Buff」段落的 feature 不重复注入

**目的**：确保 Agent 从 system-map → 功能 feature → 具体 buff 的正向 2 跳可达链路。

---

## 三、文件组织结构

```
AIGC/knowledge/features/
├── gen1/                          ← 1 代架构
│   ├── buff/                      ← Buff 系统
│   │   ├── buff-framework.json    ← 框架（1 个）
│   │   ├── buff-add-effect-obj.json  ← 每个 Buff 1 个文件
│   │   ├── buff-down-hp.json
│   │   └── ...
│   ├── mode/                      ← 模式系统
│   ├── role/                      ← 角色系统
│   ├── car/                       ← 载具系统
│   └── ...
└── gen2/                          ← 2 代架构
    └── ...
```

---

## 四、category 命名规范

使用斜杠分级：`系统` 或 `系统/子类型`

### 强制规则

- **框架/基础文件**（`xxx-base.json` 或 `xxx-framework.json`）→ 仅系统名，如 `mode`、`role`、`car`、`buff`
- **非框架文件** → **必须**包含子类型，如 `mode/golddash`、`role/damage`、`car/robot`、`buff/combat`
- 子类型一般从 `name` 字段去掉系统前缀得到：`mode-golddash` → `mode/golddash`
- 特殊映射：`fly-vehicle` → `car/fly`（属于载具系统但 name 不以 car- 开头）

### Buff 系统 category 值

| category | 说明 | 示例 Buff |
|----------|------|----------|
| `buff` | 框架层 | buff-framework |
| `buff/combat` | 伤害/击退/爆炸 | buff-down-hp, buff-knockback |
| `buff/movement` | 冲刺/加速/位移 | buff-sprint, buff-speed-up |
| `buff/defense` | 护盾/减伤 | buff-shield, buff-add-hp |
| `buff/visual` | 特效/物体生成 | buff-add-effect-obj, buff-show-hp |
| `buff/item` | 道具/场景交互 | buff-props-trigger, buff-lobby-shoot |
| `buff/pve` | PVE 怪物专属 | buff-pve-xxx |
| `buff/mode/{模式名}` | 特定模式专属 | buff-golddash-xxx |
| `buff/role-skill` | 角色技能专属 | buff-ganda-xxx |

### 其他系统 category 值

| category | 说明 |
|----------|------|
| `mode` | 模式框架 |
| `mode/{模式名}` | 具体模式 |
| `role` | 角色框架 |
| `role/{子系统}` | 角色功能子系统 |
| `car` | 载具框架 |
| `car/{类型}` | 具体载具类型 |

---

## 五、notes 字段写作规范

`notes` 是**纯文本**，用于记录标准字段无法覆盖的补充信息。

### 通用推荐内容（按优先级）

1. **routing** — Buff 的端侧执行策略（如 `routing: Server+Client`）
2. **key_fields** — BSO 上的关键可配置字段列表（如 `key_fields: EffectSign, LifeTime, Range`）
3. **继承关系** — 继承自哪个基类（如 `继承自 BSDownHpObj`）
4. **架构说明** — 设计模式、特殊机制
5. **注意事项** — 已知 Bug、使用限制

### 各系统 notes 模板

#### Mode 系统

```
GameMode 枚举 {EnumName}={Value}. 共 {N} 文件. 三端分布: C={n1}/S={n2}/H={n3}. key_classes: {Manager, Data, Logic...}. 子目录: {Client: Logic(n), Stage(n); Server: ...}. {额外玩法说明}
```

示例：
```
GameMode 枚举 GoldDash=28. 共 264 文件. 三端分布: C=125/S=126/H=13. key_classes: ClientGoldDashData, ClientGoldDashMgr. 子目录: Client: Logic(65), Other(54), Stage(3); Server: Logic(76), Other(44), Stage(3). 含独立的撤离点、金库、AI 系统等复杂子模块
```

#### Buff 系统

```
routing: {Server|Client|Server+Client|Host}. key_fields: {Field1, Field2, ...}. {继承关系/补充说明}
```

#### Role 系统

```
{核心类名}是{功能描述}。{继承/依赖关系}。{三端分布说明}
```

#### Car 系统

```
{核心说明}。{MoveType 统计类型}。{使用限制或注意事项}
```

---

## 六、禁止行为

- ❌ **禁止** 在标准 9 字段之外添加额外字段（如 `buff_list`、`key_classes`、`directories`、`manufacturing_doc`）
- ❌ **禁止** 将多个独立功能单元合并到一个 feature（违反颗粒度规则）
- ❌ **禁止** 将有独立控制器类的实例聚合到 family feature 中（必须拆分为独立 feature）
- ❌ **禁止** 将框架代码和具体实例混在同一个 feature 中（框架单独一个 feature）
- ❌ **禁止** system-map §三 实例清单的 feature 列使用「同上」或空值（每行必须精确指向一个 feature）
- ❌ **禁止** 在 notes 中使用 JSON 格式（notes 是纯文本）
- ❌ **禁止** 遗漏任何标准字段（即使值为空数组或空字符串）
- ❌ **禁止** 使用 camelCase 或 PascalCase 作为 `name` 值（必须 kebab-case）
- ❌ **禁止** 在 `files.code` 中使用通配符（必须是具体文件路径）
- ❌ **禁止** 在 `files.code` 中使用目录路径（必须是 `.cs` 精确文件路径）
- ❌ **禁止** 非框架文件的 `category` 仅写系统名（如 `mode`），必须含子类型（如 `mode/golddash`）

> **关于 `manufacturing_doc`**：制作文档的关联由 `system-map.md §二` 统一管理（系统→制作文档映射），
> 不应在每个 feature.json 中重复声明。如需从 feature 找到对应制作文档，通过 `category` 字段查询 system-map 即可。

---

## 七、验证检查清单

创建或修改 feature.json 后，必须通过以下检查：

- [ ] JSON 语法有效（可被 `json.loads()` 解析）
- [ ] 包含且仅包含 9 个标准字段
- [ ] `files` 包含且仅包含 `code`、`config`、`asset`、`template` 四个子字段
- [ ] `name` 使用 kebab-case
- [ ] `architecture` 值为 `gen1` 或 `gen2`
- [ ] `files.code` 中的路径以 `Assets/` 开头
- [ ] `files.code` 全部为 `.cs` 文件路径（禁止目录路径）
- [ ] `dependencies` 中引用的 feature name 确实存在
- [ ] 文件名与 `name` 字段一致（`{name}.json`）
- [ ] 非框架文件的 `category` 包含 `/` 分隔的子类型
- [ ] `notes` 非空且 ≥20 字符（推荐 ≥50 字符）

---

## 八、变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2025-01 | 初始版本，定义 9 字段标准和 Buff 颗粒度规则 |
| v1.1 | 2025-01 | 新增：files.code 精确路径强制规则、category 子类型强制规则、各系统 notes 模板、禁止目录路径、验证清单扩展 |
| v1.2 | 2025-07 | 明确禁止 `manufacturing_doc` 字段（制作文档映射由 system-map.md §二 管理）；清理已有 JSON 中的违规字段 |
| v2.0 | 2025-07 | JSON → MD 格式迁移（YAML frontmatter + MD 正文）；文件扩展名 .json → .md |
| v2.1 | 2025-07 | 新增「聚合 vs 拆分判断规则」（独立控制器必须拆、共享控制器+仅数据差异可聚合）；新增 system-map 对齐约束（§三 feature 列禁止「同上」）；细化 Car/Weapon/IdCard/Item 颗粒度定义；新增禁止行为 3 条 |
| v2.2 | 2025-07 | 新增「关联实例段落规范」（消费者 feature 必须挂载功能专属 buff 的 wiki-link 列表），确保 system-map → 功能 → buff 正向可达 |
