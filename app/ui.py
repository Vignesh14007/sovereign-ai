import streamlit as st
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.agent.orchestrator import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sovereign AI Workbench",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .brand {
        text-align: center;
        margin-bottom: 2.5rem;
    }

    .brand-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .brand-subtitle {
        font-size: 16px;
        color: #888;
    }

    .answer-box {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 14px;
        padding: 24px;
        margin-top: 25px;
    }

    .result-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .status {
        text-align: center;
        color: #21c55d;
        font-size: 13px;
        margin-top: 12px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="brand">
    <div class="brand-title">🛡️ Sovereign AI Workbench</div>
    <div class="brand-subtitle">
        Confidential Industrial Intelligence
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT
# ============================================================

request = st.text_area(
    "Your request",
    placeholder=(
        "Ask an industrial question or describe a task...\n\n"
        "For example:\n"
        "What was the highest gross crude throughput in FY 2022-23?"
    ),
    height=150,
    label_visibility="collapsed",
)


uploaded_file = st.file_uploader(
    "Upload a document or image",
    type=["png", "jpg", "jpeg", "pdf", "txt"],
)


# ============================================================
# RUN
# ============================================================

run_button = st.button(
    "Run",
    type="primary",
    use_container_width=True,
)


if run_button:

    if not request.strip():
        st.warning("Please enter a question or task.")
        st.stop()

    image_path = None

    if uploaded_file is not None:

        input_dir = BASE_DIR / "data" / "input"
        input_dir.mkdir(parents=True, exist_ok=True)

        image_path = input_dir / uploaded_file.name

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    with st.spinner("Processing..."):

        try:

            result = run_agent(
                request=request.strip(),
                image_path=str(image_path) if image_path else None,
            )

        except Exception as e:
            st.error(
                "Something went wrong while processing your request."
            )
            st.stop()


    # ========================================================
    # RESULT
    # ========================================================

    answer = result.get("answer", "")

    if answer:

        st.markdown("""
        <div class="answer-box">
            <div class="result-title">Result</div>
        """, unsafe_allow_html=True)

        st.write(answer)

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # GENERATED REVIEW
    # ========================================================

    generated_review = result.get("generated_review")

    if generated_review:

        st.markdown("""
        <div class="answer-box">
            <div class="result-title">Review</div>
        """, unsafe_allow_html=True)

        st.text(generated_review)

        st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # GENERATED DELIVERABLE
    # ========================================================

    output_path = result.get("output")

    if output_path and Path(output_path).exists():

        st.markdown("<br>", unsafe_allow_html=True)

        with open(output_path, "rb") as f:
            st.download_button(
                "Download Document",
                data=f.read(),
                file_name=Path(output_path).name,
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="status">● Secure local workspace</div>',
    unsafe_allow_html=True,
)
