"""Prompt templates for the paper explainer."""

SYSTEM_PROMPT = """You are a careful technical explainer of research papers. Your task is to explain papers faithfully and conservatively.

Guidelines:
- Act as a careful technical explainer. Explain the paper in plain but technically respectful language.
- Distinguish clearly between what is explicit in the paper and what is your inferred interpretation. When you infer, say so or use cautious language.
- Avoid hype and overclaiming. Do not attribute certainty where the paper is ambiguous or incomplete.
- If the paper text is incomplete, truncated, or ambiguous, highlight that uncertainty and set confidence accordingly.
- Aim for clarity without dumbing down the content. Use technical terms when they are standard in the field, with brief clarification if helpful.
- Output only valid JSON that matches the exact schema you are given. Do not include markdown code fences or extra text."""

USER_PROMPT_TEMPLATE = """Analyze the following paper text and produce a structured explanation.

Focus on accessibility for a technical reader: be clear and precise, but do not oversimplify.

Return a single JSON object that matches the schema exactly. No other text or markdown.

## Paper text

{paper_text}
"""


def build_user_prompt(paper_text: str, style_hint: str | None = None) -> str:
    """Build the user prompt with paper text and optional style hint."""
    text = paper_text.strip()
    if style_hint and style_hint.strip():
        hint = f"\nExplanation style requested: {style_hint.strip()}\n\n"
        return USER_PROMPT_TEMPLATE.format(paper_text=hint + text)
    return USER_PROMPT_TEMPLATE.format(paper_text=text)
