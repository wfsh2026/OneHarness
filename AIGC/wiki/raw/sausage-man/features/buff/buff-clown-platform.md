---
name: buff-clown-platform
display_name: BSClownPlatform - 小丑平台同BSSandPlatform结构
category: buff/misc
version: 1.0.0
dependencies:
- buff-framework
---

# BSClownPlatform - 小丑平台同BSSandPlatform结构

1代 Buff 系统 小丑平台同BSSandPlatform结构。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOClownPlatform.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSClownPlatform.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSClownPlatformServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSClownPlatformClient.cs` |

## 备注

key_fields: EffectRange, LifeTime, StartPlatformTime, PlatformHeight, GlideMoveStateBuff, EndBuff等.
[纯代码Buff] 特定玩法模式专属Buff，由模式逻辑直接实例化，无独立SO配置。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
