# 1 代核心开发规则（Core Rules — Gen1）

> **适用范围**：DL（涉及 1 代 C/S/H 架构的所有编码任务）
> **不适用**：GPO / Ability / Scene Agent（它们只用 2 代共享 `core-rules.md`）
> **优先级**：仅次于 `safety-rules.md`，不可被任何 feature 需求覆盖
>
> ⚠️ 本文件是 **编码规范**，各系统的制作流程见对应 `制作文档/{领域}/{系统}制作.md`

## 📌 场景导航（按任务类型快速定位）

| 场景 | 必读章节 |
|------|---------|
| **任何 1 代编码任务** | 第一章 + 第二章 + 第六章 |
| 新增 Buff / 效果 | 额外读 第三章 |
| 新增物品 / 模式 / 角色技能 | 额外读 第四章 |
| 涉及资源加载 / ToBundle 路径 | 额外读 第五章 |
| 涉及网络消息 / RPC | 额外读 第三章 §3.4 |
| 排查运行时错误 | 直接看 第六章 |

---

# 第一章：开发前必问清单

凡触发以下任一场景，必须先向用户提问，等待确认后再动手。

## 1.1 关于"代际归属"

**触发条件**：需求中的目标代码既存在于 `Assets/Script/Biubiubiu2/` 也存在于 `Assets/Script/`（非 Biubiubiu2）时。

**必须询问**：
> "这个功能涉及 1 代代码还是 2 代代码？
> A. **1 代**（C/S/H 三层架构，在 `Assets/Script/` 下）
> B. **2 代**（ECS 架构，在 `Assets/Script/Biubiubiu2/` 下）"

## 1.2 关于"已有实例复用"

**触发条件**：开始实现任何新功能前。

**执行顺序**：
1. 查 `knowledge/system-map.md §六` 已有实例清单
2. 查 `knowledge/features/{系统}/` feature JSON 代码路径
3. 找到相似实例 → 以其为模板开发
4. 找不到 → 向用户确认是否为全新功能

## 1.3 关于"配置表修改"

**触发条件**：需求涉及新增物品、Buff、模式时。

**必须确认**：
> "新增 {类型} 需要修改以下配置表，请确认：
> - `PickItemData.txt`（物品主表）
> - `BuffAsset.txt`（Buff 路径映射）
> - 其他相关配置表
> 这些是否需要策划侧提供数据？"

---

# 第二章：C/S/H 三层架构规则（全局强制）

## Rule 1：三端分离——Host / Server / Client

1 代所有业务逻辑必须遵循 **C/S/H 三文件模式**：

| 层 | 路径前缀 | 职责 | 状态写权 |
|------|---------|------|---------|
| **Host**（共享） | `Host/Modules/{Domain}/` | 初始化、配置加载、状态机 | 有限（共享状态） |
| **Server**（服务端） | `Server/Modules/{Domain}/` | 权威计算、伤害结算、数据验证 | ✅ 完全控制 |
| **Client**（客户端） | `Client/Modules/{Domain}/` | UI / 特效 / 动画 / 表现 | ❌ 只读展示 |

```csharp
// ✅ 正确：三层分离
// Host 端
public class BSBeatBack : BuffSystemBase {
    public BSBeatBackServer ServerLogic { get; set; }
    public BSBeatBackClient ClientLogic { get; set; }
}

// Server 端
public class BSBeatBackServer {
    public void Init(BuffSystemBase buffSystem) {
        ((BSBeatBack) buffSystem).ServerLogic = this;
    }
}

// Client 端
public class BSBeatBackClient {
    public void Init(BuffSystemBase buffSystem) {
        ((BSBeatBack) buffSystem).ClientLogic = this;
    }
}

// ❌ 错误：在 Host 层直接写伤害计算
public class BSBeatBack : BuffSystemBase {
    public void CalculateDamage() { ... }  // ❌ 应放 Server 端
}
```

## Rule 2：Host→Server/Client 注册方式

Server/Client 通过 `RequestGameLoop<T>()` 在 Host 端注册：

