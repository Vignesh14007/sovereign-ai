import sqlite3
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

AUTH_DIR = BASE_DIR / "data" / "auth"

DATABASE_PATH = AUTH_DIR / "auth.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite connection.

    The database is stored locally inside the project so
    authentication data does not depend on an external service.
    """

    AUTH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():
    """
    Create authentication tables if they do not already exist.
    """

    with get_connection() as connection:

        # ----------------------------------------------------
        # ADMIN TABLE
        # ----------------------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                admin_id TEXT UNIQUE NOT NULL,

                name TEXT NOT NULL,

                email TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'admin',

                status TEXT NOT NULL DEFAULT 'active',

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL,

                last_login TEXT

            )
            """
        )


        # ----------------------------------------------------
        # EMPLOYEE TABLE
        # ----------------------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                employee_id TEXT UNIQUE NOT NULL,

                name TEXT NOT NULL,

                email TEXT UNIQUE NOT NULL,

                department TEXT,

                designation TEXT,

                password_hash TEXT,

                status TEXT NOT NULL DEFAULT 'pending',

                first_login INTEGER NOT NULL DEFAULT 1,

                permission_ai INTEGER NOT NULL DEFAULT 1,

                permission_documents INTEGER NOT NULL DEFAULT 0,

                permission_reports INTEGER NOT NULL DEFAULT 0,

                permission_code_execution INTEGER NOT NULL DEFAULT 0,

                permission_sensitive_documents INTEGER NOT NULL DEFAULT 0,

                created_by TEXT,

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL,

                last_login TEXT

            )
            """
        )


        connection.commit()


# ============================================================
# ADMIN OPERATIONS
# ============================================================

def create_admin(
    admin_id,
    name,
    email,
    password_hash,
):
    """
    Create a new administrator account.
    """

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO admins (
                admin_id,
                name,
                email,
                password_hash,
                role,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                admin_id,
                name,
                email,
                password_hash,
                "admin",
                "active",
                now,
                now,
            ),
        )

        connection.commit()


def get_admin_by_email(email):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM admins
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    return dict(row) if row else None


def get_admin_by_id(admin_id):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM admins
            WHERE admin_id = ?
            """,
            (admin_id,),
        ).fetchone()

    return dict(row) if row else None


def update_admin_last_login(admin_id):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE admins
            SET last_login = ?,
                updated_at = ?
            WHERE admin_id = ?
            """,
            (
                now,
                now,
                admin_id,
            ),
        )

        connection.commit()


# ============================================================
# EMPLOYEE OPERATIONS
# ============================================================

def create_employee(
    employee_id,
    name,
    email,
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
    Create a new employee account.

    New employees start in PENDING status and must complete
    first-time activation before normal access.
    """

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO employees (
                employee_id,
                name,
                email,
                department,
                designation,
                status,
                first_login,
                permission_ai,
                permission_documents,
                permission_reports,
                permission_code_execution,
                permission_sensitive_documents,
                created_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                name,
                email,
                department,
                designation,
                "pending",
                1,
                permission_ai,
                permission_documents,
                permission_reports,
                permission_code_execution,
                permission_sensitive_documents,
                created_by,
                now,
                now,
            ),
        )

        connection.commit()


def get_employee_by_email(email):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM employees
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    return dict(row) if row else None


def get_employee_by_id(employee_id):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM employees
            WHERE employee_id = ?
            """,
            (employee_id,),
        ).fetchone()

    return dict(row) if row else None


def get_all_employees():

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM employees
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


def update_employee_status(
    employee_id,
    status,
):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE employees
            SET status = ?,
                updated_at = ?
            WHERE employee_id = ?
            """,
            (
                status,
                now,
                employee_id,
            ),
        )

        connection.commit()


def update_employee_password(
    employee_id,
    password_hash,
):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE employees
            SET password_hash = ?,
                first_login = 0,
                status = 'active',
                updated_at = ?
            WHERE employee_id = ?
            """,
            (
                password_hash,
                now,
                employee_id,
            ),
        )

        connection.commit()


def update_employee_last_login(
    employee_id,
):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE employees
            SET last_login = ?,
                updated_at = ?
            WHERE employee_id = ?
            """,
            (
                now,
                now,
                employee_id,
            ),
        )

        connection.commit()


def update_employee_permissions(
    employee_id,
    permission_ai,
    permission_documents,
    permission_reports,
    permission_code_execution,
    permission_sensitive_documents,
):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE employees
            SET
                permission_ai = ?,
                permission_documents = ?,
                permission_reports = ?,
                permission_code_execution = ?,
                permission_sensitive_documents = ?,
                updated_at = ?
            WHERE employee_id = ?
            """,
            (
                permission_ai,
                permission_documents,
                permission_reports,
                permission_code_execution,
                permission_sensitive_documents,
                now,
                employee_id,
            ),
        )

        connection.commit()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()
