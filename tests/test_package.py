import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


run_evals = load_module("run_evals", "scripts/run_evals.py")


class PackageContractTest(unittest.TestCase):
    def test_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate-package.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_omp_and_pi_extension_manifests_are_declared(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf8"))
        extension = ["./extensions/blunt.ts"]
        self.assertEqual({"extensions": extension}, package["omp"])
        self.assertEqual(
            {"extensions": extension, "skills": ["./skills"]},
            package["pi"],
        )
        self.assertTrue((ROOT / "extensions" / "blunt.ts").is_file())

    def test_skill_remains_explicitly_invoked(self):
        skill = (ROOT / "skills" / "blunt" / "SKILL.md").read_text(encoding="utf8")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertIn("name: blunt", frontmatter)
        self.assertIn("disable-model-invocation: true", frontmatter)

    def test_stop_phrases_agree_across_runtimes(self):
        # "stop blunt mode" and "normal mode" are a cross-runtime contract:
        # the extension, the hooks, the OpenCode plugin, the command file, the
        # skill body, and both INSTALL docs must all agree on the same phrases.
        expectation = {
            "extensions/blunt.ts": [
                '"stop blunt mode": true,',
                '"normal mode": true,',
            ],
            ".opencode/plugins/blunt.mjs": ['"stop blunt mode" or "normal mode"'],
            ".opencode/command/blunt.md": ['"stop blunt mode" or "normal mode"'],
            "skills/blunt/SKILL.md": ["stop blunt mode", "normal mode"],
        }
        for relative, markers in expectation.items():
            text = (ROOT / relative).read_text(encoding="utf8")
            for marker in markers:
                self.assertIn(marker, (ROOT / relative).read_text(encoding="utf8"),
                              f"{relative} lost the toggle phrase: {marker}")

    def test_codex_policy_disables_implicit_invocation(self):
        text = (ROOT / "skills" / "blunt" / "agents" / "openai.yaml").read_text(
            encoding="utf8"
        )
        self.assertIn("allow_implicit_invocation: false", text)

    def test_gemini_command_passes_args_through(self):
        toml = (ROOT / "skills" / "blunt" / "agents" / "gemini.toml").read_text(
            encoding="utf8"
        )
        self.assertIn("{{args}}", toml)

    def test_all_runtime_files_reference_the_canonical_skill(self):
        markers = {
            "extensions/blunt.ts": '"SKILL.md",',
            "hooks/always-on.mjs": '"skills", "blunt", "SKILL.md"',
            "hooks/always-on.sh": "skills/blunt/SKILL.md",
            "hooks/always-on.ps1": "../skills/blunt/SKILL.md",
            ".opencode/plugins/blunt.mjs": "'blunt', 'SKILL.md'",
            "GEMINI.md": "@./skills/blunt/SKILL.md",
        }
        for relative, marker in markers.items():
            text = (ROOT / relative).read_text(encoding="utf8")
            self.assertIn(marker, text, f"{relative} must reference the canonical skill")


class EvalAssetsTest(unittest.TestCase):
    def test_cases_validate(self):
        cases = run_evals.load_cases(ROOT / "evals" / "cases.jsonl")
        errors = run_evals.validate_cases(cases)
        self.assertEqual([], errors)

    def test_runner_config_is_well_formed(self):
        config = json.loads((ROOT / "evals" / "runners.json").read_text(encoding="utf8"))
        known_formats = {"text", "claude-json", "codex-jsonl"}
        for name, runner in config.items():
            self.assertTrue(runner.get("command"), f"runner {name}: empty command")
            self.assertIn(runner.get("response_format", "text"), known_formats,
                          f"runner {name}: unknown response_format")

    def test_rubric_has_judge_slice_and_gate(self):
        rubric = (ROOT / "evals" / "rubric.md").read_text(encoding="utf8")
        self.assertIn("<!-- judge:begin -->", rubric)
        self.assertIn("<!-- judge:end -->", rubric)
        self.assertIn("Release", rubric)


if __name__ == "__main__":
    unittest.main()