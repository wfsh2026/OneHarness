---
name: buff-pve-add-hp
display_name: BSPveAddHp - PveAddHp
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveAddHp - PveAddHp

BSPveAddHp Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAddHp.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAddHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveAddHpClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveAddHpServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveAddHp/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
