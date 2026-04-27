#!/usr/bin/env bash
# ============================================================
# component-gen.sh — Component 代码生成工具
#
# 生成 Unity ECS-like Component 模板，包含完整生命周期文档注释，
# 帮助 AI 正确编写组件逻辑、避免常见错误。
#
# 用法:
#   component-gen.sh --name <PascalCase> --side <server|client> \
#     --type <ai|ability|weapon|character|mode> \
#     [--has-init-data] [--has-update] [--no-entity] \
#     [--has-network] [--no-network] [--has-sync] \
#     [--desc "中文描述"] [--dry-run] [--project-root <path>]
#
# 示例:
#   # 服务端 AI 组件（全部功能）
#   component-gen.sh --name ServerAICyberBubbleMove --side server \
#     --type ai --has-init-data --has-update --has-sync \
#     --desc "赛博泡泡移动组件"
#
#   # 客户端 Mode 组件（最小化）
#   component-gen.sh --name ClientModeLobbyTimer --side client \
#     --type mode --has-init-data --has-update \
#     --desc "大厅倒计时组件"
#
#   # 服务端 Ability 组件（默认 ComponentBase）
#   component-gen.sh --name ServerAbilityFireBall --side server \
#     --type ability --has-init-data --desc "火球术技能组件"
#
#   # 预览模式
#   component-gen.sh --name TestComp --side server --type ai --dry-run
#
# OUTPUT FILES (供 Phase 4 技术文档 S-05 引用):
#   CREATE: Assets/Scripts/GamePlay/{Server|Client}/{AI|Ability|Weapon|Character|Mode}/Components/{Name}.cs
#           — Component 模板 (含生命周期方法注释: OnAwake/OnSetEntityObj/OnSetNetwork/OnUpdate/OnClose)
#           — 基类由 --side + --type 决定 (如: server+ai → ServerNetworkComponentBase)
#   MODIFY: (无，不自动注册到 System，需手动在 System 中 AddComponent)
# ============================================================
set -euo pipefail

# ============================================================
# 参数默认值
# ============================================================
NAME=""
SIDE=""
COMP_TYPE=""        # ai|ability|weapon|character|mode
HAS_INIT_DATA=false
HAS_UPDATE=false
HAS_ENTITY=true           # 默认生成 OnSetEntityObj
HAS_NETWORK="auto"        # auto=client时true,server时false
HAS_SYNC=false
DESC=""
TEMPLATE=""             # findtarget|lifetime|move|rotate|scale
DRY_RUN=false
PROJECT_ROOT=""

# ============================================================
# usage
# ============================================================
usage() {
    cat <<'EOF'
用法: component-gen.sh --name <PascalCase> --side <server|client> --type <type> [选项]

必填参数:
  --name <Name>         组件名称（PascalCase，如 ServerAICyberBubbleMove）
  --side <server|client> 服务端或客户端

类型标志（必选）:
  --type <type>         组件类型: ai|ability|weapon|character|mode
  --ai                  等同于 --type ai（兼容旧版）
  --mode                等同于 --type mode（兼容旧版）

功能标志:
  --has-init-data       生成 InitData 结构体模板
  --has-update          生成 OnUpdate 帧更新方法（默认关）
  --no-entity           不生成 OnSetEntityObj（默认开）
  --has-network         强制生成 OnSetNetwork（客户端默认开，服务端默认关）
  --no-network          不生成 OnSetNetwork
  --has-sync            生成 Sync/SyncData 方法（仅服务端）

可选参数:
  --desc <string>       中文描述
  --dry-run             仅预览，不写入文件
  --project-root <path> 项目根目录（默认: 自动检测）
EOF
    exit 0
}

