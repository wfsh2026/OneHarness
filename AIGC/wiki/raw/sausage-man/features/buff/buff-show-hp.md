---
name: buff-show-hp
display_name: BSShowHP - 显示血条/Debuff UI
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSShowHP - 显示血条/Debuff UI

1代 Buff 系统 显示血条/Debuff UI。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOShowHP.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSShowHP.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSShowHPServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSShowHPClient.cs` |

## 备注

routing: GameLoop. key_fields: DebuffUiSign, EffectSign, hpScaleNum, Offset, LifeTime.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
