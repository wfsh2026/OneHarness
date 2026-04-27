---
name: item-activity
display_name: 战场活动道具系统
category: item/activity
version: 1.0.0
dependencies:
  - item-base
  - buff-framework
---

# 战场活动道具系统

管理 ItemType.ActivityItems(738197504) 的战场活动道具：节日/活动限定的可拾取道具（粽子/红包/鞭炮/灯笼/KFC 等），通过 ActivityItemSkinConfig 实现活动道具皮肤映射（Sign→WarSign→PrefabName），拾取后触发对应 Buff 效果。各活动道具复用 PickItemNet 框架，差异仅在 Prefab 模型和 Buff 配置

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/Config/ActivityItemSkinConfig.cs` | 活动道具皮肤配置管理 — Sign/WarSign/PrefabName 三字段映射，从 ActivityItemSkin.txt 加载 |
| `Assets/Script/Config/ActivityItemSkinConfig_Part.cs` | 配置扩展 — GetByWarSign() 反查接口，支持从战场标识反查活动道具配置 |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/ActivityItemSkin.txt` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityZongZi.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityShovel.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityRockJelly.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityRedPacket.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityPizza.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityFunnyBox.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityBell.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityFirecrackers.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityLamp.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityBelial.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityEgg.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityFoolBox.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityFoolBox1.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityKFC.prefab` |
| `Assets/ToBundle/GamePlayItem/PickItems/ActivityFairyStick.prefab` |

## 关联 Buff

### 活动道具专属 Buff（1）

| feature | 说明 |
|---------|------|
| [[buff-fairy-stick]] | 仙女棒活动道具 Buff |

## 备注

ActivityItems 是战场活动道具的统一 ItemType(738197504)。拾取由 item-base 的 PickItemNet 框架处理，ActivityItemSkinConfig 负责将道具 Sign 映射到 WarSign 和 PrefabName。各活动道具无独立控制器代码，差异仅在 Prefab 模型和绑定的 Buff SO 配置。ItemData.SortActivityItemsLevel1() 控制拾取优先级排序。URI.cs 通过 ItemData.ActivityItems 常量路由到 ActivityItems/ 资源目录

依赖：[[item-base]] · [[buff-framework]]
