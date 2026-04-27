#!/bin/bash
# ============================================================
# gpo-gen.sh — GPO 代码生成工具
# 生成 Server/Client AI System + 所有注册（GpoType/gpo.cs/Switch/IGPOM）
#
# OUTPUT FILES (供 Phase 4 技术文档 S-05 引用):
#   CREATE: Assets/Scripts/GamePlay/Server/AI/Systems/ServerAI{Name}System.cs
#           — 服务端 AI System (S_AI_Base, 挂载组件入口)
#   CREATE: Assets/Scripts/GamePlay/Client/AI/Systems/ClientAI{Name}System.cs
#           — 客户端 AI System (条件: --sync-client true)
#   MODIFY: Assets/Scripts/Template/data/GpoType.cs
#           — 插入 Id_{Name} 常量 + Data 数组条目
#   MODIFY: Assets/Scripts/Template/data/gpo.cs
#           — 插入 Id_{Name} 常量 + Data 数组条目
#   MODIFY: Assets/Scripts/Template/gpo/IGPOM.cs
#           — GetGPOMData() 添加 switch case
#   MODIFY: Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs
#           — AddSwitchAI() 添加 case 分支
#   MODIFY: Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs
#           — AddSwitchAI() 添加 case 分支 (条件: --sync-client true)
# ============================================================
set -euo pipefail

# ============================================================
# 参数解析
# ============================================================
NAME=""
DISPLAY_NAME=""
TYPE_ID=""
GPO_ID=""
GPOM_NAME=""
SYNC_CLIENT="true"
MODEL=""               # Asset path → opt-out graybox, use CreateEntity
SHAPE="capsule"        # capsule|sphere|cube (graybox default)
SIZE=""                # shape-specific size (auto-default per shape)
COLOR="green"          # named color or r,g,b
DRY_RUN=false
PROJECT_ROOT="."

usage() {
    cat <<EOF
用法: gpo-gen.sh --name <名称> --display-name <中文名> [选项]

必需参数:
  --name           GPO 类型名称 (PascalCase, 如 GoldenEgg)
  --display-name   中文显示名称 (如 "夺金-蛋")

可选参数:
  --type-id        GpoType ID (不提供则自动递增)
  --gpo-id         Gpo 表 ID (不提供则自动递增，用于 gpo.cs 注册)
  --gpom-name      GPOM 类型名 (默认与 --name 相同)
  --sync-client    是否生成客户端 System (默认 true)
  --shape          灰盒形状 (capsule|sphere|cube, 默认 capsule)
  --size           灰盒尺寸 (capsule: radius,height; sphere: radius; cube: x,y,z)
  --color          灰盒颜色 (green|red|blue|yellow 或 r,g,b, 默认 green)
  --model          资产路径 → 改用 CreateEntity() 加载正式模型（禁用灰盒）
  --dry-run        仅预览，不写入文件
  --project-root   项目根目录 (默认当前目录)

示例:
  gpo-gen.sh --name GoldenEgg --display-name "夺金-蛋"           # 灰盒默认
  gpo-gen.sh --name GoldenEgg --display-name "夺金-蛋" --shape sphere --color yellow
  gpo-gen.sh --name NewBoss --display-name "新Boss" --model "Assets/Art/AI/Boss"
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)         NAME="$2"; shift 2 ;;
        --display-name) DISPLAY_NAME="$2"; shift 2 ;;
        --type-id)      TYPE_ID="$2"; shift 2 ;;
        --gpo-id)       GPO_ID="$2"; shift 2 ;;
        --gpom-name)    GPOM_NAME="$2"; shift 2 ;;
        --sync-client)  SYNC_CLIENT="$2"; shift 2 ;;
        --model)        MODEL="$2"; shift 2 ;;
        --shape)        SHAPE="$2"; shift 2 ;;
        --size)         SIZE="$2"; shift 2 ;;
        --color)        COLOR="$2"; shift 2 ;;
        --dry-run)      DRY_RUN=true; shift ;;
        --ugc)          UGC_MODE="true"; shift ;;
        --project-root) PROJECT_ROOT="$2"; shift 2 ;;
        -h|--help)      usage ;;
        *)              echo "❌ 未知参数: $1"; usage ;;
    esac
