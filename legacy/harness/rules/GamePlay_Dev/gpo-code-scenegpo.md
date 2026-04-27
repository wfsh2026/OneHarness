# SceneGPO 开发规范（详细）

> **加载条件**：开发 SceneGPO（基地 / 可破坏掩体 / 触发区域 / Buff刷新点）时加载本文件。  
> 普通 AI GPO 开发只需读 `gpo-code.md`，不需要本文件。

---

## 一、SceneGPO 类型速查

| 类型 | GodMode | 典型示例 |
|------|---------|---------|
| 可受击 SceneGPO | `false` | 基地、可破坏掩体 |
| 区域/触发型 SceneGPO | `true` | Buff 刷新点、区域检测 |

---

## 二、SceneGPO 架构真相（必读）

`ServerAIWorld.OnSetSceneGPOCallBack` **硬编码** 使用 `GPOM_SceneGpoSet.Id_BaseSceneGpo` 创建 GPO，
**不管 `SceneGPOEntity.SceneGPOIndex` 是什么值**。

**核心结论**：所有 SceneGPO 共用同一个 GPOM（Hp=0），框架层不支持按 Index 区分 GPOM 数据。
若需自定义 HP 等属性，必须在 `SceneGPOBase` 子类上自定义字段（如 `MaxHp`），由服务端组件自行读取。

---

## 三、可破坏 SceneGPO 的双层架构

| 层级 | 类 | 继承 | 挂载位置 | 职责 |
|------|-----|------|---------|------|
| **Prefab 标记层** | `SceneGPODestructibleCover` | `SceneGPOBase` | 子节点 GPOComponents | 类型标识 + MaxHp 配置（Inspector 设置） |
| **System 处理层** | `ServerAISceneGPODestructibleCover` | `ServerNetworkComponentBase` | System 动态注入（EnsureComponent） | HP 自管理 + Event_Disapear 驱动显隐 |

**⚠️ 关键约束**：`SceneGPOBase` 子类**不能挂在 SceneGPOEntity 所在的根节点上**（框架 Editor 检查报错），必须挂子节点。

---

## 四、受伤链路（可破坏掩体）

```
炮弹命中 HitCollider(isTrigger) → HitType.Layer=World → Event_GPOHurt
→ ServerAISceneGPODestructibleCover.OnGPOHurt → currentHp -= Hurt
→ HP≤0 → mySystem.Dispatcher(SE_GPO.Event_Disapear { IsDisapear=true })
→ ServerGPOShowEntity → Rpc_IsShowEntity(false) → ClientGPOShowEntity → SetActive(false)
→ 5s Timer → Dispatcher(Event_Disapear{false}) → 复生
```

⚠️ **显隐同步必须通过 `SE_GPO.Event_Disapear` + `ServerGPOShowEntity`**，不能直接 Dispatcher `SE_Entity.Event_IsShowEntity`（无 RPC，客户端收不到）。

---

## 五、GodMode 条件化

`ServerAISceneGPOSystem` 默认对所有 SceneGPO 添加 GodMode。可破坏掩体需在 `OnLoadEntityEnd` 中条件化：

```csharp
bool hasDestructible = baseList.Any(c => c is SceneGPODestructibleCover);
if (!hasDestructible) {
    AddTag(GamePlayTagData.TagEnum.GodMode);  // 普通 SceneGPO 保持无敌
}
// 可破坏掩体跳过，炮弹可命中
```

---

## 六、客户端 System 必须添加 ClientGPOShowEntity

```csharp
protected override void AddComponents() {
    AddComponent<ClientGPOAttribute>();
    AddComponent<ClientGPOShowEntity>();  // 必须！接收 Rpc_IsShowEntity
}
```

---

## 七、Prefab 碰撞体结构（可破坏掩体）

```
BrickWall_N1 (root, Layer=Default)
├── BoxCollider                       ← 角色阻挡（Default 层）
├── HitType (Layer=Ignore)            ← 根节点不参与炮弹命中
├── SceneGPOEntity (IsServer=false/true)
├── HitCollider (子节点, Layer=ClientLayer/ServerLayer)
│   ├── BoxCollider (isTrigger=true)  ← 炮弹射线检测（isTrigger 不阻挡角色）
│   └── HitType (Layer=World)         ← 炮弹命中目标
└── GPOComponents (子节点)
    └── SceneGPODestructibleCover (MaxHp=5400/2700)
```

**Layer 设计要点**：
- 角色 DriverControllerLayer 与 ServerLayer/ClientLayer 互相忽略（角色可穿过）
- 炮弹射线只打 ClientLayer（客户端）/ ServerLayer（服务端）
- 因此：角色阻挡用 Default；炮弹检测用 ClientLayer/ServerLayer + isTrigger

---

## 八、SceneGPOEntity 配置规则

| 字段 | 值 | 说明 |
|------|-----|------|
| `IsServer` | `true` | 服务端场景必须设置，否则 GPO 无法被服务端识别 |
| `IsServer` | `false` | 客户端场景默认值 |
| `Sign` | 字符串常量 | ModeSystem 通过 Sign 查找并绑定逻辑 |
| Layer | `ServerLayer`（Layer 8） | 服务端场景必须，否则射线检测失效 |

---

## 九、GPOM 数据行写入位置

可破坏掩体数据写入 `GPOM_SceneGpoSet`（不新建分支），因为 `IGPOM.cs` 中 `Id_SceneGpo` 路由到该 Set。

但由于 ServerAIWorld 硬编码 `Id_BaseSceneGpo`，这些数据行**不会被自动查找**——HP 必须通过 `SceneGPODestructibleCover.MaxHp` 字段手动配置。

---

## 十、SceneGPO vs 动态 AI GPO 对比

| 特性 | SceneGPO | 动态 AI GPO |
|------|---------|------------|
| 生命周期 | 场景加载时自动初始化 | 运行时 AddAI 创建 |
| 网络同步 | TargetRpc_AddAI 仍需下发 | 同左 |
| 位置控制 | 固定（场景 Transform 决定） | 动态指定生成位置 |
| 销毁控制 | 通常复活，不真正销毁 | 可完全销毁（RemoveAI） |

> 场景建设完整规范见 `scene-code.md`。
