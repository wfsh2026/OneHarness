---
name: buff-buff-create-car
display_name: BSBuffCreateCar - Buff触发生成载具
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSBuffCreateCar - Buff触发生成载具

1代 Buff 系统 Buff触发生成载具。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBuffCreateCar.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBuffCreateCar.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBuffCreateCarServer.cs` |

## 备注

key_fields: carSign. 继承自 BSRoleStateChange.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
