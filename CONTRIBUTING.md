# Contributing

This project is verification-first. New computer-use capabilities should improve measurable task reliability rather than only add more actions.

## Development

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[windows,dev]"
pytest -q
python -m compileall -q src tests
```

## Change requirements

- Add or update tests for routing, verification, or execution behavior.
- Prefer semantic APIs/UIA over raw coordinates.
- Define observable postconditions for new state-changing actions.
- Do not weaken permission or authentication boundaries for convenience.
- Keep benchmark claims reproducible and distinguish measured results from hypotheses.

See `docs/VERIFICATION.md` before adding benchmark claims.
