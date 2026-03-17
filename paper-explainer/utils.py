"""Utility helpers for the paper explainer app."""

from __future__ import annotations


def truncate_preview(text: str, max_chars: int = 2000) -> str:
    """Truncate text for UI preview with an indicator if shortened."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n\n… (truncated)"
