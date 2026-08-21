# Grok Computer Use

A verification-first Windows computer-use MCP + Grok Build skill.

This is deliberately an **R&D baseline**, not a claim of state of the art. Its first target is the hard part current agents still struggle with: reliable multi-application Windows workflows.

## What is implemented

- Grok Build project MCP config (`.grok/config.toml`)
- Grok computer-use skill with explicit observe → act → verify → recover loop
- Windows UI Automation semantic observation and control targeting
- screenshot / coordinate / keyboard fallback
- deterministic postcondition verifier
- route scoring primitives for API → shell → browser → UIA → vision → coordinate fallback
- unit tests for routing and verification
- evaluation plan built around ablation tests + WindowsWorld

## Windows install

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

Then:

```powershell
grok inspect
grok mcp doctor grok-computer-use
pytest -q
```

From the project root, open Grok Build and try:

```text
/computer-use Open Notepad, type "verification works", save it to C:\\Temp\\grok-test.txt, and verify the result.
```

## Why this architecture

Pure screenshot agents fail for reasons that are avoidable on Windows: stale coordinates, ambiguous controls, repeated no-op clicks, and unverified cross-app handoffs. This package prefers UIA semantics, falls back to vision only when necessary, and makes verification a required part of the agent loop.

See `docs/COMPETITION.md` and `docs/VERIFICATION.md`.

## Safety and project status

This project can generate real mouse, keyboard, clipboard, and application-launch actions. Keep the MCP local, review `SECURITY.md`, and use an isolated Windows account or VM when testing unfamiliar workflows.

The current release is an **alpha research baseline**. Browser CDP routing, filesystem-aware verification, isolated/non-disruptive execution, and full WindowsWorld integration remain planned work.

## Development

```powershell
python -m pip install -e ".[windows,dev]"
pytest -q
python -m compileall -q src tests
```

CI runs the core tests on Windows and Linux for Python 3.11/3.12, plus a Windows adapter import smoke test.

## License

MIT. See `LICENSE`.
