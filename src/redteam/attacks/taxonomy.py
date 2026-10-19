"""Taxonomy of attack categories, harm domains, and payload models."""

from enum import Enum
from pydantic import BaseModel, Field


class AttackCategory(str, Enum):
    """Categorization of adversarial bypass techniques."""
    DIRECT_JAILBREAK = "direct_jailbreak"
    OBFUSCATION_CIPHER = "obfuscation_cipher"
    INDIRECT_INJECTION = "indirect_injection"
    ROLEPLAY_FRAMING = "roleplay_framing"
    BENIGN_CONTROL = "benign_control"


class HarmDomain(str, Enum):
    """Domain of risk or safety concern targeted by the probe."""
    CYBER_EXPLOIT = "cyber_exploit"
    CBRN_DANGEROUS = "cbrn_dangerous"
    HARASSMENT = "harassment"
    AUTONOMOUS_ABUSE = "autonomous_abuse"
    BENIGN_SYSTEMS = "benign_systems"


class AttackPayload(BaseModel):
    """Concrete adversarial or benign probe delivered to target model."""
    id: str = Field(description="Unique probe identifier")
    category: AttackCategory = Field(description="Adversarial attack class")
    domain: HarmDomain = Field(description="Harm or topic domain")
    seed_prompt: str = Field(description="Underlying raw request or intent")
    mutated_prompt: str = Field(description="Adversarially transformed input prompt")
    technique: str = Field(description="Specific mutation technique name")
    is_benign: bool = Field(default=False, description="True if probe is a benign control for over-refusal")