done

[[ -z "$NAME" ]] && echo "❌ 必须提供 --name" && usage
[[ -z "$DISPLAY_NAME" ]] && echo "❌ 必须提供 --display-name" && usage
[[ -z "$GPOM_NAME" ]] && GPOM_NAME="$NAME"

# ============================================================
# 路径配置
# ============================================================
ROOT="${PROJECT_ROOT}"

# 自动检测项目布局
CODEGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_CODEGEN_DIR="$CODEGEN_DIR"
source "$CODEGEN_DIR/path-config.sh"

# 注册文件
GPO_TYPE_FILE="$ROOT/$SCRIPTS_BASE/Template/data/GpoType.cs"
GPO_DATA_FILE="$ROOT/$SCRIPTS_BASE/Template/data/gpo.cs"
IGPOM_FILE="$ROOT/$SCRIPTS_BASE/Template/gpo/IGPOM.cs"
SERVER_SWITCH="$ROOT/$SCRIPTS_BASE/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs"
CLIENT_SWITCH="$ROOT/$SCRIPTS_BASE/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs"

# 输出目录
SERVER_SYSTEM_DIR="$ROOT/$SCRIPTS_BASE/GamePlay/Server/AI/Systems"
CLIENT_SYSTEM_DIR="$ROOT/$SCRIPTS_BASE/GamePlay/Client/AI/Systems"

# 输出文件
SERVER_FILE="$SERVER_SYSTEM_DIR/ServerAI${NAME}System.cs"
CLIENT_FILE="$CLIENT_SYSTEM_DIR/ClientAI${NAME}System.cs"

# 模板变量（PGC 默认值，UGC 钩子可覆写）
SERVER_NS="Sofunny.BiuBiuBiu2.ServerGamePlay"
CLIENT_NS="Sofunny.BiuBiuBiu2.ClientGamePlay"
SERVER_CLASS="ServerAI${NAME}System"
CLIENT_CLASS="ClientAI${NAME}System"
GPOM_STRUCT="GPOM_${GPOM_NAME}"
GPOM_SET_CLASS="GPOM_${GPOM_NAME}Set"
EXTRA_USING=""

# ── UGC 钩子：覆写路径/NS/类名/ID ──
if [[ "${UGC_MODE:-}" == "true" && ! -f "$_CODEGEN_DIR/ugc/gpo-gen-ugc.sh" ]]; then
    echo "⚠️ UGC hook 不存在: ugc/gpo-gen-ugc.sh，回退 PGC 流程"
    UGC_MODE=false
fi
if [[ "${UGC_MODE:-}" == "true" ]]; then
    source "$_CODEGEN_DIR/ugc/gpo-gen-ugc.sh" config
fi

# ============================================================
# 工具函数
# ============================================================

# 在第一个匹配 pattern 的行之前插入多行文本
insert_before() {
    local pattern="$1"
    local text="$2"
    local file="$3"
    local tmp="${file}.tmp.$$"
    local txt_file="${file}.ins.$$"
    printf '%s\n' "$text" > "$txt_file"
    awk -v pat="$pattern" -v tf="$txt_file" '
        !done && $0 ~ pat {
            while ((getline line < tf) > 0) print line
            done = 1
        }
        { print }
    ' "$file" > "$tmp"
    mv "$tmp" "$file"
    rm -f "$txt_file"
}

# 在最后一个匹配 pattern 的行之后插入多行文本
insert_after_last() {
    local pattern="$1"
    local text="$2"
    local file="$3"
    local tmp="${file}.tmp.$$"
    local last_line
    last_line=$(grep -n "$pattern" "$file" | tail -1 | cut -d: -f1)
    if [[ -n "$last_line" ]]; then
        local txt_file="${file}.ins.$$"
        printf '%s\n' "$text" > "$txt_file"
        awk -v ln="$last_line" -v tf="$txt_file" '
            NR==ln { print; while ((getline line < tf) > 0) print line; next }
            { print }
        ' "$file" > "$tmp"
        mv "$tmp" "$file"
        rm -f "$txt_file"
    else
        echo "⚠️  未找到匹配: $pattern in $file"
    fi
}

