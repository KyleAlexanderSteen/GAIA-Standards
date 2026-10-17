#!/usr/bin/env python3
"""Unit tests for the stage-evidence reference checker."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "stage_evidence_check.py"

def run(body: str) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        path = f.name
    return subprocess.run([sys.executable, str(SCRIPT), "--body", path], capture_output=True, text=True)

class TestStageEvidence(unittest.TestCase):
    def test_missing_section_fails(self):
        r = run("no stage section here")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("missing", r.stderr.lower())

    def test_no_stages_checked_fails(self):
        body = "## Stage reached\n- [ ] SPECIFICATION\n"
        r = run(body)
        self.assertNotEqual(r.returncode, 0)

    def test_specification_only_passes(self):
        body = "## Stage reached\n- [x] SPECIFICATION\n"
        r = run(body)
        self.assertEqual(r.returncode, 0)
        self.assertIn("PASS", r.stdout)

    def test_implementation_without_evidence_fails(self):
        body = "## Stage reached\n- [x] IMPLEMENTATION\n## Evidence\n"
        r = run(body)
        self.assertNotEqual(r.returncode, 0)

    def test_implementation_with_evidence_passes(self):
        body = "## Stage reached\n- [x] IMPLEMENTATION\n## Evidence\n- IMPLEMENTATION: file.py\n"
        r = run(body)
        self.assertEqual(r.returncode, 0)

    def test_test_without_evidence_fails(self):
        body = "## Stage reached\n- [x] TEST\n## Evidence\n"
        r = run(body)
        self.assertNotEqual(r.returncode, 0)

    def test_test_with_evidence_passes(self):
        body = "## Stage reached\n- [x] TEST\n## Evidence\n- TEST: python -m unittest\n"
        r = run(body)
        self.assertEqual(r.returncode, 0)

if __name__ == "__main__":
    unittest.main()
