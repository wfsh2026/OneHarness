# 2 代 Knowledge 知识库构建技术方案

> [项目负责人] 已熟读 [[Project_Lead]]（定位文件）
> 工作流：[[workflow-knowledge]]
> 姊妹文档：[[Gen1-knowledge构建技术方案]]
> 状态：📋 待用户审核

---

## 零、定位声明

本文档描述 **sausage-man-2022** 项目中 **2 代（Biubiubiu2）** 架构的 Knowledge 知识库构建方案。  
2 代采用 ECS 风格 System/Component 架构，有完整参考项目可迁移适配。

---

## 一、2 代架构概述

### 1.1 基本信息

| 维度 | 说明 |
|------|------|
| **代码位置** | `Assets/Script/Biubiubiu2/` |
| **代码量** | ~2,083 .cs 文件 |
| **架构风格** | ECS 风格 System/Component |
| **核心命名空间** | `Sofunny.BiuBiuBiu2.*` |
| **参考项目** | `G:\BiuBiuBiu2-ShottingDuck-UGC\` |
| **参考知识库** | `G:\BiuBiuBiu2-ShottingDuck-UGC\AIGC\knowledge\` |

### 1.2 代码结构

```
Assets/Script/Biubiubiu2/              ← 2 代框架层 (2,083 .cs)
├── GamePlay/              (1,111)     ← 核心玩法
│   ├── Server/                        ← 服务端 System/Component
│   ├── Client/                        ← 客户端 System/Component
│   └── Host/                          ← 主机端
├── Data/                  (275)       ← 数据定义
├── Message/               (265)       ← 消息协议
├── UI/                    (109)       ← UI 层
├── Template/              (65)        ← 模板数据
├── Component/             (44)        ← 共享 Component
├── Editor/                (37)        ← 编辑器工具
├── Utils/                 (30)        ← 工具库
├── 3rd/                   (137)       ← 第三方库
├── Asset/                 (5)
├── Lanuch/                (3)
├── Main/                  (1)
└── Stage/                 (1)
```

---

## 二、构建策略：迁移适配

### 2.1 数据来源

参考项目 `G:\BiuBiuBiu2-ShottingDuck-UGC\AIGC\knowledge\` 中已有完整知识库：

| 资产 | 数量 | 说明 |
|------|------|------|
| system-map.md | 1 份 (33KB) | 完整系统地图（10 大系统 + 实例清单） |
| features/*.md | 362 份 | YAML frontmatter + 代码文件表 |
| wiki-map.json | 1 份 | 文档名→路径映射索引 |
| graph.json | 1 份 | 代码图谱 |
| graph.html + html/ | 可视化 | HTML 交互式可视化 |

### 2.2 路径适配规则

参考项目与本项目的代码路径存在前缀差异：

```
参考项目:  Assets/Scripts/GamePlay/Server/GPO/...
本项目:    Assets/Script/Biubiubiu2/GamePlay/Server/GPO/...

替换规则:
  Assets/Scripts/ → Assets/Script/Biubiubiu2/
  Assets\Scripts\ → Assets\Script\Biubiubiu2\
```

### 2.3 参考项目系统清单（迁移目标）

从参考项目 system-map 中提取的 10 大系统：

| 系统 | 描述 | 关键内容 |
|------|------|---------|
| GPO 系统 | 地面可拾取物 | 17 种 GPO 类型 |
| 枪械系统 | 武器管理 | 5 种武器类型 |
| 载具系统 | 载具驾驶/交互 | 载具类型清单 |
| 模式系统 | 游戏模式管理 | 14 种模式 |
| Ability 系统 | 技能框架 | 46 种 AB + 19 种 AE |
| 3C 系统 | Character/Camera/Control | 角色控制 |
| 镜头系统 | 相机管理 | 镜头类型 |
| UI 系统 | 界面管理 | UI 框架 |
| 全局事件系统 | 事件总线 | 事件类型清单 |
| 场景工具系统 | 场景编辑器 | 工具链 |

### 2.4 features 目录结构（迁移后）

```
aigc/wiki/raw/biu2-framework/
├── ability/          ← 60+ json（技能系统功能包）
├── gpo/              ← 16+ json（GPO 系统功能包）
├── mode/             ← 11  json（模式系统功能包）
├── cross-cut/        ← 15+ json（跨领域功能包）
├── ugc/              ← 3   json（UGC 功能包）
└── ui/               ← 30+ json（UI 系统功能包）
```

---

## 三、执行计划

### 步骤 1：迁移 system-map 2 代部分

1. 从参考项目复制 system-map 内容
2. 替换所有路径前缀
3. 写入本项目 [[knowledge/system-map]] 的 2 代专属区域

### 步骤 2：迁移 features 功能包

1. 批量复制 `features/` 目录到 `features/gen2/`
2. 对所有 .md 文件执行路径替换
3. 重建 `wiki-map.json`（`wiki-resolve.py --build`）

### 步骤 3：路径验证

1. 抽取 json 中的文件路径（约 200-300 条）
2. 检查这些路径在本项目中是否存在
3. 记录不存在的路径（可能是版本差异）
4. 标记或移除无效条目

### 步骤 4：用户审核

- 审核迁移后的 system-map 2 代部分
- 抽查 features json 内容正确性
- 确认路径验证结果

---

## 四、风险与注意事项

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 参考项目与本项目版本差异 | 部分功能可能不存在 | 路径验证步骤识别 |
| 路径前缀替换遗漏 | json 中路径指向错误位置 | 正则全局替换 + 抽检 |
| 2 代可能引用 1 代代码 | 依赖关系不完整 | 在 system-map 中标注跨代依赖 |

---

## 五、验收标准

| 产出物 | 验收标准 |
|--------|---------|
| system-map.md（2 代部分） | 10 大系统条目完整，路径正确 |
| features/gen2/ | 110+ json 迁移完成，路径替换正确 |
| 路径验证报告 | 有效路径率 > 85% |

---

*文档版本：v1.0（草案）*
*创建时间：2026-04-11*
*状态：📋 待用户审核*
