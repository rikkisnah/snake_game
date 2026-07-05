#ai-assisted with OCA/OpenAI Model with human supervision

"""Regression tests for scripts/score_architecture.py."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "score_architecture.py"
SPEC = importlib.util.spec_from_file_location("score_architecture", SCRIPT_PATH)
assert SPEC is not None
score_architecture = importlib.util.module_from_spec(SPEC)
sys.modules["score_architecture"] = score_architecture
assert SPEC.loader is not None
SPEC.loader.exec_module(score_architecture)


DISCLOSURE = "#ai-assisted with OCA/OpenAI Model with human supervision"
DISCLOSURE_MD = "<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->"


class ScoreArchitectureTests(unittest.TestCase):
    """Scorecard policy regression tests."""

    def test_current_repo_scores_cleanly(self) -> None:
        repo = Path(__file__).resolve().parents[1]

        results = score_architecture.run_scorecard(repo)

        self.assertTrue(results)
        self.assertTrue(all(result.score == 10 for result in results), results)

    def test_agents_line_limit_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "AGENTS.md").write_text("\n".join(["line"] * 210), encoding="utf-8")

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("under 200" in violation for violation in result.violations))

    def test_claude_symlink_requirement_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp), symlink=False)

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("CLAUDE.md" in violation for violation in result.violations))

    def test_validate_must_include_score_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "Makefile").write_text(
                f"{DISCLOSURE}\nscore-gate:\n\tpython3 scripts/score_architecture.py --min-score 10\nvalidate: check\n",
                encoding="utf-8",
            )

            result = score_architecture.score_build_and_tooling(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("validate target" in violation for violation in result.violations))

    def test_score_gate_requires_ten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            makefile = (repo / "Makefile").read_text(encoding="utf-8").replace("--min-score 10", "--min-score 8")
            (repo / "Makefile").write_text(makefile, encoding="utf-8")

            result = score_architecture.score_build_and_tooling(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("--min-score 10" in violation for violation in result.violations))

    def test_missing_required_docs_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "README.md").unlink()

            result = score_architecture.score_documentation_accuracy(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("README.md" in violation for violation in result.violations))

    def test_missing_clean_code_guide_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "docs/agent/clean-code-guide.md").unlink()

            result = score_architecture.score_documentation_accuracy(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("clean-code-guide" in violation for violation in result.violations))

    def test_missing_subagents_guide_lowers_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "docs/agent/subagents-guide.md").unlink()

            docs_result = score_architecture.score_documentation_accuracy(repo)
            review_result = score_architecture.score_agentic_reviewability(repo)

        self.assertLess(docs_result.score, 10)
        self.assertLess(review_result.score, 10)
        self.assertTrue(any("subagents-guide" in violation for violation in docs_result.violations))
        self.assertTrue(any("subagents guide" in violation for violation in review_result.violations))

    def test_agents_must_link_to_clean_code_guide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            agents = (repo / "AGENTS.md").read_text(encoding="utf-8").replace(
                "docs/agent/clean-code-guide.md",
                "docs/agent/missing.md",
            )
            (repo / "AGENTS.md").write_text(agents, encoding="utf-8")

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)

    def test_agents_must_link_to_subagents_guide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            agents = (repo / "AGENTS.md").read_text(encoding="utf-8").replace(
                "docs/agent/subagents-guide.md",
                "docs/agent/missing-subagents.md",
            )
            (repo / "AGENTS.md").write_text(agents, encoding="utf-8")

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("subagents-guide" in violation for violation in result.violations))

    def test_agents_must_include_skill_aware_subagent_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            # The top-level agent contract must mention skill-driven delegation directly.
            agents = (repo / "AGENTS.md").read_text(encoding="utf-8").replace(
                "Apply this rule during skill-driven work as well as ordinary repo work.",
                "",
            )
            (repo / "AGENTS.md").write_text(agents, encoding="utf-8")

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("skill-driven work" in violation for violation in result.violations))

    def test_agents_must_include_subagent_decision_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            agents = (repo / "AGENTS.md").read_text(encoding="utf-8").replace(
                "Use a subagent when the task can be done independently and its result can be summarized compactly.",
                "",
            )
            (repo / "AGENTS.md").write_text(agents, encoding="utf-8")

            result = score_architecture.score_instruction_parity(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("summarized compactly" in violation for violation in result.violations))

    def test_missing_scorecard_tests_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "tests/test_score_architecture.py").unlink()

            result = score_architecture.score_test_quality(repo)

        self.assertLess(result.score, 10)

    def test_missing_type_or_public_contract_signals_lower_score_where_applicable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            source = repo / "src/example.py"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"{DISCLOSURE}\n\ndef public_function():\n    return 1\n", encoding="utf-8")

            result = score_architecture.score_type_or_contract_safety(repo)

        if score_architecture.LANGUAGE == "python":
            self.assertLess(result.score, 10)
        else:
            self.assertTrue(result.score <= 10)

    def test_generic_public_helper_names_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            source = repo / "src/bad_names.py"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"{DISCLOSURE}\n\ndef helper() -> None:\n    return None\n", encoding="utf-8")

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_long_functions_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            body = "\n".join("    value = 1" for _ in range(55))
            (repo / "src/long_func.py").write_text(
                f"{DISCLOSURE}\n\ndef long_function() -> None:\n{body}\n",
                encoding="utf-8",
            )

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_bare_except_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "src/bare_except.py").write_text(
                f"{DISCLOSURE}\n\ndef run() -> None:\n    try:\n        risky()\n    except:\n        raise\n",
                encoding="utf-8",
            )

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_swallowed_errors_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "src/swallowed.py").write_text(
                f"{DISCLOSURE}\n\ndef run() -> None:\n    try:\n        risky()\n    except Exception:\n        pass\n",
                encoding="utf-8",
            )

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_hidden_side_effects_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "src/hidden.py").write_text(
                f"{DISCLOSURE}\n\ndef calculate_total() -> None:\n    open('out.txt', 'w').write('x')\n",
                encoding="utf-8",
            )

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_utils_dumping_ground_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            helpers = "\n".join(f"def public_{index}() -> None:\n    return None\n" for index in range(6))
            (repo / "src/utils.py").write_text(f"{DISCLOSURE}\n\n{helpers}", encoding="utf-8")

            result = score_architecture.score_clean_code(repo)

        self.assertLess(result.score, 10)

    def test_missing_behavior_tests_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "tests").rename(repo / "tests-moved")

            result = score_architecture.score_test_quality(repo)

        self.assertLess(result.score, 10)

    def test_duplicate_public_helpers_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "src/a.py").write_text(f"{DISCLOSURE}\n\ndef duplicate() -> None:\n    return None\n", encoding="utf-8")
            (repo / "src/b.py").write_text(f"{DISCLOSURE}\n\ndef duplicate() -> None:\n    return None\n", encoding="utf-8")

            result = score_architecture.score_duplication(repo)

        self.assertLess(result.score, 10)

    def test_secret_patterns_lower_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "README.md").write_text(
                f"{DISCLOSURE_MD}\n\napi_key = 'abcdef1234567890abcdef'\n",
                encoding="utf-8",
            )

            result = score_architecture.score_secret_safety(repo)

        self.assertLess(result.score, 10)

    def test_committed_env_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / ".env").write_text("TOKEN=<token>\n", encoding="utf-8")

            result = score_architecture.score_secret_safety(repo)

        self.assertLess(result.score, 10)

    def test_context_too_large_lowers_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "CONTEXT.md").write_text(DISCLOSURE_MD + "\n" + "\n".join("line" for _ in range(70)), encoding="utf-8")

            result = score_architecture.score_context_governance(repo)

        self.assertLess(result.score, 10)

    def test_oca_openai_disclosure_header_rule_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "README.md").write_text("# Missing header\n", encoding="utf-8")

            result = score_architecture.score_disclosure_headers(repo)

        self.assertLess(result.score, 10)

    def test_all_generated_markdown_requires_disclosure_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "docs/agent/review-guide.md").write_text("# Missing header\n", encoding="utf-8")

            result = score_architecture.score_disclosure_headers(repo)

        self.assertLess(result.score, 10)

    def test_incomplete_subagents_guide_lowers_reviewability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._clean_repo(Path(tmp))
            (repo / "docs/agent/subagents-guide.md").write_text(
                f"{DISCLOSURE_MD}\n# Subagents Guide\n\nUse subagents.\n",
                encoding="utf-8",
            )

            result = score_architecture.score_agentic_reviewability(repo)

        self.assertLess(result.score, 10)
        self.assertTrue(any("Codex" in violation for violation in result.violations))

    def _clean_repo(self, repo: Path, *, symlink: bool = True) -> Path:
        for path in (
            "docs/agent",
            "docs/adr",
            "scripts",
            "tests",
            "src",
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)

        files = {
            "README.md": self._readme(),
            "AGENTS.md": self._agents(),
            "MEMORY.md": self._memory(),
            "CONTEXT.md": self._context(),
            "Makefile": self._makefile(),
            "scripts/score_architecture.py": f"{DISCLOSURE}\n",
            "tests/test_score_architecture.py": self._score_tests_text(),
            "docs/agent/clean-code-guide.md": self._clean_code(),
            "docs/agent/review-guide.md": self._review(),
            "docs/agent/subagents-guide.md": self._subagents(),
            "docs/agent/testing-guide.md": f"{DISCLOSURE_MD}\n# Testing Guide\n",
            f"docs/agent/{score_architecture.LANGUAGE}-style-guide.md": f"{DISCLOSURE_MD}\n# Style Guide\n",
            "docs/adr/template.md": f"{DISCLOSURE_MD}\n# ADR-NNNN: Title\n",
            "CREATE-PR.md": self._create_pr(),
            "DEVELOP.md": f"{DISCLOSURE_MD}\n# Develop\n\nDocumentation drift is a bug.\n",
        }
        if score_architecture.RUNTIME_TYPE in {"library", "cli", "api", "webapp", "service"}:
            files["INSTALL.md"] = f"{DISCLOSURE_MD}\n# Install\n"
        if score_architecture.RUNTIME_TYPE in {"api", "webapp", "service"}:
            files["DEPLOY.md"] = f"{DISCLOSURE_MD}\n# Deploy\n"

        for relative_path, content in files.items():
            path = repo / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        if symlink:
            os.symlink("AGENTS.md", repo / "CLAUDE.md")
        else:
            (repo / "CLAUDE.md").write_text("not a symlink\n", encoding="utf-8")
        return repo

    def _readme(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# Repo\n\n"
            "make setup\nmake format\nmake test\nmake lint\nmake score\nmake validate\n"
            "AGENTS.md\nMEMORY.md\nCONTEXT.md\ndocs/agent/\n"
        )

    def _agents(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# Agents\n\n"
            "Runtime: library\n"
            "CLAUDE.md must be a symlink\n"
            "docs/agent/clean-code-guide.md\n"
            "docs/agent/review-guide.md\n"
            "docs/agent/subagents-guide.md\n"
            "docs/agent/testing-guide.md\n"
            "Documentation drift is a bug\n"
            "Never write secrets\n"
            "Use subagents where applicable\n"
            "Apply this rule during skill-driven work as well as ordinary repo work.\n"
            "clear ownership, expected output, constraints, and validation expectations\n"
            "primary agent remains responsible\n"
        )

    def _memory(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# Memory\n\n"
            "## Project Context\n## Stable Facts\n## Decisions\n## Assumptions\n"
            "## Constraints\n## Proposals\n## Do Not Store Here\n"
            "not the source of truth\n"
        )

    def _context(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# CONTEXT.md\n\n"
            "Temporary working context.\n"
            "Do not merge real working notes into main or master.\n"
        )

    def _makefile(self) -> str:
        return (
            f"{DISCLOSURE}\n"
            "help:\n\t@echo help\n"
            "setup:\n\t@echo setup\n"
            "format:\n\t@echo format\n"
            "test:\n\t@echo test\n"
            "test-%:\n\t@echo test\n"
            "lint:\n\t@echo lint\n"
            "score:\n\tpython3 scripts/score_architecture.py\n"
            "score-gate:\n\tpython3 scripts/score_architecture.py --min-score 10\n"
            "check: lint test\n"
            "validate: check score-gate\n"
            "clean:\n\t@echo clean\n"
            "clean-env:\n\t@echo clean-env\n"
        )

    def _score_tests_text(self) -> str:
        return (
            f"{DISCLOSURE}\n"
            "def test_current_repo_scores_cleanly(): pass\n"
            "def test_agents_line_limit_is_enforced(): pass\n"
            "def test_claude_symlink_requirement_is_enforced(): pass\n"
            "def test_secret_patterns_lower_score(): pass\n"
            "def test_clean_code_violations_lower_score(): pass\n"
        )

    def _clean_code(self) -> str:
        return f"{DISCLOSURE_MD}\n# Clean Code Guide\n\n## Required Explanations\n"

    def _review(self) -> str:
        return f"{DISCLOSURE_MD}\n# Review Guide\n\nDocumentation drift is a bug.\n"

    def _subagents(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# Subagents Guide\n\n"
            "Claude Task delegation.\n"
            "Codex spawn_agent delegation.\n"
            "parallelizable work.\n"
            "independent review.\n"
            "disjoint write scopes.\n"
        )

    def _create_pr(self) -> str:
        return (
            f"{DISCLOSURE_MD}\n# Create PR\n\n"
            "git status --short\nmake validate\nDo not push\nrisks\n"
        )


if __name__ == "__main__":
    unittest.main()
