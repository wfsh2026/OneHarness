> ⚠️ 该文件由 session-sync.sh 自动维护，禁止 AI 手动编辑。所有写入必须通过 aigc/harness/tools/session-sync.sh 执行。

# 当前会话状态

## 项目：{项目名}
## 工作流类型：业务开发
## 当前阶段：Phase 7 测试验收阶段（策划案对比审计 + 性能优化已完成）

## 门控记录
| 门控 | 结果 | 时间 |
|------|------|------|
| p2 需求深度分析 | ✅ 通过 | 2026-04-09 |
| Phase3-gate | PASS | 2026-04-09 |
| p4 文档化与开发计划 | ✅ 通过 | 2026-04-09 |
| Phase5-gate | PASS | 2026-04-09 |

## 主进度：体验节点验收清单

### 【体验节点 1】{功能名}
| 步骤 | 内容 | 状态 |
|------|------|------|
| ① [项目负责人] | 初始化 active.md + session-log.md | ✅ |
## 开发里程碑

### Phase 1 — 载具基础骨架
| 体验节点 | 验收目标 | 负责 Agent | 状态 |
|---------|---------|-----------|------|
| UX-1 载具生成与交互 | 在 BR 模式中 MotoSheep 按与 JetCar 一致的比例在地图生成，玩家靠近可看到交互提示并成功上车/下车/换座 | [DL] | 📋 |
| UX-2 载具驾驶操控 | 上车后可正常 WASD/摇杆 控制方向，加速/刹车/氮气/跳跃响应正常，极速 77km/h，氮气极速 119km/h，转向角 44° | [DL] | 📋 |
| UX-3 载具数值配置 | SOCarData.txt 中 MotoSheep 条目 HP=1230/Oil=5000/CarRoleNum=2，MotorCarSetting 物理参数与策划案一致 | [DL] | 📋 |

### Phase 2 — 彩虹飞跃技能
| 体验节点 | 验收目标 | 负责 Agent | 状态 |
|---------|---------|-----------|------|
| UX-4 技能释放与彩虹路生成 | 驾驶 MotoSheep 时按 E 键/点击 GUI 按钮，前方 5m 处生成两段式彩虹路（30°坡道30m + 平坦冲刺道50m），CD 30秒正常计时 | [Ability] | 📋 |
| UX-5 彩虹路增益效果 | 任意载具驶上彩虹路后极速+30%（77→100km/h）、加速+30%、0 油耗；离开后恢复正常 | [Ability] | 📋 |
| UX-6 彩虹路规则验证 | 彩虹路为中立（敌方载具也可用）、遇地形障碍截断、5秒渐变消散、多次释放可叠加 | [Ability] | 📋 |

