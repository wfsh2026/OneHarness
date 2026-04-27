---
name: buff-pve-auto-recover-hp
display_name: BSPveAutoRecoverHp - PveAutoRecoverHp
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveAutoRecoverHp - PveAutoRecoverHp

BSPveAutoRecoverHp Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAutoRecoverHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAutoRecoverHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveAutoRecoverHpServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveAutoRecoverHp/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。

依赖：[[buff-framework]]
