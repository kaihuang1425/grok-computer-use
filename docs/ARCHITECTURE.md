# Architecture

Grok CUA Lab separates planning from execution and verification.

```text
Grok / Grok Build
       |
 computer-use skill
       |
 local stdio MCP
       |
 execution router
  API -> shell -> browser -> UIA -> vision -> coordinates
       |
 Windows adapter
       |
 deterministic verifier
       |
 checkpoint / recovery
```

## Components

- `.grok/skills/computer-use/SKILL.md` — behavioral policy: observe, act, verify, recover.
- `.grok/config.toml` — local MCP registration.
- `src/grok_cua/server.py` — MCP surface.
- `src/grok_cua/adapters/windows.py` — Windows UIA, screenshots, keyboard/mouse fallback.
- `src/grok_cua/core/router.py` — execution-surface scoring and fallback ordering.
- `src/grok_cua/core/verifier.py` — explicit postcondition checks and failure classification.
- `src/grok_cua/core/trace.py` — JSONL trajectory logging primitive.
- `eval/` + `docs/VERIFICATION.md` — reproducible evaluation contract.

## Reliability rule

A successful action is not equivalent to a successful state transition. State-changing actions should be followed by evidence that the expected state exists. If verification fails, re-observe and change strategy rather than blindly repeating the same action.

## Current limitations

- Windows-only desktop adapter.
- Browser DOM/CDP route is designed but not yet implemented.
- Verifier currently covers UI-visible state; filesystem/app-specific postconditions should be added next.
- Non-disruptive isolated desktop/VM execution is not yet implemented.