### Phase 3 — 表现层与联调验收
| 体验节点 | 验收目标 | 负责 Agent | 状态 |
|---------|---------|-----------|------|
| UX-7 视觉与镜头反馈 | 驶入彩虹路时 FOV 放大 10°（2秒过渡），驶出恢复；彩虹路消散时有 Opacity 渐变表现 | [DL] | 📋 |
| UX-8 完整链路验收 | 载具生成→上车→驾驶→释放技能→驶过彩虹路→效果生效→彩虹路消散→载具损毁爆炸 全链路无报错可运行 | [DL] | 📋 |
| ㉓ [PL] | Phase 6 逐模块开发开始 | ✅ |
| ㉓ [DL] | CAB_RainbowLeapSystem.cs 业务逻辑填充完成 | ✅ |
| ㉔ [DL] | RainbowRoadMeshBuilder.cs 创建完成 | ✅ |
| ㉕ [DL] | RainbowRoad_Entity.cs 创建完成 | ✅ |
| ㉖ [DL] | AbilityM_RainbowLeap.csv 数值填充完成 | ✅ |
| ㉗ [DL] | MotoSheep_MotorCarSetting.asset 创建完成(maxSpeed=77,shiftSpeed=119,SteerAngle=44) | ✅ |
| ㉓ [项目负责人] | 编译错误修复(Bug#14): CAB_RainbowLeapSystem.cs SetGameObjectEntity+GetGameObj 按 core-rules 修复 | ✅ |
| ㊸ [DL] | SAB_RainbowLeapSystem: SABC射线起点改为spawnPoint，修复打到车自身 | ✅ |
| ㊹ [DL] | SAB_RainbowLeapSystem: 斜坡地面吸附clamp[+0,+1.0m] | ✅ |
| ㊺ [DL] | SOCarSkill.txt: MotoSheep SkillCD=10(测试用，正式改回30) | ✅ |
| ㊻ [DL] | 技术文档: 载具+Ability配置文件速查表 | ✅ |
| ㊼ [DL] | CAB fallback bug：sprintLen>0 改为 serverSentData=rampLength>0，两字段统一判断 | ✅ |
| ㊽ [DL] | SABC 障碍物检测重构：Physics.Raycast→RaycastNonAlloc，层级掩码白名单（Default+Terrain），排除 Car/Role 动态碰撞体 | ✅ |
| ㊾ [DL] | TaskItemData.txt 添加 MotoSheep 条目（ItemId 占位符 2033459119683276801，需服务器正式 ID 替换） | ✅ |
| ㊽ [DL] | SABC 升级为双射线检测：Ray1=斜坡角度仰角（只有高墙才截断），Ray2=斜坡顶端水平（冲刺段）；SAB 传入 RampAngle 参数 | ✅ |
| ㊽ [DL] | SABC 最终版：双 SphereCast（Ray1=斜坡仰角球半径15m，Ray2=冲刺段水平球半径25m）；SAB 传入全部宽度参数 | ✅ |
| ㊿ [DL] | SABC 改回 3 条平行 RaycastNonAlloc（中心+左/右侧偏移=远端宽/2），修复 SphereCast 起点重叠导致穿透的问题 | ✅ |
| ㊿ [DL] | 动态宽度检测：SABC 生成点左右预测有效半宽，侧偏移量自适应，Rpc+CAB 同步传宽度，mesh 最小保证 2m | ✅ |
| P6-1 [DL] | ClientRainbowLeapMeshBuild OnAwake 优化: 提取 ClampWidths+BuildRoadGameObject | ✅ |
| P6-2 [DL] | ServerRainbowLeapObstacleDetect OnAwake 重构: 提取 5 个方法(InitDirections/DetectEffectiveWidth/DetectObstacles/DetectRampObstacle/DetectSprintObstacle), static readonly s_ObstacleMask | ✅ |
| P6-3 [DL] | RainbowRoadMeshBuilder 三级缓存: Material 全局缓存+Mesh 对象池(Stack)+顶点数组预分配复用 | ✅ |
| P6-4 [DL] | RainbowRoad.prefab 预制体创建: MeshFilter+MeshRenderer+MeshCollider+BoxCollider+RainbowRoadMeshBuilder+RainbowRoad_Entity | ✅ |
| P6-5 [DL] | CAB_RainbowLeapSystem 重写: CreateEntityToPool(RainbowRoad)+OnLoadEntityEnd+BuildRoadOnEntity | ✅ |
| P6-6 [DL] | 池安全生命周期: MeshBuilder.OnDisable 归还 Mesh+Entity.OnDisable 重置 PropertyBlock | ✅ |
| P6-7 [DL] | 消除运行时 Material/Shader.Find: 创建 RainbowRoad_Mat.mat(URP/Lit+Transparent), 预挂到 prefab MeshRenderer | ✅ |
| P6-8 [DL] | RainbowRoad_Mat.mat 迁移到 Assets/Art/Effects/Materials/ | ✅ |
| P6-9 [DL] | RainbowRoad_Entity 零 GC 优化: 缓存 MaterialPropertyBlock+WaitForSeconds, 提取 CacheRenderers() | ✅ |
| P6-10 [DL] | 删除废弃 ClientRainbowLeapMeshBuild.cs (无外部引用) | ✅ |
| ㉛ [DL] | ServerRainbowLeapObstacleDetect CS1061 修复：initData.StartPoint→rayStartPoint 字段 | ✅ |
| ㉜ [DL] | Temp_SetMeshBuilderRefs.cs 已确认执行成功并清理 | ✅ |
| ㉝ [DL] | 回调模式→OnSetEntityObj 自驱动模式：删除 OnComponentReady/roadBuildComp，BuildRoad 移入 OnSetEntityObj | ✅ |
| ㉞ [DL] | P0+P1 Review 修复(5项): 协程泄漏防护/_lifecycleRoutine、RecalculateNormals删除、三角形数组静态复用s_Triangles、GetComponent null检查、Renderer缓存跨池复用 | ✅ |
| ㉟ [DL] | 最终边界+性能审查完成：10项边界逐一确认、移除空OnLoadEntityEnd死代码、零编译错误 | ✅ |
| ㊱ [DL] | RainbowIslandCreateData + MaltCliff 添加 MotoSheep carSign Ratio=20 | ✅ |
| ㊲ [DL] | 彩虹飞跃测试计划文档创建(9大类70+用例) | ✅ |
| ㊳ [DL] | 1代架构载具制作规范沉淀(规范文档) | ✅ |
| ㊴ [PL] | 全量文档状态更新：开发计划/载具系统/Ability技术文档 → ✅ 开发完成 | ✅ |
| ㊲ [DL] | 彩虹飞跃测试计划文档创建(9大类70+用例) | ✅ |
| ㊳ [DL] | 1代架构载具制作规范沉淀(规范文档) | ✅ |
| ㊴ [PL] | 全量文档状态更新：开发计划/载具系统/Ability技术文档均更新为✅开发完成 | ✅ |
| ㊵ [DL] | M_SpawnDistance 5→3 + 速度倍率 1.5x/2x→2x/3x + CRITICAL#1 base.OnClear() 修复 | ✅ |
| ㊶ [DL] | SABC暂时屏蔽：地面检测(固定y-5f)+宽度检测(配置半宽)+障碍物截断(全量生成) | ✅ |
| ㊷ [DL] | SAB+SABC+CarNetServer水平化：forward ProjectOnPlane + _estimatedSpeedXZKmh(XZ-only速度) | ✅ |
| ㊸ [DL] | 技术文档同步更新：Ability文档(流程图+调试TODO表+速度机制)+载具文档(XZ速度字段) | ✅ |
| G1 [DL] | MotorCarController extraEngineTorque/extraShiftEngineTorque 扩展 + Car.cs HandleRainbowRoadEnter/Exit 增加扭矩 boost(+30%加速效率) | ✅ |
| G2 [DL] | SOCarSkill.txt: MotoSheep SkillCD=5→30, SkillTime=10→5（正式数值） | ✅ |
| G3 [DL] | CarNetServer.cs: 瞬时速度估算优化（_lastEstimateTime + 位置差值/实际时间差） | ✅ |
| G4 [DL] | 载具设计策划案修订：§五 斜坡长度 30m→50m【修订】 | ✅ |
| G5 [DL] | 全量验收清单生成：57项逐条比对策划案 vs 实现（45✅ 1⚠️ 4⚠️ 5❌ 1N/A） | ✅ |
| G6 [DL] | 性能分析报告：Mesh生成+网络+物理+GC 全链路分析（11章） | ✅ |
| P0-1 [DL] | Car.cs HandleRainbowRoadExit: GetComponentInParent→IsChildOf 优化（省100-300μs/次） | ✅ |
| P0-2 [DL] | RainbowRoad_Entity: WaitForSeconds 静态缓存（同duration复用，省1 alloc/次） | ✅ |
| G7 [DL] | PcRayColliderData.txt: 添加 MotoSheep0/MotoSheep1 条目（PC端射线交互碰撞盒） | ✅ |

## 文档产出清单
| 文档 | 路径 | 状态 |
|------|------|------|
| checklist.md | `aigc/harness/session-state/暴躁绵羊/checklist.md` | ✅ |
| active.md | `aigc/harness/session-state/暴躁绵羊/active.md` | ✅ |
| session-log.md | `aigc/harness/session-state/暴躁绵羊/session-log.md` | ✅ |
| 载具设计策划案：暴躁绵羊（修订版）.md | `aigc/docs/Gameplay_Designer/` | ✅ |
| 暴躁绵羊开发计划.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/` | ✅ |
| README.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/技术文档/` | ✅ |
| 暴躁绵羊-载具系统.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/技术文档/` | ✅ |
| 暴躁绵羊-彩虹飞跃Ability.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/技术文档/` | ✅ |
| CAB_RainbowLeapSystem.cs | `Assets/Script/Biubiubiu2/GamePlay/Client/Ability/System/CAB/` | ✅ |
| RainbowRoadMeshBuilder.cs | `Assets/Script/Biubiubiu2/GamePlay/Client/Ability/Component/Other/RainbowRoad/` | ✅ |
| RainbowRoad_Entity.cs | `Assets/Script/Biubiubiu2/GamePlay/Client/Ability/Component/Other/RainbowRoad/` | ✅ |
| AbilityM_RainbowLeap.csv | `Assets/ToBundle/Biubiubiu2/Configs/Ability/AB/` | ✅ |
| MotoSheep_MotorCarSetting.asset | `Assets/ToBundle/ScriptableObject/Vehicle/MotoSheep_MotorCarSetting.asset` | ✅ |
| MotoSheep.prefab | `Assets/ToBundle/Biubiubiu2/GamePlay/SausageMirrorAI/Server/MotoSheep.prefab` | ✅ |
| MotoSheep Skin Prefabs | `Assets/ToBundle/Skin/Cars/MotoSheep/MotoSheep/ (MotoSheep.prefab, MotoSheep_Low.prefab, MotoSheep_Spoiled.prefab)` | 🔄 |
| RainbowRoad.prefab | `Assets/ToBundle/Biubiubiu2/GamePlay/Ability/RainbowRoad.prefab` | ✅ |
| RainbowRoad_Mat.mat | `Assets/Art/Effects/Materials/RainbowRoad_Mat.mat` | ✅ |
| ClientRainbowLeapMeshBuild.cs | `Assets/Script/.../RainbowRoad/ClientRainbowLeapMeshBuild.cs` | ❌ 已删除 |
| 彩虹飞跃测试计划.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/彩虹飞跃测试计划.md` | ✅ |
| 暴躁绵羊-载具系统.md | `aigc/docs/GamePlay_Dev/暴躁绵羊/技术文档/暴躁绵羊-载具系统.md` | ✅ |
| 载具制作.md | `aigc/docs/GamePlay_Dev/sausage-framework/载具制作.md` | ✅ |
| 验收清单.md | `aigc/harness/session-state/暴躁绵羊/验收清单.md` | ✅ |
| 性能分析报告.md | `aigc/harness/session-state/暴躁绵羊/性能分析报告.md` | ✅ |

## 关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|
| 1 | 彩虹之路实现方式 | 使用AbilitySystem,BSORainbowBridge仅参考Mesh生成,客户端Mesh+服务端Ability状态 | 2026-04-09 |
| 2 | 能源系统 | 彩虹能源=基础汽油,不扩展消耗系统 | 2026-04-09 |
| 3 | modeMaxHp | 当前只配1230一档,结构预留多模式血量 | 2026-04-09 |
| 4 | 技能触发方式 | 第一阶段E键或GUI按钮,UI后续接入 | 2026-04-09 |
| 5 | 美术资源 | 拷贝PonyVehicle预制改名SheepVehicle,全部占位 | 2026-04-09 |
| 6 | 投放配置路径 | Vehicle.asset+SOCarData.txt+MotorCarSetting三处配置 | 2026-04-09 |
| 7 | 彩虹路中立性 | 彩虹路是中立动态道路,所有玩家和载具均可使用,无需特殊处理 | 2026-04-09 |
| 8 | 彩虹路地形碰撞 | 前方有障碍时停止生成,不穿墙 | 2026-04-09 |
| 9 | FOV过渡时间 | 2秒过渡,时间可配置,参考CameraController.SetCameraRatio | 2026-04-09 |
| 10 | 多次释放彩虹路 | 可叠加不覆盖,通过技能CD和彩虹路自身CD控制 | 2026-04-09 |
| 11 | SheepVehicle与MotoSheep关系 | SheepVehicle复用MotoSheep的ID和常量,替换MotoSheep | 2026-04-09 |
| 12 | AE→载具速度的生效链路 | 去掉AE_RainbowRoadBuff，改为RainbowRoad_Entity.OnTriggerEnter/Exit直接修改MotorCarController属性 | 2026-04-09 |
| 13 | MotorCarController修改策略 | 允许在MotorCarController中新增addMaxSpeed/addShiftSpeed字段+Set方法，GetMaxSpeed返回maxSpeed+addMaxSpeed。属于基础功能扩展，不需要子类 | 2026-04-09 |
| 14 | 加速效率(EngineTorque)boost实现 | 沿用extraMaxSpeed模式新增extraEngineTorque/extraShiftEngineTorque + protected virtual Get + public Set，Car.cs HandleRainbowRoadEnter通过BaseEngineTorque*SpeedBoostPct计算 | 2026-07-14 |
| 15 | Vehicle.asset投放方式 | MotoSheep只走随机生成(CreateData Ratio=20)，不需要Vehicle.asset固定刷新点 | 2026-07-14 |
| 16 | PcRayColliderData配置 | 复用PonyVehicle碰撞盒参数(InnerSize=1.18/1.33/1, InteractiveDistance=4)，MotoSheep0驾驶+MotoSheep1乘坐 | 2026-07-15 |

## Bug 记录
| # | 现象 | 根因 | 修复 | 状态 |
|---|------|------|------|------|
| 1 | ability-gen.sh生成AB后，ServerAbilityManager_SwitchAB和ClientAbilityManager_SwitchAB中缺少RainbowLeap的switch case | codegen工具只写入了14_Proto_AbilityAB_Auto.cs，未写入SwitchAB文件 | 手动补入两个switch case条目 | ✅ |
| 2 | RainbowRoadMeshBuilder和RainbowRoad_Entity缺少namespace | 创建文件时遗漏了namespace Sofunny.BiuBiuBiu2.ClientGamePlay | 补入命名空间 | ✅ |
| 14 | CAB_RainbowLeapSystem.cs 两个编译错误: SetGameObjectEntity() 缺参数, IEntity.GetGameObject() 不存在 | 未按 core-rules Rule 11 规范传参, EntityBase 方法名是 GetGameObj 不是 GetGameObject | SetGameObjectEntity(new GameObject(RainbowRoad), StageData.GameWorldLayerType.Ability) + iEnter.GetGameObj() | ✅ |
| 15 | rampLength被截断为2.28m，彩虹路Mesh近乎平无坡度角 | SABC射线从车中心出发，打到车自身碰撞体（约2.28m处） | 射线起点改为车前SpawnDistance(5m)处，即彩虹路实际生成位置 | ✅ |
| 16 | Mesh朝下，坡面时方向倾斜错误 | CAB forward包含俯仰角，LookRotation基于倾斜forward | Vector3.ProjectOnPlane(forward,up)水平化forward | ✅ |
| 17 | rampLen 被旁边车辆碰撞体截断（2.28m） | SABC 层级掩码 ~(1<<11) 只排了 Terrain，Car/CarHitPart/Role 层仍被检测到，导致附近车辆碰撞体截断射线 | 层级掩码改为 (1<<Default)|(1<<Terrain) 白名单模式，只检测结构性障碍物 | ✅ |
| 1 | CS1061: InitData 不包含 StartPoint 定义 | StartPoint 已改名为 RawStartPoint，但 DetectRampObstacle/DetectSprintObstacle 仍引用旧名 | 添加 rayStartPoint 字段缓存 ComputeRayStartPoint()，替换所有 initData.StartPoint 为 rayStartPoint | ✅ |
| 18 | SAB_RainbowLeapSystem.OnClear缺少base.OnClear() | 生成代码未自动添加base调用 | L31补回base.OnClear() | ✅ |

## 规范沉淀
5. **程序化 Entity 构建必须严格遵循 core-rules Rule 11: SetGameObjectEntity(go, layer) 需要传入 new GameObject 和 StageData.GameWorldLayerType; IEntity 的获取 GameObject 方法是 GetGameObj() 而非 GetGameObject(); 编码前必须读 core-rules.md 第四部分**
6. **上下文摘要恢复后，必须执行全局索引检查：先读 aigc/harness/session-state/active.md 确认当前活跃功能，若与用户指令不一致则立即更新索引。跳过此步会导致全局索引停留在旧功能**
1. **1代架构载具必须在SOCreateObjData/{地图}CreateData.asset中注册carSign+Ratio，否则不会在该地图生成**
1. **SOCreateObjData注册遗漏导致载具不生成——新增载具必须在目标地图的CreateData.asset中添加carSign+Ratio条目**

## ⚠️ 遗留待确认
- 功能命名待确定
