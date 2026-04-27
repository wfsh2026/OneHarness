---
name: buff-add-server-scene-obj
display_name: BSAddServerSceneObj - 服务器场景物体生成
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSAddServerSceneObj - 服务器场景物体生成

1代 Buff 系统 服务器场景物体生成。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOAddServerSceneObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSAddServerSceneObj.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSAddServerSceneObjServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSAddServerSceneObjClient.cs` |

## 备注

routing: Server + Client. key_fields: sceneObjResPath.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
