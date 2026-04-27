---
name: buff-drop-level
display_name: BSDropLevel - 等级下降
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSDropLevel - 等级下降

1代 Buff 系统 等级下降。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSODropLevel.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSDropLevel.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSDropLevelServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSDropLevelClient.cs` |

## 备注

key_fields: DownSpeed, UpSpeed, MaxDownHeight.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
