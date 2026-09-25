import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

from app.knowledge.ingestion import extract_text, get_file_metadata
from app.knowledge.chunker import chunk_document
from app.knowledge.database import (
    create_document,
    update_chunk_count,
    update_status,
)


BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = BASE_DIR / "data" / "knowledge" / "documents"
CHUNKS_DIR = BASE_DIR / "data" / "knowledge" / "chunks"

CHUNKS_FILE = CHUNKS_DIR / "knowledge_chunks.jsonl"


def generate_document_id() -> str:
    """
    Generate a unique knowledge-base document ID.
    """

    return f"DOC-{uuid.uuid4().hex[:8].upper()}"


def save_chunks(document_id: str, chunks: list[dict]) -> int:
    """
    Append processed document chunks to the knowledge-base
    JSONL file.
    """

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()

    with CHUNKS_FILE.open("a", encoding="utf-8") as file:

        for chunk in chunks:

            record = {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "character_count": chunk["character_count"],
                "created_at": now,
            }

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    return len(chunks)


def process_document(
    source_path: str | Path,
    category: str,
    department: str | None = None,
    equipment: str | None = None,
    description: str | None = None,
    uploaded_by: str = "admin",
    version: str = "1.0",
) -> dict:
    """
    Process one company document and add it to the
    local knowledge base.

    Pipeline:

        Source file
            ↓
        Copy into knowledge storage
            ↓
        Extract text
            ↓
        Chunk text
            ↓
        Store chunks
            ↓
        Create metadata record
    """

    source_path = Path(source_path)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source document not found: {source_path}"
        )

    metadata = get_file_metadata(source_path)

    document_id = generate_document_id()

    document_folder = DOCUMENTS_DIR / document_id

    document_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination_path = document_folder / source_path.name

    # Copy the original document into the controlled
    # knowledge-base storage.
    destination_path.write_bytes(
        source_path.read_bytes()
    )

    create_document(
        document_id=document_id,
        name=source_path.stem,
        original_filename=source_path.name,
        category=category,
        department=department,
        equipment=equipment,
        description=description,
        version=version,
        status="processing",
        file_path=str(destination_path),
        file_type=metadata["extension"],
        file_size=metadata["size"],
        uploaded_by=uploaded_by,
    )

    try:

        # Extract document text.
        text = extract_text(destination_path)

        # Convert the extracted text into searchable chunks.
        chunks = chunk_document(text)

        if not chunks:
            raise ValueError(
                "Document produced no usable text chunks."
            )

        # Store chunks.
        chunk_count = save_chunks(
            document_id=document_id,
            chunks=chunks,
        )

        # Update metadata with successful processing.
        update_chunk_count(
            document_id=document_id,
            chunk_count=chunk_count,
        )

        update_status(
            document_id=document_id,
            status="active",
        )

        return {
            "success": True,
            "document_id": document_id,
            "name": source_path.stem,
            "filename": source_path.name,
            "category": category,
            "chunk_count": chunk_count,
            "file_path": str(destination_path),
        }

    except Exception:

        update_status(
            document_id=document_id,
            status="failed",
        )

        raise
