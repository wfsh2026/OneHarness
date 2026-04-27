#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# serve.sh — Unity WebGL 本地开发服务器
# ============================================================
# 前台运行，关闭终端或 Ctrl+C 自动停止。
#
# 用法:
#   ./serve.sh [目录] [--port 8080]
#
# 示例:
#   ./serve.sh                                    # 默认 WebGL 目录 + 8080
#   ./serve.sh /path/to/WebGL --port 9000         # 指定目录和端口
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SERVER_PY="$SCRIPT_DIR/_server.py"
DEFAULT_DIR="$PROJECT_ROOT/Build/Package/webgl/WebGL"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

# ─── 参数解析 ───
SERVE_DIR=""
PORT=8080

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port|-p) PORT="$2"; shift 2 ;;
        -h|--help)
            head -13 "$0" | grep "^#" | sed 's/^# \?//'
            exit 0 ;;
        -*) echo -e "${RED}❌ 未知选项: $1${NC}"; exit 1 ;;
        *) SERVE_DIR="$1"; shift ;;
    esac
done

[ -z "$SERVE_DIR" ] && SERVE_DIR="$DEFAULT_DIR"
[[ ! "$SERVE_DIR" = /* ]] && SERVE_DIR="$PROJECT_ROOT/$SERVE_DIR"

if [ ! -d "$SERVE_DIR" ]; then
    echo -e "${RED}❌ 目录不存在: $SERVE_DIR${NC}"
    echo -e "   请先构建 WebGL 或指定正确路径"
    exit 1
fi

# ─── 清理旧服务（如果有残留的 PID 文件） ───
PID_FILE="$PROJECT_ROOT/.webgl-server.pid"
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if command -v taskkill &>/dev/null; then
        taskkill //PID "$OLD_PID" //F > /dev/null 2>&1 || true
    else
        kill "$OLD_PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
    sleep 1
fi

# ─── 前台启动 ───
echo ""
echo -e "${GREEN}🌐 WebGL 服务器启动中...${NC}"
echo -e "   目录: ${CYAN}$SERVE_DIR${NC}"
echo -e "   地址: ${CYAN}http://localhost:$PORT/${NC}"
[ -f "$SERVE_DIR/index.html" ] && echo -e "   入口: ${CYAN}http://localhost:$PORT/index.html${NC}"
echo ""
echo -e "   ${YELLOW}按 Ctrl+C 停止服务器${NC}"
echo ""

# 找 Python
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo -e "${RED}❌ 未找到 Python，请安装 Python 3${NC}"
    exit 1
fi

# 清理函数
cleanup() {
    echo ""
    echo -e "${GREEN}🛑 服务器已停止${NC}"
    rm -f "$PID_FILE"
}
trap cleanup EXIT INT TERM

# 前台运行（Ctrl+C 或关闭终端会触发 cleanup）
$PYTHON "$SERVER_PY" "$SERVE_DIR" "$PORT" "$PID_FILE"