# ============================================================
# 文件存在性检查
# ============================================================
CREATED_FILES=()
MODIFIED_FILES=()

check_file_not_exists() {
    if [[ -f "$1" ]]; then
        echo "❌ 文件已存在: $1"
        exit 1
    fi
}

check_file_not_exists "$SERVER_FILE"
if [[ "$SYNC_CLIENT" == "true" ]]; then
    check_file_not_exists "$CLIENT_FILE"
fi

# 幂等检查
if grep -q "Id_${NAME}" "$GPO_TYPE_FILE" 2>/dev/null; then
    echo "❌ ${NAME} 已在 GpoType.cs 中注册"
    exit 1
fi

# 确认注册目标文件存在
for f in "$GPO_TYPE_FILE" "$GPO_DATA_FILE" "$IGPOM_FILE" "$SERVER_SWITCH"; do
    [[ ! -f "$f" ]] && echo "❌ 注册目标文件不存在: $f" && exit 1
done
if [[ "$SYNC_CLIENT" == "true" ]]; then
    [[ ! -f "$CLIENT_SWITCH" ]] && echo "❌ 注册目标文件不存在: $CLIENT_SWITCH" && exit 1
fi

# ============================================================
# ID 分配
# ============================================================
if [[ -z "$TYPE_ID" ]]; then
    MAX_TYPE_ID=$(grep -oE 'public const int Id_[A-Za-z_0-9]+ = [0-9]+' "$GPO_TYPE_FILE" \
        | grep -oE '[0-9]+$' | sort -n | tail -1 || echo "")
    [[ -z "$MAX_TYPE_ID" ]] && MAX_TYPE_ID=0
    TYPE_ID=$((MAX_TYPE_ID + 1))
fi

# GPO_ID 自动递增（从 gpo.cs 的 Gpo 数据条目中取最大 Id）
if [[ -z "$GPO_ID" ]]; then
    MAX_GPO_ID=$(grep -oE 'new Gpo\( [0-9]+' "$GPO_DATA_FILE" \
        | grep -oE '[0-9]+$' | sort -n | tail -1 || echo "")
    [[ -z "$MAX_GPO_ID" ]] && MAX_GPO_ID=0
    GPO_ID=$((MAX_GPO_ID + 1))
fi

# ============================================================
# 灰盒参数验证 & 配置
# ============================================================
case "$SHAPE" in
    capsule|sphere|cube) ;;
    *) echo "❌ --shape 必须是 capsule|sphere|cube，当前: $SHAPE"; exit 1 ;;
esac

# Size 默认值
if [[ -z "$SIZE" ]]; then
    case "$SHAPE" in
        capsule) SIZE="0.4,1.5" ;;
        sphere)  SIZE="0.5" ;;
        cube)    SIZE="1,1,1" ;;
    esac
fi

# Color → C# 代码
case "$COLOR" in
    green)  COLOR_CODE="Color.green" ;;
    red)    COLOR_CODE="Color.red" ;;
    blue)   COLOR_CODE="Color.blue" ;;
    yellow) COLOR_CODE="Color.yellow" ;;
    white)  COLOR_CODE="Color.white" ;;
    *)
        IFS=',' read -r _cr _cg _cb <<< "$COLOR"
        COLOR_CODE="new Color(${_cr}f, ${_cg}f, ${_cb}f)"
        ;;
esac

