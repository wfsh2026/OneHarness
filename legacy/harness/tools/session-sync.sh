#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# session-sync.sh — Session 状态自动同步工具
# 替代 AI 手动编辑 active.md / session-log.md
# ============================================================
# 用法: session-sync.sh <command> --feature <name> [options]
#
# 子命令:
#   stage    — 更新 active.md 当前阶段行
#   gate     — 追加门控记录
#   progress — 追加主进度条目
#   doc      — 追加文档产出条目
#   adr      — 追加关键决策记录
#   bug      — 追加 Bug 记录（同时写 session-log 推理）
#   log      — 纯追加 session-log 条目
#   lesson   — 追加规范沉淀条目
#   ux       — 开发里程碑管理（--init 初始化 / --id 更新状态）
#
# 公共参数:
#   --feature <name>    session-state 目录名（如"代码生成工具"）
#   --project-root <path> 项目根目录（默认: 脚本推算）
#   --dry-run           预览模式，不实际写入
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT=""
FEATURE="${SESSION_FEATURE:-}"  # 支持环境变量 SESSION_FEATURE
DRY_RUN=false

# ─── 临时文件清理 ───
_TMP_FILES=()
_cleanup() {
    for f in "${_TMP_FILES[@]+${_TMP_FILES[@]}}"; do
        rm -f "$f" 2>/dev/null
    done
}
trap _cleanup EXIT

# 安全创建临时文件（自动注册清理）
_mktemp() {
    local tmp
    tmp=$(mktemp)
    _TMP_FILES+=("$tmp")
    echo "$tmp"
}

# ─── 颜色 ───
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── 帮助 ───
show_help() {
    echo "用法: session-sync.sh <command> --feature <name> [options]"
    echo ""
    echo "子命令:"
    echo "  stage    --text <阶段描述> --background <背景> --reasoning <推理> --conclusion <结论> [--phase <N>]"
    echo "  gate     --name <门控名> --result <结果> --background <背景> --reasoning <推理> --conclusion <结论> [--time <时间>]"
    echo "  progress --num <序号> --agent <Agent> --content <内容> --background <背景> --reasoning <推理> --conclusion <结论> [--status <状态>]"
    echo "  doc      --name <文档名> --path <路径> --background <背景> --reasoning <推理> --conclusion <结论> [--status <状态>]"
    echo "  adr      --id <编号> --point <决策点> --decision <方案> --background <背景> --reasoning <推理> --conclusion <结论> [--time <时间>]"
    echo "  bug      --id <编号> --symptom <现象> --cause <根因> --fix <修复>"
    echo "  log      --title <标题> --background <背景> --reasoning <推理> --conclusion <结论>"
    echo "  lesson   --id <编号> --text <规范内容> --background <背景> --reasoning <推理> --conclusion <结论>"
    echo "  ux       --init | --id <UX-N> --status <📋|🔄|✅|❌> [--background <背景> --reasoning <推理> --conclusion <结论>]"
    echo "  init     [--template dev|discussion] — 初始化 active.md + session-log.md"
    echo ""
    echo "门控继承链 (--phase N):"
    echo "  1:无门控  2:gate-check p2  3:继承p2  4:gate-check p4"
    echo "  5~7:继承p4  8:gate-check p8  9+:继承p8"
    echo ""
    echo "公共参数:"
    echo "  --feature <name>       session-state 目录名（必需）"
    echo "  --project-root <path>  项目根目录"
    echo "  --dry-run              预览模式"
    exit 0
}

# ─── 错误处理 ───
die() { echo -e "${RED}❌ $1${NC}" >&2; exit 1; }
info() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
preview() { echo -e "${CYAN}[预览] $1${NC}"; }

# ─── 三段式字段最小字数校验 ───
# 用法: check_field_min <子命令名> <字段名> <文本> [最小字数]
# 默认阈值矩阵（字段 × 子命令）：
#   reasoning: log=80, adr=60, stage/gate/progress/doc/lesson=40
#   background: log=50, adr=40, 其余=30
#   conclusion: log=40, adr=35, 其余=25
check_field_min() {
    local cmd_name="$1"
    local field_name="$2"
    local text="$3"
    local min_len="${4:-}"

    # 如果未指定阈值，按 字段×子命令 自动选择
    if [ -z "$min_len" ]; then
        case "$field_name" in
            reasoning)
                case "$cmd_name" in
                    log)     min_len=120 ;;
                    adr)     min_len=100 ;;
                    lesson)  min_len=80 ;;
                    doc)     min_len=80 ;;
                    progress) min_len=80 ;;
                    *)       min_len=60 ;;
                esac
                ;;
            background)
                case "$cmd_name" in
                    log)     min_len=60 ;;
                    adr)     min_len=50 ;;
                    doc)     min_len=40 ;;
                    progress) min_len=40 ;;
                    *)       min_len=30 ;;
                esac
                ;;
            conclusion)
                case "$cmd_name" in
                    log)     min_len=50 ;;
                    adr)     min_len=45 ;;
                    doc)     min_len=35 ;;
                    progress) min_len=35 ;;
                    *)       min_len=30 ;;
                esac
                ;;
            *)
                min_len=15
                ;;
        esac
    fi

    # 计算 UTF-8 字符数（中文字 = 1，英文字母 = 1）
    # 注意：Git Bash 默认 locale 可能不是 UTF-8，必须显式设置
    local char_count
    char_count=$(echo -n "$text" | LC_ALL=en_US.UTF-8 wc -m)

    if [ "$char_count" -lt "$min_len" ]; then
        local hint=""
        case "$field_name" in
            reasoning)  hint="请补充：备选方案列举、各方案优劣/否定理由、最终选择依据、潜在风险。一句话推理 = 没有推理。" ;;
            background) hint="请补充：触发事件、当前状态、前置条件、影响范围。" ;;
            conclusion) hint="请补充：产出物清单、下一步计划、影响范围、遗留问题。" ;;
        esac
        die "$cmd_name 的 --$field_name 内容过短（${char_count}字 < 最低${min_len}字）。\n   规则：一句话 = 无效记录。$hint"
    fi
}

