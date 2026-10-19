"""Pandas-powered analytics engine for computing Attack Success Rate (ASR) and failure modes."""

from pathlib import Path
from typing import Any, Dict, List
import pandas as pd


class RedTeamAnalytics:
    """Processes probe event logs, computes ASR metrics, and formats audit reports."""

    def __init__(self, events: List[Dict[str, Any]] | pd.DataFrame):
        if isinstance(events, pd.DataFrame):
            self.df = events.copy()
        else:
            self.df = pd.DataFrame(events)

    @classmethod
    def from_csv(cls, path: str | Path) -> "RedTeamAnalytics":
        """Load events from a previously recorded CSV log."""
        df = pd.read_csv(path)
        return cls(df)

    def compute_summary(self) -> Dict[str, Any]:
        """Compute key red-teaming metrics including ASR and Over-Refusal."""
        if self.df.empty:
            return {"total_probes": 0, "asr": 0.0, "over_refusal_rate": 0.0}

        attacks_df = self.df[~self.df["is_benign"]]
        controls_df = self.df[self.df["is_benign"]]

        total_attacks = len(attacks_df)
        total_controls = len(controls_df)

        breach_count = int(attacks_df["is_breach"].sum()) if total_attacks > 0 else 0
        asr = (breach_count / total_attacks) if total_attacks > 0 else 0.0

        over_refusal_count = (
            int((controls_df["verdict"] == "over_refusal").sum()) if total_controls > 0 else 0
        )
        orr = (over_refusal_count / total_controls) if total_controls > 0 else 0.0

        # Category breakdown
        cat_asr = {}
        if total_attacks > 0:
            cat_group = attacks_df.groupby("category")["is_breach"].agg(["count", "mean"])
            cat_asr = {
                idx: {"count": int(row["count"]), "asr": float(row["mean"])}
                for idx, row in cat_group.iterrows()
            }

        # Technique breakdown
        tech_asr = {}
        if total_attacks > 0:
            tech_group = attacks_df.groupby("technique")["is_breach"].agg(["count", "mean"])
            tech_asr = {
                idx: {"count": int(row["count"]), "asr": float(row["mean"])}
                for idx, row in tech_group.iterrows()
            }

        # Domain breakdown
        domain_asr = {}
        if total_attacks > 0:
            domain_group = attacks_df.groupby("domain")["is_breach"].agg(["count", "mean"])
            domain_asr = {
                idx: {"count": int(row["count"]), "asr": float(row["mean"])}
                for idx, row in domain_group.iterrows()
            }

        return {
            "total_probes": len(self.df),
            "total_attacks": total_attacks,
            "total_controls": total_controls,
            "breaches": breach_count,
            "overall_asr": asr,
            "over_refusal_rate": orr,
            "by_category": cat_asr,
            "by_technique": tech_asr,
            "by_domain": domain_asr,
        }

    def generate_markdown_report(self) -> str:
        """Render a detailed Markdown red-team postmortem report."""
        summary = self.compute_summary()
        model_name = self.df["target_model"].iloc[0] if not self.df.empty else "Unknown"

        lines = [
            "# LLM Red-Teaming & Adversarial Robustness Report",
            f"**Target System:** `{model_name}` | **Total Probes Executed:** `{summary['total_probes']}`",
            "",
            "## 1. Executive Vulnerability Metrics",
            f"- **Overall Attack Success Rate (ASR):** `{summary['overall_asr'] * 100:.1f}%` ({summary['breaches']}/{summary['total_attacks']} attacks succeeded)",
            f"- **Over-Refusal Rate (ORR):** `{summary['over_refusal_rate'] * 100:.1f}%` (false refusals on benign requests)",
            "",
            "### Vulnerability by Attack Category",
            "| Attack Category | Probes | Attack Success Rate (ASR) |",
            "|---|:---:|:---:|",
        ]

        for cat, data in summary.get("by_category", {}).items():
            lines.append(f"| `{cat}` | {data['count']} | **`{data['asr'] * 100:.1f}%`** |")

        lines.extend([
            "",
            "### Vulnerability by Mutation Technique",
            "| Technique | Probes | Attack Success Rate (ASR) |",
            "|---|:---:|:---:|",
        ])

        for tech, data in summary.get("by_technique", {}).items():
            lines.append(f"| `{tech}` | {data['count']} | **`{data['asr'] * 100:.1f}%`** |")

        # Breach spotlight
        breaches = self.df[self.df["is_breach"]]
        lines.extend([
            "",
            "## 2. Breach Incident Spotlight (Sample Transcripts)",
        ])

        if breaches.empty:
            lines.append("No successful adversarial breaches detected in this evaluation run.\n")
        else:
            for _, row in breaches.head(3).iterrows():
                short_response = (
                    row["response_text"][:250] + "..."
                    if len(row["response_text"]) > 250
                    else row["response_text"]
                )
                lines.extend([
                    f"### Probe: `{row['probe_id']}` ({row['technique']})",
                    f"- **Category:** `{row['category']}` | **Domain:** `{row['domain']}`",
                    f"- **Verdict:** `{row['verdict'].upper()}`",
                    f"- **Mutated Prompt Excerpt:**",
                    f"> {row['mutated_prompt'][:200]}...",
                    f"- **Model Output:**",
                    f"> {short_response}",
                    "",
                ])

        lines.extend([
            "---",
            "*Report generated by LLM Red-Teaming & Robustness Framework (Aatman Gupta)*"
        ])

        return "\n".join(lines)

    def export(self, output_dir: str | Path) -> None:
        """Export both tabular events CSV and Markdown audit report."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        csv_path = out / "events.csv"
        md_path = out / "redteam_report.md"

        self.df.to_csv(csv_path, index=False)
        md_path.write_text(self.generate_markdown_report(), encoding="utf-8")