# ── 灰盒 OnStart 生成函数 ──
emit_server_onstart() {
    echo "        protected override void OnStart() {"
    echo "            base.OnStart();"
    if [[ -z "$MODEL" ]]; then
        echo "            // 灰盒 Entity (gpo-gen.sh --shape $SHAPE)"
        echo "            var root = new GameObject(\"${NAME}_Server\");"
        echo "            root.layer = LayerData.ServerLayer;"
        case "$SHAPE" in
            capsule)
                IFS=',' read -r _r _h <<< "$SIZE"
                echo "            var col = root.AddComponent<CapsuleCollider>();"
                echo "            col.radius = ${_r}f;"
                echo "            col.height = ${_h}f;"
                ;;
            sphere)
                echo "            var col = root.AddComponent<SphereCollider>();"
                echo "            col.radius = ${SIZE}f;"
                ;;
            cube)
                IFS=',' read -r _x _y _z <<< "$SIZE"
                echo "            var col = root.AddComponent<BoxCollider>();"
                echo "            col.size = new Vector3(${_x}f, ${_y}f, ${_z}f);"
                ;;
        esac
        echo "            var rootHit = root.AddComponent<HitType>();"
        echo "            rootHit.Part = GPOData.PartEnum.RootBody;"
        echo "            rootHit.Layer = GPOData.LayerEnum.World;"
        echo "            root.AddComponent<AIEntity>();"
        echo "            SetGameObjectEntity(root, StageData.GameWorldLayerType.AI);"
    else
        echo "            CreateEntity(AISkinSign + \"Server\");"
    fi
    echo "        }"
}

emit_client_onstart() {
    echo "        protected override void OnStart() {"
    echo "            iEntity.SetPoint(startPoint);"
    if [[ -z "$MODEL" ]]; then
        local prim_type
        case "$SHAPE" in
            capsule) prim_type="Capsule" ;;
            sphere)  prim_type="Sphere" ;;
            cube)    prim_type="Cube" ;;
        esac
        echo "            // 灰盒 Entity (gpo-gen.sh --shape $SHAPE)"
        echo "            var root = GameObject.CreatePrimitive(PrimitiveType.${prim_type});"
        echo "            root.name = \"${NAME}_Client\";"
        echo "            root.layer = LayerData.ClientLayer;"
        case "$SHAPE" in
            capsule)
                IFS=',' read -r _r _h <<< "$SIZE"
                echo "            root.transform.localScale = new Vector3(${_r}f * 2f, ${_h}f / 2f, ${_r}f * 2f);"
                ;;
            sphere)
                echo "            root.transform.localScale = Vector3.one * ${SIZE}f * 2f;"
                ;;
            cube)
                IFS=',' read -r _x _y _z <<< "$SIZE"
                echo "            root.transform.localScale = new Vector3(${_x}f, ${_y}f, ${_z}f);"
                ;;
        esac
        echo "            var renderer = root.GetComponent<Renderer>();"
        echo "            if (renderer != null) renderer.material.color = ${COLOR_CODE};"
        echo "            var rootHit = root.AddComponent<HitType>();"
        echo "            rootHit.Part = GPOData.PartEnum.RootBody;"
        echo "            rootHit.Layer = GPOData.LayerEnum.World;"
        echo "            root.AddComponent<AIEntity>();"
        echo "            SetGameObjectEntity(root, StageData.GameWorldLayerType.AI);"
    else
        echo "            CreateEntity(AISkinSign);"
    fi
    echo "        }"
}

# 预生成 OnStart 内容
SERVER_ONSTART="$(emit_server_onstart)"
CLIENT_ONSTART="$(emit_client_onstart)"

echo "📝 配置信息:"
echo "   名称: $NAME"
echo "   显示名: $DISPLAY_NAME"
echo "   TypeId: $TYPE_ID"
echo "   GpoId: $GPO_ID"
echo "   GPOM类型: GPOM_$GPOM_NAME"
echo "   同步客户端: $SYNC_CLIENT"
if [[ -z "$MODEL" ]]; then
    echo "   实体模式: 灰盒 (shape=$SHAPE, size=$SIZE, color=$COLOR)"
else
    echo "   实体模式: 模型 ($MODEL)"
fi
echo ""

# ============================================================
# 1. 创建 ServerAI{Name}System.cs
# ============================================================