# 向后兼容旧调用签名
check_reasoning_min() {
    check_field_min "$1" "reasoning" "$2" "${3:-}"
}

# 三段式全字段校验（一次调用校验 background + reasoning + conclusion）
check_three_part_min() {
    local cmd_name="$1"
    local background="$2"
    local reasoning="$3"
    local conclusion="$4"
    check_field_min "$cmd_name" "background" "$background"
    check_field_min "$cmd_name" "reasoning" "$reasoning"
    check_field_min "$cmd_name" "conclusion" "$conclusion"
}

# ─── 路径解析 ───
resolve_paths() {
    if [ -z "$PROJECT_ROOT" ]; then
        PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    fi
    [ -z "$FEATURE" ] && die "--feature 参数必需"

    SESSION_DIR="$PROJECT_ROOT/harness/session-state/$FEATURE"
    ACTIVE_FILE="$SESSION_DIR/active.md"
    LOG_FILE="$SESSION_DIR/session-log.md"

    [ -f "$ACTIVE_FILE" ] || die "active.md 不存在: $ACTIVE_FILE"
    [ -f "$LOG_FILE" ] || die "session-log.md 不存在: $LOG_FILE"
}

# ============================================================
# 核心操作函数
# ============================================================

# 在指定锚点(## 标题)之前插入内容
# 如果锚点前一行是空行，在空行前插入（保持表格和标题之间的空行）
insert_before_section() {
    local section_pattern="$1"
    local new_content="$2"
    local file="$ACTIVE_FILE"

    # 找到锚点行号（先精确匹配，再模糊匹配）
    local line_num
    line_num=$(grep -n "^${section_pattern}" "$file" | head -1 | cut -d: -f1) || true
    
    # 模糊匹配：如果精确匹配失败，提取核心关键词再搜索
    if [ -z "$line_num" ]; then
        local keyword
        keyword=$(echo "$section_pattern" | sed 's/^## //' | sed 's/^⚠️ //')
        if [ -n "$keyword" ]; then
            # 策略1：整体搜索
            line_num=$(grep -n "^## .*${keyword}" "$file" | head -1 | cut -d: -f1) || true
        fi
        # 策略2：取最后一个关键词（如"关键决策"→"决策"）
        if [ -z "$line_num" ] && [ -n "$keyword" ]; then
            # 提取最后2个字作为核心词
            local core_word
            core_word=$(echo "$keyword" | grep -oE '.{2}$') || true
            if [ -n "$core_word" ]; then
                line_num=$(grep -n "^## .*${core_word}" "$file" | head -1 | cut -d: -f1) || true
            fi
        fi
    fi
    
    [ -z "$line_num" ] && die "未找到锚点: ${section_pattern} (也未模糊匹配到)"

    # 检查前一行是否为空（line_num=1 时无前一行，直接在锚点前插入）
    local insert_at
    if [ "$line_num" -le 1 ]; then
        insert_at=1
    else
        local prev=$((line_num - 1))
        local prev_text
        prev_text=$(sed -n "${prev}p" "$file")
        if [ -z "$prev_text" ]; then
            insert_at=$prev  # 在空行位置插入（空行会被推后）
        else
            insert_at=$line_num  # 直接在锚点行前插入
        fi
    fi

    if $DRY_RUN; then
        preview "将在 $file L${insert_at} 前插入:"
        echo "$new_content"
        return
    fi

    # 使用 awk 插入（避免 sed 特殊字符问题）
    # 把 new_content 写入临时文件，awk 通过 getline 读取
    local tmpContent
    tmpContent=$(_mktemp)
    echo "$new_content" > "$tmpContent"

    awk -v at="$insert_at" -v cfile="$tmpContent" '
    NR == at {
        while ((getline line < cfile) > 0) print line
        close(cfile)
    }
    { print }
    ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
}

# 读取 active.md 中当前阶段号（返回数字，无法解析时返回0）
_get_current_phase() {
    local file="$ACTIVE_FILE"
    [ -f "$file" ] || { echo 0; return; }
    # 从 "## 当前阶段：Phase N ..." 中提取 N（兼容 Git Bash，不用 -P）
    local phase_line
    phase_line=$(grep -m1 '^## 当前阶段：' "$file" 2>/dev/null || true)
    local num
    num=$(echo "$phase_line" | sed -n 's/.*Phase[[:space:]]*\([0-9]\{1,\}\).*/\1/p' 2>/dev/null)
    echo "${num:-0}"
}

