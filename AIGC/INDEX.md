# AIGC 通用角色入口

本目录的可提交内容只保存通用 AI 角色调度逻辑、项目接入机制和模板，不保存任何具体项目事实。

## 默认读取顺序

1. `AIGC/INDEX.md`
2. `AIGC/roles/INDEX.md`
3. `AIGC/roles/common/RULE.md`
4. `AIGC/roles/role-manager/RULE.md`
5. 角色管理员按任务命中的角色规则。
6. 需要目标项目事实时，由角色管理员按 `AIGC/roles/role-manager/project-adapter-routing.md` 读取本机 `AIGC/project-adapters/INDEX.md` 和命中的项目适配包。
7. 需要通用架构知识时，读取 `AIGC/wiki/INDEX.md`。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `roles/` | 角色库、角色管理员、通用角色规则和角色派发规则。 |
| `wiki/` | 给角色调度快速检索的通用知识库。 |
| `capabilities/` | 当前 AIGC 能力索引、版本和变更记录。 |
| `project-adapters/` | 本机项目适配包、项目专属角色、项目知识和运行记录；必须被 Git 忽略。 |
| `tharness.yaml` | 最小自检工具的配置入口。 |

历史项目资料不得保留在可提交的通用 AIGC 主分支；需要本机沉淀时写入 `AIGC/project-adapters/`，需要长期归档时使用独立归档仓库。

## 调度原则

- 所有用户请求先由角色管理员接收。
- 角色管理员是唯一主会话用户沟通者和唯一角色派发者。
- 具体角色任务必须通过 SubAgent 或全新会话执行。
- 执行角色只遵守通用最小规则、自己的角色规则和任务包允许读取的资料。
- Tharness 不保留独立质量门控阶段；验证、审查和交付判断由角色管理员按风险派发或判断。

## 不允许写入的内容

- 具体项目的运行记录。
- 具体项目的知识沉淀。
- 具体项目的决策事实。
- 具体项目的代码结构分析。

这些内容必须写入 `AIGC/project-adapters/{project_id}/` 下的本机项目适配包；该目录不得提交到 Git。
