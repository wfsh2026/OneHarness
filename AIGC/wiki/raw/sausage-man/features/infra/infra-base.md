---
name: infra-base
display_name: 基础设施层
category: infra
version: 1.0.0
dependencies: []
---

# 基础设施层

项目基础设施四大模块：Utils 工具库(494文件/音频/动画/UI/数学/网络HTTP/性能/调试/输入/对象池/存储/3D图形/SDK)、Config 配置系统(678文件/GameData/RoleData/ItemData/BuffData/SO设置)、Data 数据层(290文件/核心数据结构/关卡配置/用户设置/Playable动画数据)、Controller UI控制器(135文件/模式控制器/大厅/商店/设置/教程/工具)

## 代码文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/Utils/ [494 files]` | 工具库 — 音频/动画/UI/数学/网络/性能/调试/输入/对象池/存储/图形/SDK |
| `Assets/Script/Config/ [678 files]` | 配置系统 — 配置表加载/SO设置/生成的内存检查 |
| `Assets/Script/Data/ [290 files]` | 数据层 — 核心数据结构/关卡/用户设置/Playable |
| `Assets/Script/Controller/ [135 files]` | UI控制器 — 模式/大厅/商店/设置/教程/工具 |

## 核心入口文件

| 路径 | 说明 |
|------|------|
| `Assets/Script/Data/GameData.cs` | 全局游戏数据 |
| `Assets/Script/Data/RoleData.cs` | 角色数据 |
| `Assets/Script/Data/ItemData.cs` | 物品类型常量与工具方法 |
| `Assets/Script/Data/BuffData.cs` | Buff 数据 |
| `Assets/Script/Data/FashionData.cs` | 时装数据 |
| `Assets/Script/Data/CustomGameData.cs` | 自定义房间数据 |
| `Assets/Script/Config/SOGameSetting.cs` | 游戏全局设置 SO |
| `Assets/Script/Config/SOMapInfo.cs` | 地图信息 SO |
| `Assets/Script/Config/SOArtSetting.cs` | 美术设置 SO |
| `Assets/Script/Utils/Camera/CameraUtility.cs` | 镜头工具(高斯模糊/截图) |
| `Assets/Script/Utils/MathUtil.cs` | 数学工具 |
| `Assets/Script/Utils/FileUtil.cs` | 文件工具 |
| `Assets/Script/Utils/HttpUtils.cs` | HTTP 工具 |
| `Assets/Script/Utils/LocalSave/ [dir]` | 本地存储系统 |
| `Assets/Script/Utils/GameObjectPool/ [dir]` | 对象池系统 |
| `Assets/Script/Controller/ExceptionHandlerController.cs` | 异常处理控制器 |

## 备注

基础设施层是项目最大的非 GamePlay 代码区(共1597文件)。Config 目录含大量自动生成的配置加载类(tab分隔txt→C#字典)和内存检查类。Controller 目录含135个 UI 控制器，按模式/功能分类。Utils 目录包含70+子工具涵盖音频、动画、网络、输入、存储、图形等全方位基础能力。Data 目录含核心数据结构(GameData/RoleData/ItemData/BuffData)驱动整个游戏运行
