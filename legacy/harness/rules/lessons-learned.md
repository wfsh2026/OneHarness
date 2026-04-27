# 开发复盘记录 (Lessons Learned)

> 本文件是所有功能开发复盘的集中归档。  
> **每次功能验收后**，若发现新坑点或流程改进点，必须在此文件追加记录，并说明已沉淀至哪个规范文件。  
> 不写进文档的经验，下次开发仍然会犯同样的错误。

---

## 问题路由表（遇到问题时应沉淿到哪里）

| 问题类型 | 沉淀目标文档 |
|---------|------------|
| 编码方式 / 组件使用 / API 约束 | `aigc/harness/rules/GamePlay_Dev/` 下各规则文件（core-rules.md 等） |
| 系统归属识别 / 意图识别 / 预检流程 | [[knowledge/system-map]] |
| 协作阶段规则 / 文档要求 / 确认流程 | [[workflow-dev]] |
| 策划案写法 / 数值描述缺失 | [[设计文档完整性思维框架]] |
| 通用开发错误（跨系统适用） | 本文件（不需要改规范，只记录经验） |

> 💡 **Skill 提取**：问题分类与路由的认知框架详见 [[开发问题模式识别框架]]

---

## 批次一：多武器 PVE 模式开发

| # | 问题描述 | 已沉淀至 |
|---|---------|---------|
| 1 | 悬浮武器误判为枪械系统改造，未询问"GPO 还是外观包装" | core-rules.md / system-map.md |
| 2 | 忽略 GPOSpawner 现有框架，自建 WaveSpawner System | core-rules.md / system-map.md |
| 3 | 三选一归入策略层，遗漏 UI 交互链路 | core-rules.md / system-map.md / workflow-dev 阶段3 |
| 4 | 悬浮武器灰盒方案缺少尺寸和挂点描述 | core-rules.md / workflow-dev 阶段2资源确认 |
| 5 | 技术设计文档缺少 Input→CMD→RPC→Client 交互链路图 | core-rules.md / system-map.md / workflow-dev 阶段2 |
| 6 | 阶段4文档输出后，AI 未等待阶段5的用户审阅交接信号，直接执行了阶段6的进度总结和开发日志创建 | workflow-dev 阶段5（第6条强制守则） |
| 7 | 阶段2中只输出了 GD 部分（需求分析/体验提案），遗漏了 DL部分（会话预检/系统归属评估/技术可行性/方案选项），导致用户在阶段5审阅时才发现文件清单不完整 | workflow-dev 阶段2（第7条强制守则） |
| 8 | 执行计划文档的开发顺序缺少用户体验节点，导致用户只能等所有功能全部完成才能第一次进入体验，体验介入时机不明确 | workflow-dev 阶段6（第8条强制守则） |

---

## 批次二：赛博炮台开发

| # | 问题描述 | 已沉淀至 |
|---|---------|---------|
| 9 | 收到"开始开发"指令后，AI 直接进入编码，**未先初始化开发日志**。导致整个开发过程的关键决策和问题无法实时记录，只能事后补录（信息丢失风险高）。 | workflow-dev 阶段6（第9条强制守则） |
| 10 | 程序化构建多层级 Entity 时，`AddComponent<AIEntity>()` 在子节点创建之前调用，导致 `EntityBase.Awake` 中 `GetComponentsInChildren<HitType>()` 收集不到任何子节点，所有 `GetBodyTran` 返回 null。 | core-rules.md |
| 11 | 服务端程序化 Entity 使用 `CreatePrimitive` 创建子节点，保留了 `Renderer`，导致服务端 Mesh 与客户端 Mesh 叠加显示。 | core-rules.md |
| 12 | 旋转角度编码方式错误：直接沿用 MachineGun 的 `270 + localEulerAngles.x` 编码，但该方式只适用于纯仰角（>0）场景；赛博炮台含俯角（-45），Unity 将负角存储为 `360-|angle|`，导致编解码角度完全错误。 | core-rules.md |

---

## 批次四：BIU26 Phase 2 缩圈重构 / 小怪 Prefab 修复

| # | 问题描述 | 已沉淿至 |
|---|---------|---------|
| 17 | 修改 Prefab 根节点 `m_LocalScale` 来控制 AI 大小无效：加载时 `EntityData` 默认 `Vector3.one` 会覆盖 Prefab 根节点 scale。正确方式：在客户端 AI System 的 `OnStart()` 中 `CreateEntity()` 前调用 `iEntity.SetLocalScale()`，利用 `EntityData.IsScaleChange` 机制。 | `entity-code.md §一（AI 实体 Scale 设置规范）` |
| 18 | YAML 手动添加组件时只追加了 MonoBehaviour 块，但没有同时在 `m_Component` 列表中追加引用行，导致 Unity 导入时找不到该组件。必须两处同时修改。 | `entity-code.md §二（Unity Prefab YAML 添加组件规范）` |



> 下次出现新复盘问题时，在对应批次末尾追加一行，或新建批次：

```markdown
## 批次N：{功能名}开发

| # | 问题描述 | 已沉淀至 |
|---|---------|---------|
| N | {问题现象简述} | {规范文件 §章节 / 本文件} |
```

---

## 批次三：BIU26 Phase 1 发育循环开发

| # | 问题描述 | 已沉淀至 |
|---|---------|---------|
| 13 | 服务端发送 `SM_AI.Event_AddAI` 未设置 `OR_InData`，客户端 System 使用 `ClientAIAttribute` 导致 NullReferenceException（InData 强转访问字段崩溃）。修复：无 InData 时改用 `ClientGPOAttribute`。 | `gpo-code.md §八` |
| 14 | 刷怪器 `ServerBIU26MinionsSpawner` 用 `Update` 轮询检测 `IsClear()` 获取死亡位置，GPO 清除后 `GetPoint()` 返回 `(0,0,0)`，掉落物生成在地图原点。修复：在 `OR_CallBack` 中注册 `SE_GPO.Event_SetIsDead`，于 GPO 清除前获取精确位置。 | `gpo-code.md §九` |
| 15 | 误以为 `IGPO` 可以强转为具体 System 类型（如 `gpo.GetGPO() as ServerXXXSystem`），编译失败。`IGPO` 是数据接口，不持有 System 引用，跨 GPO 查询需通过 `gpo.Dispatcher(SE_AI.Event_GetMasterGPO)` 同步事件完成。 | `gpo-code.md §十` |
| 16 | 多个同类 GPO（悬浮武器）全部堆叠在同一位置，因 `slotIndex` 始终为 0（`SetSlotIndex()` 从未调用）。修复：改用自组织方案，每帧遍历 GPOList 自行计算 slot，不需要中央管理器。 | `gpo-code.md §十.4` |

