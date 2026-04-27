---
name: buff-manual-add-speed
display_name: BSManualAddSpeed - 手动增加速度
category: buff/movement
version: 1.0.0
dependencies:
- buff-framework
---

# BSManualAddSpeed - 手动增加速度

1代 Buff 系统 手动增加速度。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOManualAddSpeed.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSManualAddSpeed.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSManualAddSpeedServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSManualAddSpeedClient.cs` |

## 备注

[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
