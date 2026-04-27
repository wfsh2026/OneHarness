#!/usr/bin/env bash
# Harness 流程门控验证入口脚本
# 用法: ./gate-check.sh init <功能名>         → 从 workflow-dev.md 生成 checklist.md
#       ./gate-check.sh <p2|p4|p8> <功能名>   → 检查对应阶段的待输入项
# 示例: ./gate-check.sh init 赛博炮台
#       ./gate-check.sh p4 赛博炮台

set -uo pipefail

PHASE="${1:-}"
FEATURE_NAME="${2:-}"

if [[ -z "$PHASE" || -z "$FEATURE_NAME" ]]; then
  echo "用法: ./gate-check.sh <init|p2|p4|p8> <功能名>"
  exit 1
fi

case "$PHASE" in
  init|p2|p4|p8) ;;
  *) echo "❌ 不支持的 phase: $PHASE（可选值: init p2 p4 p8）"; exit 1 ;;
esac

# 脚本在 harness/tools/Workflow/workflow-dev/，往上4层到仓库根
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
for i in $(seq 4); do REPO_ROOT="$(dirname "$REPO_ROOT")"; done

WF_DOC="$REPO_ROOT/harness/rules/Workflow/workflow-dev.md"
CHECKLIST_DIR="$REPO_ROOT/harness/session-state/$FEATURE_NAME"
CHECKLIST_PATH="$CHECKLIST_DIR/checklist.md"

CYAN='\033[36m'; GREEN='\033[32m'; RED='\033[31m'; YELLOW='\033[33m'; RESET='\033[0m'

# ═══════════════════════════════════════════════════════════════
# init：拷贝 workflow-dev.md 整表 → 生成 checklist.md（6列）
#   Agent 行 → 完成情况=⏳ 待输入
#   用户行   → 完成情况=ignore
# ═══════════════════════════════════════════════════════════════
if [[ "$PHASE" == "init" ]]; then
  echo -e "${CYAN}== 初始化 checklist.md：$FEATURE_NAME ==${RESET}"

  if [[ ! -f "$WF_DOC" ]]; then
    echo -e "${RED}❌ workflow-dev.md 不存在: $WF_DOC${RESET}"
    exit 1
  fi

  mkdir -p "$CHECKLIST_DIR"

  {
    echo "# $FEATURE_NAME workflow-dev Agent 流程验收清单"
    echo ""
    echo "> 状态说明：⏳ 待输入 = Agent 尚未完成此项；ignore = 用户侧行为；完成 = 已完成"
    echo "> Agent 完成某项工作后，将对应行的「完成情况」改为「完成」，「完成 Agent」填写对应角色"
    echo ""
    echo "| 阶段 | 用户行动 | Agent 行动 | 完成情况 | 完成 Agent | sh 验收 |"
    echo "|-----|---------|-----------|---------|-----------|--------|"

    in_table=0
    while IFS= read -r line; do
      # 检测表头行，开始提取
      if echo "$line" | grep -qE '^\| 阶段 \|'; then
        in_table=1
        continue
      fi
      # 跳过分隔行
      if echo "$line" | grep -qE '^\|[-|[:space:]]+\|'; then
        continue
      fi
      # 遇到下一个二级标题则结束
      if [[ "$in_table" -eq 1 ]] && echo "$line" | grep -qE '^##'; then
        break
      fi
      # 处理内容行
      if [[ "$in_table" -eq 1 ]] && echo "$line" | grep -qE '^\|'; then
        IFS=$'\t' read -r col_phase col_user col_agent <<< "$(echo "$line" | awk -F'|' '{
          gsub(/^[ \t]+|[ \t]+$/, "", $2)
          gsub(/^[ \t]+|[ \t]+$/, "", $3)
          gsub(/^[ \t]+|[ \t]+$/, "", $4)
          print $2 "\t" $3 "\t" $4
        }')"

        # Agent 行优先；否则用户行；否则空行
        if [[ -n "$col_agent" && "$col_agent" != "—" ]]; then
          done_status="⏳ 待输入"
          done_agent="⏳ 待输入"
          sh_result="⏳"
        elif [[ -n "$col_user" && "$col_user" != "—" ]]; then
          done_status="ignore"
          done_agent="—"
          sh_result="—"
        else
          done_status="—"
          done_agent="—"
          sh_result="—"
        fi

        echo "| $col_phase | $col_user | $col_agent | $done_status | $done_agent | $sh_result |"
      fi
    done < "$WF_DOC"
  } > "$CHECKLIST_PATH"

  echo -e "${GREEN}✅ checklist.md 已生成: harness/session-state/$FEATURE_NAME/checklist.md${RESET}"
  exit 0
fi

# ═══════════════════════════════════════════════════════════════
# p2/p4/p8：扫描 checklist.md 对应阶段的「⏳ 待输入」项
#   有则输出错误列表并 exit 1，无则 exit 0
# ═══════════════════════════════════════════════════════════════
declare -A PHASE_MARKERS
PHASE_MARKERS[p2]="**2."
PHASE_MARKERS[p4]="**4."
PHASE_MARKERS[p8]="**8."

