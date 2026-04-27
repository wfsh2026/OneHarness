---
name: idcard-framework
display_name: 身份卡系统框架 - IdCard Framework
category: idcard
version: 1.0.0
dependencies:
- role-equipment
---

# 身份卡系统框架 - IdCard Framework

身份卡系统的基础设施层，包含配置解析（IdCardSkinConfig/SORoleSkillConfig）、皮肤换装系统（12部位时装）、技能UI框架（RoleSkill/UIRoleSkill）、网络同步（IdCardSkinData）。每张身份卡提供2个技能，通过BSO/BS架构实现，本框架管理卡片的拾取、装备、皮肤替换和技能UI渲染。

## 代码文件

| 路径 |
|------|
| `Assets/Script/Config/IdCardSkinConfig.cs [身份卡皮肤配置解析，字段: id/IdCardSign/Clips]` |
| `Assets/Script/Config/IdCardSkinFashionConfig.cs [身份卡时装配置，12部位: Head/Hair/Shirt/Bottoms/Shoe/Coat等]` |
| `Assets/Script/Config/Partial/PartialIdCardSkinConfig.cs [皮肤动画Clip查询扩展方法]` |
| `Assets/Script/Config/SORoleSkillConfig.cs [技能配置解析，22字段: SkillSign/Cooldown/SkillCardType/PrefabName等]` |
| `Assets/Script/Data/Base/IdentityCardSkinEquip.cs [身份卡皮肤装备DTO: ItemId/SkinId/SkinSign/SkinIndex]` |
| `Assets/Script/GamePlay/Client/Modules/Role/RoleLogicClient/RoleLogicClient_IdCardSkin.cs [客户端身份卡换皮核心: Image/Effect/ItemAsset/Car/Sound/Material/Fashion/AnimationClip替换]` |
| `Assets/Script/GamePlay/Host/Network/Proto/Base/Struct/ProtoStruct_RoleData_IdCardSkinData.cs [身份卡皮肤网络同步协议: ItemId/SkinId/SkinIndex]` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkill.cs [战场技能管理: 拾取/装备/移除身份卡，管理RoleSkillEffect]` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillBase.cs [技能表现层基类: Init/OnDown/OnDrag/OnUp/CmdUseSkill/ResetCD]` |
| `Assets/Script/UI/War/Role/RoleSkill/RoleSkillEffect.cs [技能头顶特效: OnEquipIDCard/OnClearEffect/AddSkillHeadEffect]` |
| `Assets/Script/UI/PlayerControl/Skill/Base/UIRoleSkillBase.cs [技能UI基类]` |
| `Assets/Script/UI/PlayerControl/Skill/Base/IUIRoleSkill.cs [技能UI接口]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillMgr.cs [技能UI管理器]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillInstant.cs [瞬发技能UI]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillState.cs [状态技能UI]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillStateForever.cs [持续状态技能UI]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillThrow.cs [投掷技能UI]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillExpandUI.cs [扩展技能UI]` |
| `Assets/Script/UI/PlayerControl/Skill/UIRoleSkillBase_ATEvent.cs [技能按钮事件处理]` |
| `Assets/Script/UI/PlayerControl/UIRoleSkillSpecial.cs [特殊技能控制]` |

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/SORoleSkill.txt [技能配置表: SkillSign/Cooldown/SkillCardType绑定身份卡]` |
| `Assets/ToBundle/Config/Txt/IdCardSkin.txt [身份卡皮肤动画配置]` |
| `Assets/ToBundle/Config/Txt/IdCardSkinFashion.txt [身份卡时装12部位配置]` |
| `Assets/ToBundle/Config/Txt/ItemAsset.txt [物品资源映射(含29张IDCard_*条目)]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Items/Equipment/FunctionalGarment/ [身份卡预制体目录: IDCard_*.prefab]` |
| `Assets/ToBundle/Items/Stunt/BombIdCardSkin/ [身份卡皮肤特效预制体]` |
| `Assets/ToBundle/UGUI/Sprite/CrystalStore/IdCard.png [商城身份卡图标]` |

## 备注

29张身份卡，20张有SkillCardType映射(1-24)，9张无映射(含联动卡Geed/Taiga/Tiga/Zero/Zeta)。每卡2技能通过BS三端架构实现(Client/Server/Host)。技能类型: 瞬发(Instant)/状态(State)/投掷(Throw)/持续(StateForever)。皮肤系统支持替换: 图片/特效/道具模型/载具/音效/材质/时装/动画。SORoleSkillConfig.SkillCardType字段将技能绑定到身份卡类型(1=Hades, 2=Neptune, ..., 24=TangSeng)。

依赖：[[role-equipment]]
