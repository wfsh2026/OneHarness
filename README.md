# Tharness

Tharness 是一套低 token、目标驱动的通用 AIGC 角色调度框架。

当前有效框架入口只在 `AIGC/` 下。默认从 `AIGC/INDEX.md` 开始读取，再进入角色库，由角色管理员负责沟通和派发。

## 默认读取

1. `AIGC/INDEX.md`
2. `AIGC/roles/INDEX.md`
3. `AIGC/roles/common/RULE.md`
4. `AIGC/roles/role-manager/RULE.md`
5. 角色管理员按任务命中的角色规则
6. 需要目标项目事实时，只从用户输入或任务包允许读取的当前工作区入口获取，不在 THarness 内建立额外接入层
7. 需要通用知识时，读取 `AIGC/wiki/INDEX.md`

禁止为了保险读取全部 wiki、全部历史资料或全部运行记录。

## 主要入口

| 路径 | 用途 |
| --- | --- |
| `AIGC/INDEX.md` | 通用框架入口。 |
| `AIGC/roles/INDEX.md` | 角色库和角色管理员入口。 |
| `AIGC/wiki/INDEX.md` | 通用架构 wiki 入口。 |
| `AIGC/capabilities/INDEX.md` | 当前能力索引。 |

## 可执行自检

当前仓库提供最小自检工具，用于把部分规则从“依赖 Agent 自觉”推进到“项目自己发现问题”。

```powershell
python tools/tharness.py doctor
python tools/tharness.py index --check
python tools/tharness.py index --write
python tools/tharness.py self-check --path AIGC/wiki/architecture/role-system.md --delivery
python tools/tharness.py check
```

入口脚本按自身位置定位 THarness 根目录，也可以从父项目直接执行：

```powershell
python THarness/tools/tharness.py check
```

## 项目快速启动锚点

THarness 可以作为独立版本化主工程使用，其他项目不需要复制 `AIGC/`。在目标项目目录部署轻量锚点：

```powershell
python D:\UnityDemo\THarness\tools\tharness.py project init --root F:\YourProject
```

之后在目标项目内启动：

```powershell
.\.tharness\start.ps1
```

也可以不部署锚点，直接对指定目录输出启动包：

```powershell
python D:\UnityDemo\THarness\tools\tharness.py project start --root F:\YourProject
```

启动锚点只记录 THarness 主工程路径和目标项目路径，不复制主工程。绑定会在目标项目根目录维护 `AGENTS.md` 桥接段，让 AI 在目标项目启动时先读取 THarness 主工程 `AGENTS.md` 和 `AIGC/INDEX.md`。通用框架、角色、规则、wiki、能力索引和工具改动写回 THarness 主工程；项目事实、项目代码、项目资源和项目专属决策留在目标项目。

## 可视化绑定工具

THarness 也提供 Rust 桌面绑定工具，用于通过界面选择目标项目目录并确认绑定：

```text
THarness-Binder.exe
```

源码位于 `tools/tharness-binder/`。打包后的应用放在 THarness 主目录 `THarness-Binder.exe`，可以直接双击启动。界面使用深色圆角扁平化设计，显示当前 THarness 主工程、目标项目文件夹选择按钮、`.tharness/` 与 `AGENTS.md` 绑定预览、确认绑定和关闭按钮。

配置入口是 `AIGC/tharness.yaml`。动态检查范围、必需入口、元数据字段和结构自检扫描规则都从该配置读取。

AI 修改 Tharness 自身时，按 `AIGC/roles/tharness-maintainer/skills/self-check.md` 的触发矩阵自动选择自检命令；也可以用 `self-check --path ... --delivery` 让工具输出本轮应运行的命令。交付前必须运行 `python tools\tharness.py check`。

## 边界

- 可提交的通用 AIGC 只保存通用角色、通用规则、通用 wiki、入口机制和模板。
- THarness 不保存具体项目事实、项目知识、项目决策、项目专属角色或运行记录。
- 具体项目信息只来自用户输入或任务包允许读取的当前工作区入口，不写入 THarness 通用层。
- 历史项目资料不得保留在主分支；需要追溯时从 Git 历史或独立归档仓库读取。
