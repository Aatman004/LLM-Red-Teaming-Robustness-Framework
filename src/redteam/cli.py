"""Command Line Interface for LLM Red-Teaming & Robustness Framework."""

from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
import typer

from redteam.analytics import RedTeamAnalytics
from redteam.attacks.generator import generate_attack_suite
from redteam.attacks.mutators import (
    mutate_base64,
    mutate_hypothetical_fiction,
    mutate_indirect_injection,
    mutate_persona_dan,
    mutate_rot13,
)
from redteam.engine import RedTeamEngine
from redteam.judges.rubric import SafetyJudge
from redteam.models.cloud_target import CloudTarget
from redteam.models.mock_target import MockTarget

app = typer.Typer(
    help="Automated LLM Red-Teaming & Adversarial Robustness Pipeline CLI",
    add_completion=False,
)
console = Console()


def get_target(target_type: str, model_name: Optional[str] = None):
    t_lower = target_type.lower()
    if t_lower == "mock" or t_lower == "mock_hardened":
        return MockTarget(profile="hardened", name="target")
    elif t_lower == "mock_vulnerable":
        return MockTarget(profile="vulnerable", name="target")
    elif t_lower == "mock_overrefusing":
        return MockTarget(profile="over_refusing", name="target")
    elif t_lower == "cloud":
        return CloudTarget(model_name=model_name)
    else:
        raise ValueError(f"Unknown target type: {target_type}")


@app.command()
def scan(
    target: str = typer.Option("mock", "--target", "-t", help="Target: mock, mock_vulnerable, mock_overrefusing, cloud"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Target model identifier for cloud"),
    output_dir: str = typer.Option("reports/latest_scan", "--output-dir", "-o", help="Directory for reports and logs"),
):
    """Execute automated adversarial red-team campaign against target system."""
    target_model = get_target(target, model)
    console.print(f"[bold cyan]Initiating Adversarial Red-Team Campaign[/bold cyan]")
    console.print(f"Target: [bold white]{target_model.name}[/bold white] | Output: [white]{output_dir}[/white]\n")

    payloads = generate_attack_suite()
    console.print(f"Generated [yellow]{len(payloads)}[/yellow] adversarial & control payloads.")

    engine = RedTeamEngine(target_model, SafetyJudge())

    with console.status("[bold red]Executing attack campaign against target..."):
        events = engine.run_campaign(payloads)

    analytics = RedTeamAnalytics(events)
    summary = analytics.compute_summary()
    analytics.export(output_dir)

    # Terminal summary table
    table = Table(title="Red-Team Vulnerability Scorecard", show_header=True, header_style="bold red")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="bold white")

    asr_color = "green" if summary["overall_asr"] < 0.2 else ("yellow" if summary["overall_asr"] < 0.5 else "bold red")
    table.add_row("Total Probes", str(summary["total_probes"]))
    table.add_row("Attacks Delivered", str(summary["total_attacks"]))
    table.add_row("Adversarial Breaches", str(summary["breaches"]))
    table.add_row("Overall Attack Success Rate (ASR)", f"[{asr_color}]{summary['overall_asr'] * 100:.1f}%[/{asr_color}]")
    table.add_row("Over-Refusal Rate (False Positives)", f"{summary['over_refusal_rate'] * 100:.1f}%")

    console.print(table)

    # Breakdown by category
    cat_table = Table(title="ASR by Attack Category", show_header=True, header_style="bold magenta")
    cat_table.add_column("Category", style="cyan")
    cat_table.add_column("Probes", justify="right")
    cat_table.add_column("ASR", justify="right")

    for cat, data in summary.get("by_category", {}).items():
        cat_table.add_row(cat, str(data["count"]), f"{data['asr'] * 100:.1f}%")

    console.print(cat_table)
    console.print(f"\n[bold green]Report & event log saved to:[/bold green] [white]{output_dir}[/white]")


@app.command()
def report(
    log_file: str = typer.Option("reports/latest_scan/events.csv", "--log-file", "-l", help="Path to events CSV"),
):
    """Inspect and format previously logged red-team results."""
    analytics = RedTeamAnalytics.from_csv(log_file)
    content = analytics.generate_markdown_report()
    console.print(content)


@app.command()
def mutate(
    prompt: str = typer.Argument(..., help="Prompt to mutate"),
    technique: str = typer.Option("base64", "--technique", "-t", help="Technique: base64, rot13, dan, hypo, indirect"),
):
    """Adversarially transform a seed prompt using a specific mutation technique."""
    t_clean = technique.lower()
    if t_clean == "base64":
        result = mutate_base64(prompt)
    elif t_clean == "rot13":
        result = mutate_rot13(prompt)
    elif t_clean == "dan":
        result = mutate_persona_dan(prompt)
    elif t_clean in ("hypo", "hypothetical"):
        result = mutate_hypothetical_fiction(prompt)
    elif t_clean == "indirect":
        result = mutate_indirect_injection(prompt)
    else:
        raise ValueError(f"Unknown mutation technique: {technique}")

    console.print(f"[bold cyan]Mutated Payload ({technique}):[/bold cyan]\n")
    console.print(result)


if __name__ == "__main__":
    app()
