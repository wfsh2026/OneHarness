---
name: buff-fire-obj
display_name: BSFireObj - 火枪/塔防炮台（继承 BSDownHpObj，可被摧毁）
category: buff/visual
version: 1.0.0
dependencies:
- buff-framework
---

# BSFireObj - 火枪/塔防炮台（继承 BSDownHpObj，可被摧毁）

1代 Buff 系统 火枪/塔防炮台（继承 BSDownHpObj，可被摧毁）。

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffScriptableObject/BSOFireObj.cs` |
| `Assets/Script/GamePlay/Host/Modules/Buff/BuffSystem/BSFireObj.cs` |
| `Assets/Script/GamePlay/Server/Modules/Buff/BuffSystem/BSFireObjServer.cs` |
| `Assets/Script/GamePlay/Client/Modules/Buff/BuffSystem/BSFireObjClient.cs` |

## 备注

routing: GameLoop. key_fields: LiftTime, CheckRange, BulletSign, DamageValue, speedAndGravity[], StartBuildEffect.
[纯代码Buff] 通用游戏机制实现，无独立SO配置（无CreateAssetMenu）。共享配置通过buff-framework依赖继承(BuffAsset.txt)。

依赖：[[buff-framework]]