# ============================================================
# 参数解析
# ============================================================
[[ $# -eq 0 ]] && usage

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)         NAME="$2";         shift 2 ;;
        --side)         SIDE="$2";         shift 2 ;;
        --type)         COMP_TYPE="$2";    shift 2 ;;
        --ai)           COMP_TYPE="ai";    shift ;;
        --mode)         COMP_TYPE="mode";  shift ;;
        --has-init-data) HAS_INIT_DATA=true; shift ;;
        --has-update)   HAS_UPDATE=true;   shift ;;
        --has-entity)   HAS_ENTITY=true;   shift ;;
        --no-entity)    HAS_ENTITY=false;  shift ;;
        --has-network)  HAS_NETWORK=true;  shift ;;
        --no-network)   HAS_NETWORK=false; shift ;;
        --has-sync)     HAS_SYNC=true;     shift ;;
        --desc)         DESC="$2";         shift 2 ;;
        --template)     TEMPLATE="$2";     shift 2 ;;
        --dry-run)      DRY_RUN=true;      shift ;;
        --ugc)          UGC_MODE="true";   shift ;;
        --project-root) PROJECT_ROOT="$2"; shift 2 ;;
        --help|-h)      usage ;;
        *) echo "❌ 未知参数: $1"; exit 1 ;;
    esac
done

# ============================================================
# 自动检测项目根目录
# ============================================================
if [[ -z "$PROJECT_ROOT" ]]; then
    _dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    while [[ "$_dir" != "/" && "$_dir" != "." ]]; do
        if [[ -d "$_dir/Assets" ]]; then
            PROJECT_ROOT="$_dir"
            break
        fi
        _dir="$(dirname "$_dir")"
    done
    [[ -z "$PROJECT_ROOT" ]] && PROJECT_ROOT="."
fi

# ─── 路径配置（自动检测项目布局）────────────────────────────────
_CODEGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_CODEGEN_DIR/path-config.sh"

# ============================================================
# 参数验证
# ============================================================
[[ -z "$NAME" ]]   && echo "❌ --name 必填" && exit 1
[[ -z "$SIDE" ]]   && echo "❌ --side 必填 (server|client)" && exit 1

if [[ "$SIDE" != "server" && "$SIDE" != "client" ]]; then
    echo "❌ --side 必须是 server 或 client，当前: $SIDE"
    exit 1
fi

if [[ -z "$COMP_TYPE" ]]; then
    echo "❌ 必须指定 --type <ai|ability|weapon|character|mode>"
    exit 1
fi

case "$COMP_TYPE" in
    ai|ability|weapon|character|mode) ;;
    *) echo "❌ --type 必须是 ai|ability|weapon|character|mode，当前: $COMP_TYPE"; exit 1 ;;
esac

if $HAS_SYNC && [[ "$SIDE" == "client" ]]; then
    echo "⚠️  --has-sync 仅对 server 有效，客户端已忽略该标志"
    HAS_SYNC=false
fi

# HAS_NETWORK auto: 客户端默认开，服务端默认关
if [[ "$HAS_NETWORK" == "auto" ]]; then
    if [[ "$SIDE" == "client" ]]; then
        HAS_NETWORK=true
    else
        HAS_NETWORK=false
    fi
fi

# 验证 PascalCase（简单检查首字母大写）
if [[ ! "$NAME" =~ ^[A-Z] ]]; then
    echo "❌ --name 必须是 PascalCase（首字母大写），当前: $NAME"
    exit 1
fi

