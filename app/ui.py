import streamlit as st

from app.auth.session import (
    initialize_session,
    is_authenticated,
    is_admin,
    is_employee,
    get_current_user,
    logout_user,
    has_permission,
)

from app.auth.ui import render_auth_ui

from app.auth.history import (
    create_history_record,
    get_employee_history,
)

from app.agent.orchestrator import run_agent
from app.admin.panel import render_admin_panel


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sovereign AI Workbench",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# GLOBAL SESSION INITIALIZATION
# ============================================================

initialize_session()


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .main-subtitle {
        font-size: 16px;
        opacity: 0.70;
        margin-bottom: 25px;
    }

    .secure-status {
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid rgba(0, 180, 100, 0.25);
        background: rgba(0, 180, 100, 0.06);
        margin-top: 20px;
    }

    .history-card {
        padding: 15px;
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 12px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

def render_header():

    col1, col2 = st.columns(
        [5, 1]
    )

    with col1:

        st.markdown(
            '<div class="main-title">'
            '🛡️ Sovereign AI Workbench'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="main-subtitle">'
            'Confidential Industrial Intelligence'
            '</div>',
            unsafe_allow_html=True,
        )

    with col2:

        if st.button(
            "Logout",
            use_container_width=True,
        ):

            logout_user()
            st.rerun()


# ============================================================
# EMPLOYEE SIDEBAR
# ============================================================

def render_employee_sidebar():

    user = get_current_user()

    st.sidebar.markdown(
        "### 👤 Employee"
    )

    st.sidebar.write(
        f"**{user.get('name', 'Employee')}**"
    )

    st.sidebar.caption(
        user.get("email", "")
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Workspace",
        [
            "AI Workbench",
            "My History",
            "My Profile",
        ],
    )

    st.sidebar.divider()

    st.sidebar.success(
        "● Secure local workspace"
    )

    return page


# ============================================================
# EMPLOYEE AI WORKBENCH
# ============================================================

def render_employee_workbench():

    st.subheader(
        "🤖 AI Workbench"
    )

    st.write(
        "Ask questions about authorized industrial "
        "documents, operational information and "
        "available local AI tools."
    )

    if not has_permission("ai"):

        st.warning(
            "Your account does not currently have "
            "AI Workbench permission."
        )

        return

    request = st.text_area(
        "Enter your request",
        placeholder=(
            "Example: What was the highest gross crude "
            "throughput achieved by MRPL in FY 2022-23?"
        ),
        height=140,
    )

    uploaded_file = st.file_uploader(
        "Optional document or image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "pdf",
            "txt",
        ],
    )

    if st.button(
        "Run AI",
        type="primary",
        use_container_width=True,
    ):

        if not request.strip():

            st.warning(
                "Please enter a request."
            )

            return

        user = get_current_user()

        image_path = None

        if uploaded_file:

            input_dir = (
                "data/input"
            )

            import os

            os.makedirs(
                input_dir,
                exist_ok=True,
            )

            file_path = os.path.join(
                input_dir,
                uploaded_file.name,
            )

            with open(
                file_path,
                "wb",
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            image_path = file_path

        try:

            with st.spinner(
                "Processing with local AI..."
            ):

                if image_path:

                    result = run_agent(
                        request,
                        image_path=image_path,
                    )

                else:

                    result = run_agent(
                        request
                    )

            response_text = result.get("answer", "No answer available.")

            create_history_record(
                employee_id=user["id"],
                request=request,
                task_type=None,
                response=response_text,
                source_documents=(
                    uploaded_file.name
                    if uploaded_file
                    else None
                ),
                execution_status="completed",
            )

            st.success(
                "Request completed."
            )

            st.markdown(
                "### Result"
            )

            st.write(
                response_text
            )

        except Exception as error:

            error_text = str(error)

            create_history_record(
                employee_id=user["id"],
                request=request,
                task_type=None,
                response=error_text,
                source_documents=(
                    uploaded_file.name
                    if uploaded_file
                    else None
                ),
                execution_status="failed",
            )

            st.error(
                "The request could not be completed."
            )

            st.exception(error)


# ============================================================
# EMPLOYEE HISTORY
# ============================================================

def render_employee_history():

    st.subheader(
        "📚 My History"
    )

    user = get_current_user()

    history = get_employee_history(
        user["id"],
        limit=50,
    )

    if not history:

        st.info(
            "You have no previous AI requests."
        )

        return

    st.caption(
        f"{len(history)} recent request(s)"
    )

    for record in history:

        created_at = record.get(
            "created_at",
            "",
        )

        request = record.get(
            "request",
            "",
        )

        response = record.get(
            "response",
            "",
        )

        status = record.get(
            "execution_status",
            "completed",
        )

        with st.expander(
            f"{created_at} — {status.upper()}"
        ):

            st.markdown(
                "**Request**"
            )

            st.write(
                request
            )

            st.markdown(
                "**Response**"
            )

            st.write(
                response
            )

            source = record.get(
                "source_documents"
            )

            if source:

                st.markdown(
                    f"**Source:** {source}"
                )


# ============================================================
# EMPLOYEE PROFILE
# ============================================================

def render_employee_profile():

    st.subheader(
        "👤 My Profile"
    )

    user = get_current_user()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"**Name**  \n"
            f"{user.get('name', '')}"
        )

        st.markdown(
            f"**Employee ID**  \n"
            f"{user.get('id', '')}"
        )

    with col2:

        st.markdown(
            f"**Email**  \n"
            f"{user.get('email', '')}"
        )

        st.markdown(
            "**Role**  \n"
            "Employee"
        )

    st.divider()

    st.markdown(
        "### 🔑 Permissions"
    )

    permissions = [
        ("AI Workbench", "ai"),
        ("Documents", "documents"),
        ("Reports", "reports"),
        ("Code Execution", "code_execution"),
        (
            "Sensitive Documents",
            "sensitive_documents",
        ),
    ]

    for label, permission in permissions:

        if has_permission(permission):

            st.success(
                f"✓ {label}"
            )

        else:

            st.info(
                f"○ {label}"
            )


# ============================================================
# EMPLOYEE WORKSPACE
# ============================================================

def render_employee_workspace():

    render_header()

    page = render_employee_sidebar()

    if page == "AI Workbench":

        render_employee_workbench()

    elif page == "My History":

        render_employee_history()

    elif page == "My Profile":

        render_employee_profile()


# ============================================================
# ADMIN WORKSPACE
# ============================================================

def render_admin_workspace():

    render_header()

    st.sidebar.markdown(
        "### 🔐 Administrator"
    )

    user = get_current_user()

    st.sidebar.write(
        f"**{user.get('name', 'Administrator')}**"
    )

    st.sidebar.caption(
        user.get("email", "")
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Administration",
        [
            "Admin Panel",
        ],
    )

    st.sidebar.divider()

    st.sidebar.success(
        "● Secure local workspace"
    )

    if page == "Admin Panel":

        render_admin_panel()


# ============================================================
# APPLICATION ROUTER
# ============================================================

if not is_authenticated():

    render_auth_ui()

elif is_admin():

    render_admin_workspace()

elif is_employee():

    render_employee_workspace()

else:

    logout_user()

    st.rerun()
