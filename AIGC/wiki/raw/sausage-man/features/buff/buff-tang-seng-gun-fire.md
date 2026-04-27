---
name: buff-tang-seng-gun-fire
display_name: BSTangSengGunFire - TangSengGunFire
category: buff/tangseng
version: 1.0.0
dependencies:
- buff-framework
---

# BSTangSengGunFire - TangSengGunFire

BSTangSengGunFire Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOTangSengGunFire.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSTangSengGunFire.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSTangSengGunFireClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSTangSengGunFireServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/TangSengGunFire/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
