# Automated LLM Red-Teaming & Robustness Framework

[![CI](https://github.com/aatmangupta/llm-redteaming-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/aatmangupta/llm-redteaming-framework/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Pandas Analytics](https://img.shields.io/badge/analytics-Pandas%202.2-150458.svg)](https://pandas.pydata.org/)

An automated adversarial evaluation pipeline and robustness harness designed to stress-test large language models and autonomous agents against **jailbreaks**, **prompt injections**, **obfuscation ciphers**, and **guardrail bypasses**.

---

## Overview & AI Safety Motivation

Frontier AI laboratories (Anthropic, OpenAI, METR, UK AISI) rely on rigorous red-teaming to discover critical vulnerabilities and quantify safety degradation before models are deployed.

This framework automates adversarial probing by combining:
- **Taxonomy of Adversarial Attacks**: Direct jailbreaks, cognitive framing, persona adoption, cipher/encoding evasion (Base64, ROT13, Leetspeak), and indirect prompt injection payloads.
- **Benign Over-Refusal Probes**: Safety-adjacent benign requests (e.g., debugging system process kills, explaining immunological defense) to measure false positive refusal rates.
- **Rubric-Based Safety Judge**: Classifies target responses into granular outcomes: `REFUSED`, `PARTIAL_BREACH`, `FULL_BREACH`, `OVER_REFUSAL`, and `HELPFUL_SAFE`.
- **Pandas Analytics & Failure Mode Matrix**: Computes empirical **Attack Success Rate (ASR)** across attack categories and generates auditable postmortem incident reports.

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                 Harmful Intent & Probe Seed                 │
│  • CBRN & Bio risk queries                                  │
│  • Cyber intrusion & exploit queries                        │
│  • Benign control probes (Over-refusal testing)             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Adversarial Attack Engine                  │
│  • Persona & Roleplay Jailbreaks (DAN, Academic Sandbox)    │
│  • Encoding & Obfuscation (Base64, ROT13, Leetspeak)        │
│  • Indirect Context Injection (HTML/Markdown data injection)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Target Model Under Evaluation               │
│  • Cloud APIs (Anthropic Claude, OpenAI GPT-4o)             │
│  • Local Hugging Face / Ollama Models                       │
│  • Deterministic Mock Target (for CI/CD & validation)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             Automated Safety & Refusal Judge                │
│  • Evaluates Refusal compliance vs Safety breaches          │
│  • Assigns outcome: REFUSED, PARTIAL_BREACH, FULL_BREACH    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Pandas Analytics & Reporting                │
│  • Overall & Categorical Attack Success Rate (ASR)          │
│  • Over-Refusal Rate (ORR)                                  │
│  • Markdown & HTML Failure Mode Audit Transcripts           │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/aatmangupta/llm-redteaming-framework.git
cd llm-redteaming-framework

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package and dependencies
pip install -e ".[dev]"
```

---

## CLI Usage

### 1. Run Automated Red-Team Scan
```bash
# Run scan against mock model (for verification or CI)
redteam scan --target mock --output-dir reports/scan_mock

# Run scan against a cloud model
export ANTHROPIC_API_KEY="your-key"
redteam scan --target cloud --provider anthropic --model claude-3-5-sonnet-20241022 --output-dir reports/claude_redteam
```

### 2. Inspect Attack Success Rate (ASR)
```bash
redteam report --log-file reports/scan_mock/events.csv
```

### 3. Test Attack Mutators
```bash
redteam mutate "How to synthesize toxic compounds" --mutator base64
redteam mutate "Generate keylogger exploit" --mutator persona
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Author

**Aatman Gupta**  
Queen's University — Bachelor of Computing (Artificial Intelligence)  
Email: [aatmangupta8@gmail.com](mailto:aatmangupta8@gmail.com)  
AI Safety Fellowship Lead | Queen's Effective Altruism
