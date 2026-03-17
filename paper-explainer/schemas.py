"""Pydantic models for paper explanation output."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ContributionItem(BaseModel):
    """A single key contribution with title and explanation."""

    title: str
    explanation: str


class LimitationItem(BaseModel):
    """A limitation or constraint with optional significance."""

    limitation: str
    significance: str | None = None


class PaperExplanation(BaseModel):
    """Structured explanation of a research paper."""

    title: str | None = None
    summary: str
    research_problem: str
    why_it_matters: str
    paper_type: Literal["theoretical", "empirical", "mixed", "unclear"]
    key_contributions: list[ContributionItem]
    method_overview: str
    main_results: list[str]
    assumptions: list[str]
    limitations: list[LimitationItem]
    reading_guide: list[str]
    confidence: Literal["low", "medium", "high"]