# ============================================================
# --template 验证与自动配置
# ============================================================
if [[ -n "$TEMPLATE" ]]; then
    case "$TEMPLATE" in
        findtarget|lifetime|move|rotate|scale) ;;
        *) echo "❌ --template 必须是 findtarget|lifetime|move|rotate|scale，当前: $TEMPLATE"; exit 1 ;;
    esac

    if [[ "$SIDE" != "server" ]]; then
        echo "❌ --template 仅支持 server 端组件"; exit 1
    fi
    # findtarget/lifetime 仅 AI；move/rotate/scale 支持 ai+ability
    case "$TEMPLATE" in
        findtarget|lifetime)
            if [[ "$COMP_TYPE" != "ai" ]]; then
                echo "❌ --template $TEMPLATE 仅支持 --type ai 组件"; exit 1
            fi
            ;;
        move|rotate|scale)
            if [[ "$COMP_TYPE" != "ai" && "$COMP_TYPE" != "ability" ]]; then
                echo "❌ --template $TEMPLATE 仅支持 --type ai 或 --type ability"; exit 1
            fi
            ;;
    esac

    # 模板自动启用所需标志
    HAS_UPDATE=true
    HAS_ENTITY=true
    # 描述前缀
    _TL="AI"; [[ "$COMP_TYPE" == "ability" ]] && _TL="Ability"
    case "$TEMPLATE" in
        findtarget)
            HAS_INIT_DATA=true
            [[ -z "$DESC" || "$DESC" == "TODO: 添加组件描述" ]] && DESC="${_TL} 索敌组件：周期扫描范围内敌方目标"
            ;;
        lifetime)
            [[ -z "$DESC" || "$DESC" == "TODO: 添加组件描述" ]] && DESC="${_TL} 生命周期组件：倒计时到期自毁"
            ;;
        move)
            HAS_INIT_DATA=true
            [[ -z "$DESC" || "$DESC" == "TODO: 添加组件描述" ]] && DESC="${_TL} 移动组件：前进 + iEntity 同步"
            ;;
        rotate)
            HAS_INIT_DATA=true
            [[ -z "$DESC" || "$DESC" == "TODO: 添加组件描述" ]] && DESC="${_TL} 旋转组件：从起始到目标旋转"
            ;;
        scale)
            HAS_INIT_DATA=true
            [[ -z "$DESC" || "$DESC" == "TODO: 添加组件描述" ]] && DESC="${_TL} 缩放组件：随时间从起始到目标缩放"
            ;;
    esac
    echo "   模板:   $TEMPLATE (已自动启用: has-update$(
        $HAS_INIT_DATA && echo ', has-init-data'
    ))"
fi

# ============================================================
# 派生配置：命名空间、基类、输出路径
# ============================================================
# 系统引用配置 — 根据 COMP_TYPE 和 SIDE 决定
HAS_SYSTEM_REF=false
SYSTEM_TYPE=""
SYSTEM_FIELD=""

case "$COMP_TYPE" in
    ai)
        HAS_SYSTEM_REF=true
        if [[ "$SIDE" == "server" ]]; then
            SYSTEM_TYPE="S_AI_Base"; SYSTEM_FIELD="mAI"
        else
            SYSTEM_TYPE="C_AI_Base"; SYSTEM_FIELD="mAI"
        fi
        ;;
    ability)
        HAS_SYSTEM_REF=true
        if [[ "$SIDE" == "server" ]]; then
            SYSTEM_TYPE="S_Ability_Base"; SYSTEM_FIELD="mAbility"
        else
            SYSTEM_TYPE="C_Ability_Base"; SYSTEM_FIELD="mAbility"
        fi
        ;;
    weapon)
        HAS_SYSTEM_REF=true
        if [[ "$SIDE" == "server" ]]; then
            SYSTEM_TYPE="S_Weapon_Base"; SYSTEM_FIELD="mWeapon"
        else
            SYSTEM_TYPE="C_Weapon_Base"; SYSTEM_FIELD="mWeapon"
        fi
        ;;
    character)
        HAS_SYSTEM_REF=true
        if [[ "$SIDE" == "server" ]]; then
            SYSTEM_TYPE="S_Character_Base"; SYSTEM_FIELD="mCharacter"
        else
            SYSTEM_TYPE="C_Character_Base"; SYSTEM_FIELD="mCharacter"
        fi
        ;;
    mode)
        HAS_SYSTEM_REF=false
        ;;
esac

