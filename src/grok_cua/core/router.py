from __future__ import annotations
from .models import Candidate, Route

# Prefer interfaces that are robust, low-disruption, and reversible.
_BASE = {
    Route.API: 1.00,
    Route.SHELL: 0.92,
    Route.BROWSER: 0.90,
    Route.UIA: 0.86,
    Route.VISION: 0.62,
    Route.COORDINATE: 0.45,
}

def score(c: Candidate) -> float:
    if not c.available:
        return -1e9
    return (
        _BASE[c.route]
        + 0.55 * c.reliability
        + 0.20 * c.reversibility
        - 0.18 * c.latency
        - 0.28 * c.disruption
    )

def choose(candidates: list[Candidate]) -> Candidate:
    available = [c for c in candidates if c.available]
    if not available:
        raise ValueError("no available execution route")
    return max(available, key=score)

FALLBACK_ORDER = [Route.API, Route.SHELL, Route.BROWSER, Route.UIA, Route.VISION, Route.COORDINATE]

def next_route(current: Route, available: set[Route]) -> Route | None:
    try:
        start = FALLBACK_ORDER.index(current) + 1
    except ValueError:
        start = 0
    for route in FALLBACK_ORDER[start:]:
        if route in available:
            return route
    return None