SERVER_CONTENT=$(cat << SERVEREOF
// 该文件由 gpo-gen.sh 自动生成，AI 不得删除该注释
using Sofunny.BiuBiuBiu2.Component;
using Sofunny.BiuBiuBiu2.Message;
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Data;
using Sofunny.BiuBiuBiu2.ServerMessage;
using Sofunny.BiuBiuBiu2.Template;
${EXTRA_USING}using UnityEngine;

namespace ${SERVER_NS} {
    public class ${SERVER_CLASS} : S_AI_Base {
        private ${GPOM_STRUCT} useMData;

        protected override void OnAwake() {
            useMData = (${GPOM_STRUCT})MData;
            AddComponents();
        }

        protected override void OnClear() {
            base.OnClear();
        }

        protected override void AddComponents() {
            base.AddComponents();
            // base.AddComponents() 已包含：
            // ServerAIDead           — 死亡处理管理
            // ServerAIMaster         — 主人关系同步
            // ServerAIHateTarget     — 仇恨值计算
            // ServerAIHurt           — 伤害处理
            // KnockbackGPO           — 击退效果
            // StrikeFlyGPO           — 击飞效果
            // ServerGPOAttackProtect — 攻击保护状态
            // ServerGPOShowEntity    — 实体显隐控制
            // ServerAIPatrolPoint    — 巡逻点管理
            // ServerGPOAbilityEffect — 能力效果管理
            // ServerAIQuality        — AI品质（Boss判定）
            // ServerGPODropItem      — 掉落物品处理
            AddComponent<ServerAIAttribute>(new ServerGPOAttribute.InitData {
                ATK = 0,
                AttackRange = 0,
                MaxHp = 0, // TODO: 从 useMData 读取 Hp
                MoveSpeed = 0, // TODO: 从 useMData 读取 MoveSpeed
            });
            // TODO: 按需添加更多组件
        }

${SERVER_ONSTART}
    }
}
SERVEREOF
)

if $DRY_RUN; then
    echo "📋 预览 ServerAI${NAME}System.cs:"
    echo "────────────────────────────────────────────────────────────"
    echo "$SERVER_CONTENT"
    echo "────────────────────────────────────────────────────────────"
    echo ""
else
    echo "📄 创建 ServerAI${NAME}System.cs ..."
    mkdir -p "$(dirname "$SERVER_FILE")"
    echo "$SERVER_CONTENT" > "$SERVER_FILE"
fi
CREATED_FILES+=("$SERVER_FILE")

# ============================================================
# 2. 创建 ClientAI{Name}System.cs（仅 sync-client=true）
# ============================================================
if [[ "$SYNC_CLIENT" == "true" ]]; then

    CLIENT_CONTENT=$(cat << CLIENTEOF
// 该文件由 gpo-gen.sh 自动生成，AI 不得删除该注释
using Sofunny.BiuBiuBiu2.Component;
using Sofunny.BiuBiuBiu2.Template;
${EXTRA_USING}using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Data;
using UnityEngine;

namespace ${CLIENT_NS} {
    public class ${CLIENT_CLASS} : C_AI_Base {
        private ${GPOM_STRUCT} useMData;

        protected override void OnAwake() {
            useMData = (${GPOM_STRUCT})MData;
            AddComponents();
        }

${CLIENT_ONSTART}

        protected override void OnClear() {
            base.OnClear();
        }

        protected override void AddComponents() {
            base.AddComponents();
            // base.AddComponents() 已包含：
            // ClientAIQuality        — AI品质同步
            // ClientGPODead          — 死亡动画表现
            // ClientGPOShowEntity    — 实体显隐表现
            // ClientGPOAbilityEffect — 能力效果显示
            // ClientAIMaster         — 主人信息同步
            // ClientAIEffect         — AI特效播放
            AddComponent<ClientAIAttribute>();
            // TODO: 按需添加客户端表现组件
        }
    }
}
CLIENTEOF
    )

    if $DRY_RUN; then
        echo "📋 预览 ClientAI${NAME}System.cs:"
        echo "────────────────────────────────────────────────────────────"
        echo "$CLIENT_CONTENT"
        echo "────────────────────────────────────────────────────────────"
        echo ""
    else
        echo "📄 创建 ClientAI${NAME}System.cs ..."
        mkdir -p "$(dirname "$CLIENT_FILE")"
        echo "$CLIENT_CONTENT" > "$CLIENT_FILE"
    fi
    CREATED_FILES+=("$CLIENT_FILE")