# 检查阶段>4时是否存在里程碑区块（缺失则报错 + 自动记录 Bug）
_check_milestone_health() {
    local file="$ACTIVE_FILE"
    [ -f "$file" ] || return 0

    local current_phase
    current_phase=$(_get_current_phase)
    [ "${current_phase:-0}" -le 4 ] && return 0

    # 阶段>4 但没有里程碑区块
    if ! grep -q "^## 开发里程碑" "$file"; then
        # 自动记录 Bug（只记录一次）
        local bug_row="| AUTO | 阶段>${current_phase}但 active.md 缺少开发里程碑区块 | Phase 4 完成时未执行 ux --init | 需执行 session-sync.sh ux --init 导入里程碑 | 🔄 |"
        if ! grep -q "缺少开发里程碑区块" "$file"; then
            if $DRY_RUN; then
                preview "将在 Bug 记录表中插入里程碑缺失 Bug"
            else
                local bug_header_line
                bug_header_line=$(grep -n "^## Bug 记录" "$file" | head -1 | cut -d: -f1)
                if [ -n "$bug_header_line" ]; then
                    # 动态查找 Bug 表第一个数据行位置（跳过标题行和分隔线）
                    local insert_at
                    insert_at=$(awk -v start="$bug_header_line" '
                        NR <= start { next }
                        /^\|[[:space:]]*#/ { next }      # 跳过 | # | ... 表头行
                        /^\|[-|[:space:]]*$/ { next }     # 跳过 |---|---| 分隔行
                        { print NR; exit }                # 第一个非表头行 = 插入点
                    ' "$file")
                    # 兜底：如果找不到数据行，在 Bug 表后下一个 ## 标题前插入
                    if [ -z "$insert_at" ]; then
                        insert_at=$(awk -v start="$((bug_header_line + 1))" '
                            NR > start && /^## / { print NR; exit }
                        ' "$file")
                    fi
                    if [ -n "$insert_at" ]; then
                        awk -v at="$insert_at" -v row="$bug_row" 'NR == at { print row } { print }' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
                    fi
                fi
            fi
        fi

        echo -e "${RED}❌ 流程违规: 当前已进入 Phase ${current_phase}，但 active.md 缺少「开发里程碑」区块！${NC}" >&2
        echo -e "${YELLOW}→ Phase 4 门控通过后必须执行: session-sync.sh ux --init${NC}" >&2
        echo -e "${YELLOW}→ 规范参考: harness/rules/GamePlay_Dev/plan-doc.md §九${NC}" >&2
        echo -e "${YELLOW}→ 已自动在 Bug 记录中登记此问题${NC}" >&2
        return 1
    fi
    return 0
}

# 替换 active.md 中的阶段行
replace_stage_line() {
    local new_text="$1"
    local file="$ACTIVE_FILE"

    if $DRY_RUN; then
        preview "替换阶段行为: ## 当前阶段：$new_text"
        return
    fi

    # 用 awk 替换（避免 sed 分隔符冲突）
    awk -v newstage="## 当前阶段：$new_text" '
    /^## 当前阶段：/ { print newstage; next }
    { print }
    ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
}

# 追加 session-log 条目
append_session_log() {
    local title="$1"
    local body="$2"
    local log_type="${3:-}"  # 可选：日志类型标签（如 Stage/Gate/Progress/Doc/ADR/Bug/Log/Lesson/UX）
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    # 构建标题行：有类型标签时显示为 ## [时间][类型] 标题
    local header_line
    if [ -n "$log_type" ]; then
        header_line="## [$timestamp][$log_type] $title"
    else
        header_line="## [$timestamp] $title"
    fi

    local entry
    entry=$(cat <<EOF

$header_line

$body
EOF
)

    if $DRY_RUN; then
        preview "将插入到 session-log.md 顶部:"
        echo "$entry"
        return
    fi

    # 插入到文件头部（第一个 --- 分隔线之后），新条目在上、旧条目在下
    local header_end
    header_end=$(grep -n "^---$" "$LOG_FILE" | head -1 | cut -d: -f1)
    if [ -n "$header_end" ]; then
        local tmp="${LOG_FILE}.tmp"
        head -n "$header_end" "$LOG_FILE" > "$tmp"
        echo "$entry" >> "$tmp"
        echo "" >> "$tmp"
        echo "---" >> "$tmp"
        echo "" >> "$tmp"
        # 跳过原文件 --- 后紧跟的空行（避免重复空行堆积）
        local next_line=$((header_end + 1))
        local next_content
        next_content=$(sed -n "${next_line}p" "$LOG_FILE")
        if [ -z "$next_content" ]; then
            next_line=$((next_line + 1))
        fi
        # 跳过旧的 --- 分隔线（如果下一行就是 ---）
        next_content=$(sed -n "${next_line}p" "$LOG_FILE")
        if [ "$next_content" = "---" ]; then
            next_line=$((next_line + 1))
            # 再跳过 --- 后的空行
            next_content=$(sed -n "${next_line}p" "$LOG_FILE")
            if [ -z "$next_content" ]; then
                next_line=$((next_line + 1))
            fi
        fi
        tail -n +"$next_line" "$LOG_FILE" >> "$tmp"
        mv "$tmp" "$LOG_FILE"
    else
        echo "$entry" >> "$LOG_FILE"
    fi
}

# ============================================================
# 子命令实现
# ============================================================

cmd_stage() {
    local TEXT="" PHASE="" REASONING="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --text) TEXT="$2"; shift 2 ;;
            --phase) PHASE="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$TEXT" ] && die "stage 需要 --text 参数"
    [ -z "$REASONING" ] && die "stage 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "stage 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "stage 需要 --conclusion 参数"
    check_three_part_min "stage" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths

    # --phase N 触发自动门控检查
    if [ -n "$PHASE" ]; then
        # 数值校验
        if ! echo "$PHASE" | grep -qE '^[0-9]+$'; then
            die "--phase 参数必须为正整数，收到: '$PHASE'"
        fi
        # 如果目标阶段>5，检查里程碑是否已导入
        if [ "$PHASE" -gt 5 ]; then
            _check_milestone_health || die "请先执行 session-sync.sh ux --init 再推进到 Phase $PHASE"
        fi
        _gate_check_for_phase "$PHASE"
    fi

    replace_stage_line "$TEXT"
    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "阶段更新" "$log_body" "Stage"
    info "阶段行已更新: $TEXT"
}

