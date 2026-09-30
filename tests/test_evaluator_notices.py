"""Offline checks: label legacy diagnostics without changing their calculations.

These tests neither run models nor measure the skill's research quality.
"""
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LegacyNoticeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = Path(self.tmp.name)
        self.mech = load_module("legacy_notice_mech", ROOT / "evolve" / "mech.py")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        p = self.run / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_freeform_values_remain_legacy_not_quality(self):
        self.write("report.md", "Evidence [paper](https://example.org/paper).\n")
        m = self.mech.mech(self.run, "notice-test-no-golden", 9000)
        self.assertEqual((m["sections"], m["traceable"], m["notes"]["claims_ok"]), (0.0, 0.0, 0.0))
        self.assertEqual(m["urls"], 1)
        self.assertIsNone(m["golden"])
        self.assertTrue(m["len_ok"])

    def test_legacy_structured_values_are_unchanged(self):
        self.write("report.md", "# 一屏\n## taxonomy\n## 对照\n## 坑\n## 未决\n## 来源\nhttps://example.org/paper\n")
        self.write("ds/notes/r1-source.md", '- [C1] Fact | src: https://example.org/paper | quote: "Text" | type: official\n')
        m = self.mech.mech(self.run, "notice-test-no-golden", 9000)
        self.assertEqual((m["sections"], m["traceable"], m["notes"]["claims_ok"]), (1.0, 1.0, 1.0))

    def test_mech_stdout_remains_json_notice_goes_to_stderr(self):
        self.write("report.md", "A short answer.\n")
        r = subprocess.run([sys.executable, str(ROOT / "evolve" / "mech.py"), str(self.run), "notice-test-no-golden"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(r.stdout), self.mech.mech(self.run, "notice-test-no-golden", 9000))
        self.assertIn("Legacy diagnostics", r.stderr)
        self.assertNotIn("Legacy diagnostics", r.stdout)

    def test_missing_report_retains_legacy_failure_values(self):
        m = self.mech.mech(self.run, "notice-test-no-golden", 9000)
        self.assertEqual(m["chars"], 0)
        self.assertFalse(m["len_ok"])

    def test_report_notice_keeps_summary_schema_and_stdout_labels(self):
        ev = load_module("legacy_notice_evaluate", ROOT / "evolve" / "evaluate.py")
        ev.RUNS = self.run
        (self.run / "notice-test").mkdir()
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            ev.report("notice-test", [])
        data = json.loads((self.run / "notice-test" / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"exp", "vs", "tasks", "score", "task_scores", "wins", "losses", "verdicts", "dims_net", "golden", "golden_vs", "chars_max", "len_ok", "traceable", "spawns", "lead_web", "cost_usd", "cost_vs_per_run", "minutes", "skill_chars", "skill_sha", "statuses", "runs"})
        self.assertIsNone(data["score"])
        self.assertIsNone(data["traceable"])
        self.assertIn("score:", stdout.getvalue())
        self.assertIn("traceable:", stdout.getvalue())
        self.assertIn("Legacy diagnostics", stderr.getvalue())
        self.assertNotIn("Legacy diagnostics", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
