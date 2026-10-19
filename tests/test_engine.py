"""Unit tests for the end-to-end RedTeamEngine."""

from redteam.attacks.generator import generate_attack_suite
from redteam.engine import RedTeamEngine
from redteam.judges.rubric import SafetyJudge
from redteam.models.mock_target import MockTarget


def test_engine_campaign_execution():
    target = MockTarget(profile="hardened")
    judge = SafetyJudge()
    engine = RedTeamEngine(target, judge)

    payloads = generate_attack_suite()[:5]
    events = engine.run_campaign(payloads)

    assert len(events) == 5
    for ev in events:
        assert "is_breach" in ev
        assert "verdict" in ev
        assert ev["target_model"] == target.name
