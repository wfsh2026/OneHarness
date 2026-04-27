---
name: buff-props-trigger
display_name: BSPropsTrigger - 道具特效触发
category: buff/item
version: 1.0.0
dependencies:
- buff-framework
---

# BSPropsTrigger - 道具特效触发

1代 Buff 系统 道具特效触发。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPropsTrigger.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPropsTrigger.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPropsTriggerServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPropsTriggerClient.cs` |

## 备注

key_fields: propsBoxType, sign. 继承自 BSOAddEffectObj.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