# 命名空间、using、输出目录、基类、事件类型
if [[ "$SIDE" == "server" ]]; then
    NAMESPACE="Sofunny.BiuBiuBiu2.ServerGamePlay"
    USING_MSG="using Sofunny.BiuBiuBiu2.ServerMessage;"
    case "$COMP_TYPE" in
        ai)
            OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Server/AI/Components"
            BASE_CLASS="ServerNetworkComponentBase"
            EVENT_TYPE="SE_AI"
            ;;
        ability)
            OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Server/Ability"
            # Ability 默认 ComponentBase；需要 ServerNetworkComponentBase 时须配合 ServerNetworkSync
            if $HAS_SYNC; then
                BASE_CLASS="ServerNetworkComponentBase"
            else
                BASE_CLASS="ComponentBase"
            fi
            EVENT_TYPE="SE_Ability"
            ;;
        weapon)
            OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Server/Weapon"
            if $HAS_SYNC; then
                BASE_CLASS="ServerNetworkComponentBase"
            else
                BASE_CLASS="ComponentBase"
            fi
            EVENT_TYPE="SE_Weapon"
            ;;
        character)
            OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Server/Character"
            BASE_CLASS="ServerNetworkComponentBase"
            EVENT_TYPE="SE_Character"
            ;;
        mode)
            OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Server/Mode/Components"
            if $HAS_SYNC; then
                BASE_CLASS="ServerNetworkComponentBase"
            else
                BASE_CLASS="ComponentBase"
            fi
            EVENT_TYPE="SE_Mode"
            ;;
    esac
else
    NAMESPACE="Sofunny.BiuBiuBiu2.ClientGamePlay"
    USING_MSG="using Sofunny.BiuBiuBiu2.ClientMessage;"
    BASE_CLASS="ComponentBase"
    case "$COMP_TYPE" in
        ai)        OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Client/AI/Components"; EVENT_TYPE="CE_AI" ;;
        ability)   OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Client/Ability";       EVENT_TYPE="CE_Ability" ;;
        weapon)    OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Client/Weapon";        EVENT_TYPE="CE_Weapon" ;;
        character) OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Client/Character";     EVENT_TYPE="CE_Character" ;;
        mode)      OUTPUT_DIR="$SCRIPTS_BASE/GamePlay/Client/Mode/Components"; EVENT_TYPE="CE_Mode" ;;
    esac
fi

OUTPUT_PATH="${PROJECT_ROOT}/${OUTPUT_DIR}/${NAME}.cs"

# ── UGC 钩子：覆写 NS/路径 ──
if [[ "${UGC_MODE:-}" == "true" && ! -f "$_CODEGEN_DIR/ugc/component-gen-ugc.sh" ]]; then
    echo "⚠️ UGC hook 不存在: ugc/component-gen-ugc.sh，回退 PGC 流程"
    UGC_MODE=false
fi
if [[ "${UGC_MODE:-}" == "true" ]]; then
    source "$_CODEGEN_DIR/ugc/component-gen-ugc.sh" config
    OUTPUT_PATH="${PROJECT_ROOT}/${OUTPUT_DIR}/${NAME}.cs"
fi

IS_NETWORK_BASE=false
[[ "$BASE_CLASS" == "ServerNetworkComponentBase" ]] && IS_NETWORK_BASE=true

# 描述兜底
[[ -z "$DESC" ]] && DESC="TODO: 添加组件描述"

# ============================================================
# 缩进常量
# ============================================================
I1="    "
I2="        "
I3="            "

# ============================================================
# 📝 [Step 1/2] 参数验证 & 配置确认
# ============================================================
echo ""
echo "📝 [Step 1/2] 参数验证 & 配置确认"
echo "   名称:     $NAME"
echo "   侧:       $SIDE"
echo "   类型:     ${COMP_TYPE}"
echo "   基类:     $BASE_CLASS"
echo "   命名空间: $NAMESPACE"
echo "   输出路径: $OUTPUT_PATH"
echo "   功能标志: $(
    flags=""
    $HAS_INIT_DATA && flags+="init-data "
    $HAS_UPDATE    && flags+="update "
    $HAS_ENTITY    && flags+="entity "
    $HAS_NETWORK   && flags+="network "
    $HAS_SYNC      && flags+="sync "
    [[ -z "$flags" ]] && flags="(无)"
    echo "$flags"
)"
echo ""

# 检查文件是否已存在
if [[ -f "$OUTPUT_PATH" ]] && ! $DRY_RUN; then
    echo "❌ 文件已存在: $OUTPUT_PATH"
    echo "   如需覆盖请先手动删除"
    exit 1
fi

# ============================================================
# 模板生成函数
# ============================================================

emit_header() {
    echo "// 该文件由 component-gen.sh 自动生成，AI 不得删除该注释"
}

