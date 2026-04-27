---
name: buff-gold-dash-scene-transfer
display_name: BSGoldDashSceneTransfer - GoldDashSceneTransfer
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashSceneTransfer - GoldDashSceneTransfer

BSGoldDashSceneTransfer Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashSceneTransfer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashSceneTransfer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashSceneTransferClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashSceneTransferServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffectObj/AddEffect_GoldDashSceneTransfer.asset` |
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/BSOGoldDashSceneTransfer.asset` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
