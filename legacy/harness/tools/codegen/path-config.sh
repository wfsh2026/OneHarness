#!/usr/bin/env bash
# =============================================================================
# path-config.sh — 项目路径映射自动检测
# =============================================================================
# 使用方式: 在 PROJECT_ROOT（或 ROOT）赋值后 source 本文件
#
#   CODEGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   source "$CODEGEN_DIR/path-config.sh"
#
# 输出变量:
#   SCRIPTS_BASE   — Scripts 根目录    (e.g. "Assets/Script/Biubiubiu2")
#   SCENES_RUNTIME — Runtime 场景目录  (e.g. "Assets/Scenes/Biubiubiu2/Runtime")
#   BUNDLE_CONFIGS — Bundle Configs    (e.g. "Assets/ToBundle/Biubiubiu2/Configs")
#
# 当前支持的项目布局:
#   sausage-man-2022  — Assets/Script/Biubiubiu2 + Assets/Scenes/Biubiubiu2
#   generic (default) — Assets/Scripts + Assets/Scenes/Runtime + Assets/Bundle/Configs
# =============================================================================

_PC_ROOT="${PROJECT_ROOT:-${ROOT:-.}}"

if [[ -d "$_PC_ROOT/Assets/Script/Biubiubiu2" ]]; then
    # sausage-man-2022 项目布局
    SCRIPTS_BASE="Assets/Script/Biubiubiu2"
    SCENES_RUNTIME="Assets/Scenes/Biubiubiu2/Runtime"
    BUNDLE_CONFIGS="Assets/ToBundle/Biubiubiu2/Configs"
else
    # 通用项目布局（默认）
    SCRIPTS_BASE="Assets/Scripts"
    SCENES_RUNTIME="Assets/Scenes/Runtime"
    BUNDLE_CONFIGS="Assets/Bundle/Configs"
fi

# ── UGC 模式扩展（由 --ugc 标志触发）──
if [[ "${UGC_MODE:-}" == "true" ]]; then
    _UGC_CFG_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/ugc/ugc-config.sh"
    if [[ -f "$_UGC_CFG_PATH" ]]; then
        source "$_UGC_CFG_PATH"
    else
        echo "⚠️ UGC 配置不存在: ugc/ugc-config.sh，回退 PGC 流程"
        UGC_MODE=false
    fi
fi
