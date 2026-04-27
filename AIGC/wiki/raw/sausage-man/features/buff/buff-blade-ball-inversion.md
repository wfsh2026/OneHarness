---
name: buff-blade-ball-inversion
display_name: BSBladeBallInversion - BladeBallInversion
category: buff/bladeball
version: 1.0.0
dependencies:
- buff-framework
---

# BSBladeBallInversion - BladeBallInversion

BSBladeBallInversion Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOBladeBallInversion.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSBladeBallInversion.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSBladeBallInversionClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSBladeBallInversionServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。
[纯代码Buff] BladeBall模式专属Buff，由模式逻辑直接实例化，无独立SO配置。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
