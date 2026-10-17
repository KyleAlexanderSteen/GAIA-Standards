#!/usr/bin/env python3
"""Independent verification for the five-domains documents."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "adr/ADR-001-five-domains-placement.md",
    "five-domains-responsibility-matrix.md",
    "gaian-registry-requirements.md",
    "test_five_domains.py",
]
NEEDLES = {
    "adr/ADR-001-five-domains-placement.md": ["Ethics", "Law", "Equality", "Coexistence", "GAIAN Registry"],
    "five-domains-responsibility-matrix.md": ["Ethics is not Law"],
    "gaian-registry-requirements.md": ["never grants authority", "Explicit consent"],
}

def main() -> int:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing {rel}")
    for rel, needles in NEEDLES.items():
        path = ROOT / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for n in needles:
                if n not in text:
                    errors.append(f"{rel} missing: {n}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("five-domains verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
