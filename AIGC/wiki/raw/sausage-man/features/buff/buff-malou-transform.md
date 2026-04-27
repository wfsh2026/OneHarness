---
name: buff-malou-transform
display_name: BSMalouTransform - MalouTransform
category: buff/malouparty
version: 1.0.0
dependencies:
- buff-framework
---

# BSMalouTransform - MalouTransform

BSMalouTransform Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOMalouTransform.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSMalouTransform.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSMalouTransformClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSMalouTransformServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/AddEffect/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
