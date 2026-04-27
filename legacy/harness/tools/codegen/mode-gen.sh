#!/usr/bin/env bash
# =============================================================================
# mode-gen.sh — 游戏模式（Mode）脚手架代码生成器
#
# 功能：一键生成新游戏模式的完整代码骨架
#   1. 创建服务端模式文件 Server{Name}Mode.cs
#   2. 创建客户端模式文件 Client{Name}Mode.cs
#   3. 在 ModeData.cs 注册枚举、ID 常量、测试模式数据、匹配入口
#   4. 在 ServerModeSystem.cs / ClientModeSystem.cs 注册 switch 分支
#
# 用法:
#   bash mode-gen.sh \
#     --name CyberBatteryTest \
#     --desc "赛博炮台PVE测试" \
#     --map-id "MapSet.Id_CyberBatteryTest" \
#     --map-sign "CyberBatteryTest" \
#     --pve
#
# 参数:
#   必须:
#     --name <PascalCase>     模式名 (e.g., "CyberBatteryTest")
#     --desc <string>         中文描述 (e.g., "赛博炮台PVE测试")
#     --map-id <string>       地图引用 (e.g., "MapSet.Id_CyberBatteryTest")
#     --map-sign <string>     ModeMatch 地图标识 (e.g., "CyberBatteryTest")
#   可选:
#     --round-time <int>      回合时间秒数 (默认: 300, -1=无限)
#     --max-players <int>     最大玩家数 (默认: 1)
#     --type <test|normal>    模式类型 (默认: test)
#     --pve                   PVE 模式 (AI 敌人, KillRoleAI 计分)
#     --pvp                   PVP 模式 (团队对抗计分)
#     --dry-run               仅预览，不写入文件
#     --project-root <path>   项目根目录 (默认: 从脚本位置自动推导)
#
# OUTPUT FILES (供 Phase 4 技术文档 S-05 引用):
#   CREATE: Assets/Scripts/GamePlay/Server/Mode/Components/MainLoop/Server{Name}Mode.cs
#           — 服务端模式主循环 (ServerNetworkComponentBase)
#   CREATE: Assets/Scripts/GamePlay/Client/Mode/Components/Client{Name}Mode.cs
#           — 客户端模式组件
#   MODIFY: Assets/Scripts/Data/ModeData.cs
#           — ×4 插入: ModeEnum 枚举值 + Id 常量 + AddTestMode 数据块 + GetAllGameMatches 条目
#   MODIFY: Assets/Scripts/GamePlay/Server/Mode/ServerModeSystem.cs
#           — switch case 分支
#   MODIFY: Assets/Scripts/GamePlay/Client/Mode/ClientModeSystem.cs
#           — switch case 分支
# =============================================================================

set -euo pipefail

# ─── 颜色常量 ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── 参数默认值 ──────────────────────────────────────────────
NAME=""
DESC=""
MAP_ID=""
MAP_SIGN=""
ROUND_TIME=300
MAX_PLAYERS=1
MODE_TYPE="test"
PVE=false
PVP=false
DRY_RUN=false
PROJECT_ROOT=""

# ─── 参数解析 ────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)         NAME="$2";         shift 2 ;;
        --desc)         DESC="$2";         shift 2 ;;
        --map-id)       MAP_ID="$2";       shift 2 ;;
        --map-sign)     MAP_SIGN="$2";     shift 2 ;;
        --round-time)   ROUND_TIME="$2";   shift 2 ;;
        --max-players)  MAX_PLAYERS="$2";  shift 2 ;;
        --type)         MODE_TYPE="$2";    shift 2 ;;
        --pve)          PVE=true;          shift   ;;
        --pvp)          PVP=true;          shift   ;;
        --dry-run)      DRY_RUN=true;      shift   ;;
        --ugc)          UGC_MODE="true";   shift   ;;
        --project-root) PROJECT_ROOT="$2"; shift 2 ;;
        *)
            echo -e "${RED}❌ 未知参数: $1${NC}" >&2
            echo "用法: bash mode-gen.sh --name <Name> --desc <Desc> --map-id <Ref> --map-sign <Sign> [options]" >&2
            exit 1
            ;;
    esac
done

