"""Streamlit app for PaperLens — AI-powered paper explainer."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from llm import explain_paper
from parse import extract_text_from_pdf, truncate_text_for_model
from utils import truncate_preview

st.set_page_config(page_title="PaperLens", layout="centered")
st.title("PaperLens")
st.markdown(
    "Upload a paper PDF or paste text and get a **structured explanation**: summary, research problem, "
    "key contributions, method, assumptions, limitations, and a suggested reading path."
)
st.divider()

# Source text: from PDF or manual paste
source_text = ""
pdf_upload = st.file_uploader("Upload PDF", type=["pdf"])
if pdf_upload:
    try:
        source_text = extract_text_from_pdf(pdf_upload)
        st.success("PDF text extracted.")
    except ValueError as e:
        st.error(str(e))
        source_text = ""

st.caption("Or paste paper text manually (overrides PDF if both are provided).")
manual_text = st.text_area(
    "Paste full text",
    height=120,
    placeholder="Paste paper or section text here…",
    label_visibility="collapsed",
)
if manual_text and manual_text.strip():
    source_text = manual_text.strip()
    if pdf_upload:
        st.info("Using manually pasted text (PDF text ignored).")

if source_text:
    preview = truncate_preview(source_text)
    with st.expander("Extracted / pasted text preview", expanded=False):
        st.text(preview)

st.divider()

# Optional: explanation style
style_options = ["standard", "concise", "deeper technical"]
explanation_style = st.radio(
    "Explanation style",
    options=style_options,
    index=0,
    horizontal=True,
    help="Concise: shorter bullets. Standard: balanced. Deeper technical: more detail on methods and formalism.",
)

explain_clicked = st.button("Explain Paper", type="primary")

if explain_clicked:
    if not source_text or not source_text.strip():
        st.error("Please upload a PDF or paste paper text first.")
    else:
        paper_input = truncate_text_for_model(source_text.strip())
        with st.spinner("Explaining paper…"):
            try:
                result = explain_paper(
                    paper_text=paper_input,
                    style_hint=explanation_style if explanation_style != "standard" else None,
                )
            except ValueError as e:
                st.error(str(e))
                result = None

        if result:
            st.divider()
            st.subheader("Paper Title")
            st.caption(result.title or "—")

            st.subheader("Summary")
            st.write(result.summary)

            st.subheader("Research Problem")
            st.write(result.research_problem)

            st.subheader("Why It Matters")
            st.write(result.why_it_matters)

            st.subheader("Paper Type")
            st.caption(result.paper_type)

            st.subheader("Key Contributions")
            for c in result.key_contributions:
                st.markdown(f"**{c.title}** — {c.explanation}")

            st.subheader("Method Overview")
            st.write(result.method_overview)

            st.subheader("Main Results")
            for r in result.main_results:
                st.markdown(f"- {r}")
            if not result.main_results:
                st.caption("None listed.")

            st.subheader("Assumptions")
            for a in result.assumptions:
                st.markdown(f"- {a}")
            if not result.assumptions:
                st.caption("None listed.")

            st.subheader("Limitations")
            for lim in result.limitations:
                sig = f" — *{lim.significance}*" if lim.significance else ""
                st.markdown(f"- {lim.limitation}{sig}")
            if not result.limitations:
                st.caption("None listed.")

            st.subheader("Reading Guide")
            for i, step in enumerate(result.reading_guide, 1):
                st.markdown(f"{i}. {step}")

            st.subheader("Confidence")
            st.caption(result.confidence)
