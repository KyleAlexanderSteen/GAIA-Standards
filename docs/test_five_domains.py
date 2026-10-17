#!/usr/bin/env python3
"""Structure checks for the five-domains ADR, matrix, and GAIAN requirements.

These are document tests. They do not claim implementation of any domain.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent

class TestFiveDomains(unittest.TestCase):
    def test_adr_exists_and_has_decision(self):
        text = (ROOT / "adr" / "ADR-001-five-domains-placement.md").read_text(encoding="utf-8")
        for needle in ["Ethics", "Law", "Equality", "Coexistence", "GAIAN Registry", "Do **not** create dedicated repositories"]:
            self.assertIn(needle, text)

    def test_matrix_covers_five_domains(self):
        text = (ROOT / "five-domains-responsibility-matrix.md").read_text(encoding="utf-8")
        for domain in ["Ethics", "Law", "Equality", "Coexistence", "GAIAN Registry"]:
            self.assertIn(domain, text)
        self.assertIn("Ethics is not Law", text)

    def test_gaian_requirements_has_mandatory_rules(self):
        text = (ROOT / "gaian-registry-requirements.md").read_text(encoding="utf-8")
        for needle in [
            "Explicit consent",
            "No silent inference",
            "Least-privilege",
            "never grants authority",
            "export",
            "delete",
        ]:
            self.assertIn(needle, text)

if __name__ == "__main__":
    unittest.main()
