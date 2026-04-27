#!/bin/bash
# ============================================================
# gpom-gen.sh — GPOM 模板数据生成工具
# 生成 GPOM_{Name}.cs (struct + Set class)
# 完全匹配项目 csv-gen 工具输出格式
#
# OUTPUT FILES (供 Phase 4 技术文档 S-05 引用):
#   CREATE: Assets/Scripts/Template/gpo/GPOM_{Name}.cs
#           — GPOM struct(IGPOM接口) + static Set 类(Data数组+查询方法)
#           — 包含 12 个 IGPOM 基础字段 + --custom-fields 自定义字段
#   MODIFY: (无)
# ============================================================
set -euo pipefail

# ============================================================
# 参数解析
# ============================================================
NAME=""
DISPLAY_NAME=""
CUSTOM_FIELDS=""
GPO_TYPE=""
PROJECT_ROOT="."
ENTRIES=()

usage() {
    cat <<EOF
用法: gpom-gen.sh --name <名称> --display-name <中文名> [选项]

必需参数:
  --name           GPOM 类型名称 (PascalCase, 如 GoldenEgg)
  --display-name   中文显示名称 (如 "夺金-蛋")

可选参数:
  --custom-fields  自定义字段，含中文描述
                   格式: "Hp:int:血量,MoveSpeed:float:移动速度"
  --gpo-type       GpoType 值 (填入数据时必需，如 10)
  --entry          数据条目 (可多次指定)
                   格式: "Sign=XXX,Name=中文名,Hp=1000"
                   必填字段: Sign, Name
                   Id 由工具自动从 gpo.cs 读取，无需手传
                   int[] 格式: "GpoTag=[1,2,3]" 或 "GpoTag=[]"
  --project-root   项目根目录 (默认当前目录)

基础字段（自动包含，无需指定）:
  AssetSign, GpoDropId, GpoDropType, GpoSoConfig, GpoTag, GpoType,
  Id, MatchMode, Name, Quality, Sign

示例:
  gpom-gen.sh --name GoldenEgg --display-name "夺金-蛋" \\
    --custom-fields "Hp:int:血量" --gpo-type 10 \\
    --entry "Sign=GoldenEgg,Name=夺金-蛋,Hp=1000" \\
    --entry "Sign=GoldenBigEgg,Name=夺金-巨蛋,Hp=10000"
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)           NAME="$2"; shift 2 ;;
        --display-name)   DISPLAY_NAME="$2"; shift 2 ;;
        --custom-fields)  CUSTOM_FIELDS="$2"; shift 2 ;;
        --gpo-type)       GPO_TYPE="$2"; shift 2 ;;
        --entry)          ENTRIES+=("$2"); shift 2 ;;
        --ugc)            UGC_MODE="true"; shift ;;
        --project-root)   PROJECT_ROOT="$2"; shift 2 ;;
        -h|--help)        usage ;;
        *)                echo "❌ 未知参数: $1"; usage ;;
    esac
done

[[ -z "$NAME" ]] && echo "❌ 必须提供 --name" && usage
[[ -z "$DISPLAY_NAME" ]] && echo "❌ 必须提供 --display-name" && usage

