# 场景建设规范

> 适用场景：所有需要新建游戏场景（含客户端场景 + 服务端场景）的功能开发。
> 前提：MCP For Unity 已连接时，AI 可直接操作场景进行新增/修改。
> 参考文档：[[场景建设-TankBattle]]

---

## 一、双场景架构规范（核心）

本项目所有包含 GPO 的游戏模式，**必须**维护两套场景：

| 场景 | 命名规范 | 职责 |
|------|---------|------|
| **客户端场景** | `{ModeName}.unity` | 含 Renderer、光照、特效挂点、视觉表现层 |
| **服务端场景** | `Server{ModeName}.unity` | 仅含碰撞体、GPO、物理检测，无任何 Renderer |

**禁止**：将两套场景合并为一个场景，或在服务端场景中保留 MeshRenderer / Light / Camera 等视觉组件。

---

## 二、场景对象分类规则

场景中的对象按以下三类处理：

| 类型 | 定义 | 服务端场景处理 |
|------|------|--------------|
| **静态障碍** | 不可破坏、无血量（围墙/边界） | 保留 BoxCollider，移除 Renderer |
| **SceneGPO（可交互场景物体）** | 有 GPO 身份（基地/可破坏掩体/拾取物刷新点等） | 保留 GPO + 碰撞体，移除 Renderer，必须设置 `IsServer=true` |
| **纯视觉对象** | 仅用于视觉表现（装饰、灯光、天空盒） | 服务端场景**完全删除** |

---

## 三、服务端场景生成工作流

### ⚠️ AI 强制工具规则

**新建场景** → 必须调用 `aigc/harness/tools/codegen/scene-gen.sh`，禁止手动创建 SceneConfig.asset 或手动注册 Map.cs/SceneData.cs。

**场景创建是两步强制流程，缺一不可：**
1. `bash scene-gen.sh ...` — 注册 + 文件创建 + 服务端配置
2. `execute_menu_item "Tools/功能/场景/AI场景转换"` — Unity 执行服务端优化

**服务端场景生成不可跳过。** 如果同名服务端场景已存在，Unity 会自动删除旧文件并重新生成。

**仅重新生成服务端场景** → 调用 `aigc/harness/tools/codegen/scene-server-gen.sh`（Bash）+ `execute_menu_item "Tools/功能/场景/AI场景转换"`（MCP）。

### 推荐方案：AI 自动化生成（scene-gen.sh 全链路）

```bash
# Step 1: 一键创建场景全套注册
bash aigc/harness/tools/codegen/scene-gen.sh \
  --name MapTDM_07_NewCity \
  --display-name "新城市" \
  --sign NewCity \
  --copy-from LevelTest_02 \
  --project-root /path/to/project

# Step 2: Unity MCP 执行服务端优化
execute_menu_item "Tools/功能/场景/AI场景转换"
```

工具自动完成：
- Map.cs 注册（ID 常量 + Data 数组）
- SceneData.cs 注册（Data 条目）
- SceneConfig.asset 创建（最小可用模板）
- 场景文件复制
- 服务端转换配置

### 仅重新生成服务端场景（scene-server-gen.sh）

```bash
# Step 1: Bash
bash aigc/harness/tools/codegen/scene-server-gen.sh \
  --scene-name LevelTest_02_Temp \
  --copy-from LevelTest_02 \
  --project-root /path/to/project

# Step 2: Unity MCP（含 EditorBuildSettings 注册）
execute_menu_item "Tools/功能/场景/AI场景转换"
```

### 历史方案（已被工具替代，仅供参考）

```csharp
// 旧方案 — 手动 Editor 脚本（现在使用 scene-gen.sh + scene-server-gen.sh 替代）
// 1. 复制客户端场景文件
File.Copy("Assets/Scenes/Runtime/XXX.unity", "Assets/Scenes/Runtime/ServerXXX.unity");

// 2. 打开服务端场景
EditorSceneManager.OpenScene("Assets/Scenes/Runtime/ServerXXX.unity");

// 3. 批量删除视觉组件
// 遍历所有 GameObject，GetComponentsInChildren<Component>()
// 删除类型：MeshRenderer, SkinnedMeshRenderer, Light, Camera, ParticleSystem, AudioSource

// 4. 设置 SceneGPOEntity.IsServer = true
// 遍历所有 SceneGPOEntity 组件，设置 IsServer = true

// 5. 保存场景
EditorSceneManager.SaveScene(scene);

// 6. 脚本自删除（可选）
AssetDatabase.DeleteAsset(AssetDatabase.GetAssetPath(MonoScript.FromMonoBehaviour(this)));
```

### Phase N 迭代更新（新增 GPO 后重新生成）

1. 重新执行 Editor 脚本（或手动操作）
2. 对新增的可破坏对象：确认 SceneGPOEntity 挂载 + IsServer=true
3. 确认新增对象的 Layer = ServerLayer（8）

---

## 四、必须检查的配置项

