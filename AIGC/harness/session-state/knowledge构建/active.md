# 当前会话状态

## 项目：sausage-man-2022 knowledge 构建
## 工作流类型：knowledge 构建
## 当前阶段：B17-B20全部完成，仅剩B16 UI系统

## 架构说明

本项目含 **两代架构**，知识库构建需分别覆盖：

| 代次 | 代码根目录 | 架构风格 | 资料状态 |
|------|----------|---------|---------|
| **1 代** | `Assets/Script/`（排除 Biubiubiu2/） | C/S/H 三端 Modules 架构 | ❌ 几乎无文档，需从代码梳理 |
| **2 代** | `Assets/Script/Biubiubiu2/` | ECS 风格 System/Component | ✅ 有完整参考（BiuBiuBiu2-ShottingDuck-UGC 项目） |

> 2 代参考项目路径：`G:\BiuBiuBiu2-ShottingDuck-UGC\AIGC\knowledge\`
> 2 代代码在参考项目中位于 `Assets\Scripts\`，在本项目中位于 `Assets\Script\Biubiubiu2\`
| B2-角色系统 | ✅ 通过 | 2026-04-11 |

## 主进度：知识库构建节点

| 步骤 | 内容 | 状态 |
|------|------|------|
| ⓪ 技术文档 | knowledge 构建技术方案文档 | 🔄 |
| ① 系统地图 | system-map.md（1 代 + 2 代合并） | 📋 |
| ② 功能目录 | features/（1 代新建 + 2 代迁移适配） | 📋 |
| ③ 文档索引 | wiki-map.json 重新生成 | 📋 |
| ④ 代码图谱 | graph.json + html/ 生成（可选） | 📋 |

| 批次进度 | 内容 | 状态 |
|----------|------|------|
| B5 [PM] | B5载具系统knowledge构建完成: system-map载具条目+5个feature.json | ✅ |

## 1 代系统地图梳理批次

| 批次 | 系统 | 代码量 | 产出制作文档 | 状态 |
|------|------|-------|------------|------|
| B1 | 模式系统 (Mode) | C:471 S:470 H:82 | `模式制作.md` | ✅ |
| B2 | 角色/3C 系统 (Role) | C:129 S:69 H:176 | `角色制作.md` | ✅ |
| B3 | Buff/技能系统 | C:268 S:285 H:477 | `Buff制作.md` | ✅ |
| B4 | AI 系统 (RoleAI) | C:214 S:108 H:53 | `AI制作.md` | ✅ |
| B5 | 载具系统 (Car/FlyVehicle) | C:59 S:2 H:11 | `载具制作.md` | ✅ |
| B6 | 射击武器 | SOWeaponControl(96+) | `射击武器制作.md` | ✅ |
| B7 | 近战武器 | SOHitPart(62) + FightClose + MeleeWeapon | `近战武器制作.md` | ✅ |
| B8 | 特殊武器 | ElasticWeapon + HiddenWeapon + MagicWeapon | `特殊武器制作.md` | ✅ |
| B9 | 投掷物系统 | Bomb + BlastBomb 相关 | `投掷物制作.md` | ✅ |
| B10 | 消耗品/药品 | Consumables 相关 | `消耗品制作.md` | ✅ |
| B11 | 武器配件 | 81-85 瞄具~握把 + 芯片 + 弹药 | `武器配件制作.md` | ✅ |
| B12 | 角色装备 | 61-72 背包~装甲 + 狗牌 | `角色装备制作.md` | ✅ |
| B13 | 身份卡系统 | IdCard 相关 | `身份卡制作.md` | ✅ |
| B14 | 战场活动道具 | Activity + War + Joker 等 | `战场道具制作.md` | ✅ |
| B15 | 打金模式道具 | GoldItem + Altar + Key 等 | `打金道具制作.md` | ✅ |
| B16 | UI 系统 | 1,968 files | `UI系统制作.md` | ✅ |
| B17 | 镜头系统 | Camera | `镜头系统制作.md` | ✅ |
| B18 | 网络/消息系统 | Network + Message | `网络消息制作.md` | ✅ |
| B19 | 子玩法模块 | GoldDash/Knockout/WolfParty 等 | `子玩法制作.md` | ✅ |
| B20 | 基础设施 | Utils/Config/Data/Controller | `基础设施制作.md` | ✅ |

## 2 代知识迁移

| 内容 | 来源 | 状态 |
|------|------|------|
| system-map 2 代部分 | 参考项目 system-map.md | 📋 |
| features/ 2 代功能包 | 参考项目 features/ (110+ json) | 📋 |
| 路径适配 | Assets\Scripts\ → Assets\Script\Biubiubiu2\ | 📋 |
| ㉓ [DL] | resource-map.md 完成 | ✅ |
| ㉔ [DL] | session-sync.sh reasoning字数守卫 | ✅ |
| ㉕ [DL] | session-sync.sh 三段式统一 | ✅ |
| ㉖ [DL] | resource-map.md 关联引用建立 | ✅ |
| ㉗ [DL] | B1模式系统knowledge交付：system-map.md更新(模式行+17实例+18关键词+依赖图) + 17个feature.json创建 | ✅ |
| ㉘ [DL] | B1模式制作.md产出完成(377行,6章,11/11规范自检通过) | ✅ |
| ㉙ [DL] | B2角色系统全部交付物产出完成: 15个feature.json + system-map条目 + 角色制作.md(1001行) | ✅ |
| ㉚ [DL] | 角色制作.md补充2.8预制资源加载+2.9Motion动画系统章节,1001→1100行 | ✅ |
| ㉛ [DL] | 载具制作.md新增1.4预制体与资源加载(317→376行),模式制作.md新增1.7预制体与资源加载(489→570行) | ✅ |
| ㉜ [PM] | B3a feature.json×5 + system-map Buff系统更新完成 | ✅ |
| ㉝ [PM] | B3a补充: buff-item.json和buff-misc.json字段信息完善 | ✅ |
| ㉓ [PM] | Car Mode Role 标准化审查完成 | ✅ |
| ㉔ [PM] | B3b+B3c 153个Buff feature.json批量生成完成，feature-index.md v1.1更新 | ✅ |
| ㉕ [DL] | Buff制作.md v1.0 完成（B3 最后交付物） | ✅ |
| ㉖ [DL] | feature.json config/asset 字段批量填充完成 — 180/245 config (73.5%), 80/245 asset (32.7%) | ✅ |
| ㉖ [DL] | Buff feature.json config/asset 批量填充: 180 config + 80 asset | ✅ |
| ㉗ [DL] | Car 系统 feature.json 按控制器家族重建: 5 → 9 个文件, 新增 Buggy/Motor/Animal/GoldDash 家族 | ✅ |
| ㉘ [PM] | ADR#8 config/asset分类标准确认+21条误分类修复(Car2+Mode19) | ✅ |
| ㉙ [PM] | Role feature.json config/asset补充(10/17) + resource-map.md角色系统章节扩展(AnimatorPool+22模式控制器目录+6个Role SO) | ✅ |
| ㉚ [PM] | Mode feature.json asset补充(12/18模式专属Animator Controller+Effect目录) | ✅ |
| ㉛ [PM] | Buff 57空白处理: 9 SO匹配修复 + 47纯代码标注 + framework共享配置 | ✅ |
| ㉜ [DL] | resource-map.md 全面扫描更新(525→921行,13→18章节+4附录,Effect/66目录+SO/48目录完整索引) | ✅ |
| ㉝ [DL] | system-map.md全面更新(新增10系统到§二地图+意图识别14条+依赖关系10系统+GPO/AB/AE标记为2代专属) + feature.json精确化(17模式SO路径从通用Mode/改为具体子目录,rookiecamp新增Effect资产) | ✅ |
| ㉞ [DL] | AI系统feature.json创建(6个特性: ai-base/ai-behavior/ai-buff/ai-spawner/ai-teammate/ai-navigation, 覆盖C/S/H三端785文件+264资产+179配置) | ✅ |
| ㉟ [DL] | 武器系统feature.json创建(5个特性:base/bullet/melee/attachment/skin) | ✅ |
| ㊱ [DL] | 道具系统feature.json创建(3个特性:item-base/loot/golddash) | ✅ |
| ㊲ [DL] | B4/B6/B7计划文档补建+system-map意图识别更新 | ✅ |
| ㊳ [DL] | B4-AI系统制作文档完成 | ✅ |
| ㊴ [DL] | B6武器战斗制作.md创建完成(26KB) | ✅ |
| ㊵ [DL] | 更新Gen1技术方案§2.4物品分类:原B7 GPO道具拆分为B7投掷物/B8消耗品/B9装备配件/B10身份卡/B11功能道具,总批次12→16 | ✅ |
| ㊶ [DL] | 技术方案文档武器拆分更新：B6武器战斗→B6射击+B7近战+B8特殊，批次18→20 | ✅ |
| ㊷ [DL] | B7近战武器制作.md + B8特殊武器制作.md 创建完成 | ✅ |
| ㊸ [DL] | 特殊武器制作.md 补充附录A SO统计表（27个SO，6分类） | ✅ |
| ㊹ [DL] | 技术方案文档 §2.4.2 和批次计划状态标记更新 B6/B7/B8 → ✅ | ✅ |
| ㊺ [DL] | 新建 weapon-shooting.json + weapon-special.json，武器features颗粒度与制作文档对齐 | ✅ |
| ㊻ [DL] | system-map.md 武器系统条目扩充：三大子系统详细代码路径+意图识别12条+依赖关系扩展 | ✅ |
| ㊼ [DL] | B9 投掷物系统完成: throwable-bomb.json + 投掷物制作.md + system-map投掷物条目 | ✅ |
| ㊽ [DL] | active.md+tech-doc+system-map 批次表对齐更新: 12批→20批，B3-B9状态修正 | ✅ |
| ㊾ [DL] | B10 消耗品系统完成：item-consumable.json + 消耗品制作.md + system-map更新 | ✅ |
| ㊿ [DL] | B11武器配件系统完成: weapon-attachment.json(44代码) + 武器配件制作.md(530行) + system-map更新(§三关键词+§四依赖+§五文档) + 技术方案B11状态更新 | ✅ |
| 51 [DL] | B12角色装备系统完成：role-equipment.json(49代码+8配置+7资源) + 角色装备制作.md(688行28KB) + system-map v1.5 + 技术方案B12标记✅ | ✅ |
| ㊵ [DL] | B13身份卡系统knowledge构建完成(29卡JSON+框架+制作文档+system-map+技术方案) | ✅ |
| ㉙ [DL] | T2 1代core-rules.md新建完成（475行16条Rule） | ✅ |
| ㉚ [DL] | T3 workflow-dev-sausage.md新建完成（185行4章） | ✅ |
| ㉓ [DL] | 7个JSON修复（武器/AI/道具display_name+code_paths扩展） | ✅ |
| ㉔ [DL] | 投掷物制作.md术语修复：移除BombArea/GameQuan内容 | ✅ |
| ㉕ [DL] | 14篇制作文档审查完成（内容一致性+术语准确性） | ✅ |
| ㉖ [DL] | 20个模式JSON审查完成（mode-*.json结构与数据校验） | ✅ |
| ㉗ [DL] | 3处ADR#6修复（模式/载具/角色制作文档补充资源加载§1.3） | ✅ |
| ㉘ [DL] | T1 system-map.md修复+代际路由完成（+61行） | ✅ |
| ㉛ [DL] | 删除workflow-dev-sausage.md，差异信息合并至core-rules附录B | ✅ |
| ㉜ [DL] | system-map.md P1+P2 修复: 统计数据同步+武器清单填充 | ✅ |
| ㉝ [DL] | system-map.md P3 修复: §6.4-6.6 2代占位段合并压缩 | ✅ |
| ㉞ [DL] | 目录重组: rules/1代架构→docs/sausage-framework, docs/{内容边界定义,范例文档}→docs/biu2-framework/. 32文件搬家+wiki-map更新+29文件路径修复+4个BIU26旧路径修复 | ✅ |
| ㉟ [DL] | 批量 wiki-link 迁移: 179 处路径引用转为 [[alias]]（31 文件） | ✅ |
| ㊱ [DL] | Agent/规则文件 wiki-link 迁移: 73 处路径引用转为 [[alias]]（12 文件，含代码块内加载指令）+ AGENTS.md 新增 wiki-link 解析协议 | ✅ |
| ㊲ [DL] | wiki-resolve.py --check 扫描范围扩展 (+knowledge/ +AGENTS.md) | ✅ |
| ㊳ [DL] | wiki-map 新增Gen1/Gen2 alias(22→14)、system-map改名消歧、check-refs.py删除 | ✅ |
| 54 [PM] | features JSON→MD批量迁移完成: 340个JSON转为MD格式(frontmatter+正文), 原JSON已删除, index.json+reverse.json已重建, feature-format.md升级v1.1→v2.0 | ✅ |
| 55 [PM] | system-map.md v2.0重构完成: 按wiki/README.md v2.1四模块结构重组(787行→401行), §二合并系统总表+意图识别+文档加载(补7列含base feature), §三实例清单补feature列(载具22+模式17+武器15+身份卡29), §四精简依赖关系, wiki-link全部解析通过 | ✅ |
| 56 [PM] | wiki-link批量消歧修复: core-rules歧义23条→0条(18文件sed替换为GamePlay_Dev/core-rules), sausage-framework/core-rules→sausage-man/core-rules(1文件), 全量check 41→17条(剩余17条均为已知不可修项: framework专属9+示例占位4+2代示例3+缺失文档1) | ✅ |
| 57 [PM] | feature-format.md v2.0→v2.1: 新增聚合vs拆分判断规则+system-map对齐约束+细化9系统颗粒度+3条禁止行为 | ✅ |
| 58 [PM] | feature拆分完成: fly-vehicle→1框架+5独立载具, weapon-special→4独立武器类型, weapon-melee→框架+实例分离. 新增10个feature(340→350), wiki-map重建(969唯一映射), 全部wiki-link可解析 | ✅ |
| 59 [PM] | system-map v2.1完成: §二意图识别表63处同上→0处(每行精确到feature wiki-link), §三实例清单重构(补角色17/AI 6/武器12/道具6/Buff分类汇总), 载具按feature粒度合并22行→13行, 非buff孤岛39→0, wiki-link 0错误 | ✅ |
| 60 [PM] | feature孤岛修复: 345个feature注入dependencies wiki-link(inject-dep-links.py), Obsidian图谱连线覆盖率 0/350→346/350, 修复item-consumable.md错误引用5条 | ✅ |
| 61 [PM] | buff分类索引完成: 23个_index-buff-*.md(覆盖全部244个buff feature), system-map §3.8和§二指向分类索引, 正向可达链路system-map→分类索引→具体buff feature打通 | ✅ |
| 62 [PM] | buff按功能挂载完成: 235个buff注入12个消费者feature(mode-golddash/mode-pverogue等), 删除19个冗余_index文件, 保留4个孤儿索引, system-map §3.8重构为消费者表格 | ✅ |
| 63 [PM] | 规范沉淀: system-map-rules.md v2.1→v2.2(新增§七 大规模实例系统分层索引规则), feature-format.md v2.1→v2.2(新增关联实例段落规范) | ✅ |
| 64 [PM] | 增量漂移检测: drift-check.py + wiki/README.md last_sync_commit 机制, 落入 README 流程规范 | ✅ |
| 65 [PM] | drift-check.py 升级为多仓库: 支持 7 个子仓库(client/script/bundle/biu2/scene/art/audio)独立追踪 sync commit, README同步状态改为表格格式 | ✅ |
| 66 [PM] | drift-check.py 通用化: 移除全部硬编码仓库配置, 从wiki/README.md同步状态表格读取(仓库key/commit/路径/关注文件glob), 任何项目可用 | ✅ |
| 67 [PM] | workflow-knowledge.md 更新: drift-check/wiki-env.json 挂入流程(环境检测+步骤8.5+步骤13.6), 单项更新表+工具速查+产出清单+active模板同步更新 | ✅ |
| 68 [PM] | workflow-knowledge.md 新增 §三-B 漂移修复流程: 新增文件分类判断(Buff/模式/身份卡/扩展)→创建/补充feature→注入wiki-link→挂消费者→更新system-map; 已删除文件→清理feature路径; 修复后验证清单5项 | ✅ |
| 69 [PM] | workflow-knowledge.md 区分首次构建/增量更新路径: §一触发条件按wiki-env.json存在性分流, 新增§三-A增量更新快速路径(drift-check→有漂移走§三-B→验证→update), 用户说'更新wiki'直接走快速路径不走完整流程 | ✅ |
| 70 [PM] | workflow-knowledge.md 重构: 572行→244行(57%压缩) | ✅ |
| 71 [PM] | P1完成: 创建3个模式feature(mode-wolfparty/mode-knockout/mode-sportsparty), system-map §3.2加3行+§二加3行意图识别, GamePlay覆盖率56.8%→61.8%(+240文件) | ✅ |
| 72 [PM] | P2完成: 补充已有feature未覆盖代码. Role(+193→9个feature), Buff(+106→buff-framework), GameWorld Features(+206→8个feature), 小模块(+208→7个feature). GamePlay覆盖率61.8%→76.4%(+713文件) | ✅ |
| 73 [PM] | P3完成: 创建9个新feature(server-cheat/server-report/beginner-tutorial/pet-system/role-skill/auxiliary-aiming/autowar-system/dev-tools/network-framework)+归属碎片文件. GamePlay覆盖率76.4%→99.5%(0未覆盖). system-map §3.10新增+§二意图行9条更新. 362 features, 999 wiki-map, 395 system-map wiki-links 0断链 | ✅ |
| 74 [PM] | 整体检查完成: 修复item-consumable YAML deps断链(5条→0), system-map §二补3个空行(时装→role-skin, 网络→network-framework, 地图→mode-common) | ✅ |
| 75 [PM] | 删除废弃的index.json(111KB)+reverse.json(492KB), 清理workflow-knowledge.md和wiki/README.md中的引用. 这两个JSON索引在MD迁移后已被wiki-map.json取代 | ✅ |
| 76 [PM] | 清除index.json/reverse.json全部引用: SCHEMA.md/wiki-README/knowledge-README/features-README/Gen2技术方案/tools-README/workflow-knowledge.md(共7个文档) + 4个工具(migrate/check-coverage/auto-assign/scan-uses)的skip列表更新 + resolve-deps.py标记待适配 | ✅ |
| 77 [PM] | glossary.md重构: 手动维护→工具自动生成(build-glossary.py). 删除与system-map重叠的§四玩法术语, 删除过时的§七 JSON索引. 保留枚举表(GameMode/MatchMod/MapMode/AttackType全量解析)+架构术语+feature统计. 集成到workflow-knowledge和tools-README | ✅ |
| ㊿㉘ [PL] | B14 战场活动道具完成 | ✅ |
| ㊿㉙ [PL] | 修正B11-B13批次状态: 📋→✅ | ✅ |
| ㊿㉚ [PL] | B15 打金模式道具完成 | ✅ |
| ㊿㉛ [项目负责人] | B17镜头系统完成：camera-system.md feature + 镜头系统制作.md + system-map更新 | ✅ |
| ㊿㉜ [项目负责人] | B18-B20批量完成：网络消息制作.md + 子玩法制作.md + infra-base.md + 基础设施制作.md + system-map更新 | ✅ |
| ㊿㉝ [项目负责人] | 6篇制作文档质量重写完成(镜头/网络/战场道具/打金道具/子玩法/基础设施)，每篇16-19KB | ✅ |
| ㉓ [项目负责人] | 子玩法制作文档拆分 21/21 完成 | ✅ |
| ㉔ [项目负责人] | 镜头系统制作.md 深度扩充完成 (16KB→30.5KB) | ✅ |
| ㉕ [项目负责人] | 制作文档目录重组完成：40个文档按11个领域分类 + gen1层级移除 | ✅ |
| ㉖ [PM] | 目录重组残留路径修复: 6文件50+处旧路径→新路径+wiki-link,Gen1技术方案B17-B20状态同步 | ✅ |
| ㉗ [PM] | B16 UI系统knowledge构建: 12 feature文件(1286代码引用) + UI系统制作.md(61.1KB) + system-map UI行更新 | ✅ |
| 28 [PM] | FootballParty OnlyUp GoldDashFast three mode docs fully rewritten based on real code analysis data | ✅ |
| 29 [PM] | Created 2 new manufacturing docs: RoleAnimation (24.1KB) and RoleFashion (28.5KB) | ✅ |
| 30 [PM] | Fixed fabricated config fields in SportsParty and PveRogue docs | ✅ |
| 31 [PM] | Created SeasonItem manufacturing doc (27.1KB) in new seasonitem/ directory | ✅ |
| ㉜ [项目负责人] | 角色动画制作.md 7主题深度补充完成(初始化/武器/舞蹈/事件/受击/载具/跳伞) | ✅ |
| ㉝ [项目负责人] | system-map孤岛修复:角色动画制作/角色时装制作/赛季道具制作/武器战斗制作4个文档关联到system-map | ✅ |
| ㉞ [项目负责人] | 3篇高严重度模式文档深度补充完成: PveRogue(9.6→17.7KB) WolfParty(10.5→18.1KB) RookieCamp(10.6→20.2KB) | ✅ |
| ㉟ [项目负责人] | SportsParty+SocialLobby两篇中严重度模式文档深度补充完成(10.3→19.6KB,9.3→17.8KB) | ✅ |
| ㊱ [项目负责人] | core-rules重命名为sausage-core-rules，ui-war-init孤岛补链(system-map+UI系统制作.md) | ✅ |

## 文档产出清单

| 文档 | 路径 | 状态 |
|------|------|------|
| knowledge构建技术方案.md | `aigc/docs/GamePlay_Dev/knowledge构建技术方案.md` | ✅ |
| active.md | `aigc/harness/session-state/knowledge构建/active.md` | ✅ |
| session-log.md | `aigc/harness/session-state/knowledge构建/session-log.md` | ✅ |
| active.md(根索引) | `aigc/harness/session-state/active.md` | ✅ |
| Gen1-knowledge构建技术方案.md | `aigc/docs/GamePlay_Dev/Knowledge/Gen1-knowledge构建技术方案.md` | ✅ |
| Gen2-knowledge构建技术方案.md | `aigc/docs/GamePlay_Dev/Knowledge/Gen2-knowledge构建技术方案.md` | ✅ |
| B1-模式系统-计划.md | `aigc/docs/GamePlay_Dev/Knowledge/plans/B1-模式系统-计划.md` | ✅ |
| B5-载具系统-计划.md | `aigc/docs/GamePlay_Dev/Knowledge/plans/B5-载具系统-计划.md` | ✅ |
| system-map.md | `AIGC/knowledge/system-map.md` | 🔄 B5载具+B1模式+B2角色+B3Buff已填充 |
| feature.json(5个) | `aigc/wiki/raw/sausage-man/features/car/` | ✅ |
| feature.json(18个) | `aigc/wiki/raw/sausage-man/features/mode/` | ✅ |
| feature.json(17个) | `aigc/wiki/raw/sausage-man/features/role/` | ✅ |
| feature.json(5个) | `aigc/wiki/raw/sausage-man/features/buff/` | ✅ B3a |
| AGENTS.md | `AGENTS.md` | 🔄 |
| 1代架构制作文档编写规范 | `aigc/wiki/raw/sausage-man/README.md` | ✅ |
| 载具制作.md修复2代引用 | `aigc/wiki/raw/sausage-man/制作文档/car/载具制作.md` | ✅ |
| 资源分布地图 | `AIGC/knowledge/resource-map.md` | ✅ |
| 模式制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/模式制作.md` | ✅ |
| 角色制作.md | `aigc/wiki/raw/sausage-man/制作文档/role/角色制作.md` | ✅ |
| Buff制作.md | `aigc/wiki/raw/sausage-man/制作文档/buff/Buff制作.md` | ✅ |
| weapon-*.json (5 files) | `aigc/wiki/raw/sausage-man/features/weapon/` | ✅ |
| item-*.json (3 files) | `aigc/wiki/raw/sausage-man/features/item/` | ✅ |
| B4/B6/B7计划文档+system-map更新 | `aigc/docs/GamePlay_Dev/Knowledge/plans/` | ✅ |
| AI制作.md | `aigc/wiki/raw/sausage-man/制作文档/ai/AI制作.md` | ✅ |
| 武器战斗制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/武器战斗制作.md` | ✅ |
| 近战武器制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/近战武器制作.md` | ✅ |
| 特殊武器制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/特殊武器制作.md` | ✅ |
| weapon-shooting.json | `aigc/wiki/raw/sausage-man/features/weapon/weapon-shooting.json` | ✅ |
| weapon-special.json | `aigc/wiki/raw/sausage-man/features/weapon/weapon-special.json` | ✅ |
| throwable-bomb.json | `aigc/wiki/raw/sausage-man/features/throwable/throwable-bomb.json` | ✅ |
| 投掷物制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/投掷物制作.md` | ✅ |
| item-consumable.md | `aigc/wiki/raw/sausage-man/features/item/item-consumable.md` | ✅ |
| 消耗品制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/消耗品制作.md` | ✅ |
| 武器配件制作.md | `aigc/wiki/raw/sausage-man/制作文档/weapon/武器配件制作.md` | ✅ |
| weapon-attachment.md | `aigc/wiki/raw/sausage-man/features/weapon/weapon-attachment.md` | ✅ |
| role-equipment.md | `aigc/wiki/raw/sausage-man/features/role-equip/role-equipment.md` | ✅ |
| system-map.md | `AIGC/knowledge/system-map.md` | ✅ |
| 角色装备制作.md | `aigc/wiki/raw/sausage-man/制作文档/role/角色装备制作.md` | ✅ |
| 身份卡制作.md | `aigc/wiki/raw/sausage-man/制作文档/idcard/身份卡制作.md` | ✅ |
| README.md | `README.md` | ✅ |
| glossary.md | `AIGC/knowledge/glossary.md` | ✅ |
| mode-common.json | `aigc/wiki/raw/sausage-man/features/mode/mode-common.json` | ✅ |
| mode-classic.json | `aigc/wiki/raw/sausage-man/features/mode/mode-classic.json` | ✅ |
| core-rules.md (1代) | `aigc/wiki/raw/sausage-man/core-rules.md` | ✅ |
| workflow-dev-sausage.md | `aigc/harness/rules/Workflow/workflow-dev-sausage.md` | ✅ |
| 投掷物制作.md | `aigc/harness/rules/GamePlay_Dev/1代架構/投掷物制作.md` | ✅(已修改) |
| mode-onlyup.json | `aigc/wiki/raw/sausage-man/features/mode/mode-onlyup.json` | ✅(已修改) |
| Agent工作流集成改造计划.md | `aigc/docs/GamePlay_Dev/Knowledge/plans/Agent工作流集成改造计划.md` | ✅ |
| workflow-dev-sausage.md | `aigc/harness/rules/Workflow/workflow-dev-sausage.md` | ❌(已删除) |
| tools/README.md | `aigc/harness/tools/README.md` | ✅ 已修正 |
| system-map-rules.md | `aigc/harness/rules/system-map-rules.md` | ✅ 已重命名 |
| check-refs.py | `aigc/harness/tools/knowledge/check-refs.py` | ❌ 已删除 |
| feature-format.md(sausage-man) | `aigc/wiki/raw/sausage-man/features/feature-format.md` | ✅ v1.1→v2.0升级 |
| feature-format.md(旧版) | `aigc/wiki/raw/sausage-man/features/feature-format.md` | ❌ 已删除 |
| feature-index.md/index.json/reverse.json | `aigc/wiki/raw/sausage-man/features/` | ❌ 已删除 |
| wiki-env.json | `aigc/wiki/wiki-env.json` | ✅ 新建 |
| build-glossary.py | `aigc/harness/tools/wiki/features/build-glossary.py` | ✅ |
| item-activity.md | `aigc/wiki/raw/sausage-man/features/item/item-activity.md` | ✅ |
| 战场道具制作.md | `aigc/wiki/raw/sausage-man/制作文档/item/战场道具制作.md` | ✅ |
| 打金道具制作.md | `aigc/wiki/raw/sausage-man/制作文档/item/打金道具制作.md` | ✅ |
| camera-system.md | `aigc/wiki/raw/sausage-man/features/camera/camera-system.md` | ✅ |
| 镜头系统制作.md | `aigc/wiki/raw/sausage-man/制作文档/camera/镜头系统制作.md` | ✅ |
| 网络消息制作.md | `aigc/wiki/raw/sausage-man/制作文档/network/网络消息制作.md` | ✅ |
| 子玩法制作.md | `aigc/wiki/raw/sausage-man/子玩法制作.md` | ✅ |
| infra-base.md | `aigc/wiki/raw/sausage-man/features/infra/infra-base.md` | ✅ |
| 基础设施制作.md | `aigc/wiki/raw/sausage-man/制作文档/infra/基础设施制作.md` | ✅ |
| PveRogue制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/PveRogue制作.md` | ✅ |
| FootballParty制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/FootballParty制作.md` | ✅ |
| OnlyUp制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/OnlyUp制作.md` | ✅ |
| SocialLobby制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/SocialLobby制作.md` | ✅ |
| RookieCamp制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/RookieCamp制作.md` | ✅ |
| BeatBeastCamp制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/BeatBeastCamp制作.md` | ✅ |
| SportsParty制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/SportsParty制作.md` | ✅ |
| WolfParty制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/WolfParty制作.md` | ✅ |
| Knockout制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/Knockout制作.md` | ✅ |
| GoldDash制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/GoldDash制作.md` | ✅ |
| 子玩法制作.md | `aigc/wiki/raw/sausage-man/子玩法制作.md` | ✅ |
| 子玩法制作.md | `aigc/wiki/raw/sausage-man/子玩法制作.md` | ❌ 已删除（合并至模式制作.md） |
| 镜头系统制作.md | `aigc/wiki/raw/sausage-man/制作文档/camera/镜头系统制作.md` | ✅ 深度扩充 16KB→30.5KB |
| Gen1-knowledge构建技术方案.md | `aigc/docs/GamePlay_Dev/Knowledge/Gen1-knowledge构建技术方案.md` | ✅ 路径修复+状态同步 |
| UI系统制作.md | `aigc/wiki/raw/sausage-man/制作文档/infra/UI系统制作.md` | ✅ 新建(61.1KB) |
| RoleAnimationDoc | `aigc/wiki/raw/sausage-man/制作文档/role/角色動畫製作.md` | ✅ |
| RoleFashionDoc | `aigc/wiki/raw/sausage-man/制作文档/role/角色時裝製作.md` | ✅ |
| SeasonItemDoc | `aigc/wiki/raw/sausage-man/制作文档/seasonitem/赛季道具制作.md` | ✅ |
| 角色动画制作.md | `aigc/wiki/raw/sausage-man/制作文档/role/角色动画制作.md` | ✅ 补充完成 24.1KB->44.3KB |
| system-map.md | `aigc/wiki/knowledge/system-map.md` | ✅ 修复4个孤岛文档关联 |
| PveRogue制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/PveRogue制作.md` | ✅ 深度补充完成(9.6KB→17.7KB) |
| WolfParty制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/WolfParty制作.md` | ✅ 深度补充完成(10.5KB→18.1KB) |
| RookieCamp制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/RookieCamp制作.md` | ✅ 深度补充完成(10.6KB→20.2KB) |
| SportsParty制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/SportsParty制作.md` | ✅ 深度补充完成(10.3KB→19.6KB) |
| SocialLobby制作.md | `aigc/wiki/raw/sausage-man/制作文档/mode/SocialLobby制作.md` | ✅ 深度补充完成(9.3KB→17.8KB) |
| sausage-core-rules.md | `aigc/wiki/raw/sausage-man/sausage-core-rules.md` | ✅ 重命名(core-rules→sausage-core-rules) |

## 关键决策（ADR）

| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|
| 1 | 架构分代 | system-map 和 features 均按 1 代/2 代分别构建 | 待确认 |
| 2 | 1代knowledge构建的文档输入源限定 | 1代唯一文档输入:aigc/docs/GamePlay_Dev/sausage-framework/;内容边界定义和范例文档均为2代文档,禁止用于1代梳理 | 2026-04-11 |
| 3 | active.md必须包含session-sync所需全部锚点section | 新建active.md时必须包含:文档产出清单/关键决策(ADR)/Bug记录/规范沉淀/遗留待确认等标准section,缺失会导致session-sync命令静默失败 | 2026-04-11 |
| 4 | 每批次是否只产出Knowledge还是也产出制作文档 | 每批次必须同步产出1代架构制作文档 | 2026-04-11 |
| 5 | B2 scope扩展包含Motion | 将Motion/(99文件)收入B2角色系统scope,新增role-animator+role-motion两个feature.json,总计17个feature pack | 2026-04-11 |
| 6 | 制作文档必须包含资源加载 | README.md新增强制章节1.3:预制体与资源加载,要求预制路径+加载方法+创建时序+动态资源列表 | 2026-04-11 |
| 7 | feature.json输出格式 | 统一为Car/Mode/Role格式 | 2026-04-12 |
| 8 | feature.json config/asset 分类标准 | 方案A按内容用途：SO目录/文件/txt数据表=config，Effect/Prefab/美术资源=asset | 2026-04-12 |
| 9 | 物品分类粒度 | 按功能模块逐个拆开:武器配件和角色装备分离,战场道具和打金道具分离,总批次12→18 | 2026-04-12 |
| 10 | 武器文档拆分 | 原B6武器战斗制作.md拆为3份：射击武器(SOWeaponControl)、近战武器(SOHitPart)、特殊武器(弹射+暗器+魔法) | 2026-04-12 |
| 11 | manufacturing_doc字段处置 | 从feature JSON移除manufacturing_doc，制作文档映射统一由system-map.md §二管理，避免N:1冗余 | 2026-04-12 |
| 12 | workflow-dev-sausage.md是否保留 | 删除，工作流差异提示融入core-rules.md附录B | 2026-04-12 |
| 13 | docs/rules目录按框架重组 | 采纳sausage-framework和biu2-framework命名 | 2026-04-12 |
| 14 | B14战场活动道具scope确认 | 仅为未覆盖的ActivityItems建feature | 2026-04-16 |
| 15 | 子玩法制作文档拆分策略 | 用户确认全部21个子玩法各自独立制作文档 | 2026-04-16 |
| 16 | 子玩法制作.md与模式制作.md合并策略 | 子玩法制作.md吸收进模式制作.md，删除子玩法制作.md，21个独立模式制作文档引用统一指向模式制作.md | 2026-04-16 |

## Bug 记录

| # | 现象 | 根因 | 修复 | 状态 |
|---|------|------|------|------|
| 1 | session-sync progress 命令静默失败 | active.md 缺少 `## 文档产出清单` 锚点 section | 补充标准锚点 sections | ✅ |
| 14 | session-sync.sh的check_field_min函数中wc -m在Git Bash/Windows上计算字节数而非字符数, 导致中文字符被计为3倍(每中文字=3bytes), 实际阈值被降低约1.7倍 | Git Bash默认locale不是UTF-8(通常是C或POSIX), wc -m在非UTF-8 locale下退化为wc -c(字节计数), echo -n 测试 | wc -m 返回47而非27 | 在wc -m调用前显式设置LC_ALL=en_US.UTF-8: char_count=\$(echo -n "\$text" | LC_ALL=en_US.UTF-8 wc -m), 内联设置不影响全局locale, 经测试中英文混合文本正确返回字符数 | ✅ |
| 14 | Buff制作.md 缺少特效 Prefab 资源加载路径文档 | 只写了 SO 加载链，遗漏了 EffectPool 特效加载链和资源放置目录 | 扩展 1.4 为 5 个子节，补充 EffectPool 加载链、EffectAssetConfig、source 映射、新建资源放置清单 | ✅ |
| 14 | §3.2~3.8配置字段使用虚构中文名而非代码实际字段名 | background agent未验证GoldDash配置源码即生成字段表 | 从7个Config源码提取真实字段替换虚构描述 | ✅ |
| 15 | cmd_bug的--reasoning参数被解析但从未使用 | session-log直接复用symptom/cause/fix | 新增--background/--reasoning/--conclusion参数，降级兼容 | ✅ |
| 14 | B13身份卡JSON质量缺陷：28张卡中23张存在缺失条目（71个code+36个asset+5个stunt共112处缺失） | 初次扫描遗漏SOSystem目录（Host端BS代码）、BSO资源变体（BladeBall/GoldDash/Assault等模式前缀）、Effect目录和Stunt预制体 | 全量审计+批量修复全部23张卡共112处缺失条目，新增SOSystem代码路径、变体资源、特效目录、投掷物预制体，验证30个JSON全部解析通过 | ✅ |
| 16 | migrate-json-to-md.py转换mode-base.json失败: Unexpected UTF-8 BOM | json.load使用utf-8编码无法处理BOM字节标记, 部分JSON文件含BOM头 | 将open编码从utf-8改为utf-8-sig自动跳过BOM | ✅ |
| 17 | wiki-sync和feature-check在Windows崩溃UnicodeEncodeError gbk | Python subprocess默认GBK编码无法编码emoji和中文路径 | run_tool添加encoding utf-8加env PYTHONIOENCODING加io.TextIOWrapper重配置stdout | ✅ |

## 规范沉淀

1. **1代knowledge梳理禁止引用2代文档(内容边界定义/范例文档),仅可引用aigc/docs/GamePlay_Dev/sausage-framework/下的文件和代码本身**
2. **session-log每条推理必须包含:备选方案列举、各方案优劣分析、选择依据、潜在风险。一句话推理=没有推理**
3. **session-sync.sh --reasoning 参数加入最小字数校验（log≥80字/adr≥50字/其余≥20字），工具级拦截一句话推理**
8. **feature-format v1.1 新增三条强制规则: files.code 禁止目录路径必须精确到cs文件和非框架category必须含子类型和各系统notes有标准模板**

## ⚠️ 遗留待确认

- 1 代各系统的具体梳理深度（模板级 vs 实例级）
- 2 代迁移后路径适配的自动化方案
