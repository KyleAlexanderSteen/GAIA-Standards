#!/usr/bin/env python3
"""Structure checks for the research-backed templates."""
from pathlib import Path
import unittest

ROOT = Path(__file__).parent

class TestTemplates(unittest.TestCase):
    def test_issue_template_has_required_sections(self):
        text = (ROOT / "issue-template.md").read_text(encoding="utf-8")
        for section in ["GAP-ID", "Acceptance criteria", "Stages", "SPECIFICATION", "IMPLEMENTATION", "TEST", "Evidence plan"]:
            self.assertIn(section, text)

    def test_pr_template_has_required_sections(self):
        text = (ROOT / "pull_request_template.md").read_text(encoding="utf-8")
        for section in ["Stage reached", "SPECIFICATION", "IMPLEMENTATION", "TEST", "Evidence", "GAP-ID"]:
            self.assertIn(section, text)

    def test_readme_exists(self):
        self.assertTrue((ROOT / "README.md").is_file())

if __name__ == "__main__":
    unittest.main()
