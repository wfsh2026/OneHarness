from __future__ import annotations

from oneharness_config import config_list


def normalize_path(path_value: str) -> str:
    return path_value.replace("\\", "/").lstrip("./")


def split_self_check_rule(rule: str) -> tuple[str, str]:
    if "|" not in rule:
        raise ValueError(f"无法解析自检规则: {rule}")
    prefix, command = rule.split("|", 1)
    prefix = normalize_path(prefix.strip()).rstrip("/")
    command = command.strip()
    if not prefix or not command:
        raise ValueError(f"自检规则缺少路径或命令: {rule}")
    return prefix, command


def plan_self_check_commands(config: dict, changed_paths: list[str], include_delivery: bool) -> list[str]:
    commands = []
    normalized_paths = [normalize_path(path) for path in changed_paths]

    for rule in config_list(config, "self_check_path_rules"):
        prefix, command = split_self_check_rule(rule)
        for path in normalized_paths:
            if path == prefix or path.startswith(prefix + "/"):
                commands.append(command)
                break

    if include_delivery:
        commands.extend(config_list(config, "self_check_delivery_commands"))

    deduped = []
    for command in commands:
        if command and command not in deduped:
            deduped.append(command)
    return deduped
