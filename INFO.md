Yes. Here’s a matching **Cursor spec** for a lightweight **Paper Explainer** prototype in the same style and with the same stack philosophy.

---

# Project Summary

## Project: Paper Explainer

### Overview

Paper Explainer is a lightweight AI-assisted research tool that helps users understand technical papers more quickly and clearly.

The tool takes in a PDF or pasted paper text and produces a structured explanation of the paper in plain but technically respectful language. Rather than only summarizing the abstract, it aims to help the reader understand the paper’s core problem, main contribution, method, assumptions, results, and limitations.

The first version is designed as a simple interactive app for students, researchers, engineers, and self-directed learners reading papers in machine learning, physics, applied math, or related technical fields.

### Core User Problem

Research papers are often difficult to parse because they assume background context, compress motivation, and present methods/results in dense language.

Readers often want help answering:

* what problem is this paper trying to solve
* why this problem matters
* what the main contribution actually is
* how the method works at a high level
* what assumptions or limitations matter
* whether the paper is theoretical, empirical, or both
* what to pay attention to if reading the full paper

The tool aims to reduce this friction by turning dense paper text into a structured explanation.

### Initial Target User

The initial user is a technically capable reader of research papers, such as:

* graduate students
* researchers entering a new area
* engineers reading academic work for applied insight
* self-directed learners in technical fields

### V1 Scope

The first version should do only a few things:

1. accept PDF upload or pasted paper text
2. extract and display paper text
3. send the text or truncated text to an LLM
4. return structured output with:

   * paper summary
   * central question/problem
   * key contributions
   * method overview
   * assumptions and limitations
   * main results
   * suggested reading path

### Why This Project

This is a good first experiment because it is:

* small in scope
* broadly useful
* aligned with technical and research interests
* feasible with a lightweight Python stack
* a good exercise in structured LLM product design

### Non-Goals for V1

The first version should not try to:

* be a full literature review assistant
* retrieve related papers
* generate citation graphs
* answer arbitrary deep follow-up questions across many documents
* support accounts, saved history, or collaboration
* guarantee perfect interpretation of every technical detail

This is an explainer, not a complete research agent.

---

# Cursor Spec

## Paper Explainer — Cursor Build Spec

### Goal

Build a lightweight local-first prototype of an AI-powered paper explainer using:

* Streamlit
* Python
* OpenAI Responses API
* Pydantic
* PyMuPDF
* python-dotenv

The app should let a user upload a paper PDF or paste paper text and receive a structured explanation of the paper.

---

## Product Requirements

### Main User Flow

The user should be able to:

1. open the Streamlit app
2. either:

   * upload a PDF, or
   * paste paper text manually
3. view extracted text from the PDF
4. click **Explain Paper**
5. receive a structured explanation containing:

   * concise summary
   * research problem
   * why it matters
   * key contributions
   * method overview
   * assumptions / limitations
   * main findings
   * recommended way to read the paper

### UX Principles

* Keep the interface minimal
* Make output highly scannable
* Use technical language carefully but accessibly
* Distinguish between what is explicit in the paper and what is inferred
* Avoid overclaiming certainty

---

## Technical Stack

### Required Libraries

Use:

* `streamlit`
* `openai`
* `pydantic`
* `pymupdf`
* `python-dotenv`

Optional:

* `pandas` only if useful later
* no database for V1

### Environment

Use a `.env` file with:

```bash
OPENAI_API_KEY=your_key_here
```

---

## File Structure

Use this structure:

```text
paper-explainer/
│
├── app.py
├── llm.py
├── parse.py
├── schemas.py
├── prompts.py
├── utils.py
├── requirements.txt
├── .env
└── README.md
```

---

## Functional Requirements

### 1. PDF Parsing

Implement PDF parsing in `parse.py`.

Requirements:

* extract text from uploaded PDF using PyMuPDF
* concatenate pages into a single string
* preserve enough spacing/newlines for readability
* handle parsing failures gracefully

Functions:

* `extract_text_from_pdf(uploaded_file) -> str`

Optional helper:

* `truncate_text_for_model(text: str, max_chars: int = ...) -> str`

For V1, simple truncation is acceptable if the paper is too long.

---

### 2. Structured Output Schema

Implement Pydantic models in `schemas.py`.

Use models similar to:

```python
from typing import Literal, List
from pydantic import BaseModel

class ContributionItem(BaseModel):
    title: str
    explanation: str

class LimitationItem(BaseModel):
    limitation: str
    significance: str | None = None

class PaperExplanation(BaseModel):
    title: str | None = None
    summary: str
    research_problem: str
    why_it_matters: str
    paper_type: Literal["theoretical", "empirical", "mixed", "unclear"]
    key_contributions: List[ContributionItem]
    method_overview: str
    main_results: List[str]
    assumptions: List[str]
    limitations: List[LimitationItem]
    reading_guide: List[str]
    confidence: Literal["low", "medium", "high"]
```

The model should enforce predictable structure.

---

### 3. Prompt Design

Implement prompts in `prompts.py`.

Need:

* one system prompt
* one user prompt template

The system prompt should instruct the model to:

* act as a careful technical explainer
* explain the paper faithfully and conservatively
* distinguish explicit claims from inferred interpretation
* avoid hype
* highlight uncertainty if the paper text is incomplete or ambiguous
* aim for clarity without dumbing down the content

The user prompt should include:

* paper text
* optional instructions such as “focus on accessibility for a technical reader”
* explicit instruction to return structured JSON matching schema

---

### 4. LLM Integration

Implement OpenAI call in `llm.py`.

Requirements:

* call the OpenAI Responses API
* use structured output aligned with the Pydantic schema
* return parsed validated object
* handle API failures gracefully

Function:

* `explain_paper(paper_text: str) -> PaperExplanation`

---

### 5. Streamlit App

Implement the UI in `app.py`.

Sections:

* title and short description
* PDF upload
* extracted text preview
* manual text paste option
* explain button
* structured results display

Display output in sections:

* Paper Title
* Summary
* Research Problem
* Why It Matters
* Paper Type
* Key Contributions
* Method Overview
* Main Results
* Assumptions
* Limitations
* Reading Guide
* Confidence

Optional V1 control:

* a radio/select box for explanation style:

  * concise
  * standard
  * deeper technical

But keep it simple if it adds friction.

---

### 6. Error Handling

The app should:

* show a friendly error if no input text is provided
* show a friendly error if the PDF cannot be parsed
* handle empty model responses
* handle invalid structured output
* avoid crashing on malformed input

---

## Output Behavior

The model output should feel like this:

### Summary

A concise but meaningful overview of the paper.

### Research Problem

What question or challenge the paper addresses.

### Why It Matters

Why the problem is important in the field or in practice.

### Paper Type

One of:

* theoretical
* empirical
* mixed
* unclear

### Key Contributions

A short list of the main contributions, each with explanation.

### Method Overview

A high-level explanation of how the paper approaches the problem.

### Main Results

A list of the main outcomes, findings, or claims.

### Assumptions

A list of assumptions, prerequisites, or framing choices.

### Limitations

A list of weaknesses, open questions, or constraints.

### Reading Guide

A suggested path for a reader, for example:

* start with abstract and introduction
* focus on section 2 for problem setup
* skim theorem proofs on first pass
* pay close attention to experiment section

### Confidence

Low / medium / high depending on how clearly the paper text supports the explanation.

---

## Non-Goals

Do not implement in V1:

* chat over the paper
* multi-document comparison
* citation retrieval
* related work search
* vector DB
* auth
* saved history
* OCR for scanned PDFs
* detailed figure parsing
* symbolic math support
* cloud deployment

---

## Acceptance Criteria

The app is successful if:

1. a user can upload a PDF and extract text
2. a user can paste paper text manually
3. clicking the button returns a structured paper explanation
4. the output is readable and segmented
5. the app handles common failures gracefully
6. the app runs locally with minimal setup

---

## Suggested Implementation Order

### Phase 1

* create file structure
* install dependencies
* set up `.env`
* build Pydantic schema

### Phase 2

* implement OpenAI call with mocked paper text
* validate structured output parsing

### Phase 3

* implement PDF extraction and truncation helper

### Phase 4

* build Streamlit UI

### Phase 5

* polish formatting and error handling

---

## README Requirements

The README should include:

* what the project does
* the lightweight stack
* how to install dependencies
* how to add the API key
* how to run the app
* known limitations

---

## Cursor Instruction Block

You can paste this directly into Cursor:

```text
Build a lightweight local-first prototype called Paper Explainer.

Tech stack:
- Python
- Streamlit
- OpenAI Responses API
- Pydantic
- PyMuPDF
- python-dotenv

Goal:
Create a simple app where a user can upload a paper PDF or paste paper text and receive a structured explanation of the paper.

The app should:
1. accept PDF upload
2. extract text from the PDF
3. allow manual pasted text as an alternative input
4. send the paper text to an LLM
5. return structured output with:
   - title
   - summary
   - research problem
   - why it matters
   - paper type
   - key contributions
   - method overview
   - main results
   - assumptions
   - limitations
   - reading guide
   - confidence

Use this file structure:
- app.py
- llm.py
- parse.py
- schemas.py
- prompts.py
- utils.py
- requirements.txt
- README.md

Implementation requirements:
- use PyMuPDF for PDF text extraction
- use Pydantic for output schema validation
- use OpenAI Responses API for generation
- use a clean Streamlit UI
- handle errors gracefully
- keep code modular and simple
- no database, auth, vector DB, OCR, or cloud deployment in V1

Pydantic schema should include:
- ContributionItem
- LimitationItem
- PaperExplanation

The model should be instructed to explain conservatively, distinguish explicit claims from inferred interpretation, and state uncertainty when necessary.

Return code that is clean, minimal, and runnable locally.
```

---

## One slight upgrade I’d recommend

For the paper explainer, I’d add one extra field:

* `who_this_is_for: str`

Example:

* “Best for readers with background in linear algebra and optimization”
* “Accessible to ML practitioners but harder for readers without PDE background”

That makes the output feel more genuinely useful than a generic summary.

If you want, I can also do a **third version** for the **Intellectual Lineage Explainer**, which is probably the most differentiated of the three.