fi

# Tab 变量（用于 GpoType.cs / IGPOM.cs 等 tab 缩进的文件）
T=$'\t'

echo ""
if $DRY_RUN; then
    echo "📋 预览完成（dry-run），跳过注册文件修改"
    if [[ "${UGC_MODE:-}" == "true" ]]; then
        echo "   将修改: GpoTypeSet_UGC.cs, CoreGameWorld_UGC.cs, ServerGameWorld_UGC.cs"
        [[ "$SYNC_CLIENT" == "true" ]] && echo "   将修改: ClientGameWorld_UGC.cs"
    else
        echo "   将修改: GpoType.cs, ServerAIWorld_Switch.cs, IGPOM.cs, gpo.cs"
        [[ "$SYNC_CLIENT" == "true" ]] && echo "   将修改: ClientAIWorld_Switch.cs"
    fi
elif [[ "${UGC_MODE:-}" == "true" ]]; then
# ── UGC MODIFY: 注册枢纽插入 ──
source "$_CODEGEN_DIR/ugc/gpo-gen-ugc.sh" modify
else
echo "🔧 修改注册文件..."

# ============================================================
# 3. 修改 GpoType.cs（2处：Id 常量 + Data 数组条目）
# ============================================================
echo "   → GpoType.cs ..."

# 3a. 插入 Id 常量（在最后一个 Id_ 常量之后）— 2 tabs 缩进
insert_after_last "public const int Id_" \
    "${T}${T}public const int Id_${NAME} = ${TYPE_ID};" \
    "$GPO_TYPE_FILE"

# 3b. 插入 Data 数组条目（在最后一个 new GpoType 之后）— 5 tabs 缩进
insert_after_last "new GpoType(" \
    "${T}${T}${T}${T}${T}, new GpoType( ${TYPE_ID}, \"${DISPLAY_NAME}\", \"${NAME}\" )" \
    "$GPO_TYPE_FILE"

MODIFIED_FILES+=("$GPO_TYPE_FILE")

# ============================================================
# 4. 修改 ServerAIWorld_Switch.cs
# ============================================================
echo "   → ServerAIWorld_Switch.cs ..."

if ! grep -q "Id_${NAME}" "$SERVER_SWITCH"; then
    SERVER_CASE_TEXT="                case GpoTypeSet.Id_${NAME}:
                    system = manager.AddSystem<ServerAI${NAME}System>(callBack);
                    break;"
    insert_before "default:" "$SERVER_CASE_TEXT" "$SERVER_SWITCH"
fi
MODIFIED_FILES+=("$SERVER_SWITCH")

# ============================================================
# 5. 修改 ClientAIWorld_Switch.cs（仅 sync-client=true）
# ============================================================
if [[ "$SYNC_CLIENT" == "true" ]]; then
    echo "   → ClientAIWorld_Switch.cs ..."

    if ! grep -q "Id_${NAME}" "$CLIENT_SWITCH"; then
        CLIENT_CASE_TEXT="                case GpoTypeSet.Id_${NAME}:
                    system = manager.AddSystem<ClientAI${NAME}System>(callBack);
                    break;"
        insert_before "default:" "$CLIENT_CASE_TEXT" "$CLIENT_SWITCH"
    fi
    MODIFIED_FILES+=("$CLIENT_SWITCH")
fi

# ============================================================
# 6. 修改 IGPOM.cs — GetGPOMData switch
# ============================================================
echo "   → IGPOM.cs (GetGPOMData) ..."

if ! grep -q "Id_${NAME}" "$IGPOM_FILE"; then
    IGPOM_CASE_TEXT="${T}${T}${T}${T}case GpoTypeSet.Id_${NAME}:
${T}${T}${T}${T}${T}mData = GPOM_${GPOM_NAME}Set.GetGPOMByIdAndMatchMode(gpoId, matchMode);
${T}${T}${T}${T}${T}break;"
    insert_before "default:" "$IGPOM_CASE_TEXT" "$IGPOM_FILE"