# 门控继承链：根据目标阶段自动决定需要哪个门控
# "进入阶段 N" 意味着 "离开阶段 N-1"，所以检查的是前一阶段的门控
# 进入 1~2  → 无门控（阶段1/2是起点和工作区）
# 进入 3    → 实际运行 gate-check p2（离开阶段2前必须通过p2门控）
# 进入 4    → 继承 p2
# 进入 5    → 实际运行 gate-check p4（离开阶段4前必须通过p4门控）
# 进入 6~7  → 继承 p4
# 进入 8    → 继承 p4（p8 门控在阶段8内部触发，不在进入时）
# 进入 9    → 实际运行 gate-check p8（离开阶段8前必须通过p8门控）
# 进入 10+  → 继承 p8
_gate_check_for_phase() {
    local target_phase="$1"

    # 确定需要哪个门控
    local required_gate=""
    local is_direct=false  # 是否需要实际运行 gate-check.sh

    if [ "$target_phase" -le 2 ] 2>/dev/null; then
        return 0  # 阶段1~2无门控
    elif [ "$target_phase" -eq 3 ]; then
        required_gate="p2"; is_direct=true
    elif [ "$target_phase" -eq 4 ]; then
        required_gate="p2"; is_direct=false
    elif [ "$target_phase" -eq 5 ]; then
        required_gate="p4"; is_direct=true
    elif [ "$target_phase" -ge 6 ] && [ "$target_phase" -le 8 ]; then
        required_gate="p4"; is_direct=false
    elif [ "$target_phase" -eq 9 ]; then
        required_gate="p8"; is_direct=true
    elif [ "$target_phase" -ge 10 ]; then
        required_gate="p8"; is_direct=false
    else
        die "无效的阶段号: $target_phase"
    fi

    local gate_check_script="$SCRIPT_DIR/Workflow/workflow-dev/gate-check.sh"
    local checklist="$PROJECT_ROOT/harness/session-state/$FEATURE/checklist.md"

    if $is_direct; then
        # 实际运行 gate-check.sh
        if [ ! -f "$gate_check_script" ]; then
            die "gate-check.sh 不存在: $gate_check_script"
        fi
        if [ ! -f "$checklist" ]; then
            die "checklist.md 不存在，请先运行: gate-check.sh init $FEATURE"
        fi

        info "门控检查: 阶段 $target_phase → 运行 gate-check $required_gate ..."
        if ! bash "$gate_check_script" "$required_gate" "$FEATURE"; then
            die "门控未通过 ($required_gate)，无法推进到阶段 $target_phase。请先完成待输入项后重试。"
        fi

        # 门控通过 → 自动记录 gate 到 active.md
        local gate_name="Phase${target_phase}-gate"
        local gate_time
        gate_time=$(date "+%Y-%m-%d")
        local row="| $gate_name | PASS | $gate_time |"
        insert_before_section "## 主进度" "$row"
        info "门控 $required_gate 通过 ✅ 已自动记录"
    else
        # 继承检查：在门控记录表区域内查找 PASS
        # 提取 "## 门控记录" 到下一个 "## " 之间的内容
        local gate_table
        gate_table=$(awk '/^## 门控记录/,/^## [^门]/' "$ACTIVE_FILE" 2>/dev/null)
        if ! echo "$gate_table" | grep -q "| .* | PASS |" 2>/dev/null; then
            die "active.md 门控记录表中无任何 PASS 记录，无法推进到阶段 $target_phase"
        fi

        # 查找对应门控的 PASS 记录
        local gate_pattern
        case "$required_gate" in
            p2)  gate_pattern="Phase2|p2|Round.*DL" ;;
            p4)  gate_pattern="Phase4|p4|Round.*文档" ;;
            p10|p8) gate_pattern="Phase8|Phase10|p8|p10|Round.*验收" ;;
        esac

        if ! echo "$gate_table" | grep -E "PASS" | grep -qiE "$gate_pattern"; then
            # 宽松兜底：只要门控表内有任何 PASS 记录
            local has_any_pass
            has_any_pass=$(echo "$gate_table" | grep -c "| .* | PASS |" 2>/dev/null || echo "0")
            has_any_pass=$(echo "$has_any_pass" | tr -d '\r\n')
            if [ "${has_any_pass:-0}" -eq 0 ]; then
                die "需要 $required_gate 门控 PASS 记录才能推进到阶段 $target_phase"
            fi
            # 有 PASS 记录但名称不精确匹配 → 放行并警告
            warn "未精确匹配到 $required_gate 门控记录，但存在其他 PASS 记录，放行"
        fi
        info "继承门控: $required_gate 已通过 → 允许推进到阶段 $target_phase"
    fi
}

