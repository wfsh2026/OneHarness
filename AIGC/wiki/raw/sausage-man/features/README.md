# Features 功能包目录

> 本目录存放所有功能包定义（feature.json）及索引文件。
> 每个 feature.json 描述一组相关代码文件及其依赖关系，用于功能级同步和代码覆盖率分析。

---

## 查询方式

1. 功能概览 → 直接读各 `.md` 文件的 YAML frontmatter（name/category/dependencies/file_count）
2. 文件→功能归属 → `grep -rl "文件名" aigc/wiki/raw/sausage-man/features/`
3. 功能覆盖率 → `python3 aigc/harness/tools/wiki/features/check-coverage.py --dir Assets/Script/GamePlay --summary`
4. 文档名→路径 → `python3 aigc/harness/tools/wiki/wiki-resolve.py --resolve "feature名"`

---

## 分类目录

| 分类 | 说明 |
|------|------|
| `ability/` | Ability 系统（AB/AE/技能基础设施） |
| `cross-cut/` | 横切关注点（核心系统、基础设施、公共组件） |
| `gpo/` | GPO 系统（游戏对象：怪物/载具/武器/场景物件） |
| `mode/` | 游戏模式（VS/淘金/训练/Boss战等） |
| `ugc/` | UGC 系统（用户自创内容） |
| `ui/` | UI 系统（大厅/背包/商城/好友等） |

> 每个分类下可能有子目录（如 `ability/ab/`、`ability/ae/`），具体结构由各分类自行组织。

---

## feature.json 格式

```json
{
  "name": "mode-vs",
  "category": "mode",
  "description": "VS 模式（对抗）",
  "deps": ["mode-base", "character-base"],
  "uses": ["gpo-base"],
  "files": [
    "Assets/Scripts/GamePlay/Server/Mode/VS/ServerVSMode.cs",
    "Assets/Scripts/GamePlay/Client/Mode/VS/ClientVSMode.cs"
  ]
}
```

| 字段 | 说明 |
|------|------|
| `name` | 功能名（全局唯一） |
| `category` | 分类（对应目录名） |
| `description` | 功能描述 |
| `deps` | 结构依赖（编译必需） |
| `uses` | 业务引用（运行时交叉调用，非编译依赖） |
| `files` | 归属文件列表（相对于仓库根目录） |

---

## 管理工具

所有工具位于 `aigc/harness/tools/knowledge/`，详见 `framework/README.md`。
