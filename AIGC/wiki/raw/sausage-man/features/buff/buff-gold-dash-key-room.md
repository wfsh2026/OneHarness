---
name: buff-gold-dash-key-room
display_name: BSGoldDashKeyRoom - GoldDashKeyRoom
category: buff/golddash
version: 1.0.0
dependencies:
- buff-framework
---

# BSGoldDashKeyRoom - GoldDashKeyRoom

BSGoldDashKeyRoom Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGoldDashKeyRoom.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGoldDashKeyRoom.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGoldDashKeyRoomClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGoldDashKeyRoomServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GoldDash/` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/Buff/Common/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
