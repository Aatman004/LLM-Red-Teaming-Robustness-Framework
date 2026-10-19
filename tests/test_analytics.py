"""Unit tests for Pandas-based ASR and metrics analytics."""

from redteam.analytics import RedTeamAnalytics


def test_analytics_asr_calculation():
    events = [
        # 2 attacks: 1 breach, 1 refused
        {
            "target_model": "test-target",
            "probe_id": "1",
            "category": "direct_jailbreak",
            "domain": "cyber_exploit",
            "technique": "direct",
            "is_benign": False,
            "mutated_prompt": "prompt 1",
            "response_text": "breached response",
            "verdict": "full_breach",
            "is_breach": True,
        },
        {
            "target_model": "test-target",
            "probe_id": "2",
            "category": "obfuscation_cipher",
            "domain": "cyber_exploit",
            "technique": "base64",
            "is_benign": False,
            "mutated_prompt": "prompt 2",
            "response_text": "I cannot fulfill this request",
            "verdict": "refused",
            "is_breach": False,
        },
        # 1 control: helpful safe
        {
            "target_model": "test-target",
            "probe_id": "3",
            "category": "benign_control",
            "domain": "benign_systems",
            "technique": "direct_benign",
            "is_benign": True,
            "mutated_prompt": "benign prompt",
            "response_text": "Helpful answer",
            "verdict": "helpful_safe",
            "is_breach": False,
        },
    ]

    analytics = RedTeamAnalytics(events)
    summary = analytics.compute_summary()

    assert summary["total_probes"] == 3
    assert summary["total_attacks"] == 2
    assert summary["total_controls"] == 1
    assert summary["breaches"] == 1
    assert summary["overall_asr"] == 0.5  # 1 out of 2 attacks breached
    assert summary["over_refusal_rate"] == 0.0

    report = analytics.generate_markdown_report()
    assert "Overall Attack Success Rate (ASR)" in report
    assert "50.0%" in report
