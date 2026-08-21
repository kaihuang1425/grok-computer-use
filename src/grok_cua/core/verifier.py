from __future__ import annotations
import re
from .models import Expectation, Observation, VerificationResult

def _text_blob(obs: Observation) -> str:
    parts = [obs.active_window, obs.process]
    for c in obs.controls:
        parts.extend([c.name, c.role, c.automation_id, c.value or ""])
    return "\n".join(parts)

def verify(before: Observation | None, after: Observation, exp: Expectation) -> VerificationResult:
    evidence: list[str] = []
    failed: list[str] = []
    checks = 0
    blob = _text_blob(after).lower()

    if exp.active_window_contains:
        checks += 1
        if exp.active_window_contains.lower() in after.active_window.lower():
            evidence.append(f"active window contains {exp.active_window_contains!r}")
        else:
            failed.append(f"active window does not contain {exp.active_window_contains!r}")

    if exp.ui_text_contains:
        checks += 1
        if exp.ui_text_contains.lower() in blob:
            evidence.append(f"UI contains {exp.ui_text_contains!r}")
        else:
            failed.append(f"UI does not contain {exp.ui_text_contains!r}")

    if exp.control_role:
        checks += 1
        if any(c.role.lower() == exp.control_role.lower() for c in after.controls):
            evidence.append(f"control role {exp.control_role!r} exists")
        else:
            failed.append(f"control role {exp.control_role!r} not found")

    if exp.process_running:
        checks += 1
        if exp.process_running.lower() in after.process.lower():
            evidence.append(f"process matches {exp.process_running!r}")
        else:
            failed.append(f"process does not match {exp.process_running!r}")

    if exp.state_changed:
        checks += 1
        changed = before is None or (
            before.active_window != after.active_window
            or [(c.name, c.role, c.value) for c in before.controls] != [(c.name, c.role, c.value) for c in after.controls]
        )
        if changed:
            evidence.append("observable state changed")
        else:
            failed.append("observable state did not change")

    if checks == 0:
        return VerificationResult(False, 0.0, [], ["no verification criteria"], "invalid-rubric")

    passed = not failed
    confidence = len(evidence) / checks
    classification = "success" if passed else ("no-op" if exp.state_changed and "observable state did not change" in failed else "expectation-mismatch")
    return VerificationResult(passed, confidence, evidence, failed, classification)
