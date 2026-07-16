from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = ROOT / "tools" / "version-feature-scan" / "version_feature_scan.py"
SPEC = importlib.util.spec_from_file_location("version_feature_scan", SCANNER_PATH)
assert SPEC and SPEC.loader
scanner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scanner
SPEC.loader.exec_module(scanner)


class VersionFeatureScanTests(unittest.TestCase):
    def test_utf8_stream_configuration_is_safe_and_explicit(self) -> None:
        class ConfigurableStream:
            def __init__(self) -> None:
                self.calls = []

            def reconfigure(self, **kwargs) -> None:
                self.calls.append(kwargs)

        configurable = ConfigurableStream()
        scanner.configure_utf8_streams([configurable, io.StringIO()])

        self.assertEqual(configurable.calls, [{"encoding": "utf-8", "errors": "replace"}])

    def fake_git(self, repo: Path, args: list[str], allow_fail: bool = False, timeout: float = 60.0) -> str:
        if args[:2] == ["rev-parse", "--is-inside-work-tree"]:
            return "true"
        if args[:2] == ["rev-parse", "--verify"]:
            if "missing-ref" in args[2]:
                raise RuntimeError("git rev-parse failed: missing-ref")
            return "a" * 40
        if args[0] == "merge-base":
            return "b" * 40
        if args[0] == "show":
            return "renamed.txt\nbinary.dat"
        if args[0] == "diff" and "--stat" in args:
            return "renamed.txt | 1 +\nbinary.dat | Bin 0 -> 3 bytes"
        if args[0] == "diff" and "--name-status" in args:
            return "R100\told-name.txt\trenamed.txt\nA\tbinary.dat"
        if args[0] == "log" and "^1.." in args[-2]:
            return "新增背包容量"
        if args[0] == "log" and "--merges" in args:
            return "c" * 40 + "\t2026-07-15\tTester\tMerge branch 'feature/v1/inventory'"
        if args[0] == "log":
            return "c" * 40 + "\t2026-07-15\tTester\tMerge branch 'feature/v1/inventory'"
        raise AssertionError(f"unexpected git args: {args}")

    def empty_git(self, repo: Path, args: list[str], allow_fail: bool = False, timeout: float = 60.0) -> str:
        if args[:2] == ["rev-parse", "--is-inside-work-tree"]:
            return "true"
        if args[:2] == ["rev-parse", "--verify"] or args[0] == "merge-base":
            return "a" * 40
        if args[0] in {"log", "diff"}:
            return ""
        raise AssertionError(f"unexpected git args: {args}")

    def run_main(self, repo: Path, output: Path, *extra: str, target: str = "HEAD", git_impl=None) -> tuple[int, str]:
        argv = [
            str(SCANNER_PATH),
            "--repo", str(repo),
            "--base", "base-version",
            "--target", target,
            "--version", "v1",
            "--output", str(output),
            "--detail-root", str(output.parent / "details"),
            *extra,
        ]
        stdout = io.StringIO()
        with patch.object(scanner, "run_git", side_effect=git_impl or self.fake_git), patch.object(sys, "argv", argv), redirect_stdout(stdout):
            return scanner.main(), stdout.getvalue()

    def test_dry_run_validates_merge_rename_and_binary_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "仓库"
            repo.mkdir()
            output = root / "out" / "功能目录审核.md"
            code, stdout = self.run_main(repo, output, "--dry-run")

            self.assertEqual(code, 0, stdout)
            self.assertIn("mode: dry-run", stdout)
            self.assertIn("merges=1", stdout)
            self.assertFalse(output.exists())
            self.assertFalse((output.parent / "git-evidence").exists())

    def test_write_generates_document_and_structured_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "仓库"
            repo.mkdir()
            output = root / "out" / "功能目录审核.md"
            code, stdout = self.run_main(repo, output)

            self.assertEqual(code, 0, stdout)
            summary = json.loads((output.parent / "git-evidence" / "scan-summary.json").read_text(encoding="utf-8"))
            self.assertTrue(output.exists())
            self.assertEqual(summary["status"], "ok")
            self.assertEqual(summary["repositories"][0]["merge_count"], 1)
            self.assertIn("renamed.txt", summary["repositories"][0]["changed_files"])
            self.assertIn("binary.dat", summary["repositories"][0]["changed_files"])
            self.assertTrue(summary["features"][0]["evidence"]["merge_commits"])
            self.assertEqual(summary["features"][0]["confidence"], "high")

    def test_empty_range_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            output = root / "out" / "review.md"
            code, stdout = self.run_main(repo, output, git_impl=self.empty_git)

            self.assertEqual(code, 0, stdout)
            summary = json.loads((output.parent / "git-evidence" / "scan-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["repositories"][0]["commit_count"], 0)
            self.assertEqual(summary["features"], [])

    def test_invalid_ref_fails_before_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            output = root / "out" / "review.md"
            code, stdout = self.run_main(repo, output, target="missing-ref")

            self.assertEqual(code, 2)
            self.assertIn("missing-ref", stdout)
            self.assertFalse(output.parent.exists())

    def test_output_conflict_and_duplicate_repo_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            output = root / "occupied"
            output.mkdir()
            conflict_code, conflict_stdout = self.run_main(repo, output)
            duplicate_code, duplicate_stdout = self.run_main(repo, root / "result.md", "--repo", str(repo))

            self.assertEqual(conflict_code, 2)
            self.assertIn("输出路径是目录", conflict_stdout)
            self.assertEqual(duplicate_code, 2)
            self.assertIn("重复仓库路径", duplicate_stdout)

    def test_git_timeout_becomes_clear_runtime_error(self) -> None:
        with patch.object(scanner.subprocess, "run", side_effect=subprocess.TimeoutExpired(["git"], 1)):
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                scanner.run_git(Path("repo"), ["status"], timeout=1)


if __name__ == "__main__":
    unittest.main()
