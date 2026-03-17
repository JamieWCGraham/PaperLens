"""OpenAI API integration for paper explanation with structured output."""

from __future__ import annotations

import json
import os

from openai import OpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import PaperExplanation


def explain_paper(paper_text: str, style_hint: str | None = None) -> PaperExplanation:
    """
    Call the OpenAI API to explain a paper and return a validated structured result.

    Uses the API with JSON mode and Pydantic validation to produce structured output
    compatible with the Responses API structured-output pattern.

    Args:
        paper_text: The full or truncated paper text to explain.
        style_hint: Optional explanation style (e.g. "concise", "deeper technical").

    Returns:
        Parsed and validated PaperExplanation.

    Raises:
        ValueError: If the API key is missing, the API call fails, or the response
            cannot be parsed into PaperExplanation.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError(
            "OPENAI_API_KEY is not set. Add it to a .env file or set the environment variable."
        )

    client = OpenAI(api_key=api_key)
    user_content = build_user_prompt(paper_text, style_hint)

    schema_instruction = (
        "Schema: PaperExplanation with fields: title (string or null), summary (string), "
        "research_problem (string), why_it_matters (string), paper_type (one of: theoretical, empirical, mixed, unclear), "
        "key_contributions (array of { title: string, explanation: string }), method_overview (string), "
        "main_results (array of strings), assumptions (array of strings), "
        "limitations (array of { limitation: string, significance: string or null }), "
        "reading_guide (array of strings), confidence (one of: low, medium, high)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + schema_instruction},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
        )
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "insufficient_quota" in err_str or "rate limit" in err_str:
            raise ValueError(
                "OpenAI API quota exceeded. Check your plan and billing at "
                "https://platform.openai.com/account/billing."
            ) from e
        raise ValueError(f"API request failed: {e}") from e

    choice = response.choices[0] if response.choices else None
    if not choice or not getattr(choice.message, "content", None):
        raise ValueError("Empty or invalid response from the model.")

    raw_content = choice.message.content.strip()
    if raw_content.startswith("```"):
        lines = raw_content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw_content = "\n".join(lines)

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model output is not valid JSON: {e}") from e

    try:
        return PaperExplanation.model_validate(data)
    except Exception as e:
        raise ValueError(f"Model output does not match expected schema: {e}") from e
