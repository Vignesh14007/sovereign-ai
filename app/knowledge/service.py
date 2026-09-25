from pathlib import Path

from app.knowledge.database import (
    get_all_documents,
    get_document,
    get_document_counts,
    update_status,
    delete_document_record,
)

from app.knowledge.processor import process_document


BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = (
    BASE_DIR
    / "data"
    / "knowledge"
    / "documents"
)

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "knowledge"
    / "chunks"
    / "knowledge_chunks.jsonl"
)


def upload_document(
    file_path,
    category,
    department=None,
    equipment=None,
    description=None,
    uploaded_by="admin",
    version="1.0",
):
    """
    Process and register an admin-uploaded document.
    """

    return process_document(
        source_path=file_path,
        category=category,
        department=department,
        equipment=equipment,
        description=description,
        uploaded_by=uploaded_by,
        version=version,
    )


def list_documents(include_archived=True):
    """
    Return documents stored in the knowledge-base metadata DB.
    """

    return get_all_documents(
        include_archived=include_archived
    )


def get_document_details(document_id):
    """
    Return one document's metadata.
    """

    return get_document(document_id)


def get_dashboard_stats():
    """
    Return statistics for the Admin Dashboard.
    """

    return get_document_counts()


def archive_document(document_id):
    """
    Archive a document without deleting its history.

    Archived documents remain in the metadata database.
    """

    document = get_document(document_id)

    if document is None:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    update_status(
        document_id=document_id,
        status="archived",
    )

    return get_document(document_id)


def activate_document(document_id):
    """
    Reactivate an archived document.
    """

    document = get_document(document_id)

    if document is None:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    update_status(
        document_id=document_id,
        status="active",
    )

    return get_document(document_id)


def delete_document(document_id):
    """
    Permanently remove a document from the local
    knowledge-base storage.

    This removes:
        1. Metadata record
        2. Stored original document
        3. Its chunks

    Use archive_document() when historical retention
    is preferred.
    """

    document = get_document(document_id)

    if document is None:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    # ---------------------------------------------------------
    # Remove physical document storage
    # ---------------------------------------------------------

    document_folder = (
        DOCUMENTS_DIR / document_id
    )

    if document_folder.exists():

        for path in document_folder.rglob("*"):

            if path.is_file():
                path.unlink()

        # Remove empty directories.
        for path in sorted(
            document_folder.rglob("*"),
            reverse=True,
        ):

            if path.is_dir():
                path.rmdir()

        document_folder.rmdir()

    # ---------------------------------------------------------
    # Remove document chunks
    # ---------------------------------------------------------

    if CHUNKS_FILE.exists():

        temporary_file = (
            CHUNKS_FILE.with_suffix(".tmp")
        )

        with (
            CHUNKS_FILE.open(
                "r",
                encoding="utf-8",
            ) as source,
            temporary_file.open(
                "w",
                encoding="utf-8",
            ) as destination,
        ):

            for line in source:

                if (
                    f'"document_id": "{document_id}"'
                    not in line
                ):
                    destination.write(line)

        temporary_file.replace(CHUNKS_FILE)

    # ---------------------------------------------------------
    # Remove metadata
    # ---------------------------------------------------------

    delete_document_record(
        document_id
    )

    return {
        "success": True,
        "document_id": document_id,
        "message": "Document permanently deleted.",
    }
