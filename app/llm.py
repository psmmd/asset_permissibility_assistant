from dataclasses import dataclass
from functools import cache

import anthropic
from pydantic import BaseModel

from app.config import settings


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0  # includes thinking tokens, which are billed as output

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(self.input_tokens + other.input_tokens, self.output_tokens + other.output_tokens)


@cache
def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


def parse[T: BaseModel](
    system: str, user: str, output_format: type[T], effort: str, model: str | None = None
) -> tuple[T, Usage]:
    """One Claude call with structured output, validated against a Pydantic model."""
    response = get_client().messages.parse(
        model=model or settings.llm_model,
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=output_format,
        output_config={"effort": effort},
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise RuntimeError(f"No structured output (stop_reason={response.stop_reason})")
    usage = Usage(response.usage.input_tokens, response.usage.output_tokens)
    return response.parsed_output, usage