```csharp
// Host 端 InitServer() 中
protected override void InitServer() {
    RequestGameLoop<BSBeatBackServer>();  // 注册 Server 逻辑
}

// Host 端 InitClient() 中
protected override void InitClient() {
    RequestGameLoop<BSBeatBackClient>();  // 注册 Client 逻辑
}
```

**⚠️ 常见错误**：忘记调用 `RequestGameLoop<T>()` → Server/Client 的 Init 不执行 → 运行时空引用。

## Rule 3：跨层通信只能走网络消息

Server 与 Client 之间 **禁止直接方法调用**，必须通过 Proto_ 网络消息：

```csharp
// ✅ 正确：Server → Client 通过 RPC
// Server 端
Proto_Role.RpcUseItem rpc = new Proto_Role.RpcUseItem {
    itemSign = sign, result = true
};
SendToAllClients(rpc);

// Client 端
void OnRpcUseItem(Proto_Role.RpcUseItem msg) {
    UpdateUI(msg.itemSign);
}

// ❌ 错误：Server 直接调用 Client 方法
clientLogic.UpdateUI(sign);  // ❌ 跨进程调用
```

## Rule 4：文件命名强制规范

| 层 | 命名格式 | 示例 |
|------|---------|------|
| Host Buff | `BS{Name}.cs` | `BSBeatBack.cs` |
| Host Buff SO | `BSO{Name}.cs` | `BSOBeatBack.cs` |
| Server Buff | `BS{Name}Server.cs` | `BSBeatBackServer.cs` |
| Client Buff | `BS{Name}Client.cs` | `BSBeatBackClient.cs` |
| Host 角色逻辑 | `RoleLogic{Function}.cs` | `RoleLogicItem.cs` |
| Server 角色 | `RoleLogicServer_{Function}.cs` | `RoleLogicServer_DownHp.cs` |
| Client 角色 | `RoleLogicClient_{Function}.cs` | `RoleLogicClient_Movement.cs` |
| Host 模式 | `AbsModeManager` 子类 | `ClassicModeMgr.cs` |
| Server 模式 | `Server{Mode}Mgr.cs` | `ServerClassicMgr.cs` |
| Client 模式 | `Client{Mode}Mgr.cs` | `ClientClassicMgr.cs` |

## Rule 5：namespace 规则

1 代代码 **不使用 namespace**（与 2 代 `Sofunny.BiuBiuBiu2.*` 不同）。所有 1 代代码在 `Assembly-CSharp` 全局命名空间下。

```csharp
// ✅ 1 代代码（无 namespace）
public class BSBeatBack : BuffSystemBase { ... }

// ❌ 1 代代码不应添加 namespace
namespace Sofunny.BiuBiuBiu2.Host {  // ❌ 这是 2 代规范
    public class BSBeatBack { ... }
}
```

## Rule 6：C# 命名规范

| 修饰符 | 命名格式 | 示例 |
|--------|---------|------|
| `private` 字段 | camelCase | `private float checkDistance;` |
| `public` 字段/属性 | PascalCase | `public float CheckDistance;` |
| `const` | SCREAMING_SNAKE_CASE | `const float CHECK_DISTANCE = 10f;` |
| 方法名 | PascalCase | `private void FindNearestEnemy()` |
| 参数 | camelCase | `void OnUpdate(float delta)` |

```csharp
// ✅ 正确
private float checkDistance;
public float CheckDistance;
const int MAX_RETRY_COUNT = 3;

// ❌ 错误
private float _checkDistance;   // 禁止下划线前缀
private float check_distance;  // 禁止蛇形命名
```

---

# 第三章：ScriptableObject 与 Buff 规范

## Rule 7：BSO → BS 创建链（四文件模式）

每个 Buff 功能由 4 个文件组成：

```
BSO{Name}.cs → BS{Name}.cs → BS{Name}Server.cs → BS{Name}Client.cs
（SO 配置）    （Host 逻辑） （Server 权威）       （Client 表现）
```

### BSO 模板（SO 配置类）

