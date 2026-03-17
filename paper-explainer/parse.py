"""PDF text extraction using PyMuPDF."""

from __future__ import annotations

import io

import pymupdf


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file.

    Args:
        uploaded_file: A file-like object (e.g. Streamlit UploadedFile) with .read() and .name.

    Returns:
        Concatenated text from all pages, with spacing preserved for readability.

    Raises:
        ValueError: If the file cannot be opened or parsed as a PDF.
    """
    if uploaded_file is None:
        raise ValueError("No file provided.")

    raw = uploaded_file.read()
    if not raw:
        raise ValueError("The uploaded file is empty.")

    try:
        doc = pymupdf.open(stream=raw, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Cannot open PDF: {e}") from e

    try:
        parts = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                parts.append(text)
            parts.append("\n")
        doc.close()
        result = "\n".join(p.strip() for p in parts if p.strip()) if parts else ""
        return result.strip() or "(No text extracted from PDF.)"
    except Exception as e:
        if "doc" in dir():
            doc.close()
        raise ValueError(f"Error extracting text from PDF: {e}") from e


def truncate_text_for_model(text: str, max_chars: int = 120_000) -> str:
    """
    Truncate paper text to fit within model context, preserving the start of the paper.

    For V1, simple truncation is used. The beginning of the paper (abstract, intro)
    is usually most important for explanation.

    Args:
        text: Full extracted paper text.
        max_chars: Maximum character count (default ~120k to leave room for prompt and output).

    Returns:
        Text truncated to at most max_chars, with a truncation notice if shortened.
    """
    if not text or len(text) <= max_chars:
        return (text or "").strip()
    return text[:max_chars].rstrip() + "\n\n[Text truncated for length. Explanation is based on the portion above.]"
