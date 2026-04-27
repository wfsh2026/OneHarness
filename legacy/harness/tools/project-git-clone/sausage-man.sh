#!/bin/sh
# =============================================================================
# sausage-man.sh — 香肠派对 多仓库拉取工具
#
# 支持两种执行场景（自动识别）：
#   - 在 aigc-framework 里执行：从 local-env.json 读取香肠派对路径
#   - 在香肠派对项目里执行：使用当前仓库根目录
#
# 用法：
#   bash aigc/harness/tools/project-git-clone/sausage-man.sh <branch> [tag]
#   bash aigc/harness/tools/project-git-clone/sausage-man.sh develop
#   bash aigc/harness/tools/project-git-clone/sausage-man.sh release/v61/0.61.1 v61.0
# =============================================================================

# === 参数 ===
branch="${1:-develop}"
global_tag="${2:-}"

if [ -z "$branch" ]; then
    echo "[ERROR] 请指定分支，例如：bash aigc/harness/tools/project-git-clone/sausage-man.sh develop"
    exit 1
fi

# === 项目根路径（自动识别执行环境）===
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "[ERROR] 未找到 git 仓库，请在项目根目录下执行。"
    exit 1
fi

if [ -f "$REPO_ROOT/aigc/harness/rules/Workflow/workflow-framework.md" ]; then
    # 在 aigc-framework 里执行 → 从 local-env.json 读香肠派对路径
    LOCAL_ENV="$REPO_ROOT/local-env.json"
    if [ ! -f "$LOCAL_ENV" ]; then
        echo "[ERROR] 未找到 local-env.json，请先完成项目绑定。"
        exit 1
    fi
    client_path=$(python3 -c "
import json, sys
env = json.load(open('$LOCAL_ENV'))
p = env.get('projects', {}).get('sausage-man', '')
if not p:
    print('[ERROR] local-env.json 中未找到 sausage-man 路径', file=sys.stderr)
    sys.exit(1)
print(p)
")
    if [ $? -ne 0 ]; then exit 1; fi
else
    # 在游戏项目里执行 → 当前仓库根目录就是项目路径
    client_path="$REPO_ROOT"
fi

echo "📂 项目路径：$client_path"
echo "🌿 目标分支：$branch"
[ -n "$global_tag" ] && echo "🏷  目标标签：$global_tag"
echo ""

# === 模块开关（0=不拉取 1=拉取保留修改 2=强制拉取）===
client=2
script=2
script_biubiubiu2=2
bundle=2
art=2
scene=2
audio=2

# === 标签 ===
tag_client="$global_tag"
tag_script="$global_tag"
tag_script_biubiubiu2="$global_tag"
tag_bundle="$global_tag"
tag_art="$global_tag"
tag_scene="$global_tag"
tag_audio="$global_tag"

# === 路径配置 ===
bundle_path="${client_path}/Assets/ToBundle"
script_path="${client_path}/Assets/Script"
gold_dash_path="${script_path}/GoldDash"
script_biubiubiu2_path="${client_path}/Assets/Script/Biubiubiu2"
art_path="${client_path}/Assets/Art"
scene_path="${client_path}/Assets/Scenes"
audio_path="${client_path}/Assets/Audio"

# === 远程 Git 地址 ===
remoteurl_client="git@git.tube:sausage-man/u3d-client.git"
remoteurl_script="git@git.tube:sausage-man/u3d-scripts.git"
remoteurl_script_biubiubiu2="git@git.tube:sausage-man/u3d-biubiubiu2-scripts.git"
remoteurl_bundle="git@git.tube:sausage-man/u3d-bundles.git"
remoteurl_art="git@git.tube:sausage-man/u3d-art.git"
remoteurl_scene="git@git.tube:sausage-man/u3d-scenes.git"
remoteurl_audio="git@git.tube:sausage-man/u3d-audio.git"

# === 进度状态 ===
progress_done=0
TMP_DIR=$(mktemp -d)

total_tasks=0
for val in $client $script $script_biubiubiu2 $bundle $art $scene $audio; do
    if [ "$val" != "0" ]; then total_tasks=$((total_tasks + 1)); fi
done

# === 工具函数 ===
draw_progress_bar() {
    local current=$1
    local total=$2
    local width=30
    local done=$((current * width / total))
    local remain=$((width - done))
    local bar=$(printf "%${done}s" | tr ' ' '#')
    bar+=$(printf "%${remain}s" | tr ' ' '.')
    echo -ne "\r[$bar] $current/$total 已完成"
}

cloneOne() {
    local mode="$1"
    local br="$2"
    local path="$3"
    local url="$4"
    local tag="$5"

    if [ "$mode" = "0" ]; then return 0; fi
    if [ ! -d "$path" ]; then
        echo "    ➤ 首次创建：$path"
        git clone "$url" "$path"
    fi

    cd "$path" || return 1
    git fetch --progress -f

    if [ -z "$tag" ]; then
        if [ "$mode" = "2" ]; then
            git stash
            git checkout -B "$br" "origin/$br" -f
        else
            git checkout -B "$br" "origin/$br"
        fi
    else
        git tag -d "$tag" 2>/dev/null
        git fetch --tags
        git stash
        git checkout -B "$br" "origin/$br" -f
        git reset --hard "$tag"
    fi

    if [ $? -eq 0 ]; then
        echo "    ➤ 最新提交: $(git log -1 --oneline)"
        return 0
    fi
    return 1
}

safe_clone() {
    local key="$1"
    local mode="$2"
    local path="$3"
    local url="$4"
    local tag="$5"

    if [ "$mode" = "0" ]; then return 0; fi

    echo ""
    echo "🔄 开始拉取：$key ($branch)"
    if [ -d "$path" ] && [ "$(ls -A "$path")" = "" ]; then rm -rf "$path"; fi

    cloneOne "$mode" "$branch" "$path" "$url" "$tag" > "/tmp/clone_${key}.log" 2>&1
    local result=$?

    if [ $result -eq 0 ]; then
        touch "$TMP_DIR/success_${key}"
        echo "[✅ 完成] $key"
    else
        touch "$TMP_DIR/fail_${key}"
        echo "[❌ 错误] $key 拉取失败，查看日志：/tmp/clone_${key}.log"
    fi

    progress_done=$((progress_done + 1))
    draw_progress_bar "$progress_done" "$total_tasks"
    echo ""
    return $result
}

# === 拉取逻辑 ===
if [ "$(ls -A "$client_path" 2>/dev/null)" = "" ]; then rm -rf "$client_path"; fi
safe_clone "client" $client "$client_path" "$remoteurl_client" "$tag_client"

if [ "$(ls -A "$script_path" 2>/dev/null)" = "" ]; then rm -rf "$script_path"; fi
safe_clone "script" $script "$script_path" "$remoteurl_script" "$tag_script"
script_success=$?

{
    if [ -d "$gold_dash_path" ] && [ "$(find "$gold_dash_path" -type f -print -quit)" ]; then
        echo "GoldDash 目录有文件，跳过 Biubiubiu2 仓库拉取"
        rm -rf "$script_biubiubiu2_path"
    else
        echo "GoldDash 目录不存在或为空，拉取 Biubiubiu2 仓库"
        rm -rf "$gold_dash_path"
        safe_clone "script_biubiubiu2" $script_biubiubiu2 "$script_biubiubiu2_path" "$remoteurl_script_biubiubiu2" "$tag_script_biubiubiu2"
    fi
} &

for entry in \
    "art $art $art_path $remoteurl_art $tag_art" \
    "scene $scene $scene_path $remoteurl_scene $tag_scene" \
    "bundle $bundle $bundle_path $remoteurl_bundle $tag_bundle" \
    "audio $audio $audio_path $remoteurl_audio $tag_audio"
do
    set -- $entry
    if [ "$2" != "0" ]; then
        ( safe_clone "$1" "$2" "$3" "$4" "$5" ) &
    fi
done

wait

# === 完成汇报 ===
success_count=$(ls "$TMP_DIR"/success_* 2>/dev/null | wc -l | tr -d ' ')
fail_count=$(ls "$TMP_DIR"/fail_* 2>/dev/null | wc -l | tr -d ' ')
rm -rf "$TMP_DIR"

echo ""
echo "======================================"
echo "🎉 所有模块拉取完毕"
echo "🌿 分支：$branch"
[ -n "$global_tag" ] && echo "🏷  标签：$global_tag"
echo "✅ 成功：$success_count"
echo "❌ 失败：$fail_count"
echo "📂 日志：/tmp/clone_模块名.log"
echo "======================================"
