#!/usr/bin/env python3
"""Structure and basic invariant tests for the reference scenarios."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
SCENARIOS = ROOT / "reference_scenarios.json"

class TestScenarios(unittest.TestCase):
    def setUp(self):
        self.scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))

    def test_is_list(self):
        self.assertIsInstance(self.scenarios, list)
        self.assertGreaterEqual(len(self.scenarios), 1)

    def test_required_fields(self):
        for s in self.scenarios:
            self.assertIn("id", s)
            self.assertIn("seed", s)
            self.assertIn("events", s)
            self.assertIn("invariants", s)
            self.assertIsInstance(s["events"], list)
            self.assertIsInstance(s["invariants"], list)

    def test_unique_ids(self):
        ids = [s["id"] for s in self.scenarios]
        self.assertEqual(len(ids), len(set(ids)))

    def test_gap_linked_example_present(self):
        gap_scenarios = [s for s in self.scenarios if s.get("gap_id")]
        self.assertGreaterEqual(len(gap_scenarios), 1)
        self.assertTrue(any(s.get("gap_id") == "GAP-2026-002" for s in gap_scenarios))

    def test_refuse_unauthorized_has_invariant(self):
        s = next(x for x in self.scenarios if x["id"] == "standards.refuse-unauthorized")
        self.assertIn("refused_action_never_executes", s["invariants"])

if __name__ == "__main__":
    unittest.main()
