---
name: weapon-skin
display_name: 武器皮肤与外观系统
category: weapon/skin
version: 1.0.0
dependencies:
- weapon-base
---

# 武器皮肤与外观系统

武器视觉定制：武器皮肤特效(WeaponSkinEffect)、神话级皮肤(WeaponMythSkinEffect)、淘汰特效(WeaponEliminateEffect)、大厅皮肤展示(LobbyWeaponSkinEffect)、随机枪皮(RandomGunSkin)、武器升级外观(SOWeaponUp)

## 配置文件

| 路径 |
|------|
| `Assets/ToBundle/Config/Txt/WeaponSkinEffect.txt [武器皮肤特效映射]` |
| `Assets/ToBundle/Config/Txt/WeaponMythSkinEffect.txt [神话级皮肤特效]` |
| `Assets/ToBundle/Config/Txt/WeaponEliminateEffect.txt [淘汰特效配置]` |
| `Assets/ToBundle/Config/Txt/LobbyWeaponSkinEffect.txt [大厅武器皮肤展示]` |
| `Assets/ToBundle/Config/Txt/SOWeaponUp.txt [武器升级外观 SO]` |

## 资源文件

| 路径 |
|------|
| `Assets/ToBundle/Effect/RandomGunSkin/ [3 files, 随机枪皮特效]` |

## 备注

武器皮肤是纯配置+资产驱动的系统，无独立代码模块（逻辑集成在 weapon-base 的 WeaponConfig 和 Client 层表现代码中）。与角色时装系统(Fashion/Skin)独立，仅处理武器外观

依赖：[[weapon-base]]
