# BIU26 技术子文档索引

> 本目录归属于 `aigc/docs/GamePlay_Dev/BIU26/` 功能文档体系。

---

## Phase 1 子文档列表

| 序号 | 文件 | 负责 Agent | 职责范围 | 状态 |
|------|------|-----------|---------|------|
| 1 | [BIU26-模式系统.md](BIU26-模式系统.md) | 开发负责人 (DL) | ServerBIU26Mode 模式主循环 · FloatingWeaponManager（解锁+生成GPO） · CoinManager · ClientCoinHUD · Proto_BIU26 协议 | ✅ 已完成 v1.1 |
| 2 | [BIU26-极坐标刷怪器.md](BIU26-极坐标刷怪器.md) | GPO 工程师 | GPOM_BIU26Set · Gpo/GpoTypeSet/IGPOM 修改 · Switch 路由追加 · ServerBIU26SpawnerSystem · ServerBIU26MinionsSpawner · ClientBIU26SpawnerSystem · 双 Prefab | ✅ 代码已完成 |
| 3 | [BIU26-悬浮武器GPO.md](BIU26-悬浮武器GPO.md) | GPO 工程师 | GPOM_BIU26FloatingWeapon · GpoTypeSet新ID · Switch路由 · ServerBIU26FloatingWeaponSystem · ClientBIU26FloatingWeaponSystem · 双 Prefab | ✅ 代码已完成 |
| 4 | [BIU26-悬浮武器Ability.md](BIU26-悬浮武器Ability.md) | Ability 工程师 | BIU26_FloatingWeapon_Bullet（飞行子弹 + 单体伤害判定，复用 AB_TrackingMissle） | ✅ Phase 1 已完成（复用 UAVMissle 占位） |
| 5 | [BIU26-场景建设.md](BIU26-场景建设.md) | 场景建设工程师 | BIU26_Dev.unity + ServerBIU26_Dev.unity 双场景 | ✅ 已完成 |

## Phase 2 子文档列表

| 序号 | 文件 | 负责 Agent | 职责范围 | 状态 |
|------|------|-----------|---------|------|
| 6 | [BIU26-缩圈系统.md](BIU26-缩圈系统.md) | 开发负责人 (DL) | ServerBIU26ZoneSystem · 三圈时序 · 圈外掉血 · 进圈金币 · 客户端边界视觉 | ⬜ 待开发 |

---

## 阅读顺序建议

1. 先读 [主计划](../BIU26_开发计划.md)（M-01 循环图 + M-02 体验节点）
2. 再读各子文档（按分工认领对应文档）

---

*由 [DL] 于 2026-03-28 生成，2026-03-29 追加 Phase 2 索引*
