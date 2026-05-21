from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "tharness.py"

sys.path.insert(0, str(ROOT / "tools"))
from tharness_checks import missing_gitignore_patterns, session_role_marker_errors


class TharnessCliTests(unittest.TestCase):
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

    def test_gate_command_is_removed(self) -> None:
        result = self.run_cli("gate")
        self.assertEqual(result.returncode, 2)
        self.assertIn("可用命令: doctor, index, check, self-check", result.stderr)

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
        result = self.run_cli("self-check", "--path", "AIGC\\wiki\\architecture\\role-system.md", "--delivery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("python tools\\tharness.py index --check", result.stdout)
        self.assertIn("python tools\\tharness.py check", result.stdout)

    def test_self_check_plans_tool_commands(self) -> None:
        result = self.run_cli("self-check", "--path", "tools\\tharness.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("python tools\\tharness.py check", result.stdout)
        self.assertIn("python -m unittest tools.test_tharness", result.stdout)

    def test_game_design_methodology_is_routable_from_roles(self) -> None:
        role_index = (ROOT / "AIGC/roles/role-manager/game-design/INDEX.md").read_text(encoding="utf-8")
        methodology = (ROOT / "AIGC/roles/role-manager/game-design/methodology.md").read_text(encoding="utf-8")
        method_index = (ROOT / "AIGC/roles/role-manager/game-design/method-cards/INDEX.md").read_text(encoding="utf-8")

        self.assertIn("methodology.md", role_index)
        self.assertIn("templates/game-design-plan.md", role_index)
        self.assertIn("method-cards/INDEX.md", methodology)
        self.assertIn("design-and-maintenance.md", method_index)
        self.assertIn("phase-index.md", method_index)
        self.assertIn("trigger-index.md", method_index)

    def test_current_config_does_not_reference_workflows_directory(self) -> None:
        config_text = (ROOT / "AIGC/tharness.yaml").read_text(encoding="utf-8")

        self.assertNotIn("AIGC/workflows", config_text)

    def test_missing_gitignore_patterns_detects_invalid_project_adapter_setup(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / ".gitignore").write_text("_sources/\n", encoding="utf-8")

            missing = missing_gitignore_patterns(repo_root, ["AIGC/project-adapters/"])

            self.assertEqual(missing, ["AIGC/project-adapters/"])

    def test_missing_gitignore_patterns_accepts_project_adapter_setup(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / ".gitignore").write_text("_sources/\nAIGC/project-adapters/\n", encoding="utf-8")

            missing = missing_gitignore_patterns(repo_root, ["AIGC/project-adapters/"])

            self.assertEqual(missing, [])

    def test_session_role_marker_detects_missing_fallback_role(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            role_file = repo_root / "session-visible-state.md"
            role_file.write_text("【当前角色】\n【主要职责】\n【工作依据】\n【详细内容】\n", encoding="utf-8")
            config = {
                "session_role_marker_file": "session-visible-state.md",
                "session_role_required_fields": ["【当前角色】", "【主要职责】", "【工作依据】", "【详细内容】"],
                "session_role_fallback_name": "角色管理员",
            }

            errors = session_role_marker_errors(repo_root, config)

            self.assertIn("会话角色标识兜底角色缺失: session-visible-state.md -> 角色管理员", errors)

    def test_session_role_marker_detects_missing_allowed_role(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            role_file = repo_root / "session-visible-state.md"
            role_file.write_text("【当前角色】角色管理员\n【主要职责】\n【工作依据】\n【详细内容】\n", encoding="utf-8")
            config = {
                "session_role_marker_file": "session-visible-state.md",
                "session_role_allowed_names": ["主程 / 开发协调员"],
                "session_role_fallback_name": "角色管理员",
            }

            errors = session_role_marker_errors(repo_root, config)

            self.assertIn("会话角色标识允许角色缺失: session-visible-state.md -> 主程 / 开发协调员", errors)

    def test_session_role_marker_rejects_execution_role_as_visible_role(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            role_file = repo_root / "session-visible-state.md"
            role_file.write_text("【当前角色】Tharness 能力维护员\n【主要职责】\n【工作依据】\n【详细内容】\n", encoding="utf-8")
            config = {
                "session_role_marker_file": "session-visible-state.md",
                "session_role_forbidden_current_role_names": ["Tharness 能力维护员"],
            }

            errors = session_role_marker_errors(repo_root, config)

            self.assertIn("会话角色标识禁止主会话角色: session-visible-state.md -> Tharness 能力维护员", errors)

    def test_session_role_marker_detects_missing_required_statement(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            role_file = repo_root / "session-visible-state.md"
            role_file.write_text("【当前角色】角色管理员\n【主要职责】\n【工作依据】\n【详细内容】\n", encoding="utf-8")
            config = {
                "session_role_marker_file": "session-visible-state.md",
                "session_role_required_statements": ["禁止使用旧 AIGC 三段式作为 Tharness 当前会话的固定回复格式"],
            }

            errors = session_role_marker_errors(repo_root, config)

            self.assertIn(
                "会话角色标识关键约束缺失: session-visible-state.md -> 禁止使用旧 AIGC 三段式作为 Tharness 当前会话的固定回复格式",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
