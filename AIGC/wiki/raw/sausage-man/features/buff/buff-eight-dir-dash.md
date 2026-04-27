---
name: buff-eight-dir-dash
display_name: BSEightDirDash - 八方向冲刺+拖尾
category: buff/movement
version: 1.0.0
dependencies:
- buff-framework
---

# BSEightDirDash - 八方向冲刺+拖尾

1代 Buff 系统 八方向冲刺+拖尾。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOEightDirDash.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSEightDirDash.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSEightDirDashServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSEightDirDashClient.cs` |

## 备注

key_fields: SprintDistance, Curve, SprintTrailEffect.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