cmd_gate() {
    local NAME="" RESULT="" TIME="" REASONING="" BACKGROUND="" CONCLUSION="" _INTERNAL_CALLER=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --result) RESULT="$2"; shift 2 ;;
            --time) TIME="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            --_internal) _INTERNAL_CALLER="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$NAME" ] && die "gate 需要 --name 参数"
    [ -z "$RESULT" ] && die "gate 需要 --result 参数"
    [ -z "$REASONING" ] && die "gate 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "gate 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "gate 需要 --conclusion 参数"
    check_three_part_min "gate" "$BACKGROUND" "$REASONING" "$CONCLUSION"
    [ -z "$TIME" ] && TIME=$(date "+%Y-%m-%d")

    # ── 安全拦截：禁止外部直接写入 PASS 记录 ──
    # PASS 记录只能由 _gate_check_for_phase 内部写入（通过 --_internal 标记）
    # AI 或人工调用 session-sync.sh gate --result "PASS" 将被拦截
    if echo "$RESULT" | grep -qi "PASS" && [ "$_INTERNAL_CALLER" != "gate_check_auto" ]; then
        die "❌ 安全拦截: 禁止手动写入 PASS 门控记录。PASS 只能由 gate-check.sh 自动验证后写入。请运行: session-sync.sh stage --phase <N> 触发自动门控检查"
    fi

    resolve_paths
    local row="| $NAME | $RESULT | $TIME |"
    insert_before_section "## 主进度" "$row"
    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "门控: $NAME" "$log_body" "Gate"
    info "门控记录已追加: $NAME"
}

cmd_progress() {
    local NUM="" AGENT="" CONTENT="" STATUS="✅" REASONING="" PHASE_HINT="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --num) NUM="$2"; shift 2 ;;
            --agent) AGENT="$2"; shift 2 ;;
            --content) CONTENT="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --phase) PHASE_HINT="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$NUM" ] && die "progress 需要 --num 参数"
    [ -z "$AGENT" ] && die "progress 需要 --agent 参数"
    [ -z "$CONTENT" ] && die "progress 需要 --content 参数"
    [ -z "$REASONING" ] && die "progress 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "progress 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "progress 需要 --conclusion 参数"
    check_three_part_min "progress" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths

    # 里程碑健康检查：阶段>4 但没有里程碑区块时报错
    _check_milestone_health || die "请先执行 session-sync.sh ux --init 再继续"

    # 阶段一致性校验：如果提供了 --phase，检查是否超前于当前阶段
    if [ -n "$PHASE_HINT" ]; then
        if ! echo "$PHASE_HINT" | grep -qE '^[0-9]+$'; then
            die "--phase 参数必须为正整数，收到: '$PHASE_HINT'"
        fi
        local current_phase
        current_phase=$(_get_current_phase)
        if [ "$current_phase" -gt 0 ] && [ "$PHASE_HINT" -gt "$current_phase" ]; then
            die "❌ 阶段校验失败: 当前阶段 Phase $current_phase，不允许记录 Phase $PHASE_HINT 的进度。请先执行 session-sync.sh stage --phase $PHASE_HINT 推进阶段。"
        fi
    fi

    local row="| $NUM [$AGENT] | $CONTENT | $STATUS |"
    insert_before_section "## 文档产出清单" "$row"
    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "进度: $CONTENT" "$log_body" "Progress"
    info "进度条目已追加: $NUM $CONTENT"
}

cmd_doc() {
    local NAME="" DOC_PATH="" STATUS="✅" REASONING="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --name) NAME="$2"; shift 2 ;;
            --path) DOC_PATH="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$NAME" ] && die "doc 需要 --name 参数"
    [ -z "$DOC_PATH" ] && die "doc 需要 --path 参数"
    [ -z "$REASONING" ] && die "doc 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "doc 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "doc 需要 --conclusion 参数"
    check_three_part_min "doc" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths
    local row="| $NAME | \`$DOC_PATH\` | $STATUS |"
    insert_before_section "## 关键决策" "$row"
    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "文档: $NAME" "$log_body" "Doc"
    info "文档条目已追加: $NAME"
}

cmd_adr() {
    local ID="" POINT="" DECISION="" REASONING="" TIME="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id) ID="$2"; shift 2 ;;
            --point) POINT="$2"; shift 2 ;;
            --decision) DECISION="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --time) TIME="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$ID" ] && die "adr 需要 --id 参数"
    [ -z "$POINT" ] && die "adr 需要 --point 参数"
    [ -z "$DECISION" ] && die "adr 需要 --decision 参数"
    [ -z "$REASONING" ] && die "adr 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "adr 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "adr 需要 --conclusion 参数"
    check_three_part_min "adr" "$BACKGROUND" "$REASONING" "$CONCLUSION"
    [ -z "$TIME" ] && TIME=$(date "+%Y-%m-%d")

    resolve_paths
    local row="| $ID | $POINT | $DECISION | $TIME |"
    insert_before_section "## Bug 记录" "$row"
    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "ADR#$ID: $POINT" "$log_body" "ADR"
    info "ADR 决策已追加: #$ID $POINT"
}

