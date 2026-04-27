---
name: item-loot
display_name: 掉落与空投系统
category: item/loot
version: 1.0.0
dependencies:
- item-base
---

# 掉落与空投系统

道具掉落分配全链路：LootBag/LootGroup/LootItem 多层随机掉落表，WarDropItem 空投/战利品投放，SplitItem 网格化道具分发(C/S 双端+7 通道 NetworkSync)，AdaptDropRate 自适应掉率。覆盖道具从生成到玩家拾取的分配逻辑

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/Item/ClientSplitItem.cs [客户端网格道具]` |
| `Assets/Script/GamePlay/Client/Modules/Item/ClientSplitItem_PickItemData.cs [网格道具数据]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItem.cs [服务端网格道具]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItem_GridData.cs [网格单元数据]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync.cs [主同步编排器]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_ItemData.cs [道具数据同步]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_PickItem.cs [拾取同步]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_RoleData.cs [角色背包同步]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_AirThrow.cs [空投同步]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_SceneDeadItemBox.cs [尸体箱同步]` |
| `Assets/Script/GamePlay/Server/Modules/Item/ServerSplitItemNetworkSync_PirateShip.cs [海盗船道具同步]` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/LootBag.txt [掉落容器定义]` |
| `Assets/ToBundle/Config/Txt/LootGroup.txt [掉落组]` |
| `Assets/ToBundle/Config/Txt/LootGroupType.txt [掉落组类型]` |
| `Assets/ToBundle/Config/Txt/LootItem.txt [掉落道具]` |
| `Assets/ToBundle/Config/Txt/LootRandom.txt [随机掉落表]` |
| `Assets/ToBundle/Config/Txt/LootRandomReduced.txt [缩减随机掉落]` |
| `Assets/ToBundle/Config/Txt/WarDropItem.txt [空投道具定义]` |
| `Assets/ToBundle/Config/Txt/WarDropItemContent.txt [空投内容物]` |
| `Assets/ToBundle/Config/Txt/WarDropItemEffect.txt [空投特效]` |
| `Assets/ToBundle/Config/Txt/WarDropItemProbability.txt [空投概率]` |
| `Assets/ToBundle/Config/Txt/AiDropMap.txt [AI掉落点位]` |
| `Assets/ToBundle/Config/Txt/AdaptDropRate.txt [自适应掉率]` |
| `Assets/ToBundle/Config/Txt/GoldPickItem.txt [金币拾取道具]` |
| `Assets/ToBundle/Config/Txt/PveItemBase.txt [PvE道具基础]` |
| `Assets/ToBundle/Config/Txt/PveItemOutput.txt [PvE道具产出]` |
| `Assets/ToBundle/ScriptableObject/ItemSpawn/ [12 files, 道具生成点SO — 含 AirDrop/ 空投定义]` |

## 备注

SplitItem 是网格化道具分发系统，将地图划分为多个网格区域，按需向客户端同步附近道具。NetworkSync 有 7 个专属通道：ItemData/PickItem/RoleData/AirThrow/SceneDeadItemBox/PirateShip。LootBag→LootGroup→LootItem 构成三层掉落表体系，LootRandom 和 AdaptDropRate 支持动态掉率调整

依赖：[[item-base]]