emit_usings() {
    echo "using Sofunny.BiuBiuBiu2.CoreGamePlay;"
    echo "using Sofunny.BiuBiuBiu2.Data;"
    echo "using Sofunny.BiuBiuBiu2.Message;"
    echo "$USING_MSG"
    echo "using UnityEngine;"
}

emit_class_doc() {
    echo "${I1}/// <summary>"
    echo "${I1}/// ${DESC}"
    echo "${I1}/// </summary>"
}

emit_dev_rules() {
    echo "${I1}// 规则: ① 非生命周期方法必须 private ② 禁止 AddComponent ③ Register↔Unregister ④ AddUpdate↔RemoveUpdate ⑤ OnClear 清null"
    # Ability/Weapon 使用 ComponentBase 时提示 ServerNetworkComponentBase 条件
    if [[ "$SIDE" == "server" && "$BASE_CLASS" == "ComponentBase" && ("$COMP_TYPE" == "ability" || "$COMP_TYPE" == "weapon") ]]; then
        echo "${I1}// 如需处理玩家断线重连或网络区域剔除: 改继承 ServerNetworkComponentBase + SyncData 同步重连数据，System 须 AddComponent<ServerNetworkSync>"
    fi
}

emit_init_data() {
    if $HAS_INIT_DATA; then
        echo "${I2}public struct InitData : SystemBase.IComponentInitData {"
        case "$TEMPLATE" in
            findtarget)
                echo "${I2}    public float CheckDistance;"
                echo "${I2}    public float ScanInterval;"
                ;;
            move)
                echo "${I2}    public float MoveSpeed;"
                ;;
            rotate)
                echo "${I2}    public Quaternion StartRota;"
                echo "${I2}    public Quaternion EndRota;"
                echo "${I2}    public float RotaSpeed;"
                ;;
            scale)
                echo "${I2}    public Vector3 StartScale;"
                echo "${I2}    public Vector3 EndScale;"
                echo "${I2}    public float Duration;"
                ;;
            *)
                echo "${I2}    // TODO: 声明 System 传入的参数"
                ;;
        esac
        echo "${I2}}"
    fi
}

emit_private_fields() {
    if $HAS_SYSTEM_REF; then
        echo "${I2}private ${SYSTEM_TYPE} ${SYSTEM_FIELD};"
    fi
    # 模板专属字段
    case "$TEMPLATE" in
        findtarget)
            echo "${I2}private float scanTimer;"
            echo "${I2}private float scanInterval;"
            echo "${I2}private float checkDistance;"
            echo "${I2}private IGPO currentTarget;"
            ;;
        lifetime)
            echo "${I2}private float remainTime;"
            ;;
        move)
            echo "${I2}private float moveSpeed;"
            echo "${I2}private Transform rootTran;"
            ;;
        rotate)
            echo "${I2}private Quaternion startRota;"
            echo "${I2}private Quaternion endRota;"
            echo "${I2}private float rotaSpeed;"
            echo "${I2}private float elapsed;"
            ;;
        scale)
            echo "${I2}private Vector3 startScale;"
            echo "${I2}private Vector3 endScale;"
            echo "${I2}private float duration;"
            echo "${I2}private float elapsed;"
            ;;
    esac
}

emit_base_properties() {
    : # 精简版不输出基类属性列表
}

# ── 生命周期 ① OnAwake ──
emit_on_awake() {
    echo "${I2}// OnAwake: 初始化数据+Register事件 | 禁止: Dispatcher、AddUpdate"
    echo "${I2}protected override void OnAwake() {"
    if $HAS_INIT_DATA; then
        echo "${I3}var data = (InitData)initDataBase;"
    fi
    if $HAS_SYSTEM_REF; then
        echo "${I3}${SYSTEM_FIELD} = (${SYSTEM_TYPE})mySystem;"
    fi
    # 模板专属 OnAwake 逻辑
    case "$TEMPLATE" in
        findtarget)
            echo "${I3}checkDistance = data.CheckDistance;"
            echo "${I3}scanInterval = data.ScanInterval;"
            ;;
        lifetime)
            echo "${I3}// TODO: 从 GPOM 读取寿命"
            echo "${I3}// remainTime = ${SYSTEM_FIELD}.useMData.LifeTime;"
            ;;
        move)
            echo "${I3}moveSpeed = data.MoveSpeed;"
            ;;
        scale)
            echo "${I3}startScale = data.StartScale;"
            echo "${I3}endScale = data.EndScale;"
            echo "${I3}duration = data.Duration;"
            echo "${I3}iEntity.SetLocalScale(startScale);"
            ;;
        rotate)
            echo "${I3}startRota = data.StartRota;"
            echo "${I3}endRota = data.EndRota;"
            echo "${I3}rotaSpeed = data.RotaSpeed;"
            echo "${I3}iEntity.SetRota(startRota);"
            ;;
    esac
    echo "${I2}}"
}

