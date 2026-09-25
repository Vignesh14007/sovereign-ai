import streamlit as st

from app.auth.service import (
    authenticate_admin,
    authenticate_employee,
    activate_employee_first_login,
)
from app.auth.session import (
    login_user,
)


# ============================================================
# PAGE STYLING
# ============================================================

def render_auth_styles():

    st.markdown(
        """
        <style>

        .auth-container {
            max-width: 850px;
            margin: 0 auto;
            padding-top: 50px;
        }

        .auth-title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .auth-subtitle {
            text-align: center;
            font-size: 18px;
            opacity: 0.75;
            margin-bottom: 45px;
        }

        .role-card {
            padding: 25px;
            border: 1px solid rgba(128,128,128,0.25);
            border-radius: 16px;
            text-align: center;
            min-height: 190px;
        }

        .role-icon {
            font-size: 42px;
            margin-bottom: 10px;
        }

        .role-title {
            font-size: 23px;
            font-weight: 600;
        }

        .role-description {
            font-size: 15px;
            opacity: 0.7;
            margin-top: 8px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN AUTH SCREEN
# ============================================================

def render_authentication():

    render_auth_styles()

    st.markdown(
        '<div class="auth-container">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-title">🛡️ Sovereign AI Workbench</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="auth-subtitle">'
        'Confidential Industrial Intelligence'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Select your access")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">🔐</div>
                <div class="role-title">Administrator</div>
                <div class="role-description">
                    Manage employees, permissions,
                    knowledge base and system controls.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Continue as Administrator",
            use_container_width=True,
            key="admin_role",
        ):

            st.session_state.auth_mode = "admin_login"
            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">👤</div>
                <div class="role-title">Employee</div>
                <div class="role-description">
                    Access AI tools, documents,
                    reports and your personal history.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Continue as Employee",
            use_container_width=True,
            key="employee_role",
        ):

            st.session_state.auth_mode = "employee_login"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ADMIN LOGIN
# ============================================================

def render_admin_login():

    st.markdown("## 🔐 Administrator Login")

    st.caption(
        "Authorized administrators only."
    )

    with st.form("admin_login_form"):

        email = st.text_input(
            "Administrator Email",
            placeholder="admin@company.local",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:

        if not email or not password:

            st.error(
                "Please enter your email and password."
            )
            return

        user = authenticate_admin(
            email=email.strip(),
            password=password,
        )

        if user:

            login_user(
                user=user,
                role="admin",
            )

            st.success(
                "Administrator login successful."
            )

            st.rerun()

        else:

            st.error(
                "Invalid administrator credentials."
            )

    if st.button(
        "← Back",
        key="admin_back",
    ):

        st.session_state.auth_mode = "role_selection"
        st.rerun()


# ============================================================
# EMPLOYEE LOGIN
# ============================================================

def render_employee_login():

    st.markdown("## 👤 Employee Login")

    st.caption(
        "Use your registered company email."
    )

    with st.form("employee_login_form"):

        email = st.text_input(
            "Employee Email",
            placeholder="employee@company.local",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:

        if not email:

            st.error(
                "Please enter your employee email."
            )
            return

        user = authenticate_employee(
            email=email.strip(),
            password=password,
        )

        if user:

            if user.get("requires_activation"):

                st.session_state.activation_employee = user
                st.session_state.auth_mode = (
                    "employee_activation"
                )
                st.rerun()

            else:

                login_user(
                    user=user,
                    role="employee",
                )

                st.success(
                    "Employee login successful."
                )

                st.rerun()

        else:

            st.error(
                "Invalid employee credentials or inactive account."
            )

    if st.button(
        "← Back",
        key="employee_back",
    ):

        st.session_state.auth_mode = "role_selection"
        st.rerun()


# ============================================================
# FIRST-TIME EMPLOYEE ACTIVATION
# ============================================================

def render_employee_activation():

    employee = st.session_state.get(
        "activation_employee"
    )

    if not employee:

        st.session_state.auth_mode = (
            "employee_login"
        )
        st.rerun()
        return

    st.markdown(
        "## 🔑 First-Time Employee Setup"
    )

    st.info(
        "Your employee account has been created "
        "and enabled by an administrator. "
        "Set your personal password to activate "
        "your account."
    )

    st.markdown(
        f"**Employee:** {employee.get('name', '')}"
    )

    st.markdown(
        f"**Email:** {employee.get('email', '')}"
    )

    with st.form("employee_activation_form"):

        new_password = st.text_input(
            "Create Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Activate Account",
            use_container_width=True,
        )

    if submitted:

        if not new_password:

            st.error(
                "Please create a password."
            )
            return

        if len(new_password) < 8:

            st.error(
                "Password must contain at least 8 characters."
            )
            return

        if new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )
            return

        result = activate_employee_first_login(
            employee_id=employee["employee_id"],
            new_password=new_password,
        )

        if result:

            st.success(
                "Account activated successfully. "
                "Please log in with your new password."
            )

            st.session_state.pop(
                "activation_employee",
                None,
            )

            st.session_state.auth_mode = (
                "employee_login"
            )

            st.rerun()

        else:

            st.error(
                "Account activation failed. "
                "Please contact the administrator."
            )

    if st.button(
        "← Back to Login",
        key="activation_back",
    ):

        st.session_state.pop(
            "activation_employee",
            None,
        )

        st.session_state.auth_mode = (
            "employee_login"
        )

        st.rerun()


# ============================================================
# AUTH ROUTER
# ============================================================

def render_auth_ui():

    if "auth_mode" not in st.session_state:

        st.session_state.auth_mode = (
            "role_selection"
        )

    mode = st.session_state.auth_mode

    if mode == "role_selection":

        render_authentication()

    elif mode == "admin_login":

        render_admin_login()

    elif mode == "employee_login":

        render_employee_login()

    elif mode == "employee_activation":

        render_employee_activation()

    else:

        st.session_state.auth_mode = (
            "role_selection"
        )

        st.rerun()