declare -A PHASE_LABELS
PHASE_LABELS[p2]="阶段2：需求深度分析"
PHASE_LABELS[p4]="阶段4：文档化与开发计划制定"
PHASE_LABELS[p8]="阶段8：功能自检与验收"

PHASE_LABEL="${PHASE_LABELS[$PHASE]:-$PHASE}"
PHASE_MARKER="${PHASE_MARKERS[$PHASE]:-}"

echo ""
echo -e "${CYAN}=====================================================${RESET}"
echo -e "${CYAN}  Harness 流程门控 [$PHASE] 功能：$FEATURE_NAME${RESET}"
echo -e "${CYAN}=====================================================${RESET}"
echo ""

if [[ ! -f "$CHECKLIST_PATH" ]]; then
  echo -e "${RED}❌ checklist.md 不存在，请先运行:${RESET}"
  echo -e "${YELLOW}   ./gate-check.sh init $FEATURE_NAME${RESET}"
  exit 1
fi

# 合法的 Agent 签名列表（简写或全名均可）
VALID_AGENTS="PL|DL|GD|GPO|Ability|Scene|项目负责人|Dev_Lead|GamePlay_Designer|GPO_Programmer|Ability_Programmer|Scene_Builder"

# 读取 checklist.md，逐行验证三列：完成情况 / 完成 Agent / sh 验收
# 6列格式: | 阶段 | 用户行动 | Agent 行动 | 完成情况 | 完成 Agent | sh 验收 |
PENDING_ITEMS=()
AGENT_ERRORS=()
SH_ERRORS=()
in_phase=0

while IFS= read -r line; do
  echo "$line" | grep -qE '^\|' || continue
  echo "$line" | grep -qE '^\|[-|[:space:]]+\|' && continue
  echo "$line" | grep -qE '^\| 阶段 \|' && continue

  IFS=$'\t' read -r col_phase col_agent_action col_done col_done_agent col_sh <<< "$(echo "$line" | awk -F'|' '{
    gsub(/^[ \t]+|[ \t]+$/, "", $2)
    gsub(/^[ \t]+|[ \t]+$/, "", $4)
    gsub(/^[ \t]+|[ \t]+$/, "", $5)
    gsub(/^[ \t]+|[ \t]+$/, "", $6)
    gsub(/^[ \t]+|[ \t]+$/, "", $7)
    print $2 "\t" $4 "\t" $5 "\t" $6 "\t" $7
  }')"

  # 阶段范围追踪
  if echo "$col_phase" | grep -qF "$PHASE_MARKER"; then
    in_phase=1
  elif echo "$col_phase" | grep -qE '^\*\*[0-9]'; then
    in_phase=0
  fi

  # 跳过 ignore 行（用户侧行为）和非当前阶段行
  [[ "$in_phase" -ne 1 ]] && continue
  [[ "$col_done" == "ignore" || "$col_done" == "—" ]] && continue

  # 检查1: 完成情况列 — 不能是 ⏳ 待输入
  if [[ "$col_done" == "⏳ 待输入" ]]; then
    PENDING_ITEMS+=("$col_agent_action")
    continue
  fi

  # 检查2: 完成 Agent 列 — 必须是合法 Agent 签名，不能是 "完成" 或空
  if [[ -n "$col_done_agent" && "$col_done_agent" != "—" ]]; then
    if ! echo "$col_done_agent" | grep -qE "^($VALID_AGENTS)$"; then
      AGENT_ERRORS+=("「$col_agent_action」→ 完成Agent列为「$col_done_agent」，应为 Agent 署名(PL/DL/GD/GPO/Ability/Scene)")
    fi
  fi

  # 检查3: sh 验收列 — 不能是 ⏳，必须有已验收标记
  if [[ "$col_sh" == "⏳" || "$col_sh" == "⏳ 待输入" ]]; then
    SH_ERRORS+=("「$col_agent_action」→ sh验收列未签署")
  fi
done < "$CHECKLIST_PATH"

