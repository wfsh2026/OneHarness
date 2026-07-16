from __future__ import annotations

import subprocess
import sys

from tharness_config import config_list


def normalize_path(path_value: str) -> str:
    return path_value.replace("\\", "/").lstrip("./").lower()


def split_self_check_rule(rule: str) -> tuple[str, str]:
    if "|" not in rule:
        raise ValueError(f"无法解析自检规则: {rule}")
    prefix, command = rule.split("|", 1)
    prefix = normalize_path(prefix.strip()).rstrip("/")
    command = command.strip()
    if not prefix or not command:
        raise ValueError(f"自检规则缺少路径或命令: {rule}")
    return prefix, command


def _current_python_command(python_executable: str | None = None) -> str:
    return subprocess.list2cmdline([python_executable or sys.executable])


def _bind_python(command: str, python_executable: str | None = None) -> str:
    if command == "python":
        return _current_python_command(python_executable)
    if command.startswith("python "):
        return f"{_current_python_command(python_executable)}{command[len('python'):]}"
    return command


def plan_self_check_commands(
    config: dict,
    changed_paths: list[str],
    include_delivery: bool,
    python_executable: str | None = None,
) -> list[str]:
    commands = []
    normalized_paths = [normalize_path(path) for path in changed_paths]

    for rule in config_list(config, "self_check_path_rules"):
        prefix, command = split_self_check_rule(rule)
        for path in normalized_paths:
            if path == prefix or path.startswith(prefix + "/"):
                commands.append(_bind_python(command, python_executable))
                break

    if include_delivery:
        commands.extend(_bind_python(command, python_executable) for command in config_list(config, "self_check_delivery_commands"))

    deduped = []
    for command in commands:
        if command and command not in deduped:
            deduped.append(command)
    return deduped
