# GAIAN Registry (schema only)

**Status:** Schema and validator only. No registry service exists.

This directory holds the JSON Schema and a fail-closed structural validator for a GAIAN Registry record.

See `docs/gaian-registry-requirements.md` for the full requirements.

## Rules encoded here

- Explicit consent is required.
- Consent must be withdrawable.
- `grants_authority` must be false or absent.
- A record never grants authority over the human.

## Run

```bash
python -m unittest standards/gaian-registry/test_validate_record.py
```