if [[ ${#ENTRIES[@]} -gt 0 && -z "$GPO_TYPE" ]]; then
    echo "❌ 提供 --entry 时必须同时提供 --gpo-type"
    exit 1
fi

# ============================================================
# 路径配置
# ============================================================
ROOT="${PROJECT_ROOT}"

# 自动检测项目布局
CODEGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_CODEGEN_DIR="$CODEGEN_DIR"
source "$CODEGEN_DIR/path-config.sh"

GPOM_DIR="$ROOT/$SCRIPTS_BASE/Template/gpo"
GPOM_FILE="$GPOM_DIR/GPOM_${NAME}.cs"
GPO_DATA_FILE="$ROOT/$SCRIPTS_BASE/Template/data/gpo.cs"

# 模板变量（PGC 默认值，UGC 钩子可覆写）
GPOM_NS="Sofunny.BiuBiuBiu2.Template"
GPOM_STRUCT_NAME="GPOM_${NAME}"
GPOM_SET_CLASS_NAME="GPOM_${NAME}Set"
GPOM_ID_PREFIX="Id_"
GPOM_SIGN_PREFIX="Sign_"
GPOM_GPOTYPE_REF="GpoTypeSet.Id_"

# ── UGC 钩子：覆写路径/NS/名称 ──
if [[ "${UGC_MODE:-}" == "true" && ! -f "$_CODEGEN_DIR/ugc/gpom-gen-ugc.sh" ]]; then
    echo "⚠️ UGC hook 不存在: ugc/gpom-gen-ugc.sh，回退 PGC 流程"
    UGC_MODE=false
fi
if [[ "${UGC_MODE:-}" == "true" ]]; then
    source "$_CODEGEN_DIR/ugc/gpom-gen-ugc.sh" config
fi

# ============================================================
# GpoId 校验：从 gpo.cs 读取正确的全局 GpoId
# Id 完全由工具自动从 gpo.cs 读取，不接受手动传参。
# --entry 中如果传了 Id=N 会被忽略（以 gpo.cs 为准）。
# ============================================================
lookup_gpoid_by_sign() {
    local sign="$1"
    if [[ "${UGC_MODE:-}" == "true" ]]; then
        # UGC: 从 GpoTypeSet_UGC.cs 查找 Id_UGC{Sign} = N
        if [[ ! -f "$UGC_GPOTYPE_SET" ]]; then
            echo ""
            return
        fi
        local ugc_id
        ugc_id=$(grep "Id_UGC${sign}" "$UGC_GPOTYPE_SET" | grep -oE '= *[0-9]+' | grep -oE '[0-9]+' | head -1 || true)
        echo "$ugc_id"
        return
    fi
    if [[ ! -f "$GPO_DATA_FILE" ]]; then
        echo ""
        return
    fi
    # 在 gpo.cs 中查找 new Gpo( ID, GpoType, ..., "Sign", ... )
    # 格式: new Gpo( 55, 31, "赛博靶子", "CyberTarget", "CyberTarget", "" )
    local line
    line=$(grep "\"${sign}\"" "$GPO_DATA_FILE" | grep "new Gpo(" | head -1)
    if [[ -z "$line" ]]; then
        echo ""
        return
    fi
    # 提取第一个参数（GpoId）
    local gpoid
    gpoid=$(echo "$line" | sed 's/.*new Gpo( *\([0-9]*\).*/\1/')
    echo "$gpoid"
}

# ============================================================
# 基础字段定义（平行数组，兼容 bash 3.2）
# ============================================================
BASE_NAMES=(AssetSign GpoDropId GpoDropType GpoSoConfig GpoTag GpoType Id MatchMode Name Quality Sign)
BASE_DESCS=("GPO资产标识" "GPO掉落ID" "GPO掉落类型" "GpoSO配置" "GPO标签类型" "GPO类型" "GPOID" "匹配模式" "GPO名称" "GPO 品质" "GPO唯一标识")
BASE_TYPES=("string" "int[]" "ushort" "string" "int[]" "int" "int" "int" "string" "byte" "string")

# ============================================================
# 合并字段查找函数（用平行数组模拟关联数组）
# ============================================================
ALL_NAMES=()
ALL_TYPES=()
ALL_DESCS=()

# 先填入基础字段
for ((i=0; i<${#BASE_NAMES[@]}; i++)); do
    ALL_NAMES+=("${BASE_NAMES[$i]}")
    ALL_TYPES+=("${BASE_TYPES[$i]}")
    ALL_DESCS+=("${BASE_DESCS[$i]}")
done

# ============================================================
# 解析自定义字段
# ============================================================
CUSTOM_NAMES=()
if [[ -n "$CUSTOM_FIELDS" ]]; then
    IFS=',' read -ra pairs <<< "$CUSTOM_FIELDS"
    for pair in "${pairs[@]}"; do
        IFS=':' read -r fname ftype fdesc <<< "$pair"
        CUSTOM_NAMES+=("$fname")
        ALL_NAMES+=("$fname")
        ALL_TYPES+=("$ftype")
        ALL_DESCS+=("${fdesc:-$fname}")
    done
fi

# 按字段名查类型
lookup_type() {
    local key="$1"
    for ((i=0; i<${#ALL_NAMES[@]}; i++)); do
        if [[ "${ALL_NAMES[$i]}" == "$key" ]]; then
            echo "${ALL_TYPES[$i]}"
            return
        fi
    done
    echo ""
}

# 按字段名查描述
lookup_desc() {
    local key="$1"
    for ((i=0; i<${#ALL_NAMES[@]}; i++)); do
        if [[ "${ALL_NAMES[$i]}" == "$key" ]]; then
            echo "${ALL_DESCS[$i]}"
            return
        fi
    done
    echo ""
}

# ============================================================
# 合并全部字段 + 按字母序排列
# ============================================================
IFS=$'\n' SORTED_NAMES=($(printf '%s\n' "${ALL_NAMES[@]}" | sort)); unset IFS

# ============================================================
# 文件存在性检查
# ============================================================
if [[ -f "$GPOM_FILE" ]]; then
    echo "❌ 文件已存在: $GPOM_FILE"
    exit 1
fi

echo "📝 配置信息:"
echo "   名称: GPOM_$NAME"
echo "   显示名: $DISPLAY_NAME"
echo "   总字段: ${#SORTED_NAMES[@]} 个 (基础 ${#BASE_NAMES[@]} + 自定义 ${#CUSTOM_NAMES[@]})"
echo "   数据条目: ${#ENTRIES[@]} 个"
echo ""

# ============================================================
# 工具函数
# ============================================================
to_camel() {
    local name="$1"
    echo "$(echo "${name:0:1}" | tr '[:upper:]' '[:lower:]')${name:1}"
}

to_csharp_value() {
    local ftype="$1"
    local val="$2"
    case "$ftype" in
        string)     echo "\"$val\"" ;;
        float)
            if [[ "$val" == *f ]]; then echo "$val"
            else echo "${val}f"
            fi ;;
        "int[]")
            if [[ "$val" == "[]" || -z "$val" ]]; then echo "new int[]{}"
            else
                local inner="${val#[}"
                inner="${inner%]}"
                echo "new int[]{$inner}"
            fi ;;
        "string[]")
            if [[ "$val" == "[]" || -z "$val" ]]; then echo "new string[]{}"
            else echo "new string[]{$val}"
            fi ;;
        *)          echo "$val" ;;
    esac
}

default_value() {
    local ftype="$1"
    case "$ftype" in
        int)        echo "0" ;;
        float)      echo "0f" ;;
        byte)       echo "0" ;;
        ushort)     echo "0" ;;
        bool)       echo "false" ;;
        string)     echo "\"\"" ;;
        "int[]")    echo "new int[]{}" ;;
        "string[]") echo "new string[]{}" ;;
        *)          echo "default(${ftype})" ;;
    esac
}

