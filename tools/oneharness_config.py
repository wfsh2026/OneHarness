from __future__ import annotations

from pathlib import Path


DEFAULT_CONFIG = "AIGC/oneharness.yaml"


def clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_simple_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    data = {}
    current_key = None

    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            if current_key is None:
                raise ValueError(f"列表项缺少所属字段: {path}")
            data.setdefault(current_key, []).append(clean_value(stripped[2:]))
            continue

        if raw_line.startswith(" "):
            raise ValueError(f"不支持嵌套配置: {path}: {raw_line}")

        if ":" not in stripped:
            raise ValueError(f"无法解析配置行: {path}: {raw_line}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not value:
            data[key] = []
            current_key = key
        else:
            data[key] = clean_value(value)
            current_key = None

    return data


def config_list(config: dict, key: str) -> list[str]:
    value = config.get(key, [])
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def config_value(config: dict, key: str) -> str:
    value = config.get(key)
    if value is None or isinstance(value, list):
        return ""
    return str(value)


def repo_path(repo_root: Path, path_value: str) -> Path:
    return repo_root / Path(path_value)


def rel_path(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()
