---
name: buff-pve-bullet-go-through-ability
display_name: BSPveBulletGoThroughAbility - PveBulletGoThroughAbility
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveBulletGoThroughAbility - PveBulletGoThroughAbility

BSPveBulletGoThroughAbility Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveBulletGoThroughAbility.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveBulletGoThroughAbility.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveBulletGoThroughAbilityClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveBulletGoThroughAbilityServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。
[纯代码Buff] PVE Rogue模式专属，由Totem系统触发，无独立SO配置。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
