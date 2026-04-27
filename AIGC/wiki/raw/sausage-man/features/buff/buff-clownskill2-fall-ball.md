---
name: buff-clownskill2-fall-ball
display_name: BSClownskill2FallBall - Clownskill2FallBall
category: buff/role-skill
version: 1.0.0
dependencies:
- buff-framework
---

# BSClownskill2FallBall - Clownskill2FallBall

BSClownskill2FallBall Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClownskill2FallBall.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownskill2FallBall.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownskill2FallBallClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownskill2FallBallServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Clownskill2/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