# ─── 自动推导项目根目录（向上遍历找 Assets/ 目录）───
if [[ -z "$PROJECT_ROOT" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    _dir="$SCRIPT_DIR"
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
_CODEGEN_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
source "$_CODEGEN_DIR/path-config.sh"

# ─── 必须参数验证 ────────────────────────────────────────────
MISSING=()
[[ -z "$NAME" ]]     && MISSING+=("--name")
[[ -z "$DESC" ]]     && MISSING+=("--desc")
if [[ "${UGC_MODE:-}" != "true" ]]; then
    [[ -z "$MAP_ID" ]]   && MISSING+=("--map-id")
    [[ -z "$MAP_SIGN" ]] && MISSING+=("--map-sign")
fi
if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo -e "${RED}❌ 缺少必要参数: ${MISSING[*]}${NC}" >&2
    exit 1
fi

if [[ "$MODE_TYPE" != "test" && "$MODE_TYPE" != "normal" ]]; then
    echo -e "${RED}❌ --type 必须是 test 或 normal，当前: $MODE_TYPE${NC}" >&2
    exit 1
fi

if [[ "$PVE" == true && "$PVP" == true ]]; then
    echo -e "${RED}❌ --pve 和 --pvp 不能同时使用${NC}" >&2
    exit 1
fi

# ─── 模板变量（PGC 默认值，UGC 钩子可覆写）──────────────────
SERVER_MODE_NS="Sofunny.BiuBiuBiu2.ServerGamePlay"
CLIENT_MODE_NS="Sofunny.BiuBiuBiu2.ClientGamePlay"
SERVER_MODE_CLASS="Server${NAME}Mode"
CLIENT_MODE_CLASS="Client${NAME}Mode"
EXTRA_USING=""

# ─── 日志（PGC/UGC 共用）────────────────────────────────────
LOG_DIR="$PROJECT_ROOT/harness/temp"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/mode-gen-${TIMESTAMP}.log"

# ─── 推导变量（PGC / UGC 共用）────────────────────────────────
# RoundWinState 枚举: PersonalScoreTop=1, TeamScoreTop=2, UniqueTeamScoreTop=3
ROUND_WIN_STATE="PersonalScoreTop"
if [[ "$PVP" == true ]]; then
    ROUND_WIN_STATE="TeamScoreTop"
fi

# ScoreChannel: PVE 用 KillRoleAI，PVP 用 KillRole，默认无
SCORE_CHANNEL=""
if [[ "$PVE" == true ]]; then
    SCORE_CHANNEL="KillRoleAI"
elif [[ "$PVP" == true ]]; then
    SCORE_CHANNEL="KillRole"
fi

# ── UGC 钩子：覆写路径/NS/名称/ID ──
if [[ "${UGC_MODE:-}" == "true" && ! -f "$_CODEGEN_DIR/ugc/mode-gen-ugc.sh" ]]; then
    echo "⚠️ UGC hook 不存在: ugc/mode-gen-ugc.sh，回退 PGC 流程"
    UGC_MODE=false
fi
if [[ "${UGC_MODE:-}" == "true" ]]; then
    source "$_CODEGEN_DIR/ugc/mode-gen-ugc.sh" config
else

# ─── ID 自动发现（强制） ──────────────────────────────────────
# ENUM_ID / MODE_ID 完全由工具从 ModeData.cs 自动读取，不接受手动传参
MODE_DATA_FILE="$PROJECT_ROOT/$SCRIPTS_BASE/Data/ModeData.cs"

if [[ ! -f "$MODE_DATA_FILE" ]]; then
    echo -e "${RED}❌ ModeData.cs 不存在: ${MODE_DATA_FILE}${NC}" >&2
    exit 1
fi

# ENUM_ID: ModeEnum { ... } 中所有 = N 的值，取最大值 +1
MAX_ENUM=$(sed -n '/public enum ModeEnum/,/}/p' "$MODE_DATA_FILE" | grep -oE '= *[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1)
if [[ -z "$MAX_ENUM" ]]; then
    echo -e "${RED}❌ 无法从 ModeData.cs 解析 ModeEnum 最大值${NC}" >&2
    exit 1
fi
ENUM_ID=$((MAX_ENUM + 1))
echo -e "${CYAN}🔍 ENUM_ID 自动分配: ${ENUM_ID} (ModeData.cs 最大值 ${MAX_ENUM} + 1)${NC}"

# MODE_ID: public const int Id_ 行的值，取最大值 +1
MAX_MODE_ID=$(grep 'public const int Id_' "$MODE_DATA_FILE" | grep -oE '= *[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1)
if [[ -z "$MAX_MODE_ID" ]]; then
    echo -e "${RED}❌ 无法从 ModeData.cs 解析 Mode ID 最大值${NC}" >&2
    exit 1
fi
MODE_ID=$((MAX_MODE_ID + 1))
echo -e "${CYAN}🔍 MODE_ID 自动分配: ${MODE_ID} (ModeData.cs 最大值 ${MAX_MODE_ID} + 1)${NC}"


# ─── 文件路径 ────────────────────────────────────────────────
MODE_DATA="$PROJECT_ROOT/$SCRIPTS_BASE/Data/ModeData.cs"
SERVER_SYSTEM="$PROJECT_ROOT/$SCRIPTS_BASE/GamePlay/Server/Mode/ServerModeSystem.cs"
CLIENT_SYSTEM="$PROJECT_ROOT/$SCRIPTS_BASE/GamePlay/Client/Mode/ClientModeSystem.cs"
SERVER_MODE_DIR="$PROJECT_ROOT/$SCRIPTS_BASE/GamePlay/Server/Mode/Components/MainLoop"
CLIENT_MODE_DIR="$PROJECT_ROOT/$SCRIPTS_BASE/GamePlay/Client/Mode/Components"
SERVER_MODE_FILE="$SERVER_MODE_DIR/Server${NAME}Mode.cs"
CLIENT_MODE_FILE="$CLIENT_MODE_DIR/Client${NAME}Mode.cs"

# ─── 文件存在性校验 ──────────────────────────────────────────
for f in "$MODE_DATA" "$SERVER_SYSTEM" "$CLIENT_SYSTEM"; do
    if [[ ! -f "$f" ]]; then
        echo -e "${RED}❌ 文件不存在: $f${NC}" >&2
        exit 1
    fi
done
for d in "$SERVER_MODE_DIR" "$CLIENT_MODE_DIR"; do
    if [[ ! -d "$d" ]]; then
        echo -e "${RED}❌ 目录不存在: $d${NC}" >&2
        exit 1
    fi
done

fi  # end of UGC_MODE else-PGC block

# ═════════════════════════════════════════════════════════════
# 工具函数
# ═════════════════════════════════════════════════════════════

log()       { echo "$@" | tee -a "$LOG_FILE"; }
log_color() { echo -e "$@" | tee -a "$LOG_FILE"; }

step() {
    local n=$1 total=8 msg="$2"
    log_color "\n${CYAN}[Step ${n}/${total}]${NC} ${msg}"
}

ok()   { log_color "  ${GREEN}✅ $1${NC}"; }
skip() { log_color "  ${YELLOW}⚠️  $1${NC}"; }
fail() { log_color "  ${RED}❌ $1${NC}" >&2; exit 1; }

# 在第一个匹配 pattern 的行之前插入多行文本（awk，跨平台）
insert_before() {
    local pattern="$1" text="$2" file="$3"
    local tmp="${file}.tmp.$$" txt_file="${file}.ins.$$"
    printf '%s\n' "$text" > "$txt_file"
    awk -v pat="$pattern" -v tf="$txt_file" '
        !done && $0 ~ pat {
            while ((getline line < tf) > 0) print line
            close(tf)
            done = 1
        }
        { print }
    ' "$file" > "$tmp"
    mv "$tmp" "$file"
    rm -f "$txt_file"
}

# 在最后一个匹配 pattern 的行之后插入多行文本
insert_after_last() {
    local pattern="$1" text="$2" file="$3"
    local tmp="${file}.tmp.$$"
    local last_line
    last_line=$(grep -n "$pattern" "$file" | tail -1 | cut -d: -f1)
    if [[ -z "$last_line" ]]; then
        skip "未找到匹配: $pattern in $(basename "$file")"
        return 1
    fi
    local txt_file="${file}.ins.$$"
    printf '%s\n' "$text" > "$txt_file"
    awk -v ln="$last_line" -v tf="$txt_file" '
        NR==ln { print; while ((getline line < tf) > 0) print line; close(tf); next }
        { print }
    ' "$file" > "$tmp"
    mv "$tmp" "$file"
    rm -f "$txt_file"
}

# 在指定行号之前插入多行文本
insert_before_line() {
    local line_num="$1" text="$2" file="$3"
    local tmp="${file}.tmp.$$" txt_file="${file}.ins.$$"
    printf '%s\n' "$text" > "$txt_file"
    awk -v ln="$line_num" -v tf="$txt_file" '
        NR==ln {
            while ((getline line < tf) > 0) print line
            close(tf)
        }
        { print }
    ' "$file" > "$tmp"
    mv "$tmp" "$file"
    rm -f "$txt_file"
}

# 通过花括号深度定位方法/块的闭合行号
find_closing_brace() {
    local pattern="$1" file="$2"
    awk -v pat="$pattern" '
        $0 ~ pat { found = 1; depth = 0 }
        found {
            for (i = 1; i <= length($0); i++) {
                c = substr($0, i, 1)
                if (c == "{") depth++
                if (c == "}") { depth--; if (depth == 0) { print NR; exit } }
            }
        }
    ' "$file"
}

# ═════════════════════════════════════════════════════════════
# 横幅
# ═════════════════════════════════════════════════════════════
log "═══════════════════════════════════════════════════════"
log "  Mode 代码生成器"
log "  模式名:   $NAME"
log "  描述:     $DESC"
log "  枚举:     ModeEnum.Mode${NAME} = $ENUM_ID"
log "  ID:       Id_${NAME} = $MODE_ID"
log "  地图:     $MAP_ID ($MAP_SIGN)"
log "  计分:     $SCORE_CHANNEL"
log "  回合时间: $ROUND_TIME"
log "  最大人数: $MAX_PLAYERS"
log "  类型:     $MODE_TYPE"
if [[ "$DRY_RUN" == true ]]; then
    log_color "  ${YELLOW}(DRY-RUN 模式 — 不写入文件)${NC}"
fi
log "═══════════════════════════════════════════════════════"

# 追踪变更用于汇总
CREATED_FILES=()
MODIFIED_FILES=()

# ═════════════════════════════════════════════════════════════
# Step 1/8: 创建服务端模式文件
# ═════════════════════════════════════════════════════════════
step 1 "创建服务端模式: Server${NAME}Mode.cs"

if [[ -f "$SERVER_MODE_FILE" ]]; then
    skip "文件已存在，跳过: $(basename "$SERVER_MODE_FILE")"
else
    read -r -d '' SERVER_CONTENT <<CSEOF || true
// 该文件由 mode-gen.sh 自动生成，AI 不得删除该注释
using System.Collections.Generic;
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Data;
using Sofunny.BiuBiuBiu2.Message;
using Sofunny.BiuBiuBiu2.ServerMessage;
${EXTRA_USING}using UnityEngine;

namespace ${SERVER_MODE_NS} {
    /// <summary>
    /// ${DESC} — 服务端模式逻辑
    /// </summary>
    public class ${SERVER_MODE_CLASS} : ComponentBase {
        private List<SE_Mode.PlayModeCharacterData> characterList;

        protected override void OnAwake() {
            Register<SE_Mode.Event_GameState>(OnGameStateCallBack);
            Register<SE_Mode.Event_AddCharacterFinish>(OnAddCharacterFinish);
            MsgRegister.Register<SM_Mode.StartMode>(OnStartModeCallBack);
            MsgRegister.Register<SM_Mode.GetStartPoint>(OnGetStartPointCallBack);
        }

        protected override void OnStart() {
            AddUpdate(OnUpdate);
        }

        protected override void OnClear() {
            characterList = null;
            RemoveUpdate(OnUpdate);
            Unregister<SE_Mode.Event_GameState>(OnGameStateCallBack);
            Unregister<SE_Mode.Event_AddCharacterFinish>(OnAddCharacterFinish);
            MsgRegister.Unregister<SM_Mode.StartMode>(OnStartModeCallBack);
            MsgRegister.Unregister<SM_Mode.GetStartPoint>(OnGetStartPointCallBack);
        }

        private void OnStartModeCallBack(SM_Mode.StartMode ent) {
            Dispatcher(new SE_Mode.Event_GetCharacterList {
                CallBack = list => characterList = list
            });
        }

        private void OnGameStateCallBack(ISystemMsg body, SE_Mode.Event_GameState ent) {
            if (ent.GameState == ModeData.GameStateEnum.RoundStart) {
                OnRoundStart();
            }
        }

        private void OnRoundStart() {
            // TODO: 回合开始逻辑
        }

        private void OnUpdate(float dt) {
            // TODO: 帧更新逻辑
        }

        private void OnGetStartPointCallBack(SM_Mode.GetStartPoint ent) {
            var isGameStart = ModeData.PlayGameState is
                ModeData.GameStateEnum.Wait or
                ModeData.GameStateEnum.WaitStartDownTime or
                ModeData.GameStateEnum.WaitRoundStart;
            Dispatcher(new SE_Mode.Event_GetCharacterSpawnPoint {
                IsGameStart = isGameStart,
                CharacterGpo = ent.CharacterGPO,
                CallBack = ent.CallBack
            });
        }

        private void OnAddCharacterFinish(ISystemMsg body, SE_Mode.Event_AddCharacterFinish ent) {
            var data = ent.Data;
            var characterGpo = data.CharacterGPO;
            if (characterGpo.GetGPOType() == GPOData.GPOType.RoleAI) return;
            characterGpo.Dispatcher(new SE_GPO.Event_ModeEquipWeapon {
                WeaponList = data.WeaponList,
            });
        }
    }
}
CSEOF

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将创建: $SERVER_MODE_FILE"
    else
        printf '%s\n' "$SERVER_CONTENT" > "$SERVER_MODE_FILE"
        CREATED_FILES+=("$SERVER_MODE_FILE")
        ok "已创建: $(basename "$SERVER_MODE_FILE")"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 2/8: 创建客户端模式文件
# ═════════════════════════════════════════════════════════════
step 2 "创建客户端模式: Client${NAME}Mode.cs"

if [[ -f "$CLIENT_MODE_FILE" ]]; then
    skip "文件已存在，跳过: $(basename "$CLIENT_MODE_FILE")"
else
    read -r -d '' CLIENT_CONTENT <<CSEOF || true
// 该文件由 mode-gen.sh 自动生成，AI 不得删除该注释
using Sofunny.BiuBiuBiu2.ClientMessage;
using Sofunny.BiuBiuBiu2.CoreGamePlay;
using Sofunny.BiuBiuBiu2.Data;
using Sofunny.BiuBiuBiu2.Message;
${EXTRA_USING}
namespace ${CLIENT_MODE_NS} {
    /// <summary>
    /// ${DESC} — 客户端模式逻辑
    /// </summary>
    public class ${CLIENT_MODE_CLASS} : ComponentBase {
        private bool showWarEnd;

        protected override void OnAwake() {
            MsgRegister.Register<CM_Mode.SetGameState>(OnSetGameState);
        }

        protected override void OnClear() {
            MsgRegister.Unregister<CM_Mode.SetGameState>(OnSetGameState);
        }

        private void OnSetGameState(CM_Mode.SetGameState ent) {
            if (showWarEnd) return;
            switch (ent.GameState) {
                case ModeData.GameStateEnum.RoundEnd:
                case ModeData.GameStateEnum.WaitNextRound:
                case ModeData.GameStateEnum.WaitModeOver:
                case ModeData.GameStateEnum.ModeOver:
                case ModeData.GameStateEnum.SaveReport:
                case ModeData.GameStateEnum.QuitApp:
                    MsgRegister.Dispatcher(new CM_UI.ShowDialog {
                        Message = "${DESC}结束",
                        invokeSureFuncAfterClose = true,
                        OnSure = () => { MsgRegister.Dispatcher(new CM_Game.QuitGame()); },
                    });
                    showWarEnd = true;
                    return;
            }
        }
    }
}
CSEOF

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将创建: $CLIENT_MODE_FILE"
    else
        printf '%s\n' "$CLIENT_CONTENT" > "$CLIENT_MODE_FILE"
        CREATED_FILES+=("$CLIENT_MODE_FILE")
        ok "已创建: $(basename "$CLIENT_MODE_FILE")"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Steps 3-8: MODIFY 操作（PGC vs UGC 分流）
# ═════════════════════════════════════════════════════════════
if [[ "${UGC_MODE:-}" == "true" ]]; then
# ── UGC MODIFY: 注册枢纽插入 ──
source "$_CODEGEN_DIR/ugc/mode-gen-ugc.sh" modify
else

# ═════════════════════════════════════════════════════════════
# Step 3/8: ModeData.cs — 添加 ModeEnum 枚举项
# ═════════════════════════════════════════════════════════════
step 3 "ModeData.cs — 添加 ModeEnum.Mode${NAME} = ${ENUM_ID}"

if grep -q "Mode${NAME}[[:space:]]*=" "$MODE_DATA"; then
    skip "ModeEnum 中已存在 Mode${NAME}，跳过"
else
    ENUM_CLOSE=$(find_closing_brace "public enum ModeEnum" "$MODE_DATA")
    if [[ -z "$ENUM_CLOSE" ]]; then
        fail "无法定位 ModeEnum 闭合括号"
    fi
    ENUM_ENTRY="            Mode${NAME} = ${ENUM_ID},"

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在 ModeEnum 第 ${ENUM_CLOSE} 行前插入: Mode${NAME} = ${ENUM_ID}"
    else
        insert_before_line "$ENUM_CLOSE" "$ENUM_ENTRY" "$MODE_DATA"
        MODIFIED_FILES+=("ModeData.cs:ModeEnum")
        ok "已添加枚举: Mode${NAME} = ${ENUM_ID}"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 4/8: ModeData.cs — 添加 ID 常量（仅 test 类型）
# ═════════════════════════════════════════════════════════════
step 4 "ModeData.cs — 添加 ID 常量 Id_${NAME} = ${MODE_ID}"

if [[ "$MODE_TYPE" != "test" ]]; then
    skip "非 test 类型，跳过 ID 常量"
elif grep -q "Id_${NAME}[[:space:]]*=" "$MODE_DATA"; then
    skip "ID 常量 Id_${NAME} 已存在，跳过"
else
    ID_ENTRY="        public const int Id_${NAME} = ${MODE_ID};"

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在最后一个 Id_ 常量后插入: Id_${NAME} = ${MODE_ID}"
    else
        insert_after_last "public const int Id_" "$ID_ENTRY" "$MODE_DATA"
        MODIFIED_FILES+=("ModeData.cs:Id_constant")
        ok "已添加常量: Id_${NAME} = ${MODE_ID}"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 5/8: ModeData.cs — 添加 AddTestMode() 数据块（仅 test 类型）
# ═════════════════════════════════════════════════════════════
step 5 "ModeData.cs — 添加 AddTestMode() 数据块"

if [[ "$MODE_TYPE" != "test" ]]; then
    skip "非 test 类型，跳过 AddTestMode 数据"
elif grep -q "Mode = ModeEnum.Mode${NAME}," "$MODE_DATA"; then
    skip "AddTestMode 中已存在 Mode${NAME} 数据块，跳过"
else
    # 构建 ScoreChannelDatas 块
    if [[ "$PVE" == true ]]; then
        SCORE_BLOCK="                ScoreChannelDatas = new[] {
                    new ScoreChannelData {
                        Channel = GetScoreChannelEnum.KillRoleAI, Score = 1,
                    },
                },"
    elif [[ "$PVP" == true ]]; then
        SCORE_BLOCK="                ScoreChannelDatas = new[] {
                    new ScoreChannelData {
                        Channel = GetScoreChannelEnum.KillRole, Score = 1,
                    },
                },"
    else
        SCORE_BLOCK="                ScoreChannelDatas = new ScoreChannelData[0],"
    fi

    DATA_BLOCK="            Datas.Add(new Data {
                Id = Id_${NAME},
                Mode = ModeEnum.Mode${NAME},
                ModeName = \"${DESC}\",
                MaxRoleNum = ${MAX_PLAYERS},
                MaxRoleNumPerTeam = ${MAX_PLAYERS},
                MinStartModeTeamNum = 1,
                MinStartPlayCharacterNum = 1,
                StartModeDownTime = 3,
                StartRoundDownTime = 0,
                WaitNextRoundTime = 5,
                WaitModeOverTime = 5,
                RoundTime = ${ROUND_TIME},
                WinScore = -1,
                ModeWinRoundCount = 1,
                MaxRoundCount = 1,
                PerRoundRandWeapon = false,
                RoundWinState = RoundWinStateEnum.${ROUND_WIN_STATE},
                ModeWinState = ModeWinStateEnum.RoundWinTop,
${SCORE_BLOCK}
                EnbaleChangeWeapon = true,
            });"

    METHOD_CLOSE=$(find_closing_brace "private static void AddTestMode" "$MODE_DATA")
    if [[ -z "$METHOD_CLOSE" ]]; then
        fail "无法定位 AddTestMode() 闭合括号"
    fi

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在 AddTestMode() 第 ${METHOD_CLOSE} 行前插入数据块"
    else
        insert_before_line "$METHOD_CLOSE" "$DATA_BLOCK" "$MODE_DATA"
        MODIFIED_FILES+=("ModeData.cs:AddTestMode")
        ok "已添加 AddTestMode() 数据块"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 6/8: ModeData.cs — 添加 GetAllGameMatches() 入口
