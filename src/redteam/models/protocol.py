"""Target model interface and response definitions."""

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class TargetResponse(BaseModel):
    """Response returned from a target model under red-team probing."""
    text: str = Field(description="Generated model response text")
    latency_seconds: float = Field(default=0.0, description="Response latency in seconds")
    tokens_generated: int = Field(default=0, description="Approximate count of tokens produced")


class TargetModel(ABC):
    """Abstract interface for any model or system evaluated by the red-team framework."""

    name: str = "generic_target"

    @abstractmethod
    def send_prompt(self, prompt: str) -> TargetResponse:
        """Submit a probe prompt to the target model and return response."""
        pass
