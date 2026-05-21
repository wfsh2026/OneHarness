# 游戏策划方法卡索引

本目录保存游戏策划方法论的可执行卡片、来源登记和检索索引，不保存书籍原文、长摘录或具体项目玩法事实。

## 默认读取

1. `phase-index.md`。
2. `trigger-index.md`。
3. 命中的 `cards/*.md`。
4. 需要校准来源时读取 `source-index.md`。
5. 需要解释体系设计或维护规则时读取 `design-and-maintenance.md`。

## 文件

| 文件 | 用途 |
| --- | --- |
| `source-index.md` | 登记书籍来源、材料状态和方法卡入口。 |
| `public-source-notes.md` | 保存公开合法来源链接和基础提炼依据。 |
| `design-and-maintenance.md` | 说明方法卡体系的设计原理和维护更新规则。 |
| `phase-index.md` | 按策划阶段选择优先方法卡。 |
| `trigger-index.md` | 按用户表达选择追问、转译或检查动作。 |
| `source-material-intake.md` | 后续导入合法来源材料时的提炼流程。 |
| `cards/art-of-game-design.md` | 策划提问方法卡。 |
| `cards/designing-games.md` | 体验转译方法卡。 |
| `cards/game-mechanics.md` | 系统机制方法卡。 |
| `cards/game-feel.md` | 战斗手感方法卡。 |
| `cards/gamers-brain.md` | 用户理解方法卡。 |
| `cards/sprint.md` | 原型验证方法卡。 |
| `cards/mom-test.md` | 真实需求访谈方法卡。 |

## 状态

| 状态 | 含义 |
| --- | --- |
| `pending-source` | 已建立卡片槽位，等待合法来源材料校准；不能当作已验证书籍结论引用。 |
| `partial` | 已用部分合法来源材料提炼，覆盖范围有限。 |
| `verified` | 已由合法来源材料、章节锚点和提炼记录校准。 |
| `blocked` | 缺少合法来源材料，暂不能继续提炼。 |

## 使用边界

- 方法卡只保存策划判断、提问、转译和检查动作。
- 来源锚点只记录章节、页码、笔记编号或公开链接，不保存大段原文。
- 书籍材料必须放在仓库外或 `_sources/` 私有目录，且 `_sources/` 不提交 Git。
- 具体项目玩法、数值、关卡、角色和运行记录不得写入本目录。
