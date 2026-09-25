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
# CONNECTION
# ============================================================

def get_history_connection():
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
# INITIALIZE HISTORY TABLE
# ============================================================

def initialize_history_table():

    with get_history_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS employee_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                employee_id TEXT NOT NULL,

                request TEXT NOT NULL,

                task_type TEXT,

                response TEXT,

                source_documents TEXT,

                execution_status TEXT NOT NULL DEFAULT 'completed',

                artifact_path TEXT,

                created_at TEXT NOT NULL

            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_employee_history_employee_id
            ON employee_history(employee_id)
            """
        )

        connection.commit()


# ============================================================
# CREATE HISTORY RECORD
# ============================================================

def create_history_record(
    employee_id,
    request,
    task_type=None,
    response=None,
    source_documents=None,
    execution_status="completed",
    artifact_path=None,
):
    """
    Store one employee's AI activity.

    Every record is tied to an employee_id so the application
    can retrieve only that employee's history.
    """

    now = datetime.now(
        timezone.utc
    ).isoformat()

    with get_history_connection() as connection:

        connection.execute(
            """
            INSERT INTO employee_history (
                employee_id,
                request,
                task_type,
                response,
                source_documents,
                execution_status,
                artifact_path,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                request,
                task_type,
                response,
                source_documents,
                execution_status,
                artifact_path,
                now,
            ),
        )

        connection.commit()


# ============================================================
# GET EMPLOYEE HISTORY
# ============================================================

def get_employee_history(
    employee_id,
    limit=50,
):
    """
    Return history belonging ONLY to the specified employee.

    This employee_id filter is important for preventing one
    employee from receiving another employee's history.
    """

    with get_history_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM employee_history
            WHERE employee_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (
                employee_id,
                limit,
            ),
        ).fetchall()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# GET SINGLE HISTORY RECORD
# ============================================================

def get_history_record(
    history_id,
    employee_id,
):
    """
    Retrieve a history record only when it belongs to the
    authenticated employee.
    """

    with get_history_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM employee_history
            WHERE id = ?
              AND employee_id = ?
            """,
            (
                history_id,
                employee_id,
            ),
        ).fetchone()

    return dict(row) if row else None


# ============================================================
# HISTORY COUNT
# ============================================================

def get_employee_history_count(
    employee_id,
):

    with get_history_connection() as connection:

        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM employee_history
            WHERE employee_id = ?
            """,
            (
                employee_id,
            ),
        ).fetchone()[0]

    return count


# ============================================================
# INITIALIZE
# ============================================================

initialize_history_table()
