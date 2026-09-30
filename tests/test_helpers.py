"""Offline regressions for optional diagnostics and the existing benchmark adapter.

These tests do not run agents, fetch sources, or assess research quality.
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "deep-search" / "scripts"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *map(str, args)],
            capture_output=True, text=True, check=False,
        )

    def test_freeform_notes_are_unassessed(self):
        self.write("notes/findings.md", "A useful finding. https://example.org/paper\n")
        result = self.run_script("notes_lint.py", self.root / "notes")
        self.assertEqual(result.returncode, 0)
        self.assertIn("NOT ASSESSED: no legacy C# claims parsed", result.stdout)
        self.assertNotIn("passed", result.stdout.lower())

    def test_legacy_claim_parsing_and_missing_fields(self):
        module = load_module("notes_lint_test", SCRIPTS / "notes_lint.py")
        path = self.write("notes/r1-a.md", '## claims\n- [C1] Fact | src: https://example.org/a | quote: "Text" | type: official\n- [C2] Missing fields\n')
        stats = module.lint(path)
        self.assertEqual((stats["claims"], stats["official"], stats["secondary"]), (2, 1, 1))
        self.assertEqual(stats["no_src"], ["C2"])
        self.assertEqual(stats["no_quote"], ["C2"])

    def test_notes_round_filter_and_explicit_limit(self):
        self.write("notes/r1-a.md", "A" * 30)
        self.write("notes/r2-b.md", "B" * 30)
        result = self.run_script("notes_lint.py", self.root / "notes", "--round", 1, "--max-chars", 20)
        self.assertEqual(result.returncode, 0)
        self.assertIn("r1-a.md", result.stdout)
        self.assertNotIn("r2-b.md", result.stdout)
        self.assertIn("notes over 20 chars", result.stdout)

    def test_empty_notes_are_unassessed(self):
        (self.root / "notes").mkdir()
        result = self.run_script("notes_lint.py", self.root / "notes")
        self.assertIn("NOT ASSESSED: no notes", result.stdout)

    def test_missing_notes_directory_is_reported(self):
        result = self.run_script("notes_lint.py", self.root / "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_no_default_budget_or_required_headings(self):
        self.write("report.md", "说明" * 11000 + " [原论文](https://example.org/paper)\n")
        self.write("grid.md", "| topic | ✅ |\n")
        result = self.run_script("roundstat.py", self.root)
        self.assertEqual(result.returncode, 0)
        self.assertIn("budget not specified", result.stdout)
        self.assertNotIn("OVER BUDGET", result.stdout)
        self.assertNotIn("vocab", result.stdout)
        self.assertNotIn("cite:", result.stdout)
        self.assertIn("not verified coverage", result.stdout)

    def test_explicit_budget_counts_characters(self):
        self.write("report.md", "中文abc")
        result = self.run_script("roundstat.py", self.root, "--budget", 4)
        self.assertIn("report.md: 5 OVER BUDGET", result.stdout)

    def test_direct_links_and_legacy_layout_are_distinct(self):
        self.write("report.md", "Evidence [here](https://example.org/source).\n")
        normal = self.run_script("roundstat.py", self.root)
        legacy = self.run_script("roundstat.py", self.root, "--legacy-layout")
        self.assertNotIn("cite:", normal.stdout)
        self.assertIn("legacy layout has no 来源 section", legacy.stdout)

    def test_optional_files_and_snapshot_names(self):
        self.write("snapshots/report.r10.md", "ten")
        self.write("snapshots/report.r2.md", "two")
        self.write("snapshots/report.final.md", "final")
        self.write("atlas.md", "A" * 12)
        self.write("details/explanation.md", "B" * 4100)
        normal = self.run_script("roundstat.py", self.root, "--budget", 5)
        legacy = self.run_script("roundstat.py", self.root, "--budget", 5, "--legacy-layout")
        self.assertEqual(normal.returncode, 0)
        self.assertLess(normal.stdout.index("report.r2.md"), normal.stdout.index("report.r10.md"))
        self.assertIn("report.final.md", normal.stdout)
        self.assertIn("main report NOT ASSESSED", normal.stdout)
        self.assertNotIn("OVER 4000", normal.stdout)
        self.assertIn("atlas.md: 12 (legacy cap 10) OVER BUDGET", legacy.stdout)
        self.assertIn("OVER 4000 (legacy cap)", legacy.stdout)

    def test_invalid_limits_are_reported(self):
        self.write("notes/a.md", "note")
        for name, directory, flag in (("roundstat.py", self.root, "--budget"), ("notes_lint.py", self.root / "notes", "--max-chars")):
            result = self.run_script(name, directory, flag, 0)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be positive", result.stderr)

    def test_existing_benchmark_worker_adapter(self):
        module = load_module("bench_run_arm_test", ROOT / "bench" / "run_arm.py")
        description, body = module.worker_body()
        self.assertTrue(description)
        self.assertIn("完整 URL", body)
        worker = module.worker_agent("offline-test-model")["research-worker"]
        self.assertEqual(worker["model"], "offline-test-model")
        self.assertIn("WebFetch", worker["tools"])
        self.assertEqual(worker["prompt"], body)
        prompt = module.cc_prompt("Research a topic")
        self.assertIn("./ds", prompt)
        self.assertIn("./report.md", prompt)


if __name__ == "__main__":
    unittest.main()
