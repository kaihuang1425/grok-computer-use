from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class Route(str, Enum):
    API = "api"
    SHELL = "shell"
    BROWSER = "browser"
    UIA = "uia"
    VISION = "vision"
    COORDINATE = "coordinate"

@dataclass(slots=True)
class Candidate:
    route: Route
    available: bool = True
    reliability: float = 0.5
    latency: float = 0.5
    disruption: float = 0.5
    reversibility: float = 0.5
    reason: str = ""

@dataclass(slots=True)
class Control:
    id: str
    name: str
    role: str
    automation_id: str = ""
    enabled: bool = True
    visible: bool = True
    bounds: tuple[int, int, int, int] | None = None
    value: str | None = None

@dataclass(slots=True)
class Observation:
    active_window: str = ""
    process: str = ""
    controls: list[Control] = field(default_factory=list)
    screen_size: tuple[int, int] | None = None
    screenshot_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class Expectation:
    active_window_contains: str | None = None
    ui_text_contains: str | None = None
    control_role: str | None = None
    process_running: str | None = None
    state_changed: bool = False

@dataclass(slots=True)
class VerificationResult:
    passed: bool
    confidence: float
    evidence: list[str]
    failed: list[str]
    classification: str
