---
name: buff-boss-scene-air-wall
display_name: BSBossSceneAirWall - BossSceneAirWall
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSBossSceneAirWall - BossSceneAirWall

BSBossSceneAirWall Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBossSceneAirWall.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBossSceneAirWallServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 2 个文件。
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