cmd_bug() {
    local ID="" SYMPTOM="" CAUSE="" FIX="" STATUS="✅" REASONING="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id) ID="$2"; shift 2 ;;
            --symptom) SYMPTOM="$2"; shift 2 ;;
            --cause) CAUSE="$2"; shift 2 ;;
            --fix) FIX="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --reasoning|--reason) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$ID" ] && die "bug 需要 --id 参数"
    [ -z "$SYMPTOM" ] && die "bug 需要 --symptom 参数"
    [ -z "$CAUSE" ] && die "bug 需要 --cause 参数"
    [ -z "$FIX" ] && die "bug 需要 --fix 参数"

    # 三段式 session-log 字段：若未提供则降级到 symptom/cause/fix
    [ -z "$BACKGROUND" ] && BACKGROUND="$SYMPTOM"
    [ -z "$REASONING" ] && REASONING="$CAUSE"
    [ -z "$CONCLUSION" ] && CONCLUSION="$FIX"

    # 校验三段式最低字数
    check_three_part_min "bug" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths

    # 找 Bug 表的结束锚点（Bug 表后面的第一个 ## 标题）
    # 先找 "## Bug 记录" 行号，然后找它之后的下一个 "## " 行
    local bug_header_line
    bug_header_line=$(grep -n "^## Bug 记录" "$ACTIVE_FILE" | head -1 | cut -d: -f1)
    [ -z "$bug_header_line" ] && die "未找到 ## Bug 记录 标题"

    local next_section_line
    next_section_line=$(awk -v start="$((bug_header_line + 1))" '
        NR > start && /^## / { print NR; exit }
    ' "$ACTIVE_FILE")
    [ -z "$next_section_line" ] && die "未找到 Bug 记录之后的章节"

    local row="| $ID | $SYMPTOM | $CAUSE | $FIX | $STATUS |"

    if $DRY_RUN; then
        preview "将在 active.md L${next_section_line} 前插入 Bug 行:"
        echo "$row"
    else
        # 在下一个 ## 之前插入（同 insert_before_section 逻辑）
        local prev=$((next_section_line - 1))
        local prev_text
        prev_text=$(sed -n "${prev}p" "$ACTIVE_FILE")
        local insert_at
        if [ -z "$prev_text" ]; then
            insert_at=$prev
        else
            insert_at=$next_section_line
        fi

        local tmpContent
        tmpContent=$(_mktemp)
        echo "$row" > "$tmpContent"

        awk -v at="$insert_at" -v cfile="$tmpContent" '
        NR == at {
            while ((getline line < cfile) > 0) print line
            close(cfile)
        }
        { print }
        ' "$ACTIVE_FILE" > "${ACTIVE_FILE}.tmp" && mv "${ACTIVE_FILE}.tmp" "$ACTIVE_FILE"

        info "Bug#$ID 已追加到 active.md"
    fi

    # 写 session-log（使用三段式字段）
    local log_body
    log_body="**背景**：$BACKGROUND"$'\n\n'"**推理**：$REASONING"$'\n\n'"**结论**：$CONCLUSION"
    append_session_log "Bug#$ID 修复" "$log_body" "Bug"
    info "Bug#$ID 已追加到 active.md + session-log.md"
}

cmd_log() {
    local TITLE="" BACKGROUND="" REASONING="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --title) TITLE="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$TITLE" ] && die "log 需要 --title 参数"
    [ -z "$BACKGROUND" ] && die "log 需要 --background 参数"
    [ -z "$REASONING" ] && die "log 需要 --reasoning 参数"
    [ -z "$CONCLUSION" ] && die "log 需要 --conclusion 参数"
    check_three_part_min "log" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths

    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"

    append_session_log "$TITLE" "$log_body" "Log"
    info "session-log 条目已追加: $TITLE"
}

cmd_lesson() {
    local ID="" TEXT="" REASONING="" BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id) ID="$2"; shift 2 ;;
            --text) TEXT="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [ -z "$ID" ] && die "lesson 需要 --id 参数"
    [ -z "$TEXT" ] && die "lesson 需要 --text 参数"
    [ -z "$REASONING" ] && die "lesson 需要 --reasoning 参数"
    [ -z "$BACKGROUND" ] && die "lesson 需要 --background 参数"
    [ -z "$CONCLUSION" ] && die "lesson 需要 --conclusion 参数"
    check_three_part_min "lesson" "$BACKGROUND" "$REASONING" "$CONCLUSION"

    resolve_paths
    local row="${ID}. **$TEXT**"
    insert_before_section "## ⚠️ 遗留待确认" "$row"

    # 清除（暂无）占位符
    if ! $DRY_RUN && grep -q "^（暂无）$" "$ACTIVE_FILE"; then
        awk '!/^（暂无）$/' "$ACTIVE_FILE" > "${ACTIVE_FILE}.tmp" && mv "${ACTIVE_FILE}.tmp" "$ACTIVE_FILE"
    fi

    local log_body=""
    log_body+="**背景**：$BACKGROUND"$'\n\n'
    log_body+="**推理**：$REASONING"$'\n\n'
    log_body+="**结论**：$CONCLUSION"
    append_session_log "规范沉淀#$ID" "$log_body" "Lesson"
    info "规范沉淀已追加: #$ID"
}

# ─── ux: 开发里程碑管理 ───
cmd_ux() {
    local ID="" STATUS="" REASONING="" INIT=false BACKGROUND="" CONCLUSION=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id) ID="$2"; shift 2 ;;
            --status) STATUS="$2"; shift 2 ;;
            --reasoning) REASONING="$2"; shift 2 ;;
            --background) BACKGROUND="$2"; shift 2 ;;
            --conclusion) CONCLUSION="$2"; shift 2 ;;
            --init) INIT=true; shift ;;
            *) shift ;;
        esac
    done

    resolve_paths

    if $INIT; then
        # 检查是否已存在里程碑区块
        if grep -q "^## 开发里程碑" "$ACTIVE_FILE"; then
            die "开发里程碑区块已存在，无需重复初始化"
        fi

        # 查找开发计划文件
        local dev_plan_dir="$PROJECT_ROOT/docs/GamePlay_Dev/$FEATURE"
        local plan_file
        plan_file=$(find "$dev_plan_dir" -name "*开发计划*" -type f 2>/dev/null | head -1) || true
        # 若未找到，扩大搜索范围到 GamePlay_Dev/ 下所有子目录
        if [ -z "$plan_file" ]; then
            plan_file=$(find "$PROJECT_ROOT/docs/GamePlay_Dev" -name "*开发计划*" -type f 2>/dev/null \
                | { grep -F "$FEATURE" || true; } | head -1) || true
        fi
        if [ -z "$plan_file" ]; then
            die "未找到开发计划文件（在 $dev_plan_dir 下搜索 *开发计划*）。
