#!/usr/bin/env python3
"""Minimal structural validator for a GAIAN Registry record.

Fails closed. Does not grant authority. Does not claim a registry service exists.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REQUIRED = ["schema_version", "gaian_id", "human_principal_ref", "consent", "privacy_boundary", "created_at"]
CONSENT_REQUIRED = ["granted", "granted_at", "scope", "withdrawable"]

def validate(record: dict) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    for key in REQUIRED:
        if key not in record:
            errors.append(f"missing {key}")
    if record.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if record.get("grants_authority") not in (None, False):
        errors.append("grants_authority must be false or absent")
    consent = record.get("consent")
    if isinstance(consent, dict):
        for key in CONSENT_REQUIRED:
            if key not in consent:
                errors.append(f"consent missing {key}")
        if consent.get("granted") is not True:
            errors.append("consent.granted must be true for a valid registration")
        if consent.get("withdrawable") is not True:
            errors.append("consent.withdrawable must be true")
        if not isinstance(consent.get("scope"), list) or not consent.get("scope"):
            errors.append("consent.scope must be a non-empty list")
    elif "consent" in record:
        errors.append("consent must be an object")
    boundary = record.get("privacy_boundary")
    if isinstance(boundary, dict):
        if not isinstance(boundary.get("readable_by"), list):
            errors.append("privacy_boundary.readable_by must be a list")
        if not isinstance(boundary.get("fields_exposed"), list):
            errors.append("privacy_boundary.fields_exposed must be a list")
    elif "privacy_boundary" in record:
        errors.append("privacy_boundary must be an object")
    return errors

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_record.py <record.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    record = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(record)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("gaian-registry record: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
