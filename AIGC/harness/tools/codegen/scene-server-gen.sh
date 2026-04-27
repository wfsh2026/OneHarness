#!/usr/bin/env bash
# =============================================================================
# scene-server-gen.sh — 客户端场景转服务端场景（自动化工具）
#
# 功能：复制客户端场景 + 写入配置文件，供 Unity Editor 的 AI场景转换 菜单执行优化。
# 工作流：
#   1. 本脚本：复制场景文件 + 写入 Temp/AIGC_SceneConvertConfig.txt
#   2. AI Agent 调用 Unity MCP: execute_menu_item "Tools/功能/场景/AI场景转换"
#      Unity 执行：打开场景 → 优化（移除渲染组件/灯光，添加 HitType）→ 另存为 Server 前缀 → 注册 BuildSettings
#
# 用法：
#   bash scene-server-gen.sh \
#     --scene-name LevelTest_02_Temp \
#     --copy-from LevelTest_02 \
#     --project-root /path/to/unity/project
#
# 参数：
#   --scene-name  NAME    目标场景名（不含路径和扩展名），如 LevelTest_02_Temp
#   --copy-from   SOURCE  源场景名（可选），指定后会先复制源场景文件
#   --project-root PATH   Unity 项目根目录
#   --scene-dir    DIR    场景目录（可选，默认 Assets/Scenes/Runtime）
#
# OUTPUT FILES (供 Phase 4 技术文档 S-05 引用):
#   CREATE: Assets/Scenes/Runtime/{SceneName}.unity
#           — 场景副本 (条件: --copy-from 指定时复制)
#   CREATE: Temp/AIGC_SceneConvertConfig.txt
#           — 服务端转换配置 (供 Unity MCP 读取)
#   REQUIRE_MCP: execute_menu_item "Tools/功能/场景/AI场景转换"
#           — 产出 Assets/Scenes/Runtime/Server{SceneName}.unity (服务端场景)
# =============================================================================

set -euo pipefail

# ─── 参数解析 ───────────────────────────────────────────
SCENE_NAME=""
COPY_FROM=""
PROJECT_ROOT=""
SCENE_DIR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --scene-name)  SCENE_NAME="$2";   shift 2 ;;
        --copy-from)   COPY_FROM="$2";    shift 2 ;;
        --project-root) PROJECT_ROOT="$2"; shift 2 ;;
        --scene-dir)   SCENE_DIR="$2";    shift 2 ;;
        *)
            echo "❌ 未知参数: $1" >&2
            echo "用法: bash scene-server-gen.sh --scene-name NAME [--copy-from SOURCE] --project-root PATH" >&2
            exit 1
            ;;
    esac
done

# ─── 参数验证 ───────────────────────────────────────────
if [[ -z "$SCENE_NAME" ]]; then
    echo "❌ 缺少必要参数: --scene-name" >&2
    exit 1
fi
if [[ -z "$PROJECT_ROOT" ]]; then
    echo "❌ 缺少必要参数: --project-root" >&2
    exit 1
fi
if [[ ! -d "$PROJECT_ROOT" ]]; then
    echo "❌ 项目目录不存在: $PROJECT_ROOT" >&2
    exit 1
fi

# ─── 路径配置（自动检测项目布局）────────────────────────────────
CODEGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$CODEGEN_DIR/path-config.sh"
[[ -z "$SCENE_DIR" ]] && SCENE_DIR="$SCENES_RUNTIME"

SCENE_FULL_DIR="$PROJECT_ROOT/$SCENE_DIR"
TARGET_SCENE="$SCENE_FULL_DIR/${SCENE_NAME}.unity"
CONFIG_FILE="$PROJECT_ROOT/Temp/AIGC_SceneConvertConfig.txt"

# ─── Step 1: 复制源场景（如果指定了 --copy-from）───────────
if [[ -n "$COPY_FROM" ]]; then
    SRC_SCENE="$SCENE_FULL_DIR/${COPY_FROM}.unity"
    if [[ ! -f "$SRC_SCENE" ]]; then
        echo "❌ 源场景文件不存在: $SRC_SCENE" >&2
        exit 1
    fi
    if [[ -f "$TARGET_SCENE" ]]; then
        echo "⚠️  目标场景已存在，将覆盖: $TARGET_SCENE"
    fi
    cp "$SRC_SCENE" "$TARGET_SCENE"
    # 不复制 .meta 文件 —— Unity 会自动生成新的 GUID
    echo "✅ 场景复制完成: ${COPY_FROM}.unity → ${SCENE_NAME}.unity"
fi

# ─── Step 2: 验证目标场景存在 ─────────────────────────────
if [[ ! -f "$TARGET_SCENE" ]]; then
    echo "❌ 目标场景不存在: $TARGET_SCENE" >&2
    echo "   如果是新场景，请使用 --copy-from 参数指定源场景" >&2
    exit 1
fi

# ─── Step 3: 写入配置文件 ─────────────────────────────────
mkdir -p "$(dirname "$CONFIG_FILE")"
echo "$SCENE_NAME" > "$CONFIG_FILE"
echo "✅ 配置文件写入: $CONFIG_FILE"

# ─── 完成 ─────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  场景准备完成！"
echo "  客户端场景: $SCENE_DIR/${SCENE_NAME}.unity"
echo "  服务端场景: $SCENE_DIR/Server${SCENE_NAME}.unity (待生成)"
echo ""
echo "  下一步: AI Agent 调用 Unity MCP 执行场景优化"
echo "    → execute_menu_item \"Tools/功能/场景/AI场景转换\""
echo "    Unity 将自动: 优化 → 另存为 Server 前缀 → 注册 EditorBuildSettings"
echo "═══════════════════════════════════════════════════════"

# ═══════════════════════════════════════════════════════════
# 输出执行日志（供 AI Agent 查阅）
# ═══════════════════════════════════════════════════════════
LOG_DIR="${PROJECT_ROOT}/harness/temp"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/scene-server-gen-${SCENE_NAME}-$(date +%Y%m%d_%H%M%S).log"

{
    echo "═══════════════════════════════════════════════════════"
    echo "  工具: scene-server-gen.sh"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  参数: --scene-name ${SCENE_NAME}"
    if [[ -n "${COPY_FROM:-}" ]]; then echo "         --copy-from ${COPY_FROM}"; fi
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "📁 新建/修改文件:"
    if [[ -n "${COPY_FROM:-}" ]]; then
        echo "  [新建] ${SCENE_FULL_DIR}/${SCENE_NAME}.unity (从 ${COPY_FROM} 复制)"
    fi
    echo "  [新建] $CONFIG_FILE"
    echo ""
    echo "⏳ 待生成（MCP 执行后）:"
    echo "  [待生成] ${SCENE_FULL_DIR}/Server${SCENE_NAME}.unity"
    echo ""
    echo "📋 后续步骤（强制）:"
    echo "  1. 【强制】调用 MCP: execute_menu_item \"Tools/功能/场景/AI场景转换\""
} > "$LOG_FILE"

echo ""
echo "📋 执行日志已保存: $LOG_FILE"