```csharp
// 位置: Host/Modules/Buff/BuffScriptableObject/

[CreateAssetMenu(menuName = "War/Buff/BSO{BuffName}")]
public class BSO{BuffName} : BuffSOBase {
    [Tooltip("参数说明")]
    public float paramName = 1.0f;

    [Tooltip("子 Buff 引用")]
    public BuffSOBase subBuffRef;

    // ⭐ 核心：创建 Host 端 BS 实例
    public override BuffSystemBase init(BuffBox buffBox) {
        BS{BuffName} system = new BS{BuffName}();
        system.Init(buffBox, this);
        return system;
    }
}
```

### BS 模板（Host 逻辑类）

```csharp
// 位置: Host/Modules/Buff/BuffSystem/

public class BS{BuffName} : BuffSystemBase {
    public BS{BuffName}Server ServerLogic { get; set; }
    public BS{BuffName}Client ClientLogic { get; set; }

    protected override void InitServer() {
        RequestGameLoop<BS{BuffName}Server>();
    }
    protected override void InitClient() {
        RequestGameLoop<BS{BuffName}Client>();
    }
}
```

## Rule 8：三种 SO 基类选择

| 效果类型 | 基类 | 使用场景 | 关键字段 |
|---------|------|---------|---------|
| 普通 Buff | `BuffSOBase` | 击退、触发器、护盾 | — |
| 可破坏物体 | `HpBuffSOBase` | 石墙、火焰盾（带血量） | `Hp`, `OnDeadBuff` |
| 速度类 | `BuffSpeedSOBase` | 加速 / 减速 | `AddSpeedRatio` |

```csharp
// ✅ 可被破坏的障碍物
public class BSOStoneWall : HpBuffSOBase {
    public float Hp = 500f;           // 血量
    public BuffSOBase OnDeadBuff;     // 被摧毁时触发
}

// ❌ 错误：带血量的物体用了普通基类
public class BSOStoneWall : BuffSOBase {
    public float Hp = 500f;  // ❌ BuffSOBase 不处理 Hp
}
```

## Rule 9：SO 资产文件路径

```
Assets/ToBundle/ScriptableObject/
├── Buff/{Category}/{BuffSign}.asset     ← Buff SO
├── Items/Weapons/{WeaponSign}.asset     ← 武器 SO
├── Screen/GameSetting/{sign}.asset      ← 模式主配置
└── Mode/{sign}.asset                    ← 模式专属 SO
```

**⚠️ SO 必须在 `BuffAsset.txt` 中注册路径映射**，否则运行时 `AssetsLoad.GetSOBuffData()` 返回 null。

## Rule 10：网络消息文件规范

```csharp
// 位置: Host/Network/Proto/Base/Proto_{Domain}.cs

class Proto_{Domain} {
    public class {MessageName} : IMessageBase {
        public int playerId;
        public string itemSign;
        // 序列化方法
    }
}

// 结构体消息
// 位置: Host/Network/Proto/Base/ProtoStruct_{DataName}.cs
class ProtoStruct_{DataName} {
    public long id;
    public int type;
}
```

---

# 第四章：配置与注册模式

## Rule 11：新增物品的 5 阶段注册

### Phase 1：常量定义

```csharp
// 位置: Assets/Script/Data/ItemData.cs
public const string NewItemSign = "NewItemSign";
```

### Phase 2：配置表注册

```
// PickItemData.txt（Tab 分隔）
ItemType   ItemSign       BuffSign        UserTime   ...
46         NewItemSign    NewItemBuff     2.0        ...

// BuffAsset.txt（Buff 路径映射）
NewItemBuff    {Category}
```

### Phase 3：SO 创建

```
Editor → Right-click → Create → War/Buff/BSO{Name}
→ 放置 Assets/ToBundle/ScriptableObject/Buff/{Category}/
→ 命名 {BuffSign}.asset
→ Inspector 配置参数
```

### Phase 4：代码注册

```csharp
// 在对应 Factory / switch 中添加 case
case ItemData.NewItemSign:
    // 处理逻辑
    break;
```

### Phase 5：验收

