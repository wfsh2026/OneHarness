---
name: ai-buff
display_name: AI Buff 系统
category: ai/buff
version: 1.0.0
dependencies:
- ai-base
---

# AI Buff 系统

AI 角色专属 Buff/Debuff 处理：属性加成(PropertyAddition)、时间效果(TimeEffect)、加血(AddHealth)、掉血(LossHp)、无敌(Invicable)、大头(BigHead)、水晶球(Crystalball)、炸弹移动(BombMove)、关羽冲刺(GuanyuSprint)等

## 代码文件

| 路径 |
|------|
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientAIBigHead.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIAddHealth.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIBombMove.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIBuff.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAICrystalball.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIDogtagShowHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIGuanyuSprint.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIInvicable.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAILossHp.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAINoobFishTouch.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAIPropertyAddition.cs` |
| `Assets/Script/GamePlay/Client/Modules/RoleAI/RoleAIBuff/ClientRoleAITimeEffect.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerAIBigHead.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIAddHealth.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIBombMove.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIBuff.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAICrystalball.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIDogtagShowHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIGuanyuSprint.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIInvicable.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAILossHp.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAINoobFishTouch.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAIPropertyAddition.cs` |
| `Assets/Script/GamePlay/Server/Modules/RoleAI/RoleAIBuff/ServerRoleAITimeEffect.cs` |
| `Assets/Script/GamePlay/Host/Modules/RoleAI/RoleAIBuff/RoleAIBuff.cs` |

## 备注

AI Buff 系统是 C/S 三端镜像实现。每个 Buff 在 Client/Server 各有一份（12+12），Host 层仅提供基类接口。AI Buff 与普通角色 Buff 系统（buff-*）独立，专门处理 AI 角色的状态效果，但底层可能共享 Buff 框架

依赖：[[ai-base]]
