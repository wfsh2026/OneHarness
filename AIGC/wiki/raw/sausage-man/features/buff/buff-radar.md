---
name: buff-radar
display_name: BSRadar - 雷达扫描
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSRadar - 雷达扫描

1代 Buff 系统 雷达扫描。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSORadar.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSRadar.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSRadarServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSRadarClient.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/Skills/` |

## 备注

key_fields: SweepSpaceTime, SweepRange, UpOffest, DwonOffest, sign, SkyEffectPointY, roleEffect:BuffSOBase. 继承自 BSOAddEffectObj.

依赖：[[buff-framework]]
