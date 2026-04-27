# Gameplay_Programmer 规则索引

> 此目录专项规则文件，配合 [[GamePlay_Dev/core-rules]]（编码 Agent 核心规则）使用。
> 全局约束见 `../safety-rules.md`，编码核心规则见 `../core-rules.md`。

---

## 各 Agent 启动必读（顺序）

| Agent | 必读顺序 |
|-------|---------|
| DL| `safety-rules` → `core-rules` → `shader-code` → `technical-doc-format` → `plan-doc` → 本 README（再按任务按需加载） |
| GPO 工程师 | `safety-rules` → `core-rules` → `shader-code` → `technical-doc-format` → `gpo-code` |
| Ability 工程师 | `safety-rules` → `core-rules` → `shader-code` → `technical-doc-format` → `ability-code` |
| 场景建设工程师 | `safety-rules` → `shader-code` → `technical-doc-format` → `scene-code` |

---

## DL专项规则按需加载

| 场景 | 加载文件 |
|------|---------|
| 涉及新 GPO / SceneGPO 开发（审核或直接开发） | `gpo-code.md` |
| 涉及 Ability / AE 开发（审核或直接开发） | `ability-code.md` |
| 涉及游戏模式开发 | `mode-code.md` |
| 涉及场景建设（审核或直接开发） | `scene-code.md` |
| 涉及镜头/相机系统 | `camera-code.md` |
| 涉及枪械开发 | `weapon-code.md` |

---

## 文件清单

| 文件 | 职责 |
|------|------|
| `gpo-code.md` | GPO 开发规范（新建必须文件 Checklist / AIEntity 顺序 / SceneGPO 架构 / 载具架构） |
| `ability-code.md` | Ability 开发规范（AB/AE 新建文件 Checklist / 触发入口 / AE 去重 / 伤害增益选型） |
| `mode-code.md` | 游戏模式开发规范（新建文件 Checklist / 常见 Bug 陷阱 / 状态机流程） |
| `scene-code.md` | 场景建设规范（双场景架构 / Editor 生成工作流 / NavMesh 烘焙规范） |
| `camera-code.md` | 镜头/辅助瞄准规范（双层控制原理 / 新 GPO 接入步骤 / 常用消息速查） |
| `weapon-code.md` | 枪械开发专项（三层模板 / 双端注册 / 动画注册） |
| `shader-code.md` | Shader 规范 + 美术占位规则（⚠️ 所有 Agent 涉及视觉对象时必读，含场景建设） |
| `technical-doc-format.md` | 技术文档格式强制规范（六大必须章节 / 声明表三类格式 / [项目负责人]专用清单） |
| `plan-doc.md` | 开发计划模式规范（触发条件 / 主计划五要素 / 子文档五要素 / ADR 格式）**⚠️ DL每次必读** |
