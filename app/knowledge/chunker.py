import re
from typing import List


DEFAULT_CHUNK_SIZE = 1800
DEFAULT_OVERLAP = 250


def clean_text(text: str) -> str:
    """
    Normalize extracted document text while preserving useful content.
    """

    if not text:
        return ""

    # Normalize line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces and tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_paragraphs(text: str) -> List[str]:
    """
    Split normalized text into meaningful paragraphs.
    """

    paragraphs = re.split(r"\n\s*\n", text)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> List[str]:
    """
    Split a document into overlapping text chunks.

    The chunker is intentionally generic so it can process
    company documents uploaded through the Admin Panel.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = clean_text(text)

    if not text:
        return []

    paragraphs = split_into_paragraphs(text)

    chunks = []

    current_parts = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        # Very large paragraph: split it directly.
        if paragraph_length > chunk_size:

            if current_parts:
                chunks.append("\n\n".join(current_parts))
                current_parts = []
                current_length = 0

            start = 0

            while start < paragraph_length:

                end = min(start + chunk_size, paragraph_length)

                piece = paragraph[start:end].strip()

                if piece:
                    chunks.append(piece)

                if end >= paragraph_length:
                    break

                start = end - overlap

            continue

        # Start a new chunk when adding this paragraph
        # would exceed the target size.
        if (
            current_parts
            and current_length + paragraph_length + 2 > chunk_size
        ):

            chunk = "\n\n".join(current_parts).strip()

            if chunk:
                chunks.append(chunk)

            # Preserve a small amount of context from the
            # previous chunk.
            overlap_parts = []
            overlap_length = 0

            for previous in reversed(current_parts):

                additional_length = len(previous) + (
                    2 if overlap_parts else 0
                )

                if overlap_length + additional_length > overlap:
                    break

                overlap_parts.insert(0, previous)
                overlap_length += additional_length

            current_parts = overlap_parts
            current_length = overlap_length

        current_parts.append(paragraph)

        current_length += paragraph_length

        if len(current_parts) > 1:
            current_length += 2

    # Add the final chunk.
    if current_parts:

        chunk = "\n\n".join(current_parts).strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def chunk_document(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> List[dict]:
    """
    Create structured chunks ready for the knowledge base.

    Each chunk contains:
        chunk_index
        text
        character_count
    """

    chunks = chunk_text(
        text=text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    return [
        {
            "chunk_index": index,
            "text": chunk,
            "character_count": len(chunk),
        }
        for index, chunk in enumerate(chunks)
    ]
