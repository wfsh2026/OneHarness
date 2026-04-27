# Shader 规范

---

## 一、不支持 Standard Shader

必须使用 `MiniLit` 或自定义 Shader。

## 二、MiniLit 属性名

```csharp
mat.SetColor("_BaseColor", Color.red);  // ✅ 正确
mat.color = Color.red;                   // ❌ 错误
```

## 三、MiniLit 不支持透明

透明效果使用 `SoFunny/Mini/MiniLit_Alpha`（已在 `Assets/Shader/`）。

## 四、MiniLit_Alpha 不支持双面渲染

`Cull Back` 硬编码，无法运行时覆盖。需双面时新建 Shader，将 `Cull Back` 改为 `Cull Off`：

```csharp
mat = new Material(Shader.Find("SoFunny/Mini/MiniLit_Alpha_DoubleSide"));
```

## 五、美术占位规则

战场美术资源先生成 Box / Sphere 占位。每个新视觉对象必须明确：
- **形状**（Cube / Sphere / Cylinder / Line）
- **颜色**（_BaseColor RGBA 值）
- **尺寸**（宽 × 高 × 深，单位：m）
- **挂点/偏移位置**描述

**禁止**只写"白色 Cube 占位"而不提供具体尺寸和挂点。

## 六、⚠️ 禁止运行时 `Shader.Find()` 创建材质

**问题**：`Shader.Find("SoFunny/Mini/MiniLit")` 在编辑器中正常，但打包后 **自定义 Shader 不一定被包含**，导致返回 `null` → `new Material(null)` 抛出 `ArgumentNullException`。

**禁止写法**：
```csharp
// ❌ 打包后崩溃
var mat = new Material(Shader.Find("SoFunny/Mini/MiniLit"));
mat.SetColor("_BaseColor", Color.red);
renderer.material = mat;
```

**正确做法**：

| 场景 | 解决方案 |
|------|---------|
| 灰盒占位（开发期） | 不设置材质，使用 Unity 默认灰色材质即可，不影响功能验证 |
| 正式美术资源 | **在本地预制体（Prefab）上预先配置材质球**，通过 `CreateEntity(sign)` 加载，**不走程序化 `new Material()`** |
| 必须程序化（如 LineRenderer） | 使用内置 Shader（如 `Sprites/Default`），或将材质球放入 `Resources/` 目录通过 `Resources.Load<Material>()` 加载 |

> ⚠️ `Sprites/Default` 是 Unity 内置 Shader，打包时自动包含，可安全用于 LineRenderer 等临时占位。
