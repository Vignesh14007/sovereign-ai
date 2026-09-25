import bcrypt

from app.auth.database import (
    create_admin,
    create_employee,
    get_admin_by_email,
    get_admin_by_id,
    get_employee_by_email,
    get_employee_by_id,
    update_admin_last_login,
    update_employee_last_login,
    update_employee_password,
)


# ============================================================
# PASSWORD SECURITY
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Plain-text passwords are never stored in the database.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    password_bytes = password.encode("utf-8")

    password_hash = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return password_hash.decode("utf-8")


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.
    """

    if not password or not password_hash:
        return False

    try:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    except (ValueError, TypeError):

        return False


# ============================================================
# ADMIN ACCOUNT
# ============================================================

def register_admin(
    admin_id: str,
    name: str,
    email: str,
    password: str,
):
    """
    Create an administrator account.
    """

    if not admin_id.strip():
        raise ValueError("Admin ID is required.")

    if not name.strip():
        raise ValueError("Admin name is required.")

    if not email.strip():
        raise ValueError("Admin email is required.")

    if len(password) < 8:
        raise ValueError(
            "Admin password must contain at least 8 characters."
        )

    existing_admin = get_admin_by_email(
        email.strip().lower()
    )

    if existing_admin:
        raise ValueError(
            "An administrator with this email already exists."
        )

    password_hash = hash_password(
        password
    )

    create_admin(
        admin_id=admin_id.strip(),
        name=name.strip(),
        email=email.strip().lower(),
        password_hash=password_hash,
    )

    return {
        "success": True,
        "admin_id": admin_id.strip(),
        "email": email.strip().lower(),
    }


# ============================================================
# ADMIN LOGIN
# ============================================================

def authenticate_admin(
    email: str,
    password: str,
):
    """
    Authenticate an administrator.

    Returns the authenticated admin record without exposing
    the password hash to the application session.
    """

    admin = get_admin_by_email(
        email.strip().lower()
    )

    if not admin:
        return None

    if admin["status"] != "active":
        return None

    if not verify_password(
        password,
        admin["password_hash"],
    ):
        return None

    update_admin_last_login(
        admin["admin_id"]
    )

    admin.pop(
        "password_hash",
        None,
    )

    return admin


# ============================================================
# EMPLOYEE ACCOUNT
# ============================================================

def register_employee(
    employee_id: str,
    name: str,
    email: str,
    department=None,
    designation=None,
    created_by=None,
    permission_ai=1,
    permission_documents=0,
    permission_reports=0,
    permission_code_execution=0,
    permission_sensitive_documents=0,
):
    """
    Create an employee account.

    Employees start in pending state and must complete their
    first-time activation before normal access.
    """

    if not employee_id.strip():
        raise ValueError(
            "Employee ID is required."
        )

    if not name.strip():
        raise ValueError(
            "Employee name is required."
        )

    if not email.strip():
        raise ValueError(
            "Employee email is required."
        )

    existing_employee = get_employee_by_email(
        email.strip().lower()
    )

    if existing_employee:
        raise ValueError(
            "An employee with this email already exists."
        )

    create_employee(
        employee_id=employee_id.strip(),
        name=name.strip(),
        email=email.strip().lower(),
        department=(
            department.strip()
            if department
            else None
        ),
        designation=(
            designation.strip()
            if designation
            else None
        ),
        created_by=created_by,
        permission_ai=int(permission_ai),
        permission_documents=int(permission_documents),
        permission_reports=int(permission_reports),
        permission_code_execution=int(
            permission_code_execution
        ),
        permission_sensitive_documents=int(
            permission_sensitive_documents
        ),
    )

    return {
        "success": True,
        "employee_id": employee_id.strip(),
        "email": email.strip().lower(),
        "status": "pending",
        "first_login": True,
    }


# ============================================================
# EMPLOYEE LOOKUP
# ============================================================

def get_employee_account(
    employee_id: str,
):
    """
    Return an employee account without exposing the password hash.
    """

    employee = get_employee_by_id(
        employee_id.strip()
    )

    if not employee:
        return None

    employee.pop(
        "password_hash",
        None,
    )

    return employee


# ============================================================
# FIRST-TIME EMPLOYEE ACTIVATION
# ============================================================

def activate_employee_first_login(
    employee_id: str,
    new_password: str,
):
    """
    Set the employee's first password.

    The employee becomes active only after completing
    first-time password setup.
    """

    if len(new_password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    employee = get_employee_by_id(
        employee_id.strip()
    )

    if not employee:
        raise ValueError(
            "Employee account not found."
        )

    if employee["status"] != "pending":
        raise ValueError(
            "This employee account is not awaiting activation."
        )

    if not employee["first_login"]:
        raise ValueError(
            "First-time activation has already been completed."
        )

    password_hash = hash_password(
        new_password
    )

    update_employee_password(
        employee_id=employee_id.strip(),
        password_hash=password_hash,
    )

    return {
        "success": True,
        "employee_id": employee_id.strip(),
        "status": "active",
        "first_login": False,
    }


# ============================================================
# EMPLOYEE LOGIN
# ============================================================

def authenticate_employee(
    email: str,
    password: str,
):
    """
    Authenticate an employee.

    Pending first-time accounts are returned with a special
    activation state instead of being logged in normally.
    """

    employee = get_employee_by_email(
        email.strip().lower()
    )

    if not employee:
        return None

    if employee["status"] == "pending":

        return {
            "requires_activation": True,
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "email": employee["email"],
        }

    if employee["status"] != "active":
        return None

    if not verify_password(
        password,
        employee["password_hash"],
    ):
        return None

    update_employee_last_login(
        employee["employee_id"]
    )

    employee.pop(
        "password_hash",
        None,
    )

    employee["requires_activation"] = False

    return employee


# ============================================================
# PERMISSION CHECK
# ============================================================

def has_permission(
    employee: dict,
    permission: str,
) -> bool:
    """
    Check whether an authenticated employee has a specific
    permission.
    """

    permission_map = {
        "ai": "permission_ai",
        "documents": "permission_documents",
        "reports": "permission_reports",
        "code_execution": "permission_code_execution",
        "sensitive_documents": (
            "permission_sensitive_documents"
        ),
    }

    field = permission_map.get(
        permission
    )

    if field is None:
        return False

    return bool(
        employee.get(field, 0)
    )
