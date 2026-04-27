# 代码生成工具 — GpomGen 技术文档

> **文档版本**：v1.0
> **创建时间**：2026-04-04
> **负责 Agent**：Dev Lead (DL)
> **Agent 定位**：[[Dev_Lead]]（已熟读）
> **父文档**：`代码生成工具开发计划.md`
> **状态**：⬜ 待开发

---

## S-01 作者签署

Dev Lead (DL)，负责 gpom-gen.sh 的规格定义。

## S-02 参考文档

| 类型 | 文档 | 用途 |
|------|------|------|
| **开发范例** | `Assets/Scripts/Template/gpo/GPOM_GoldenEgg.cs` | 简单 GPOM（12 基础字段） |
| **开发范例** | `Assets/Scripts/Template/gpo/GPOM_Helicopter.cs` | 复杂 GPOM（基础+战斗字段） |
| **边界定义** | `Assets/Scripts/Template/gpo/IGPOM.cs` | IGPOM 接口定义（12 基础字段） |
| **规则文件** | [[gpo-code]] | GPO 开发规则 |

## S-03 功能需求

AI Agent 调用一条命令生成独立的 GPOM 模板数据文件，包含 struct 定义和 Set 查询类。

## S-04 功能定位

定义 gpom-gen.sh 的输入参数、模板结构。用于独立创建 GPOM 数据文件（不含 System 和注册）。gpo-gen.sh 内部会调用此逻辑完成完整 GPO 创建。

## S-04.5 架构预分析

N/A（无新建 System/Component）。GPOM 是纯数据结构，由 struct + static Set 类组成。

---

## S-05 文件清单

### 5.1 脚本创建的文件（1类）

```
Assets/Scripts/Template/gpo/
└── GPOM_{Name}.cs                         【新建】GPOM struct + Set 类
```

---

## S-06 脚本执行流程

```
gpom-gen.sh 接收命令行参数
    │
    ▼
[验证阶段] 检查参数完整性 + 文件不存在
    │
    ▼
[创建阶段] heredoc 生成 GPOM_{Name}.cs
    │ - struct GPOM_{Name} : IGPOM（12 基础字段 + 自定义字段）
    │ - static class GPOM_{Name}Set（Data 数组 + GetGPOMByIdAndMatchMode 方法）
    ▼
[输出摘要] exit 0
```

## S-07 灰盒资源占位

N/A — 纯数据结构文件。

## S-08 边界条件

### IGPOM 12 个基础字段（必须包含）

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | int | 数据 ID |
| Name | string | 名称标识 |
| Sign | string | 唯一签名 |
| AssetSign | string | 资源标识 |
| GpoType | int | GPO 类型 |
| GpoTag | int | GPO 标签 |
| GpoDropId | int | 掉落 ID |
| GpoDropType | int | 掉落类型 |
| GpoSoConfig | string | SO 配置路径 |
| Hp | int | 生命值 |
| MatchMode | int | 匹配模式 |
| Quality | int | 品质 |

### 禁止做的事
- 禁止生成不含 12 个基础字段的 GPOM 文件
- 禁止自动填充 Data 数组条目（数据由用户/AI 后续填入）

---

## S-09 验收标准

- [ ] **编译层**：gpom-gen.sh 生成的 GPOM_{Name}.cs 可被 Unity 编译通过
- [ ] **结构层**：struct 实现 IGPOM 接口，包含完整 12 基础字段
- [ ] **Set 类**：包含 Data 数组（初始为空）+ GetGPOMByIdAndMatchMode 查询方法
- [ ] **幂等层**：文件已存在时报错退出

---

## 附录：命令行参数规格

```bash
gpom-gen.sh \
  --name <GpomName>              # 必填，如 LandMine
  --custom-fields <field_list>   # 可选，自定义字段，如 "Atk:int,ExplosionRadius:float"
  --project-root <path>          # 可选，项目根路径
```

## 附录：GPOM 文件结构模板

```csharp
// 基于 GPOM_GoldenEgg.cs / GPOM_Helicopter.cs 格式
namespace Sofunny.BiuBiuBiu2.Data {
    public struct GPOM_{Name} : IGPOM {
        // 12 基础字段
        public int Id { get; set; }
        public string Name { get; set; }
        // ... (省略，完整见 IGPOM.cs)
        
        // 自定义字段
        public int Atk;
        public float ExplosionRadius;
    }
    
    public static class GPOM_{Name}Set {
        public static GPOM_{Name}[] Data = new GPOM_{Name}[] {
            // 数据条目（初始为空，后续手动填入）
        };
        
        public static GPOM_{Name} GetGPOMByIdAndMatchMode(int id, int matchMode) {
            for (int i = 0; i < Data.Length; i++) {
                if (Data[i].Id == id && Data[i].MatchMode == matchMode) {
                    return Data[i];
                }
            }
            return default;
        }
    }
}
```