# ── 生命周期 ② OnSetEntityObj ──
emit_on_set_entity() {
    if $HAS_ENTITY; then
        echo "${I2}// OnSetEntityObj: SetEntity后触发 | 获取Transform等引用"
        echo "${I2}protected override void OnSetEntityObj(IEntity iEntity) {"
        echo "${I3}base.OnSetEntityObj(iEntity);"
        case "$TEMPLATE" in
            move)
                echo "${I3}rootTran = iEntity.GetBodyTran(GPOData.PartEnum.RootBody);"
                ;;
            rotate|scale)
                echo "${I3}// 参考: rootTran = iEntity.GetBodyTran(GPOData.PartEnum.RootBody);"
                ;;
        esac
        echo "${I2}}"
    fi
}

# ── 生命周期 ③ OnSetNetwork ──
emit_on_set_network() {
    if $HAS_NETWORK; then
        echo "${I2}// OnSetNetwork: 网络组件就绪 | AI/GPO仅一次，Character可多次"
        echo "${I2}protected override void OnSetNetwork() {"
        echo "${I3}base.OnSetNetwork();"
        echo "${I2}}"
    fi
}

# ── 生命周期 ④ OnStart ──
emit_on_start() {
    echo "${I2}// OnStart: OnAwake后1帧 | 可Dispatcher、AddUpdate"
    echo "${I2}protected override void OnStart() {"
    echo "${I3}base.OnStart();"
    if $HAS_UPDATE; then
        echo "${I3}AddUpdate(OnUpdate);"
    fi
    echo "${I2}}"
}

