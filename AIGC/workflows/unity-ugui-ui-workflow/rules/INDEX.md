# Unity UGUI UI 工作流规则索引

默认只读本索引。按命中条件读取具体规则。

| 文件 | read_when |
| --- | --- |
| `input-completeness.md` | 需要判断 UI 图片、素材、分辨率、交互和项目设置是否足够进入施工。 |
| `ui-planning.md` | 需要由 UI 开发者把 UI 图片解释为界面语义、交互状态、节点规划和资源核查输入。 |
| `technical-art-assembly.md` | 需要由 UI 资源整理员验收用户已切元素、整理正式资源、输出拼接还原文档。 |
| `unity-construction.md` | 需要由 UI 开发者生成 Unity UGUI Prefab 施工方案、Editor 创建脚本、Controller 或绑定表。 |
| `screenshot-calibration.md` | 需要基于目标 UI 图和 Unity 截图输出偏差表、回派角色和修正清单。 |
| `context-isolation.md` | 复杂 UI、长资源清单、长 manifest、多轮截图校准、大代码产物或长交付报告可能压爆主会话上下文。 |


## 组合读取规则

| 用户请求 | 必读文件 |
| --- | --- |
| 判断输入是否够 | `input-completeness.md` |
| 只做 UI 语义分析 | `input-completeness.md` + `ui-planning.md` |
| 输出 UGUI 施工方案 | `input-completeness.md` + `ui-planning.md` + `technical-art-assembly.md` |
| 生成 Unity 脚本 | `input-completeness.md` + `ui-planning.md` + `technical-art-assembly.md` + `unity-construction.md` |
| 做截图校准 | `screenshot-calibration.md` + 必要时回读 `technical-art-assembly.md` 或 `unity-construction.md` |
| 复杂 UI 或长产物 | `context-isolation.md` + 当前阶段对应规则 |
| 输出完整报告 | `templates/ui-ugui-delivery.md` + 当前阶段对应规则 |
