"""Orchestrator executing red-team campaigns and logging structured probe events."""

from datetime import datetime
import time
from typing import Any, Dict, List, Optional
from redteam.attacks.taxonomy import AttackPayload
from redteam.judges.rubric import SafetyJudge
from redteam.models.protocol import TargetModel


class RedTeamEngine:
    """Executes adversarial attack suites against target models with automated evaluation."""

    def __init__(self, target: TargetModel, judge: Optional[SafetyJudge] = None):
        self.target = target
        self.judge = judge or SafetyJudge()

    def run_campaign(self, payloads: List[AttackPayload]) -> List[Dict[str, Any]]:
        """Run all attack payloads against the target model and return structured event records."""
        events: List[Dict[str, Any]] = []

        for p in payloads:
            start_ts = datetime.utcnow()
            res = self.target.send_prompt(p.mutated_prompt)
            eval_res = self.judge.evaluate(p, res.text)

            event = {
                "timestamp": start_ts.isoformat(),
                "target_model": self.target.name,
                "probe_id": p.id,
                "category": p.category.value,
                "domain": p.domain.value,
                "technique": p.technique,
                "is_benign": p.is_benign,
                "seed_prompt": p.seed_prompt,
                "mutated_prompt": p.mutated_prompt,
                "response_text": res.text,
                "latency_seconds": res.latency_seconds,
                "tokens_generated": res.tokens_generated,
                "verdict": eval_res["verdict"].value,
                "is_breach": eval_res["is_breach"],
                "has_refusal": eval_res["has_refusal"],
                "explanation": eval_res["explanation"],
            }
            events.append(event)

        return events