# ── OnUpdate ──
emit_on_update() {
    if $HAS_UPDATE; then
        echo "${I2}private void OnUpdate(float delta) {"
        case "$TEMPLATE" in
            findtarget)
                echo "${I3}if (!isLoadEntityBase) return;"
                echo "${I3}scanTimer += delta;"
                echo "${I3}if (scanTimer < scanInterval) return;"
                echo "${I3}scanTimer = 0f;"
                echo ""
                echo "${I3}IGPO bestTarget = null;"
                echo "${I3}float bestDist = checkDistance;"
                echo "${I3}var gpoList = mAI.GPOList;"
                echo "${I3}if (gpoList == null) return;"
                echo "${I3}foreach (var gpo in gpoList) {"
                echo "${I3}    if (gpo.IsClear()) continue;"
                echo "${I3}    if (gpo.GetTeamID() == iGPO.GetTeamID()) continue;"
                echo "${I3}    if (gpo.HasTag(GamePlayTagData.TagEnum.Dead)) continue;"
                echo "${I3}    float dist = Vector3.Distance(iEntity.GetPoint(), gpo.GetPoint());"
                echo "${I3}    if (dist > bestDist) continue;"
                echo "${I3}    // TODO: 可选遮挡检测 Physics.Raycast"
                echo "${I3}    bestDist = dist;"
                echo "${I3}    bestTarget = gpo;"
                echo "${I3}}"
                echo "${I3}if (bestTarget != currentTarget) {"
                echo "${I3}    currentTarget = bestTarget;"
                echo "${I3}    mySystem.Dispatcher(new SE_AI.Event_SetInsightTarget { TargetGPO = currentTarget });"
                echo "${I3}}"
                ;;
            lifetime)
                echo "${I3}remainTime -= delta;"
                echo "${I3}if (remainTime <= 0f) {"
                echo "${I3}    MsgRegister.Dispatcher(new SM_AI.Event_RemoveAI { GpoId = GpoID });"
                echo "${I3}}"
                ;;
            move)
                echo "${I3}if (!isLoadEntityBase) return;"
                echo "${I3}if (rootTran == null) return;"
                echo "${I3}// iEntity.SetPoint() 等价 rootTran.position（会同步到客户端）"
                echo "${I3}var point = iEntity.GetPoint() + rootTran.forward * moveSpeed * delta;"
                echo "${I3}iEntity.SetPoint(point);"
                ;;
            rotate)
                echo "${I3}if (!isLoadEntityBase) return;"
                echo "${I3}// iEntity.SetRota() 等价 rootTran.rotation（会同步到客户端）"
                echo "${I3}elapsed += delta * rotaSpeed;"
                echo "${I3}float t = Mathf.Clamp01(elapsed);"
                echo "${I3}iEntity.SetRota(Quaternion.Slerp(startRota, endRota, t));"
                echo "${I3}if (t >= 1f) RemoveUpdate(OnUpdate);"
                ;;
            scale)
                echo "${I3}if (!isLoadEntityBase) return;"
                echo "${I3}elapsed += delta;"
                echo "${I3}float t = Mathf.Clamp01(elapsed / duration);"
                echo "${I3}// iEntity.SetLocalScale() 等价 rootTran.localScale（会同步到客户端）"
                echo "${I3}iEntity.SetLocalScale(Vector3.Lerp(startScale, endScale, t));"
                echo "${I3}if (t >= 1f) RemoveUpdate(OnUpdate);"
                ;;
        esac
        echo "${I2}}"
    fi
}

# ── 生命周期 ⑤ OnClear ──
emit_on_clear() {
    echo "${I2}// OnClear: Unregister + RemoveUpdate + null所有引用"
    echo "${I2}protected override void OnClear() {"
    # 模板专属 Unregister
    # (当前无模板需要 Unregister)
    if $HAS_UPDATE; then
        echo "${I3}RemoveUpdate(OnUpdate);"
    fi
    # 模板专属 null
    case "$TEMPLATE" in
        findtarget)
            echo "${I3}currentTarget = null;"
            ;;
    esac
    case "$TEMPLATE" in
        move)
            echo "${I3}rootTran = null;"
            ;;
    esac
    if $HAS_SYSTEM_REF; then
        echo "${I3}${SYSTEM_FIELD} = null;"
    fi
    echo "${I3}base.OnClear();"
    echo "${I2}}"
}

# ── Sync（服务端 ServerNetworkComponentBase 专用）──
emit_sync_data() {
    if $HAS_SYNC; then
        echo "${I2}// SyncData: 玩家进入视野时同步当前状态"
        echo "${I2}protected override ITargetRpc SyncData() {"
        echo "${I3}return null;"
        echo "${I2}}"
    fi
}

# ── 模板专属私有方法 ──
emit_template_private_methods() {
    : # 当前无模板需要私有方法
}

# ============================================================
# 主模板组装
# ============================================================
generate() {
    emit_header
    emit_usings
    echo ""
    echo "namespace ${NAMESPACE} {"

    emit_class_doc
    emit_dev_rules
    echo "${I1}public class ${NAME} : ${BASE_CLASS} {"
    echo ""

    # InitData
    emit_init_data

    # 私有字段
    emit_private_fields
    echo ""

    # ① OnAwake
    emit_on_awake
    echo ""

    # ② OnStart
    emit_on_start
    echo ""

    # ③ OnClear
    emit_on_clear
    echo ""

    # ④ OnSetEntityObj
    emit_on_set_entity
    if $HAS_ENTITY; then echo ""; fi

    # ⑤ OnSetNetwork
    emit_on_set_network
    if $HAS_NETWORK; then echo ""; fi

    # ⑥ Sync（仅服务端 + ServerNetworkComponentBase）
    if $IS_NETWORK_BASE; then
        emit_sync_data
        echo ""
    fi

    # ⑦ OnUpdate
    emit_on_update
    if $HAS_UPDATE; then echo ""; fi

    # ⑧ 模板专属私有方法
    if [[ -n "$TEMPLATE" ]]; then
        emit_template_private_methods
        echo ""
    fi

    # 关闭 class + namespace
    echo "${I1}}"
    echo "}"
}

