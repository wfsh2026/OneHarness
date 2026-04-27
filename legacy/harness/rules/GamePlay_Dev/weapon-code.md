# 枪械开发专项规范

新增枪械时，以下每条都是**必须完成**的步骤，缺少任意一条导致运行时崩溃或功能失效。

---

## 一、三层模板数据 Checklist（WeaponSkin 管线）

| 步骤 | 文件 | 内容 |
|------|------|------|
| 1 | `Item.cs` — ItemSet 常量区 | `public const int Id_XXX = N;` |
| 2 | `Item.cs` — ItemSet 常量区 | `public const int Id_XXXDefault = M;` |
| 3 | `Item.cs` — data 数组 | `new Item(N, "枪名", ..., type=0)` 武器道具行 |
| 4 | `Item.cs` — data 数组 | `new Item(M, "XXX-默认", ..., type=8)` 皮肤道具行 |
| 5 | `WeaponSkin.cs` — data 数组 | `new WeaponSkin(skinId, weaponItemId, skinItemId, 1, true, ...)` |

---

## 二、WeaponManager 双端注册（必须同时）

```csharp
// ClientWeaponManager.cs — OnStart() switch
case ItemSet.Id_R8: system = AddSystem<ClientR8GunSystem>(callBack); break;

// ServerWeaponManager.cs — OnStart() switch
case ItemSet.Id_R8: weapon = AddSystem<ServerR8GunSystem>(callBack); break;
```

---

## 三、角色握枪动画在 AnimConfig_HTR 注册

不注册时角色**完全没有握枪姿势**。

```csharp
// AnimConfig_HTR.cs — 常量区
public const string Group_R8 = "R8";

// AnimConfig_HTR.cs — GetGroupData() switch
case Group_R8:
    return new GroupPlayData {
        ReloadClip    = GetAnimClip(AnimClip_R1895.Clip_Reload),  // 占位复用已有动画
        FireClip      = GetAnimClip(AnimClip_R1895.Clip_Fire),
        StandRaiseGun = GetAnimClip(AnimClip_R1895.Clip_StandRaiseGun),
    };
```
