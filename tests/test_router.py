from grok_cua.core.models import Candidate, Route
from grok_cua.core.router import choose, next_route

def test_prefers_semantic_route():
    c = choose([
        Candidate(Route.UIA, reliability=.9, latency=.2, disruption=.1, reversibility=.8),
        Candidate(Route.VISION, reliability=.9, latency=.5, disruption=.4, reversibility=.8),
        Candidate(Route.COORDINATE, reliability=.95, latency=.1, disruption=.5, reversibility=.5),
    ])
    assert c.route is Route.UIA

def test_fallback_escalates():
    assert next_route(Route.UIA, {Route.UIA, Route.VISION, Route.COORDINATE}) is Route.VISION