# ============================================================
# 📄 [Step 2/2] 生成组件文件
# ============================================================
CONTENT="$(generate)"

if $DRY_RUN; then
    echo "📋 [Step 2/2] 预览模式 — 不写入文件"
    echo "────────────────────────────────────────────────────────────"
    echo "$CONTENT"
    echo "────────────────────────────────────────────────────────────"
    echo ""
    echo "📋 预览完成，未创建任何文件"
else
    echo "📄 [Step 2/2] 生成组件文件..."
    mkdir -p "$(dirname "$OUTPUT_PATH")"
    echo "$CONTENT" > "$OUTPUT_PATH"
    echo "   ✅ 已创建: ${OUTPUT_PATH}"
fi

# ============================================================
# 日志
# ============================================================
LOG_DIR="${PROJECT_ROOT}/harness/temp"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/component-gen-${NAME}-$(date +%Y%m%d_%H%M%S).log"

{
    echo "═══════════════════════════════════════════════════════════"
    echo "  工具: component-gen.sh"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  参数: --name ${NAME} --side ${SIDE} --type ${COMP_TYPE}$(
        [[ -n "$TEMPLATE" ]]   && echo " --template ${TEMPLATE}"
        $HAS_INIT_DATA && echo ' --has-init-data'
        $HAS_UPDATE    && echo ' --has-update'
        $HAS_ENTITY    && echo ' --has-entity'
        $HAS_NETWORK   && echo ' --has-network'
        $HAS_SYNC      && echo ' --has-sync'
        [[ "$DESC" != "TODO: 添加组件描述" ]] && echo " --desc \"${DESC}\""
        $DRY_RUN       && echo ' --dry-run'
    )"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📊 派生配置:"
    echo "  命名空间: ${NAMESPACE}"
    echo "  基类:     ${BASE_CLASS}"
    echo "  输出目录: ${OUTPUT_DIR}"
    echo ""
    if $DRY_RUN; then
        echo "📋 模式: 预览（dry-run），未创建文件"
    else
        echo "📁 新建文件 (1 个):"
        echo "  [新建] ${OUTPUT_PATH}"
    fi
    echo ""
    echo "📋 后续步骤:"
    echo "  1. 在 ${NAME}.cs 中填充 TODO 标记的逻辑"
    if $HAS_INIT_DATA; then
        echo "  2. 在对应的 System 中通过 AddComponent<${NAME}>(new ${NAME}.InitData { ... }) 添加组件"
    else
        echo "  2. 在对应的 System 中通过 AddComponent<${NAME}>() 添加组件"
    fi
    echo "  3. 确保 OnClear 中清理了所有资源"
    if $HAS_SYNC; then
        echo "  4. 实现 SyncData() 返回正确的协议对象"
    fi
} > "$LOG_FILE"

echo ""
echo "📋 执行日志已保存: $LOG_FILE"

# ============================================================
# 总结
# ============================================================
echo ""
echo "✅ component-gen.sh 执行完成！"
echo ""
if ! $DRY_RUN; then
    echo "📁 创建的文件:"
    echo "   + ${OUTPUT_PATH}"
    echo ""
fi
echo "📋 后续步骤:"
echo "   1. 填充 ${NAME}.cs 中的 TODO 标记"
if $HAS_INIT_DATA; then
    echo "   2. 在 System 中: AddComponent<${NAME}>(new ${NAME}.InitData { ... })"
else
    echo "   2. 在 System 中: AddComponent<${NAME}>()"
fi
echo "   3. 确保 OnClear 清理了所有资源（Register ↔ Unregister, AddUpdate ↔ RemoveUpdate）"
if $HAS_SYNC; then
    echo "   4. 实现 SyncData() 返回正确的同步协议"
fi
echo ""