# 解析 entry 中的 key=value 对
parse_entry_val() {
    local entry_str="$1"
    local key="$2"
    local result=""
    IFS=',' read -ra kvs <<< "$entry_str"
    for kv in "${kvs[@]}"; do
        local k="${kv%%=*}"
        local v="${kv#*=}"
        if [[ "$k" == "$key" ]]; then
            result="$v"
            break
        fi
    done
    echo "$result"
}

# ============================================================
# GpoId 自动填充：每条 entry 的 Id 强制从 gpo.cs 读取
# - --entry 中即使传了 Id=N 也会被替换为 gpo.cs 的值
# ============================================================
VALIDATED_ENTRIES=()
for entry_str in "${ENTRIES[@]+"${ENTRIES[@]}"}"; do
    e_sign=$(parse_entry_val "$entry_str" "Sign")
    if [[ -n "$e_sign" ]]; then
        correct_id=$(lookup_gpoid_by_sign "$e_sign")
        if [[ -z "$correct_id" ]]; then
            if [[ "${UGC_MODE:-}" == "true" ]]; then
                echo "❌ Sign=${e_sign} 在 GpoTypeSet_UGC.cs 中未找到 Id_UGC${e_sign}。请确认 gpo-gen.sh --ugc 已先执行" >&2
            else
                echo "❌ Sign=${e_sign} 在 gpo.cs 中未找到 GpoId。请确认 gpo-gen.sh 已先执行" >&2
            fi
            exit 1
        fi
        # 移除 entry 中可能存在的手传 Id，统一用 gpo.cs 的值
        entry_str=$(echo "$entry_str" | sed 's/,\?Id=[0-9]*//' | sed 's/^,//')
        entry_str="${entry_str},Id=${correct_id}"
        echo "🔍 Id 自动填充: Sign=${e_sign} → Id=${correct_id} (来自 gpo.cs)"
    fi
    VALIDATED_ENTRIES+=("$entry_str")
done
ENTRIES=("${VALIDATED_ENTRIES[@]+"${VALIDATED_ENTRIES[@]}"}")

