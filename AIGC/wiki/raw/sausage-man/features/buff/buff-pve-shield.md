---
name: buff-pve-shield
display_name: BSPveShield - PveShield
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveShield - PveShield

BSPveShield Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveShield.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveShield.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveShieldClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveShieldServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/PveShield/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