# 汇总输出
total_errors=$(( ${#PENDING_ITEMS[@]} + ${#AGENT_ERRORS[@]} + ${#SH_ERRORS[@]} ))

if [[ "$total_errors" -eq 0 ]]; then
  # ── p4 额外检查：active.md 体验节点完整性 ──
  if [[ "$PHASE" == "p4" ]]; then
    ACTIVE_PATH="$CHECKLIST_DIR/active.md"
    # 在 docs/GamePlay_Dev/<功能名>/ 下搜索 *开发计划.md
    DEV_PLAN_DIR="$REPO_ROOT/docs/GamePlay_Dev/$FEATURE_NAME"
    DEV_PLAN_FILE=""
    if [[ -d "$DEV_PLAN_DIR" ]]; then
      DEV_PLAN_FILE=$(find "$DEV_PLAN_DIR" -maxdepth 1 -name "*开发计划*" -type f 2>/dev/null | head -1)
    fi

    if [[ -n "$DEV_PLAN_FILE" && -f "$ACTIVE_PATH" ]]; then
      # 开发计划中的体验节点数 (匹配 【用户体验节点 N】)
      PLAN_COUNT=$(grep -cE '【用户体验节点' "$DEV_PLAN_FILE" 2>/dev/null || echo 0)
      # active.md 中的体验节点数 (匹配 【体验节点 N】)
      ACTIVE_COUNT=$(grep -cE '【体验节点' "$ACTIVE_PATH" 2>/dev/null || echo 0)

      if [[ "$PLAN_COUNT" -gt 0 && "$ACTIVE_COUNT" -lt "$PLAN_COUNT" ]]; then
        echo -e "${RED}❌ active.md 体验节点不完整：开发计划定义了 $PLAN_COUNT 个体验节点，但 active.md 只有 $ACTIVE_COUNT 个${RESET}"
        echo -e "${YELLOW}→ 请在 active.md 中补全所有 【体验节点 1】~【体验节点 $PLAN_COUNT】${RESET}"
        echo -e "${YELLOW}→ 参考: $(basename "$DEV_PLAN_FILE") 的 M-02 章节${RESET}"
        exit 1
      elif [[ "$PLAN_COUNT" -gt 0 ]]; then
        echo -e "${GREEN}  ↳ active.md 体验节点: $ACTIVE_COUNT/$PLAN_COUNT ✅${RESET}"
      fi
    elif [[ -z "$DEV_PLAN_FILE" ]]; then
      echo -e "${YELLOW}⚠️ 未找到开发计划文件，跳过体验节点检查${RESET}"
    elif [[ ! -f "$ACTIVE_PATH" ]]; then
      echo -e "${RED}❌ active.md 不存在: $ACTIVE_PATH${RESET}"
      exit 1
    fi

    # ── p4 额外检查：技术文档代码块数量限制（禁止完整C#实现） ──
    TECH_DOC_DIR="$DEV_PLAN_DIR/技术文档"
    MAX_CODE_BLOCKS=5
    if [[ -d "$TECH_DOC_DIR" ]]; then
      CODE_BLOCK_OVERFLOW=()
      for doc in "$TECH_DOC_DIR"/*.md; do
        [[ -f "$doc" ]] || continue
        [[ "$(basename "$doc")" == "README.md" ]] && continue
        block_count=$(grep -cE '```(csharp|cs)' "$doc" 2>/dev/null | tr -d '\r\n')
        block_count=${block_count:-0}
        if [[ "$block_count" -gt "$MAX_CODE_BLOCKS" ]]; then
          CODE_BLOCK_OVERFLOW+=("$(basename "$doc"): ${block_count}个代码块 (上限${MAX_CODE_BLOCKS})")
        fi
      done
      if [[ ${#CODE_BLOCK_OVERFLOW[@]} -gt 0 ]]; then
        echo -e "${RED}❌ 技术文档代码块过多（禁止包含完整C#实现，每文档上限${MAX_CODE_BLOCKS}个 csharp 块）：${RESET}"
        for overflow_err in "${CODE_BLOCK_OVERFLOW[@]}"; do
          echo -e "${YELLOW}  → $overflow_err${RESET}"
        done
        echo -e "${YELLOW}→ 请精简文档：S-04.5 仅需 System/Component 名称+职责表，完整代码由阶段6 codegen 生成${RESET}"
        exit 1
      else
        echo -e "${GREEN}  ↳ 技术文档代码块检查: 全部 ≤${MAX_CODE_BLOCKS} ✅${RESET}"
      fi
    fi
  fi

  echo -e "${GREEN}✅ $PHASE_LABEL 门控通过，所有 Agent 行均已完成且验收签署齐全${RESET}"
  exit 0
fi

echo -e "${RED}❌ $PHASE_LABEL 门控未通过（共 $total_errors 项问题）：${RESET}"
echo ""

if [[ "${#PENDING_ITEMS[@]}" -gt 0 ]]; then
  echo -e "${RED}── 未完成项（完成情况=⏳ 待输入）──${RESET}"
  for item in "${PENDING_ITEMS[@]}"; do
    echo -e "  ${YELLOW}⏳ $item${RESET}"
  done
  echo ""
fi

if [[ "${#AGENT_ERRORS[@]}" -gt 0 ]]; then
  echo -e "${RED}── Agent 签名缺失（完成Agent列必须为合法署名）──${RESET}"
  for item in "${AGENT_ERRORS[@]}"; do
    echo -e "  ${YELLOW}⚠️ $item${RESET}"
  done
  echo ""
fi

if [[ "${#SH_ERRORS[@]}" -gt 0 ]]; then
  echo -e "${RED}── sh 验收未签署 ──${RESET}"
  for item in "${SH_ERRORS[@]}"; do
    echo -e "  ${YELLOW}⚠️ $item${RESET}"
  done
  echo ""
fi

echo -e "${YELLOW}→ 修复方法：${RESET}"
echo -e "${YELLOW}  1. 完成情况列：⏳ 待输入 → 完成${RESET}"
echo -e "${YELLOW}  2. 完成Agent列：填写 Agent 署名（PL/DL/GD/GPO/Ability/Scene）${RESET}"
echo -e "${YELLOW}  3. sh验收列：填写 ✅已验收 或 PASS${RESET}"
exit 1
