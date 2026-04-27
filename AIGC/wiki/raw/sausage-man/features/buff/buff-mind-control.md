---
name: buff-mind-control
display_name: BSMindControl - 精神控制三阶段
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSMindControl - 精神控制三阶段

1代 Buff 系统 精神控制三阶段。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOMindControl.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSMindControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMindControlServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMindControlClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: LastTime, BallSpeed, FxBallStart, FxBallLoop, FxBallOver, RoleSkillFx等.

依赖：[[buff-framework]]
