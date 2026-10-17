#!/usr/bin/env python3
"""Tests for the GAIAN Registry record validator."""
import json
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from validate_record import validate

VALID = {
    "schema_version": "1.0.0",
    "gaian_id": "GAIAN-ABC12345",
    "human_principal_ref": "human:example",
    "consent": {
        "granted": True,
        "granted_at": "2026-10-16T00:00:00Z",
        "scope": ["read:profile"],
        "withdrawable": True
    },
    "privacy_boundary": {
        "readable_by": ["human:example"],
        "fields_exposed": ["gaian_id"]
    },
    "created_at": "2026-10-16T00:00:00Z",
    "grants_authority": False
}

class TestValidate(unittest.TestCase):
    def test_valid_passes(self):
        self.assertEqual(validate(VALID), [])

    def test_missing_consent_fails(self):
        bad = dict(VALID)
        del bad["consent"]
        self.assertTrue(validate(bad))

    def test_grants_authority_true_fails(self):
        bad = dict(VALID)
        bad["grants_authority"] = True
        self.assertTrue(any("grants_authority" in e for e in validate(bad)))

    def test_consent_not_withdrawable_fails(self):
        bad = json.loads(json.dumps(VALID))
        bad["consent"]["withdrawable"] = False
        self.assertTrue(any("withdrawable" in e for e in validate(bad)))

if __name__ == "__main__":
    unittest.main()
