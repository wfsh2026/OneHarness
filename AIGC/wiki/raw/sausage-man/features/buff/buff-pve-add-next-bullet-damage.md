---
name: buff-pve-add-next-bullet-damage
display_name: BSPveAddNextBulletDamage - PveAddNextBulletDamage
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveAddNextBulletDamage - PveAddNextBulletDamage

BSPveAddNextBulletDamage Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAddNextBulletDamage.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAddNextBulletDamage.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveAddNextBulletDamageServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。
[纯代码Buff] PVE Rogue模式专属，由Totem系统触发，无独立SO配置。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
