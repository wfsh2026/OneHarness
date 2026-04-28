from __future__ import annotations

from pathlib import Path

from oneharness_config import config_list, load_simple_yaml, rel_path, repo_path
from oneharness_markdown import markdown_files


def wiki_pages_from_index(repo_root: Path, index_file: Path) -> tuple[list[Path], list[str]]:
    index_config = load_simple_yaml(index_file)
    exclude_names = config_list(index_config, "exclude")
    errors = []
    pages = []

    for watch in config_list(index_config, "watch"):
        base = repo_path(repo_root, watch)
        if not base.exists():
            errors.append(f"wiki watch 路径不存在: {watch}")
            continue
        pages.extend(markdown_files(base, exclude_names))

    return sorted(set(pages)), errors


def write_wiki_index(repo_root: Path, index_file: Path, pages: list[Path]) -> None:
    index_config = load_simple_yaml(index_file)
    lines = []

    for key in ("watch", "exclude"):
        values = config_list(index_config, key)
        lines.append(f"{key}:")
        for value in values:
            lines.append(f"  - {value}")
        lines.append("")

    lines.append("pages:")
    for page in sorted(rel_path(repo_root, path) for path in pages):
        lines.append(f"  - {page}")

    index_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