# 生成一条数据的构造函数参数
gen_entry_args() {
    local entry_str="$1"
    local args=""

    for fn in "${SORTED_NAMES[@]}"; do
        local ftype
        ftype=$(lookup_type "$fn")
        local val
        val=$(parse_entry_val "$entry_str" "$fn")

        if [[ -n "$val" ]]; then
            val=$(to_csharp_value "$ftype" "$val")
        elif [[ "$fn" == "AssetSign" ]]; then
            local sign_val
            sign_val=$(parse_entry_val "$entry_str" "Sign")
            val=$(to_csharp_value "string" "$sign_val")
        elif [[ "$fn" == "GpoType" && -n "$GPO_TYPE" ]]; then
            val="$GPO_TYPE"
        elif [[ "$fn" == "Quality" ]]; then
            val="1"
        else
            val=$(default_value "$ftype")
        fi

        if [[ -n "$args" ]]; then
            args="$args, $val"
        else
            args="$val"
        fi
    done
    echo "$args"
}

# ============================================================
# 生成 GPOM_{Name}.cs
# ============================================================
echo "📄 创建 ${GPOM_STRUCT_NAME}.cs ..."

T=$'\t'

{
    echo '// 该文件由 gpom-gen.sh 自动生成，AI 不得删除该注释'
    echo 'using System;'
    echo 'using System.Collections.Generic;'
    echo ''
    echo ''
    echo "namespace ${GPOM_NS} {"
    echo "    /// <summary>"
    echo "    /// ${DISPLAY_NAME}"
    echo "    /// </summary>"
    echo "${T}public struct ${GPOM_STRUCT_NAME} : IGPOM {"

    # --- 字段声明（按字母序，每个带 summary） ---
    for fn in "${SORTED_NAMES[@]}"; do
        echo "${T}${T}/// <summary>"
        echo "${T}${T}/// $(lookup_desc "$fn")"
        echo "${T}${T}/// </summary>"
        echo "${T}${T}public readonly $(lookup_type "$fn") ${fn} { get; }"
    done

    # --- IGPOM 接口实现 ---
    echo ''
    echo "${T}${T}// 实现IGPOM接口"
    echo "${T}${T}public string GetAssetSign() => AssetSign;"
    echo "${T}${T}public int[] GetGpoDropId() => GpoDropId;"
    echo "${T}${T}public ushort GetGpoDropType() => GpoDropType;"
    echo "${T}${T}public string GetGpoSoConfig() => GpoSoConfig;"
    echo "${T}${T}public int[] GetGpoTag() => GpoTag;"
    echo "${T}${T}public int GetGpoType() => GpoType;"
    echo "${T}${T}public int GetId() => Id;"
    echo "${T}${T}public int GetMatchMode() => MatchMode;"
    echo "${T}${T}public string GetName() => Name;"
    echo "${T}${T}public byte GetQuality() => Quality;"
    echo "${T}${T}public string GetSign() => Sign;"

    # --- 构造函数 ---
    echo ''
    echo '        /// <summary>'
    echo '        /// 构造函数'
    echo '        /// </summary>'

    for fn in "${SORTED_NAMES[@]}"; do
        cn=$(to_camel "$fn")
        echo "        /// <param name=\"${cn}\"></param>"
    done

    # 构造签名
    param_list=""
    for fn in "${SORTED_NAMES[@]}"; do
        cn=$(to_camel "$fn")
        ft=$(lookup_type "$fn")
        if [[ -n "$param_list" ]]; then
            param_list="${param_list}, ${ft} ${cn}"
        else
            param_list="${ft} ${cn}"
        fi
    done
    echo "${T}${T}public ${GPOM_STRUCT_NAME}( ${param_list} ) {"

    for fn in "${SORTED_NAMES[@]}"; do
        cn=$(to_camel "$fn")
        echo "${T}${T}${T}${fn} = ${cn};"
    done
    echo "${T}${T}}"

    echo "${T}}"
    echo ''

    # ========== Set 类 ==========
    echo '    /// <summary>'
    echo "    /// ${GPOM_SET_CLASS_NAME} that holds all the table data"
    echo '    /// </summary>'
    echo "    public static class ${GPOM_SET_CLASS_NAME} {"
    echo "        public static readonly ${GPOM_STRUCT_NAME}[] Data;"

    # --- 常量（从 entries 生成） ---
    if [[ ${#ENTRIES[@]} -gt 0 ]]; then
        echo "${T}${T}/// <summary>"
        echo "${T}${T}/// 常量类型"
        echo "${T}${T}/// </summary>"
        echo ''
        echo ''
        for entry_str in "${ENTRIES[@]}"; do
            e_sign=$(parse_entry_val "$entry_str" "Sign")
            e_id=$(parse_entry_val "$entry_str" "Id")
            echo "${T}${T}public const int ${GPOM_ID_PREFIX}${e_sign} = ${e_id};"
        done
        echo "${T}${T}/// <summary>"
        echo "${T}${T}/// 常量类型"
        echo "${T}${T}/// </summary>"
        echo ''
        echo ''
        for entry_str in "${ENTRIES[@]}"; do
            e_sign=$(parse_entry_val "$entry_str" "Sign")
            echo "${T}${T}public const string ${GPOM_SIGN_PREFIX}${e_sign} = \"${e_sign}\";"
        done
    fi

    echo ''
    echo '        /// <summary>'
    echo '        /// 构造函数'
    echo '        /// </summary>'
    echo "        static ${GPOM_SET_CLASS_NAME}() {"
    echo "            Data = new ${GPOM_STRUCT_NAME}[] {"

    if [[ ${#ENTRIES[@]} -gt 0 ]]; then
        first=true
        for entry_str in "${ENTRIES[@]}"; do
            args=$(gen_entry_args "$entry_str")
            if [[ "$first" == true ]]; then
                echo "${T}${T}${T} new ${GPOM_STRUCT_NAME}( ${args} )"
                first=false
            else
                echo "${T}${T}${T}, new ${GPOM_STRUCT_NAME}( ${args} )"
            fi
        done
    fi

    echo '            };'
    echo '        }'
    echo ''
    echo "${T}${T}/// <summary>"
    echo "${T}${T}/// 根据指定条件获取单个 ${GPOM_STRUCT_NAME}"
    echo "${T}${T}/// </summary>"
    echo "${T}${T}/// <param name=\"Id\"></param>"
    echo "${T}${T}/// <param name=\"MatchMode\"></param>"
    echo "${T}${T}public static ${GPOM_STRUCT_NAME} GetGPOMByIdAndMatchMode(int id, int matchMode = 0) {"
    echo "${T}${T}${T}foreach (${GPOM_STRUCT_NAME} data in Data) {"
    echo "${T}${T}${T}${T}if (data.Id == id && data.MatchMode == matchMode) {"
    echo "${T}${T}${T}${T}${T}return data;"
    echo "${T}${T}${T}${T}}"
    echo "${T}${T}${T}}"
    echo "${T}${T}${T}return default(${GPOM_STRUCT_NAME});"
    echo "${T}${T}}"
    echo '    }'

    echo '}'

} > "$GPOM_FILE"

echo ''
echo '✅ gpom-gen.sh 执行完成！'
echo ''
echo '📁 创建的文件:'
echo "   + $GPOM_FILE"
if [[ ${#ENTRIES[@]} -gt 0 ]]; then
    echo "📊 数据条目: ${#ENTRIES[@]} 条"
else
    echo ''
    echo '📋 后续步骤:'
    echo "   使用 --entry 和 --gpo-type 参数重新运行以填入数据"
fi

# ============================================================
# 输出执行日志（供 AI Agent 查阅）
# ============================================================
LOG_DIR="${ROOT}/harness/temp"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/gpom-gen-${NAME}-$(date +%Y%m%d_%H%M%S).log"

{
    echo "═══════════════════════════════════════════════════════"
    echo "  工具: gpom-gen.sh"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  参数: --name ${NAME} --display-name ${DISPLAY_NAME}"
    if [[ -n "${GPO_TYPE:-}" ]]; then echo "         --gpo-type ${GPO_TYPE}"; fi
    if [[ -n "${CUSTOM_FIELDS:-}" ]]; then echo "         --custom-fields: ${CUSTOM_FIELDS}"; fi
    echo "         --entry: ${#ENTRIES[@]} 条"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "📁 新建文件 (1 个):"
    echo "  [新建] $GPOM_FILE"
    echo ""
    echo "📝 修改文件 (0 个):"
    echo "  （无）"
    if [[ ${#ENTRIES[@]} -gt 0 ]]; then
        echo ""
        echo "📊 数据条目: ${#ENTRIES[@]} 条"
    fi
    echo ""
    echo "📋 后续步骤:"
    if [[ ${#ENTRIES[@]} -eq 0 ]]; then
        echo "  1. 使用 --entry 和 --gpo-type 参数重新运行以填入数据"
    else
        echo "  1. 运行 gpo-gen.sh 创建对应的 GPO Server/Client AI System"
    fi
} > "$LOG_FILE"

echo ""
echo "📋 执行日志已保存: $LOG_FILE"