→ 请先让 [DL] 创建「{功能名}开发计划.md」，格式见 harness/rules/GamePlay_Dev/plan-doc.md §三 M-02"
        fi

        # ── 格式校验 ──
        local phase_count ux_count table_header_count
        phase_count=$(grep -c "^### Phase [0-9]" "$plan_file" 2>/dev/null || echo 0)
        phase_count=$(echo "$phase_count" | tr -d '\r\n')
        ux_count=$(grep -c "^| UX-" "$plan_file" 2>/dev/null || echo 0)
        ux_count=$(echo "$ux_count" | tr -d '\r\n')
        table_header_count=$(grep -c "^| 体验节点" "$plan_file" 2>/dev/null || echo 0)
        table_header_count=$(echo "$table_header_count" | tr -d '\r\n')

        local errors=()
        if [ "${phase_count:-0}" -eq 0 ]; then
            errors+=("❌ 未找到 Phase 标题（需要 '### Phase N — {名称}' 格式）")
        fi
        if [ "${table_header_count:-0}" -eq 0 ]; then
            errors+=("❌ 未找到体验节点表头（需要 '| 体验节点 | 验收目标 | 负责 Agent |' 格式）")
        fi
        if [ "${ux_count:-0}" -eq 0 ]; then
            errors+=("❌ 未找到 UX 体验节点行（需要 '| UX-N {简述} | {目标} | [{Agent}] |' 格式）")
        fi
        if [ "${table_header_count:-0}" -gt 0 ] && [ "${phase_count:-0}" -ne "${table_header_count:-0}" ]; then
            errors+=("⚠️ Phase 标题数(${phase_count})与表头数(${table_header_count})不匹配，每个 Phase 下必须有一个完整表格")
        fi

        if [ ${#errors[@]} -gt 0 ]; then
            echo -e "${RED}❌ 开发计划 M-02 格式不符合规范（$(basename "$plan_file")）：${NC}" >&2
            for err in "${errors[@]}"; do
                echo -e "${YELLOW}  $err${NC}" >&2
            done
            echo -e "${YELLOW}→ 请让 [DL] 按 harness/rules/GamePlay_Dev/plan-doc.md §三 M-02 格式重写后重试${NC}" >&2
            echo -e "${YELLOW}→ 需要: Phase 标题(### Phase N) + 表格(| 体验节点 | 验收目标 | 负责 Agent |) + UX 行(| UX-N ... |)${NC}" >&2
            exit 1
        fi

        echo -e "${GREEN}  ↳ 格式校验通过: ${phase_count} Phase, ${ux_count} UX 项${NC}"

        # 从开发计划中提取 Phase 表格，添加状态列
        local tmpMilestone
        tmpMilestone=$(_mktemp)
        {
            echo "## 开发里程碑"
            echo ""
            awk '
            /^### Phase [0-9]/ { print; next }
            /^\| 体验节点/ { print $0 " 状态 |"; in_table=1; next }
            /^\|---/ && in_table { print $0 "------|"; next }
            /^\| UX-/ && in_table { print $0 " 📋 |"; next }
            /^$/ && in_table { in_table=0; print ""; next }
            /^\*\*→/ && in_table { in_table=0 }
            /^##/ && in_table { in_table=0 }
            ' "$plan_file"
            echo ""
        } > "$tmpMilestone"

        local section_content
        section_content=$(cat "$tmpMilestone")

        # 后置校验：确认提取结果非空
        local extracted_ux
        extracted_ux=$(echo "$section_content" | grep -c "| UX-" 2>/dev/null || echo 0)
        extracted_ux=$(echo "$extracted_ux" | tr -d '\r\n')
        if [ "${extracted_ux:-0}" -eq 0 ]; then
            die "提取失败：虽然格式校验通过，但 awk 未提取到任何 UX 行。
→ 可能是开发计划的表格格式与预期不符（行首有空格、制表符等）。
→ 请检查 $(basename "$plan_file") 确保 UX 行以 '| UX-' 开头（无前导空格）。
→ 格式参考: harness/rules/GamePlay_Dev/plan-doc.md §三 M-02"
        fi

        if $DRY_RUN; then
            preview "将在 ## 文档产出清单 前插入开发里程碑区块:"
            echo "$section_content"
            return
        fi

        insert_before_section "## 文档产出清单" "$section_content"
        info "开发里程碑区块已创建（从 $(basename "$plan_file") 导入）"
        return
    fi

    # ── 更新模式 ──
    [ -z "$ID" ] && die "ux 需要 --id 参数 (如 UX-5) 或 --init 标志"
    [ -z "$STATUS" ] && die "ux 需要 --status 参数 (📋/🔄/✅/❌)"

    if ! grep -q "| ${ID} " "$ACTIVE_FILE"; then
        die "未找到里程碑项: $ID (请确认开发里程碑区块已初始化: session-sync.sh ux --init)"
    fi

    if $DRY_RUN; then
        preview "将更新 $ID 状态为: $STATUS"
        return
    fi

    # 替换 UX-ID 行的最后一个单元格（状态列）
    # 利用贪婪匹配：\(.*|\) 匹配到倒数第二个 |，然后替换最后一个 cell
    # 使用跨平台兼容的 sed -i 语法（GNU sed 不需要 "" 参数）
    if sed --version >/dev/null 2>&1; then
        sed -i "/| ${ID} /s/\\(.*|\\)[^|]*|[[:space:]]*$/\\1 ${STATUS} |/" "$ACTIVE_FILE"
    else
        sed -i "" "/| ${ID} /s/\\(.*|\\)[^|]*|[[:space:]]*$/\\1 ${STATUS} |/" "$ACTIVE_FILE"
    fi

    if [ -n "$REASONING" ]; then
        [ -z "$BACKGROUND" ] && die "ux 需要 --background 参数（当提供 --reasoning 时）"
        [ -z "$CONCLUSION" ] && die "ux 需要 --conclusion 参数（当提供 --reasoning 时）"
        local log_body=""
        log_body+="**背景**：$BACKGROUND"$'\n\n'
        log_body+="**推理**：$REASONING"$'\n\n'
        log_body+="**结论**：$CONCLUSION"
        append_session_log "里程碑 $ID → $STATUS" "$log_body" "UX"
    fi

    info "里程碑已更新: $ID → $STATUS"
}

cmd_init() {
    local TEMPLATE="dev"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --template) TEMPLATE="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    [ -z "$FEATURE" ] && die "init 需要 --feature 参数"
    if [ -z "$PROJECT_ROOT" ]; then
        PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    fi

    local session_dir="$PROJECT_ROOT/harness/session-state/$FEATURE"

    # 检查是否已存在
    if [ -f "$session_dir/active.md" ]; then
        die "active.md 已存在: $session_dir/active.md（如需重建请先手动删除）"
    fi

    if $DRY_RUN; then
        preview "将创建目录: $session_dir"
        preview "将创建文件: active.md + session-log.md (模板: $TEMPLATE)"
        echo ""
        echo "=== active.md 预览 ==="
        _generate_active_template "$TEMPLATE"
        echo ""
        echo "=== session-log.md 预览 ==="
        _generate_log_template
        return
    fi

    # 创建目录
    mkdir -p "$session_dir"

    # 生成 active.md
    _generate_active_template "$TEMPLATE" > "$session_dir/active.md"
    info "active.md 已创建: $session_dir/active.md (模板: $TEMPLATE)"

    # 生成 session-log.md
    _generate_log_template > "$session_dir/session-log.md"
    info "session-log.md 已创建: $session_dir/session-log.md"

    echo ""
    echo -e "${GREEN}✅ 初始化完成: harness/session-state/$FEATURE/${NC}"
    echo "  → active.md (模板: $TEMPLATE)"
    echo "  → session-log.md"
}

