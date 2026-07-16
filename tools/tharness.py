#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tharness_checks import run_check, run_doctor, run_index
from tharness_behavior import deterministic_behavior_eval
from tharness_config import DEFAULT_CONFIG, config_value, load_simple_yaml, rel_path, repo_path
from tharness_index import write_wiki_index
from tharness_project import run_project_command
from tharness_roles_ui import run_roles_ui_command
from tharness_self_check import plan_self_check_commands


def print_report(title: str, errors: list[str], warnings: list[str], info: list[str]) -> None:
    status = "PASS" if not errors else "FAIL"
    print(f"{title}: {status}")
    for item in info:
        print(f"INFO  {item}")
    for item in warnings:
        print(f"WARN  {item}")
    for item in errors:
        print(f"ERROR {item}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tharness 自检工具")
    parser.add_argument("command", nargs="?", help="doctor | index | registry | check | eval | self-check | project | roles-ui")
    parser.add_argument("project_command", nargs="?", help="project 子命令: init | start")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="检查配置文件")
    parser.add_argument("--check", action="store_true", help="index 命令只校验，不输出生成列表")
    parser.add_argument("--write", action="store_true", help="index 命令写回页面清单")
    parser.add_argument("--path", action="append", default=[], help="self-check 命令的变更路径，可重复传入")
    parser.add_argument("--delivery", action="store_true", help="self-check 命令包含交付前结构自检")
    parser.add_argument("--root", default=".", help="project 命令的目标项目目录，默认当前目录")
    parser.add_argument("--force", action="store_true", help="project init 覆盖已存在的启动锚点文件")
    parser.add_argument("--no-open", action="store_true", help="roles-ui 启动后不自动打开浏览器")
    parser.add_argument("--port", type=int, default=0, help="roles-ui 监听端口，默认自动选择可用端口")
    return parser.parse_args(argv)


def run_index_command(repo_root: Path, config: dict, check: bool, write: bool) -> int:
    errors, warnings, info, pages = run_index(repo_root, config)
    if write:
        index_file = repo_path(repo_root, config_value(config, "wiki_index_file"))
        write_wiki_index(repo_root, index_file, pages)
        errors, warnings, info, pages = run_index(repo_root, config)
        info.append(f"索引已写入: {rel_path(repo_root, index_file)}")

    print_report("index", errors, warnings, info)
    if not check and not write:
        print("pages:")
        for page in pages:
            print(f"  - {rel_path(repo_root, page)}")
    return 1 if errors else 0


def run_self_check_command(config: dict, paths: list[str], delivery: bool) -> int:
    if not paths and not delivery:
        print("错误: self-check 需要至少一个 --path 或 --delivery", file=sys.stderr)
        return 2

    try:
        commands = plan_self_check_commands(config, paths, delivery, sys.executable)
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    print("self-check: PASS")
    if not commands:
        print("INFO  未命中自检命令")
        return 0

    print("commands:")
    for command in commands:
        print(f"  - {command}")
    return 0


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    args = parse_args(argv)
    if args.command not in {"doctor", "index", "registry", "check", "eval", "self-check", "project", "roles-ui"}:
        print("错误: 未知命令。可用命令: doctor, index, registry, check, eval, self-check, project, roles-ui", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]

    if args.command == "project":
        return run_project_command(repo_root, args.project_command, args.root, args.force)

    try:
        config = load_simple_yaml(repo_path(repo_root, args.config))
    except (FileNotFoundError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    try:
        if args.command == "roles-ui":
            return run_roles_ui_command(repo_root, config, args.port, args.no_open)

        if args.command == "doctor":
            errors, warnings, info = run_doctor(repo_root, config)
            print_report("doctor", errors, warnings, info)
            return 1 if errors else 0

        if args.command == "index":
            return run_index_command(repo_root, config, args.check, args.write)

        if args.command == "self-check":
            return run_self_check_command(config, args.path, args.delivery)

        if args.command == "registry":
            from tharness_checks import registry_consistency_errors
            errors = registry_consistency_errors(repo_root, config)
            print_report("registry", errors, [], ["机器事实源 schema 与衍生索引一致"] if not errors else [])
            return 1 if errors else 0

        if args.command == "eval":
            errors, passed = deterministic_behavior_eval(repo_root, config)
            print_report(
                "eval", errors, [],
                [f"确定性行为用例: {len(passed) + len(errors)}", f"通过: {len(passed)}", "边界: policy contract only; not a model behavior eval"],
            )
            return 1 if errors else 0

        errors, warnings, info = run_check(repo_root, config)
        print_report("check", errors, warnings, info)
        return 1 if errors else 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
