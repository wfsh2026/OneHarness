#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from oneharness_checks import run_doctor, run_gate, run_index
from oneharness_config import DEFAULT_CONFIG, config_value, load_simple_yaml, rel_path, repo_path
from oneharness_index import write_wiki_index
from oneharness_self_check import plan_self_check_commands


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
    parser = argparse.ArgumentParser(description="OneHarness 自检工具")
    parser.add_argument("command", nargs="?", help="doctor | index | gate | self-check")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="检查配置文件")
    parser.add_argument("--check", action="store_true", help="index 命令只校验，不输出生成列表")
    parser.add_argument("--write", action="store_true", help="index 命令写回页面清单")
    parser.add_argument("--path", action="append", default=[], help="self-check 命令的变更路径，可重复传入")
    parser.add_argument("--delivery", action="store_true", help="self-check 命令包含交付前门控")
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
        commands = plan_self_check_commands(config, paths, delivery)
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
    args = parse_args(argv)
    if args.command not in {"doctor", "index", "gate", "self-check"}:
        print("错误: 未知命令。可用命令: doctor, index, gate, self-check", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    try:
        config = load_simple_yaml(repo_path(repo_root, args.config))
    except (FileNotFoundError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    try:
        if args.command == "doctor":
            errors, warnings, info = run_doctor(repo_root, config)
            print_report("doctor", errors, warnings, info)
            return 1 if errors else 0

        if args.command == "index":
            return run_index_command(repo_root, config, args.check, args.write)

        if args.command == "self-check":
            return run_self_check_command(config, args.path, args.delivery)

        errors, warnings, info = run_gate(repo_root, config)
        print_report("gate", errors, warnings, info)
        return 1 if errors else 0
    except (FileNotFoundError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
