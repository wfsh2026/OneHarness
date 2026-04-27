---
name: buff-gourd-adsorb
display_name: BSGourdAdsorb - GourdAdsorb
category: buff/gourd
version: 1.0.0
dependencies:
- buff-framework
---

# BSGourdAdsorb - GourdAdsorb

BSGourdAdsorb Buff 实现，包含 BSO 配置 + BS 逻辑 + 三端实现。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOGourdAdsorb.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSGourdAdsorb.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSGourdAdsorbClient.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSGourdAdsorbServer.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/ScriptableObject/Buff/GourdAdsorbXCC/` |

## 备注

三层架构: BSO(ScriptableObject) + BS(Host逻辑) + Client/Server。共 4 个文件。

依赖：[[buff-framework]]