# ═════════════════════════════════════════════════════════════
step 6 "ModeData.cs — 添加 GetAllGameMatches() 匹配入口"

if grep -q "Id_${NAME}.*${MAP_SIGN}" "$MODE_DATA"; then
    skip "GetAllGameMatches 中已存在 ${NAME} 入口，跳过"
else
    MATCH_ENTRY="            list.Insert(list.Count, new ModeMatch(Id_${NAME}, Id_${NAME}, ${MAP_ID}, \"${MAP_SIGN}\", \"${DESC}\", \"${DESC}\", 0, 0, 0, \"\",\"\"));"

    # 定位 GetAllGameMatches 方法内的 return list;
    RETURN_LINE=$(awk '/GetAllGameMatches/{ f=1 } f && /return list;/{ print NR; exit }' "$MODE_DATA")
    if [[ -z "$RETURN_LINE" ]]; then
        fail "无法定位 GetAllGameMatches 中的 return list;"
    fi

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在 GetAllGameMatches return 前（第 ${RETURN_LINE} 行）插入匹配入口"
    else
        insert_before_line "$RETURN_LINE" "$MATCH_ENTRY" "$MODE_DATA"
        MODIFIED_FILES+=("ModeData.cs:GetAllGameMatches")
        ok "已添加匹配入口: ${NAME}"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 7/8: ServerModeSystem.cs — 添加 switch case
