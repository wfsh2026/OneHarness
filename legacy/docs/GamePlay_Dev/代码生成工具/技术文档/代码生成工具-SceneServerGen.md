# 技术文档 — SceneServerGen（场景转服务端工具）

> 文档版本: v1.0  
> 最后更新: 2026-04-04  
> 对应工具: `aigc/harness/tools/codegen/scene-server-gen.sh` + `Assets/Editor/ServerSceneOptimizer/ServerSceneOptimizer.cs`

---

## 零、定位声明

本文档是**场景转服务端工具**的完整技术参考。AI Agent 在执行场景转换任务前**必须阅读本文档**。

---

## 一、工具概述

将客户端 Unity 场景转换为服务端优化场景。服务端场景移除所有渲染相关组件，保留碰撞和游戏逻辑。

**双步骤架构**：
1. **Bash 脚本** (`scene-server-gen.sh`)：复制场景文件 + 写入配置
2. **C# Editor 脚本** (`ServerSceneOptimizer.AIConvertScene`)：打开场景 → 优化 → 另存为 Server 前缀 → 注册 BuildSettings

---

## 二、AI Agent 使用流程

### 步骤 1：运行 Bash 脚本

```bash
bash aigc/harness/tools/codegen/scene-server-gen.sh \
  --scene-name <目标场景名> \
  --copy-from <源场景名> \     # 可选，用于从现有场景复制
  --project-root <项目根目录>
```

### 步骤 2：调用 Unity MCP 执行转换

```
execute_menu_item "Tools/功能/场景/AI场景转换"
```

### 步骤 3：验证结果

检查 Unity Console 日志：
- ✅ `[AI场景转换] 完成: ... => ...`
- ❌ 任何 error 日志表示失败

---

## 三、参数说明

| 参数 | 必选 | 说明 | 示例 |
|------|------|------|------|
| `--scene-name` | ✅ | 目标场景名（不含路径/扩展名） | `LevelTest_02_Temp` |
| `--copy-from` | ❌ | 源场景名，指定后复制源场景 | `LevelTest_02` |
| `--project-root` | ✅ | Unity 项目根目录 | `/path/to/project` |
| `--scene-dir` | ❌ | 场景目录（默认 `Assets/Scenes/Runtime`） | `Assets/Scenes/Custom` |

---

## 四、场景优化操作（C# 执行）

### 移除的组件

| 组件类型 | Unity ClassID | 处理方式 |
|----------|--------------|---------|
| MeshRenderer | 23 | 移除组件 |
| MeshFilter | 33 | 移除组件 |
| ParticleSystem | 198 | 移除组件 |
| LODGroup | 205 | 移除组件 |
| LineRenderer | 120 | 移除组件 |
| Light | 108 | **移除整个 GameObject**（因 URP UniversalAdditionalLightData 依赖） |

### 修改的组件

| 组件 | 操作 |
|------|------|
| SceneGPOEntity | 设置 `IsServer = true` |
| 所有 Collider | 添加 `HitType` 组件（`Layer = GPOData.LayerEnum.Ignore`） |

### 额外操作

| 操作 | 说明 |
|------|------|
| EditorBuildSettings | 自动注册客户端场景和服务端场景 |
| 场景回切 | 转换完成后自动回到客户端场景 |
| 配置清理 | 删除 `Temp/AIGC_SceneConvertConfig.txt` |

---

## 五、文件路径

```
输入场景:  Assets/Scenes/Runtime/{SceneName}.unity
输出场景:  Assets/Scenes/Runtime/Server{SceneName}.unity
配置文件:  {ProjectRoot}/Temp/AIGC_SceneConvertConfig.txt（临时，用完即删）
C# 脚本:  Assets/Editor/ServerSceneOptimizer/ServerSceneOptimizer.cs
Bash 脚本: aigc/harness/tools/codegen/scene-server-gen.sh
```

---

## 六、注意事项

1. **不复制 .meta 文件** — 复制场景时不复制 .meta，Unity 自动生成新 GUID
2. **Light 整体移除** — URP 的 `UniversalAdditionalLightData` 依赖 Light 组件，无法单独移除，因此销毁整个 Light GameObject
3. **幂等性** — EditorBuildSettings 注册前检查是否已存在，不会重复添加
4. **人机共用** — 人类通过 `Tools/功能/场景/服务器场景转换` 使用 GUI 版本，AI 通过 `Tools/功能/场景/AI场景转换` 使用自动化版本
5. **Prefab 安全** — 场景优化通过 Unity Editor API 运行（非 YAML 操作），正确处理 PrefabInstance 内部组件

---

## 七、验证案例

### 案例：LevelTest_02_Temp

```bash
# Step 1: Bash
bash aigc/harness/tools/codegen/scene-server-gen.sh \
  --scene-name LevelTest_02_Temp \
  --copy-from LevelTest_02 \
  --project-root /path/to/project

# Step 2: MCP
execute_menu_item "Tools/功能/场景/AI场景转换"

# 预期结果:
# - Assets/Scenes/Runtime/LevelTest_02_Temp.unity (复制)
# - Assets/Scenes/Runtime/ServerLevelTest_02_Temp.unity (生成)
# - EditorBuildSettings 中注册两个场景
# - Console: "[AI场景转换] 完成: ..."
```
