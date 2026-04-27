# 代码生成工具 — ModeGen 技术文档

> **文档版本**：v1.0
> **创建时间**：2026-04-05
> **负责 Agent**：Dev Lead (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：`代码生成工具开发计划.md`
> **状态**：✅ 已完成

---

## S-01 作者签署

Dev Lead (DL)，负责 mode-gen.sh 的规格定义和开发。

## S-02 参考文档

| 类型 | 文档 | 用途 |
|------|------|------|
| **开发范例** | `Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/ServerJellyBeanMode.cs` | Server Mode 范例 |
| **开发范例** | `Assets/Scripts/GamePlay/Client/Mode/Components/ClientJellyBeanMode.cs` | Client Mode 范例 |
| **边界定义** | `Assets/Scripts/Data/ModeData.cs` | ModeEnum + ModeData 注册格式（修改目标） |
| **边界定义** | `Assets/Scripts/GamePlay/Server/Mode/ServerModeSystem.cs` | Server Mode 路由 switch 格式 |
| **边界定义** | `Assets/Scripts/GamePlay/Client/Mode/ClientModeSystem.cs` | Client Mode 路由 switch 格式 |
| **规则文件** | [[mode-code]] | Mode 开发规则 |

## S-03 功能需求

AI Agent 调用一条命令，即可获得新游戏模式的全部骨架代码（Server/Client Mode 文件）+ 所有注册（ModeEnum 枚举、ID 常量、测试模式数据、匹配入口、Server/Client switch 路由），无遗漏。

## S-04 功能定位

定义 mode-gen.sh 的完整输入参数、输出文件、模板结构和注册逻辑。本文档是编写脚本的唯一技术依据。解决的核心痛点：Mode 注册分散在 ModeData.cs 的 4 个不同位置 + 2 个 System switch 文件，手动操作极易遗漏。

## S-04.5 架构预分析

Mode 系统的代码结构分三层：
1. **数据层**：ModeData.cs 中的 ModeEnum 枚举 + Id 常量 + AddTestMode() 数据块 + GetAllGameMatches() 匹配入口
2. **服务端**：Server{Name}Mode.cs（模式生命周期 + 回合逻辑 + 计分）
3. **客户端**：Client{Name}Mode.cs（UI 表现 + 结算弹窗）

注册关系：ModeEnum → Id 常量 → AddTestMode 数据 → GetAllGameMatches 入口 → ServerModeSystem switch → ClientModeSystem switch

---

## S-05 文件清单

### 5.1 脚本创建的文件（2类）

```
Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/
└── Server{Name}Mode.cs                    【新建】服务端模式逻辑（ComponentBase）

Assets/Scripts/GamePlay/Client/Mode/Components/
└── Client{Name}Mode.cs                    【新建】客户端模式逻辑（ComponentBase）
```

### 5.2 脚本修改的文件（3类，ModeData.cs 4 处修改）

```
Assets/Scripts/Data/
└── ModeData.cs                            【修改】4处：
                                             ① ModeEnum 枚举添加 Mode{Name} = {enumId}
                                             ② Id 常量添加 Id_{Name} = {modeId}（仅 test 类型）
                                             ③ AddTestMode() 数据块添加 Datas.Add(new Data {...})（仅 test 类型）
                                             ④ GetAllGameMatches() 添加 ModeMatch 入口

Assets/Scripts/GamePlay/Server/Mode/
└── ServerModeSystem.cs                    【修改】switch 添加 case（before default:）

Assets/Scripts/GamePlay/Client/Mode/
└── ClientModeSystem.cs                    【修改】switch 添加 case（before default:）
```

---

## S-06 脚本执行流程

```
mode-gen.sh 接收命令行参数
    │
    ▼
[验证阶段] 检查必须参数完整性 + 6 个文件/目录存在性
    │ 失败 → 报错退出（exit 1）
    ▼
[推导阶段] 根据 --pve/--pvp 推导：
    │ RoundWinState: PersonalScoreTop / TeamScoreTop
    │ ScoreChannel: KillRoleAI / KillRole / 空
    ▼
[Step 1] 创建 Server{Name}Mode.cs
    │ heredoc 模板：ComponentBase 基类
    │ 含 OnAwake/OnStart/OnClear/OnUpdate 生命周期
    │ 含 StartMode/GameState/GetStartPoint/AddCharacterFinish 事件注册
    ▼
[Step 2] 创建 Client{Name}Mode.cs
    │ heredoc 模板：ComponentBase 基类
    │ 含 SetGameState 事件监听 + 结算弹窗
    ▼
[Step 3] ModeData.cs — ModeEnum 枚举项
    │ 定位 ModeEnum 闭合括号 → 前插入 Mode{Name} = {enumId}
    ▼
[Step 4] ModeData.cs — Id 常量（仅 test 类型）
    │ 定位最后一个 Id_ 常量 → 后插入 Id_{Name} = {modeId}
    ▼
[Step 5] ModeData.cs — AddTestMode() 数据块（仅 test 类型）
    │ 定位方法闭合括号 → 前插入完整 Datas.Add(new Data {...})
    │ 含 ScoreChannelDatas 配置（PVE/PVP/无）
    ▼
[Step 6] ModeData.cs — GetAllGameMatches() 匹配入口
    │ 定位 return list; → 前插入 ModeMatch 条目
    ▼
[Step 7] ServerModeSystem.cs — switch case
    │ 定位 default: → 前插入 case Mode{Name}: AddComponent
    ▼
[Step 8] ClientModeSystem.cs — switch case
    │ 定位 default: → 前插入 case Mode{Name}: AddComponent
    ▼
[输出汇总] 列出创建/修改的文件列表
    │ 日志写入 AIGC/temp/mode-gen-{timestamp}.log
    ▼ exit 0
```

## S-07 灰盒资源占位

N/A — 本工具为代码生成脚本，不涉及视觉对象。

## S-08 边界条件

### 依赖外部接口
- Mac BSD `awk`：用于花括号深度定位（find_closing_brace）和行插入
- `grep -q`：幂等性检查
- `tee -a`：同时输出到终端和日志文件

### 禁止做的事
- 禁止覆盖已存在的 Mode 文件（幂等保护）
- 禁止同时使用 `--pve` 和 `--pvp`（互斥）
- 禁止在 normal 类型中生成 Id 常量和 AddTestMode 数据块（由线上数据管理）

### test vs normal 差异表

| 差异点 | test | normal |
|--------|------|--------|
| ModeEnum 枚举 | ✅ 生成 | ✅ 生成 |
| Id 常量 | ✅ 生成 | ❌ 跳过 |
| AddTestMode 数据块 | ✅ 生成（硬编码数据） | ❌ 跳过（线上数据） |
| GetAllGameMatches 入口 | ✅ 生成 | ✅ 生成 |
| Server/Client switch | ✅ 生成 | ✅ 生成 |

### PVE vs PVP 差异表

| 差异点 | PVE | PVP | 默认（无标志） |
|--------|-----|-----|--------------|
| RoundWinState | PersonalScoreTop | TeamScoreTop | PersonalScoreTop |
| ScoreChannel | KillRoleAI | KillRole | 空数组 |

### 插入定位策略

| 修改点 | 定位方式 | 插入位置 |
|--------|---------|---------|
| ModeEnum 枚举 | `find_closing_brace "public enum ModeEnum"` | 闭合 `}` 前 |
| Id 常量 | `insert_after_last "public const int Id_"` | 最后一个 Id_ 后 |
| AddTestMode 数据块 | `find_closing_brace "private static void AddTestMode"` | 方法闭合 `}` 前 |
| GetAllGameMatches 入口 | awk 定位方法内 `return list;` | return 前 |
| Server/Client switch | `insert_before "default:"` | default: 前 |

---

## S-09 验收标准

- [x] **编译层**：mode-gen.sh 生成的 Server/Client Mode .cs 文件可被 Unity 编译通过
- [x] **注册层**：ModeData.cs 4 处注册（ModeEnum + Id 常量 + AddTestMode + GetAllGameMatches）格式与现有条目一致
- [x] **路由层**：ServerModeSystem.cs + ClientModeSystem.cs switch case 正确注册
- [x] **幂等层**：重复运行相同参数，脚本提示已存在并跳过，不产生重复注册
- [x] **PVE/PVP 分支**：`--pve` 和 `--pvp` 标志正确影响 ScoreChannel 和 RoundWinState
- [x] **test/normal 分支**：test 类型生成完整注册，normal 类型跳过 Id 常量和 AddTestMode

---

## 附录：命令行参数规格

```bash
mode-gen.sh \
  --name <PascalCase>            # 必填，模式名，如 CyberBatteryTest
  --desc <string>                # 必填，中文描述，如 "赛博炮台PVE测试"
  --map-id <string>              # 必填，地图引用，如 "MapSet.Id_CyberBatteryTest"
  --map-sign <string>            # 必填，ModeMatch 地图标识
  --round-time <int>             # 可选，回合时间秒数（默认 300，-1=无限）
  --max-players <int>            # 可选，最大玩家数（默认 1）
  --type <test|normal>           # 可选，模式类型（默认 test）
  --pve                          # 可选，PVE 模式（KillRoleAI 计分）
  --pvp                          # 可选，PVP 模式（KillRole 计分，TeamScoreTop）
  --dry-run                      # 可选，仅预览不写入
  --project-root <path>          # 可选，项目根目录
  # enum-id / mode-id 由工具自动从 ModeData.cs 读取，无参数入口
```

## 附录：Server Mode 模板结构

```csharp
// Server{Name}Mode.cs 骨架
namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class Server{Name}Mode : ComponentBase {
        // 事件注册（OnAwake）
        Register<SE_Mode.Event_GameState>(OnGameStateCallBack);
        Register<SE_Mode.Event_AddCharacterFinish>(OnAddCharacterFinish);
        MsgRegister.Register<SM_Mode.StartMode>(OnStartModeCallBack);
        MsgRegister.Register<SM_Mode.GetStartPoint>(OnGetStartPointCallBack);

        // 生命周期
        OnStart → AddUpdate(OnUpdate)
        OnClear → 清理所有注册 + RemoveUpdate + null引用

        // 核心回调
        OnStartModeCallBack → 获取角色列表
        OnGameStateCallBack → RoundStart 回合开始
        OnGetStartPointCallBack → 出生点分配
        OnAddCharacterFinish → 武器装备
    }
}
```

## 附录：ModeData.cs 注册点示意

```csharp
// ① ModeEnum
public enum ModeEnum {
    // ...existing...
    Mode{Name} = {enumId},      // ← 工具插入
}

// ② Id 常量（仅 test）
public const int Id_{Name} = {modeId};  // ← 工具插入

// ③ AddTestMode() 数据块（仅 test）
private static void AddTestMode() {
    // ...existing...
    Datas.Add(new Data {         // ← 工具插入完整数据块
        Id = Id_{Name},
        Mode = ModeEnum.Mode{Name},
        ModeName = "{desc}",
        // ... 完整字段配置
    });
}

// ④ GetAllGameMatches()
public static List<ModeMatch> GetAllGameMatches() {
    // ...existing...
    list.Insert(list.Count, new ModeMatch(Id_{Name}, ...));  // ← 工具插入
    return list;
}
```
