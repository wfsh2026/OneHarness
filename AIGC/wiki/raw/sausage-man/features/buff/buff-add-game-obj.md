---
name: buff-add-game-obj
display_name: BSAddGameObj - 加载游戏物体（直接引用 GameObject）
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddGameObj - 加载游戏物体（直接引用 GameObject）

1代 Buff 系统 加载游戏物体（直接引用 GameObject）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddGameObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddGameObj.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddGameObjServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddGameObjClient.cs` |

## 备注

routing: GameLoop. key_fields: gameObj (GameObject ref), LifeTime.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
