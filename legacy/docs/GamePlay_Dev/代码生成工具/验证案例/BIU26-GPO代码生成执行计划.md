# BIU26-GPO 代码生成执行计划

> **来源需求**：[[BIU26-悬浮武器GPO]]
> **使用工具**：`gpom-gen.sh` + `gpo-gen.sh`
> **状态**：⏳ 待用户确认后执行

---

## 一、执行概览

| 步骤 | 工具 | 操作 | 产出 |
|------|------|------|------|
| 1 | `gpom-gen.sh` | 创建 GPOM 模板数据 | `GPOM_BIU26FloatingWeapon.cs` |
| 2 | `gpo-gen.sh` | 创建 Server/Client System + 注册 | 2 文件新建 + 4 文件修改 |
| 3 | 手动编码 | 自定义组件（非工具范围） | 2 自定义组件文件 |

---

## 二、Step 1 — gpom-gen.sh 执行

### 命令

```bash
gpom-gen.sh \
  --name BIU26FloatingWeapon \
  --display-name "悬浮武器" \
  --custom-fields "Atk:int,AttackIntervalTime:float,AttackRange:float,Hp:int,MaxAttackDistance:float" \
  --project-root <项目根目录>
```

### 参数说明

| 参数 | 值 | 来源 |
|------|-----|------|
| `--name` | `BIU26FloatingWeapon` | GPO 技术文档 S-01 |
| `--display-name` | `"悬浮武器"` | GPO 技术文档 S-01 |
| `--custom-fields` | `Atk:int,AttackIntervalTime:float,AttackRange:float,Hp:int,MaxAttackDistance:float` | GPO 技术文档 S-08 §8.1 |

> **注意**：Quality 已在基础字段中（`byte` 类型），无需重复指定。
> **基础字段（自动包含）**：AssetSign, GpoDropId, GpoDropType, GpoSoConfig, GpoTag, GpoType, Id, MatchMode, Name, Quality, Sign

### 预期产出

**新建文件**：`Assets/Scripts/Template/gpo/GPOM_BIU26FloatingWeapon.cs`

```csharp
// 预期生成的 struct 字段（基础 11 + 自定义 5 = 16 字段）
public struct GPOM_BIU26FloatingWeapon : IGPOM {
    public string AssetSign;
    public int Atk;                    // ← 自定义
    public float AttackIntervalTime;   // ← 自定义
    public float AttackRange;          // ← 自定义
    public int[] GpoDropId;
    public ushort GpoDropType;
    public string GpoSoConfig;
    public int[] GpoTag;
    public int GpoType;
    public int Hp;                     // ← 自定义
    public int Id;
    public int MatchMode;
    public float MaxAttackDistance;     // ← 自定义
    public string Name;
    public byte Quality;
    public string Sign;
    // ... IGPOM 接口实现 + 构造函数
}

public class GPOM_BIU26FloatingWeaponSet {
    public const int Id_BIU26FloatingWeapon = 1;
    public const string Sign_BIU26FloatingWeapon = "BIU26FloatingWeapon";
    public static GPOM_BIU26FloatingWeapon[] Data;
    // GetGPOMByIdAndMatchMode()
}
```

### GPOM 字段与需求对应

| 需求字段 (S-08 §8.1) | GPOM 字段 | 类型 | 建议默认值 |
|----------------------|-----------|------|-----------|
| Id | `Id` (基础) | int | 自动分配 |
| Sign | `Sign` (基础) | string | "BIU26FloatingWeapon" |
| Atk | `Atk` (自定义) | int | 300 |
| AttackRange | `AttackRange` (自定义) | float | 15f |
| AttackIntervalTime | `AttackIntervalTime` (自定义) | float | 1.5f |
| MaxAttackDistance | `MaxAttackDistance` (自定义) | float | 15f |
| Quality | `Quality` (基础) | byte | 1 |
| Hp | `Hp` (自定义) | int | 0（悬浮武器不需要血量?） |

---

## 三、Step 2 — gpo-gen.sh 执行

### 命令

```bash
gpo-gen.sh \
  --name BIU26FloatingWeapon \
  --display-name "悬浮武器" \
  --sync-client true \
  --project-root <项目根目录>
```

### 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--name` | `BIU26FloatingWeapon` | 与 GPOM 名称一致 |
| `--display-name` | `"悬浮武器"` | 中文名 |
| `--type-id` | （自动递增，预计 29） | 当前最大 ID 为 28 (HeroDummy) |
| `--sync-client` | `true` | 需要客户端视觉跟随 |
| `--gpom-name` | （省略，默认与 name 相同） | 自动使用 BIU26FloatingWeapon |

### 预期产出

#### 新建文件 (2 个)

