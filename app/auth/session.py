import streamlit as st


# ============================================================
# SESSION INITIALIZATION
# ============================================================

def initialize_session():

    defaults = {
        "authenticated": False,
        "user_role": None,
        "user_id": None,
        "user_name": None,
        "user_email": None,
        "permissions": {},
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# LOGIN
# ============================================================

def login_user(
    user,
    role,
):
    """
    Store only the authenticated user's safe session data.

    Password hashes are never stored in Streamlit session state.
    """

    initialize_session()

    st.session_state.authenticated = True
    st.session_state.user_role = role
    st.session_state.user_id = (
        user.get("admin_id")
        or user.get("employee_id")
    )
    st.session_state.user_name = user.get(
        "name"
    )
    st.session_state.user_email = user.get(
        "email"
    )

    if role == "employee":

        st.session_state.permissions = {
            "ai": bool(
                user.get(
                    "permission_ai",
                    0,
                )
            ),
            "documents": bool(
                user.get(
                    "permission_documents",
                    0,
                )
            ),
            "reports": bool(
                user.get(
                    "permission_reports",
                    0,
                )
            ),
            "code_execution": bool(
                user.get(
                    "permission_code_execution",
                    0,
                )
            ),
            "sensitive_documents": bool(
                user.get(
                    "permission_sensitive_documents",
                    0,
                )
            ),
        }

    else:

        st.session_state.permissions = {
            "admin": True,
            "ai": True,
            "documents": True,
            "reports": True,
            "code_execution": True,
            "sensitive_documents": True,
        }


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    keys_to_clear = [
        "authenticated",
        "user_role",
        "user_id",
        "user_name",
        "user_email",
        "permissions",
    ]

    for key in keys_to_clear:

        if key in st.session_state:
            del st.session_state[key]

    initialize_session()


# ============================================================
# AUTHENTICATION CHECK
# ============================================================

def is_authenticated():

    initialize_session()

    return bool(
        st.session_state.authenticated
    )


# ============================================================
# ROLE CHECK
# ============================================================

def get_user_role():

    initialize_session()

    return st.session_state.user_role


def is_admin():

    return (
        is_authenticated()
        and get_user_role() == "admin"
    )


def is_employee():

    return (
        is_authenticated()
        and get_user_role() == "employee"
    )


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():

    initialize_session()

    return {
        "id": st.session_state.user_id,
        "name": st.session_state.user_name,
        "email": st.session_state.user_email,
        "role": st.session_state.user_role,
    }


# ============================================================
# PERMISSION CHECK
# ============================================================

def has_permission(
    permission,
):

    initialize_session()

    return bool(
        st.session_state.permissions.get(
            permission,
            False,
        )
    )
