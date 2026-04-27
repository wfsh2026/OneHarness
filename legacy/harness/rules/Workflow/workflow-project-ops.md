# 工作流：项目运维操作 (workflow-project-ops.md)

> 工作流类型：项目运维
> 适用场景：拉取代码、切换分支、更新 git。适用于所有仓库（aigc-framework 自身 + 各游戏项目）。
> 通用 session 记录规范见：[[session-guide]]
> 工具配置见：`aigc/harness/tools/project-git-clone/`

---

## 一、完整流程图

```
  用户侧                                    AI 侧
  ──────                                    ─────

1. 发起运维请求
   ├─ 帮我切换到 xxx 分支
   ├─ 拉取最新代码
   ├─ 更新到 develop / main
   └─ 切到 xxx tag
        │
        ▼
                            2. 识别当前仓库 + 目标项目
                            ├─ 读取 README.md 确认当前仓库
                            ├─ 确认目标分支/tag（用户已说明则直接使用）
                            └─ 定位对应脚本（见 §三 对应表）

                            3. 输出流程声明
                            → 进入 [项目运维] 工作流
                            → 操作：{切换/拉取} 分支 {branch}
                            → 脚本：harness/tools/project-git-clone/{script}.sh
                            → session-state：不建立
        │
        ▼
4. 用户已明确指令 → 直接执行；未明确分支 → ask_user 确认
        │
        ▼
                            5. 执行脚本
                            bash aigc/harness/tools/project-git-clone/{script}.sh {branch} [tag]

                            6. 汇报结果
                            ├─ 输出各模块成功/失败状态
                            └─ 失败时说明模块名和日志路径
```

---

## 二、强制等待原则

| 阶段 | 强制等待 | 禁止行为 |
|------|---------|---------|
| 分支/tag 未明确时 | ask_user 确认目标分支 | 不得猜测分支名自行执行 |
| 用户已明确目标分支 | 直接执行，无需再次确认 | 不得以「需要确认」为由拒绝执行 |
| 执行完成后 | 内联输出结果摘要 | 不得执行 git commit / push 等写操作 |

---

## 三、项目 → 脚本 对应表

| 项目 | 脚本 | AI 执行 timeout |
|------|------|----------------|
| aigc-framework | `aigc/harness/tools/project-git-clone/aigc-framework.sh` | 60s |
| Shotting-Duck-UGC | `aigc/harness/tools/project-git-clone/shotting-duck-ugc.sh` | 120s |
| Shotting-Duck | `aigc/harness/tools/project-git-clone/shotting-duck.sh` | 120s |
| sausage-man | `aigc/harness/tools/project-git-clone/sausage-man.sh` | 300s |

---

## 四、工具调用规范

```bash
# 切换分支
bash aigc/harness/tools/project-git-clone/sausage-man.sh develop

# 切换到指定 tag
bash aigc/harness/tools/project-git-clone/sausage-man.sh main v1.1.0

# framework 自身更新
bash aigc/harness/tools/project-git-clone/aigc-framework.sh main
```

> ⚠️ 脚本会执行 git stash，执行前确认工作区无需保留的改动。
> ⚠️ AI 禁止执行任何 git commit / push 操作。

---

## 五、禁止行为

- ❌ 禁止在用户未说明分支时自行猜测分支名
- ❌ 禁止执行任何 `git commit` / `git push` / `git merge` 等写操作
- ❌ 禁止将「切换分支/拉取代码」与「framework 同步」混淆——用户说切换分支时，禁止执行 `frameworkToProject-diff.sh` 或 `frameworkToProject-sync.sh`
- ❌ 用户已明确说明目标分支时，禁止再次要求用户确认，应直接执行
