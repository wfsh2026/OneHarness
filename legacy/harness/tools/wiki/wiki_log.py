"""wiki/log.md 自动追加模块

所有 wiki 工具在完成操作后调用此模块，自动向 wiki/log.md 插入一条记录（最新在上）。

类型约定：
  - ingest   : 摄入新资料 / feature 分配 / system-map 更新
  - lint     : 健康检查 / wiki-map 重建 / 覆盖率检查 / 图谱重建
  - query    : 有归档价值的查询
  - schema   : 规则 / 结构变更

质量要求（不满足则拒绝写入）：
  - title ≥ 6 字符，需说明「做了什么」而非仅「什么类型」
  - details 必填，≥ 30 字符，需包含具体影响（文件名/系统名/数量+上下文）
  - 每条 detail 行 ≥ 8 字符
  - 禁止纯数字/计数条目（如"结果: 8"），需说明语境

用法（Python import）：
    from wiki_log import append_wiki_log
    append_wiki_log("lint", "wiki-map 重建（119→191）",
                    "扩展 wiki-resolve.py 扫描 aigc/docs/，新增 72 个文档映射\\n歧义项: 3（均为 parent/name 前缀冲突）")

用法（CLI）：
    python3 harness/tools/wiki/wiki_log.py schema "system-map 新增构建系统行" "关联 build-system.md、AssetBuilder、HybridCLRBuilder 等 7 个文件\\n说明备注调整为兼容 Editor 路径"
"""

import os
import re
from datetime import datetime
from pathlib import Path

# 从工具脚本位置推算项目根目录：harness/tools/wiki/ → 上 3 级
_REPO_ROOT = Path(__file__).resolve().parents[4]   # aigc/harness/tools/wiki/ → 项目根
_LOG_PATH = _REPO_ROOT / "aigc" / "wiki" / "log.md"

# ── 质量门禁 ────────────────────────────────────────────────
MIN_TITLE_LEN = 6
MIN_DETAILS_TOTAL_LEN = 30
MIN_DETAIL_LINE_LEN = 8


class LogQualityError(ValueError):
    """日志条目质量不达标"""
    pass


def _validate_entry(log_type: str, title: str, details: str) -> None:
    """校验日志条目质量，不达标抛出 LogQualityError。"""
    errors = []

    # 1. 标题长度
    if len(title.strip()) < MIN_TITLE_LEN:
        errors.append(
            f"标题过短（{len(title.strip())}字符 < {MIN_TITLE_LEN}）。"
            f"需说明「做了什么」，如 'wiki-map 重建（119→191）' 而非 'wiki-map'"
        )

    # 2. details 必填
    stripped_details = details.strip()
    if not stripped_details:
        errors.append(
            "details 不能为空。每条日志必须说明具体影响（涉及哪些文件/系统、改了什么、结果如何）"
        )
    else:
        # 3. details 总长度
        if len(stripped_details) < MIN_DETAILS_TOTAL_LEN:
            errors.append(
                f"details 内容过短（{len(stripped_details)}字符 < {MIN_DETAILS_TOTAL_LEN}）。"
                f"需包含具体文件名/系统名/变更内容，不要只写数字或状态"
            )

        # 4. 每行最短长度
        short_lines = []
        for line in stripped_details.splitlines():
            line = line.strip()
            if line and len(line) < MIN_DETAIL_LINE_LEN:
                short_lines.append(line)
        if short_lines:
            errors.append(
                f"以下 detail 行过短（< {MIN_DETAIL_LINE_LEN}字符），需补充上下文：\n"
                + "\n".join(f"  ✗ '{l}'" for l in short_lines)
            )

    if errors:
        msg = f"❌ 日志质量不达标（{len(errors)} 项问题）：\n" + "\n".join(
            f"  {i+1}. {e}" for i, e in enumerate(errors)
        )
        raise LogQualityError(msg)


def append_wiki_log(log_type: str, title: str, details: str = "") -> None:
    """向 wiki/log.md 插入一条操作记录（最新在最前）。

    Args:
        log_type: ingest | lint | query | schema
        title: 操作标题（一行，≥6字符）
        details: 补充说明（必填，≥30字符，多行会缩进为列表项）

    Raises:
        LogQualityError: 条目不满足质量要求
    """
    _validate_entry(log_type, title, details)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## [{date_str}] {log_type} | {title}\n"
    if details:
        for line in details.strip().splitlines():
            entry += f"\n- {line}"
        entry += "\n"

    # 确保目录存在
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 如果文件不存在，写入头部
    if not _LOG_PATH.exists():
        header = (
            "# Wiki 操作日志\n\n"
            "> 记录 knowledge/ 下文件的修改历史\n\n"
            "---\n"
        )
        _LOG_PATH.write_text(header + entry, encoding="utf-8")
        return

    # 已有文件：在 header（第一个 `---` 行）之后插入新条目
    content = _LOG_PATH.read_text(encoding="utf-8")
    separator = "\n---\n"
    idx = content.find(separator)
    if idx >= 0:
        insert_pos = idx + len(separator)
        new_content = content[:insert_pos] + entry + content[insert_pos:]
    else:
        new_content = content + entry
    _LOG_PATH.write_text(new_content, encoding="utf-8")


# ── CLI 入口 ──────────────────────────────────────────────
VALID_TYPES = {"ingest", "lint", "query", "schema"}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("用法: python3 harness/tools/wiki/wiki_log.py <type> <title> <details>")
        print(f"  type: {', '.join(sorted(VALID_TYPES))}")
        print(f"  title: 操作标题（≥{MIN_TITLE_LEN}字符，说明做了什么）")
        print(f"  details: 具体影响说明（≥{MIN_DETAILS_TOTAL_LEN}字符，多行用 \\n 分隔）")
        print()
        print("示例:")
        print('  python3 wiki_log.py lint "wiki-map 重建（119→191）" "扩展扫描 aigc/docs/ 新增 72 映射\\n歧义 3 项"')
        print('  python3 wiki_log.py schema "system-map 新增构建系统" "关联 build-system.md 等 7 个文件"')
        sys.exit(1)

    log_type = sys.argv[1]
    if log_type not in VALID_TYPES:
        print(f"❌ 无效类型 '{log_type}'，可选: {', '.join(sorted(VALID_TYPES))}")
        sys.exit(1)

    title = sys.argv[2]
    details = sys.argv[3].replace("\\n", "\n")

    try:
        append_wiki_log(log_type, title, details)
        print(f"✅ wiki/log.md 已追加: [{log_type}] {title}")
    except LogQualityError as e:
        print(str(e))
        sys.exit(1)
