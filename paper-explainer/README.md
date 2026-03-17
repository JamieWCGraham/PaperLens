# PaperLens

A lightweight local-first prototype of an **AI-powered paper explainer**. Upload a paper PDF or paste text and receive a structured explanation: summary, research problem, why it matters, key contributions, method overview, assumptions, limitations, main results, reading guide, and confidence.

## Stack

- **Streamlit** — UI
- **Python** — app and logic
- **OpenAI API** — structured explanation (JSON mode + Pydantic validation; compatible with Responses API usage)
- **Pydantic** — output schema
- **PyMuPDF** — PDF text extraction
- **python-dotenv** — environment variables

## Install

```bash
cd paper-explainer
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## API key

1. Copy `.env.example` to `.env`.
2. Set your key in `.env`:

   ```
   OPENAI_API_KEY=your_key_here
   ```

Do not commit `.env`; it is listed in `.gitignore`.

## Run

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Usage

1. Either **upload a PDF** or **paste paper text** in the text area (paste overrides PDF).
2. Optionally choose explanation style: **concise**, **standard**, or **deeper technical**.
3. Click **Explain Paper**.
4. Read the structured output: summary, research problem, contributions, method, results, assumptions, limitations, reading guide, and confidence.

## Known limitations

- **No chat** — single-shot explanation only; no follow-up questions over the paper.
- **Text-only PDFs** — extraction is via PyMuPDF; scanned PDFs (images) are not supported (no OCR).
- **Length** — very long papers are truncated (~120k characters) so the model can respond; explanation is based on the beginning of the paper.
- **No persistence** — no database, saved history, or auth; everything is in-memory for the session.
- **Local only** — V1 is intended for local use; no cloud deployment or multi-user setup.
