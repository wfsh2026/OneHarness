from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "tharness.py"

sys.path.insert(0, str(ROOT / "tools"))
from tharness_checks import missing_gitignore_patterns, registry_consistency_errors, session_role_marker_errors, version_consistency_errors
from tharness_behavior import removed_role_reference_errors, tool_contract_errors


class TharnessCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
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
        self.assertIn("可用命令: doctor, index, registry, check, eval, self-check, project, roles-ui", result.stderr)

    def test_missing_config_fails(self) -> None:
        result = self.run_cli("doctor", "--config", "aigc/missing.yaml")
        self.assertEqual(result.returncode, 2)
        self.assertIn("配置文件不存在", result.stderr)

    def test_doctor_passes_current_repo(self) -> None:
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("doctor: PASS", result.stdout)

    def test_check_resolves_root_from_entry_script(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CLI), "check"],
            cwd=ROOT.parent,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("check: PASS", result.stdout)

    def test_project_start_can_use_external_root_without_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_cli("project", "start", "--root", temp_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("project-start: PASS", result.stdout)
        self.assertIn("manifest: not found; using transient startup", result.stdout)
        self.assertIn(str(ROOT), result.stdout)

    def test_project_init_creates_lightweight_anchor_without_copying_framework(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_cli("project", "init", "--root", temp_dir)
            project_root = Path(temp_dir)
            anchor = project_root / ".tharness"

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((anchor / "project.yaml").exists())
            self.assertTrue((anchor / "start.ps1").exists())
            self.assertTrue((anchor / "start.cmd").exists())
            self.assertTrue((project_root / "AGENTS.md").exists())
            self.assertFalse((project_root / "AIGC").exists())
            self.assertIn(str(ROOT), (anchor / "project.yaml").read_text(encoding="utf-8"))
            agents_text = (project_root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(str(ROOT / "AGENTS.md"), agents_text)
            self.assertIn(str(ROOT / "AIGC" / "INDEX.md"), agents_text)

            start_result = self.run_cli("project", "start", "--root", temp_dir)

        self.assertEqual(start_result.returncode, 0, start_result.stdout + start_result.stderr)
        self.assertIn("manifest: found", start_result.stdout)
        self.assertIn("write-policy:", start_result.stdout)

    def test_project_init_refuses_to_overwrite_changed_anchor_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = self.run_cli("project", "init", "--root", temp_dir)
            anchor_readme = Path(temp_dir) / ".tharness" / "README.md"
            anchor_readme.write_text("local edit\n", encoding="utf-8")

            second = self.run_cli("project", "init", "--root", temp_dir)
            forced = self.run_cli("project", "init", "--root", temp_dir, "--force")

        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 2)
        self.assertIn("--force", second.stderr)
        self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)

    def test_project_init_merges_agents_bridge_without_removing_existing_rules(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            agents_path = project_root / "AGENTS.md"
            agents_path.write_text("# Project Rules\n\nKeep local notes.\n", encoding="utf-8")

            first = self.run_cli("project", "init", "--root", temp_dir)
            first_text = agents_path.read_text(encoding="utf-8")
            second = self.run_cli("project", "init", "--root", temp_dir)
            second_text = agents_path.read_text(encoding="utf-8")

        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertIn("# Project Rules", first_text)
        self.assertIn("Keep local notes.", first_text)
        self.assertIn("THARNESS_BINDING_START", first_text)
        self.assertIn(str(ROOT / "AIGC" / "INDEX.md"), first_text)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first_text, second_text)

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
        result = self.run_cli("self-check", "--path", "aigc\\wiki\\architecture\\role-system.md", "--delivery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"{sys.executable} tools\\tharness.py index --check", result.stdout)
        self.assertIn(f"{sys.executable} tools\\tharness.py check", result.stdout)

    def test_self_check_plans_tool_commands(self) -> None:
        result = self.run_cli("self-check", "--path", "tools\\tharness.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"{sys.executable} tools\\tharness.py check", result.stdout)
        self.assertIn(f"{sys.executable} -m unittest tools.test_tharness", result.stdout)

    def test_registry_consistency_detects_half_integrated_role_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "aigc/roles/known/skills").mkdir(parents=True)
            (root / "aigc/roles/known/tools").mkdir(parents=True)
            (root / "aigc/roles/unknown").mkdir(parents=True)
            (root / "aigc/roles/role-manager/role-routing").mkdir(parents=True)
            (root / "aigc/capabilities").mkdir(parents=True)
            (root / "aigc/roles/known/RULE.md").write_text("# Known\n", encoding="utf-8")
            (root / "aigc/roles/known/skills/INDEX.md").write_text("# Skills\n", encoding="utf-8")
            (root / "aigc/roles/known/tools/INDEX.md").write_text("# Tools\n", encoding="utf-8")
            (root / "aigc/roles/unknown/RULE.md").write_text("# Unknown\n", encoding="utf-8")
            route = root / "aigc/roles/role-manager/role-routing/known.md"
            route.write_text("# Known Role\n", encoding="utf-8")
            (root / "aigc/roles/role-manager/role-routing/INDEX.md").write_text("| Known Role | `known.md` |\n", encoding="utf-8")
            (root / "aigc/roles/INDEX.md").write_text("| Known Role | `known/RULE.md` |\n", encoding="utf-8")
            (root / "aigc/capabilities/INDEX.md").write_text("| `known-cap` | Known |\n", encoding="utf-8")
            (root / "aigc/capabilities/registry.yaml").write_text(
                "schema_version: 2\n"
                "role_registry:\n"
                "  - known|Known Role|AIGC/roles/known/RULE.md|AIGC/roles/role-manager/role-routing/known.md|known-cap|dispatchable|tested|known|tested|core|-\n"
                "capability_registry:\n"
                "  - known-cap|AIGC/roles/known/RULE.md|known|tested|tested|2026-07-16|core|-\n",
                encoding="utf-8",
            )
            required = [
                "AIGC/roles/known/RULE.md",
                "AIGC/roles/known/skills/INDEX.md",
                "AIGC/roles/known/tools/INDEX.md",
                "AIGC/roles/role-manager/role-routing/known.md",
                "AIGC/capabilities/registry.yaml",
            ]
            config = {
                "role_root": "AIGC/roles",
                "role_rule_file_name": "RULE.md",
                "role_index_file": "AIGC/roles/INDEX.md",
                "role_routing_index_file": "AIGC/roles/role-manager/role-routing/INDEX.md",
                "capability_index_file": "AIGC/capabilities/INDEX.md",
                "capability_registry_file": "AIGC/capabilities/registry.yaml",
                "check_required_paths": required,
                "session_role_forbidden_current_role_names": ["Known Role"],
            }

            errors = registry_consistency_errors(root, config)

            self.assertIn("角色目录未登记到机器注册源: unknown", errors)

            (root / "aigc/capabilities/INDEX.md").write_text("| capability_id | name |\n", encoding="utf-8")
            reverse_errors = registry_consistency_errors(root, config)
            self.assertIn("机器注册源能力未登记到能力索引: known-cap", reverse_errors)

    def test_registry_and_behavior_eval_pass_current_repo(self) -> None:
        registry = self.run_cli("registry")
        behavior = self.run_cli("eval")
        self.assertEqual(registry.returncode, 0, registry.stdout + registry.stderr)
        self.assertIn("registry: PASS", registry.stdout)
        self.assertEqual(behavior.returncode, 0, behavior.stdout + behavior.stderr)
        self.assertIn("确定性行为用例: 14", behavior.stdout)

    def test_tool_contract_check_rejects_missing_field(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tools_index = root / "aigc/roles/sample/tools/INDEX.md"
            tools_index.parent.mkdir(parents=True)
            tools_index.write_text(
                "## tool: sample\n"
                "- tool_id: `sample`\n"
                "- purpose: sample\n"
                "- phase: test\n",
                encoding="utf-8",
            )
            errors = tool_contract_errors(root, {"role_root": "AIGC/roles"})
            self.assertIn("工具契约字段缺失: AIGC/roles/sample/tools/INDEX.md -> sample.preconditions", errors)

    def test_version_consistency_rejects_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "aigc/capabilities").mkdir(parents=True)
            (root / "aigc/capabilities/VERSION.md").write_text("current_version: 5.0.0\n", encoding="utf-8")
            (root / "aigc/capabilities/INDEX.md").write_text("当前系统版本：`4.9.0`\n", encoding="utf-8")
            errors = version_consistency_errors(root, {"system_version": "5.0.0", "capability_index_file": "AIGC/capabilities/INDEX.md"})
            self.assertIn("能力索引与 system_version 不一致: 5.0.0", errors)

    def test_removed_role_reference_check_rejects_active_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "aigc/roles/active/RULE.md"
            path.parent.mkdir(parents=True)
            path.write_text("route: intern-ui-developer\n", encoding="utf-8")
            errors = removed_role_reference_errors(root)
            self.assertIn("已删除角色仍被活动入口引用: AIGC/roles/active/RULE.md -> intern-ui-developer", errors)

    def test_old_developer_roles_are_removed_and_domains_are_complete(self) -> None:
        slugs = (
            "intern-engine-architecture-developer",
            "intern-ui-developer",
            "intern-gameplay-systems-developer",
            "intern-combat-developer",
        )
        registry = (ROOT / "aigc/capabilities/registry.yaml").read_text(encoding="utf-8")
        for slug in slugs:
            self.assertFalse((ROOT / "aigc/roles" / slug).exists())
            self.assertFalse((ROOT / "aigc/roles/role-manager/role-routing" / f"{slug}.md").exists())
            self.assertNotIn(slug, registry)
        for domain in ("architecture", "ui", "gameplay", "combat"):
            text = (ROOT / "aigc/roles/project-developer/domains" / f"{domain}.md").read_text(encoding="utf-8")
            for heading in ("## 职责", "## 禁止范围", "## 输入边界", "## 输出边界", "## 验证边界"):
                self.assertIn(heading, text)

    def test_game_design_methodology_is_routable_from_roles(self) -> None:
        role_index = (ROOT / "aigc/roles/role-manager/game-design/INDEX.md").read_text(encoding="utf-8")
        methodology = (ROOT / "aigc/roles/role-manager/game-design/methodology.md").read_text(encoding="utf-8")
        method_index = (ROOT / "aigc/roles/role-manager/game-design/method-cards/INDEX.md").read_text(encoding="utf-8")

        self.assertIn("methodology.md", role_index)
        self.assertIn("templates/game-design-plan.md", role_index)
        self.assertIn("method-cards/INDEX.md", methodology)
        self.assertIn("design-and-maintenance.md", method_index)
        self.assertIn("phase-index.md", method_index)
        self.assertIn("trigger-index.md", method_index)

    def test_current_config_does_not_reference_workflows_directory(self) -> None:
        config_text = (ROOT / "aigc/tharness.yaml").read_text(encoding="utf-8")

        self.assertNotIn("aigc/workflows", config_text)

    def test_missing_gitignore_patterns_detects_missing_required_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / ".gitignore").write_text("_sources/\n", encoding="utf-8")

            missing = missing_gitignore_patterns(repo_root, ["runtime-cache/"])

            self.assertEqual(missing, ["runtime-cache/"])

    def test_missing_gitignore_patterns_accepts_existing_required_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / ".gitignore").write_text("_sources/\nruntime-cache/\n", encoding="utf-8")

            missing = missing_gitignore_patterns(repo_root, ["runtime-cache/"])

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
