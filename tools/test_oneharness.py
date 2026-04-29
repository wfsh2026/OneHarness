from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "oneharness.py"


class OneHarnessCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_unknown_command_fails(self) -> None:
        result = self.run_cli("unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("未知命令", result.stderr)

    def test_missing_config_fails(self) -> None:
        result = self.run_cli("doctor", "--config", "AIGC/missing.yaml")
        self.assertEqual(result.returncode, 2)
        self.assertIn("配置文件不存在", result.stderr)

    def test_doctor_passes_current_repo(self) -> None:
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("doctor: PASS", result.stdout)

    def test_index_write_passes_current_repo(self) -> None:
        result = self.run_cli("index", "--write")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("index: PASS", result.stdout)
        self.assertIn("索引已写入", result.stdout)

    def test_self_check_requires_path_or_delivery(self) -> None:
        result = self.run_cli("self-check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("至少一个 --path 或 --delivery", result.stderr)

    def test_self_check_plans_wiki_and_delivery_commands(self) -> None:
        result = self.run_cli("self-check", "--path", "AIGC\\wiki\\architecture\\entry-map.md", "--delivery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("python tools\\oneharness.py index --check", result.stdout)
        self.assertIn("python tools\\oneharness.py gate", result.stdout)

    def test_self_check_plans_tool_commands(self) -> None:
        result = self.run_cli("self-check", "--path", "tools\\oneharness.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("python tools\\oneharness.py gate", result.stdout)
        self.assertIn("python -m unittest tools.test_oneharness", result.stdout)

    def test_game_design_methodology_is_routable(self) -> None:
        rules_index = (ROOT / "AIGC/workflows/planning-discussion/rules/INDEX.md").read_text(encoding="utf-8")
        template_index = (ROOT / "AIGC/workflows/planning-discussion/templates/INDEX.md").read_text(encoding="utf-8")
        method_index = (ROOT / "AIGC/workflows/planning-discussion/method-cards/INDEX.md").read_text(encoding="utf-8")

        self.assertIn("game-design-methodology.md", rules_index)
        self.assertIn("game-design-plan.md", template_index)
        self.assertIn("design-and-maintenance.md", method_index)
        self.assertIn("phase-index.md", method_index)
        self.assertIn("trigger-index.md", method_index)


if __name__ == "__main__":
    unittest.main()
