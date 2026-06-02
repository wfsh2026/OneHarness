---
id: role-tharness-maintainer-self-check
title: 自检触发规则
role: Tharness 能力维护员
phase: self-check
read_when: 本轮修改影响 AIGC 文档、角色规则、自检工具、配置或准备交付时。
updated: 2026-05-20
---

# 自检触发规则

## 结论

修改 Tharness 自身时，Agent 必须按影响范围自动运行对应自检命令，并把结果写入验证或交付说明。

## 触发矩阵

| 修改范围 | 必须运行 |
| --- | --- |
| `AIGC/wiki/**` | `python tools\tharness.py index --check` |
| `AIGC/roles/**` | `python tools\tharness.py check` |
| `AIGC/capabilities/**` | `python tools\tharness.py doctor` |
| `AIGC/tharness.yaml` | `python tools\tharness.py check` |
| `tools/**` | `python tools\tharness.py check` 和 `python -m unittest tools.test_tharness` |
| 交付前 | `python tools\tharness.py check` |

## 执行规则

1. 先按修改范围选择最小命令。
2. 多个范围命中时，运行所有命中的命令。
3. 交付前始终运行 `python tools\tharness.py check`。
4. 命令失败时，先修复失败项，再重新运行。
5. 无法运行命令时，必须说明原因、影响和替代检查。

## 工具辅助

不确定命中范围时，使用 `self-check` 命令让工具输出应运行命令：

```powershell
python tools\tharness.py self-check --path AIGC/wiki/architecture/role-system.md --delivery
```

## 禁止

- 禁止把未运行自检写成已通过。
- 禁止为了自检读取无关历史资料。
- 禁止把一次性命令输出写入 wiki 正文。
