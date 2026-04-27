# 代码生成工具 — ComponentGen 技术文档

> **文档版本**：v1.0
> **创建时间**：2026-04-05
> **负责 Agent**：Dev Lead (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：`代码生成工具开发计划.md`
> **状态**：✅ 已完成

---

## S-01 作者签署

Dev Lead (DL)，负责 component-gen.sh 的规格定义和开发。

## S-02 参考文档

| 类型 | 文档 | 用途 |
|------|------|------|
| **开发范例** | `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIFindTarget.cs` | Server AI Component 范例（ServerNetworkComponentBase） |
| **开发范例** | `Assets/Scripts/GamePlay/Client/AI/Components/ClientAIHelicopterMove.cs` | Client AI Component 范例 |
| **开发范例** | `Assets/Scripts/GamePlay/Server/Mode/Components/ServerJellyBeanMode.cs` | Server Mode Component 范例（ComponentBase） |
| **边界定义** | `Assets/Scripts/CoreGamePlay/ComponentBase.cs` | ComponentBase 基类定义（生命周期接口） |
| **边界定义** | `Assets/Scripts/CoreGamePlay/ServerNetworkComponentBase.cs` | ServerNetworkComponentBase 基类定义（含 SyncData） |
| **规则文件** | [[gpo-code]] | GPO/AI 组件开发规则 |
| **规则文件** | [[ability-code]] | Ability 组件开发规则 |
| **规则文件** | [[mode-code]] | Mode 组件开发规则 |

## S-03 功能需求

AI Agent 调用一条命令，即可获得一个带完整生命周期文档注释的 Component 模板文件，包含正确的基类选择、命名空间、系统引用和生命周期方法顺序，避免 AI 手动编写时常犯的基类错误和生命周期遗漏。

## S-04 功能定位

定义 component-gen.sh 的完整输入参数、模板结构和类型派生规则。本文档是编写脚本的唯一技术依据。解决的核心痛点：
1. **基类选择困惑**：5 种类型 × 2 侧 = 10 种组合，各有不同的基类和命名空间
2. **生命周期遗漏**：OnAwake/OnStart/OnClear/OnSetEntityObj/OnSetNetwork/SyncData 的正确配对和清理
3. **系统引用缺失**：AI/Ability/Weapon/Character 各有不同的 System 引用字段

## S-04.5 架构预分析

Component 是项目 ECS-like 架构的最小逻辑单元，挂载在 System 上。本工具**只生成单个 .cs 文件**，不做任何注册操作（组件由 System 的 `AddComponent<T>()` 动态挂载，无需静态注册）。

核心派生矩阵：

| Type × Side | 基类 | 命名空间 | 系统引用 |
|-------------|------|---------|---------|
| ai × server | ServerNetworkComponentBase | ServerGamePlay | S_AI_Base mAI |
| ai × client | ComponentBase | ClientGamePlay | C_AI_Base mAI |
| ability × server | ComponentBase（默认）/ ServerNetworkComponentBase（+sync） | ServerGamePlay | S_Ability_Base mAbility |
| ability × client | ComponentBase | ClientGamePlay | C_Ability_Base mAbility |
| weapon × server | ComponentBase（默认）/ ServerNetworkComponentBase（+sync） | ServerGamePlay | S_Weapon_Base mWeapon |
| weapon × client | ComponentBase | ClientGamePlay | C_Weapon_Base mWeapon |
| character × server | ServerNetworkComponentBase | ServerGamePlay | S_Character_Base mCharacter |
| character × client | ComponentBase | ClientGamePlay | C_Character_Base mCharacter |
| mode × server | ComponentBase（默认）/ ServerNetworkComponentBase（+sync） | ServerGamePlay | （无） |
| mode × client | ComponentBase | ClientGamePlay | （无） |

---

## S-05 文件清单

### 5.1 脚本创建的文件（1类）

```
Assets/Scripts/GamePlay/{Server|Client}/{AI|Ability|Weapon|Character|Mode}/Components/
└── {Name}.cs                              【新建】Component 模板文件
```

输出目录根据 `--type` + `--side` 自动选择：

| type | server 目录 | client 目录 |
|------|------------|-------------|
| ai | `Server/AI/Components` | `Client/AI/Components` |
| ability | `Server/Ability` | `Client/Ability` |
| weapon | `Server/Weapon` | `Client/Weapon` |
| character | `Server/Character` | `Client/Character` |
| mode | `Server/Mode/Components` | `Client/Mode/Components` |

### 5.2 脚本修改的文件

无 — component-gen.sh 不修改任何现有文件。组件注册由 System 代码中的 `AddComponent<T>()` 完成。

---

## S-06 脚本执行流程

```
component-gen.sh 接收命令行参数
    │
    ▼
[Step 1/2] 参数验证 & 配置确认
    │ 检查必须参数（--name, --side, --type）
    │ 验证 PascalCase 命名
    │ 推导基类 / 命名空间 / 输出路径
    │ 推导 HAS_NETWORK（auto: client=true, server=false）
    │ 检查文件不存在
    ▼
[Step 2/2] 生成组件文件
    │ 组装模板：
    │   ├── emit_header()        → 自动生成标记注释
    │   ├── emit_usings()        → using 引用
    │   ├── emit_class_doc()     → XML 文档注释
    │   ├── emit_dev_rules()     → 开发规则注释（5条）
    │   ├── emit_init_data()     → InitData 结构体（可选）
    │   ├── emit_private_fields() → 系统引用字段
    │   ├── emit_on_awake()      → ① OnAwake（初始化+Register）
    │   ├── emit_on_start()      → ② OnStart（1帧后+AddUpdate）
    │   ├── emit_on_clear()      → ③ OnClear（清理+Unregister）
    │   ├── emit_on_set_entity() → ④ OnSetEntityObj（可选）
    │   ├── emit_on_set_network()→ ⑤ OnSetNetwork（可选）
    │   ├── emit_sync_data()     → ⑥ SyncData（仅 server+sync）
    │   └── emit_on_update()     → ⑦ OnUpdate（可选）
    ▼
[日志] 写入 AIGC/temp/component-gen-{Name}-{timestamp}.log
    ▼ exit 0
```

## S-07 灰盒资源占位

N/A — 本工具为代码生成脚本，不涉及视觉对象。

## S-08 边界条件

### 依赖外部接口
- 无外部命令依赖（纯 bash echo/printf 生成）
- 项目根目录自动检测：向上遍历找 `Assets/` 目录

### 禁止做的事
- 禁止覆盖已存在的文件（文件存在时 exit 1）
- 禁止在客户端使用 `--has-sync`（自动忽略并警告）
- 禁止 `--name` 非 PascalCase 命名

### 功能标志默认值表

| 标志 | 默认值 | 说明 |
|------|--------|------|
| `--has-init-data` | false | 需显式启用 |
| `--has-update` | false | 需显式启用 |
| `--has-entity`（OnSetEntityObj） | **true** | 默认生成，`--no-entity` 关闭 |
| `--has-network`（OnSetNetwork） | **auto** | client=true, server=false |
| `--has-sync`（SyncData） | false | 仅 server 有效 |

### 基类选择规则

| 条件 | 基类 |
|------|------|
| type=ai, side=server | ServerNetworkComponentBase（固定） |
| type=character, side=server | ServerNetworkComponentBase（固定） |
| type=ability/weapon/mode, side=server, **无** --has-sync | ComponentBase |
| type=ability/weapon/mode, side=server, **有** --has-sync | ServerNetworkComponentBase |
| 所有 client | ComponentBase（固定） |

### 生命周期方法生成顺序

```
① OnAwake     — 初始化数据 + Register 事件 | 禁止: Dispatcher、AddUpdate
② OnStart     — OnAwake 后 1 帧 | 可 Dispatcher、AddUpdate
③ OnClear     — Unregister + RemoveUpdate + null 所有引用
④ OnSetEntityObj — SetEntity 后触发 | 获取 Transform 等引用（默认开）
⑤ OnSetNetwork  — 网络组件就绪 | AI/GPO 仅一次，Character 可多次
⑥ SyncData      — 玩家进入视野时同步当前状态（仅 server + ServerNetworkComponentBase）
⑦ OnUpdate      — 帧更新（需 AddUpdate/RemoveUpdate 配对）
```

### 内嵌开发规则注释（5条）

工具在每个生成的组件类开头注入以下规则提醒：
1. 非生命周期方法必须 `private`
2. 禁止 `AddComponent`
3. `Register` ↔ `Unregister` 配对
4. `AddUpdate` ↔ `RemoveUpdate` 配对
5. `OnClear` 清 null

---

## S-09 验收标准

- [x] **编译层**：component-gen.sh 生成的 .cs 文件可被 Unity 编译通过（无语法错误）
- [x] **基类层**：10 种 type×side 组合均选择正确的基类和命名空间
- [x] **生命周期层**：OnAwake/OnStart/OnClear 三个核心方法始终生成，配对关系正确（Register↔Unregister, AddUpdate↔RemoveUpdate）
- [x] **标志层**：5 个功能标志（init-data/update/entity/network/sync）独立控制，组合使用无冲突
- [x] **幂等层**：文件已存在时报错退出，不覆盖
- [x] **注释层**：生成的代码包含生命周期文档注释和开发规则提醒

---

## 附录：命令行参数规格

```bash
component-gen.sh \
  --name <PascalCase>            # 必填，组件名，如 ServerAICyberBubbleMove
  --side <server|client>         # 必填，服务端或客户端
  --type <ai|ability|weapon|character|mode>  # 必填，组件所属系统类型
  --has-init-data                # 可选，生成 InitData 结构体
  --has-update                   # 可选，生成 OnUpdate 方法
  --no-entity                    # 可选，不生成 OnSetEntityObj（默认生成）
  --has-network                  # 可选，强制生成 OnSetNetwork
  --no-network                   # 可选，不生成 OnSetNetwork
  --has-sync                     # 可选，生成 SyncData（仅 server）
  --desc <string>                # 可选，中文描述
  --dry-run                      # 可选，仅预览不写入
  --project-root <path>          # 可选，项目根目录
```

## 附录：生成示例

### Server AI 全功能组件

```bash
bash aigc/harness/tools/codegen/component-gen.sh \
  --name ServerAICyberBubbleMove --side server --type ai \
  --has-init-data --has-update --has-sync \
  --desc "赛博泡泡移动组件"
```

生成结果：
```csharp
// 基类: ServerNetworkComponentBase
// 系统引用: private S_AI_Base mAI;
// 含: InitData + OnAwake + OnStart + OnClear + OnSetEntityObj + OnSetNetwork + SyncData + OnUpdate
```

### Client Mode 标准组件

```bash
bash aigc/harness/tools/codegen/component-gen.sh \
  --name ClientModeLobbyTimer --side client --type mode \
  --has-init-data --has-update \
  --desc "大厅倒计时组件"
```

生成结果：
```csharp
// 基类: ComponentBase
// 无系统引用（mode 类型无 System 引用）
// 含: InitData + OnAwake + OnStart + OnClear + OnSetEntityObj + OnSetNetwork(auto) + OnUpdate
```

### Server Ability 最小组件

```bash
bash aigc/harness/tools/codegen/component-gen.sh \
  --name ServerAbilityFireBall --side server --type ability \
  --has-init-data --desc "火球术技能组件"
```

生成结果：
```csharp
// 基类: ComponentBase（无 --has-sync）
// 系统引用: private S_Ability_Base mAbility;
// 含: InitData + OnAwake + OnStart + OnClear + OnSetEntityObj
// 注释提醒: "如需处理断线重连: 改继承 ServerNetworkComponentBase + SyncData"
```
