"""Cloud API target client for frontier LLMs."""

import os
import time
from typing import Optional
import httpx
from redteam.models.protocol import TargetModel, TargetResponse


class CloudTarget(TargetModel):
    """Integrates cloud frontier LLMs as target endpoints for adversarial red-teaming."""

    def __init__(
        self,
        provider: str = "anthropic",
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.provider = provider.lower()
        if self.provider == "anthropic":
            self.name = model_name or "claude-3-5-sonnet-20241022"
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        else:
            self.name = model_name or "gpt-4o-mini"
            self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    def send_prompt(self, prompt: str) -> TargetResponse:
        start = time.perf_counter()

        if self.provider == "anthropic":
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            payload = {
                "model": self.name,
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            }
            with httpx.Client(timeout=30.0) as client:
                res = client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                text = data["content"][0]["text"]
        else:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "content-type": "application/json",
            }
            payload = {
                "model": self.name,
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            }
            with httpx.Client(timeout=30.0) as client:
                res = client.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                text = data["choices"][0]["message"]["content"]

        latency = time.perf_counter() - start
        return TargetResponse(
            text=text,
            latency_seconds=latency,
            tokens_generated=len(text.split()),
        )