```
- [ ] ItemData.{Sign} 常量已定义
- [ ] PickItemData.txt 已注册
- [ ] BuffAsset.txt 映射已添加
- [ ] SO 已创建并配置
- [ ] 预制体已放到正确路径
- [ ] 代码 case 已添加
- [ ] 编译零错误
```

## Rule 12：ID 分配规范

| ID 类型 | 格式 | 分配规则 | 检查文件 |
|--------|------|---------|---------|
| ItemType | 整数枚举 | 不可重复，见 ItemData.cs | `ItemData.cs` |
| ItemSign | 字符串 | PickItemData.txt 主键唯一 | `PickItemData.txt` |
| BuffSign | 字符串 | BuffAsset.txt 主键唯一 | `BuffAsset.txt` |
| SkillCardType | 整数 1-30 | 已用 1-10,15-16,18-24 | `SORoleSkill.txt` |

**⚠️ `useItemSigns` 数组只能在末尾追加**——中间插入会导致所有旧物品快捷键映射错乱。

## Rule 13：配置表格式要求

- 格式：**TSV**（Tab 分隔）
- 编码：**UTF-8**
- 路径：`Assets/ToBundle/Config/Txt/{TableName}.txt`
- 主键：第一列（通常为 ItemSign 或 BuffSign）

```
// ✅ 正确：Tab 分隔，UTF-8
ItemType\tItemSign\tBuffSign\tUserTime
46\tBandage\tBandageBuff\t2.0

// ❌ 错误：逗号分隔
ItemType,ItemSign,BuffSign,UserTime
```

---

# 第五章：资源加载（ToBundle 路径体系）

## Rule 14：ToBundle 目录结构

```
Assets/ToBundle/
├── ScriptableObject/                    ← SO 配置
│   ├── Buff/{Category}/                 ← 170+ 子目录
│   ├── Items/{Domain}/                  ← 装备/配件
│   ├── Screen/{ScreenType}/             ← 游戏/赛制配置
│   └── Mode/                            ← 模式专属
├── GamePlayItem/                        ← 游戏物品预制体
│   ├── WeaponControls/                  ← 武器预制体 (96 个)
│   ├── PickItems/                       ← 拾取物
│   └── Bullet/                          ← 弹体
├── Config/Txt/                          ← 配置表 (TSV)
├── Skin/Items/                          ← 武器皮肤 (4691 个)
└── Effect/Buff/                         ← 特效预制体
```

## Rule 15：4 种标准加载链

| 加载类型 | API | 路径模板 |
|---------|-----|---------|
| 配置表 | `ConfigManager.GetConfigRawDatas("表名")` | `ToBundle/Config/Txt/{Table}.txt` |
| Buff SO | `AssetsLoad.GetSOBuffData(sign)` | `ToBundle/ScriptableObject/Buff/{Cat}/{sign}.asset` |
| 武器 SO | `ConfigLoader.GetSOWeaponData(sign)` | `ToBundle/ScriptableObject/Items/{subPath}/{sign}.asset` |
| 预制体 | `ItemPool.GetWeaponControl(sign)` | `ToBundle/GamePlayItem/WeaponControls/{sign}.prefab` |

```csharp
// ✅ 正确：通过标准 API 加载
var so = AssetsLoad.GetSOBuffData(buffSign);

// ❌ 错误：硬编码路径直接加载
var so = Resources.Load<BuffSOBase>("Buff/MyBuff");  // ❌ 不走 AssetBundle
```

## Rule 16：皮肤资源命名规范

```
{原始标识}_Skin{索引}
```

示例：`AK47_Skin01`, `AK47_Skin02`

命名不规范 → 皮肤加载失败。

---

# 第六章：常见错误与预防

## 10 大踩坑禁区