| 检查项 | 错误后果 | 正确值 |
|--------|---------|-------|
| 服务端场景中的 SceneGPOEntity.IsServer | GPO 无法被服务端 System 识别 | `true` |
| GPO 对象的 Unity Layer | 炮弹/碰撞检测无法命中 | `ServerLayer`（Layer 8）|
| 服务端场景存在 MeshRenderer | 视觉叠加，客户端渲染错误 | 全部删除 |
| 出生点是否写入 MapXXX.asset 的 PlayerSpawnPoints | 玩家无法正常出生 | 必须配置 |
| 场景配置 ScriptableObject 的 Mode 字段 | 模式无法正确关联场景 | 与 ModeSet.Id_XXX 一致 |

---

## 五、场景层级结构推荐（新建场景时参考）

### 客户端场景层级

```
{ModeName} [Scene]
├── Environment
│   ├── Terrain / Ground          // 地面（含 Renderer）
│   ├── BoundaryWalls             // 边界围墙
│   └── Decorations               // 视觉装饰（正式美术用）
├── Covers
│   ├── Indestructible            // 不可破坏掩体
│   └── Destructible              // 可破坏掩体（SceneGPOEntity）
├── Bases / KeyObjects            // 关键 GPO 对象（基地/旗帜等）
├── SpawnPoints                   // 出生点（空 GameObject，无 Renderer）
└── Lighting
    ├── DirectionalLight
    └── Skybox
```

### 服务端场景层级（与客户端镜像，仅保留物理层）

```
Server{ModeName} [Scene]
├── Environment
│   └── Terrain_Collider          // 仅 BoxCollider，无 Renderer
├── Covers
│   ├── Indestructible            // BoxCollider，无 Renderer，无 GPO
│   └── Destructible              // SceneGPOEntity（IsServer=true）
├── Bases / KeyObjects            // GPO + HitType，无 Renderer
└── SpawnPoints                   // 空 GameObject
```

---

## 六、场景配置 ScriptableObject 规范

每个模式需要一个 `MapXXX.asset`，包含：
- `Mode`：对应 `ModeSet.Id_XXX`
- `PlayerSpawnPoints`：出生点 Transform 数组（客户端/服务端分别引用）
- `AISpawnPoints`（若有）：AI 刷新点标识（通常用 GPO Sign 字符串）

**禁止**：出生点数量不足（推荐每队 ≥5 个，避免多人模式出生点冲突）。

---

## 七、MCP For Unity 场景操作约定

当 MCP For Unity 连接时，AI 可直接：
- 创建新 GameObject 并配置 Transform
- 添加/修改 Component 属性（BoxCollider、SceneGPOEntity 等）
- 复制已有对象并调整位置（掩体批量布局）
- 截图验证场景布局是否符合策划案

**AI 操作场景前必须确认**：
1. 当前操作的是哪个场景（客户端 or 服务端）
2. 操作完成后，两套场景是否需要同步更新

---

## 八、NavMesh 烘焙规范（2026-03-27 坦克大乱斗 沉淀）

### 8.1 NavMesh 在哪个场景烘焙

**NavMesh 在客户端场景烘焙，但服务端场景才是实际使用方。**

工作流：
1. 在客户端场景（`XXX.unity`）里烘焙 NavMesh
2. 重新生成服务端场景（复制客户端 → 剥离 Renderer）
3. 服务端场景自动继承 NavMeshSurface 组件和 navMeshData 引用

### 8.2 NavMeshSurface 配置规范

项目使用 **AI Navigation 包**（`Unity.AI.Navigation.NavMeshSurface`），每个场景一般需要**两种 Agent** 各烘焙一个 Surface：

| Surface | AgentTypeID | 说明 |
|---------|------------|------|
| Surface（主） | `0` | 人形/大型单位 |
| MinSurface | `-1372625422` | 坦克/小型单位 |

参照各地图 `NavMesh-HumSurface.asset` + `NavMesh-MidSurface.asset`（或 ShipwreckBay 的 `NavMesh-Surface.asset` + `NavMesh-MinSurface.asset`）。

### 8.3 NavMeshSurface 必须的属性配置

| 属性 | 正确值 | 错误值（坑） |
|------|--------|------------|
| `CollectObjects` | **Volume** | ~~CurrentObjectHierarchy~~（默认值，只烘焙子节点，覆盖范围错误） |
| `Size` | 场景实际尺寸（如 130×20×130） | ~~10×10×10~~（默认值，不覆盖地图） |
| `Center` | (0, 5, 0)（地图中心，Y 抬高覆盖地面以上） | (0, 0, 0) |

**⚠️ 关键踩坑：`CollectObjects` 必须选 Volume**

- 默认值 `CurrentObjectHierarchy` 只收集 NavMeshData GO 的子节点，几乎什么都收集不到
- 必须选 `Volume`，配合 Size 和 Center 明确烘焙范围
- `BuildNavMesh()` 程序化调用时，属性必须先 `ApplyModifiedPropertiesWithoutUndo` + 保存场景，再 Bake——否则 Unity 在烘焙过程中会重置属性到默认值

### 8.4 正确的程序化烘焙流程

