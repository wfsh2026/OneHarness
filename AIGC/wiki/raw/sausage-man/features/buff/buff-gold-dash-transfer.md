---
name: buff-gold-dash-transfer
display_name: BSGoldDashTransfer - GoldDashTransfer
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashTransfer - GoldDashTransfer

BSGoldDashTransfer Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashTransfer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashTransfer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashTransferClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashTransferServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/AddEffect_GoldDashTransfer.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/BSOGoldDashTransfer.asset` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
