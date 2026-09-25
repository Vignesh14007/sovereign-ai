import sqlite3
from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
DATABASE_PATH = KNOWLEDGE_DIR / "metadata.db"


def get_connection():
    """
    Create a connection to the local knowledge-base metadata database.
    """
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the documents table if it does not already exist.
    """
    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                document_id TEXT UNIQUE NOT NULL,

                name TEXT NOT NULL,
                original_filename TEXT NOT NULL,

                category TEXT NOT NULL,
                department TEXT,

                equipment TEXT,
                description TEXT,

                version TEXT NOT NULL DEFAULT '1.0',

                status TEXT NOT NULL DEFAULT 'active',

                file_path TEXT NOT NULL,

                file_type TEXT,

                file_size INTEGER,

                chunk_count INTEGER DEFAULT 0,

                uploaded_by TEXT NOT NULL DEFAULT 'admin',

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def create_document(
    document_id,
    name,
    original_filename,
    category,
    department=None,
    equipment=None,
    description=None,
    version="1.0",
    status="active",
    file_path="",
    file_type=None,
    file_size=None,
    uploaded_by="admin",
):
    """
    Add a new document record to the knowledge-base database.
    """

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO documents (
                document_id,
                name,
                original_filename,
                category,
                department,
                equipment,
                description,
                version,
                status,
                file_path,
                file_type,
                file_size,
                chunk_count,
                uploaded_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                document_id,
                name,
                original_filename,
                category,
                department,
                equipment,
                description,
                version,
                status,
                file_path,
                file_type,
                file_size,
                0,
                uploaded_by,
                now,
                now,
            ),
        )

        connection.commit()


def update_chunk_count(document_id, chunk_count):
    """
    Store the number of chunks generated from a document.
    """

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE documents
            SET chunk_count = ?,
                updated_at = ?
            WHERE document_id = ?
            """,
            (
                chunk_count,
                now,
                document_id,
            ),
        )

        connection.commit()


def update_status(document_id, status):
    """
    Change the document lifecycle status.

    Supported statuses:
    active
    archived
    processing
    failed
    """

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE documents
            SET status = ?,
                updated_at = ?
            WHERE document_id = ?
            """,
            (
                status,
                now,
                document_id,
            ),
        )

        connection.commit()


def get_document(document_id):
    """
    Retrieve one document by its document ID.
    """

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM documents
            WHERE document_id = ?
            """,
            (document_id,),
        ).fetchone()

    return dict(row) if row else None


def get_all_documents(include_archived=True):
    """
    Retrieve document records.

    By default, archived documents are included so the admin
    can maintain document history.
    """

    with get_connection() as connection:

        if include_archived:

            rows = connection.execute(
                """
                SELECT *
                FROM documents
                ORDER BY updated_at DESC
                """
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT *
                FROM documents
                WHERE status != 'archived'
                ORDER BY updated_at DESC
                """
            ).fetchall()

    return [dict(row) for row in rows]


def delete_document_record(document_id):
    """
    Permanently remove the metadata record.

    This function only removes the database record.
    The physical file should be handled separately.
    """

    with get_connection() as connection:

        connection.execute(
            """
            DELETE FROM documents
            WHERE document_id = ?
            """,
            (document_id,),
        )

        connection.commit()


def get_document_counts():
    """
    Return useful dashboard statistics.
    """

    with get_connection() as connection:

        total = connection.execute(
            """
            SELECT COUNT(*)
            FROM documents
            """
        ).fetchone()[0]

        active = connection.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE status = 'active'
            """
        ).fetchone()[0]

        archived = connection.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE status = 'archived'
            """
        ).fetchone()[0]

        processing = connection.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE status = 'processing'
            """
        ).fetchone()[0]

        failed = connection.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE status = 'failed'
            """
        ).fetchone()[0]

    return {
        "total": total,
        "active": active,
        "archived": archived,
        "processing": processing,
        "failed": failed,
    }


# Initialize the database when this module is first used.
initialize_database()
