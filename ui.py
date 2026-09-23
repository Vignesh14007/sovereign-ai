import streamlit as st
from pathlib import Path
import tempfile
from datetime import datetime

from app.agent.orchestrator import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sovereign AI Workbench",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background-color: #f4f6f8;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #e5e7eb;
}


/* ================================
   HEADINGS
================================ */

.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 3px;
}

.main-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 20px;
}


/* ================================
   CARDS
================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background-color: #ffffff;
}


/* ================================
   METRICS
================================ */

div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px;
}


/* ================================
   BUTTONS
================================ */

.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
}


/* ================================
   TEXT AREA
================================ */

textarea {
    border-radius: 10px !important;
}


/* ================================
   FILE UPLOADER
================================ */

div[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border-radius: 12px;
}


/* ================================
   SECURITY
================================ */

.security-box {
    background-color: #111827;
    border-radius: 14px;
    padding: 20px;
}

.security-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
}

.security-text {
    color: #9ca3af;
    font-size: 12px;
}


/* ================================
   TRACE
================================ */

.trace {
    background-color: #f8fafc;
    border-left: 3px solid #10b981;
    border-radius: 6px;
    padding: 9px 12px;
    margin-bottom: 6px;
    font-size: 13px;
}


/* ================================
   FOOTER
================================ */

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 11px;
    padding-top: 25px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🛡️ Sovereign AI")

    st.caption(
        "Confidential Industrial Intelligence"
    )

    st.divider()

    st.subheader("Workspace")

    if st.button(
        "＋  New Task",
        use_container_width=True,
    ):
        st.session_state.last_result = None
        st.rerun()

    st.markdown("**WORKBENCH**")

    st.write("▣  Task History")
    st.write("◈  Knowledge Base")
    st.write("▤  Generated Documents")
    st.write("◉  Audit Logs")

    st.markdown("**SYSTEM**")

    st.write("●  Local Models")
    st.write("●  System Status")
    st.write("●  Security")

    st.divider()

    st.info(
        "🔒 ON-PREMISE\n\n"
        "AI inference runs locally.\n\n"
        "No external AI APIs."
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [7, 3]
)

with header_left:

    st.markdown(
        '<div class="main-title">'
        'Sovereign AI Workbench'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Agentic multimodal AI for confidential industrial workflows'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Inference",
            "LOCAL",
        )

    with b:
        st.metric(
            "External API",
            "0",
        )

    with c:
        st.metric(
            "Data Egress",
            "0",
        )


# ============================================================
# TASK INPUT
# ============================================================

with st.container(border=True):

    st.subheader(
        "What do you want to accomplish?"
    )

    st.caption(
        "Describe an industrial task. The agent will "
        "classify the request, select the appropriate "
        "local model, retrieve knowledge, execute tools "
        "and generate the required deliverable."
    )

    request = st.text_area(
        "Task",
        placeholder=(
            "Examples:\n"
            "• Create an inspection review note for the HX-101 report.\n"
            "• Analyze this engineering drawing.\n"
            "• Calculate the average temperature using Python.\n"
            "• What was the measured wall thickness at P3?"
        ),
        height=130,
        label_visibility="collapsed",
    )


# ============================================================
# FILE UPLOAD
# ============================================================

with st.container(border=True):

    st.subheader(
        "Attach supporting data"
    )

    st.caption(
        "Upload an industrial document, image or dataset "
        "for local processing."
    )

    uploaded_file = st.file_uploader(
        "Upload file",
        type=[
            "txt",
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "csv",
        ],
        label_visibility="collapsed",
    )


# ============================================================
# PREPARE UPLOAD
# ============================================================

image_path = None