fi
MODIFIED_FILES+=("$IGPOM_FILE")

# ============================================================
# 7. 修改 gpo.cs — Gpo 数据表（2处：Id 常量 + Data 数组条目）
# ============================================================
echo "   → gpo.cs ..."

# 7a. 插入 Id 常量（在最后一个 Id_ 常量之后）
if ! grep -q "Id_${NAME}" "$GPO_DATA_FILE"; then
    insert_after_last "public const int Id_" \
        "${T}${T}public const int Id_${NAME} = ${GPO_ID};" \
        "$GPO_DATA_FILE"
fi

# 7b. 插入 Data 数组条目（在最后一个 new Gpo( 之后）
if ! grep -q "\"${NAME}\"" "$GPO_DATA_FILE"; then
    insert_after_last "new Gpo(" \
        "${T}${T}${T}${T}${T}${T}, new Gpo( ${GPO_ID}, ${TYPE_ID}, \"${DISPLAY_NAME}\", \"${NAME}\", \"${NAME}\", \"\" )" \
        "$GPO_DATA_FILE"
fi

MODIFIED_FILES+=("$GPO_DATA_FILE")

fi  # end of !DRY_RUN registration block

# ============================================================
# 输出摘要
# ============================================================
echo ""
echo "✅ gpo-gen.sh 执行完成！"
echo ""

echo "📁 创建的文件:"
for f in "${CREATED_FILES[@]}"; do
    echo "   + $f"
done
echo ""

echo "📝 修改的文件:"
for f in "${MODIFIED_FILES[@]}"; do
    echo "   ~ $f"
done
echo ""

echo "📋 后续步骤:"
echo "   1. 运行 gpom-gen.sh 创建 GPOM_${GPOM_NAME}.cs 模板数据文件（如尚未创建）"
echo "   2. 在 ServerAI${NAME}System.cs 的 AddComponents() 中添加业务组件"
if [[ "$SYNC_CLIENT" == "true" ]]; then
    echo "   3. 在 ClientAI${NAME}System.cs 的 AddComponents() 中添加客户端表现组件"
fi
echo "   4. 在 CSV 中配置 GPOM 数据行"

# ============================================================
# 输出执行日志（供 AI Agent 查阅）
# ============================================================
LOG_DIR="${PROJECT_ROOT}/harness/temp"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/gpo-gen-${NAME}-$(date +%Y%m%d_%H%M%S).log"

{
    echo "═══════════════════════════════════════════════════════"
    echo "  工具: gpo-gen.sh"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  参数: --name ${NAME} --display-name ${DISPLAY_NAME} --type-id ${TYPE_ID} --gpo-id ${GPO_ID} --gpom-name ${GPOM_NAME} --sync-client ${SYNC_CLIENT}$(
        [[ -z "$MODEL" ]] && echo " --shape ${SHAPE} --size ${SIZE} --color ${COLOR}" || echo " --model ${MODEL}"
        $DRY_RUN && echo ' --dry-run'
    )"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "📁 新建文件 (${#CREATED_FILES[@]} 个):"
    for f in "${CREATED_FILES[@]}"; do
        echo "  [新建] $f"
    done
    echo ""
    echo "📝 修改文件 (${#MODIFIED_FILES[@]} 个):"
    for f in "${MODIFIED_FILES[@]}"; do
        echo "  [修改] $f"
    done
    echo ""
    echo "📋 后续步骤:"
    echo "  1. 运行 gpom-gen.sh 创建 GPOM_${GPOM_NAME}.cs 模板数据文件（如尚未创建）"
    echo "  2. 在 ServerAI${NAME}System.cs 的 AddComponents() 中添加业务组件"
    if [[ "$SYNC_CLIENT" == "true" ]]; then
        echo "  3. 在 ClientAI${NAME}System.cs 的 AddComponents() 中添加客户端表现组件"
    fi
    echo "  4. 在 CSV 中配置 GPOM 数据行"
} > "$LOG_FILE"

echo ""
echo "📋 执行日志已保存: $LOG_FILE"
