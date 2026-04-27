---
name: item-golddash
display_name: GoldDash道具变异系统
category: item/golddash
version: 1.0.0
dependencies:
- item-base
- mode-golddash
---

# GoldDash道具变异系统

GoldDash(淘金热)模式专属道具子系统：VariationCollection/VariationStrategy 实现道具品质变异（纯度/特效/体积/稀有度），GoldDashPickItem/GoldDashItemManager 管理 GoldDash 专属拾取与生成，含护甲/头盔/背包/保险箱多层级升级体系

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashCollectionMono.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashCollectionMonoBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashCollectionNoBoneMono.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashItemManagerData.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashItemUtil.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashPickItem.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashPickItemNet.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashPickItemNetClient.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldDashPickItemNetServer.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/GoldPickItemInfo.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/IGoldDashItemManager.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/IPickItemNetClientBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/IPickItemNetServerBase.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationBodyLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationEffectLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationNoBoneNodeLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationNodeLogic.cs` |
| `Assets/Script/GamePlay/Host/Modules/Item/GoldDash/VariationCollection/GoldDashVariationScaleLogic.cs` |
| `Assets/Script/GamePlay/Client/Modules/Item/GoldDash/ClientGoldDashItemManager.cs` |
| `Assets/Script/GamePlay/Client/Modules/IdTag/IdTagEffectControl.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/GoldDashVariationCore.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/ServerCollectionVariationManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/ServerGoldDashItemManager.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/ServerVariationInfo.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/BaseVariationStrategy.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/EffectVariationStrategy.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/PurityVariationStrategy.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/VariationStrategyData.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/VariationSystem.cs` |
| `Assets/Script/GamePlay/Server/Modules/Item/GoldDash/VariationStrategy/VolumeVariationStrategy.cs` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/GoldDashItem.txt [道具主表]` |
| `Assets/ToBundle/Config/Txt/GoldDashItemType.txt [道具类型]` |
| `Assets/ToBundle/Config/Txt/GoldDashItemTypeSet.txt [类型集合]` |
| `Assets/ToBundle/Config/Txt/GoldDashItemTypeSetContent.txt [集合内容]` |
| `Assets/ToBundle/Config/Txt/GoldDashItemConvertSausageItem.txt [道具转换]` |
| `Assets/ToBundle/Config/Txt/GoldDashItemCustomSize.txt [道具自定义尺寸]` |
| `Assets/ToBundle/Config/Txt/GoldDashBackpackBaseValue.txt [背包基础值]` |
| `Assets/ToBundle/Config/Txt/GoldDashBackpackLevel.txt [背包等级]` |
| `Assets/ToBundle/Config/Txt/GoldDashArmorLevel.txt [护甲等级]` |
| `Assets/ToBundle/Config/Txt/GoldDashHelmetBaseValue.txt [头盔基础值]` |
| `Assets/ToBundle/Config/Txt/GoldDashVestBaseValue.txt [护甲基础值]` |
| `Assets/ToBundle/Config/Txt/GoldDashKeyBagLevel.txt [钥匙包等级]` |
| `Assets/ToBundle/Config/Txt/GoldDashSafeBoxLevel.txt [保险箱等级]` |
| `Assets/ToBundle/Config/Txt/GoldDashBoxEffect.txt [箱子特效]` |
| `Assets/ToBundle/Config/Txt/GoldDashBoxItemEffect.txt [箱子道具特效]` |
| `Assets/ToBundle/Config/Txt/GoldDashMapCollectItem.txt [地图收集道具]` |
| `Assets/ToBundle/Config/Txt/GoldDashInteractAction.txt [交互动作]` |
| `Assets/ToBundle/Config/Txt/GoldDashInteractItemInfo.txt [交互道具信息]` |
| `Assets/ToBundle/Config/Txt/GoldDashWarItemSetContent.txt [战斗道具集]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollection.txt [收集系统]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionType.txt [收集类型]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionSeasonShow.txt [赛季展示]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionSeasonShowItem.txt [赛季展示道具]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationBase.txt [变异基础]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationClass.txt [变异等级]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationMod.txt [变异模组]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationModRand.txt [模组随机]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationModType.txt [模组类型]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationPart.txt [变异部件]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationPartRand.txt [部件随机]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationRand.txt [变异随机]` |
| `Assets/ToBundle/Config/Txt/GoldDashCollectionVariationShow.txt [变异展示]` |
| `Assets/ToBundle/Config/Txt/GoldDashPlayerAiFindBoxPriority.txt [AI找箱优先级]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/GoldDash/ [20 files, GoldDash道具模型]` |

## 备注

GoldDash 道具系统是该模式的核心玩法机制。VariationStrategy 实现类Diablo式的道具品质变异：BaseVariationStrategy(基础)→PurityVariationStrategy(纯度)→EffectVariationStrategy(特效)→VolumeVariationStrategy(体积)。VariationCollection 处理视觉变异在模型上的表现(Body/Effect/Node/Scale/NoBoneNode)。33 个配置txt覆盖道具/装备/收集/变异全体系

依赖：[[item-base]] · [[mode-golddash]]
