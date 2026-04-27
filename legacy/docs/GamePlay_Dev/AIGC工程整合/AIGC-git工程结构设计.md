# AIGC 多项目 Git 工程结构设计

> **版本**：v2.0
> **日期**：2026-04-03
> **状态**：✅ 已实施

---

## 一、整体结构

```
~git/
├── aigc-framework/           ← 独立 git 仓库（AIGC 框架 master 来源）
├── Shotting-Duck-UGC/        ← 嘎嘎射击 UGC 版，独立 git
├── Shotting-Duck/            ← 嘎嘎射击主项目，独立 git
├── sausage-man/              ← 香肠派对，独立 git
```

各游戏项目 git 保持完全独立，成员正常 clone 自己的项目即可使用 AIGC 完整功能，无需任何额外操作。

---

## 二、aigc-framework 目录结构

```
aigc-framework/
├── AGENTS.md                          ← 同步到各项目根目录
├── local-env.json                     ← 本机路径配置（不进 git，.gitignore）
├── .gitignore
├── README.md
└── AIGC/
    ├── agents/                        ← 通用 Agent 定义
    ├── rules/                         ← 通用开发规则
    │   ├── INDEX.md
    │   ├── safety-rules.md
    │   ├── system-map.md
    │   ├── session-guide.md
    │   ├── lessons-learned.md
    │   ├── GamePlay_Dev/
    │   ├── QualityGate/
    │   └── Workflow/
    ├── skills/                        ← 通用技能文件
    ├── docs/
    │   └── GamePlay_Dev/
    │       ├── 范例文档/
    │       └── 内容边界定义/
    └── tools/
        ├── framework-sync/            ← 同步工具（不同步给游戏项目）
        │   ├── diff-aigc.sh           ← 只读分析，生成 diff-report.json
        │   ├── sync-aigc.sh           ← 执行同步，消费 diff-report.json
        │   ├── sync-config.json       ← 同步配置（项目key/exclude规则）
        │   └── diff-report.json       ← 临时产物（不进 git，.gitignore）
        ├── project-git-clone/         ← 各项目仓库拉取脚本
        └── mcps/                      ← MCP 工具说明
```

---

## 三、各游戏项目目录结构

```
{GameProject}/
├── AGENTS.md                ← 由 sync 覆盖同步
└── AIGC/
    ├── agents/              ← 由 sync 覆盖同步
    ├── rules/               ← 由 sync 同步（exclude 保护专属文件）
    ├── skills/              ← 由 sync 覆盖同步
    ├── docs/                ← 通用子目录由 sync 同步，专属子目录不碰
    ├── tools/               ← project-git-clone/ 和 mcps/ 由 sync 同步
    └── session-state/       ← 项目专属，sync 完全不碰
```

---

## 四、项目专属文件（sync exclude 保护）

| 项目 | 专属文件 / 目录 |
|------|--------------|
| shotting-duck-ugc | — （无 exclude，接收全部内容） |
| sausage-man | `rules/GamePlay_Dev/ugc-code.md`、`docs/GamePlay_Dev/biu2-framework/内容边界定义/UGC GPO 内容边界定义.md`、`skills/Gameplay_Designer/` 下4个专属文件 |
| shotting-duck | `rules/GamePlay_Dev/ugc-code.md`、`docs/GamePlay_Dev/biu2-framework/内容边界定义/UGC GPO 内容边界定义.md`、`skills/GamePlay_Dev/Art/` |
| 所有项目 | `rules/Workflow/workflow-framework.md`、`rules/Workflow/workflow-env-setup.md`（framework 仓库专属工作流）|
| 所有项目 | `session-state/`（各项目私有，sync 不碰）|

---

## 五、同步机制

**同步方向**：
- **framework → 游戏项目**：框架更新后推送到各游戏项目
- **游戏项目 → framework**：某项目沉淀了新的通用内容，手动复制到 framework 后再同步给其他项目

**触发**：手动执行，修改 `aigc-framework` 后运行。

**工具**：`aigc/harness/tools/framework-sync/`，需先 diff 分析、确认后再 sync 执行。

```bash
# 第一步：分析差异（只读）
bash aigc/harness/tools/framework-sync/diff-aigc.sh all

# 第二步：用户确认后执行同步
bash aigc/harness/tools/framework-sync/sync-aigc.sh all

# 支持单个项目
bash aigc/harness/tools/framework-sync/diff-aigc.sh shotting-duck-ugc
bash aigc/harness/tools/framework-sync/sync-aigc.sh shotting-duck-ugc
```

### sync 逻辑分三类

| 同步对象 | 策略 |
|---------|------|
| `AGENTS.md` | 直接覆盖 |
| `aigc/harness/agents/`、`aigc/harness/skills/`、`aigc/harness/rules/` | sync-config.json 配置 exclude 后覆盖 |
| `aigc/harness/tools/project-git-clone/`、`aigc/harness/tools/mcps/` | 覆盖同步 |
| `aigc/docs/GamePlay_Dev/biu2-framework/范例文档/`、`内容边界定义/` | 精确子目录同步 |
| `aigc/harness/tools/framework-sync/` | **不同步**（framework 专属工具）|
| `aigc/harness/session-state/` | **不同步**（各项目私有）|

---

## 六、日常工作流

### 6.1 更新 AIGC 框架后同步

```
1. 在 aigc-framework 修改对应文件
2. bash aigc/harness/tools/framework-sync/diff-aigc.sh all   ← 查看差异
3. 确认无误后执行同步
4. bash aigc/harness/tools/framework-sync/sync-aigc.sh all
5. 各游戏项目 git add + git commit（用户手动执行）
6. aigc-framework git add + git commit（用户手动执行）
```

### 6.2 新增项目接入

```
1. 在 sync-config.json 的 projects 追加新项目 key + exclude
2. 在 local-env.json 追加新项目本机路径
3. bash aigc/harness/tools/framework-sync/diff-aigc.sh [新项目key]
4. bash aigc/harness/tools/framework-sync/sync-aigc.sh [新项目key]
5. 新项目 git add + git commit（用户手动执行）
```

### 6.3 修改 exclude 规则

```
1. 修改 aigc/harness/tools/framework-sync/sync-config.json
2. 重新运行 diff-aigc.sh 验证效果
3. 确认无误后执行 sync-aigc.sh
```

---

## 七、版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | 初版，基于方案迭代 v1～v5 设计结论 |
| v1.1 | 2026-04-03 | tools/ 移入 AIGC/ 目录下，与 agents/rules/skills 并列 |
| v2.0 | 2026-04-03 | 工程已实施；工具链升级为 diff+sync 双脚本；目录结构更新；local-env.json 分离本机路径；rules/ 子目录整理 |