# ═════════════════════════════════════════════════════════════
step 7 "ServerModeSystem.cs — 添加 Mode${NAME} 分支"

if grep -q "ModeEnum.Mode${NAME}" "$SERVER_SYSTEM"; then
    skip "ServerModeSystem 中已存在 Mode${NAME} 分支，跳过"
else
    SERVER_CASE="                case ModeData.ModeEnum.Mode${NAME}:
                    AddComponent<Server${NAME}Mode>();
                    AddComponent<ServerTeamModeSpawnPoint>();
                    break;"

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在 ServerModeSystem default: 前插入 case"
    else
        insert_before "default:" "$SERVER_CASE" "$SERVER_SYSTEM"
        MODIFIED_FILES+=("ServerModeSystem.cs")
        ok "已添加 Server switch case"
    fi
fi

# ═════════════════════════════════════════════════════════════
# Step 8/8: ClientModeSystem.cs — 添加 switch case
# ═════════════════════════════════════════════════════════════
step 8 "ClientModeSystem.cs — 添加 Mode${NAME} 分支"

if grep -q "ModeEnum.Mode${NAME}" "$CLIENT_SYSTEM"; then
    skip "ClientModeSystem 中已存在 Mode${NAME} 分支，跳过"
else
    CLIENT_CASE="                case ModeData.ModeEnum.Mode${NAME}:
                    AddComponent<Client${NAME}Mode>();
                    break;"

    if [[ "$DRY_RUN" == true ]]; then
        ok "[DRY-RUN] 将在 ClientModeSystem default: 前插入 case"
    else
        insert_before "default:" "$CLIENT_CASE" "$CLIENT_SYSTEM"
        MODIFIED_FILES+=("ClientModeSystem.cs")
        ok "已添加 Client switch case"
    fi
fi

fi  # end of UGC_MODE MODIFY guard

# ═════════════════════════════════════════════════════════════
# 汇总
# ═════════════════════════════════════════════════════════════
log ""
log "═══════════════════════════════════════════════════════"
log "  生成完成!"
if [[ ${#CREATED_FILES[@]} -gt 0 ]]; then
    log_color "  ${GREEN}创建文件 (${#CREATED_FILES[@]}):${NC}"
    for f in "${CREATED_FILES[@]}"; do
        log "    + $(basename "$f")"
    done
fi
if [[ ${#MODIFIED_FILES[@]} -gt 0 ]]; then
    log_color "  ${GREEN}修改文件 (${#MODIFIED_FILES[@]}):${NC}"
    for f in "${MODIFIED_FILES[@]}"; do
        log "    ~ $f"
    done
fi
if [[ ${#CREATED_FILES[@]} -eq 0 && ${#MODIFIED_FILES[@]} -eq 0 ]]; then
    log_color "  ${YELLOW}无变更（所有内容已存在）${NC}"
fi
log "  日志: $LOG_FILE"
log "═══════════════════════════════════════════════════════"