**1. `Assets/Scripts/GamePlay/Server/AI/Systems/ServerAIBIU26FloatingWeaponSystem.cs`**

```csharp
namespace Sofunny.BiuBiuBiu2.ServerGamePlay {
    public class ServerAIBIU26FloatingWeaponSystem : S_AI_Base {
        private GPOM_BIU26FloatingWeapon useMData;

        protected override void OnAwake() {
            useMData = (GPOM_BIU26FloatingWeapon)MData;
            AddComponents();
        }

        protected override void AddComponents() {
            base.AddComponents();  // 12 个通用组件
            AddComponent<ServerAIAttribute>(...);  // MaxHp = useMData.Hp
            // TODO: 按需添加更多组件
        }

        protected override void OnStart() {
            base.OnStart();
            CreateEntity(AISkinSign + "Server");
            // + SetGameObjectEntity 注释参考
        }
    }
}
```

**2. `Assets/Scripts/GamePlay/Client/AI/Systems/ClientAIBIU26FloatingWeaponSystem.cs`**

```csharp
namespace Sofunny.BiuBiuBiu2.ClientGamePlay {
    public class ClientAIBIU26FloatingWeaponSystem : C_AI_Base {
        protected override void OnAwake() { ... AddComponents(); }
        protected override void OnStart() {
            CreateEntity(AISkinSign);  // + SetGameObjectEntity 注释参考
        }
        protected override void AddComponents() {
            base.AddComponents();  // 6 个通用组件
            AddComponent<ClientAIAttribute>();
        }
    }
}
```

#### 修改文件 (4 个)

| 文件 | 修改内容 |
|------|---------|
| `Assets/Scripts/Template/data/GpoType.cs` | 新增 `Id_BIU26FloatingWeapon = 29` + Data 数组条目 |
| `Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs` | 新增 `case GpoTypeSet.Id_BIU26FloatingWeapon: → ServerAIBIU26FloatingWeaponSystem` |
| `Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs` | 新增 `case GpoTypeSet.Id_BIU26FloatingWeapon: → ClientAIBIU26FloatingWeaponSystem` |
| `Assets/Scripts/Template/gpo/IGPOM.cs` | 新增 `case GpoTypeSet.Id_BIU26FloatingWeapon: → GPOM_BIU26FloatingWeaponSet.GetGPOMByIdAndMatchMode()` |

---

## 四、Step 3 — 手动编码（非工具范围）

以下文件无法由工具生成，需要工程师手动实现：

| 文件 | 说明 | 参考 |
|------|------|------|
| `ServerBIU26FloatingWeaponAttack.cs` | 定时触发 Ability 攻击组件 | GPO 技术文档 S-08 §8.3 骨架 |
| `ClientBIU26FloatingWeaponView.cs` | 客户端视觉跟随+水平排列组件 | GPO 技术文档 S-08 §8.4 骨架 |

> 这两个是业务定制组件，结构因需求而异，不适合模板化。
> 工具生成的 System 文件中有 `// TODO: 按需添加更多组件` 标记，工程师在此处 AddComponent。

---

## 五、执行后需手动调整

工具生成的 Server System 中 `ServerAIAttribute.InitData` 使用了占位值：
```csharp
ATK = 0,           // → 应改为 useMData.Atk
AttackRange = 0,   // → 应改为 useMData.AttackRange
MoveSpeed = 0,     // → 悬浮武器可能不需要，可删除
```

需要工程师根据 BIU26 技术文档 S-08 §8.2 骨架代码进行调整：
```csharp
AddComponent<ServerAIAttribute>(new ServerGPOAttribute.InitData {
    ATK          = useMData.Atk,
    AttackRange  = useMData.AttackRange,
    MaxHp        = useMData.Hp,
});
```

同时需要额外 AddComponent：
```csharp
AddComponent<ServerAIFindInsightTarget>(new ServerAIFindInsightTarget.InitData {
    CheckDistance        = useMData.MaxAttackDistance,
    LayerMask            = LayerData.ServerLayerMask | LayerData.DefaultLayerMask,
    IgnoreTeamId         = TeamId,
    IgnoreCollierTrigger = false,
});
AddComponent<ServerBIU26FloatingWeaponAttack>();
```

---

## 六、验证清单

- [ ] GPOM_BIU26FloatingWeapon.cs 生成，包含 5 个自定义字段
- [ ] GpoType.cs 中 `Id_BIU26FloatingWeapon = 29` 存在
- [ ] ServerAIWorld_Switch.cs 中有对应 case 路由
- [ ] ClientAIWorld_Switch.cs 中有对应 case 路由
- [ ] IGPOM.cs 中有对应 case 路由
- [ ] ServerAIBIU26FloatingWeaponSystem.cs 编译无错误
- [ ] ClientAIBIU26FloatingWeaponSystem.cs 编译无错误