| # | 错误 | 症状 | 预防措施 |
|---|------|------|---------|
| 1 | BS init() 返回类型不匹配 | NullReferenceException | `new BS{Name}()` 类名与文件一致 |
| 2 | 缺少 `RequestGameLoop<T>()` | Server/Client Init 不执行 | Host 端必须调用 |
| 3 | Server/Client Logic 未赋值 | 空引用 | Init() 中赋值 `((BS{Name}) buffSystem).ServerLogic = this` |
| 4 | SkillCardType 编号冲突 | 新卡技能在旧卡上触发 | 查已用编号再分配 |
| 5 | useItemSigns 中间插入 | 所有旧物品快捷键错乱 | **只在末尾追加** |
| 6 | ItemData 常量未定义 | CS1061 编译错误 | 先在 ItemData.cs 定义 |
| 7 | SO 路径未在 BuffAsset.txt 注册 | 运行时加载返回 null | 检查映射表 |
| 8 | 载具未加入地图投放 | 地图中无新车辆 | 检查 SOCreateObjData |
| 9 | 皮肤命名不规范 | 加载失败 | 遵循 `{Sign}_Skin{N}` |
| 10 | Proto 消息未实现序列化 | 网络同步失败 | 实现 IMessageBase |

## 编译前检查单

```
✅ 编译时必检：
- [ ] ItemData.{Sign} 已定义
- [ ] PickItemData.txt 已注册
- [ ] BuffAsset.txt / ItemAsset.txt 路径映射已添加
- [ ] 预制体放在正确 ToBundle/ 路径下
- [ ] 无 CS error（警告可接受）

✅ 运行时必检：
- [ ] ConfigManager 能加载配置表
- [ ] AssetsLoad 能加载 SO（非 null）
- [ ] ItemPool 能获取预制体
- [ ] 无 NullReferenceException
```

---

# 附录：系统入口类速查

| 系统 | Host 入口 | Server 入口 | Client 入口 |
|------|----------|-----------|-----------|
| Buff | `BuffControl` + `BS{Name}` | `BS{Name}Server` | `BS{Name}Client` |
| 角色 | `BattleRoleLogic` | `RoleLogicServer` | `RoleLogicClient` |
| 模式 | `AbsModeManager` 子类 | `Server{Mode}Mgr` | `Client{Mode}Mgr` |
| AI | `RoleAILogic` | `ServerRoleAILogic` | `ClientRoleAILogic` |
| 载具 | `CarNet` | `CarNetServer` | `CarNetClient` |
| 武器 | `WeaponControl` / `HitPart` | — | — |
| 投掷物 | `RoleSkillBomb` 子类 | `BSClientBombServer` | `BSClientBombClient` |

> 详细系统地图见 `knowledge/system-map.md §二`
> 各系统制作流程见对应 `制作文档/{领域}/{系统}制作.md`

---

# 附录 B：1 代开发工作流差异提示

> 1 代开发 **使用共享 `workflow-dev.md` 流程**，但以下步骤需替换/跳过：

| 共享流程步骤 | 1 代处理方式 |
|-------------|-------------|
| S-04.7 Codegen 工具预读清单 | **跳过**（1 代无 codegen 工具） |
| Codegen 指令清单 | **跳过** |
| GPO/Ability/Scene Agent 子文档填充 | **跳过**（DL 独立完成） |
| 阶段 6 派发子任务给 GPO/Ability/Scene | **替换**为 DL 独立按 C/S/H 编码 |
| 阶段 6 Codegen 执行 | **替换**为 5 阶段手动注册（见 Rule 11） |

**1 代阶段 6 编码顺序**：
1. 先完成 5 阶段注册（Rule 11-13）
2. 按 Host → Server → Client 顺序编码（Rule 1）
3. 每个文件完成后检查 第六章·编译前检查单

**1 代验收额外检查**（阶段 8 叠加）：
- [ ] ItemData 常量已定义且无冲突
- [ ] SO 在 BuffAsset.txt 有路径映射
- [ ] 预制体在正确的 ToBundle/ 目录下
- [ ] 无 namespace（全局命名空间）

**规范反哺**（阶段 12 叠加）：
- 更新 `knowledge/system-map.md §六` 已有实例清单
- 更新 `knowledge/features/{系统}/` feature JSON
- 若发现新坑点 → 更新本文件第六章
