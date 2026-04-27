# Session State 索引

> **用途**：标识当前活跃的开发功能，供各 Agent 新会话启动时定位正确的 active.md。

## 当前活跃功能

**功能**：Knowledge 知识库构建（system-map + features 全量梳理）
**active.md 路径**：`aigc/harness/session-state/knowledge构建/active.md`

---

## 所有功能目录

| 功能 | 路径 | 状态 |
|------|------|------|
| 暴躁绵羊 | `aigc/harness/session-state/暴躁绵羊/active.md` | 🔄 Phase 2 彩虹飞跃调试中（Bug#15/16 已修复，待游戏验证）|
| BIU26 | `aigc/harness/session-state/BIU26/active.md` | 🔄 阶段2 需求深度分析（刚启动）|
| BattleRoleLogic重构 | `aigc/harness/session-state/BattleRoleLogic重构/active.md` | 🔄 4A 7/7 完成 — 4B 待开始（TeammateBehavior + States 类型提取）|
| Knowledge 知识库构建 | `aigc/harness/session-state/knowledge构建/active.md` | 🔄 Phase 1 技术方案已创建，待审阅 |

---

## Agent 使用规范

1. **新会话启动时**：先读本文件（索引），找到"当前活跃功能"的 active.md 路径，再读取对应文件
2. **功能切换/新功能启动时**：若用户指令对应的功能与索引不一致，由 **Session Recorder** 负责：
   - 在 `session-state/{新功能}/` 下创建新 active.md
   - 更新本索引的"当前活跃功能"指向新功能
3. **写入规范**：所有功能子目录的 active.md 和本索引，均由 Session Recorder 专职维护，其他 Agent 不得直接修改
