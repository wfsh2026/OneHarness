from __future__ import annotations

from pathlib import Path

from oneharness_config import clean_value


def parse_front_matter(path: Path) -> dict | None:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return None

    fields = {}
    for line in lines[1:end_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        fields[key.strip()] = clean_value(value.strip())

    return fields


def missing_front_matter_fields(fields: dict | None, required: list[str], allow_empty: list[str]) -> list[str]:
    if fields is None:
        return required

    missing = []
    for field in required:
        value = str(fields.get(field, "")).strip()
        if field not in fields:
            missing.append(field)
        elif not value and field not in allow_empty:
            missing.append(field)
    return missing


def is_excluded(path: Path, base: Path, exclude_names: list[str]) -> bool:
    rel = path.relative_to(base).as_posix()
    parts = set(path.relative_to(base).parts)

    for item in exclude_names:
        normalized = item.replace("\\", "/").rstrip("/")
        if path.name == normalized or normalized in parts:
            return True
        if rel == normalized or rel.startswith(normalized + "/"):
            return True
    return False


def markdown_files(base: Path, exclude_names: list[str]) -> list[Path]:
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.md")
        if path.is_file() and not is_excluded(path, base, exclude_names)
    )