```
❌ 错误：AddComponent → 设属性 → 立刻 BuildNavMesh()
   （Bake 过程中重置属性到默认值，烘焙结果错误）

✅ 正确：
   1. AddComponent NavMeshSurface
   2. SerializedObject 设置所有属性
   3. ApplyModifiedPropertiesWithoutUndo()
   4. EditorSceneManager.SaveScene()    ← 必须先保存
   5. AssetDatabase.Refresh()
   6. 让用户在 Inspector 手动点 Bake
      （或通过 EditorApplication.delayCall 异步触发）
```

### 8.5 NavMesh 数据文件位置

Unity 自动在 `Assets/Scenes/Runtime/{SceneName}/` 目录下生成 `NavMesh-{SurfaceName}.asset`。每次 Bake 生成一个新文件（如 `NavMesh-NavMeshData 1.asset`、`NavMesh-NavMeshData 2.asset`...），旧文件不自动删除——需手动清理历史烘焙数据，保留最新的两个。

### 8.6 服务端场景同步

服务端场景转换工具（`scene-gen.sh` + MCP `AIConvertScene`）在复制客户端场景后批量删除视觉组件。`NavMeshSurface` 不属于 MeshRenderer/Light/Camera 等被删除的类型，因此**自动保留**在服务端场景中，无需额外处理。

---

## 九、ZoneMarker / 区域标记碰撞体规范（2026-03-29 BIU26 沉淀）

### 9.1 强制规则

**ZoneMarkers 父节点下的所有 Collider 必须设置 `isTrigger = true`。**

ZoneMarker 用于检测玩家是否进入某逻辑区域（刷怪圈、安全区、进攻区等），本质是逻辑触发器而非物理墙壁。若未勾选 isTrigger，Default 层 Collider 会被物理系统判定为实体，玩家会被"隐形碰撞体罩住"无法进入中心区域。

### 9.2 标准命名结构

`
ZoneMarkers（空父节点）
├── Zone_Outer    CapsuleCollider  isTrigger=true
├── Zone_Mid      CapsuleCollider  isTrigger=true
└── Zone_Inner    CapsuleCollider  isTrigger=true
`

### 9.3 创建 ZoneMarker 时的检查清单

- isTrigger = true（必选）
- Layer 为 Default 或专用 Zone 层均可（不影响触发逻辑）
- 不要在 ZoneMarkers 下放置有 Renderer 的物体（服务端不可见）
- 修改后在 PlayMode 跑一遍，确认玩家可自由穿越

---

## 十、新场景创建模板（通用）

### 10.1 基础场景复用

**新场景不从空场景开始，必须以 `Map_Template` 为基础进行复制。**

`Map_Template` 已集成以下基础环境（直接继承，无需重做）：
- 天空盒（Skybox）
- 环境光（Ambient Light）
- 方向光（Directional Light）

**制作流程**：
1. 复制 `Map_Template.unity` → 重命名为目标场景名（如 `MapArena.unity`）
2. 在新场景中删除不需要的 GameObject（**光源 GameObject 必须保留，不可删除**）
3. 添加新场景特有的 GameObject 和碰撞体
4. 复制步骤1的客户端场景文件 → 重命名为 `Server{TargetName}.unity`（如 `ServerMapArena.unity`）
5. 在 Unity 中打开服务端场景，执行菜单 **Tools → 功能 → 场景 → 服务器场景转换**（`ServerSceneOptimizer`）
   - 工具会自动删除：`MeshRenderer`、`MeshFilter`、`ParticleSystem`、`LODGroup`、`LineRenderer`、`Light`
   - 自动设置所有 `SceneGPOEntity.IsServer = true`
   - 自动为所有 Collider 添加 `HitType(Layer=Ignore)`
   - 点击 **场景优化 => 服务器** 按钮完成，工具自动保存场景
6. 在对应的 `CoreGameWorld`（或 `CoreGameWorld_UGC`）`OnInit()` 中注册新场景数据

> ⚠️ **禁止**：不能直接复制已有的服务端场景作为基础。  
> 服务端场景必须始终从对应客户端场景生成，保证两者内容一一对应。

### 10.2 光源保护规则

| 操作 | 规则 |
|------|------|
| 删除场景 GameObject | ✅ 允许（除光源外） |
| 删除 Directional Light | ❌ 禁止 |
| 修改 Directional Light 参数 | ✅ 允许（按需调整方向/强度） |
| 添加新光源 | ✅ 允许 |

> 原因：`Map_Template` 的全局光照烘焙依赖于 Directional Light，删除后场景会变全黑。

### 10.3 场景注册（UGC 示例）

UGC 新场景在 `CoreGameWorld_UGC.OnInit()` 中更新注册：

```csharp
SceneData.RegisterUGCScene(new SceneData.Data {
    ID            = SceneData.SceneId_UGCTest,   // PGC 已定义的 ID 常量
    StageSign     = "MapArena",                  // 与 .unity 文件名一致（去掉 .unity）
    ElementConfig = "SceneConfig_Arena",         // 对应的 SceneConfig asset 名
});
```
