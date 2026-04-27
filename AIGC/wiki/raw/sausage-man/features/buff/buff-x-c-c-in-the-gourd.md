---
name: buff-x-c-c-in-the-gourd
display_name: BSXCCInTheGourd - XCCInTheGourd
category: buff/gourd
version: 1.0.0
dependencies:
- buff-framework
---

# BSXCCInTheGourd - XCCInTheGourd

BSXCCInTheGourd Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOXCCInTheGourd.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSXCCInTheGourd.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSXCCInTheGourdClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSXCCInTheGourdServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GourdAdsorbXCC/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
