---
name: buff-cyber-titan-shield
display_name: BSCyberTitanShield - CyberTitanShield
category: buff/cybertitan
version: 1.0.0
dependencies:
- buff-framework
---

# BSCyberTitanShield - CyberTitanShield

BSCyberTitanShield Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOCyberTitanShield.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSCyberTitanShield.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSCyberTitanShieldClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSCyberTitanShieldServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/DownHpObj/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
