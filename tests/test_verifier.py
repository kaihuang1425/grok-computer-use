from grok_cua.core.models import Observation, Control, Expectation
from grok_cua.core.verifier import verify

def test_verifier_passes_on_explicit_evidence():
    before=Observation(active_window='Home')
    after=Observation(active_window='Settings - Network', controls=[Control('1','Wi-Fi','button')])
    r=verify(before, after, Expectation(active_window_contains='Settings', ui_text_contains='Wi-Fi', state_changed=True))
    assert r.passed and r.confidence == 1.0

def test_verifier_rejects_noop():
    before=Observation(active_window='Settings', controls=[Control('1','Wi-Fi','button')])
    after=Observation(active_window='Settings', controls=[Control('1','Wi-Fi','button')])
    r=verify(before, after, Expectation(state_changed=True))
    assert not r.passed and r.classification == 'no-op'