# ─── 模板生成函数 ───

_generate_active_template() {
    local tmpl="$1"
    case "$tmpl" in
        dev)     _template_dev ;;
        discussion) _template_discussion ;;
        *)       die "未知模板: $tmpl（支持: dev, discussion）" ;;
    esac
}

_template_dev() {
    cat <<'TEMPLATE'
> ⚠️ 该文件由 session-sync.sh 自动维护，禁止 AI 手动编辑。所有写入必须通过 harness/tools/session-sync.sh 执行。

# 当前会话状态

## 项目：{项目名}
## 工作流类型：业务开发
## 当前阶段：初始化

## 门控记录
| 门控 | 结果 | 时间 |
|------|------|------|

## 主进度：体验节点验收清单

### 【体验节点 1】{功能名}
| 步骤 | 内容 | 状态 |
|------|------|------|
| ① [项目负责人] | 初始化 active.md + session-log.md | ✅ |

## 文档产出清单
| 文档 | 路径 | 状态 |
|------|------|------|

## 关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|

## Bug 记录
| # | 现象 | 根因 | 修复 | 状态 |
|---|------|------|------|------|

## 规范沉淀
（暂无）

## ⚠️ 遗留待确认
- 功能命名待确定
TEMPLATE
}

_template_discussion() {
    cat <<'TEMPLATE'
> ⚠️ 该文件由 session-sync.sh 自动维护，禁止 AI 手动编辑。所有写入必须通过 harness/tools/session-sync.sh 执行。

# 当前会话状态

## 项目：{话题名}
## 工作流类型：轻量讨论
## 当前阶段：讨论中

## 关键决策（ADR）
| # | 决策点 | 选定方案 | 时间 |
|---|-------|---------|------|

## ⚠️ 遗留待确认
（暂无）
TEMPLATE
}

_generate_log_template() {
    cat <<TEMPLATE
> ⚠️ 该文件由 session-sync.sh 自动维护，禁止 AI 手动编辑。所有写入必须通过 harness/tools/session-sync.sh 执行。

# Session Log — $FEATURE

> 推理日志：记录关键决策的思考过程，不是进度记录（进度记录在 active.md）

---
TEMPLATE
}

# ============================================================
# 主入口
# ============================================================

[ $# -lt 1 ] && show_help

COMMAND="$1"
shift

# 先提取公共参数
REMAINING_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --feature) FEATURE="$2"; shift 2 ;;
        --project-root) PROJECT_ROOT="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        --help|-h) show_help ;;
        *) REMAINING_ARGS+=("$1"); shift ;;
    esac
done

# 分发子命令（使用 :+ 防止空数组在旧 bash set -u 下报错）
case "$COMMAND" in
    stage)    cmd_stage ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    gate)     cmd_gate ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    progress) cmd_progress ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    doc)      cmd_doc ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    adr)      cmd_adr ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    bug)      cmd_bug ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    log)      cmd_log ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    lesson)   cmd_lesson ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    ux)       cmd_ux ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    init)     cmd_init ${REMAINING_ARGS[@]:+"${REMAINING_ARGS[@]}"} ;;
    help)     show_help ;;
    *)        die "未知子命令: $COMMAND（支持: init/stage/gate/progress/doc/adr/bug/log/lesson/ux）" ;;
esac
