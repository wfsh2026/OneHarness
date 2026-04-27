---
name: buff-play-box-line
display_name: BSPlayBoxLine - 箱子连线解谜
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSPlayBoxLine - 箱子连线解谜

1代 Buff 系统 箱子连线解谜。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPlayBoxLine.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPlayBoxLine.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPlayBoxLineServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPlayBoxLineClient.cs` |

## 备注

key_fields: moveBuff:BuffSOBase.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