if uploaded_file is not None:

    suffix = Path(
        uploaded_file.name
    ).suffix.lower()

    upload_dir = (
        Path(tempfile.gettempdir())
        / "sovereign_ai_uploads"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_path = (
        upload_dir
        / uploaded_file.name
    )

    temp_path.write_bytes(
        uploaded_file.getbuffer()
    )

    if suffix in [
        ".png",
        ".jpg",
        ".jpeg",
    ]:
        image_path = str(temp_path)

    st.success(
        f"Attached: {uploaded_file.name}"
    )


# ============================================================
# ACTIONS
# ============================================================

run_col, clear_col, info_col = st.columns(
    [2, 1, 4]
)

with run_col:

    run_button = st.button(
        "▶  Run Agent",
        type="primary",
        use_container_width=True,
    )

with clear_col:

    clear_button = st.button(
        "Clear",
        use_container_width=True,
    )

    if clear_button:

        st.session_state.last_result = None
        st.rerun()

with info_col:

    st.caption(
        "Local orchestration  •  Local RAG  •  Local models  •  Local tools"
    )


# ============================================================
# RUN AGENT
# ============================================================

if run_button:

    if not request.strip():

        st.warning(
            "Please describe the task before running the agent."
        )

    else:

        with st.status(
            "Running Sovereign AI Agent...",
            expanded=True,
        ) as status:

            try:

                st.write(
                    "🔎 Classifying task..."
                )

                st.write(
                    "🧠 Selecting local model..."
                )

                st.write(
                    "📚 Retrieving local knowledge..."
                )

                st.write(
                    "⚙️ Executing required tools..."
                )

                st.write(
                    "✓ Generating result..."
                )

                result = run_agent(
                    request.strip(),
                    image_path=image_path,
                )

                st.session_state.last_result = result

                st.session_state.history.append(
                    {
                        "time": datetime.now().strftime(
                            "%H:%M:%S"
                        ),
                        "request": request.strip(),
                        "task_type": result.get(
                            "task_type",
                            "unknown",
                        ),
                        "model": result.get(
                            "model",
                            "unknown",
                        ),
                    }
                )

                status.update(
                    label="Agent completed successfully",
                    state="complete",
                )

            except Exception as exc:

                status.update(
                    label="Agent execution failed",
                    state="error",
                )

                st.error(
                    f"Execution error: {exc}"
                )


# ============================================================
# RESULT
# ============================================================

result = st.session_state.last_result


if result is not None:

    st.divider()

    st.header("Agent Result")

    # --------------------------------------------------------
    # RESULT METADATA
    # --------------------------------------------------------

    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "Task Type",
            result.get(
                "task_type",
                "Unknown",
            ),
        )

    with r2:

        st.metric(
            "Model Selected",
            result.get(
                "model",
                "Unknown",
            ),
        )

    with r3:

        output = result.get(
            "output"
        )

        st.metric(
            "Deliverable",
            "Generated"
            if output
            else "None",
        )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    answer = result.get(
        "answer"
    )

    if answer:

        st.subheader(
            "Result"
        )

        with st.container(border=True):

            st.markdown(
                answer
            )


    # --------------------------------------------------------
    # GENERATED REVIEW
    # --------------------------------------------------------

    generated_review = result.get(
        "generated_review"
    )

    if generated_review:

        st.subheader(
            "Generated Review"
        )

        with st.container(border=True):

            st.code(
                generated_review,
                language="text",
            )


    # --------------------------------------------------------
    # ARTIFACT
    # --------------------------------------------------------

    output_path = result.get(
        "output"
    )

    if output_path:

        output_file = Path(
            output_path
        )

        if output_file.exists():

            st.subheader(
                "Generated Deliverable"
            )

            with st.container(border=True):

                st.success(
                    f"✓ {output_file.name}"
                )

                with open(
                    output_file,
                    "rb",
                ) as file:

                    st.download_button(
                        "⬇ Download Document",
                        data=file,
                        file_name=output_file.name,
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),
                        use_container_width=True,
                    )


    # --------------------------------------------------------
    # GENERATED CODE
    # --------------------------------------------------------

    generated_code = result.get(
        "generated_code"
    )

    if generated_code:

        st.subheader(
            "Generated Code"
        )

        st.code(
            generated_code,
            language="python",
        )


    # --------------------------------------------------------
    # SANDBOX EXECUTION
    # --------------------------------------------------------

    execution = result.get(
        "execution"
    )

    if execution:

        st.subheader(
            "Sandbox Execution"
        )

        e1, e2 = st.columns(2)

        with e1:

            st.metric(
                "Status",
                execution.get(
                    "status",
                    "unknown",
                ),
            )

        with e2:

            st.metric(
                "Return Code",
                str(
                    execution.get(
                        "returncode",
                        "-",
                    )
                ),
            )

        stdout = execution.get(
            "stdout"
        )

        stderr = execution.get(
            "stderr"
        )

        if stdout:

            st.write(
                "**Output**"
            )

            st.code(
                stdout,
                language="text",
            )

        if stderr:

            st.error(
                stderr
            )


    # --------------------------------------------------------
    # AGENT TRACE
    # --------------------------------------------------------

    trace = result.get(
        "trace",
        [],
    )

    if trace:

        st.subheader(
            "Agent Execution Trace"
        )

        with st.expander(
            "View execution steps",
            expanded=False,
        ):

            for item in trace:

                st.markdown(
                    f"✓ {item}"
                )


# ============================================================
# RECENT TASKS
# ============================================================

if st.session_state.history:

    st.divider()

    st.header(
        "Recent Tasks"
    )

    for item in reversed(
        st.session_state.history[-5:]
    ):

        request_text = item[
            "request"
        ]

        if len(request_text) > 75:

            request_text = (
                request_text[:75]
                + "..."
            )

        with st.expander(
            f"{item['time']}  •  {request_text}"
        ):

            h1, h2 = st.columns(2)

            with h1:

                st.write(
                    f"**Task:** {item['task_type']}"
                )

            with h2:

                st.write(
                    f"**Model:** {item['model']}"
                )


# ============================================================
# SOVEREIGNTY PANEL
# ============================================================

st.divider()

st.subheader(
    "🛡️ Sovereignty & Security"
)

security_columns = st.columns(5)

security_data = [
    ("AI Inference", "Local / On-Premise"),
    ("External AI APIs", "0"),
    ("Cloud Dependency", "0"),
    ("Knowledge", "Local RAG"),
    ("Audit", "Local Logs"),
]

for column, (label, value) in zip(
    security_columns,
    security_data,
):

    with column:

        st.metric(
            label,
            value,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    Sovereign AI Workbench • SIH26117<br>
    Confidential Industrial Intelligence • Local Processing
</div>
""",
    unsafe_allow_html=True,
)
