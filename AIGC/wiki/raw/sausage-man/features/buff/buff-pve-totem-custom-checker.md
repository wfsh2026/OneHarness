---
name: buff-pve-totem-custom-checker
display_name: BSPveTotemCustomChecker - PveTotemCustomChecker
category: buff/pve
version: 1.0.0
dependencies:
- buff-framework
---

# BSPveTotemCustomChecker - PveTotemCustomChecker

BSPveTotemCustomChecker Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOPveTotemCustomChecker.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSPveTotemCustomChecker.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSPveTotemCustomCheckerServer.cs` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 3 个文件。
[纯代码Buff] Totem机制实现层，SO配置由对应的BSOTotem*类管理，本Buff仅提供运行时逻辑。共享配置通过buff-framework依赖继承。

依赖：[[buff-framework]]
