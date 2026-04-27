---
name: buff-pve-add-attr-in-duration
display_name: BSPveAddAttrInDuration - PveAddAttrInDuration
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveAddAttrInDuration - PveAddAttrInDuration

BSPveAddAttrInDuration Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveAddAttrInDuration.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveAddAttrInDuration.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSPveAddAttrInDurationClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveAddAttrInDurationServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。
[纯代码Buff] PVE Rogue模式专属，由Totem系统触发，无独立SO配置。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
